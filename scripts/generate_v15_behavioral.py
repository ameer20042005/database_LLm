# -*- coding: utf-8 -*-
"""
توليد v15 — توسيع الفئات السلوكية الرقيقة (gap*/ord*/cat1_*/v9).

═══════════════════════════════════════════════════════════════
لماذا: كتلة behavioral تبلغ 5.4% من هدف 9% حتى بعد v14
═══════════════════════════════════════════════════════════════
سبب النقص أن هذي الفئات صغيرة أصلاً (8–35 مثالاً)، وبلوغ الحصة منها
يتطلب تكرار ×2 وأكثر — وهو بالضبط خطر الحفظ اللي نتجنبه. الحل توسيعها
بأمثلة جديدة مبنية على نفس المبدأ السلوكي بمحاور مستقلة.

كل فئة تحافظ على عمودها الفقري السلوكي حرفياً:
  gap1  إحالة: معلومة مو بالقائمة → «أتأكدلك وأرد عليك» (بلا اختراع رقم)
  gap3  سؤال حقل واحد بصيغ مختلفة، بلا إعادة سؤال حقل انطاه الزبون
  gap4  ماكو المطلوب → صراحة + بديل من القائمة حرفياً
  gap5  تغيير رأي وسط الطلب (إلغاء/تعديل كمية/رجوع للتصفح)
  ord3  بوابة التأكيد: ملخّص → طلب تأكيد صريح (بلا [ORDER_READY] بعد)
  ord1  المسار الكامل: أربع حقول → ملخّص → تأكيد → [ORDER_READY]
  ord2  حجب العلامة لأن شرط ما اكتمل
  cat1_ تفصيلة مو بالكتالوج (ضمان/توصيل/تركيب/استهلاك) → أتأكدلك

الإخراج: data/iraqi_v15_behavioral.jsonl
"""
import json
import random
import sys
from collections import Counter
from pathlib import Path

sys.stdout.reconfigure(encoding="utf-8")
random.seed(20260729)
DATA = Path(__file__).resolve().parent.parent / "data"
SOURCE = "generate_v15_behavioral.py"

PRODUCTS = [
    ("مكيف هيتاشي 2 طن سبلت", 680_000), ("طباخ ميديا 5 عيون", 370_000),
    ("فريزر زانوسي 400 لتر", 585_000), ("غسالة گري 7 كغم اوتوماتيك", 560_000),
    ("تلفزيون هايسنس 43 بوصة سمارت", 680_000), ("مكيف هيتاشي 1 طن سبلت", 445_000),
    ("فريزر كونكورد 200 لتر", 590_000), ("ثلاجة سامسونگ 18 قدم", 1_150_000),
    ("نشافة بيكو 8 كغم", 495_000), ("سخان كهربائي 80 لتر", 165_000),
    ("مروحة سقفية 56 بوصة", 78_000), ("ميكرويف شارب 25 لتر", 210_000),
    ("طاولة سفرة 6 كراسي", 640_000), ("كنفة 7 مقاعد", 1_250_000),
    ("موبايل سامسونگ A15", 315_000), ("لابتوب لينوفو i5", 890_000),
]
NAMES = ["حيدر الجبوري", "كرار عبد", "أحمد الساعدي", "مصطفى الزاملي",
         "علي حسين", "زينب كاظم", "نور الهدى", "سجاد العامري",
         "محمد الربيعي", "فاطمة علي", "حسن الخفاجي", "عمار الدليمي",
         "يوسف الطائي", "مريم صادق", "أمير الشمري", "ليلى حمودي"]
PHONES = [f"077{n:08d}" for n in random.sample(range(10_000_000, 99_999_999), 40)]
CITIES = ["بغداد", "البصرة", "أربيل", "النجف", "كربلاء", "الموصل",
          "السماوة", "الديوانية", "بابل", "ذي قار", "كركوك", "الأنبار"]
ADDRS = ["الكرادة محلة 909 زقاق 15", "حي الجامعة شارع 12 دار 8",
         "المنصور محلة 605 زقاق 3", "الدورة محلة 836 دار 22",
         "حي الحسين قرب الجامع", "شارع الرشيد عمارة النور",
         "حي السلام محلة 44 زقاق 9", "المعقل شارع الكورنيش دار 5",
         "حي الأطباء محلة 12", "الجزائر شارع 20 دار 33"]

