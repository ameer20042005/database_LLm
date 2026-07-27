# -*- coding: utf-8 -*-
"""
بناء iraqi_val_v13.jsonl — سدّ فجوة التغطية التقييمية.

المشكلة المقيسة: 36 فئة تدريب بلا **أي** تمثيل بـiraqi_val_v8.jsonl،
وهي بالذات الفئات المرجَّحة 6–16× (v9–v12) — أي أعلى استثمار تدريبي
بأدنى قابلية قياس. أخطرها [ORDER_READY]: 440 رد تدريبي و**صفر** تقييمي،
فما في طريقة لمعرفة هل تعلّمها الموديل كشرط مركّب أم كعادة ختامية.

المنهج — الاقتطاع لا التوليد:
    التقييم يُبنى بسحب شريحة من **نفس** ملفات الدفعات، ثم حذفها من
    التدريب يتم تلقائياً بفحص التلوث بالخلية 6 (يقارن messages حرفياً).
    البديل — توليد أمثلة تقييم جديدة — يقيس قدرة المولّد لا قدرة
    الموديل، ويخاطر بقياس توزيع مختلف عن اللي اتدرب عليه.

النسبة: 12% من كل فئة، بحد أدنى مثالين وحد أقصى 60 — الحد الأدنى يضمن
أن الفئات الصغيرة (items_dual_form بـ8 أمثلة) تبقى مقيسة ولو بخشونة،
والحد الأقصى يمنع فئة كبيرة من ابتلاع التقييم.

الإخراج: data/iraqi_val_v13.jsonl
"""
import json
import random
import sys
from collections import Counter, defaultdict
from pathlib import Path

sys.stdout.reconfigure(encoding="utf-8")
random.seed(20260727)
DATA = Path(__file__).resolve().parent.parent / "data"

SRC_GLOBS = ["iraqi_v9_generated*.jsonl", "iraqi_v10_*.jsonl",
             "iraqi_v11_gaps.jsonl", "iraqi_v12_order.jsonl",
             "iraqi_v13_scope.jsonl"]
VAL_RATIO, MIN_PER_CAT, MAX_PER_CAT = 0.12, 2, 60


def main():
    by_cat = defaultdict(list)
    for g in SRC_GLOBS:
        for f in sorted(DATA.glob(g)):
            for line in f.open(encoding="utf-8"):
                d = json.loads(line)
                by_cat[d.get("category", "?")].append(d)

    # ما اتدرب عليه v8 مقيس أصلاً بـval_v8 — نتجنب ازدواج القياس
    already = set()
    vv8 = DATA / "iraqi_val_v8.jsonl"
    if vv8.exists():
        for line in vv8.open(encoding="utf-8"):
            already.add(json.loads(line).get("category"))

    out, skipped = [], []
    for cat, rows in sorted(by_cat.items()):
        if cat in already:
            # الفئة مقيسة أصلاً بـval_v8 (مثل json_extraction بـv9)
            skipped.append(cat)
            continue
        n = max(MIN_PER_CAT, min(MAX_PER_CAT, round(len(rows) * VAL_RATIO)))
        n = min(n, len(rows))
        out.extend(random.sample(rows, n))

    random.shuffle(out)

    # ── فحص: صفر تكرار حرفي داخل التقييم ──
    key = lambda m: json.dumps(m, ensure_ascii=False, sort_keys=True)
    seen, uniq = set(), []
    for r in out:
        k = key(r["messages"])
        if k not in seen:
            seen.add(k)
            uniq.append(r)
    out = uniq

    # ── فحص: صفر تداخل مع val_v8 ──
    if vv8.exists():
        v8keys = {key(json.loads(l)["messages"]) for l in vv8.open(encoding="utf-8")}
        before = len(out)
        out = [r for r in out if key(r["messages"]) not in v8keys]
        if before != len(out):
            print(f"ℹ️ حُذف {before - len(out)} مثال مكرر مع val_v8")

    dst = DATA / "iraqi_val_v13.jsonl"
    with dst.open("w", encoding="utf-8") as fh:
        for r in out:
            fh.write(json.dumps(r, ensure_ascii=False) + "\n")

    c = Counter(r.get("category") for r in out)
    print(f"✅ {dst.name}: {len(out):,} مثال عبر {len(c)} فئة")
    print(f"\n{'الفئة':<36}{'تقييم':>7}{'تدريب':>9}{'%':>7}")
    for cat, n in c.most_common():
        tot = len(by_cat[cat])
        print(f"  {cat:<34}{n:>7,}{tot:>9,}{100 * n / tot:>6.1f}%")
    if skipped:
        print(f"\nℹ️ {len(skipped)} فئة مقيسة أصلاً بـval_v8، ما انسحبت مرة ثانية:")
        print("   " + ", ".join(skipped))
    print("\n⚠️ ملاحظة: هذي الأمثلة لا زالت بملفات التدريب — فحص التلوث")
    print("   بالخلية 6 يحذفها من التدريب تلقائياً عند التحميل.")


if __name__ == "__main__":
    main()
