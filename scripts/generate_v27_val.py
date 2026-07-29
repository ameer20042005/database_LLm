# -*- coding: utf-8 -*-
"""v27 — تقييم نواقص التقييم، بقوائم وبراندات حصرية وبذرة مختلفة."""
import json
import random
import sys
from collections import Counter
from pathlib import Path

sys.stdout.reconfigure(encoding="utf-8")
sys.path.insert(0, str(Path(__file__).resolve().parent))

import generate_v27_eval_gaps as G          # noqa: E402

DATA = Path(__file__).resolve().parent.parent / "data"

# أزواج غامضة حصرية — ولا واحد منها بالتدريب
G.PAIRS = [
    ("مكيف شباك 2 طن نوع اول (ديجيتال)", 460000,
     "مكيف شباك 2 طن نوع ثاني (عادي)", 350000, "الشباك 2 طن"),
    ("ثلاجة 20 قدم نوع اول (ديجيتال)", 980000,
     "ثلاجة 20 قدم نوع ثاني (عادي)", 820000, "الـ20 قدم"),
    ("سخان 100 لتر نوع اول (ستانلس)", 240000,
     "سخان 100 لتر نوع ثاني (عادي)", 180000, "المية لتر"),
]
G.SINGLES = [
    ("خلاط كنوود 800 واط", 88000), ("مكواة بخار 2200 واط", 42000),
    ("مروحة عمودية 18 انچ", 65000), ("قلاية هوائية 5 لتر", 125000),
]
G.BRANDS = ["دايسون", "فيليبس", "براون", "الكترولوكس", "ويرلبول",
            "هيتاشي", "باناسونيك", "سيمنس"]
G.KINDS = ["مكنسة", "خلاط", "فرن", "مكيف", "ثلاجة"]


def main():
    random.seed(77023)
    rows, seen = [], set()
    plan = [
        (G.gen_merged_doubt,          170),
        (G.gen_merged_doubt_short,     70),
        (G.gen_ambiguous_price,        70),
        (G.gen_ambiguous_after_first,  80),
        (G.gen_reject_clean,          120),
        (G.gen_reject_then_alt,        70),
        (G.gen_sequential_named,      100),
        (G.gen_sequential_two_brands,  60),
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
    p = DATA / "iraqi_v27_val_extra.jsonl"
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
