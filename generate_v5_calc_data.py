"""Generate v5 Category E: deferred-calculation examples (Iraqi Arabic).

E4B is unreliable at arithmetic, so this category does NOT teach the model to
compute totals - it teaches it to state the components and defer:
    "اثنين ويا الخصم شكد؟"
    -> "الواحد 700,000 وعليهم خصم 5% للقطعتين، أحسبهالك بالفاتورة بالضبط"
The reply always contains the correct unit price and discount rate verbatim
from the catalog/services block and never a computed total (asserted here at
generation time, and re-checked generically by validate_v5.py's "every
number in an assistant turn exists in the system prompt" rule, since a
fabricated total would almost never coincidentally match a catalog number).

Domains without a per-unit discount concept (سيارات, عقارات) are excluded so
the services block's "discount" line is always present.

Run:
    python generate_v5_calc_data.py --n 600
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
    fmt_price,
    flatten_types,
    load_bank,
    service_profile_for,
    user_ask_item,
    assistant_answer_item,
)

NO_DISCOUNT_DOMAINS = {"سيارات", "عقارات"}

Q_QTY_DISCOUNT = [
    "اثنين ويا الخصم شكد؟",
    "لو أخذ اثنين شكد الحساب؟",
    "شكد المجموع لو أخذ وحدتين مع الخصم؟",
    "أريد قطعتين، شنو يصير السعر بعد الخصم؟",
    "لو أخذ فدين شكد يصير؟",
]

A_DEFER_TEMPLATES = [
    "زين، الوحدة {price} دينار وعليهم خصم {rate}% للقطعتين، أحسبهالك بالفاتورة بالضبط",
    "هسه، {price} دينار الوحدة وبالخصم {rate}% للفدين، الحساب الأكيد أطلعه بالفاتورة",
    "خوش سؤال، الواحد بـ{price} وخصم {rate}% لو أخذت اثنين، والمجموع بالكاشير",
    "زين، سعر الوحدة {price} دينار مع خصم {rate}% للقطعتين، والرقم النهائي بالفاتورة",
]


def gen_calc(all_types, rng):
    discount_types = [(d, t, c) for d, t, c in all_types if d not in NO_DISCOUNT_DOMAINS]
    items = build_catalog(discount_types, rng)
    profile = service_profile_for(items)
    assert profile["discount"], "calc category requires a discount-eligible domain"
    services, services_text = build_services(rng, profile)
    target = rng.choice(items)
    system = build_system(items, services_text, rng)
    messages = [{"role": "system", "content": system}]

    messages.append({"role": "user", "content": user_ask_item(target, rng)})
    messages.append({"role": "assistant", "content": assistant_answer_item(target, rng)})

    messages.append({"role": "user", "content": rng.choice(Q_QTY_DISCOUNT)})
    reply = rng.choice(A_DEFER_TEMPLATES).format(price=fmt_price(target["price"]), rate=services["discount_rate"])
    assert fmt_price(target["price"]) in reply
    assert f"{services['discount_rate']}%" in reply
    messages.append({"role": "assistant", "content": reply})

    return messages, "grounded_catalog_calc"


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--n", type=int, default=600)
    ap.add_argument("--seed", type=int, default=42)
    ap.add_argument("--val-ratio", type=float, default=0.05)
    ap.add_argument("--out-train", default=str(DATA_DIR / "v5" / "calc_train.jsonl"))
    ap.add_argument("--out-val", default=str(DATA_DIR / "v5" / "calc_val.jsonl"))
    args = ap.parse_args()

    rng = random.Random(args.seed)
    all_types = flatten_types(load_bank())

    records = []
    for i in range(args.n):
        msgs, cat = gen_calc(all_types, rng)
        records.append({
            "id": f"v5_calc_{i + 1:05d}", "category": cat, "dialect": "iraqi_arabic",
            "messages": msgs, "source_file": "generate_v5_calc_data.py",
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