fmt = lambda n: f"{n:,}"


def _cat(k=2):
    return random.sample(PRODUCTS, k)


def _sysmsg(items, tail):
    body = "\n".join(f"- {n}: {fmt(p)} دينار" for n, p in items)
    return f"أنت موظف مبيعات بمحل عراقي.\n\nالموجود حالياً:\n{body}\n\n{tail}"


T_REFER = ("انسخ الأسعار والأسماء حرفياً من القائمة. إذا انسألت عن معلومة "
           "مو مكتوبة بالقائمة (تركيب، توصيل، ضمان...) گول أتأكدلك وأرد "
           "عليك — لا تخترع رقم.")
T_ALT = ("انسخ الأسعار والأسماء حرفياً من القائمة. إذا طلب الزبون شي مو "
         "موجود بالقائمة، گول ماكو بصراحة واعرض عليه البدائل الموجودة.")
T_ORDER = ("انسخ الأسعار والأسماء حرفياً من القائمة. إذا وافق الزبون على "
           "الشراء، اجمع منه هذي الحقول وحدة وحدة: الاسم، رقم الهاتف، "
           "المحافظة، العنوان بالتفصيل. اسأل عن الناقص بس — لا تعيد سؤال "
           "حقل انطاك اياه، ولا تخترع رقم ولا عنوان ولا اسم ما گاله الزبون.\n"
           "لمن تكتمل الحقول الأربعة، لخّص الطلب واسأله يأكد. وبعد ما يأكد "
           "صراحةً، اختم ردك بسطر مستقل فيه [ORDER_READY]")


def _row(cat, msgs, **kw):
    d = {"messages": msgs, "category": cat, "dialect": "iraqi_arabic",
         "source_file": SOURCE}
    d.update(kw)
    return d


PRICE_ASK = ["شكد سعر {p}", "بيش {p}؟", "{p} بشكد عندكم؟",
             "خويه شگد سعر {p}", "گلي سعر {p} لو سمحت",
             "عندكم {p}؟ وبيش؟", "ابو الشباب، بيش {p}"]
PRICE_REPLY = ["نورتنا، {p} يطلعلك بـ{v} دينار", "حياك الله، {p} عدنا بـ{v} دينار",
               "أهلين، {p} سعره {v} دينار", "ميت هلا، {p} عدنا بـ{v} دينار",
               "تدلل، {p} بـ{v} دينار", "{p} سعره {v} دينار عيني"]

# ── gap1: إحالة لمعلومة مو بالقائمة ──
REFER_Q = ["التركيب ياخذ شكد وقت عدكم؟", "الضمان شكد مدته؟",
           "التوصيل لبيتي بشكد؟", "استهلاك الكهرباء شكد؟",
           "اكو قطع غيار متوفرة؟", "منشأه من وين؟",
           "اكو تقسيط عليه؟", "شكد وزنه؟", "يجي بألوان ثانية؟",
           "الصيانة الدورية شكد تكلف؟", "اكو خدمة ما بعد البيع؟",
           "شكد ياخذ وقت التوصيل؟"]
REFER_A = ["{t} ما مكتوب عندي بالقائمة عيني، اتأكدلك وأرد عليك",
           "والله هذي المعلومة مو موجودة عندي، خلي اتأكدلك وأخبرك",
           "ما عندي هذا التفصيل مكتوب، أسأل وأرجعلك بالجواب",
           "هذا الشي ما أگدر أگلك بيه من راسي، اتأكدلك أول",
           "ما مكتوب عندي والله، انطيني وقت أتأكد وأرد عليك",
           "أخاف أگلك رقم غلط — اتأكدلك وأخبرك أكيد"]


def gen_gap1(n=420):
    out = []
    for _ in range(n):
        items = _cat(random.randint(1, 3))
        p, v = items[0]
        q = random.choice(REFER_Q)
        topic = q.split()[0].strip("؟")
        msgs = [{"role": "system", "content": _sysmsg(items, T_REFER)},
                {"role": "user", "content": random.choice(PRICE_ASK).format(p=p)},
                {"role": "assistant",
                 "content": random.choice(PRICE_REPLY).format(p=p, v=fmt(v))},
                {"role": "user", "content": q},
                {"role": "assistant",
                 "content": random.choice(REFER_A).format(t=topic)}]
        out.append(_row("gap1_referral_variety", msgs))
    return out


