"""v5 dataset orchestrator (Phase 2 entry point).

Builds data/v5/train.jsonl + data/v5/val.jsonl by generating every synthetic
category (A copy, B memory, C reject/resist, D drift, E calc, F greet, plus
the bonus "clarify" ask-before-assuming category and the no-system chat
slice) and folding in the audited/cleaned v4 dialect-only slice produced by
`audit_corpus.py` (run that first - this script warns and skips the v4
fold-in if data/v5/v4_dialect_kept.jsonl doesn't exist yet).

Every category gets its own seed derived deterministically from --seed, so a
full re-run with the same --seed reproduces byte-identical output.

Run:
    python generate_v5.py --seed 42
"""
import argparse
import json
import random
from collections import Counter, defaultdict
from pathlib import Path

import generate_v5_calc_data as calc
import generate_v5_clarify_data as clarify
import generate_v5_drift_data as drift
import generate_v5_greet_data as greet
import generate_v5_grounded_data as grounded
import generate_v5_memory_data as memory
import text_checks as tc
from audit_corpus import find_near_duplicates, verify_no_leakage

ROOT = Path(__file__).parent
DATA_DIR = ROOT / "data"
OUT_DIR = DATA_DIR / "v5"

MAX_SHARD_BYTES = 40 * 1024 * 1024  # ~40 MB/shard, well under GitHub's 100 MB push limit

# target volumes (all --n-<category> overridable). Scaled ~8x the original
# spec suggestions so the final mix (synthetic + audited v4 slice) lands in
# the ~150-200K range, comparable to the original v4-only corpus size.
DEFAULT_COUNTS = {
    "copy": 32000,      # Category A
    "reject": 6400,      # Category C (product/price_floor/offtopic sub-modes)
    "resist": 3200,      # Category C (brand-substitution sub-mode)
    "memory": 12000,     # Category B
    "drift": 6400,       # Category D
    "calc": 4800,        # Category E
    "greet": 4000,       # Category F
    "chat": 2000,        # bonus: no-system greetings (pool is ~2.4K rows; stay under it)
    "clarify": 4800,     # bonus: "ask before assuming" (not in the original spec)
}


def mk(id_, category, messages, source_file, meta=None):
    rec = {"id": id_, "category": category, "dialect": "iraqi_arabic",
           "messages": messages, "source_file": source_file}
    if meta is not None:
        rec["meta"] = meta
    return rec


def build_category(name, all_types, bank, n, seed):
    rng = random.Random(seed)
    records = []
    if name == "copy":
        for i in range(n):
            msgs, cat = grounded.gen_copy(i, all_types, rng)
            records.append(mk(f"v5_copy_{i + 1:05d}", cat, msgs, "generate_v5_grounded_data.py"))
    elif name == "reject":
        for i in range(n):
            msgs, cat = grounded.gen_reject(i, bank, all_types, rng)
            records.append(mk(f"v5_reject_{i + 1:05d}", cat, msgs, "generate_v5_grounded_data.py"))
    elif name == "resist":
        for i in range(n):
            msgs, cat = grounded.gen_resist(i, all_types, rng)
            records.append(mk(f"v5_resist_{i + 1:05d}", cat, msgs, "generate_v5_grounded_data.py"))
    elif name == "chat":
        for i in range(n):
            msgs, cat = grounded.gen_chat(i, rng)
            records.append(mk(f"v5_chat_{i + 1:05d}", cat, msgs,
                               "generate_v5_grounded_data.py (sampled from greetings_smalltalk_only.jsonl)"))
    elif name == "memory":
        for i in range(n):
            msgs, cat, meta = memory.gen_memory(all_types, rng)
            records.append(mk(f"v5_memory_{i + 1:05d}", cat, msgs, "generate_v5_memory_data.py", meta=meta))
    elif name == "drift":
        for i in range(n):
            msgs, cat = drift.gen_drift(all_types, rng)
            records.append(mk(f"v5_drift_{i + 1:05d}", cat, msgs, "generate_v5_drift_data.py"))
    elif name == "calc":
        for i in range(n):
            msgs, cat = calc.gen_calc(all_types, rng)
            records.append(mk(f"v5_calc_{i + 1:05d}", cat, msgs, "generate_v5_calc_data.py"))
    elif name == "greet":
        for i in range(n):
            msgs, cat = greet.gen_greet_sys(all_types, rng)
            records.append(mk(f"v5_greetsys_{i + 1:05d}", cat, msgs, "generate_v5_greet_data.py"))
    elif name == "clarify":
        ratios = clarify.RATIOS
        counts = {k: round(n * v) for k, v in ratios.items()}
        first_key = next(iter(ratios))
        counts[first_key] += n - sum(counts.values())
        for pattern, gen_fn in clarify.GENERATORS.items():
            for i in range(counts[pattern]):
                msgs, cat = gen_fn(all_types, rng)
                records.append(mk(f"v5_clarify_{pattern}_{i + 1:05d}", cat, msgs, "generate_v5_clarify_data.py"))
    else:
        raise ValueError(f"unknown category: {name}")
    return records


