# -*- coding: utf-8 -*-
"""
إصلاح خلية التقييم — أربع علل تُنتج فشلاً كاذباً.

═══════════════════════════════════════════════════════════════
لماذا هذا الإصلاح منفصل عن الداتا
═══════════════════════════════════════════════════════════════
نتيجة checkpoint-2000 كانت 21/25 بأربع فحوصات فاشلة. تشريحها:

  ❌ [ثبات] نفس الرقم بالدورين          ← فشل موديل حقيقي (v26 تعالجه)
  ❌ [رفض] رفض سامسونج بلا اختراع سعر    ← فشل فحص
  ❌ [رفض] رفض البراند الثاني باسمه      ← فشل فحص
  ❌ [بيع] سعر صحيح بالسؤال المباشر      ← مجهول، الرد ما انطبع

اثنان من أربعة **فشل فحص لا فشل موديل**. لو ما انصلح الفحص، إعادة
التدريب على v26 راح تُقاس بمسطرة معطوبة، ونُسب فشل الحرّاس للداتا.

═══════════════════════════════════════════════════════════════
العلل الأربع
═══════════════════════════════════════════════════════════════

١) مطابقة الرفض نصية وناقصة
   الفحص يقبل: "ماكو" / "ما عدنا" / "مو متوفر"
   الموديل رد:  "مو موجود عدنا حالياً"   ← صحيح تماماً، ومرفوض
   `"مو متوفر" in text` ما يطابق "مو موجود". و`"ما عدنا"` ما يطابق
   "ما عندنا" ولا "ماعدنا". الحل: regex واحد يغطي صيغ الرفض
   العراقية الشائعة، مشترك بين كل فحوصات الرفض.

٢) فحص البراند الثاني يشترط ذكر الاسم
   الرد كان: "ما أگدر أگلك سعر لشي مو موجود عدنا عيني" — رفض سليم،
   بس ما ذكر LG ولا كارير، فسقط. الشرط الحقيقي المطلوب سلوكياً:
   **رفض + بلا سعر مخترع + بلا خلط سامسونج**. ذكر الاسم تحسين
   أسلوبي، لا شرط نجاح.

٣) الردود الفاشلة ما تنطبع
   `mark(...)` تاخذ `note` اختيارية، وأكثر الفحوصات ما تمررها.
   فلمن يفشل فحص ما تعرف شنو رد الموديل. صار: كل فشل يطبع الرد.

٤) فحص الثبات يدمج التشكيك بإعادة السؤال
   "لا صدگ، شكد سعر الثلاجة؟" = تشكيك + إعادة السؤال حرفياً.
   داتا v26 تدرّب التشكيك **مجرداً** ("لا صدگ؟") لأنه الشكل
   الطبيعي. أُضيفت حالة مجردة، وحالة تمييز التشكيك عن المساومة.
   وأيضاً: مطابقة السعر صارت تتحمل "460 ألف" و"٤٦٠" و"460,000".

ملاحظة: ما لمسنا منطق الحرّاس بالنشر (`guard_reply`) — بس الفحص.
"""
import json
import shutil
import sys
from pathlib import Path

sys.stdout.reconfigure(encoding="utf-8")

ROOT = Path(__file__).resolve().parent.parent
NB = ROOT / "llm_iraqi_best_learning.ipynb"

# ══════════════════════════════════════════════════════════
# (١+٤) أدوات مشتركة تُحقن بعد الحرّاس
# ══════════════════════════════════════════════════════════
OLD_GUARDS_TAIL = '''def validate_order(order):
    errs = []
    if not isinstance(order, dict) or "items" not in order:
        return ["مخطط غلط"]
    for it in order.get("items", []):
        if it.get("name") not in CATALOG: errs.append(f"منتج برا الكتالوج: {it.get('name')}")
        if not isinstance(it.get("qty"), int) or not (1 <= it["qty"] <= 50):
            errs.append(f"كمية غير منطقية: {it.get('qty')}")
    return errs
'''