# ── gap4: ماكو المطلوب → بديل من القائمة ──
MISSING = ["ماطور ماي", "دراجة هوائية", "خيمة سفر", "مولدة كهرباء",
           "جهاز رياضي", "سجاد إيراني", "ساعة حائط", "مكنسة بخار",
           "دفاية زيتية", "حوض مطبخ", "شاشة عرض", "طابعة ليزر"]
ALT_A = ["والله {m} ماكو عدنا هسه، بس اكو {p} بـ{v} دينار — يناسبك؟",
         "{m} ما عدنا للأسف، الموجود عدنا {p} بـ{v} دينار، تحبه؟",
         "ماكو {m} عيني، بس أگدر أعرضلك {p} بـ{v} دينار",
         "للأسف {m} مو متوفر، اللي موجود {p} بـ{v} دينار — تشوفه؟",
         "{m} خلص من عدنا، بس {p} موجود بـ{v} دينار إذا يفيدك"]


def gen_gap4(n=420):
    out = []
    for _ in range(n):
        items = _cat(random.randint(1, 2))
        p, v = items[0]
        m = random.choice(MISSING)
        msgs = [{"role": "system", "content": _sysmsg(items, T_ALT)},
                {"role": "user",
                 "content": random.choice([f"محتاج {m}، اكو عدكم؟",
                                           f"عندكم {m}؟", f"دور لي على {m}",
                                           f"أريد {m} لو متوفر"])},
                {"role": "assistant",
                 "content": random.choice(ALT_A).format(m=m, p=p, v=fmt(v))}]
        out.append(_row("gap4_alternatives_phrasing", msgs))
    return out


# ── gap3: صياغة أسئلة الحقول ──
SLOT_Q = {
    "name": ["شنو اسمك حتى أسجل الطلب؟", "انطيني اسمك لو سمحت",
             "باسم منو أسجل الطلب؟", "اسمك الكريم عيني؟"],
    "phone": ["شنو رقمك حتى يكون عدنا بالطلب؟", "دزلي رقم هاتفك حتى نكدر نوصلك",
              "انطيني رقم موبايلك", "رقمك شنو حتى نتصل بيك؟"],
    "city": ["من وين انت حتى أسجل المحافظة؟", "من اي محافظة انت؟",
             "وين محافظتك عيني؟", "تريدها توصل لأي محافظة؟"],
    "addr": ["انطيني العنوان بالتفصيل حتى يلگاك المندوب",
             "العنوان بالضبط شنو؟", "وين بالضبط بالمحافظة؟",
             "دزلي عنوانك مفصل حتى ما يضيع المندوب"],
}
ACK = ["تدلل عيني", "على العين", "زين عيني", "خوش", "ماشي", "تمام"]


def gen_gap3(n=420):
    out = []
    for _ in range(n):
        items = _cat(2)
        p, v = items[0]
        slot = random.choice(list(SLOT_Q))
        msgs = [{"role": "system", "content": _sysmsg(items, T_ORDER)},
                {"role": "user", "content": random.choice(PRICE_ASK).format(p=p)},
                {"role": "assistant",
                 "content": random.choice(PRICE_REPLY).format(p=p, v=fmt(v))},
                {"role": "user",
                 "content": random.choice(["اوكي اريده، سجل الطلب",
                                           "زين احجزلي وحدة", "تمام، اثبته",
                                           "خذه، اريد اشتريه"])},
                {"role": "assistant",
                 "content": f"{random.choice(ACK)}، {random.choice(SLOT_Q[slot])}"}]
        out.append(_row("gap3_slot_questions", msgs))
    return out


