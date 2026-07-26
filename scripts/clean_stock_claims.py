# -*- coding: utf-8 -*-
"""
تنظيف ادعاءات المخزون/الندرة والخصومات غير المكتوبة من بيانات التدريب والتقييم.

═══════════════════════════════════════════════════════════════════
لماذا هذا السكربت
═══════════════════════════════════════════════════════════════════
ملف AA.md (قسم 2) يمنع منعاً باتاً بردود البائع:
  - ادعاء المخزون: «باقي حبتين»، «آخر قطعة»
  - ادعاء الندرة أو المبيعات: «مبيعة من الأسبوع الماضي»، «ما يجي ثاني»
  - عروض أو خصومات غير مكتوبة بالكتالوج: «سعر خاص»، «على خاطرك آخر سعر»

لكن القياس الفعلي وجد أن هذا المنع لم يُطبَّق برمجياً أبداً: التلوث أصله
بيانات v4 القديمة، وانتقل بالوراثة لـv6 وv7 وv8 لأن سكربتات
prepare_v*_data.py نظّفت اللهجة والأرقام فقط.

الأخطر: ملف التقييم iraqi_val_v8.jsonl ملوّث هو الآخر — أي أن eval_loss
و load_best_model_at_end و EarlyStoppingCallback **تكافئ** النموذج على
تقليد السلوك الممنوع. تنظيف التدريب وحده لا يكفي: لو بقي التقييم ملوثاً،
تحسّن النموذج الحقيقي يظهر كتدهور بالمقياس.

هذا التلوث ينقض مباشرة فئة gap6_anti_sycophancy بدفعة v11 (الصمود تحت
الضغط) — ومهما رُجّحت v11 تبقى v8 أكبر، فالحذف هو الحل الوحيد.

═══════════════════════════════════════════════════════════════════
مبدأ الحذف
═══════════════════════════════════════════════════════════════════
الفحص يجري على **ردود assistant فقط** — كلام الزبون حر (زبون يقول «سمعت
عدكم خصم» شيء مشروع وواقعي، والمطلوب أن يرد البائع بلا تنازل).

تُحذف المحادثة كاملة عند أول رد مخالف، لا الرسالة وحدها: بقاء باقي
المحادثة بلا الرد المخالف يكسر التسلسل ويترك سياقاً معلقاً.

الاستثناءات (allowlist) تمنع الإيجابيات الكاذبة — مثل «ما يشمله» بسياق
تفصيل ضمان مكتوب بالكتالوج، وهي سلوك مطلوب لا مخالفة.

الاستعمال:
    python scripts/clean_stock_claims.py            # تقرير فقط، لا يكتب شيئاً
    python scripts/clean_stock_claims.py --apply    # ينفّذ الحذف ويكتب الملفات
"""
import argparse
import json
import re
import shutil
import sys
from collections import Counter, defaultdict
from pathlib import Path

sys.stdout.reconfigure(encoding="utf-8")
DATA = Path(__file__).resolve().parent.parent / "data"

# ════════════════════════════════════════════════════════════════
# أنماط المخالفة — مطبّقة على ردود assistant حصراً
# ════════════════════════════════════════════════════════════════
PATTERNS = {
    "ادعاء مخزون/ندرة": re.compile(
        r"آخر قطعة|اخر قطعة|آخر حبة|اخر حبة|آخر وحدة|اخر وحدة"
        r"|باقي حبتين|باقي وحدة|باقي حبة|باقي بس"
        r"|ما يجي ثاني|ما تجي ثاني|ما يجي غيره"
        r"|مبيعة|نفدت|نفذت|خلصت الكمية|الكمية قليلة|كميات محدودة"
        r"|طلب هواي علي|عليه طلب هواي|الكل يطلبه|الكل ياخذه"
    ),
    "خصم/سعر غير مكتوب": re.compile(
        r"سعر خاص|خاص الك|خاصة الك|خصم خاص|نزلتها الك|نزلته الك"
        r"|على خاطرك.{0,25}(?:آخر سعر|اخر سعر)"
        r"|سوينالك خصم|أعطيك خصم|انطيك خصم|اعطيك خصم"
        r"|للزبائن القدام|بدل \d"
    ),
    "عرض محدود بالوقت": re.compile(
        r"لحد نهاية اليوم|لحد نهاية الأسبوع|لحد نهاية الاسبوع"
        r"|بكره يرجع للسعر|يرجع للسعر الأصلي|العرض ينتهي|لفترة محدودة"
    ),
    "وعد توفير غير مضمون": re.compile(
        r"راح نوفره|نوفرلك|نجيبه الك|نطلبه الك|بالوجبة الجاية|يوصل قريب"
    ),
    "إطراء متودد": re.compile(
        r"سؤال ممتاز|سؤال حلو|سؤال رائع|من ذوقك|اختيار موفق"
        r"|عندك حق تماما|كلامك صحيح 100|عيونك الحلوة"
    ),
}

