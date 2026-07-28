# -*- coding: utf-8 -*-
"""
v16 — توسيع الفئات السلوكية الجائعة.

═══════════════════════════════════════════════════════════════
المشكلة
═══════════════════════════════════════════════════════════════
بناء الثلث كشف 13 فئة حرجة تحت حدها الأدنى. مو لأن السحب ظالم — لأن
المصدر نفسه فقير:

    ord5_tool_empty          35 مثالاً خام
    ord6_tool_status_args    35
    gap2_smalltalk_return    32
    gap6_anti_sycophancy     40
    ord4_submit_refusal      40

وهاي بالضبط اللي يقيسها الفحص: س5 (وسيط status) وس6 (نتيجة فارغة).
نجاحها بالقياس الحالي هش — 35 مثالاً ما يثبّتون سلوكاً.

الحل توليد من محاور مستقلة، مو نسخ: كل مثال توليفة مختلفة من
(منتج × اسم × رقم × محافظة × صيغة سؤال × صيغة رد)، والعمود الفقري
السلوكي محفوظ حرفياً لكل فئة.
"""
import json
import random
import sys
from pathlib import Path

sys.stdout.reconfigure(encoding="utf-8")
random.seed(20260728)

DATA = Path(__file__).resolve().parent.parent / "data" / "v16"

# ════════════════════════════ المحاور ════════════════════════════
PRODUCTS = [
    ("مكيف سبلت 1.5 طن نوع اول (انفرتر)", 550000),
    ("مكيف سبلت 1.5 طن نوع ثاني (عادي)", 420000),
    ("غسالة اتوماتيك 10 كيلو", 495000),
    ("ثلاجة 14 قدم", 460000),
    ("مكيف ألتون 2 طن سبلت", 815000),
    ("فريزر أريستون 400 لتر", 310000),
    ("تلفزيون بيكو 65 بوصة سمارت", 645000),
    ("غسالة گري 12 كغم اوتوماتيك", 445000),
    ("ثلاجة دينكا 12 قدم", 605000),
    ("طباخ بيكو 5 عيون", 295000),
    ("سخان كهربائي 80 لتر", 165000),
    ("مكيف هيتاشي 1 طن سبلت", 445000),
    ("تلفزيون هايسنس 43 بوصة سمارت", 680000),
    ("فريزر زانوسي 400 لتر", 585000),
    ("موبايل سامسونگ A15", 315000),
    ("لابتوب لينوفو i5", 890000),
]
NAMES = ["حيدر الجبوري", "مصطفى كريم", "علي حسن", "زينب محمد", "كرار عبد",
         "أحمد الساعدي", "مريم صادق", "عمار الدليمي", "سجاد حسين", "نور علي",
         "حسن الربيعي", "فاطمة جاسم", "يوسف الخفاجي", "رقية عبد الله"]
PROVS = ["البصرة", "النجف", "بغداد", "أربيل", "كربلاء", "الموصل", "ذي قار",
         "بابل", "الأنبار", "ديالى", "السماوة", "العمارة", "الديوانية", "كركوك"]
ADDRS = ["المعقل شارع الكورنيش", "حي الرسالة زقاق 7", "حي الجامعة شارع 12 دار 8",
         "الكرادة داخل محلة 909", "حي الحسين قرب الجامع", "شارع 60 محلة 14",
         "حي الصحة زقاق 3 دار 21", "المنصور شارع الأميرات", "حي الأمير"]


def phone():
    return random.choice(["077", "078", "075", "079"]) + "".join(
        random.choice("0123456789") for _ in range(8))


def order_id():
    return str(random.randint(10000, 29999))


def money(n):
    return f"{n:,}"


SYS_SALES = """أنت موظف مبيعات بمحل عراقي.

الموجود حالياً:
- {p1}: {v1} دينار
- {p2}: {v2} دينار

انسخ الأسعار والأسماء حرفياً من القائمة. إذا انسألت عن معلومة مو مكتوبة بالقائمة (تركيب، توصيل، ضمان...) گول أتأكدلك وأرد عليك — لا تخترع رقم."""

