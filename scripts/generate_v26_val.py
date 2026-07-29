# -*- coding: utf-8 -*-
"""v26 — تقييم الثبات والقوائم والإلغاء، بقوائم حصرية وبذرة مختلفة."""
import json
import random
import sys
from collections import Counter
from pathlib import Path

sys.stdout.reconfigure(encoding="utf-8")
sys.path.insert(0, str(Path(__file__).resolve().parent))

import generate_v26_consistency as G          # noqa: E402

DATA = Path(__file__).resolve().parent.parent / "data"

# قوائم حصرية — ولا صنف منها بالتدريب
G.CATALOG = {
    "الثلاجات": [
        ("ثلاجة يونيون اير 20 قدم", 940000),
        ("ثلاجة كريازي 12 قدم", 480000),
        ("ثلاجة دايو 16 قدم", 705000),
    ],
    "الغسالات": [
        ("غسالة اريستون 7 كغم", 430000),
        ("غسالة بوش 9 كغم", 810000),
        ("غسالة ميديا 11 كغم", 645000),
    ],
    "المكيفات": [
        ("مكيف كاريير 1 طن", 470000),
        ("مكيف ميتسوبيشي 2.5 طن", 990000),
    ],
    "المدافئ": [
        ("مدفأة نفطية 10 لتر", 210000),
    ],
    "الأفران": [
        ("فرن غاز 60 سم", 340000),
    ],
}
G.MISSING = ["نشافة ملابس", "جهاز تنقية هواء", "روبوت مكنسة",
             "ثلاجة سيارة", "طباخ كهربائي محمول", "غلاية بخار"]


def main():
    random.seed(66017)
    rows, seen = [], set()
    plan = [
        (G.gen_price_doubt,          160),
        (G.gen_price_triple,          90),
        (G.gen_doubt_vs_bargain,      90),
        (G.gen_category_list,         80),
        (G.gen_category_list_single,  40),
        (G.gen_more_in_category,      70),
        (G.gen_cancel_reset,          90),
        (G.gen_cancel_requantify,     60),
        (G.gen_cancel_switch,         60),
        (G.gen_reject_standard,       60),
        (G.gen_reject_with_list,      50),
        (G.gen_reject_doubt,          60),
    ]
    for fn, n in plan:
        kept = 0
        for r in fn(n * 6):
            if kept >= n:
                break
            k = json.dumps(r["messages"], ensure_ascii=False, sort_keys=True)
            if k in seen:
                continue
            seen.add(k)
            rows.append(r)
            kept += 1

    errs = G.validate(rows)
    p = DATA / "iraqi_v26_val_extra.jsonl"
    with p.open("w", encoding="utf-8") as fh:
        for r in rows:
            fh.write(json.dumps(r, ensure_ascii=False) + "\n")

    print(f"{'✅' if not errs else '❌'} {len(rows)} مثال تقييم -> {p.name}")
    for k, v in Counter(r["category"] for r in rows).most_common():
        print(f"   {k:<32}{v:>5}")
    if errs:
        for k, v in errs.most_common():
            print(f"   ❌ {k:<44}{v:>5}")


if __name__ == "__main__":
    main()
