# -*- coding: utf-8 -*-
"""
بناء نسخة v16 — ثلث الحجم، أوزان معدّلة على نتائج القياس.

═══════════════════════════════════════════════════════════════
لماذا الثلث
═══════════════════════════════════════════════════════════════
95,000 مثال مو ميزة بحد ذاتها. القياس طلع 8/11 و17/25، والفشل ما كان
من قلة الأمثلة — كان من **تناقضها**. تقليل الحجم للثلث (31,667):
  • يقصّر زمن الحقبة ثلاث مرات -> تجارب أسرع على checkpoints
  • يقلل هيمنة الكتل الضخمة (off_topic كانت 10,450 مثالاً لسلوك واحد)
  • الجودة بعد إصلاح v16 أعلى، فالمثال الواحد يعلّم أكثر

═══════════════════════════════════════════════════════════════
لماذا هذي الأوزان
═══════════════════════════════════════════════════════════════
الأوزان القديمة وزّعت بالموضوع. الجديدة توزّع بـ**ما فشل بالقياس**:

  off_topic  11% -> 6%   الرفض العام كان 10,450 مثالاً وينجح أصلاً
                          (رفض 2/3). حجمه كان يزاحم السلوكيات الأدق.
  behavioral  9% -> 20%  كل الفشل تقريباً هنا: الحقل الناقص (س1)،
                          الاجمالي (حساب 1/5)، بوابة التأكيد. الكتلة
                          كانت 9% وتحمل أثقل سلوك مطلوب.
  sales      46% -> 38%  تبقى الأكبر، بس 46% كانت فائضة: `sales`
                          ناجحة بالقياس (السعر حرفياً ✅، الثبات ✅).
  fluency    13% -> 16%  اللهجة فشلت (2/3، و84.5% من الأدوار
                          الاجتماعية بأقل من ماركرين).
  general    15% -> 12%  ما تُقاس بالفحص، تكفي للحفاظ على العمومية.
  qa          6% -> 8%   الضمان/المواصفة (س8) تتعلّم من هنا.

MAX_DUP يبقى 2، والحارس على مستوى المحادثة كما هو.
"""
import json
import random
import sys
from collections import Counter, defaultdict
from pathlib import Path

sys.stdout.reconfigure(encoding="utf-8")
random.seed(20260728)

ROOT = Path(__file__).resolve().parent.parent
DATA = ROOT / "data"
SRC = DATA / "v16"          # المصدر: المصلَّح، لا الخام

TARGETS = {
    "sales":      0.38,
    "behavioral": 0.20,
    "fluency":    0.16,
    "general":    0.12,
    "qa":         0.07,
    "off_topic":  0.08,
}
MAX_DUP = 2
TARGET_TOTAL = 31667        # ثلث 95,000

TRAIN_GLOBS = ["iraqi_train_v8_part*.jsonl", "iraqi_v9_generated*.jsonl",
               "iraqi_v10_*.jsonl", "iraqi_v11_gaps.jsonl",
               "iraqi_v12_order.jsonl", "iraqi_v13_scope.jsonl",
               "iraqi_v14_expand.jsonl", "iraqi_v15_behavioral.jsonl",
               "iraqi_v16_missing_field.jsonl", "iraqi_v16_thin.jsonl",
               "iraqi_v17_deep_refusal.jsonl",
               "iraqi_v19_offtopic_tiers.jsonl",
               "iraqi_v20_cosmetics_identity.jsonl",
               "iraqi_v25_grounded_free.jsonl",
               "iraqi_v26_consistency.jsonl",
               "iraqi_v27_eval_gaps.jsonl",
               "iraqi_v28_promise_dialect.jsonl"]
VAL_GLOBS = ["iraqi_val_v8.jsonl", "iraqi_val_v13.jsonl",
             "iraqi_v16_val_extra.jsonl", "iraqi_v17_val_extra.jsonl",
             "iraqi_v19_val_extra.jsonl",
             "iraqi_v20_val_extra.jsonl",
             "iraqi_v25_val_extra.jsonl",
             "iraqi_v26_val_extra.jsonl",
             "iraqi_v27_val_extra.jsonl",
             "iraqi_v28_val_extra.jsonl"]