# ── gap5: تغيير الرأي وسط الطلب ──
CHANGE = [("لا لحظة، ألغي الطلب", "ماشي عيني، ألغيته — إذا بدا لك شي ثاني أني موجود"),
          ("خليها اثنين مو وحدة", "زين، عدلتها لاثنين"),
          ("رجعني للبضاعة، أريد أشوف غيره", "تدلل، شوف على راحتك"),
          ("غيرت رأيي، أريد الثاني", "ماشي، أسجلك الثاني بدله"),
          ("خليها ثلاثة", "تمام، ثلاثة"),
          ("أجّلها لبكرة", "على راحتك عيني، أني موجود بأي وقت"),
          ("ألغي وخلص", "ماشي، ملغى — تدلل بأي وقت"),
          ("خفضها لوحدة بس", "زين، وحدة بس")]


def gen_gap5(n=380):
    out = []
    for _ in range(n):
        items = _cat(2)
        p, v = items[0]
        ch, rep = random.choice(CHANGE)
        msgs = [{"role": "system", "content": _sysmsg(items, T_ORDER)},
                {"role": "user", "content": random.choice(PRICE_ASK).format(p=p)},
                {"role": "assistant",
                 "content": random.choice(PRICE_REPLY).format(p=p, v=fmt(v))},
                {"role": "user", "content": "زين احجزلي وحدة"},
                {"role": "assistant",
                 "content": f"{random.choice(ACK)}، {random.choice(SLOT_Q['name'])}"},
                {"role": "user", "content": ch},
                {"role": "assistant", "content": rep}]
        out.append(_row("gap5_midorder_change", msgs))
    return out


# ── ord1/ord2/ord3: مسار الطلب والعلامة ──
def _order_head(items, p, v):
    return [{"role": "system", "content": _sysmsg(items, T_ORDER)},
            {"role": "user", "content": random.choice(PRICE_ASK).format(p=p)},
            {"role": "assistant",
             "content": random.choice(PRICE_REPLY).format(p=p, v=fmt(v))},
            {"role": "user",
             "content": random.choice(["اوكي اريده، سجل الطلب",
                                       "زين احجزلي وحدة", "تمام اثبته"])}]


def _collect(nm, ph, ct, ad):
    """أربع دورات جمع الحقول — الترتيب ثابت لأنه سلوك مقصود."""
    return [{"role": "assistant", "content": f"{random.choice(ACK)}، {random.choice(SLOT_Q['name'])}"},
            {"role": "user", "content": f"اسمي {nm}"},
            {"role": "assistant", "content": f"{random.choice(ACK)}، {random.choice(SLOT_Q['phone'])}"},
            {"role": "user", "content": f"رقمي {ph}"},
            {"role": "assistant", "content": f"{random.choice(ACK)}، {random.choice(SLOT_Q['city'])}"},
            {"role": "user", "content": ct},
            {"role": "assistant", "content": f"{random.choice(ACK)}، {random.choice(SLOT_Q['addr'])}"},
            {"role": "user", "content": ad}]


def _summary(p, v, nm, ph, ct, ad):
    return (f"هذا هو طلبك: {p} عدد 1 بـ{fmt(v)} دينار، باسم {nm} "
            f"ورقم هاتفك {ph}، التوصيل لـ{ct} — {ad}. أثبتلك الطلب؟")


