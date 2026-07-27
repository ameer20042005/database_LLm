# -*- coding: utf-8 -*-
"""
بناء الملف الموحّد النهائي — كل التدريب بملف واحد، بلا ترجيح وقت التشغيل.

═══════════════════════════════════════════════════════════════
لماذا ملف موحّد بدل الترجيح بالنوتبوك
═══════════════════════════════════════════════════════════════
الترجيح بالتكرار (repeat) كان يحقق التوزيع المستهدف بثمن مباشر:
**نفس المثال يتكرر ٨–١٢ مرة**، وفئة بـ4 أمثلة تصير 32 نسخة من أربع
جمل. هذا حفظ (memorization) لا تعميم.

هنا التوزيع يتحقق بـ**الاختيار** لا بالتكرار:
  • الفئة الكبيرة: عينة عشوائية بحجم الحصة المستهدفة (بلا تكرار)
  • الفئة الصغيرة: تدخل كاملة، وحصتها تُرفع بالتوليد لا بالنسخ
  • سقف تكرار صارم: MAX_DUP=2، ولا يُستعمل إلا للفئات السلوكية
    الحرجة اللي ما ممكن توسيعها آلياً

النتيجة ملف واحد جاهز للتدريب مباشرةً: `data/iraqi_final_train.jsonl`
مع `data/iraqi_final_val.jsonl` للتقييم.

الإخراج يطبع التوزيع الفعلي مقابل المستهدف حتى يكون كل رقم مُتحقَّقاً منه.
"""
import json
import random
import sys
from collections import Counter, defaultdict
from pathlib import Path

sys.stdout.reconfigure(encoding="utf-8")
random.seed(20260728)
DATA = Path(__file__).resolve().parent.parent / "data"

# ════════════════════════════════════════════════════════════════════
# التوزيع المستهدف (نسبة من الداتا العراقية، قبل إضافة Aya)
# ════════════════════════════════════════════════════════════════════
# ملاحظة على الحسابيات: النسب الخمس المطلوبة أصلاً تجمع 99%، وتترك 1%
# لكتلة «الحياة العامة» بـv8 (18,347 مثالاً = 15%+ من الداتا). فتخصيص
# حصة صريحة لها هنا، وتُخصم من حصة المبيعات لأنها أقرب لها موضوعياً.
TARGETS = {
    "sales":      0.46,   # مبيعات/كتالوج — الأساس
    "general":    0.15,   # حياة عامة (يومي/عمل/صحة/تعليم/عائلة...)
    "fluency":    0.13,   # سوالف/تحية/أمثال/نكت
    "off_topic":  0.11,   # رفض عام خارج نطاق البيع
    "behavioral": 0.09,   # v9–v14 السلوكية (items/gap/ord/cat)
    "qa":         0.06,   # QA عامة
}
MAX_DUP = 2          # سقف التكرار المطلق — كان ×12
TARGET_TOTAL = 95000  # حجم الداتا العراقية المستهدف

TRAIN_GLOBS = ["iraqi_train_v8_part*.jsonl", "iraqi_v9_generated*.jsonl",
               "iraqi_v10_*.jsonl", "iraqi_v11_gaps.jsonl",
               "iraqi_v12_order.jsonl", "iraqi_v13_scope.jsonl",
               "iraqi_v14_expand.jsonl", "iraqi_v15_behavioral.jsonl"]
VAL_GLOBS = ["iraqi_val_v8.jsonl", "iraqi_val_v13.jsonl"]

FLUENCY_PREFIX = ("greetings", "smalltalk", "proverbs", "jokes",
                  "praise_expressions", "negative_traits")
BEHAVIORAL_PREFIX = ("cat1_", "cat2_", "cat3_", "cat4_", "cat5_", "cat6_",
                     "extraction_", "items_", "gap1_", "gap2_", "gap3_",
                     "gap4_", "gap5_", "gap6_", "ord1_", "ord2_", "ord3_",
                     "ord4_", "ord5_", "ord6_", "natural_sale",
                     "sequential_refusal", "missing_info",
                     "order_total_no_number", "greetings_smalltalk")
SALES_PREFIX = ("grounded_", "json_", "sales_", "tool_call", "ataakadlak",
                "persistence_refusal", "confirm_later", "repeat_question",
                "praise_no_upsell", "order_no_upsell", "qa_bargaining",
                "qa_price")