def assert_no_placeholders(records):
    """Mandatory Phase-2 guard: raise if a raw '{' or '}' survives anywhere."""
    for i, rec in enumerate(records):
        for m in rec["messages"]:
            content = m["content"]
            found = tc.find_placeholders(content)
            if found or "{" in content or "}" in content:
                raise AssertionError(
                    f"record #{i} id={rec.get('id')!r} has an unfilled template artifact: "
                    f"{found!r} in content={content[:100]!r}"
                )


def write_sharded_jsonl(records, out_dir, prefix, max_shard_bytes=MAX_SHARD_BYTES):
    """Shard records into <=max_shard_bytes-sized *_partNN.jsonl files, same
    convention as convert_to_jsonl.py uses for v4, so no single file trips
    GitHub's 100 MB push limit."""
    lines = [json.dumps(r, ensure_ascii=False) + "\n" for r in records]
    shards, cur, cur_bytes = [], [], 0
    for line in lines:
        cur.append(line)
        cur_bytes += len(line.encode("utf-8"))
        if cur_bytes >= max_shard_bytes:
            shards.append(cur)
            cur, cur_bytes = [], 0
    if cur:
        shards.append(cur)

    paths = []
    for i, shard_lines in enumerate(shards, start=1):
        path = out_dir / f"{prefix}_part{i:02d}.jsonl"
        with open(path, "w", encoding="utf-8") as f:
            f.writelines(shard_lines)
        paths.append(path)
    return paths