def gen_ord(n_pos=340, n_gate=340, n_withheld=420):
    out = []
    for _ in range(n_pos):
        items = _cat(2); p, v = items[0]
        nm, ph, ct, ad = (random.choice(NAMES), random.choice(PHONES),
                          random.choice(CITIES), random.choice(ADDRS))
        msgs = _order_head(items, p, v) + _collect(nm, ph, ct, ad)
        msgs.append({"role": "assistant", "content": _summary(p, v, nm, ph, ct, ad)})
        msgs.append({"role": "user",
                     "content": random.choice(["نعم اكد", "إي أكد", "اثبته",
                                               "تمام اكده", "زين ثبته"])})
        msgs.append({"role": "assistant",
                     "content": random.choice(
                         ["تم تثبيت طلبك عيني، وياتك بأقرب وقت ان شاء الله.",
                          "ثبتناه، ويوصلك قريب ان شاء الله.",
                          "تم عيني، والمندوب راح يتصل بيك."]) + "\n[ORDER_READY]"})
        out.append(_row("ord1_marker_positive", msgs, direction="positive"))

    # ord3: بوابة التأكيد — ملخّص وسؤال، بلا علامة (ما أكد بعد)
    for _ in range(n_gate):
        items = _cat(2); p, v = items[0]
        nm, ph, ct, ad = (random.choice(NAMES), random.choice(PHONES),
                          random.choice(CITIES), random.choice(ADDRS))
        msgs = _order_head(items, p, v) + _collect(nm, ph, ct, ad)
        msgs.append({"role": "assistant", "content": _summary(p, v, nm, ph, ct, ad)})
        out.append(_row("ord3_confirm_gate", msgs, direction="negative"))

    # ord2: حجب العلامة — حقل ناقص، فما اكتمل الشرط
    for _ in range(n_withheld):
        items = _cat(2); p, v = items[0]
        nm, ph, ct = random.choice(NAMES), random.choice(PHONES), random.choice(CITIES)
        msgs = _order_head(items, p, v)
        stop = random.randint(1, 3)          # يتوقف قبل اكتمال الحقول
        full = _collect(nm, ph, ct, random.choice(ADDRS))
        # القطع عند سؤال الحقل التالي (دور assistant) لا عند رد الزبون:
        # المحادثة لازم تنتهي بدور assistant وإلا ما اكو هدف للتدريب،
        # والسلوك المطلوب تعليمه هو **سؤال الحقل الناقص** بلا علامة.
        msgs += full[:stop * 2 + 1]
        assert msgs[-1]["role"] == "assistant"
        out.append(_row("ord2_marker_withheld", msgs, direction="negative"))
    return out


# ── cat1_*: تفصيلة مو بالكتالوج ──
CAT1 = {
    "cat1_warranty_detail": (
        ["الضمان يشمل شنو بالضبط؟", "الضمان شكد سنة؟",
         "إذا خرب بالضمان تبدلوه؟", "الضمان يغطي الكهرباء؟"],
        ["تفاصيل الضمان ما مكتوبة عندي بالقائمة، اتأكدلك وأخبرك",
         "ما عندي تفصيل الضمان مكتوب عيني، أسأل وأرجعلك",
         "هذا ما أگدر أجزم بيه — اتأكدلك أول"]),
    "cat1_delivery_detail": (
        ["التوصيل بشكد؟", "توصلون لمحافظتي؟", "التوصيل ياخذ كم يوم؟",
         "اكو توصيل مجاني؟"],
        ["أجور التوصيل ما مكتوبة عندي، اتأكدلك وأرد عليك",
         "تفاصيل التوصيل مو موجودة بالقائمة، أسأل وأخبرك",
         "ما عندي رقم التوصيل مكتوب — خلي اتأكد"]),
    "cat1_install_detail": (
        ["التركيب بشكد؟", "التركيب مشمول بالسعر؟", "منو يجي يركبه؟",
         "التركيب ياخذ شكد وقت؟"],
        ["أجور التركيب ما مكتوبة عندي بالقائمة، اتأكدلك",
         "ما عندي تفصيل التركيب — أسأل وأرجعلك بالجواب",
         "هذا ما مكتوب عندي عيني، اتأكدلك وأخبرك"]),
    "cat1_consumption_detail": (
        ["استهلاك الكهرباء شكد؟", "يشتغل على المولدة؟",
         "كم أمبير يسحب؟", "استهلاكه عالي لو واطي؟"],
        ["الاستهلاك ما مكتوب عندي بالقائمة، اتأكدلك وأخبرك",
         "ما عندي رقم الاستهلاك — أسأل وأرد عليك",
         "هذا تفصيل فني ما موجود عندي، خلي اتأكدلك"]),
}


def gen_cat1(per=260):
    out = []
    for cat, (qs, ans) in CAT1.items():
        for _ in range(per):
            items = _cat(random.randint(1, 2)); p, v = items[0]
            msgs = [{"role": "system", "content": _sysmsg(items, T_REFER)},
                    {"role": "user", "content": random.choice(PRICE_ASK).format(p=p)},
                    {"role": "assistant",
                     "content": random.choice(PRICE_REPLY).format(p=p, v=fmt(v))},
                    {"role": "user", "content": random.choice(qs)},
                    {"role": "assistant", "content": random.choice(ans)}]
            out.append(_row(cat, msgs))
    return out


