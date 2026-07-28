# -*- coding: utf-8 -*-
"""
v19 — تحييد تقمّص دور الطبيب بفئة `healthcare`.

═══════════════════════════════════════════════════════════════
المشكلة
═══════════════════════════════════════════════════════════════
إضافة `off_topic_medical_strict` ما تكفي لحالها: فئة `healthcare`
الموجودة (378 دور) تعلّم **العكس** صراحةً — البائع يتقمّص طبيباً:

    U: «وجع معدة»
    A: «يشبه صداع مزمن. خذ فيتامينات وارتاح يوم كامل»   ← تشخيص + وصفة

    U: «ابنتي عندها كحة وضيق بالصدر»
    A: «ما تشوف شر. كم عمرها؟»                          ← تاريخ مرضي

    U: «زكام وحرارة، خطيرة؟»
    A: «ما هي خطيرة لو اتعالجت»                          ← طمأنة عن الخطورة

هذا نفس درس v16: **إضافة السلوك الصح فوق السلوك الغلط تخلي الموديل
يشوف الاثنين بنفس الوزن.** والفرق هنا إن الغلط مو خطأ قياس — هو خطر
فعلي على صحة الزبون.

═══════════════════════════════════════════════════════════════
التمييز المهم
═══════════════════════════════════════════════════════════════
مو كل `healthcare` غلط. الفئة فيها نوعان:

  أ. **محادثات عيادة مشروعة** — حجز موعد، دوام الدكتور، سعر الكشفية،
     عنوان العيادة. هذي محادثات خدمية عادية ولا تحتاج تعديل.

  ب. **تقمّص طبي** — تشخيص، وصف دواء، طمأنة عن الخطورة، أخذ تاريخ
     مرضي. هذي تنحيّد.

الكشف يعتمد على **رد المساعد** لا سؤال الزبون: الرد اللي ينطي تشخيصاً
أو دواءً أو حكماً على الخطورة يتبدّل بإحالة. والرد اللي ينطي موعداً أو
عنواناً يبقى.
"""
import json
import random
import re
import sys
from collections import Counter
from pathlib import Path

sys.stdout.reconfigure(encoding="utf-8")
random.seed(20260731)

SRC = Path(__file__).resolve().parent.parent / "data" / "v16"

# ── علامات التقمّص الطبي بردّ المساعد ──
DIAGNOSE = re.compile(
    r"يشبه|أعراض|اعراض|حالتك|تشخيص|مو خطير|ما هي خطير|خطيرة لو|"
    r"طبيعي هذا|بسيطة وتروح|تحتاج متابعة|يمكن يكون|غالباً")
PRESCRIBE = re.compile(
    r"خذ\s|خذي\s|تاخذ\s|انطيه|أنطيه|انطيها|استعمل|استخدم|"
    r"حبوب|مسكن|فيتامين|شراب|مرهم|دواء|جرعة|علاج|كمّد|كمادات")
HISTORY = re.compile(
    r"كم عمر|شكد عمر|من شوكت|من متى|شنو الأعراض|درجة الحرارة|"
    r"وينك تراجعت|شكد صارلك")
# محادثة عيادة مشروعة — ما تنلمس
LEGIT = re.compile(
    r"موعد|حجز|الدوام|دوام|الكشفية|كشفية|العنوان|عنوان العيادة|"
    r"رقم العيادة|أوقات|السعر|تلفون العيادة")

REFER = [
    "ما أگدر أنصحك بأمور صحية عيني، لازم تراجع دكتور أو صيدلية",
    "هاي أمور طبية ما أفهم بيها عيني — راجع دكتور، هو اللي يگلك الصح",
    "والله ما أجازف بصحتك بكلام ما أفهم بيه، الأفضل تشوف طبيب",
    "سلامتك عيني، بس أي دواء بلا فحص ممكن يضرك — راجع مختص",
    "الله يعافيك، بس هذا سؤال لأهل الطب مو إلي — روح للصيدلية أو العيادة",
    "الله يشفيه، بس ما أنصح بدواء أبداً — أقرب صيدلية أو دكتور يفيدك أكثر",
]


def is_roleplay(text):
    """رد المساعد يتقمّص طبيباً؟"""
    if LEGIT.search(text):
        return False
    return bool(DIAGNOSE.search(text) or PRESCRIBE.search(text)
                or HISTORY.search(text))


# ── تنظيف نهائي للمحادثات المحوّلة ──
# `is_roleplay` تفحص الرد الواحد، فتترك محادثة محوّلة فيها أدوار ثانية
# ما انمسكت: موعد عيادة بسعر («كشف الأطفال 23,000»)، أو دعوة للمراجعة
# بلا ذكر طبيب، أو لهجة مصرية موروثة. بما إن الفئة صارت «قاعدة صارمة»،
# كل أدوارها لازم تلتزم — لا سعر ولا تشخيص، وإحالة صريحة بالآخر.
NUM = re.compile(r"\d[\d,]{2,}")
DOC = re.compile(r"دكتور|طبيب|صيدلي|صيدلية|عيادة|مستشفى|مختص")
NON_IRAQI = re.compile(r"مفيتش|مفيش|عايز|إزاي|ازاي|دلوقتي|كده")


def enforce_strict(msgs):
    """يفرض قاعدة الطبقة الطبية على كل أدوار المحادثة."""
    out = [dict(m) for m in msgs]
    ai = [i for i, m in enumerate(out) if m["role"] == "assistant"]
    if not ai:
        return out, False
    changed = False
    for i in ai:
        t = out[i]["content"]
        if NUM.search(t) or DIAGNOSE.search(t) or PRESCRIBE.search(t) \
                or HISTORY.search(t) or NON_IRAQI.search(t):
            out[i]["content"] = random.choice(REFER)
            changed = True
    # الرد الأخير لازم يحيل صراحةً
    last = ai[-1]
    if not DOC.search(out[last]["content"]):
        out[last]["content"] = random.choice(REFER)
        changed = True
    return out, changed


def main():
    stats = Counter()
    for f in sorted(SRC.glob("*.jsonl")):
        rows = []
        for line in f.open(encoding="utf-8"):
            d = json.loads(line)
            if d.get("category") != "healthcare":
                rows.append(d)
                continue

            msgs = [dict(m) for m in d["messages"]]
            touched = any(m["role"] == "assistant" and is_roleplay(m["content"])
                          for m in msgs)
            if touched:
                # الفئة تتغيّر لقاعدة صارمة، فكل أدوارها تلتزم — مو الدور
                # اللي انمسك بس.
                msgs, _ = enforce_strict(msgs)
                stats["roleplay_neutralized"] += 1
                d["category"] = "off_topic_medical_strict"
            else:
                stats["legit_kept"] += 1
            d["messages"] = msgs
            rows.append(d)

        with f.open("w", encoding="utf-8") as fh:
            for r in rows:
                fh.write(json.dumps(r, ensure_ascii=False) + "\n")

    print("=" * 60)
    print("v19 — تحييد التقمّص الطبي")
    print("=" * 60)
    for k, v in stats.most_common():
        print(f"  {k:<28}{v:>8,}")


if __name__ == "__main__":
    main()