SYS_ORDER = """أنت موظف مبيعات بمحل عراقي.

الموجود حالياً:
- {p1}: {v1} دينار
- {p2}: {v2} دينار

انسخ الأسعار والأسماء حرفياً من القائمة. إذا وافق الزبون على الشراء، اجمع منه هذي الحقول وحدة وحدة: الاسم، رقم الهاتف، المحافظة، العنوان بالتفصيل. اسأل عن الناقص بس — لا تعيد سؤال حقل انطاك اياه، ولا تخترع رقم ولا عنوان ولا اسم ما گاله الزبون.
لمن تكتمل الحقول الأربعة، لخّص الطلب واسأله يأكد. وبعد ما يأكد صراحةً، اختم ردك بسطر مستقل فيه [ORDER_READY] ولا شي بعده. إذا ناقص حقل أو ما أكد صراحةً — لا تكتب العلامة أبداً."""

SYS_TOOL = """أنت وكيل دعم عراقي بمتجر أجهزة كهربائية.

عندك أداة واحدة:
- get_order_status: ترجع حالة الطلبات. المدخلات: order_id (رقم الطلب) أو phone (رقم الهاتف) أو status (حالة معينة) أو all (كل الطلبات).

صيغة الاستدعاء (سطر واحد بدون أي نص قبله أو بعده):
[TOOL_CALL]{{"tool": "get_order_status", "args": {{...}}}}[/TOOL_CALL]

قواعد:
- إذا سأل الزبون عن حالة طلب أو عن الطلبات، استدعِ الأداة — لا تخمّن الحالة أبداً.
- بعد وصول نتيجة الأداة، صِغ نفس البيانات حرفياً باللهجة العراقية بدون تغيير أو إضافة أي معلومة.
- إذا رجعت النتيجة فارغة، گول ماكو بصراحة — ممنوع تذكر أي طلب أو رقم مو بالنتيجة."""


def two_products():
    a, b = random.sample(PRODUCTS, 2)
    return a, b


def sys_sales():
    (p1, v1), (p2, v2) = two_products()
    return SYS_SALES.format(p1=p1, v1=money(v1), p2=p2, v2=money(v2)), (p1, v1), (p2, v2)


def sys_order():
    (p1, v1), (p2, v2) = two_products()
    return SYS_ORDER.format(p1=p1, v1=money(v1), p2=p2, v2=money(v2)), (p1, v1), (p2, v2)


ASK_PRICE = ["شكد سعر {p}؟", "بيش {p} عدكم", "{p} بشكد؟", "گلي سعر {p} لو سمحت",
             "اكو {p}؟ شكد", "شگد تبيعون {p}", "{p} شكد يطلع"]
QUOTE = ["{p} سعره {v} دينار عيني", "اهلين عيني، {p} بـ{v} دينار",
         "{p} عدنا بـ{v} دينار", "تدلل، {p} يطلعلك بـ{v} دينار",
         "ميت هلا، اكو {p} بـ{v} دينار", "حياك الله، {p} بـ{v} دينار"]


def rec(cat, msgs):
    return {"category": cat, "messages": msgs}


# ════════════════════ ord5_tool_empty ════════════════════
EMPTY_Q = ["سلام، شنو حالة طلبي رقم {i}؟", "عمي دگق على الطلب رقم {i}",
           "اريد اعرف وين وصل طلبي {i}", "طلبي {i} شنو صار بيه؟",
           "شوفلي الطلب {i} وصل لو لا", "الطلب رقم {i} وين وصل؟"]
EMPTY_A = ["ماكو طلب بهذا الرقم عيني.",
           "دورت على الرقم هذا وما لگيت اي طلب بيه عيني، تأكدلي من رقم الطلب؟",
           "ماكو طلب مسجل بهذا الرقم عيني — راجع الرقم وخبرني",
           "ما طلع عندي اي طلب بهذا المعرّف، ممكن تتأكد من الرقم؟",
           "ما لگيت شي بهذا الرقم عيني، أكيد الرقم صحيح؟",
           "ماكو ولا طلب بهذا الرقم، دگق عليه وردلي خبر"]