# ── v9: فئات صغيرة ──
def gen_v9(per=200):
    out = []
    for _ in range(per):          # natural_sale
        items = _cat(2); p, v = items[0]
        msgs = _order_head(items, p, v)
        msgs.append({"role": "assistant",
                     "content": f"{random.choice(ACK)}، {random.choice(SLOT_Q['name'])}"})
        out.append(_row("natural_sale", msgs))
    for _ in range(per):          # sequential_refusal
        items = _cat(2); p, v = items[0]
        m1, m2 = random.sample(MISSING, 2)
        msgs = [{"role": "system", "content": _sysmsg(items, T_ALT)},
                {"role": "user", "content": f"عندكم {m1}؟"},
                {"role": "assistant", "content": f"ماكو {m1} عدنا والله"},
                {"role": "user", "content": f"طيب {m2}؟"},
                {"role": "assistant",
                 "content": f"هم ماكو عيني، الموجود عدنا {p} بـ{fmt(v)} دينار"}]
        out.append(_row("sequential_refusal", msgs))
    for _ in range(per):          # missing_info
        items = _cat(2); p, v = items[0]
        msgs = [{"role": "system", "content": _sysmsg(items, T_ORDER)},
                {"role": "user", "content": "سجل طلبي"},
                {"role": "assistant",
                 "content": f"تدلل، بس أول شنو تريد من الموجود؟"},
                {"role": "user", "content": f"{p}"},
                {"role": "assistant",
                 "content": f"{random.choice(ACK)}، {random.choice(SLOT_Q['name'])}"}]
        out.append(_row("missing_info", msgs))
    for _ in range(per):          # order_total_no_number
        items = _cat(2); p, v = items[0]
        q = random.randint(2, 4)
        msgs = [{"role": "system", "content": _sysmsg(items, T_REFER)},
                {"role": "user", "content": f"اريد {q} من {p}، شكد الاجمالي؟"},
                {"role": "assistant",
                 "content": f"{p} بـ{fmt(v)} دينار للوحدة، و{q} منها يطلع "
                            f"{fmt(v * q)} دينار"}]
        out.append(_row("order_total_no_number", msgs))
    return out


def main():
    rows = (gen_gap1() + gen_gap4() + gen_gap3() + gen_gap5() +
            gen_ord() + gen_cat1() + gen_v9())

    key = lambda m: json.dumps(m, ensure_ascii=False, sort_keys=True)
    seen, uniq = set(), []
    for r in rows:
        k = key(r["messages"])
        if k not in seen:
            seen.add(k)
            uniq.append(r)
    dup = len(rows) - len(uniq)
    rows = uniq

    existing = set()
    for f in DATA.glob("*.jsonl"):
        if f.name.startswith(("iraqi_v15", "iraqi_final")):
            continue
        for line in f.open(encoding="utf-8"):
            try:
                existing.add(key(json.loads(line)["messages"]))
            except Exception:
                pass
    before = len(rows)
    rows = [r for r in rows if key(r["messages"]) not in existing]

    # ── فحص: [ORDER_READY] بس بالموجب ──
    for r in rows:
        blob = " ".join(t["content"] for t in r["messages"]
                        if t["role"] == "assistant")
        has = "[ORDER_READY]" in blob
        if has and r["category"] != "ord1_marker_positive":
            raise AssertionError(f"علامة بفئة سالبة: {r['category']}")
        if not has and r["category"] == "ord1_marker_positive":
            raise AssertionError("فئة موجبة بلا علامة")

    random.shuffle(rows)
    out = DATA / "iraqi_v15_behavioral.jsonl"
    with out.open("w", encoding="utf-8") as fh:
        for r in rows:
            fh.write(json.dumps(r, ensure_ascii=False) + "\n")

    c = Counter(r["category"] for r in rows)
    print(f"✅ {out.name}: {len(rows):,} مثال جديد")
    print(f"   (حُذف {dup:,} مكرر داخلياً، {before-len(rows):,} متداخل مع القائم)")
    print(f"\n{'الفئة':<34}{'جديد':>8}")
    for k, v in c.most_common():
        print(f"  {k:<32}{v:>8,}")
    print("\n✅ [ORDER_READY] موجودة بـord1 حصراً")


if __name__ == "__main__":
    main()
