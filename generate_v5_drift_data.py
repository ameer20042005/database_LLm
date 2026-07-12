"""Generate v5 Category D: anti-price-drift stress conversations (Iraqi Arabic).

Directly targets the production failure mode where the same product got
quoted at three different prices across one conversation (711K -> 191K ->
1,000,000). Structure: ask a target item's price, thread 2-4 distractor turns
(other items / negotiate / stock-check) in between, then re-ask the target's
price - sometimes indirectly ("چان شگد گتلي {name}؟") - one or two more times
before closing. By construction the assistant always restates the identical
verbatim price/warranty from the system catalog; the training signal is
staying correct across many intervening turns instead of drifting, which
validate_v5.py's "every number in an assistant turn exists in the system
prompt" check verifies generically (no extra metadata needed here).

Run:
    python generate_v5_drift_data.py --n 800
"""
import argparse
import json
import random
from pathlib import Path

from generate_v5_grounded_data import (
    DATA_DIR,
    Q_CLOSING,
    A_CLOSING,
    Q_NEGOTIATE,
    A_HOLD_PRICE,
    Q_STOCK,
    A_STOCK,
    build_catalog,
    build_services,
    build_system,
    flatten_types,
    is_realestate,
    load_bank,
    service_profile_for,
    user_ask_item,
    assistant_answer_item,
)

Q_REASK_INDIRECT = [
    "چان شگد گتلي {name}؟",
    "شنو گلت سعر {name} مرة ثانية؟",
    "تذكرني، {name} بيش گتلي؟",
    "شكد گلت سعر {name}، نسيت؟",
]
Q_REASK_DIRECT = ["شكد {name} بعد؟", "بيش {name} تاني مرة؟"]


def gen_drift(all_types, rng):
    items = build_catalog(all_types, rng)
    target = rng.choice(items)
    other_items = [it for it in items if it is not target]
    profile = service_profile_for(items)
    services, services_text = build_services(rng, profile)
    system = build_system(items, services_text, rng)
    messages = [{"role": "system", "content": system}]

    messages.append({"role": "user", "content": user_ask_item(target, rng)})
    messages.append({"role": "assistant", "content": assistant_answer_item(target, rng)})

    last_item = [target]
    scene_pool = ["item", "negotiate_other"] if is_realestate(target) else ["item", "negotiate_other", "stock"]

    def add_distractor_block(n):
        for _ in range(n):
            pool = [it for it in other_items if it is not last_item[0]] or other_items or [target]
            it = rng.choice(pool)
            last_item[0] = it
            scene = rng.choice(scene_pool) if other_items else rng.choice([s for s in scene_pool if s != "item"] or ["negotiate_other"])
            if scene == "item":
                messages.append({"role": "user", "content": user_ask_item(it, rng)})
                messages.append({"role": "assistant", "content": assistant_answer_item(it, rng)})
            elif scene == "negotiate_other":
                messages.append({"role": "user", "content": rng.choice(Q_NEGOTIATE)})
                messages.append({"role": "assistant", "content": rng.choice(A_HOLD_PRICE)})
            else:
                messages.append({"role": "user", "content": rng.choice(Q_STOCK)})
                messages.append({"role": "assistant", "content": rng.choice(A_STOCK)})

    n_reasks = rng.choice([1, 2])
    for _ in range(n_reasks):
        add_distractor_block(rng.randint(2, 4))
        reask = rng.choice(Q_REASK_INDIRECT + Q_REASK_DIRECT).format(name=target["name"])
        messages.append({"role": "user", "content": reask})
        messages.append({"role": "assistant", "content": assistant_answer_item(target, rng)})

    add_distractor_block(rng.randint(1, 3))
    messages.append({"role": "user", "content": rng.choice(Q_CLOSING)})
    messages.append({"role": "assistant", "content": rng.choice(A_CLOSING)})

    return messages, "grounded_catalog_drift"


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--n", type=int, default=800)
    ap.add_argument("--seed", type=int, default=42)
    ap.add_argument("--val-ratio", type=float, default=0.05)
    ap.add_argument("--out-train", default=str(DATA_DIR / "v5" / "drift_train.jsonl"))
    ap.add_argument("--out-val", default=str(DATA_DIR / "v5" / "drift_val.jsonl"))
    args = ap.parse_args()

    rng = random.Random(args.seed)
    all_types = flatten_types(load_bank())

    records = []
    for i in range(args.n):
        msgs, cat = gen_drift(all_types, rng)
        records.append({
            "id": f"v5_drift_{i + 1:05d}", "category": cat, "dialect": "iraqi_arabic",
            "messages": msgs, "source_file": "generate_v5_drift_data.py",
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