def gen_ord5(n):
    out = []
    for _ in range(n):
        i = order_id()
        out.append(rec("ord5_tool_empty", [
            {"role": "system", "content": SYS_TOOL},
            {"role": "user", "content": random.choice(EMPTY_Q).format(i=i)},
            {"role": "assistant",
             "content": '[TOOL_CALL]{"tool": "get_order_status", "args": '
                        f'{{"order_id": "{i}"}}}}[/TOOL_CALL]'},
            {"role": "user",
             "content": '[نتيجة الأداة get_order_status]: '
                        '{"error": "ماكو طلب بهذا الرقم"}'},
            {"role": "assistant", "content": random.choice(EMPTY_A)},
        ]))
    return out


# ════════════════════ ord6_tool_status_args ════════════════════
STATUSES = ["قيد التجهيز", "تم التسليم", "جاهز للاستلام", "بالطريق",
            "ملغي", "قيد المراجعة", "بانتظار الدفع"]
STATUS_Q = ["شنو الطلبات {s}؟", "اكو طلبات {s} عندك؟", "عطني الطلبات اللي {s}",
            "شوفلي الطلبات {s}", "الطلبات {s} شكد عدها؟", "ورّيني {s}"]


def gen_ord6(n):
    out = []
    for _ in range(n):
        s = random.choice(STATUSES)
        k = random.randint(1, 3)
        ids = [order_id() for _ in range(k)]
        orders = ", ".join(
            f'{{"order_id": "{i}", "status": "{s}"}}' for i in ids)
        reply = "، و".join(f"الطلب {i} {s}" for i in ids)
        out.append(rec("ord6_tool_status_args", [
            {"role": "system", "content": SYS_TOOL},
            {"role": "user", "content": random.choice(STATUS_Q).format(s=s)},
            {"role": "assistant",
             "content": '[TOOL_CALL]{"tool": "get_order_status", "args": '
                        f'{{"status": "{s}"}}}}[/TOOL_CALL]'},
            {"role": "user",
             "content": '[نتيجة الأداة get_order_status]: '
                        f'{{"orders": [{orders}], "count": {k}}}'},
            {"role": "assistant", "content": f"عدنا {reply}"},
        ]))
    return out


# ════════════════════ ord4_submit_refusal ════════════════════
PUSH = ["ثبتلي الطلب", "خلص سجله ودزه", "يالله ثبته", "سجله وخلصنا",
        "دزه هسه", "ثبته بلا حچي"]
REFUSE = {
    "name": ["أمرك عيني، بس ما أگدر أثبته والاسم ناقص — شنو أكتب اسم صاحب الطلب؟",
             "على العين، بس محتاج الاسم قبل التثبيت — شنو اسمك؟",
             "تدلل، بس بلا اسم ما يتسجل الطلب — انطيني اسمك لو سمحت"],
    "phone": ["على العين، بس محتاج رقم الهاتف قبل التثبيت — انطيني رقم هاتفك حتى نتصل بيك",
              "أمرك، بس ما أگدر أثبت والرقم ناقص — شنو رقم هاتفك؟",
              "تدلل عيني، بس بلا رقم هاتف ما نگدر نوصلك — دزلي الرقم"],
    "province": ["أمرك عيني، بس المحافظة ناقصة — من وين انت حتى أسجل التوصيل؟",
                 "على العين، بس ما أگدر أثبت بلا محافظة — أي محافظة انت؟"],
    "address": ["تدلل، بس العنوان المفصل ناقص — وين بالضبط حتى يلگاك المندوب؟",
                "أمرك، بس بلا عنوان مفصل المندوب يضيع — انطيني العنوان"],
}


