# -*- coding: utf-8 -*-
"""
v27 — النواقص اللي كشفتها ردود الموديل بالتقييم.

═══════════════════════════════════════════════════════════════
مصدر هذي الفجوات: ردود الموديل نفسها، لا افتراض
═══════════════════════════════════════════════════════════════

١) التشكيك **المدموج بإعادة السؤال** — صفر تغطية
   ────────────────────────────────────────────────────────
   رد الموديل:
       👤 لا صدگ، شكد سعر الثلاجة؟
       🤖 ما أگدر أغير السعر، بس الكتالوج صح

   v26 درّبت التشكيك **المجرد** ("لا صدگ؟") وهذا صح، بس القياس
   يستعمل الصيغة **المدموجة**: تشكيك + إعادة السؤال حرفياً بجملة
   وحدة. الفحص على الداتا: **صفر** مثال بهالشكل.

   والصيغة المدموجة أصعب: الجزء الأول ("لا صدگ") يشبه المساومة،
   والثاني ("شكد سعر...") سؤال سعر مباشر. الموديل يتشبث بالأول
   ويهمل الثاني. المطلوب: **الرقم أولاً**، والتطمين بعده.

٢) الوصف الجزئي اللي يطابق صنفين
   ────────────────────────────────────────────────────────
   رد الموديل:
       🤖 مكيف سبلت 1.5 طن نوع اول (انفرتر) بـ550,000
       👤 شكد سعر الطن ونص؟
       🤖 مكيف سبلت 1.5 طن نوع ثاني (عادي) بـ420,000   ← قفز للثاني

   "الطن ونص" يطابق صنفين بالكتالوج. الموديل اختار واحداً اعتباطاً
   وناقض نفسه بالدور السابق. الصح: **يعطي الاثنين** أو يستوضح.
   القياس: 62 مثالاً بوصف جزئي، ولا واحد منها عن **السعر**.

٣) الرفض ويا بديل **غير مطلوب** — 416 مثالاً تعلّم الغلط
   ────────────────────────────────────────────────────────
   رد الموديل:
       👤 عندكم تلفزيون سامسونج؟
       🤖 مو موجود حالياً، بس عندنا مكيف سبلت بـ420,000   ← مكيف؟!

   السستم يگول صراحة: «ولا تعرض بديل الا اذا طلب». بس الداتا فيها
   416 مثالاً بنمط «رفض + بس عدنا...»، **90 منها من فئة كتبتها v26
   نفسها** (reject_standard_with_list). يعني v26 زادت الطين بلة
   بهالنقطة.

   العلاج شقّان:
     أ) دفعة جديدة: رفض **نظيف** بلا أي بديل، والبديل بس لمن يُطلب
     ب) سكربت منفصل ينظف الـ416 القديمة (v27_clean، مو هنا)

   وفرق مهم: البديل من **نفس الفئة** لمن يُطلب = مقبول.
   البديل من فئة **مختلفة** بلا طلب = خطأ دايماً (تلفزيون -> مكيف).

٤) الرفض المتسلسل يفقد اسم البراند
   ────────────────────────────────────────────────────────
   رد الموديل:
       👤 طيب شوفلي سبلت LG او كارير؟
       🤖 ما أگدر أگلك سعر لشي مو موجود عدنا عيني   ← أي شي؟

   رفض سليم منطقياً بس مجهول المرجع. بعد رفضين متتاليين الموديل
   يفقد التسمية. الصح: **يسمّي البراند المرفوض** حتى يبين إنه فاهم
   السؤال الجديد لا مكرر رفضه القديم.
"""
import json
import random
import re
import sys
from collections import Counter
from pathlib import Path

sys.stdout.reconfigure(encoding="utf-8")
random.seed(20260729)

DATA = Path(__file__).resolve().parent.parent / "data" / "v16"

