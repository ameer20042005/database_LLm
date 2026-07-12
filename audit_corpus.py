"""Phase 1: audit and clean the existing v4 corpus.

Input: data/iraqi_train_v4_part0{1,2,3}.jsonl + data/iraqi_val_v4.jsonl
(~174K records, free-form sales dialogue, no system-prompt/catalog grounding).

Pipeline:
  1. placeholder detection            -> flagged_placeholders.jsonl, dropped
  2. exact-duplicate removal          (normalized-text hash)
  3. near-duplicate removal           (MinHash/LSH, Jaccard >= 0.9)
  4. train/val leakage verification   (post-dedup, should already be zero by
                                        construction since dedup runs over the
                                        combined train+val set with train
                                        inserted first; re-verified explicitly)
  5. corruption detection             (mixed-script mid-word, >80-token
                                        assistant turns) -> flagged, dropped
  6. grounding-risk classification    -> v4_price_bearing_excluded.jsonl vs
                                        v4_dialect_kept.jsonl (the latter is
                                        what generate_v5.py actually folds in,
                                        per the "facts live in the system
                                        prompt, not the weights" architecture:
                                        v4 has no system/catalog turn, so any
                                        assistant reply stating a concrete
                                        price would just re-teach memorized
                                        pricing if trained as-is)
  7. audit_report.md                  stats before/after each stage

Run:
    python audit_corpus.py --seed 42
"""
import argparse
import glob
import hashlib
import json
import re
import sys
from collections import Counter
from pathlib import Path

from datasketch import MinHash, MinHashLSH

import text_checks as tc

ROOT = Path(__file__).parent
DATA_DIR = ROOT / "data"
OUT_DIR = DATA_DIR / "v5"

DEFAULT_TRAIN_GLOB = str(DATA_DIR / "iraqi_train_v4_part*.jsonl")
DEFAULT_VAL_PATH = str(DATA_DIR / "iraqi_val_v4.jsonl")

PRICE_RE = re.compile(r'\d[\d,]*\s*(?:دينار|الف|ألف)')
MAX_ASSISTANT_TOKENS = 80