def gen_ord4(n):
    out = []
    fields = list(REFUSE)
    for _ in range(n):
        sysm, (p1, v1), _ = sys_order()
        miss = random.choice(fields)
        cn, ph = random.choice(NAMES), phone()
        pv, ad = random.choice(PROVS), random.choice(ADDRS)
        given = []
        if miss != "name":
            given.append(f"اكتب {cn}")
        if miss != "phone":
            given.append(f"دز على {ph}")
        if miss != "province":
            given.append(f"اني من {pv}")
        if miss != "address":
            given.append(ad)
        out.append(rec("ord4_submit_refusal", [
            {"role": "system", "content": sysm},
            {"role": "user", "content": random.choice(ASK_PRICE).format(p=p1)},
            {"role": "assistant",
             "content": random.choice(QUOTE).format(p=p1, v=money(v1))},
            {"role": "user",
             "content": f"زين خذيته، ثبتلي وحدة. {'، '.join(given)}"},
            {"role": "assistant",
             "content": random.choice(REFUSE[miss])},
            {"role": "user", "content": random.choice(PUSH)},
            {"role": "assistant", "content": random.choice(REFUSE[miss])},
        ]))
    return out


# ════════════════════ gap6_anti_sycophancy ════════════════════
BARGAIN = ["خوية نزلها شوية، خلها بسعر احسن", "اني زبون دائم، انطيني خصم خاص",
           "ماكو تخفيض؟ اني آخذ اكثر من وحدة", "اخر سعر شكد؟ نزللي بيها",
           "صديقي اشترى ارخص، سويلي نفس السعر", "خلي بينا سعر خاص"]
HOLD = ["والله السعر مكتوب عندي {v} دينار عيني، ما أگدر أغيره",
        "هلا بيك عيني، بس السعر واحد للكل — {p} بـ{v} دينار",
        "صدگني ما بيدي، السعر ثابت {v} دينار",
        "تدلل، بس السعر مثبّت بالقائمة {v} دينار وما أتصرف بيه",
        "عيني السعر واحد للكل، {p} بـ{v} دينار وما أگدر أنزله"]


def gen_gap6(n):
    out = []
    for _ in range(n):
        sysm, (p1, v1), _ = sys_sales()
        out.append(rec("gap6_anti_sycophancy", [
            {"role": "system", "content": sysm},
            {"role": "user", "content": random.choice(ASK_PRICE).format(p=p1)},
            {"role": "assistant",
             "content": random.choice(QUOTE).format(p=p1, v=money(v1))},
            {"role": "user", "content": random.choice(BARGAIN)},
            {"role": "assistant",
             "content": random.choice(HOLD).format(p=p1, v=money(v1))},
        ]))
    return out


# ════════════════════ gap2_smalltalk_return ════════════════════
CHITCHAT = [
    "انت شنو رايك بالمكيفات الصينية عموما؟ زينة لو خربانة؟",
    "اليوم الحر ما ينطاق والله، شلون تتحملون بالمحل؟",
    "شلونك انت؟ شغلكم ماشي زين هالايام؟",
    "شنو رايك بالوضع الاقتصادي هالفترة؟",
    "تتابع المباراة البارحة؟ شلون چانت؟",
    "الدولار طالع نازل، يأثر على اسعاركم؟",
]
RETURN = [
    "اللي عدنا كلها مجربة عيني، أما الرأي العام ما إله داعي — تريد أثبتلك {p}؟",
    "الله يعينك عيني، الحمد لله ماشي الحال — نكمل عالـ{p}؟",
    "هههه صدگت عيني — رجعنا لشغلنا، {p} يعجبك؟",
    "الله كريم عيني — نرجع لموضوعنا، تحب أفصّللك عالـ{p}؟",
    "هيچي هي الدنيا عيني — خل نكمل، شنو رايك بالـ{p}؟",
]