FLUENCY_PREFIX = ("greetings", "smalltalk", "proverbs", "jokes",
                  "praise_expressions", "negative_traits",
                  # v28 — كثافة الماركر العراقي بالكلام الاجتماعي
                  "casual_dialect_dense")
BEHAVIORAL_PREFIX = ("cat1_", "cat2_", "cat3_", "cat4_", "cat5_", "cat6_",
                     "extraction_", "items_", "gap1_", "gap2_", "gap3_",
                     "gap4_", "gap5_", "gap6_", "gap7_", "ord1_", "ord2_",
                     "ord3_", "ord4_", "ord5_", "ord6_", "natural_sale",
                     "sequential_refusal", "missing_info",
                     "order_total_no_number", "greetings_smalltalk",
                     "deep_refusal_in_sales",
                     # v26 — الإلغاء إعادة ضبط حالة، فهو سلوك لا بيع
                     "cancel_state_reset", "cancel_requantify",
                     "cancel_switch_item",
                     # v28 — وعد الحساب النظيف بلا رقم جزئي
                     "order_total_clean_promise")
SALES_PREFIX = ("grounded_", "json_", "sales_", "tool_call", "ataakadlak",
                "cosmetics_",
                "persistence_refusal", "confirm_later", "repeat_question",
                "praise_no_upsell", "order_no_upsell", "qa_bargaining",
                "qa_price",
                # v26 — ثبات الرقم، قائمة الفئة، وصيغ الرفض القياسية
                "price_consistency_", "price_doubt_vs_bargain",
                "category_list_", "reject_standard_", "reject_consistency_",
                # v27 — نواقص كشفها التقييم
                "price_doubt_merged", "ambiguous_", "reject_clean_",
                "reject_then_alt_", "reject_sequential_", "reject_two_brands_")

# ── الفئات الحرجة: لا تنزل تحت حد أدنى مهما كانت حصة كتلتها ──
# `random.sample` على مستوى الكتلة يسحب بالتناسب، فالفئة اللي حجمها 40
# تنسحب لـ13 مثالاً بالثلث — وهي بالضبط الفئات اللي فشل عليها القياس.
# الحد الأدنى يضمن بقاءها، والفائض ينخصم من أكبر فئة بنفس الكتلة.
FLOORS = {
    "gap7_missing_field_ask": 560,   # س1 — الحقل الناقص
    "deep_refusal_in_sales":  900,   # v17 — الامتناع داخل زخم البيع
    # v19 — الطبقة الطبية قاعدة سلامة، ما تنسحب بالتناسب أبداً
    "off_topic_medical_strict": 900,
    "off_topic_general_polite": 300,
    "off_topic_product_alt":    300,
    "off_topic_seller_identity": 420,   # v20 — هوية البائع بالرفض
    "cosmetics_sale":           420,   # v20 — الكوزمتك بضاعة لا دواء
    "cosmetics_medical_edge":   240,
    # v25 — المجانية المؤسَّسة: بلاها الموديل يتعلم «ما تگول بلاش أبداً»
    "grounded_free_delivery":   340,
    "grounded_free_install":    200,
    "grounded_free_threshold":  200,
    "grounded_free_edge":       260,
    # ── v26 ──
    # ثبات الرقم تحت التشكيك: الفشل الوحيد المؤكد بالقياس الأخير.
    # التشكيك ≠ مساومة — بلا `price_doubt_vs_bargain` يرجع الخلط.
    "price_consistency_doubt":  520,
    "price_consistency_triple": 300,
    "price_doubt_vs_bargain":   300,
    # قائمة الفئة: 1,295 محادثة تسأل، وولا وحدة تعدّد
    "category_list_request":    280,
    "category_list_more":       240,
    "category_list_single":     140,
    # الإلغاء إعادة ضبط: الاجمالي الملغى كان يتسرّب للرد التالي
    "cancel_state_reset":       300,
    "cancel_requantify":        200,
    "cancel_switch_item":       200,
    # صيغ رفض قياسية — منوال يسهل قياسه، والتنويع القديم يبقى ذيلاً
    "reject_standard_form":     220,
    "reject_standard_with_list": 180,
    "reject_consistency_doubt": 200,

    # ── v27: نواقص كشفتها ردود الموديل بالتقييم ──
    "price_doubt_merged":       600,   # التشكيك المدموج — صفر تغطية قبلها
    "price_doubt_merged_short": 260,
    "ambiguous_partial_both":   260,   # وصف جزئي يطابق صنفين
    "ambiguous_after_first":    300,
    "reject_clean_no_alt":        420, # رفض بلا بديل غير مطلوب
    "reject_then_alt_on_request": 260,
    "reject_sequential_named":    360,
    "reject_two_brands_named":    200,

    "order_total_no_number":  260,   # حساب — الاجمالي بلا اختراع
    "cat5_sum_over_precomputed": 200,
    "ord3_confirm_gate":      300,
    "ord2_marker_withheld":   300,
    "ord1_marker_positive":   300,
    "cat1_warranty_detail":   320,   # س8 — الضمان
    "cat2_spec_deflection":   200,
    "ord4_submit_refusal":    120,
    "ord5_tool_empty":        120,
    "ord6_tool_status_args":  120,
    "gap6_anti_sycophancy":   120,
    "gap2_smalltalk_return":  120,
    "extraction_city_preserve": 150,
    "extraction_name_no_marker": 150,
    "cat3_policy_invention":  180,
    "cat4_topic_swap":        150,
    "cat6_conditional_coherence": 150,

    # ── v28: وعد الحساب النظيف + كثافة اللهجة الاجتماعية ──
    # order_total_no_number (277 مثال) كلها دور وحيد وتكرر السعر
    # المفرد قبل الوعد — صفر تغطية للوعد **النظيف** بلا أي رقم،
    # وصفر تغطية للسيناريو المرکّب (سعر+بديل+فرق ثم كمية+تركيب).
    "order_total_clean_promise":       300,
    "order_total_clean_promise_short": 180,
    # 61.4% من 3,041 محادثة اجتماعية بأقل من 3 ماركرات عراقية —
    # الفشل بالكلام الاجتماعي تحديداً لا كلام البيع.
    "casual_dialect_dense":            340,
}