def write_stats(out_dir, train, val, all_records):
    all_count = len(all_records)
    cat_counts = Counter(r["category"] for r in all_records)

    lines = ["# v5 Dataset Stats\n"]
    lines.append(f"Total: {all_count} (train {len(train)} / val {len(val)})\n")

    lines.append("## Category proportions\n")
    lines.append("| Category | Count | % |")
    lines.append("|---|---|---|")
    for cat, n in sorted(cat_counts.items(), key=lambda x: -x[1]):
        lines.append(f"| {cat} | {n} | {n / all_count:.1%} |")

    buckets = Counter()
    dialect_hits, dialect_total = 0, 0
    for r in all_records:
        for m in r["messages"]:
            if m["role"] != "assistant":
                continue
            n_tok = tc.count_tokens(m["content"])
            if n_tok <= 10:
                buckets["0-10"] += 1
            elif n_tok <= 20:
                buckets["11-20"] += 1
            elif n_tok <= 40:
                buckets["21-40"] += 1
            elif n_tok <= 60:
                buckets["41-60"] += 1
            else:
                buckets["61+"] += 1
            dialect_total += 1
            if tc.contains_dialect_keyword(m["content"]):
                dialect_hits += 1

    lines.append("\n## Assistant-turn token-length histogram\n")
    lines.append("| Bucket | Count |")
    lines.append("|---|---|")
    for b in ["0-10", "11-20", "21-40", "41-60", "61+"]:
        lines.append(f"| {b} | {buckets.get(b, 0)} |")

    lines.append("\n## Dialect keyword coverage\n")
    pct = dialect_hits / max(1, dialect_total)
    lines.append(f"{dialect_hits}/{dialect_total} assistant turns ({pct:.1%}) contain >=1 Iraqi dialect keyword.\n")

    sys_lens = sorted(
        tc.count_tokens(r["messages"][0]["content"])
        for r in all_records if r["messages"] and r["messages"][0]["role"] == "system"
    )
    if sys_lens:
        n = len(sys_lens)
        lines.append("## System-prompt token length (categories with a catalog)\n")
        lines.append(f"min={sys_lens[0]} p25={sys_lens[n // 4]} median={sys_lens[n // 2]} "
                      f"p75={sys_lens[3 * n // 4]} max={sys_lens[-1]} (n={n})\n")

    (out_dir / "stats.md").write_text("\n".join(lines), encoding="utf-8")


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--seed", type=int, default=42)
    ap.add_argument("--v4-dialect-n", type=int, default=80000,
                     help="subsample cap on the audited v4 dialect-only slice "
                          "(~76K records available; default is set above that "
                          "so all of it is used, roughly balancing the ~76K new "
                          "catalog-grounded synthetic examples 1:1)")
    for name, default in DEFAULT_COUNTS.items():
        ap.add_argument(f"--n-{name}", type=int, default=default)
    ap.add_argument("--out-dir", default=str(OUT_DIR))
    ap.add_argument("--val-ratio", type=float, default=0.02)
    ap.add_argument("--minhash-threshold", type=float, default=0.9)
    ap.add_argument("--num-perm", type=int, default=128)
    args = ap.parse_args()

    out_dir = Path(args.out_dir)
    out_dir.mkdir(parents=True, exist_ok=True)

    bank = grounded.load_bank()
    all_types = grounded.flatten_types(bank)

    all_records = []
    for offset, name in enumerate(DEFAULT_COUNTS):
        n = getattr(args, f"n_{name}")
        seed = args.seed + offset * 1000 + 1
        recs = build_category(name, all_types, bank, n, seed)
        all_records.extend(recs)
        print(f"{name}: {len(recs)}")

    assert_no_placeholders(all_records)
    print(f"synthetic total: {len(all_records)} (placeholder guard passed)")

    v4_path = out_dir / "v4_dialect_kept.jsonl"
    if v4_path.exists():
        v4_records = []
        with open(v4_path, encoding="utf-8") as f:
            for line in f:
                line = line.strip()
                if line:
                    v4_records.append(json.loads(line))
        rng_v4 = random.Random(args.seed + 999)
        rng_v4.shuffle(v4_records)
        v4_sample = v4_records[:args.v4_dialect_n]
        all_records.extend(v4_sample)
        print(f"v4_dialect_kept: sampled {len(v4_sample)} / {len(v4_records)} available")
    else:
        print(f"WARNING: {v4_path} not found -- run audit_corpus.py first. Skipping v4 fold-in.")

    print("scanning merged set for near-duplicates...")
    keep_idx, drop_idx = find_near_duplicates(
        all_records, threshold=args.minhash_threshold, num_perm=args.num_perm, seed=args.seed
    )
    if drop_idx:
        print(f"removed {len(drop_idx)} near-duplicate record(s) from the merged set")
    all_records = [all_records[i] for i in keep_idx]

    rng = random.Random(args.seed)
    rng.shuffle(all_records)

    by_cat = defaultdict(list)
    for r in all_records:
        by_cat[r["category"]].append(r)

    train, val = [], []
    for cat, recs in by_cat.items():
        n_val = max(1, int(len(recs) * args.val_ratio)) if len(recs) >= 20 else 0
        val.extend(recs[:n_val])
        train.extend(recs[n_val:])
    rng.shuffle(train)
    rng.shuffle(val)

    print("verifying zero train/val leakage on final split...")
    leaked = verify_no_leakage(train, val, threshold=args.minhash_threshold, num_perm=args.num_perm, seed=args.seed)
    if leaked:
        leaked_set = set(leaked)
        val = [r for i, r in enumerate(val) if i not in leaked_set]
        print(f"final-split leakage check: dropped {len(leaked)} val record(s)")
    else:
        print("final-split leakage check: clean (0 overlap)")

    # train is large at this scale (150K+ records) - shard it so no single
    # file trips GitHub's 100 MB push limit. val stays a single small file.
    for stale in list(out_dir.glob("train.jsonl")) + list(out_dir.glob("train_part*.jsonl")):
        stale.unlink()
    train_paths = write_sharded_jsonl(train, out_dir, "train")
    val_path = out_dir / "val.jsonl"
    with open(val_path, "w", encoding="utf-8") as f:
        for r in val:
            f.write(json.dumps(r, ensure_ascii=False) + "\n")

    write_stats(out_dir, train, val, all_records)

    print(f"\nFINAL: train={len(train)} val={len(val)} total={len(train) + len(val)}")
    for p in train_paths:
        print(f"wrote {p} ({p.stat().st_size / 1024 / 1024:.1f} MB)")
    print(f"wrote {val_path} ({val_path.stat().st_size / 1024 / 1024:.1f} MB)")
    print(f"wrote {out_dir / 'stats.md'}")


if __name__ == "__main__":
    main()
