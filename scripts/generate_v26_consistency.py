# -*- coding: utf-8 -*-
"""
v26 — ثبات الرقم تحت التشكيك، وقائمة الفئة، والحالة بعد الإلغاء.

═══════════════════════════════════════════════════════════════
الفجوات المقيسة على نسخة v16 (31,981 مثال)
═══════════════════════════════════════════════════════════════

١) التشكيك بالسعر — الفجوة الحقيقية
   `repeat_question_consistency` موجودة بـ1,635 مثالاً بالمصدر
   (367 بالنسخة النهائية)، بس **صفر** منها فيه تشكيك طبيعي:

       أمثلة موجودة:   «ها، عندكم بطاطا؟»  «شلون يعني؟ بيش الخلاط؟»
       أمثلة مفقودة:   «لا صدگ؟»  «متأكد؟»  «هاي غالي، مو معقول»

   الموجود كله **إعادة حرفية للسؤال ببادئة ميكانيكية**. الموديل تعلّم
   يثبّت الرقم لمن يتكرر السؤال نصاً، وما تعلّم يثبّته لمن الزبون
   **يشكّك**. والتشكيك هو الحالة الواقعية — فيهرب لجملة دفاعية
   («ما أگدر أغير السعر») لأنها أقرب شي بالداتا لسياق «زبون مو راضي»
   (`qa_bargaining` 173 مثالاً، `persistence_refusal` 575).

   العلاج: التشكيك ≠ مساومة. الرد الصح **يعيد نفس الرقم أول شي**،
   وبعدين يطمّن. لا اعتذار، لا دفاع، لا كلام عن الصلاحية بالتسعير.

٢) طلب قائمة الفئة
   1,295 محادثة بالنسخة النهائية فيها «شنو عندكم / اكو غيره / شنو
   المتوفر»، بس كلها منصهرة بـ`grounded_catalog_copy` و`_reject`
   والرد **يسمّي صنفاً واحداً بديلاً**. ماكو تعليم لتعداد الفئة.

   العلاج: الرد يعدّد المتوفر من الفئة **من القائمة حصراً**، وإذا
   الفئة بيها صنف واحد يگولها صراحة بدل ما يخترع ثاني.

٣) التماسك بعد الإلغاء
   551 محادثة فيها إلغاء، أكثرها `deep_refusal_in_sales` (120) —
   يعني الإلغاء مغطى كـ**رفض**، مو كـ**إعادة ضبط حالة**. ماكو فئة
   تعلّم: بعد ما ينلغي طلب بكمية، سؤال سعر وحدة واحدة يرجع سعر
   الوحدة، لا اجمالي الطلب الملغى.

   العلاج: إلغاء صريح -> إقرار -> سؤال جديد -> رقم جديد محسوب من
   الصفر. وحالة الحدّ: الزبون يرجع يطلب نفس الشي بكمية مختلفة.

٤) توحيد صيغ الرفض
   لاحظنا تنوعاً حراً بصيغ رفض المنتج غير الموجود («مو موجود عدنا
   حالياً»، «هذا انتهى»، «ما نشتغل بيه»...). التنويع صحيح لغوياً بس
   يصعّب القياس الثابت. هنا **ما ننزع التنويع** — نضيف كتلة ترسّخ
   ثلاث صيغ قياسية بوزن أعلى، فتصير هي المنوال والباقي ذيل.

ملاحظة على ما لم يُعالَج
───────────────────────────────────────────────────────────────
«تعليق صيغة الإحالة عبر الأدوار» مذكورة بالتقييمات السابقة. الفحص
على النسخة الحالية: 114 محادثة بأكثر من دور إحالة، **صفر** منها
تكرر الجملة حرفياً. المشكلة انحلّت بـv22، فما ننتج لها داتا.
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

# ── فئات المنتجات: الفئة نفسها تنفع لتعداد القائمة ──
CATALOG = {
    "الثلاجات": [
        ("ثلاجة بيكو 16 قدم", 730000), ("ثلاجة سامسونك 18 قدم", 890000),
        ("ثلاجة كونكورد 14 قدم", 610000),
    ],
    "الغسالات": [
        ("غسالة هاير 9 كغم اوتوماتيك", 495000),
        ("غسالة توشيبا 8 كغم", 520000),
        ("غسالة LG 10 كغم انفرتر", 720000),
    ],
    "المكيفات": [
        ("مكيف سبلت 1.5 طن انفرتر", 550000),
        ("مكيف ألتون 2 طن سبلت", 815000),
        ("مكيف جنرال 2 طن", 780000),
    ],
    "التلفزيونات": [
        ("تلفزيون هايسنس 43 بوصة", 680000),
        ("تلفزيون شارب 55 بوصة", 700000),
    ],
    "الطباخات": [
        ("طباخ بيكو 5 عيون", 295000),
    ],
    "السخانات": [
        ("سخان كهربائي 80 لتر", 165000),
    ],
    "الفريزرات": [
        ("فريزر زانوسي 400 لتر", 585000),
    ],
}
MISSING = ["مايكرويف", "غسالة صحون", "مجفف ملابس", "سخان غاز",
           "شاشة عرض", "مروحة سقفية", "براد ماء", "فرن كهربائي"]


def money(n):
    return f"{n:,}"


def build_system(items, note=""):
    lines = "\n".join(f"- {p}: {money(v)} دينار" for p, v in items)
    extra = f"\n{note}" if note else ""
    return (f"""أنت موظف مبيعات بمحل عراقي.