# الطبقات الثلاث (v19) + الفئة القديمة، كلها كتلة واحدة بالتوزيع
OFF_TOPIC_CATS = ("off_topic_refusal_general", "off_topic_medical_strict",
                  "off_topic_general_polite", "off_topic_product_alt",
                  "off_topic_seller_identity")


def bucket_of(cat):
    if cat in OFF_TOPIC_CATS:
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


def load(globs, base):
    rows = []
    for g in globs:
        for f in sorted(base.glob(g)):
            for line in f.open(encoding="utf-8"):
                d = json.loads(line)
                d.setdefault("category", "?")
                rows.append(d)
    return rows


key = lambda m: json.dumps(m, ensure_ascii=False, sort_keys=True)


def pick_with_floors(cats, want):
    """يسحب `want` مثالاً من كتلة، مع احترام الحد الأدنى للفئات الحرجة."""
    picked, remaining = [], want

    # ١) الفئات الحرجة أولاً — الحد الأدنى أو كل المتاح
    floored = {c: v for c, v in cats.items() if c in FLOORS}
    for c, rows in floored.items():
        n = min(FLOORS[c], len(rows), remaining)
        if n <= 0:
            continue
        picked += random.sample(rows, n) if n <= len(rows) else list(rows)
        remaining -= n

    # ٢) الباقي بالتناسب من الفئات غير الحرجة
    rest = [r for c, v in cats.items() if c not in FLOORS for r in v]
    # الفائض من الحرجة (اللي تجاوز حده) يدخل بالمسابقة العامة هم
    for c, rows in floored.items():
        n = min(FLOORS[c], len(rows))
        if len(rows) > n:
            rest += rows[n:]

    if remaining > 0 and rest:
        if len(rest) >= remaining:
            picked += random.sample(rest, remaining)
        else:
            picked += list(rest)
            need = remaining - len(rest)
            for _ in range(MAX_DUP - 1):
                if need <= 0:
                    break
                take = min(need, len(rest))
                picked += random.sample(rest, take)
                need -= take
    return picked