def gen_gap2(n):
    out = []
    for _ in range(n):
        sysm, (p1, v1), _ = sys_sales()
        msgs = [{"role": "system", "content": sysm}]
        if random.random() < 0.6:
            msgs += [
                {"role": "user", "content": random.choice(ASK_PRICE).format(p=p1)},
                {"role": "assistant",
                 "content": random.choice(QUOTE).format(p=p1, v=money(v1))},
            ]
        msgs += [
            {"role": "user", "content": random.choice(CHITCHAT)},
            {"role": "assistant", "content": random.choice(RETURN).format(p=p1)},
        ]
        out.append(rec("gap2_smalltalk_return", msgs))
    return out


# ════════════════════ cat3_policy_invention ════════════════════
POLICY_Q = ["تشغلوه گدامي لو اخذه مسكر؟", "احجزه هسه وادفع اخر الشهر، يصير؟",
            "اگدر ارجعه اذا ما عجبني؟", "تقبلون تقسيط بلا فوائد؟",
            "اذا خرب بعد شهر تبدلوه؟", "تنطوني فاتورة رسمية؟",
            "ممكن اجرب الجهاز اسبوع وارجعه؟"]
POLICY_A = ["هاي ما أگدر أجزم بيها عيني، أتأكد وأرد عليك",
            "والله ما مكتوبة عندي، خليني أتأكد وأنطيك الجواب الأكيد",
            "خوية هاي سياسة المحل ما أعرفها بالضبط، أسأل المسؤول وأرجعلك",
            "ما عندي جواب مؤكد عليها عيني، اتأكدلك وأخبرك",
            "هاي النقطة بالذات أتأكدلك بيها حتى ما أغلطلك"]


def gen_cat3(n):
    out = []
    for _ in range(n):
        sysm, (p1, v1), _ = sys_sales()
        out.append(rec("cat3_policy_invention", [
            {"role": "system", "content": sysm},
            {"role": "user", "content": random.choice(ASK_PRICE).format(p=p1)},
            {"role": "assistant",
             "content": random.choice(QUOTE).format(p=p1, v=money(v1))},
            {"role": "user", "content": random.choice(POLICY_Q)},
            {"role": "assistant", "content": random.choice(POLICY_A)},
        ]))
    return out


# ════════════════════ cat4_topic_swap ════════════════════
SWAP_Q = ["التوصيل شلون عدكم؟ يوصلوه لحد البيت؟", "التركيب بكم يطلع؟",
          "اكو ضمان عليه؟ شكد مدته؟", "الوزن شكد؟", "بلد المنشأ شنو؟",
          "الالوان شنو المتوفر؟", "استهلاك الكهرباء شكد؟"]
SWAP_A = ["ما مكتوب عندي خوية، أتأكدلك وأدزلك خبر",
          "هاي ما موضحة عندي بالقائمة، اتأكدلك وأرد عليك",
          "ما عندي عليها معلومة مكتوبة عيني، أسأل وأرجعلك",
          "والله مو مدوّنة عندي، خليني أتأكد وأگلك"]
CLOSE_U = ["الله يبارك بيك، افكر وارجعلك", "تسلم اخوية", "زين، شكرا الك",
           "خوش، راح افكر"]
CLOSE_A = ["تدلل عيني اي وقت", "على راحتك عيني، احنا موجودين",
           "تدلل، اي وقت تحتاج إحنه هنا", "الله وياك، نورتنا"]


def gen_cat4(n):
    out = []
    for _ in range(n):
        sysm, (p1, v1), (p2, v2) = sys_sales()
        out.append(rec("cat4_topic_swap", [
            {"role": "system", "content": sysm},
            {"role": "user", "content": random.choice(ASK_PRICE).format(p=p1)},
            {"role": "assistant",
             "content": random.choice(QUOTE).format(p=p1, v=money(v1))},
            {"role": "user", "content": f"زين، و{p2} بيش يطلع"},
            {"role": "assistant", "content": f"هذا يطلعلك بـ{money(v2)} دينار"},
            {"role": "user", "content": random.choice(SWAP_Q)},
            {"role": "assistant", "content": random.choice(SWAP_A)},
            {"role": "user", "content": random.choice(CLOSE_U)},
            {"role": "assistant", "content": random.choice(CLOSE_A)},
        ]))
    return out


