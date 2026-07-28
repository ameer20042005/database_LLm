# -*- coding: utf-8 -*-
"""
v17 — تقييم `deep_refusal_in_sales`.

نفس منهج `generate_v16_val.py`: يعيد استعمال مولّدات v17 نفسها بس
بـ**بذرة مختلفة وقوائم حصرية** (منتجات وأصناف مفقودة ما تظهر بالتدريب
أبداً)، حتى يقيس السلوك لا الحفظ.

بلا هذا الملف تصير `deep_refusal_in_sales` فئة تدريب بلا تقييم — وهي
القاعدة اللي يفرضها البنّاء بـ`assert`.
"""
import json
import random
import sys
from pathlib import Path

sys.stdout.reconfigure(encoding="utf-8")
sys.path.insert(0, str(Path(__file__).resolve().parent))

import generate_v17_deep_refusal as G          # noqa: E402

DATA = Path(__file__).resolve().parent.parent / "data"

# ── قوائم حصرية للتقييم ──
G.PRODUCTS = [
    ("ثلاجة بيكو 16 قدم", 730000),
    ("غسالة هاير 9 كغم اوتوماتيك", 495000),
    ("مكيف كاريير 1.5 طن سبلت", 615000),
    ("تلفزيون توشيبا 50 بوصة سمارت", 720000),
    ("فريزر ميديا 250 لتر", 405000),
    ("طباخ الحافظ 4 عيون", 265000),
]
G.MISSING = ["تلفزيون شاومي 75 بوصة", "غسالة سيمنس 12 كغم",
             "ثلاجة هيتاشي 22 قدم", "مكيف دايكن 4 طن"]

TARGET = 240


def main():
    random.seed(88002)                          # ≠ بذرة التدريب
    rows, seen = [], set()
    for fn, n in ((G.gen_pattern_a, 90), (G.gen_pattern_b, 80),
                  (G.gen_pattern_c, 70)):
        kept = 0
        for r in fn(int(n * 2.5)):
            if kept >= n:
                break
            k = json.dumps(r["messages"], ensure_ascii=False, sort_keys=True)
            if k in seen:
                continue
            seen.add(k)
            rows.append(r)
            kept += 1

    rows = rows[:TARGET]
    p = DATA / "iraqi_v17_val_extra.jsonl"
    with p.open("w", encoding="utf-8") as fh:
        for r in rows:
            fh.write(json.dumps(r, ensure_ascii=False) + "\n")
    print(f"✅ {len(rows)} مثال تقييم -> {p.name}")


if __name__ == "__main__":
    main()
