"""Generate v5 Category F: greetings-with-system-prompt (Iraqi Arabic).

Greetings *without* a system prompt already work well (existing `gen_chat` in
generate_v5_grounded_data.py, sampled from greetings_smalltalk_only.jsonl).
This category specifically pairs a full system prompt + catalog with a PURE
small-talk exchange: the user never asks about a product, and the assistant
must not proactively pitch one. This targets the topic-drift failure mode
(model randomly pivoting to an unrelated product) by reinforcing "answer
what's asked, don't drift topically" even with a full catalog sitting right
there in context.

Run:
    python generate_v5_greet_data.py --n 500
"""
import argparse
import json
import random
from pathlib import Path

from generate_v5_grounded_data import (
    DATA_DIR,
    build_catalog,
    build_services,
    build_system,
    flatten_types,
    load_bank,
    service_profile_for,
)

OPENING_PAIRS = [
    ("السلام عليكم", "وعليكم السلام، هلا وغلا"),
    ("هلو", "هلا بيك، شخبارك؟"),
    ("مساء الخير", "مساء النور، شلون الصحة؟"),
    ("صباح الخير", "صباح النور، شلونك اليوم؟"),
    ("شلونك؟", "الحمد لله تمام، وانته شلونك؟"),
]

SMALLTALK_PAIRS = [
    ("الحمد لله زين، وانت شلونك؟", "الحمد لله تمام، تسلم"),
    ("الجو حر هواي اليوم", "إي والله حر، الله يعين"),
    ("شخبار الأهل؟", "الحمد لله كلهم زينين"),
    ("شنو أخبارك اليوم؟", "الحمد لله ماشي الحال"),
]

CLOSING_PAIRS = [
    ("فمان الله", "الله وياك"),
    ("تسلم، أشوفك بعدين", "بالسلامة، تسلم"),
    ("زين، مع السلامة", "مع السلامة، الله يخليك"),
    ("يعطيك العافية", "الله يعافيك"),
]


def gen_greet_sys(all_types, rng):
    items = build_catalog(all_types, rng)
    profile = service_profile_for(items)
    services, services_text = build_services(rng, profile)
    system = build_system(items, services_text, rng)
    messages = [{"role": "system", "content": system}]

    q, a = rng.choice(OPENING_PAIRS)
    messages.append({"role": "user", "content": q})
    messages.append({"role": "assistant", "content": a})

    n_extra = rng.randint(0, 2)
    for _ in range(n_extra):
        q, a = rng.choice(SMALLTALK_PAIRS)
        messages.append({"role": "user", "content": q})
        messages.append({"role": "assistant", "content": a})

    q, a = rng.choice(CLOSING_PAIRS)
    messages.append({"role": "user", "content": q})
    messages.append({"role": "assistant", "content": a})

    return messages, "grounded_greet_system"


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--n", type=int, default=500)
    ap.add_argument("--seed", type=int, default=42)
    ap.add_argument("--val-ratio", type=float, default=0.05)
    ap.add_argument("--out-train", default=str(DATA_DIR / "v5" / "greet_train.jsonl"))
    ap.add_argument("--out-val", default=str(DATA_DIR / "v5" / "greet_val.jsonl"))
    args = ap.parse_args()

    rng = random.Random(args.seed)
    all_types = flatten_types(load_bank())

    records = []
    for i in range(args.n):
        msgs, cat = gen_greet_sys(all_types, rng)
        records.append({
            "id": f"v5_greetsys_{i + 1:05d}", "category": cat, "dialect": "iraqi_arabic",
            "messages": msgs, "source_file": "generate_v5_greet_data.py",
        })

    rng.shuffle(records)
    n_val = int(len(records) * args.val_ratio)
    val_records, train_records = records[:n_val], records[n_val:]

    Path(args.out_train).parent.mkdir(parents=True, exist_ok=True)
    with open(args.out_train, "w", encoding="utf-8") as f:
        for r in train_records:
            f.write(json.dumps(r, ensure_ascii=False) + "\n")
    with open(args.out_val, "w", encoding="utf-8") as f:
        for r in val_records:
            f.write(json.dumps(r, ensure_ascii=False) + "\n")

    print(f"total: {len(records)} (train {len(train_records)} / val {len(val_records)})")


if __name__ == "__main__":
    main()