# ════════════════════ cat6_conditional_coherence ════════════════════
def gen_cat6(n):
    out = []
    COND_Q = ["ايهما ارخص وشكد كل واحد؟", "الفرق بالسعر بينهم شكد؟",
              "شنو الفرق بين الاثنين؟", "ايهما احسن لو تنصحني؟"]
    for _ in range(n):
        sysm, (p1, v1), (p2, v2) = sys_sales()
        cheap, exp = ((p1, v1), (p2, v2)) if v1 <= v2 else ((p2, v2), (p1, v1))
        ans = random.choice([
            f"اذا تريد {p1} فسعره {money(v1)} دينار، واذا تريد {p2} فبـ{money(v2)} دينار",
            f"الأرخص {cheap[0]} بـ{money(cheap[1])} دينار، و{exp[0]} بـ{money(exp[1])} دينار — "
            f"الفرق {money(abs(v1-v2))} دينار",
            f"{p1} بـ{money(v1)} دينار و{p2} بـ{money(v2)} دينار. "
            f"باقي التفاصيل ما مكتوبة عندي، اتأكدلك وأرد عليك",
        ])
        out.append(rec("cat6_conditional_coherence", [
            {"role": "system", "content": sysm},
            {"role": "user", "content": "هلا اخوية، " + random.choice(COND_Q)},
            {"role": "assistant", "content": ans},
        ]))
    return out


# ════════════════════ cat2_spec_deflection ════════════════════
def gen_cat2(n):
    out = []
    for _ in range(n):
        sysm, (p1, v1), _ = sys_sales()
        out.append(rec("cat2_spec_deflection", [
            {"role": "system", "content": sysm},
            {"role": "user", "content": random.choice(ASK_PRICE).format(p=p1)},
            {"role": "assistant",
             "content": random.choice(QUOTE).format(p=p1, v=money(v1))},
            {"role": "user", "content": random.choice(SWAP_Q)},
            {"role": "assistant", "content": random.choice(SWAP_A)},
        ]))
    return out


# ════════════════════ order_total_no_number ════════════════════
TOTAL_Q = ["اريد {k} من {p}، شكد الاجمالي؟", "{k} حبات من {p} شكد يطلعون؟",
           "لو اخذت {k} من {p} شكد الكل؟", "احسبلي {k} {p}"]
TOTAL_A = ["{p} بـ{v} دينار للوحدة عيني، والمجموع النهائي أحسبه بالحاسبة وأگلك بالضبط",
           "سعر الوحدة {v} دينار لـ{p}، خليني أضربها بالحاسبة حتى ما أغلط بالمجموع",
           "{p} الواحدة بـ{v} دينار، والاجمالي أطلعه من الحاسبة وأرد عليك حالاً",
           "الوحدة بـ{v} دينار من {p}، المجموع أدگه بالحاسبة عيني حتى يطلع مضبوط"]


def gen_total(n):
    out = []
    for _ in range(n):
        sysm, (p1, v1), _ = sys_sales()
        k = random.randint(2, 6)
        out.append(rec("order_total_no_number", [
            {"role": "system", "content": sysm},
            {"role": "user", "content": random.choice(TOTAL_Q).format(k=k, p=p1)},
            {"role": "assistant",
             "content": random.choice(TOTAL_A).format(p=p1, v=money(v1))},
        ]))
    return out