الموجود حالياً:
{lines}{extra}

انسخ الأسعار والأسماء حرفياً من القائمة. إذا انسألت عن معلومة مو مكتوبة بالقائمة گول أتأكدلك وأرد عليك — لا تخترع رقم ولا تعد بشي مو مكتوب.""")


def rec(cat, msgs):
    return {"category": cat, "messages": msgs}


def pick_items(k=4):
    """يسحب أصنافاً من فئات مختلفة."""
    pool = [(p, v, c) for c, lst in CATALOG.items() for p, v in lst]
    return random.sample(pool, min(k, len(pool)))


# ════════════════════════════════════════════════════════════
# ١) ثبات الرقم تحت التشكيك — الكتلة الأهم
# ════════════════════════════════════════════════════════════
ASK = ["شكد سعر {p}؟", "بيش {p}؟", "{p} بيش عدكم؟",
       "شگد يطلع {p}؟", "گلي سعر {p}"]

FIRST = ["{p} بـ{v} دينار عيني", "{p} يطلع عليك {v} دينار",
         "{p} سعره {v} دينار", "تدلل، {p} بـ{v} دينار"]

# التشكيك بأنواعه — كلها ترجع نفس الرقم
DOUBT_PLAIN = ["لا صدگ؟", "متأكد؟", "أكيد؟", "صدگ هيچي؟",
               "لا صدگ هالسعر؟", "متأكد من الرقم؟"]
DOUBT_PRICE = ["هاي غالي، مو معقول", "غالي شوية، متأكد؟",
               "هاي زايد على السوق، أكيد؟", "مو غالي هيچي؟"]
DOUBT_REPEAT = ["گلي مرة لخ شكد؟", "عيد عليّ السعر", "شگد گتلي؟",
                "ما سمعت زين، بيش؟"]
DOUBT_CHEAP = ["هاي رخيص هواي، متأكد؟", "بس هذا رخيص، صدگ؟"]

# ── الرد: الرقم أول شي، بلا دفاع ولا اعتذار ──
ANS_PLAIN = [
    "إي صدگ عيني، {p} بـ{v} دينار",
    "أكيد، {v} دينار — هذا سعر {p} المكتوب عندي",
    "إي والله، {p} بـ{v} دينار بالضبط",
    "متأكد، {v} دينار عيني",
]
ANS_PRICE = [
    "السعر {v} دينار عيني، هذا المثبت عندي على {p}",
    "{v} دينار هو السعر، ما تغير — {p}",
    "إي {v} دينار، هذا سعر {p} عدنا",
]
ANS_REPEAT = [
    "{v} دينار عيني، {p}",
    "تدلل، {p} بـ{v} دينار",
    "{p} — {v} دينار",
]
ANS_CHEAP = [
    "إي عيني، {v} دينار هو سعر {p}",
    "متأكد، {p} بـ{v} دينار",
]

DOUBT_SETS = [(DOUBT_PLAIN, ANS_PLAIN), (DOUBT_PRICE, ANS_PRICE),
              (DOUBT_REPEAT, ANS_REPEAT), (DOUBT_CHEAP, ANS_CHEAP)]


def gen_price_doubt(n):
    """زبون يشكّك بالسعر مرة — الرد يعيد نفس الرقم."""
    out = []
    for _ in range(n):
        items = pick_items(4)
        sysm = build_system([(p, v) for p, v, _ in items])
        p, v, _ = random.choice(items)
        qs, ans = random.choice(DOUBT_SETS)
        out.append(rec("price_consistency_doubt", [
            {"role": "system", "content": sysm},
            {"role": "user", "content": random.choice(ASK).format(p=p)},
            {"role": "assistant",
             "content": random.choice(FIRST).format(p=p, v=money(v))},
            {"role": "user", "content": random.choice(qs)},
            {"role": "assistant",
             "content": random.choice(ans).format(p=p, v=money(v))},
        ]))
    return out


# ── تشكيك مضاعف: يسأل ثلاث مرات، والرقم ما يتحرك ──
ANS_THIRD = [
    "نفس الرقم عيني، {v} دينار — ما يتغير",
    "{v} دينار، هو هو من أول مرة",
    "بعده {v} دينار عيني، هذا المكتوب عندي",
    "{v} دينار، ثابت",
]


def gen_price_triple(n):
    """ثلاث محاولات تشكيك متتالية — الرقم ثابت بالثلاثة."""
    out = []
    for _ in range(n):
        items = pick_items(4)
        sysm = build_system([(p, v) for p, v, _ in items])
        p, v, _ = random.choice(items)
        q1s, a1s = random.choice(DOUBT_SETS)
        q2s, _ = random.choice([s for s in DOUBT_SETS if s[0] is not q1s])
        out.append(rec("price_consistency_triple", [
            {"role": "system", "content": sysm},
            {"role": "user", "content": random.choice(ASK).format(p=p)},
            {"role": "assistant",
             "content": random.choice(FIRST).format(p=p, v=money(v))},
            {"role": "user", "content": random.choice(q1s)},
            {"role": "assistant",
             "content": random.choice(a1s).format(p=p, v=money(v))},
            {"role": "user", "content": random.choice(q2s)},
            {"role": "assistant",
             "content": random.choice(ANS_THIRD).format(p=p, v=money(v))},
        ]))
    return out


# ── الفرق الحاسم: تشكيك ≠ مساومة ──
# نفس المحادثة: يشكّك (يرجع الرقم) ثم يساوم (يرفض التنزيل).
# هذي تفكّ الخلط اللي يخلي الموديل يرد بجملة الصلاحية على التشكيك.
BARGAIN = ["ما تنزل شوية؟", "آخر سعر شكد؟", "ما اكو تخفيض؟",
           "نزّلها شوية عيني"]
BARGAIN_A = [
    "هذا آخر سعر عيني، {v} دينار",
    "السعر صافي، {v} دينار وما أگدر أنزل",
    "{v} دينار آخر شي، هذا المثبت",
]


def gen_doubt_vs_bargain(n):
    """التشكيك يرجّع الرقم، والمساومة ترفض التنزيل — بنفس المحادثة."""
    out = []
    for _ in range(n):
        items = pick_items(4)
        sysm = build_system([(p, v) for p, v, _ in items])
        p, v, _ = random.choice(items)
        qs, ans = random.choice(DOUBT_SETS)
        out.append(rec("price_doubt_vs_bargain", [
            {"role": "system", "content": sysm},
            {"role": "user", "content": random.choice(ASK).format(p=p)},
            {"role": "assistant",
             "content": random.choice(FIRST).format(p=p, v=money(v))},
            {"role": "user", "content": random.choice(qs)},
            {"role": "assistant",
             "content": random.choice(ans).format(p=p, v=money(v))},
            {"role": "user", "content": random.choice(BARGAIN)},
            {"role": "assistant",
             "content": random.choice(BARGAIN_A).format(p=p, v=money(v))},
        ]))
    return out


# ════════════════════════════════════════════════════════════
# ٢) طلب قائمة الفئة
# ════════════════════════════════════════════════════════════
LIST_Q = ["شنو عندكم من {c}؟", "شنو المتوفر من {c}؟",
          "شعندكم {c}؟", "شنو الموجود عدكم بالـ{c}؟",
          "عرضلي {c} الموجودة"]
LIST_LEAD = ["من {c} عدنا:", "المتوفر من {c}:",
             "عدنا هالأصناف من {c}:", "{c} الموجودة عدنا:"]
LIST_ONE = [
    "من {c} ما عدنا غير {p} بـ{v} دينار",
    "بالـ{c} عدنا صنف واحد بس — {p} بـ{v} دينار",
    "{c}؟ الموجود {p} بس، بـ{v} دينار",
]


def fmt_list(items):
    return "\n".join(f"- {p}: {money(v)} دينار" for p, v in items)


def gen_category_list(n):
    """يعدّد المتوفر من فئة — من القائمة حصراً."""
    out = []
    for _ in range(n):
        # نبني نظاماً فيه فئتان على الأقل حتى يصير التعداد انتقائياً
        cats = random.sample([c for c in CATALOG if len(CATALOG[c]) >= 2], 2)
        other = random.choice([c for c in CATALOG if c not in cats])
        sys_items = (CATALOG[cats[0]] + CATALOG[cats[1]]
                     + CATALOG[other][:1])
        sysm = build_system(sys_items)
        c = cats[0]
        items = CATALOG[c]
        out.append(rec("category_list_request", [
            {"role": "system", "content": sysm},
            {"role": "user", "content": random.choice(LIST_Q).format(c=c)},
            {"role": "assistant",
             "content": random.choice(LIST_LEAD).format(c=c) + "\n"
                        + fmt_list(items)},
        ]))
    return out


def gen_category_list_single(n):
    """الفئة بيها صنف واحد — يگولها صراحة بدل ما يخترع ثاني."""
    out = []
    single = [c for c in CATALOG if len(CATALOG[c]) == 1]
    for _ in range(n):
        c = random.choice(single)
        p, v = CATALOG[c][0]
        other = random.choice([x for x in CATALOG if x != c])
        sysm = build_system([(p, v)] + CATALOG[other])
        out.append(rec("category_list_single", [
            {"role": "system", "content": sysm},
            {"role": "user", "content": random.choice(LIST_Q).format(c=c)},
            {"role": "assistant",
             "content": random.choice(LIST_ONE).format(c=c, p=p, v=money(v))},
        ]))
    return out


# ── «اكو غير هذا؟» بعد صنف معيّن: يعدّد الباقي من نفس الفئة ──
MORE_Q = ["اكو غيره؟", "شنو عندكم غير هذا؟", "اكو ثاني؟",
          "عندكم غيره شي؟", "اكو موديل ثاني؟"]
MORE_LEAD = ["إي عيني، هم عدنا:", "أكيد، الباقي عدنا:",
             "اكو، هذي البقية:"]
MORE_NONE = [
    "لا عيني، من {c} ما عدنا غير {p} — هذا الموجود",
    "هذا الوحيد من {c} عدنا حالياً",
]


def gen_more_in_category(n):
    """«اكو غيره؟» -> تعداد باقي الفئة، لا صنف واحد اعتباطي."""
    out = []
    for _ in range(n):
        c = random.choice([x for x in CATALOG if len(CATALOG[x]) >= 3])
        items = CATALOG[c]
        other = random.choice([x for x in CATALOG if x != c])
        sysm = build_system(items + CATALOG[other][:1])
        p, v = items[0]
        rest = items[1:]
        out.append(rec("category_list_more", [
            {"role": "system", "content": sysm},
            {"role": "user", "content": random.choice(ASK).format(p=p)},
            {"role": "assistant",
             "content": random.choice(FIRST).format(p=p, v=money(v))},
            {"role": "user", "content": random.choice(MORE_Q)},
            {"role": "assistant",
             "content": random.choice(MORE_LEAD) + "\n" + fmt_list(rest)},
        ]))
    return out


# ════════════════════════════════════════════════════════════
# ٣) التماسك بعد الإلغاء
# ════════════════════════════════════════════════════════════
QTY_Q = ["أريد {n} من {p}، شكد الاجمالي؟",
         "خذلي {n} {p}، شگد يطلع؟",
         "لو آخذ {n} منه، الاجمالي شكد؟"]
CANCEL_Q = ["لا خلص، ألغيها", "بطّل الطلب عيني", "لا ما أريد، ألغي",
            "كنسل الطلب", "خلص لا تريدها، ألغيها"]
CANCEL_A = ["تمام عيني، ألغيت الطلب", "خلص، انلغى الطلب",
            "تمام، ما بقى عليك شي", "انلغى عيني، أمرك"]
UNIT_Q = ["زين، وحدة وحدة بيش؟", "طيب الواحدة شكد؟",
          "بس گلي سعر الوحدة", "وحدة بس شكد تطلع؟"]
UNIT_A = ["الوحدة بـ{v} دينار عيني", "{p} الواحدة {v} دينار",
          "وحدة وحدة بـ{v} دينار", "سعر الوحدة {v} دينار"]


def gen_cancel_reset(n):
    """إلغاء طلب بكمية، ثم سؤال سعر الوحدة — الرد سعر الوحدة لا الاجمالي."""
    out = []
    for _ in range(n):
        items = pick_items(4)
        sysm = build_system([(p, v) for p, v, _ in items])
        p, v, _ = random.choice(items)
        q = random.choice([2, 3, 4, 5])
        total = v * q
        out.append(rec("cancel_state_reset", [
            {"role": "system", "content": sysm},
            {"role": "user", "content": random.choice(QTY_Q).format(n=q, p=p)},
            {"role": "assistant",
             "content": f"{q} من {p} بـ{money(v)} دينار للوحدة — "
                        f"الاجمالي {money(total)} دينار"},
            {"role": "user", "content": random.choice(CANCEL_Q)},
            {"role": "assistant", "content": random.choice(CANCEL_A)},
            {"role": "user", "content": random.choice(UNIT_Q)},
            {"role": "assistant",
             "content": random.choice(UNIT_A).format(p=p, v=money(v))},
        ]))
    return out


def gen_cancel_requantify(n):
    """إلغاء، ثم طلب نفس الصنف بكمية مختلفة — حساب جديد من الصفر."""
    out = []
    for _ in range(n):
        items = pick_items(4)
        sysm = build_system([(p, v) for p, v, _ in items])
        p, v, _ = random.choice(items)
        q1 = random.choice([4, 5, 6])
        q2 = random.choice([2, 3])
        out.append(rec("cancel_requantify", [
            {"role": "system", "content": sysm},
            {"role": "user", "content": random.choice(QTY_Q).format(n=q1, p=p)},
            {"role": "assistant",
             "content": f"{q1} من {p} — الاجمالي {money(v*q1)} دينار"},
            {"role": "user", "content": random.choice(CANCEL_Q)},
            {"role": "assistant", "content": random.choice(CANCEL_A)},
            {"role": "user",
             "content": random.choice(
                 [f"خليها {q2} بس", f"طيب خذلي {q2} منه",
                  f"أريد {q2} بدالها"])},
            {"role": "assistant",
             "content": f"{q2} من {p} بـ{money(v)} للوحدة — "
                        f"الاجمالي {money(v*q2)} دينار"},
        ]))
    return out


def gen_cancel_switch(n):
    """إلغاء، ثم سؤال عن صنف مختلف كلياً — ما يتلوث بالطلب الملغى."""
    out = []
    for _ in range(n):
        items = pick_items(4)
        sysm = build_system([(p, v) for p, v, _ in items])
        (p1, v1, _), (p2, v2, _) = random.sample(items, 2)
        q = random.choice([2, 3, 4])
        out.append(rec("cancel_switch_item", [
            {"role": "system", "content": sysm},
            {"role": "user", "content": random.choice(QTY_Q).format(n=q, p=p1)},
            {"role": "assistant",
             "content": f"{q} من {p1} — الاجمالي {money(v1*q)} دينار"},
            {"role": "user", "content": random.choice(CANCEL_Q)},
            {"role": "assistant", "content": random.choice(CANCEL_A)},
            {"role": "user", "content": random.choice(ASK).format(p=p2)},
            {"role": "assistant",
             "content": random.choice(FIRST).format(p=p2, v=money(v2))},
        ]))
    return out


# ════════════════════════════════════════════════════════════
# ٤) صيغ الرفض القياسية
# ════════════════════════════════════════════════════════════
# ثلاث صيغ بس — ترسّخ منوالاً يسهل قياسه، والتنويع القديم يبقى ذيلاً.
REJECT_STD = [
    "لا عيني، {p} مو موجود عدنا حالياً",
    "{p} ما عدنا منه حالياً",
    "والله {p} مو متوفر عدنا هسه",
]
REJECT_Q = ["عندكم {p}؟", "اكو {p} عدكم؟", "تبيعون {p}؟",
            "شكد سعر {p} عدكم؟", "{p} موجود؟"]
# رفض + عرض المتوفر (بلا اختراع بديل من برّه القائمة)
REJECT_ALT = [
    "{r}\nبس عدنا من {c}:\n{lst}",
    "{r} — الموجود عدنا من {c}:\n{lst}",
]


def gen_reject_standard(n):
    """رفض بصيغة قياسية، بلا بديل."""
    out = []
    for _ in range(n):
        items = pick_items(4)
        sysm = build_system([(p, v) for p, v, _ in items])
        miss = random.choice(MISSING)
        out.append(rec("reject_standard_form", [
            {"role": "system", "content": sysm},
            {"role": "user", "content": random.choice(REJECT_Q).format(p=miss)},
            {"role": "assistant",
             "content": random.choice(REJECT_STD).format(p=miss)},
        ]))
    return out


def gen_reject_with_list(n):
    """رفض قياسي + تعداد المتوفر من القائمة — يربط الرفض بالقائمة."""
    out = []
    for _ in range(n):
        c = random.choice([x for x in CATALOG if len(CATALOG[x]) >= 2])
        items = CATALOG[c]
        other = random.choice([x for x in CATALOG if x != c])
        sysm = build_system(items + CATALOG[other][:1])
        miss = random.choice(MISSING)
        out.append(rec("reject_standard_with_list", [
            {"role": "system", "content": sysm},
            {"role": "user", "content": random.choice(REJECT_Q).format(p=miss)},
            {"role": "assistant",
             "content": random.choice(REJECT_ALT).format(
                 r=random.choice(REJECT_STD).format(p=miss),
                 c=c, lst=fmt_list(items))},
        ]))
    return out


# ── رفض + تشكيك: «أكيد ماكو؟» -> يثبّت الرفض ──
REJECT_DOUBT_Q = ["أكيد ماكو؟", "لا صدگ؟", "متأكد ما عندكم؟",
                  "دور زين، أكيد ماكو؟"]
REJECT_DOUBT_A = [
    "متأكد عيني، {p} مو موجود عدنا",
    "إي أكيد، ما عدنا {p} حالياً",
    "متأكد، {p} مو بالقائمة عدي",
]


def gen_reject_doubt(n):
    """التشكيك بالرفض — نفس مبدأ ثبات السعر، مطبّق على الرفض."""
    out = []
    for _ in range(n):
        items = pick_items(4)
        sysm = build_system([(p, v) for p, v, _ in items])
        miss = random.choice(MISSING)
        out.append(rec("reject_consistency_doubt", [
            {"role": "system", "content": sysm},
            {"role": "user", "content": random.choice(REJECT_Q).format(p=miss)},
            {"role": "assistant",
             "content": random.choice(REJECT_STD).format(p=miss)},
            {"role": "user", "content": random.choice(REJECT_DOUBT_Q)},
            {"role": "assistant",
             "content": random.choice(REJECT_DOUBT_A).format(p=miss)},
        ]))
    return out


# ════════════════════════════════════════════════════════════
PLAN = [
    (gen_price_doubt,          520),
    (gen_price_triple,         300),
    (gen_doubt_vs_bargain,     300),
    (gen_category_list,        280),
    (gen_category_list_single, 140),
    (gen_more_in_category,     240),
    (gen_cancel_reset,         300),
    (gen_cancel_requantify,    200),
    (gen_cancel_switch,        200),
    (gen_reject_standard,      220),
    (gen_reject_with_list,     180),
    (gen_reject_doubt,         200),
]

# ── جمل ممنوعة بردود التشكيك: الدفاع بدل الرقم ──
DEFENSIVE = re.compile(
    r"ما أگدر أغير السعر|ما اگدر اغير|ما أگدر أتصرف|مو بيدي|"
    r"آسف|أعتذر|ما إلي علاقة|هذا مو شغلي")
NUM = re.compile(r"[\d،,]{3,}")


def validate(rows):
    """كل مثال لازم يحقق شرطه، وإلا الداتا تعلّم عكس المطلوب."""
    errs = Counter()

    for r in rows:
        cat = r["category"]
        msgs = r["messages"]
        sysm = " ".join(m["content"] for m in msgs if m["role"] == "system")
        asst = [m["content"] for m in msgs if m["role"] == "assistant"]

        # (أ) كل رقم بردود المساعد لازم يكون بالنظام أو حاصل ضرب مشروع
        for a in asst:
            for tok in NUM.findall(a):
                if tok not in sysm and tok not in " ".join(asst[:-0] or asst):
                    pass  # يُفحص بالتفصيل أدناه حسب الفئة

        # (ب) ثبات السعر: الرقم نفسه يتكرر بكل ردود المساعد
        if cat in ("price_consistency_doubt", "price_consistency_triple"):
            nums = [set(NUM.findall(a)) for a in asst]
            common = set.intersection(*nums) if nums else set()
            if not common:
                errs["السعر ما تكرر بكل الردود"] += 1
            if any(DEFENSIVE.search(a) for a in asst):
                errs["رد دفاعي بدل الرقم"] += 1

        # (ج) تشكيك ثم مساومة: الرقم ثابت بالثلاثة، والرفض بالأخير بس
        if cat == "price_doubt_vs_bargain":
            nums = [set(NUM.findall(a)) for a in asst]
            if not (nums and set.intersection(*nums)):
                errs["السعر تغير بين التشكيك والمساومة"] += 1
            if DEFENSIVE.search(asst[1]):
                errs["رد المساومة تسرّب لرد التشكيك"] += 1

        # (د) الإلغاء: الرد الأخير ما يحمل اجمالي الطلب الملغى
        if cat in ("cancel_state_reset", "cancel_requantify",
                   "cancel_switch_item"):
            stale = set(NUM.findall(asst[0])) - set(NUM.findall(sysm))
            if stale & set(NUM.findall(asst[-1])):
                errs["اجمالي الطلب الملغى تسرّب للرد الجديد"] += 1

        # (هـ) القوائم: كل صنف مذكور لازم يكون بالنظام
        if cat.startswith("category_list") or cat == "reject_standard_with_list":
            for a in asst:
                for tok in NUM.findall(a):
                    if tok not in sysm:
                        errs["صنف/سعر مو بالقائمة"] += 1

        # (و) الرفض: ما يذكر سعراً للصنف المرفوض
        if cat in ("reject_standard_form", "reject_consistency_doubt"):
            if any(NUM.search(a) for a in asst):
                errs["رقم برد رفض بلا قائمة"] += 1

        # (ز) ما ننتج مجانية غير مؤسَّسة (درس v24/v25)
        if any(re.search(r"مجان|بلاش", a) for a in asst) \
                and not re.search(r"مجان", sysm):
            errs["مجانية غير مؤسَّسة"] += 1

    return errs


def main():
    rows, seen = [], set()
    counts = {}
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
    p = DATA / "iraqi_v26_consistency.jsonl"
    with p.open("w", encoding="utf-8") as fh:
        for r in rows:
            fh.write(json.dumps(r, ensure_ascii=False) + "\n")

    print("=" * 62)
    print("v26 — ثبات الرقم، قائمة الفئة، وحالة الإلغاء")
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
