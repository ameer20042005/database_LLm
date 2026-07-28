# -*- coding: utf-8 -*-
"""
v16 — تقييم للفئات الجديدة/الموسّعة.

`gap7_missing_field_ask` طلعت فئة تدريب **بلا تقييم** ببناء الثلث —
يعني ندرّب سلوكاً وما نگدر نقيسه. هذا يكسر قاعدة «كل فئة تدريب مقيسة»
اللي التزم بيها المشروع من v13.

هنا نبني تقييماً بنفس محاور المولّد بس **ببذرة مختلفة وقيم مختلفة**
(أسماء/أرقام/محافظات/منتجات ما تظهر بالتدريب)، حتى ما يكون التقييم
حفظاً. التلوث يُفحص بالبناء أصلاً، وهنا نضمنه بالتصميم.
"""
import json
import random
import sys
from pathlib import Path

sys.stdout.reconfigure(encoding="utf-8")
random.seed(99001)                    # بذرة مختلفة عن التدريب (20260728)

DATA = Path(__file__).resolve().parent.parent / "data"

# ── قيم حصرية للتقييم: ما تتقاطع مع قوائم المولّد ──
VAL_PRODUCTS = [
    ("ثلاجة بيكو 16 قدم", 730000),
    ("غسالة هاير 9 كغم اوتوماتيك", 495000),
    ("مكيف كاريير 1.5 طن سبلت", 615000),
    ("تلفزيون توشيبا 50 بوصة سمارت", 720000),
    ("فريزر ميديا 250 لتر", 405000),
    ("طباخ الحافظ 4 عيون", 265000),
]
VAL_NAMES = ["باقر الموسوي", "شهد الطائي", "منتظر عواد", "تبارك سلمان",
             "أمير الزيدي", "دعاء ناصر"]
VAL_PROVS = ["واسط", "المثنى", "صلاح الدين", "دهوك", "السليمانية", "القادسية"]
VAL_ADDRS = ["حي الزهراء زقاق 5", "شارع الجمهورية محلة 302",
             "حي النصر قرب المستشفى", "المركز شارع السوق الكبير"]


def phone():
    return "078" + "".join(random.choice("0123456789") for _ in range(8))


def money(n):
    return f"{n:,}"


SYS_ORDER = """أنت موظف مبيعات بمحل عراقي.

الموجود حالياً:
- {p1}: {v1} دينار
- {p2}: {v2} دينار

انسخ الأسعار والأسماء حرفياً من القائمة. إذا وافق الزبون على الشراء، اجمع منه هذي الحقول وحدة وحدة: الاسم، رقم الهاتف، المحافظة، العنوان بالتفصيل. اسأل عن الناقص بس — لا تعيد سؤال حقل انطاك اياه، ولا تخترع رقم ولا عنوان ولا اسم ما گاله الزبون.
لمن تكتمل الحقول الأربعة، لخّص الطلب واسأله يأكد. وبعد ما يأكد صراحةً، اختم ردك بسطر مستقل فيه [ORDER_READY]"""

FIELD_ASK = {
    "phone": ["بس انطيني رقم هاتفك حتى نكدر نوصلك",
              "ناقص رقم هاتفك بس عيني، دزه لو سمحت",
              "خوش، بقى رقم الهاتف حتى يتصل بيك المندوب"],
    "name": ["بس انطيني اسمك حتى أسجل الطلب",
             "ناقص اسمك بس عيني"],
    "province": ["بس گلي من أي محافظة حتى أسجل التوصيل",
                 "ناقص المحافظة بس، من وين انت عيني؟"],
    "address": ["بس انطيني العنوان بالتفصيل حتى ما يضيع المندوب",
                "ناقص العنوان المفصل بس عيني"],
}


def gen_missing_field(n):
    out = []
    for _ in range(n):
        (p1, v1), (p2, v2) = random.sample(VAL_PRODUCTS, 2)
        sysm = SYS_ORDER.format(p1=p1, v1=money(v1), p2=p2, v2=money(v2))
        field = random.choice(list(FIELD_ASK))
        cn, ph = random.choice(VAL_NAMES), phone()
        pv, ad = random.choice(VAL_PROVS), random.choice(VAL_ADDRS)
        parts = []
        if field != "name":
            parts.append(f"اسمي {cn}")
        if field != "phone":
            parts.append(f"رقمي {ph}")
        if field != "province":
            parts.append(f"اني من {pv}")
        if field != "address":
            parts.append(ad)
        out.append({"category": "gap7_missing_field_ask", "messages": [
            {"role": "system", "content": sysm},
            {"role": "user", "content": f"شكد سعر {p1}؟"},
            {"role": "assistant", "content": f"{p1} سعره {money(v1)} دينار عيني"},
            {"role": "user",
             "content": f"زين اريدها، ثبتلي الطلب. {'، '.join(parts)}"},
            {"role": "assistant", "content": random.choice(FIELD_ASK[field])},
        ]})
    return out


def main():
    rows, seen = [], set()
    for r in gen_missing_field(400):
        k = json.dumps(r["messages"], ensure_ascii=False, sort_keys=True)
        if k in seen:
            continue
        seen.add(k)
        rows.append(r)
    rows = rows[:220]

    p = DATA / "iraqi_v16_val_extra.jsonl"
    with p.open("w", encoding="utf-8") as fh:
        for r in rows:
            fh.write(json.dumps(r, ensure_ascii=False) + "\n")
    print(f"✅ {len(rows)} مثال تقييم -> {p.name}")


if __name__ == "__main__":
    main()