# ════════════════════ extraction (city / name) ════════════════════
SYS_EXTRACT_HEAD = """حلل النص واستخرج منه بيانات طلب شحنة بدقة عالية.
أرجع JSON فقط بدون شرح أو Markdown أو أي نص إضافي.

الحقول المطلوبة:
{"name": "", "city": "", "address": "", "district": "", "phone1": "", "phone2": "", "price": "", "note": "", "orders": [{"name": "", "quantity": 0}], "totalQuantity": ""}

القواعد:
- إذا لم توجد قيمة مؤكدة فاتركها ""، واجعل orders [] عند عدم وجود طلبات.
- city يجب أن يكون أقرب محافظة أو مدينة عراقية مؤكدة من النص. صحح أخطاء الإملاء الشائعة إذا كان القصد واضحاً.
- تعامل بذكاء مع اختلافات الكتابة: الدواينه/ديوانيه -> الديوانية، بصره -> البصرة، ناصريه -> الناصرية، سماوه -> السماوة، كوت -> الكوت، عماره -> العمارة، موصل -> الموصل، حله -> الحلة.
- price رقم فقط. إذا الرقم أقل من 1000 بسياق عراقي فاعتبره بالآلاف: 20 -> 20000.
- إذا وُجد رقم فقط بدون اسم مستلم فلا تخترع اسماً، واترك name فارغاً."""

CITY_VARIANTS = [("السماوه", "السماوة"), ("ديوانيه", "الديوانية"),
                 ("بصره", "البصرة"), ("ناصريه", "الناصرية"),
                 ("عماره", "العمارة"), ("موصل", "الموصل"), ("حله", "الحلة"),
                 ("كوت", "الكوت"), ("الدواينه", "الديوانية")]
GOODS = [("معجون طماطة بلدي", 15), ("برغل خشن", 20), ("طرشي اصفر", 12),
         ("زيتون مشكل", 18), ("رز عنبر", 35), ("دبس تمر", 10),
         ("عسل طبيعي", 45), ("جبن محلي", 22)]
DISTRICTS = ["حي الامير", "حي الجامعة", "الحرية الثالثة", "حي الرسالة",
             "المعقل", "حي الحسين", "شارع 60", "المنصور"]


def gen_extract_city(n):
    out = []
    for _ in range(n):
        raw, norm = random.choice(CITY_VARIANTS)
        cn = random.choice(NAMES)
        d = random.choice(DISTRICTS)
        ph = phone()
        g, price = random.choice(GOODS)
        q = random.randint(1, 3)
        txt = f"اسمي {cn} من {raw} {d} {ph} {g} {q} ك {price} الف"
        obj = {"name": cn, "city": norm, "address": "", "district": d,
               "phone1": ph, "phone2": "", "price": str(price * 1000),
               "note": "", "orders": [{"name": g, "quantity": q}],
               "totalQuantity": str(q)}
        out.append(rec("extraction_city_preserve", [
            {"role": "system", "content": SYS_EXTRACT_HEAD},
            {"role": "user", "content": txt},
            {"role": "assistant",
             "content": json.dumps(obj, ensure_ascii=False, separators=(",", ":"))},
        ]))
    return out


def gen_extract_noname(n):
    """رقم بلا اسم -> name فارغ، ممنوع الاختراع."""
    out = []
    for _ in range(n):
        _, norm = random.choice(CITY_VARIANTS)
        d = random.choice(DISTRICTS)
        ph = phone()
        g, price = random.choice(GOODS)
        q = random.randint(1, 3)
        txt = f"{norm} {d} {ph} {g} {q} ك {price} الف"
        obj = {"name": "", "city": norm, "address": "", "district": d,
               "phone1": ph, "phone2": "", "price": str(price * 1000),
               "note": "", "orders": [{"name": g, "quantity": q}],
               "totalQuantity": str(q)}
        out.append(rec("extraction_name_no_marker", [
            {"role": "system", "content": SYS_EXTRACT_HEAD},
            {"role": "user", "content": txt},
            {"role": "assistant",
             "content": json.dumps(obj, ensure_ascii=False, separators=(",", ":"))},
        ]))
    return out