# ── كتالوج فيه أزواج **متعمدة** يطابقها وصف جزئي واحد ──
PAIRS = [
    ("مكيف سبلت 1.5 طن نوع اول (انفرتر)", 550000,
     "مكيف سبلت 1.5 طن نوع ثاني (عادي)", 420000, "الطن ونص"),
    ("ثلاجة 16 قدم نوع اول (نوفروست)", 730000,
     "ثلاجة 16 قدم نوع ثاني (عادي)", 610000, "الـ16 قدم"),
    ("غسالة 9 كغم اوتوماتيك (انفرتر)", 620000,
     "غسالة 9 كغم اوتوماتيك (عادي)", 495000, "التسع كغم"),
    ("تلفزيون 55 بوصة سمارت 4K", 700000,
     "تلفزيون 55 بوصة عادي", 480000, "الـ55 بوصة"),
]
SINGLES = [
    ("طباخ بيكو 5 عيون", 295000), ("سخان كهربائي 80 لتر", 165000),
    ("فريزر زانوسي 400 لتر", 585000), ("مايكروويف 25 لتر", 135000),
]
# براندات مو موجودة — للرفض
BRANDS = ["سامسونج", "LG", "كارير", "توشيبا", "بوش", "ميتسوبيشي",
          "دايكن", "شارب", "هايسنس", "بيكو الأصلي"]
KINDS = ["تلفزيون", "سبلت", "غسالة", "ثلاجة", "مكيف"]


def money(n):
    return f"{n:,}"


def build_system(items):
    lines = "\n".join(f"- {p}: {money(v)} دينار" for p, v in items)
    return (f"""انت بائع بمحل الكترونيات بالسماوة. ردودك قصيرة وباللهجة العراقية.
جاوب من الكتالوج حصراً:
{lines}

قواعد صارمة:
- المنتج او البراند المو موجود بالكتالوج: گول مو متوفر حالياً حتى لو الزبون أصر، ولا تعرض بديل الا اذا طلب.
- الضمان والمواصفات غير المذكورة: گول اتأكدلك وأرد عليك.""")


def rec(cat, msgs):
    return {"category": cat, "messages": msgs}


def mixed_catalog():
    """كتالوج فيه زوج غامض + أصناف مفردة."""
    a, va, b, vb, label = random.choice(PAIRS)
    singles = random.sample(SINGLES, 2)
    items = [(a, va), (b, vb)] + singles
    random.shuffle(items)
    return items, (a, va, b, vb, label)


# ════════════════════════════════════════════════════════════
# ١) التشكيك المدموج بإعادة السؤال
# ════════════════════════════════════════════════════════════
ASK = ["شكد سعر {p}؟", "بيش {p}؟", "شگد يطلع {p}؟", "گلي سعر {p}"]
FIRST = ["تفضل، {p} سعره {v} دينار", "{p} بـ{v} دينار عيني",
         "{p} يطلع عليك {v} دينار"]

# الصيغة المدموجة: تشكيك + إعادة السؤال بجملة وحدة
MERGED_Q = [
    "لا صدگ، {q}",
    "لا صدگ هالسعر، {q}",
    "متأكد؟ {q}",
    "أكيد؟ {q}",
    "مو معقول، {q}",
    "لا تضحك عليّ، {q}",
    "صدگ هيچي؟ {q}",
    "هاي غالي، {q}",
]
# الرد: **الرقم أول شي**، بلا دفاع
MERGED_A = [
    "إي صدگ، {p} بـ{v} دينار — نفس الرقم",
    "{v} دينار عيني، هذا سعر {p} المكتوب عندي",
    "نفس السعر، {p} بـ{v} دينار",
    "{v} دينار، ما تغير — {p}",
    "إي والله، {p} بـ{v} دينار بالضبط",
]


def gen_merged_doubt(n):
    out = []
    for _ in range(n):
        items, _ = mixed_catalog()
        sysm = build_system(items)
        p, v = random.choice(items)
        q = random.choice(ASK).format(p=p)
        out.append(rec("price_doubt_merged", [
            {"role": "system", "content": sysm},
            {"role": "user", "content": q},
            {"role": "assistant",
             "content": random.choice(FIRST).format(p=p, v=money(v))},
            {"role": "user", "content": random.choice(MERGED_Q).format(q=q)},
            {"role": "assistant",
             "content": random.choice(MERGED_A).format(p=p, v=money(v))},
        ]))
    return out