def main():
    if not SRC.exists():
        sys.exit("❌ data/v16 مو موجود — شغّل scripts/fix_v16_contradictions.py أولاً")

    train_raw, val = load(TRAIN_GLOBS, SRC), load(VAL_GLOBS, DATA)

    # ── تنظيف: تكرار حرفي ──
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

    by_bucket = defaultdict(lambda: defaultdict(list))
    for r in train_raw:
        by_bucket[bucket_of(r["category"])][r["category"]].append(r)

    out, report = [], []
    for b, target in TARGETS.items():
        cats = by_bucket.get(b, {})
        avail = sum(len(v) for v in cats.values())
        want = int(TARGET_TOTAL * target)
        picked = pick_with_floors(cats, want)
        out.extend(picked)
        report.append((b, target, avail, len(picked),
                       len(picked) / max(avail, 1)))

    random.shuffle(out)

    # ── كتابة ──
    N_PARTS = 2                       # الثلث يطلع ~32 MB -> جزءان
    written = []
    per = -(-len(out) // N_PARTS)
    for i in range(N_PARTS):
        chunk = out[i * per:(i + 1) * per]
        if not chunk:
            continue
        p = DATA / f"iraqi_v16_train_part{i+1:02d}.jsonl"
        with p.open("w", encoding="utf-8") as fh:
            for r in chunk:
                fh.write(json.dumps(r, ensure_ascii=False) + "\n")
        written.append((p, len(chunk)))

    fva = DATA / "iraqi_v16_val.jsonl"
    with fva.open("w", encoding="utf-8") as fh:
        for r in val:
            fh.write(json.dumps(r, ensure_ascii=False) + "\n")

    # ════════════════════════ التقرير ════════════════════════
    tot = len(out)
    print("=" * 74)
    print(f"نسخة v16 — {tot:,} مثال (ثلث 95,000)")
    print("=" * 74)
    print(f"  تنظيف: {dup_raw:,} مكرر حرفي + {leak:,} تلوث train/val")
    print()
    print(f"{'الكتلة':<14}{'مستهدف':>9}{'متاح':>10}{'المختار':>10}{'فعلي':>8}{'سحب':>8}")
    for b, t, avail, n, ratio in report:
        print(f"  {b:<12}{100*t:>8.0f}%{avail:>10,}{n:>10,}"
              f"{100*n/tot:>7.1f}%{ratio:>7.2f}×")
    print(f"  {'المجموع':<12}{'100%':>9}{'':>10}{tot:>10,}{100:>7.1f}%")

    _mx = Counter(key(r["messages"]) for r in out).most_common(1)[0][1]
    assert _mx <= MAX_DUP, f"محادثة مكررة {_mx} مرات — السقف {MAX_DUP}"

    uniq_n = len({key(r["messages"]) for r in out})
    print()
    print(f"  محادثات فريدة   {uniq_n:>8,}  ({100*uniq_n/tot:.1f}%)")
    print(f"  فئات            {len(set(r['category'] for r in out)):>8}")
    print(f"  التقييم         {len(val):>8,}")

    # ── الفئات الحرجة: تحققت من حدها؟ ──
    cc = Counter(r["category"] for r in out)
    print(f"\n  الفئات الحرجة (الحد الأدنى مضمون):")
    miss = []
    for c, floor in sorted(FLOORS.items(), key=lambda x: -x[1]):
        got = cc.get(c, 0)
        ok = "✅" if got >= min(floor, 1) else "❌"
        if got < floor * 0.9:
            miss.append(c)
        print(f"    {ok} {c:<32}{got:>6} / {floor}")
    if miss:
        print(f"    ⚠️ تحت الحد: {miss}")

    tr_c, va_c = set(cc), set(r["category"] for r in val)
    gap = sorted(tr_c - va_c)
    print(f"\n{'✅ كل فئة تدريب مقيسة' if not gap else f'⚠️ {len(gap)} فئة بلا تقييم: {gap}'}")

    print(f"\n📁 الملفات:")
    for p, n in written:
        print(f"   {p.name:<34}{n:>7,} مثال{p.stat().st_size/1048576:>8.1f} MB")
    print(f"   {fva.name:<34}{len(val):>7,} مثال{fva.stat().st_size/1048576:>8.1f} MB")


if __name__ == "__main__":
    main()
