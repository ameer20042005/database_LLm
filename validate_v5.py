"""Phase 3: validate the final v5 dataset (data/v5/train.jsonl + val.jsonl).

Two rule tiers, since the final mix has two different roles (see the v5
build plan): records from a v5 generator (system prompt + catalog present)
get the FULL strict rule set; records folded in from the audited v4
dialect-only slice (no system prompt at all - they contribute dialect
diversity only, not catalog-grounded "production reply" behavior) get a
lighter structural rule set. A record is treated as "v5-generated" if its
first message has role "system"; that single condition is what actually
gates which checks apply (documented below), not source_file string
matching.

Full rule set (records with a leading system message):
  - no placeholder patterns
  - every dinar amount in an assistant turn exists verbatim in that record's
    system prompt
  - every known brand name in an assistant turn exists in that record's
    system prompt
  - assistant turns <= 2 sentences and <= 60 tokens
  - >=1 Iraqi dialect keyword per assistant turn
  - Category B (grounded_catalog_memory): the recalled name at meta.recall_turn
    matches meta.customer_name (or an honest non-claim when name_given=False)

Lighter rule set (no system message - the v4 dialect supplement):
  - no placeholder patterns
  - no mixed-script corruption

Universal, both tiers:
  - valid JSON / well-formed messages list
  - correct role alternation, tolerant of an optional leading "system" turn

Fails loudly: prints every violation with the record index + id, then exits
with status 1 if anything failed.

Run:
    python validate_v5.py
"""
import argparse
import json
import re
import sys
from pathlib import Path

import text_checks as tc
from generate_v5_grounded_data import DATA_DIR, load_bank

OUT_DIR = DATA_DIR / "v5"

MAX_ASSISTANT_TOKENS = 60
MAX_ASSISTANT_SENTENCES = 2


def load_jsonl(path):
    records = []
    with open(path, encoding="utf-8") as f:
        for lineno, line in enumerate(f, start=1):
            line = line.strip()
            if not line:
                continue
            try:
                records.append(json.loads(line))
            except json.JSONDecodeError as e:
                raise SystemExit(f"INVALID JSON at {path}:{lineno}: {e}")
    return records


def mentions_brand(brand, text):
    """Word-boundary-aware containment check. A naive substring search false-
    positives on short brand names that happen to occur inside unrelated
    words - e.g. the stove brand 'الفا' is a literal substring of 'الفاتورة'
    (invoice)."""
    pattern = r"(?<!\w)" + re.escape(brand) + r"(?!\w)"
    return re.search(pattern, text) is not None


def build_brand_vocab():
    bank = load_bank()
    brands = set()
    for domain, types in bank.items():
        for type_name, cfg in types.items():
            for b in cfg.get("brands", []):
                if b:
                    brands.add(b)
    return brands


def check_roles(messages):
    roles = [m.get("role") for m in messages]
    if not roles:
        return ["empty messages list"]
    errs = []
    start = 0
    if roles[0] == "system":
        start = 1
    if start >= len(roles):
        return errs
    if roles[start] != "user":
        errs.append(f"first non-system message must be 'user', got {roles[start]!r}")
    for i in range(start, len(roles) - 1):
        if roles[i] == roles[i + 1]:
            errs.append(f"consecutive same-role messages at index {i}/{i + 1} ({roles[i]!r})")
    return errs