def bucket_of(cat):
    if cat == "off_topic_refusal_general":
        return "off_topic"
    if cat.startswith(BEHAVIORAL_PREFIX):
        return "behavioral"
    if cat.startswith(FLUENCY_PREFIX):
        return "fluency"
    if cat.startswith(SALES_PREFIX):
        return "sales"
    if cat.startswith("qa_"):
        return "qa"
    return "general"


def load(globs):
    rows = []
    for g in globs:
        for f in sorted(DATA.glob(g)):
            for line in f.open(encoding="utf-8"):
                d = json.loads(line)
                d.setdefault("category", "?")
                rows.append(d)
    return rows


key = lambda m: json.dumps(m, ensure_ascii=False, sort_keys=True)


def main():
    train_raw, val = load(TRAIN_GLOBS), load(VAL_GLOBS)

    # ── تنظيف: تكرار حرفي داخل الخام ──
    seen, uniq = set(), []
    for r in train_raw:
        k = key(r["messages"])
        if k not in seen:
            seen.add(k)
            uniq.append(r)
    dup_raw = len(train_raw) - len(uniq)
    train_raw = uniq

    # ── تنظيف: تلوث train/val ──
    vkeys = {key(r["messages"]) for r in val}
    before = len(train_raw)
    train_raw = [r for r in train_raw if key(r["messages"]) not in vkeys]
    leak = before - len(train_raw)

    # ── تجميع بالكتلة والفئة ──
    by_bucket = defaultdict(lambda: defaultdict(list))
    for r in train_raw:
        by_bucket[bucket_of(r["category"])][r["category"]].append(r)

    # ── الاختيار: كل كتلة تُقلَّص أو تُكرَّر (بحد MAX_DUP) لحصتها ──
    out, report = [], []
    for b, target in TARGETS.items():
        cats = by_bucket.get(b, {})
        avail = sum(len(v) for v in cats.values())
        want = int(TARGET_TOTAL * target)
        rows = [r for v in cats.values() for r in v]

        if avail >= want:
            # وفرة: عينة عشوائية بلا أي تكرار — الحالة المثلى
            picked = random.sample(rows, want)
            dup = 1.0
        else:
            # نقص: نأخذ الكل، ثم نكرر بحد MAX_DUP **لكل محادثة**.
            # random.sample على rows*MAX_DUP يضمن المتوسط لا الحد الأقصى:
            # المصادفة تسحب نفس المثال مرتين من النسختين فيصير ×3 مع
            # الأصل. السحب من نسخة واحدة إضافية يحدّه بـ×2 قطعاً.
            picked = list(rows)
            need = min(want, avail * MAX_DUP) - avail
            for _ in range(MAX_DUP - 1):
                if need <= 0:
                    break
                take = min(need, avail)
                picked += random.sample(rows, take)
                need -= take
            dup = len(picked) / avail
        out.extend(picked)
        report.append((b, target, avail, len(picked), dup))

    random.shuffle(out)

    # ── كتابة: مقسّمة لأجزاء ──
    # الملف الموحّد يطلع ~95 MB، وحد GitHub الصلب 100 MB (وتحذير عند 50).
    # التقسيم لأربعة أجزاء يخلي كل جزء ~24 MB — تحت التحذير أصلاً، ويسهّل
    # الـdiff والسحب. النوتبوك يقراهن بـglob فيرجعن ملفاً واحداً بالذاكرة.
    N_PARTS = 4
    written = []
    per = -(-len(out) // N_PARTS)          # سقف القسمة
    for i in range(N_PARTS):
        chunk = out[i * per:(i + 1) * per]
        if not chunk:
            continue
        p = DATA / f"iraqi_final_train_part{i+1:02d}.jsonl"
        with p.open("w", encoding="utf-8") as fh:
            for r in chunk:
                fh.write(json.dumps(r, ensure_ascii=False) + "\n")
        written.append((p, len(chunk)))

    fva = DATA / "iraqi_final_val.jsonl"
    with fva.open("w", encoding="utf-8") as fh:
        for r in val:
            fh.write(json.dumps(r, ensure_ascii=False) + "\n")

    # الملف الموحّد القديم ما عاد مستعملاً — يُحذف حتى لا يُرفع بالغلط
    old = DATA / "iraqi_final_train.jsonl"
    if old.exists():
        old.unlink()

    # ════════════════════════════ التقرير ════════════════════════════
    tot = len(out)
    print("=" * 72)
    print("الملف الموحّد النهائي")
    print("=" * 72)
    print(f"  تنظيف: حُذف {dup_raw:,} مكرر حرفي + {leak:,} تلوث train/val")
    print()
    print(f"{'الكتلة':<14}{'مستهدف':>9}{'متاح خام':>11}{'المختار':>10}{'فعلي':>8}{'تكرار':>8}")
    for b, t, avail, n, dup in report:
        flag = "" if dup <= 1.001 else ("  ⚠️" if dup > 1.5 else "  ·")
        print(f"  {b:<12}{100*t:>8.0f}%{avail:>11,}{n:>10,}{100*n/tot:>7.1f}%{dup:>7.2f}×{flag}")
    print(f"  {'المجموع':<12}{'100%':>9}{'':>11}{tot:>10,}{100:>7.1f}%")

    # ── الحارس المباشر: أقصى تكرار لمحادثة واحدة ──
    # النسبة بالفئة ما تكفي — لازم يُقاس على مستوى المحادثة نفسها،
    # لأن هذا هو اللي يحفظه الموديل فعلاً.
    _mx = Counter(key(r["messages"]) for r in out).most_common(1)[0][1]
    assert _mx <= MAX_DUP, f"محادثة مكررة {_mx} مرات — السقف {MAX_DUP}"

    uniq_n = len({key(r["messages"]) for r in out})
    print()
    print(f"  محادثات فريدة       {uniq_n:>9,}  ({100*uniq_n/tot:.1f}%)")
    print(f"  نسخ مكررة           {tot-uniq_n:>9,}  ({100*(tot-uniq_n)/tot:.1f}%)")
    print(f"  فئات                {len(set(r['category'] for r in out)):>9}")
    print(f"  التقييم             {len(val):>9,}")

    # ── فحص الحفظ: أي فئة تكررت أكثر من MAX_DUP ──
    cc = Counter(r["category"] for r in out)
    raw_cc = Counter(r["category"] for r in train_raw)
    risky = [(c, raw_cc[c], n) for c, n in cc.items()
             if raw_cc[c] and n / raw_cc[c] > MAX_DUP + 0.01]
    if risky:
        print(f"\n⚠️ {len(risky)} فئة تجاوزت سقف التكرار ×{MAX_DUP}:")
        for c, r0, n in sorted(risky, key=lambda x: -x[2] / x[1])[:10]:
            print(f"   {c:<34}{r0:>5} → {n:>6,}  (×{n/r0:.1f})")
    else:
        print(f"\n✅ ولا فئة تجاوزت سقف التكرار ×{MAX_DUP}")

    # ── فحص: أصغر الفئات ونسبة تكرارها ──
    thin = sorted(((c, raw_cc[c], cc[c]) for c in cc if raw_cc[c] < 100),
                  key=lambda x: x[1])[:12]
    if thin:
        print(f"\nأصغر الفئات (خام < 100) — للمتابعة:")
        for c, r0, n in thin:
            print(f"   {c:<34}{r0:>5} خام → {n:>6,} بالملف  (×{n/max(r0,1):.1f})")

    # ── فحص التغطية التقييمية ──
    tr_c = set(cc)
    va_c = set(r["category"] for r in val)
    miss = sorted(tr_c - va_c)
    print(f"\n{'✅ كل فئة تدريب مقيسة' if not miss else f'⚠️ {len(miss)} فئة بلا تقييم: {miss[:8]}'}")

    print(f"\n📁 الملفات المكتوبة:")
    for p, n in written:
        print(f"   {p.name:<36}{n:>8,} مثال{p.stat().st_size/1048576:>9.1f} MB")
    print(f"   {fva.name:<36}{len(val):>8,} مثال{fva.stat().st_size/1048576:>9.1f} MB")
    _mx_mb = max(p.stat().st_size for p, _ in written) / 1048576
    print(f"\n{'✅' if _mx_mb < 50 else '⚠️'} أكبر جزء {_mx_mb:.1f} MB "
          f"(حد GitHub الصلب 100 MB، والتحذير عند 50 MB)")


if __name__ == "__main__":
    main()
