# -*- coding: utf-8 -*-
"""v25 — تقييم المجانية المؤسَّسة، بقوائم حصرية وبذرة مختلفة."""
import json
import random
import sys
from collections import Counter
from pathlib import Path

sys.stdout.reconfigure(encoding="utf-8")
sys.path.insert(0, str(Path(__file__).resolve().parent))

import generate_v25_grounded_free as G          # noqa: E402

DATA = Path(__file__).resolve().parent.parent / "data"

G.PRODUCTS = [
    ("ثلاجة كونكورد 18 قدم", 640000), ("غسالة توشيبا 8 كغم", 520000),
    ("مكيف جنرال 2 طن سبلت", 780000), ("تلفزيون شارب 55 بوصة", 700000),
]
G.CITIES = ["السليمانية", "الديوانية", "الكوت", "العمارة"]
G.OUT_FEE = [12000, 18000, 30000]


def main():
    random.seed(55006)
    rows, seen = [], set()
    for fn, n in ((G.gen_delivery, 110), (G.gen_install, 60),
                  (G.gen_threshold, 60), (G.gen_edge, 80)):
        kept = 0
        for r in fn(n * 5):
            if kept >= n:
                break
            k = json.dumps(r["messages"], ensure_ascii=False, sort_keys=True)
            if k in seen:
                continue
            seen.add(k)
            rows.append(r)
            kept += 1
    p = DATA / "iraqi_v25_val_extra.jsonl"
    with p.open("w", encoding="utf-8") as fh:
        for r in rows:
            fh.write(json.dumps(r, ensure_ascii=False) + "\n")
    print(f"✅ {len(rows)} مثال تقييم -> {p.name}")
    for k, v in Counter(r["category"] for r in rows).most_common():
        print(f"   {k:<30}{v:>5}")


if __name__ == "__main__":
    main()