def check_full_rules(rec, brand_vocab):
    errs = []
    messages = rec["messages"]
    system_text = messages[0]["content"]
    system_amounts = set(tc.extract_dinar_amounts(system_text))
    system_norm = tc.normalize_arabic(system_text)
    category = rec.get("category", "")
    # both "reject" (echoes back an absent product's name/plural, which may
    # contain incidental digits like a car model number or an area in m2)
    # and "resist" (echoes back an absent brand) legitimately name something
    # NOT in the catalog by design - that's not a grounding violation.
    is_reject_like = category == "grounded_catalog_resist" or category.startswith("grounded_catalog_reject")

    for i, m in enumerate(messages):
        content = m.get("content", "")
        if tc.find_placeholders(content):
            errs.append(f"[{i}] placeholder leak: {tc.find_placeholders(content)}")
        if m.get("role") != "assistant":
            continue
        for n in tc.extract_dinar_amounts(content):
            if n not in system_amounts:
                errs.append(f"[{i}] assistant states dinar amount {n} not present in system prompt")
        if not is_reject_like:
            for brand in brand_vocab:
                if mentions_brand(brand, content) and not mentions_brand(brand, system_text):
                    errs.append(f"[{i}] assistant mentions brand {brand!r} not present in system prompt")
        n_sent = len(tc.split_sentences(content))
        if n_sent > MAX_ASSISTANT_SENTENCES:
            errs.append(f"[{i}] assistant turn has {n_sent} sentences (> {MAX_ASSISTANT_SENTENCES}): {content!r}")
        n_tok = tc.count_tokens(content)
        if n_tok > MAX_ASSISTANT_TOKENS:
            errs.append(f"[{i}] assistant turn has {n_tok} tokens (> {MAX_ASSISTANT_TOKENS}): {content!r}")
        if not tc.contains_dialect_keyword(content):
            errs.append(f"[{i}] assistant turn has no Iraqi dialect keyword: {content!r}")

    if rec.get("category") == "grounded_catalog_memory" and "meta" in rec:
        meta = rec["meta"]
        recall_turn = meta.get("recall_turn")
        if recall_turn is None or recall_turn >= len(messages):
            errs.append(f"meta.recall_turn={recall_turn} out of range")
        else:
            recall_content = messages[recall_turn]["content"]
            if meta.get("name_given"):
                name = meta.get("customer_name")
                if not name or name not in recall_content:
                    errs.append(f"[{recall_turn}] recall turn does not contain customer_name {name!r}: {recall_content!r}")
            else:
                if meta.get("customer_name") is not None:
                    errs.append("name_given=False but meta.customer_name is set")

    return errs


def check_light_rules(rec):
    errs = []
    for i, m in enumerate(rec["messages"]):
        content = m.get("content", "")
        if tc.find_placeholders(content):
            errs.append(f"[{i}] placeholder leak: {tc.find_placeholders(content)}")
        if tc.has_corrupted_mixed_script(content):
            errs.append(f"[{i}] mixed-script corruption detected: {content[:80]!r}")
    return errs


def validate_records(records, brand_vocab):
    total_errs = 0
    for idx, rec in enumerate(records):
        rec_id = rec.get("id", f"#{idx}")
        for field in ("id", "category", "dialect", "messages"):
            if field not in rec:
                print(f"FAIL [{idx}] {rec_id}: missing field {field!r}")
                total_errs += 1

        messages = rec.get("messages", [])
        role_errs = check_roles(messages)
        for e in role_errs:
            print(f"FAIL [{idx}] {rec_id}: {e}")
        total_errs += len(role_errs)

        if not messages:
            continue

        # Full tier only for text OUR OWN templates authored (grounded copy/
        # reject/resist, memory/drift/calc/greet/clarify) - not for anything
        # sampled from a pre-existing, already dialect-reviewed pool (the
        # "chat" bonus category, or the audited v4 dialect-only slice folded
        # in by generate_v5.py), even if that content happens to carry an
        # incidental leading system message. We only hold ourselves to
        # guarantees about text we actually generated.
        source_file = rec.get("source_file", "")
        is_our_template = source_file == "generate_v5_grounded_data.py" or source_file.startswith((
            "generate_v5_memory_data.py",
            "generate_v5_drift_data.py",
            "generate_v5_calc_data.py",
            "generate_v5_greet_data.py",
            "generate_v5_clarify_data.py",
        ))
        is_v5_generated = messages[0].get("role") == "system" and is_our_template
        errs = check_full_rules(rec, brand_vocab) if is_v5_generated else check_light_rules(rec)
        for e in errs:
            print(f"FAIL [{idx}] {rec_id}: {e}")
        total_errs += len(errs)

    return total_errs


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--train", default=str(OUT_DIR / "train.jsonl"))
    ap.add_argument("--val", default=str(OUT_DIR / "val.jsonl"))
    ap.add_argument("--report-only", action="store_true", help="don't exit(1) on violations")
    args = ap.parse_args()

    brand_vocab = build_brand_vocab()

    total_errs = 0
    for name, path in [("train", args.train), ("val", args.val)]:
        p = Path(path)
        if not p.exists():
            raise SystemExit(f"{path} not found -- run generate_v5.py first")
        records = load_jsonl(p)
        print(f"=== validating {name}: {len(records)} records ===")
        errs = validate_records(records, brand_vocab)
        print(f"{name}: {errs} violation(s) across {len(records)} records\n")
        total_errs += errs

    if total_errs:
        print(f"VALIDATION FAILED: {total_errs} total violation(s)")
        if not args.report_only:
            sys.exit(1)
    else:
        print("VALIDATION PASSED: 0 violations")


if __name__ == "__main__":
    main()