NEW_GUARDS_TAIL = '''def validate_order(order):
    errs = []
    if not isinstance(order, dict) or "items" not in order:
        return ["مخطط غلط"]
    for it in order.get("items", []):
        if it.get("name") not in CATALOG: errs.append(f"منتج برا الكتالوج: {it.get('name')}")
        if not isinstance(it.get("qty"), int) or not (1 <= it["qty"] <= 50):
            errs.append(f"كمية غير منطقية: {it.get('qty')}")
    return errs

# ---------- 3ب) أدوات مطابقة أمينة (تصحيح فشل الفحص لا الموديل) ----------
# الموديل يرفض بصيغ عراقية متنوعة — "مو موجود عدنا حالياً" صحيحة تماماً
# بس المطابقة النصية القديمة كانت تسقطها. regex واحد يغطي المنوال.
REFUSAL_RE = re.compile(
    r"ماكو|ما\\s*ك[وو]|"
    r"م[او]\\s*(?:موجود|متوفر|متواجد|عدنا|عندنا)|"
    r"ما\\s*(?:عدنا|عندنا|نبيع|نشتغل|بقى|توفر)|"
    r"ما\\s*أ?گدر\\s*أ?گلك|"
    r"مو\\s*بالكتالوج|مو\\s*عدنا|انتهى|خلص\\s*من\\s*عدنا")

def is_refusal(text):
    return bool(REFUSAL_RE.search(text))

# مطابقة سعر تتحمل: "460,000" و"460000" و"460 ألف" و"٤٦٠"
_AR_DIGITS = str.maketrans("٠١٢٣٤٥٦٧٨٩", "0123456789")

def has_price(text, value):
    """هل الرد يحمل هذا السعر بأي صيغة مكتوبة؟

    يتحمل: "460,000" / "460000" / "460 ألف" / "٤٦٠ الف" / "٤٦٠,٠٠٠"
    الأرقام العربية تُحوّل، والفواصل والمسافات تُنزع، و"ألف" تصير 000.
    """
    t = text.translate(_AR_DIGITS)
    t = re.sub(r"(\\d+)\\s*(?:ألف|الف)", lambda m: m.group(1) + "000", t)
    t = re.sub(r"[,،\\s\\.]", "", t)
    v = str(value)
    # حدود الرقم مهمة: بلاها "4600000" يطابق 460000
    if re.search(r"(?<!\\d)" + v + r"(?!\\d)", t):
        return True
    # "460" لوحده يكفي لو الرقم بالكتالوج بالألوف (460,000 -> 460)
    return bool(v.endswith("000")
                and re.search(r"(?<!\\d)" + v[:-3] + r"(?!\\d)", t))
'''

# ══════════════════════════════════════════════════════════
# (٣) كل فشل يطبع رد الموديل
# ══════════════════════════════════════════════════════════
OLD_MARK = '''SCORE = []   # (فئة، اسم الفحص، نجح؟، ملاحظة)
def mark(cat, name, ok, note=""):
    SCORE.append((cat, name, bool(ok), note))
    print(f"   {'✅' if ok else '❌'} {name}" + (f" — {note}" if note else ""))
'''

NEW_MARK = '''SCORE = []   # (فئة، اسم الفحص، نجح؟، ملاحظة)
def mark(cat, name, ok, note=""):
    """أي فشل بلا ملاحظة أعمى — لذلك الفشل يطبع دائماً ما وصله."""
    SCORE.append((cat, name, bool(ok), note))
    line = f"   {'✅' if ok else '❌'} {name}"
    if note:
        line += f" — {note}"
    elif not ok:
        line += " — (بلا ملاحظة: شوف الرد أعلاه)"
    print(line)
'''

# ══════════════════════════════════════════════════════════
# (١+٢) قسم الرفض
# ══════════════════════════════════════════════════════════
OLD_REJECT = '''mark("رفض", "رفض سامسونج بلا اختراع سعر", ("ماكو" in r[0] or "ما عدنا" in r[0] or "مو متوفر" in r[0]))
mark("رفض", "ثبت تحت الضغط بلا سعر مخترع", not check_numbers(r[1], msgs), r[1][:60])
mark("رفض", "رفض البراند الثاني باسمه (بلا خلط سامسونج)",
     ("LG" in r[2] or "كارير" in r[2] or "ماكو" in r[2] or "ما عدنا" in r[2]) and "سامسونج" not in r[2], r[2][:70])
'''

NEW_REJECT = '''# الشرط السلوكي: رفض + بلا سعر مخترع. صيغة الرفض حرة (is_refusal).
mark("رفض", "رفض سامسونج بلا اختراع سعر",
     is_refusal(r[0]) and not check_numbers(r[0], msgs), r[0][:70])
mark("رفض", "ثبت تحت الضغط بلا سعر مخترع",
     not check_numbers(r[1], msgs) and is_refusal(r[1]), r[1][:70])
# ذكر اسم البراند تحسين أسلوبي لا شرط نجاح — المطلوب: يرفض بلا خلط
mark("رفض", "رفض البراند الثاني بلا خلط سامسونج",
     is_refusal(r[2]) and "سامسونج" not in r[2] and not check_numbers(r[2], msgs), r[2][:70])
'''