# استثناءات: عبارات تطابق النمط لكنها سلوك مطلوب لا مخالفة
ALLOW = re.compile(
    r"ما يشمله?|ما يغطي|ما يشمل الكسر"      # تفصيل ضمان مكتوب بالكتالوج (v10)
    r"|ما عندي خصم|ما عدنا خصم|ماكو خصم|الخصومات ما"   # نفي الخصم = مطلوب
    r"|ما أگدر أنطي|ما اگدر انطي|ما بيدي"    # رفض صريح
)


def violations_in(reply):
    """يرجع قائمة أسماء المخالفات بهذا الرد، بعد استبعاد الاستثناءات."""
    if ALLOW.search(reply):
        return []
    return [lab for lab, rx in PATTERNS.items() if rx.search(reply)]


def scan(path):
    """يفحص ملفاً — يرجع (كل الأسطر، مؤشرات الملوثة، عدّاد الأنواع، أمثلة)."""
    rows, dirty, kinds, samples = [], [], Counter(), defaultdict(list)
    with open(path, encoding="utf-8") as f:
        for i, line in enumerate(f):
            line = line.rstrip("\n")
            if not line.strip():
                continue
            rows.append(line)
            try:
                r = json.loads(line)
            except json.JSONDecodeError:
                continue
            for m in r.get("messages", []):
                if m.get("role") != "assistant":
                    continue
                labs = violations_in(m.get("content", ""))
                if labs:
                    dirty.append(len(rows) - 1)
                    for lab in labs:
                        kinds[lab] += 1
                        if len(samples[lab]) < 3:
                            samples[lab].append(m["content"][:100])
                    break
    return rows, dirty, kinds, samples


# الملفات المستعملة فعلياً بالنوت بوك (تدريب + تقييم)
TARGETS = [
    "iraqi_train_v8_part01.jsonl",
    "iraqi_train_v8_part02.jsonl",
    "iraqi_train_v8_part03.jsonl",
    "iraqi_val_v8.jsonl",          # ← ملف التقييم: الأهم
    "iraqi_v9_generated.jsonl",
    "iraqi_v9_generated_extra.jsonl",
]


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--apply", action="store_true",
                    help="ينفّذ الحذف فعلياً (بدونه تقرير فقط)")
    args = ap.parse_args()

    print("═" * 72)
    print("فحص ادعاءات المخزون/الندرة/الخصومات غير المكتوبة".center(66))
    print("═" * 72)

    all_kinds = Counter()
    total_rows = total_dirty = 0
    plans = []

    for fname in TARGETS:
        path = DATA / fname
        if not path.exists():
            print(f"\n⚠️ {fname} غير موجود — تخطٍ")
            continue
        rows, dirty, kinds, samples = scan(path)
        total_rows += len(rows)
        total_dirty += len(dirty)
        all_kinds += kinds
        plans.append((path, rows, set(dirty)))

        tag = "  ← ملف التقييم" if "val" in fname else ""
        pct = 100 * len(dirty) / len(rows) if rows else 0
        mark = "✅" if not dirty else "⚠️"
        print(f"\n{mark} {fname}{tag}")
        print(f"   {len(dirty):,} محادثة مخالفة من {len(rows):,} ({pct:.2f}%)")
        for lab, c in kinds.most_common():
            print(f"      {lab:<24}{c:>6,}")
            for s in samples[lab][:2]:
                print(f"          • {s}")

    print("\n" + "═" * 72)
    print(f"المجموع: {total_dirty:,} محادثة مخالفة من {total_rows:,} "
          f"({100 * total_dirty / total_rows:.2f}%)")
    print("\nتوزيع أنواع المخالفة:")
    for lab, c in all_kinds.most_common():
        print(f"   {lab:<24}{c:>7,}")

    if not args.apply:
        print("\n" + "─" * 72)
        print("هذا تقرير فقط — لم يُكتب أي ملف.")
        print("للتنفيذ:  python scripts/clean_stock_claims.py --apply")
        return

    # ── التنفيذ ──
    print("\n" + "═" * 72)
    print("التنفيذ: نسخ احتياطية ثم كتابة الملفات النظيفة")
    print("═" * 72)
    backup = DATA / "_backup_pre_clean"
    backup.mkdir(exist_ok=True)
    for path, rows, dirty in plans:
        bak = backup / path.name
        if not bak.exists():
            shutil.copy2(path, bak)
        kept = [r for i, r in enumerate(rows) if i not in dirty]
        with open(path, "w", encoding="utf-8", newline="\n") as f:
            for r in kept:
                f.write(r + "\n")
        print(f"   {path.name:<34} {len(rows):>7,} → {len(kept):>7,}  "
              f"(حُذف {len(dirty):,})")
    print(f"\n✅ النسخ الاحتياطية بـ {backup}")
    print("   للتراجع: انسخ الملفات من هناك فوق data/")


if __name__ == "__main__":
    main()