def gen_merged_doubt_short(n):
    """نفس الشي بس الإعادة مختصرة: «لا صدگ، شكد؟» بلا اسم المنتج."""
    out = []
    SHORT = ["لا صدگ، شكد؟", "متأكد؟ بيش گتلي؟", "لا صدگ، عيد السعر",
             "أكيد؟ شگد يعني؟", "مو معقول، شكد گتلي؟"]
    for _ in range(n):
        items, _ = mixed_catalog()
        sysm = build_system(items)
        p, v = random.choice(items)
        out.append(rec("price_doubt_merged_short", [
            {"role": "system", "content": sysm},
            {"role": "user", "content": random.choice(ASK).format(p=p)},
            {"role": "assistant",
             "content": random.choice(FIRST).format(p=p, v=money(v))},
            {"role": "user", "content": random.choice(SHORT)},
            {"role": "assistant",
             "content": random.choice(MERGED_A).format(p=p, v=money(v))},
        ]))
    return out


# ════════════════════════════════════════════════════════════
# ٢) الوصف الجزئي اللي يطابق صنفين
# ════════════════════════════════════════════════════════════
AMBIG_Q = ["شكد سعر {l}؟", "بيش {l}؟", "{l} شگد؟", "گلي سعر {l}"]
# الصح: يعطي **الاثنين** بلا ما ينحاز
BOTH_A = [
    "عدنا منه اثنين: {a} بـ{va} دينار، و{b} بـ{vb} دينار",
    "اكو نوعين — {a} بـ{va} دينار، و{b} بـ{vb} دينار",
    "{a} بـ{va} دينار، والثاني {b} بـ{vb} دينار",
]
# أو يستوضح
CLARIFY_A = [
    "عدنا نوعين من {l}، تريد الأول لو الثاني؟",
    "اكو اثنين منه — أي واحد تقصد؟",
]


def gen_ambiguous_price(n):
    """وصف جزئي يطابق صنفين -> يعطي الاثنين."""
    out = []
    for _ in range(n):
        items, (a, va, b, vb, label) = mixed_catalog()
        sysm = build_system(items)
        out.append(rec("ambiguous_partial_both", [
            {"role": "system", "content": sysm},
            {"role": "user", "content": random.choice(AMBIG_Q).format(l=label)},
            {"role": "assistant",
             "content": random.choice(BOTH_A).format(
                 a=a, va=money(va), b=b, vb=money(vb))},
        ]))
    return out


def gen_ambiguous_after_first(n):
    """الحالة اللي فشل بيها الموديل بالضبط:
    عرض الأول، ثم انسأل بوصف جزئي -> **لا ينط للثاني** بلا تنبيه."""
    out = []
    for _ in range(n):
        items, (a, va, b, vb, label) = mixed_catalog()
        sysm = build_system(items)
        out.append(rec("ambiguous_after_first", [
            {"role": "system", "content": sysm},
            {"role": "user", "content": f"عندكم {label}؟"},
            {"role": "assistant",
             "content": f"إي عيني، {a} بـ{money(va)} دينار"},
            {"role": "user", "content": random.choice(AMBIG_Q).format(l=label)},
            {"role": "assistant",
             "content": random.choice([
                 f"هو نفسه اللي گتلك عليه — {a} بـ{money(va)} دينار. "
                 f"وإذا تريد الثاني، {b} بـ{money(vb)} دينار",
                 f"{a} بـ{money(va)} دينار مثل ما گتلك، "
                 f"واكو هم {b} بـ{money(vb)} دينار",
             ])},
        ]))
    return out


# ════════════════════════════════════════════════════════════
# ٣) الرفض النظيف — بلا بديل غير مطلوب
# ════════════════════════════════════════════════════════════
REJ_Q = ["عندكم {k} {b}؟", "اكو {b} عدكم؟", "تبيعون {k} {b}؟",
         "شكد سعر {b} عدكم؟"]
# رفض نظيف: بلا أي «بس عدنا...»
REJ_CLEAN = [
    "لا عيني، {b} مو موجود عدنا",
    "{b} ما عدنا منه حالياً",
    "والله {b} مو متوفر عدنا هسه",
    "{b} مو بالكتالوج عدي عيني",
]


def gen_reject_clean(n):
    """رفض بلا بديل — السستم يمنع عرض البديل بلا طلب."""
    out = []
    for _ in range(n):
        items, _ = mixed_catalog()
        sysm = build_system(items)
        b = random.choice(BRANDS)
        k = random.choice(KINDS)
        out.append(rec("reject_clean_no_alt", [
            {"role": "system", "content": sysm},
            {"role": "user", "content": random.choice(REJ_Q).format(k=k, b=b)},
            {"role": "assistant", "content": random.choice(REJ_CLEAN).format(b=b)},
        ]))
    return out