# ══════════════════════════════════════════════════════════
# (٤) قسم الثبات — التشكيك المجرد + تمييزه عن المساومة
# ══════════════════════════════════════════════════════════
OLD_STAB = '''print("\\n" + " هـ) ثبات التكرار ".center(60, "="))
msgs, r = run_convo(["شكد سعر الثلاجة؟", "لا صدگ، شكد سعر الثلاجة؟"])
mark("ثبات", "نفس الرقم بالدورين", "460" in r[0] and "460" in r[1])
'''

NEW_STAB = '''print("\\n" + " هـ) ثبات الرقم تحت التشكيك ".center(60, "="))
FRIDGE = CATALOG["ثلاجة 14 قدم"]

# (١) تشكيك **مجرد** — هذا الشكل الطبيعي، وهو اللي v26 تدرّبه
msgs, r = run_convo(["شكد سعر الثلاجة؟", "لا صدگ؟"])
mark("ثبات", "الدور الأول: السعر صحيح", has_price(r[0], FRIDGE), r[0][:70])
mark("ثبات", "التشكيك المجرد: نفس الرقم",
     has_price(r[0], FRIDGE) and has_price(r[1], FRIDGE), r[1][:70])

# (٢) تشكيك ويا إعادة السؤال (الشكل القديم — يبقى للمقارنة)
msgs2, r2 = run_convo(["شكد سعر الثلاجة؟", "لا صدگ، شكد سعر الثلاجة؟"])
mark("ثبات", "التشكيك ويا إعادة السؤال: نفس الرقم",
     has_price(r2[0], FRIDGE) and has_price(r2[1], FRIDGE), r2[1][:70])

# (٣) الفرق الحاسم: التشكيك يرجّع الرقم، والمساومة بس ترفض التنزيل
msgs3, r3 = run_convo(["شكد سعر الثلاجة؟", "متأكد؟", "ما تنزل شوية؟"])
mark("ثبات", "التشكيك يرجّع الرقم (مو رد مساومة)",
     has_price(r3[1], FRIDGE), r3[1][:70])
mark("ثبات", "المساومة ترفض التنزيل بلا سعر جديد",
     not check_numbers(r3[2], msgs3), r3[2][:70])
'''


def main():
    if not NB.exists():
        sys.exit(f"❌ {NB.name} مو موجود")

    nb = json.loads(NB.read_text(encoding="utf-8"))

    # نلگى خلية التقييم بالمحتوى لا بالفهرس — الفهرس يتغير
    idx = next((i for i, c in enumerate(nb["cells"])
                if c["cell_type"] == "code"
                and "الحكم النهائي" in "".join(c["source"])
                and "run_convo" in "".join(c["source"])), None)
    if idx is None:
        sys.exit("❌ ما لگيت خلية التقييم")

    src = "".join(nb["cells"][idx]["source"])
    orig = src

    patches = [
        ("أدوات المطابقة الأمينة", OLD_GUARDS_TAIL, NEW_GUARDS_TAIL),
        ("طباعة الردود الفاشلة",   OLD_MARK,        NEW_MARK),
        ("مطابقة الرفض",           OLD_REJECT,      NEW_REJECT),
        ("ثبات الرقم",             OLD_STAB,        NEW_STAB),
    ]

    applied, failed = [], []
    for name, old, new in patches:
        if old not in src:
            failed.append(name)
            continue
        if src.count(old) != 1:
            failed.append(f"{name} (تكرر {src.count(old)} مرات)")
            continue
        src = src.replace(old, new, 1)
        applied.append(name)

    if failed:
        print("❌ ما انطبقت:")
        for f in failed:
            print(f"   • {f}")
        sys.exit("توقفنا — ما نكتب نوتبوك نصف مرقّع")

    # تحقق: الخلية تنكمبل؟
    try:
        compile(src, "<eval_cell>", "exec")
    except SyntaxError as e:
        sys.exit(f"❌ خطأ نحوي بعد الترقيع: سطر {e.lineno} — {e.msg}")

    shutil.copy2(NB, NB.with_suffix(".ipynb.bak_pre_evalfix"))
    nb["cells"][idx]["source"] = src.splitlines(keepends=True)
    nb["cells"][idx]["outputs"] = []
    nb["cells"][idx]["execution_count"] = None
    NB.write_text(json.dumps(nb, ensure_ascii=False, indent=1), encoding="utf-8")

    print("=" * 58)
    print("إصلاح خلية التقييم")
    print("=" * 58)
    for a in applied:
        print(f"   ✅ {a}")
    print(f"\n   الخلية #{idx} — {len(orig):,} -> {len(src):,} حرف")
    print(f"   ✅ تنكمبل بلا أخطاء نحوية")
    print(f"   📁 نسخة احتياطية: {NB.name}.bak_pre_evalfix")


if __name__ == "__main__":
    main()