def load_jsonl(path):
    records = []
    with open(path, encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if line:
                records.append(json.loads(line))
    return records


def write_jsonl(path, records):
    path.parent.mkdir(parents=True, exist_ok=True)
    with open(path, "w", encoding="utf-8") as f:
        for r in records:
            f.write(json.dumps(r, ensure_ascii=False) + "\n")


def record_text(rec):
    return " ".join(m.get("content", "") for m in rec.get("messages", []))


def norm_hash(rec):
    return hashlib.sha1(tc.normalize_arabic(record_text(rec)).encode("utf-8")).hexdigest()


def build_minhash(rec, num_perm, seed):
    m = MinHash(num_perm=num_perm, seed=seed)
    for sh in tc.shingles(record_text(rec), k=3):
        m.update(sh.encode("utf-8"))
    return m


def find_near_duplicates(records, threshold=0.9, num_perm=128, seed=1, progress_every=20000):
    """Streaming near-dup removal: insert in order, drop anything that already
    matches an earlier-inserted representative. Returns (keep_indices, drop_indices).
    Reused as-is by generate_v5.py to re-check the final train/val split."""
    lsh = MinHashLSH(threshold=threshold, num_perm=num_perm)
    keep, drop = [], []
    for i, rec in enumerate(records):
        mh = build_minhash(rec, num_perm, seed)
        if lsh.query(mh):
            drop.append(i)
        else:
            lsh.insert(str(i), mh)
            keep.append(i)
        if progress_every and (i + 1) % progress_every == 0:
            print(f"  near-dup scan: {i + 1}/{len(records)}", file=sys.stderr)
    return keep, drop


def verify_no_leakage(train_records, val_records, threshold=0.9, num_perm=128, seed=1):
    """Build LSH from train only, query every val record against it. Returns
    list of val indices that collide with a train record (exact or near-dup)."""
    lsh = MinHashLSH(threshold=threshold, num_perm=num_perm)
    train_hashes = set()
    for rec in train_records:
        train_hashes.add(norm_hash(rec))
        lsh.insert(rec["id"], build_minhash(rec, num_perm, seed))

    leaked = []
    for i, rec in enumerate(val_records):
        if norm_hash(rec) in train_hashes:
            leaked.append(i)
            continue
        if lsh.query(build_minhash(rec, num_perm, seed)):
            leaked.append(i)
    return leaked


def token_len_histogram(records, role="assistant"):
    buckets = Counter()
    for rec in records:
        for m in rec.get("messages", []):
            if m.get("role") != role:
                continue
            n = tc.count_tokens(m.get("content", ""))
            if n <= 10:
                buckets["0-10"] += 1
            elif n <= 20:
                buckets["11-20"] += 1
            elif n <= 40:
                buckets["21-40"] += 1
            elif n <= 80:
                buckets["41-80"] += 1
            else:
                buckets["81+"] += 1
    return buckets


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--seed", type=int, default=42)
    ap.add_argument("--train-glob", default=DEFAULT_TRAIN_GLOB)
    ap.add_argument("--val-path", default=DEFAULT_VAL_PATH)
    ap.add_argument("--out-dir", default=str(OUT_DIR))
    ap.add_argument("--minhash-threshold", type=float, default=0.9)
    ap.add_argument("--num-perm", type=int, default=128)
    args = ap.parse_args()

    out_dir = Path(args.out_dir)
    out_dir.mkdir(parents=True, exist_ok=True)

    train_paths = sorted(glob.glob(args.train_glob))
    if not train_paths:
        raise SystemExit(f"no train files matched glob: {args.train_glob}")
    print(f"loading {len(train_paths)} train shard(s) + 1 val file...")
    train_records = [r for p in train_paths for r in load_jsonl(p)]
    val_records = load_jsonl(args.val_path)
    n_train_raw, n_val_raw = len(train_records), len(val_records)
    print(f"raw: train={n_train_raw} val={n_val_raw} total={n_train_raw + n_val_raw}")

    report = {
        "raw_train": n_train_raw,
        "raw_val": n_val_raw,
    }

    # ---- 1. placeholder detection ----
    flagged_placeholders = []

    def has_placeholder(rec):
        for m in rec.get("messages", []):
            found = tc.find_placeholders(m.get("content", ""))
            if found:
                return found
        return None

    def filter_placeholders(records, split):
        kept, flagged = [], []
        for rec in records:
            found = has_placeholder(rec)
            if found:
                flagged.append({**rec, "_split": split, "_flagged_placeholders": found})
            else:
                kept.append(rec)
        return kept, flagged

    train_records, flg_t = filter_placeholders(train_records, "train")
    val_records, flg_v = filter_placeholders(val_records, "val")
    flagged_placeholders = flg_t + flg_v
    write_jsonl(out_dir / "flagged_placeholders.jsonl", flagged_placeholders)
    report["placeholder_removed"] = len(flagged_placeholders)
    print(f"placeholders: removed {len(flagged_placeholders)} (train {len(flg_t)}, val {len(flg_v)})")

    # ---- 2. exact duplicates (train inserted first, so val loses ties) ----
    seen_hashes = set()
    deduped_train, exact_dropped_train = [], 0
    for rec in train_records:
        h = norm_hash(rec)
        if h in seen_hashes:
            exact_dropped_train += 1
            continue
        seen_hashes.add(h)
        deduped_train.append(rec)

    deduped_val, exact_dropped_val = [], 0
    for rec in val_records:
        h = norm_hash(rec)
        if h in seen_hashes:
            exact_dropped_val += 1
            continue
        seen_hashes.add(h)
        deduped_val.append(rec)

    train_records, val_records = deduped_train, deduped_val
    report["exact_dup_removed_train"] = exact_dropped_train
    report["exact_dup_removed_val"] = exact_dropped_val
    print(f"exact dups removed: train={exact_dropped_train} val={exact_dropped_val}")

    # ---- 3. near duplicates (MinHash/LSH, combined so cross-split dups drop too) ----
    combined = train_records + val_records
    split_at = len(train_records)
    print("scanning near-duplicates (MinHash/LSH)...")
    keep_idx, drop_idx = find_near_duplicates(
        combined, threshold=args.minhash_threshold, num_perm=args.num_perm, seed=args.seed
    )
    keep_set = set(keep_idx)
    new_train = [combined[i] for i in range(split_at) if i in keep_set]
    new_val = [combined[i] for i in range(split_at, len(combined)) if i in keep_set]
    report["near_dup_removed"] = len(drop_idx)
    print(f"near dups removed: {len(drop_idx)} (train {len(train_records) - len(new_train)}, "
          f"val {len(val_records) - len(new_val)})")
    train_records, val_records = new_train, new_val

    # ---- 4. train/val leakage verification (post-dedup) ----
    print("verifying zero train/val leakage...")
    leaked_val_idx = verify_no_leakage(
        train_records, val_records, threshold=args.minhash_threshold, num_perm=args.num_perm, seed=args.seed
    )
    if leaked_val_idx:
        leaked_set = set(leaked_val_idx)
        val_records = [r for i, r in enumerate(val_records) if i not in leaked_set]
    report["leakage_val_dropped"] = len(leaked_val_idx)
    print(f"leakage check: {len(leaked_val_idx)} val record(s) still overlapped train -> dropped")

    # ---- 5. corruption detection ----
    def is_corrupted(rec):
        for m in rec.get("messages", []):
            content = m.get("content", "")
            if tc.has_corrupted_mixed_script(content):
                return "mixed_script"
            if m.get("role") == "assistant" and tc.count_tokens(content) > MAX_ASSISTANT_TOKENS:
                return "assistant_too_long"
        return None

    flagged_corrupt = []

    def filter_corrupt(records, split):
        kept = []
        for rec in records:
            reason = is_corrupted(rec)
            if reason:
                flagged_corrupt.append({**rec, "_split": split, "_reason": reason})
            else:
                kept.append(rec)
        return kept

    train_records = filter_corrupt(train_records, "train")
    val_records = filter_corrupt(val_records, "val")
    write_jsonl(out_dir / "flagged_corrupted.jsonl", flagged_corrupt)
    report["corrupted_removed"] = len(flagged_corrupt)
    print(f"corrupted/oversized removed: {len(flagged_corrupt)}")

    # ---- 6. grounding-risk classification ----
    def is_price_bearing(rec):
        for m in rec.get("messages", []):
            if m.get("role") == "assistant" and PRICE_RE.search(m.get("content", "")):
                return True
        return False

    all_surviving = train_records + val_records
    price_bearing, dialect_kept = [], []
    for rec in all_surviving:
        (price_bearing if is_price_bearing(rec) else dialect_kept).append(rec)

    write_jsonl(out_dir / "v4_price_bearing_excluded.jsonl", price_bearing)
    write_jsonl(out_dir / "v4_dialect_kept.jsonl", dialect_kept)
    report["price_bearing_excluded"] = len(price_bearing)
    report["dialect_kept"] = len(dialect_kept)
    print(f"grounding-risk split: price_bearing_excluded={len(price_bearing)} dialect_kept={len(dialect_kept)}")

    # ---- 7. report ----
    hist_before = token_len_histogram(
        [r for p in train_paths for r in load_jsonl(p)] + load_jsonl(args.val_path)
    )
    hist_after = token_len_histogram(dialect_kept)

    lines = []
    lines.append("# v4 Corpus Audit Report\n")
    lines.append(f"Seed: {args.seed}\n")
    lines.append("## Counts\n")
    lines.append("| Stage | Train | Val | Total |")
    lines.append("|---|---|---|---|")
    lines.append(f"| raw | {n_train_raw} | {n_val_raw} | {n_train_raw + n_val_raw} |")
    lines.append(f"| after placeholder removal ({report['placeholder_removed']} removed) | "
                 f"{n_train_raw - len(flg_t)} | {n_val_raw - len(flg_v)} | "
                 f"{n_train_raw + n_val_raw - report['placeholder_removed']} |")
    lines.append(f"| after exact-dup removal (train {exact_dropped_train}, val {exact_dropped_val} removed) | "
                 f"{len(deduped_train)} | {len(deduped_val)} | {len(deduped_train) + len(deduped_val)} |")
    lines.append(f"| after near-dup removal ({report['near_dup_removed']} removed) | "
                 f"{len(new_train) if leaked_val_idx is not None else ''} | | |")
    lines.append(f"| after leakage fix ({report['leakage_val_dropped']} val records dropped) | "
                 f"{len(train_records)} | {len(val_records)} | {len(train_records) + len(val_records)} |")
    lines.append(f"| after corruption removal ({report['corrupted_removed']} removed) | "
                 f"final surviving = {len(all_surviving) - report['corrupted_removed']} | | |")
    lines.append("")
    lines.append("## Grounding-risk classification (v4 has no system-prompt/catalog grounding)\n")
    lines.append(f"- **Price-bearing, excluded from v5 mix**: {len(price_bearing)} "
                 f"({len(price_bearing) / max(1, len(all_surviving)):.1%}) — assistant turn states a concrete "
                 f"dinar price with no system catalog to ground it; would re-teach memorized/hallucinated pricing.")
    lines.append(f"- **Dialect-kept, folded into v5 mix**: {len(dialect_kept)} "
                 f"({len(dialect_kept) / max(1, len(all_surviving)):.1%}) — daily talk, social, greetings, "
                 f"negotiation phrasing without concrete numbers; contributes dialect diversity only.")
    lines.append("")
    lines.append("## Assistant-turn token-length histogram\n")
    lines.append("| Bucket | Before (raw v4) | After (dialect_kept) |")
    lines.append("|---|---|---|")
    for bucket in ["0-10", "11-20", "21-40", "41-80", "81+"]:
        lines.append(f"| {bucket} | {hist_before.get(bucket, 0)} | {hist_after.get(bucket, 0)} |")
    lines.append("")
    lines.append("## Outputs\n")
    lines.append("- `data/v5/flagged_placeholders.jsonl`")
    lines.append("- `data/v5/flagged_corrupted.jsonl`")
    lines.append("- `data/v5/v4_price_bearing_excluded.jsonl` (excluded from final mix)")
    lines.append("- `data/v5/v4_dialect_kept.jsonl` (folded into final mix by generate_v5.py)")

    (out_dir / "audit_report.md").write_text("\n".join(lines), encoding="utf-8")
    print(f"\nwrote {out_dir / 'audit_report.md'}")
    print(f"final dialect_kept (to be folded into v5 mix): {len(dialect_kept)}")


if __name__ == "__main__":
    main()
