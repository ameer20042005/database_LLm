# -*- coding: utf-8 -*-
"""
دمج بيانات v8 -> النسخة النهائية للتدريب

المدخلات: v7 النهائية (iraqi_train_v7_part01..03 + iraqi_val_v7) + دفعة v8 المركزة
(iraqi_v8_batch_train/val من generate_v8_batch.py: أتأكدلك 200، JSON بكميات مختلطة 150،
مقاومة الضغط 100، مدح بلا upsell 50).

تُعاد كل فحوصات v7 على المجموع الكامل: بنية، لهجة، تأريض أرقام (مع استثناء
json_fixed_schema المتحقق حسابياً)، تكرار حرفي، تلوث train/val، سقف الهياكل (3).

الناتج: data/iraqi_train_v8_part01..03.jsonl + data/iraqi_val_v8.jsonl
"""
import json
import glob
import os
import random
import sys
from collections import Counter

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

import prepare_v6_data as p6  # noqa: E402
from generate_v7_extras import order_json_valid, duration_grounded  # noqa: E402

random.seed(44)

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
    """سبب الرفض أو None — نفس معايير v7."""
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
    d = lambda name: os.path.join(ROOT, "data", name)
    train = load(sorted(glob.glob(d("iraqi_train_v7_part*.jsonl"))) + [d("iraqi_v8_batch_train.jsonl")])
    val = load([d("iraqi_val_v7.jsonl"), d("iraqi_v8_batch_val.jsonl")])
    print(f"مدخلات: train={len(train)}  val={len(val)}")

    stats = Counter()

    # ---- 1) تنظيف val: فحوصات + تكرار داخلي ----
    val_clean, val_keys, val_skels = [], set(), set()
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
        val_skels.add(p6.skeleton_key(r))
        val_clean.append(r)

    # ---- 2) تنظيف train: فحوصات + تكرار حرفي + تلوث مع val + سقف الهياكل ----
    # دفعة v8 لها أولوية بقاء عند سقف الهياكل: تُعالج أولاً قبل الخلط
    v8_rows = [r for r in train if r.get("source_file") == "generate_v8_batch.py"]
    old_rows = [r for r in train if r.get("source_file") != "generate_v8_batch.py"]
    random.shuffle(old_rows)

    out, seen, skel_count = [], set(), Counter()
    for r in v8_rows + old_rows:
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
        if sk in val_skels:
            stats["train_val_skeleton_leak"] += 1
            continue
        if skel_count[sk] >= MAX_PER_SKELETON:
            stats["train_skeleton_dup"] += 1
            continue
        seen.add(k)
        skel_count[sk] += 1
        out.append(r)
    train = out
    random.shuffle(train)

    print(f"\nإجمالي train v8: {len(train)}")
    print(f"إجمالي val v8: {len(val_clean)}")
    n_v8_kept = sum(1 for r in train if r.get("source_file") == "generate_v8_batch.py")
    print(f"من دفعة v8 المركزة بقي بالتدريب: {n_v8_kept}")
    print("\nفئات الإصلاحات ضمن train:")
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
        path = d(f"iraqi_train_v8_part{i:02d}.jsonl")
        with open(path, "w", encoding="utf-8") as f:
            for r in part:
                f.write(json.dumps(r, ensure_ascii=False) + "\n")
        print(f"كتب {path}: {len(part)} سطر")
    with open(d("iraqi_val_v8.jsonl"), "w", encoding="utf-8") as f:
        for r in val_clean:
            f.write(json.dumps(r, ensure_ascii=False) + "\n")
    print(f"كتب data/iraqi_val_v8.jsonl: {len(val_clean)} سطر")


if __name__ == "__main__":
    main()
