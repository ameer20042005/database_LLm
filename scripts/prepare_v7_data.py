# -*- coding: utf-8 -*-
"""
دمج بيانات v7 مع بيانات v6 النهائية -> v7

يستورد فحوصات prepare_v6_data.py (بنية، لهجة، تأريض أرقام) ويعيد تطبيقها على
المجموع الكامل (v6 النهائية + v7 extras)، مع إعادة فحص التلوث train/val
والتكرار الحرفي وسقف الهياكل (3) على المجموع.

استثناء وحيد: فئة json_fixed_schema لا تمر بفحص تأريض الأرقام النصي (أرقام JSON
بدون فواصل آلاف عمداً) — بدلاً عنه تُتحقق حسابياً: json.loads + total + مطابقة
المنتجات والأسعار مع كتالوج المثال (order_json_valid من generate_v7_extras).

الناتج: data/iraqi_train_v7_part01..03.jsonl + data/iraqi_val_v7.jsonl
"""
import json
import glob
import random
from collections import Counter

import prepare_v6_data as p6
from generate_v7_extras import order_json_valid, duration_grounded

random.seed(43)

MAX_PER_SKELETON = 3


def load(paths):
    rows = []
    for p in paths:
        with open(p, encoding="utf-8") as f:
            for line in f:
                if line.strip():
                    rows.append(json.loads(line))
    return rows


def reason(r):
    """سبب الرفض أو None — نفس معايير v6 مع استثناء JSON المحسوب."""
    if not p6.structure_ok(r):
        return "structure"
    if not p6.dialect_clean(r):
        return "dialect"
    cat = r.get("category", "")
    if cat == "json_fixed_schema":
        if not order_json_valid(r):
            return "json"
    elif not p6.numbers_grounded(r):
        return "numbers"
    if cat == "ataakadlak_expanded" and not duration_grounded(r):
        return "duration"
    return None


def main():
    train = load(sorted(glob.glob("data/iraqi_train_v6_part*.jsonl"))
                 + ["data/iraqi_v7_extras_train.jsonl"])
    val = load(["data/iraqi_val_v6.jsonl", "data/iraqi_v7_extras_val.jsonl"])
    print(f"مدخلات: train={len(train)}  val={len(val)}")

    stats = Counter()

    # ---- 1) تنظيف val: فحوصات + تكرار داخلي ----
    val_clean, val_keys = [], set()
    for r in val:
        why = reason(r)
        if why:
            stats[f"val_{why}"] += 1
            continue
        k = p6.conv_key(r)
        if k in val_keys:
            stats["val_exact_dup"] += 1
            continue
        val_keys.add(k)
        val_clean.append(r)

    # ---- 2) تنظيف train: فحوصات + تكرار حرفي + تلوث مع val + سقف الهياكل ----
    out, seen, skel_count = [], set(), Counter()
    random.shuffle(train)
    for r in train:
        why = reason(r)
        if why:
            stats[f"train_{why}"] += 1
            continue
        k = p6.conv_key(r)
        if k in seen:
            stats["train_exact_dup"] += 1
            continue
        if k in val_keys:
            stats["train_val_leak"] += 1
            continue
        sk = p6.skeleton_key(r)
        if skel_count[sk] >= MAX_PER_SKELETON:
            stats["train_skeleton_dup"] += 1
            continue
        seen.add(k)
        skel_count[sk] += 1
        out.append(r)
    train = out

    print(f"\nإجمالي train v7: {len(train)}")
    print(f"إجمالي val v7: {len(val_clean)}")
    print("\nفئات v7 الجديدة ضمن train:")
    cats = Counter(r.get("category") for r in train)
    for c in ("persistence_refusal", "ataakadlak_expanded", "json_fixed_schema", "praise_no_upsell"):
        print(f"  {c}: {cats[c]}")
    print("\nإحصائيات الحذف:")
    for k, v in sorted(stats.items()):
        print(f"  {k}: {v}")
    if not stats:
        print("  لا شيء")

    # ---- 3) الكتابة: 3 أجزاء train + val ----
    n = len(train)
    thirds = [train[: n // 3], train[n // 3: 2 * n // 3], train[2 * n // 3:]]
    for i, part in enumerate(thirds, 1):
        path = f"data/iraqi_train_v7_part{i:02d}.jsonl"
        with open(path, "w", encoding="utf-8") as f:
            for r in part:
                f.write(json.dumps(r, ensure_ascii=False) + "\n")
        print(f"كتب {path}: {len(part)} سطر")
    with open("data/iraqi_val_v7.jsonl", "w", encoding="utf-8") as f:
        for r in val_clean:
            f.write(json.dumps(r, ensure_ascii=False) + "\n")
    print(f"كتب data/iraqi_val_v7.jsonl: {len(val_clean)} سطر")


if __name__ == "__main__":
    main()