ALT_ASK = ["طيب شنو عندكم؟", "زين شمعندكم؟", "خير، شنو المتوفر؟",
           "طيب عرضلي الموجود", "شنو تنصحني بيه؟"]


def gen_reject_then_alt(n):
    """البديل **بعد ما يُطلب** — هذا الشكل المقبول."""
    out = []
    for _ in range(n):
        items, _ = mixed_catalog()
        sysm = build_system(items)
        b = random.choice(BRANDS)
        k = random.choice(KINDS)
        lst = "\n".join(f"- {p}: {money(v)} دينار" for p, v in items[:3])
        out.append(rec("reject_then_alt_on_request", [
            {"role": "system", "content": sysm},
            {"role": "user", "content": random.choice(REJ_Q).format(k=k, b=b)},
            {"role": "assistant", "content": random.choice(REJ_CLEAN).format(b=b)},
            {"role": "user", "content": random.choice(ALT_ASK)},
            {"role": "assistant",
             "content": random.choice(["الموجود عدنا:", "هذا المتوفر:",
                                       "عدنا هالأصناف:"]) + "\n" + lst},
        ]))
    return out


# ════════════════════════════════════════════════════════════
# ٤) الرفض المتسلسل — كل رفض يسمّي براندَه
# ════════════════════════════════════════════════════════════
SEQ_A2 = [
    "{b2} هم مو موجود عدنا عيني",
    "ولا {b2} عدنا، نفس الشي",
    "{b2} هم ما عدنا منه",
]
SEQ_A3 = [
    "ولا {b3} عيني، هذوله كلهم مو عدنا",
    "{b3} هم مو متوفر — ما نشتغل بهالماركات",
]
PRESSURE = ["اكيد عندكم، كل المحلات عدها",
            "لا تگلي ماكو، دور زين",
            "شلون ماكو؟ محل مثل مالتكم!"]
PRESSURE_A = [
    "والله ما أگدر أوعدك بشي مو موجود عدنا، {b} مو بالكتالوج",
    "صدگني عيني، {b} ما عدنا — ما أحب أوهمك",
]


def gen_sequential_named(n):
    """رفضان متتاليان، كل واحد **يسمّي براندَه** لا يعمّم."""
    out = []
    for _ in range(n):
        items, _ = mixed_catalog()
        sysm = build_system(items)
        b1, b2 = random.sample(BRANDS, 2)
        k = random.choice(KINDS)
        msgs = [
            {"role": "system", "content": sysm},
            {"role": "user", "content": random.choice(REJ_Q).format(k=k, b=b1)},
            {"role": "assistant", "content": random.choice(REJ_CLEAN).format(b=b1)},
        ]
        if random.random() < 0.5:
            msgs += [
                {"role": "user", "content": random.choice(PRESSURE)},
                {"role": "assistant",
                 "content": random.choice(PRESSURE_A).format(b=b1)},
            ]
        msgs += [
            {"role": "user", "content": f"طيب شوفلي {k} {b2}؟"},
            {"role": "assistant", "content": random.choice(SEQ_A2).format(b2=b2)},
        ]
        out.append(rec("reject_sequential_named", msgs))
    return out


def gen_sequential_two_brands(n):
    """براندان بسؤال واحد -> يسمّيهما الاثنين."""
    out = []
    A = ["ولا {b1} ولا {b2} عدنا عيني",
         "{b1} و{b2} الاثنين مو موجودين عدنا",
         "لا {b1} ولا {b2}، ما نشتغل بيهم"]
    for _ in range(n):
        items, _ = mixed_catalog()
        sysm = build_system(items)
        b0, b1, b2 = random.sample(BRANDS, 3)
        k = random.choice(KINDS)
        out.append(rec("reject_two_brands_named", [
            {"role": "system", "content": sysm},
            {"role": "user", "content": random.choice(REJ_Q).format(k=k, b=b0)},
            {"role": "assistant", "content": random.choice(REJ_CLEAN).format(b=b0)},
            {"role": "user", "content": f"طيب شوفلي {k} {b1} او {b2}؟"},
            {"role": "assistant", "content": random.choice(A).format(b1=b1, b2=b2)},
        ]))
    return out