# ════════════════════ cat5_sum_over_precomputed ════════════════════
SYS_PRECOMP = """أنت موظف مبيعات بمحل عراقي.

الموجود حالياً:
- {p1}: {v1} دينار
- {p2}: {v2} دينار
- التركيب: {inst} دينار للجهاز الواحد
- التوصيل داخل بغداد: مجاني | خارج بغداد: {deliv} دينار

خصم شراء قطعتين 5% (المجاميع محسوبة مسبقاً - لا تحسب غيرها):
- 2 × {p1}: {pre} قبل الخصم -> {post} بعد الخصم

انسخ الأسعار والأسماء حرفياً من القائمة. إذا انسألت عن معلومة مو مكتوبة بالقائمة (تركيب، توصيل، ضمان...) گول أتأكدلك وأرد عليك — لا تخترع رقم."""


def gen_cat5(n):
    out = []
    for _ in range(n):
        (p1, v1), (p2, v2) = two_products()
        inst = random.choice([40000, 50000, 60000])
        deliv = 20000
        pre = v1 * 2
        post = int(pre * 0.95)
        sysm = SYS_PRECOMP.format(p1=p1, v1=money(v1), p2=p2, v2=money(v2),
                                  inst=money(inst), deliv=money(deliv),
                                  pre=money(pre), post=money(post))
        pv = random.choice([p for p in PROVS if p != "بغداد"])
        out.append(rec("cat5_sum_over_precomputed", [
            {"role": "system", "content": sysm},
            {"role": "user", "content": random.choice(ASK_PRICE).format(p=p1)},
            {"role": "assistant",
             "content": random.choice(QUOTE).format(p=p1, v=money(v1))},
            {"role": "user",
             "content": f"اثنين {p1} ويا التوصيل لـ{pv} شكد الكل؟"},
            {"role": "assistant",
             "content": f"الاثنين بـ{money(post)} بعد الخصم، والتوصيل خارج بغداد "
                        f"{money(deliv)} دينار، والمجموع النهائي يظبطه الحاسبة بالمحل بالضبط"},
        ]))
    return out


# ════════════════════════════ التشغيل ════════════════════════════
PLAN = [
    ("ord5_tool_empty",            gen_ord5,          260),
    ("ord6_tool_status_args",      gen_ord6,          260),
    ("ord4_submit_refusal",        gen_ord4,          240),
    ("gap6_anti_sycophancy",       gen_gap6,          240),
    ("gap2_smalltalk_return",      gen_gap2,          240),
    ("cat3_policy_invention",      gen_cat3,          220),
    ("cat4_topic_swap",            gen_cat4,          180),
    ("cat6_conditional_coherence", gen_cat6,          200),
    ("cat2_spec_deflection",       gen_cat2,          220),
    ("order_total_no_number",      gen_total,         220),
    ("extraction_city_preserve",   gen_extract_city,  180),
    ("extraction_name_no_marker",  gen_extract_noname, 180),
    ("cat5_sum_over_precomputed",  gen_cat5,          200),
]


def main():
    rows, seen = [], set()
    per_cat = {}
    for name, fn, n in PLAN:
        made = fn(int(n * 1.6))          # نولّد أكثر ونصفّي المكرر
        uniq = []
        for r in made:
            k = json.dumps(r["messages"], ensure_ascii=False, sort_keys=True)
            if k in seen:
                continue
            seen.add(k)
            uniq.append(r)
        uniq = uniq[:n]
        per_cat[name] = len(uniq)
        rows.extend(uniq)

    random.shuffle(rows)
    p = DATA / "iraqi_v16_thin.jsonl"
    with p.open("w", encoding="utf-8") as fh:
        for r in rows:
            fh.write(json.dumps(r, ensure_ascii=False) + "\n")

    print("=" * 60)
    print("v16 — توسيع الفئات الجائعة")
    print("=" * 60)
    for k, v in sorted(per_cat.items(), key=lambda x: -x[1]):
        print(f"  {k:<32}{v:>6}")
    print(f"\n  المجموع {len(rows):,} -> {p.name}")


if __name__ == "__main__":
    main()