# ════════════════════════════════════════════════════════════
PLAN = [
    (gen_merged_doubt,        600),   # الفشل الأول — أكبر وزن
    (gen_merged_doubt_short,  260),
    (gen_ambiguous_price,     260),
    (gen_ambiguous_after_first, 300),
    (gen_reject_clean,        420),
    (gen_reject_then_alt,     260),
    (gen_sequential_named,    360),
    (gen_sequential_two_brands, 200),
]

NUM = re.compile(r"[\d،,]{3,}")
# نمط البديل غير المطلوب — اللي وقع بيه الموديل، وبيه 416 مثالاً قديماً
UNSOLICITED = re.compile(
    r"(?:مو موجود|ما عدنا|ماكو|مو متوفر|مو بالكتالوج)[^.،]{0,40}"
    r"(?:بس|لكن)\s*(?:عدنا|عندنا|اكو|أكو)")
DEFENSIVE = re.compile(r"ما أگدر أغير السعر|ما اگدر اغير|السعر ثابت")


def validate(rows):
    errs = Counter()
    for r in rows:
        cat, msgs = r["category"], r["messages"]
        sysm = " ".join(m["content"] for m in msgs if m["role"] == "system")
        asst = [m["content"] for m in msgs if m["role"] == "assistant"]

        # كل رقم لازم يكون بالنظام
        for a in asst:
            for tok in NUM.findall(a):
                if tok not in sysm:
                    errs["رقم مو بالكتالوج"] += 1

        # (أ) التشكيك المدموج: الرقم يتكرر، وبلا جملة دفاعية
        if cat.startswith("price_doubt_merged"):
            n0, n1 = set(NUM.findall(asst[0])), set(NUM.findall(asst[1]))
            if not (n0 and n0 == n1):
                errs["السعر ما ثبت بالتشكيك المدموج"] += 1
            if any(DEFENSIVE.search(a) for a in asst):
                errs["جملة دفاعية بدل الرقم"] += 1

        # (ب) الوصف الغامض: لازم **الرقمين** بالرد
        if cat.startswith("ambiguous"):
            if len(set(NUM.findall(asst[-1]))) < 2:
                errs["الوصف الغامض ما أعطى الصنفين"] += 1

        # (ج) الرفض: ولا بديل غير مطلوب أبداً
        if cat.startswith("reject"):
            for a in asst:
                if UNSOLICITED.search(a):
                    errs["بديل غير مطلوب برد رفض"] += 1
            # الرفض النظيف: بلا أي رقم
            if cat in ("reject_clean_no_alt", "reject_sequential_named",
                       "reject_two_brands_named"):
                if any(NUM.search(a) for a in asst):
                    errs["رقم برد رفض نظيف"] += 1

        # (د) الرفض المتسلسل: الرد الأخير يسمّي البراند
        if cat == "reject_sequential_named":
            last_user = [m["content"] for m in msgs if m["role"] == "user"][-1]
            brand = next((b for b in BRANDS if b in last_user), None)
            if brand and brand not in asst[-1]:
                errs["الرفض المتسلسل ما سمّى البراند"] += 1
    return errs


def main():
    rows, seen, counts = [], set(), {}
    for fn, n in PLAN:
        kept = []
        for r in fn(n * 6):
            if len(kept) >= n:
                break
            k = json.dumps(r["messages"], ensure_ascii=False, sort_keys=True)
            if k in seen:
                continue
            seen.add(k)
            kept.append(r)
        counts[kept[0]["category"]] = len(kept)
        rows.extend(kept)

    errs = validate(rows)
    random.shuffle(rows)
    p = DATA / "iraqi_v27_eval_gaps.jsonl"
    with p.open("w", encoding="utf-8") as fh:
        for r in rows:
            fh.write(json.dumps(r, ensure_ascii=False) + "\n")

    print("=" * 62)
    print("v27 — نواقص كشفها التقييم")
    print("=" * 62)
    for k, v in counts.items():
        print(f"  {k:<32}{v:>6}")
    print(f"  {'المجموع':<32}{len(rows):>6}")
    print()
    if errs:
        print("  ❌ أخطاء تحقق:")
        for k, v in errs.most_common():
            print(f"     {k:<44}{v:>5}")
    else:
        print(f"  ✅ التحقق نظيف على {len(rows)} مثالاً")
    print(f"  📁 {p.name}")


if __name__ == "__main__":
    main()
