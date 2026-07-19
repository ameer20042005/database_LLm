# -*- coding: utf-8 -*-
"""
توليد داتا v10 التصحيحية — تصحيح الفجوات الست من سجل تدخلات الدروع.

المخرجات:
  data/iraqi_v10_corrective.jsonl  (~350 محادثة، 6 فئات، اتجاهين: إجابة من الكتالوج / إحالة)
  data/iraqi_v10_extraction.jsonl  (~80 مثال استخراج تفاصيل الشحنة)
  data/iraqi_v10_items.jsonl       (~60 مثال استخراج المنتجات)

المبدأ الحاكم: التعليم شرطي بكتالوج المحادثة — المكتوب يُجاب حرفياً،
وغير المكتوب يُحال. الكتالوجات متغيرة بكل محادثة حتى يتعلم الموديل
"انسخ من الكتالوج" مو "احفظ حقائق".
"""
import difflib
import json
import random
import sys
from pathlib import Path

sys.stdout.reconfigure(encoding="utf-8")
random.seed(20260718)
DATA = Path(__file__).resolve().parent.parent / "data"
SOURCE = "generate_v10_corrective.py"

fmt = lambda n: f"{n:,}"


def too_similar(msg, pool, threshold=0.9):
    """فحص تشابه متناظر — نفس منطق validate_v10.py بالضبط."""
    for prev in pool:
        r = max(difflib.SequenceMatcher(None, msg, prev).ratio(),
                difflib.SequenceMatcher(None, prev, msg).ratio())
        if r > threshold:
            return True
    return False

SYSTEM_TMPL = (
    "أنت موظف مبيعات بمحل عراقي.\n\nالموجود حالياً:\n{items}\n\n"
    "انسخ الأسعار والأسماء حرفياً من القائمة. إذا انسألت عن معلومة مو مكتوبة "
    "بالقائمة (تركيب، توصيل، ضمان...) گول أتأكدلك وأرد عليك — لا تخترع رقم."
)

# ============================================================
# أدوات عامة
# ============================================================
BRANDS = ["شارب", "گري", "سامسونج", "LG", "هايسنس", "ميديا", "توشيبا", "بيكو",
          "كونكورد", "دينكا", "ألتون", "زانوسي", "دايو", "هيتاشي", "أريستون",
          "نيوال", "سيمفر", "فيلبس", "باناسونيك", "كاندي"]


def rand_price(lo, hi, step=5000):
    return random.randrange(lo // step, hi // step + 1) * step


def make_product(kinds=None):
    kind = random.choice(kinds or ["ac", "fridge", "washer", "freezer", "tv", "stove"])
    b = random.choice(BRANDS)
    if kind == "ac":
        size = random.choice(["1 طن", "1.5 طن", "2 طن"])
        style = random.choice(["انفرتر", "سبلت", ""])
        name = f"مكيف {b} {size}" + (f" {style}" if style else "")
        price = rand_price(400_000, 1_200_000)
    elif kind == "fridge":
        name = f"ثلاجة {b} {random.choice(['12 قدم', '14 قدم', '16 قدم', '18 قدم'])}"
        price = rand_price(350_000, 900_000)
    elif kind == "washer":
        name = f"غسالة {b} {random.choice(['7 كغم', '8 كغم', '10 كغم', '12 كغم'])} اوتوماتيك"
        price = rand_price(300_000, 750_000)
    elif kind == "freezer":
        name = f"فريزر {b} {random.choice(['200 لتر', '300 لتر', '400 لتر'])}"
        price = rand_price(300_000, 650_000)
    elif kind == "tv":
        name = f"تلفزيون {b} {random.choice(['43 بوصة', '50 بوصة', '55 بوصة', '65 بوصة'])} سمارت"
        price = rand_price(250_000, 1_100_000)
    else:
        name = f"طباخ {b} 5 عيون"
        price = rand_price(200_000, 550_000)
    return name, price


def pick_products(n=2, kinds=None):
    prods = {}
    while len(prods) < n:
        nm, pr = make_product(kinds)
        prods[nm] = pr
    return list(prods.items())


REFER_TAILS = [
    "اتأكدلك وأرد عليك",
    "أتأكدلك وأدزلك خبر",
    "أسأل وأرد عليك",
    "خل أتأكد وأخبرك",
    "أتأكدلك من المدير وأرجعلك",
    "اتأكدلك اليوم وأرد عليك",
    "أتأكد منها وأنطيك الجواب الأكيد",
    "أسألك صاحب المحل وأرد عليك",
    "اتأكدلك حتى ما أغلطلك عيني",
    "أتأكدلك هسه وأخبرك",
    "خليني أتأكد وأرجعلك بالجواب",
    "أتأكدلك وما أطول عليك",
]
tail = lambda: random.choice(REFER_TAILS)

LEADS = ["والله", "بصراحة", "صدگ", "والله عيني", "خوية"]
lead = lambda: random.choice(LEADS)

OPENERS = ["هلا بيك", "حياك الله", "هلا وغلا", "اهلين عيني", "تدلل خوية",
           "نورتنا", "حياك عيني", "يا هلا بيك", "اهلا بيك", "هلا حبيبي", "ميت هلا"]

FIRST_Q = [
    "بيش {p} عدكم",
    "شكد سعر {p}",
    "سلام عليكم، شكد {p} عدكم",
    "هلو، عندكم {p}؟ بيش سعره",
    "شگد تبيعون {p}",
    "{p} بيش عدكم",
    "مرحبا، بيش {p}",
    "هلو اخوية، شكد يطلع {p}",
    "اريد اسأل عن سعر {p} لو سمحت",
    "بيش ماخذين {p}",
    "صباح الخير، اكو {p}؟ شكد",
    "هلا، {p} موجود عدكم؟ بيش",
    "مساء الخير، شكد سعر {p} هسه",
    "اخوية بيش {p} اخر سعر",
]
FIRST_A = [
    "{o}، {p} عدنا بـ{pr} دينار",
    "{o}، اكو {p} بـ{pr} دينار وخوش جهاز",
    "{o}، سعر {p} {pr} دينار",
    "{o}، {p} يطلعلك بـ{pr} دينار",
    "{o}، موجود عيني، {p} بـ{pr} دينار",
    "{o}، {p} بـ{pr} دينار وصدگني يسوى",
]
SECOND_Q = ["و{p} شكد؟", "طيب {p} بيش", "زين، و{p} بيش يطلع", "اما {p} شكد سعره", "و{p} عدكم؟ شكد"]
SECOND_A = ["{p} بـ{pr} دينار عيني", "هذا يطلعلك بـ{pr} دينار", "سعره {pr} دينار خوية",
            "{p} عدنا بـ{pr}", "بـ{pr} دينار، وهم خوش جهاز"]
CLOSE_U = ["زين شكرا الله يخليك", "تسلم اخوية", "اوكي ممنون", "زين خل افكر واخبرك",
           "تمام شكرا جزيلا", "الله يبارك بيك، افكر وارجعلك"]
CLOSE_A = ["تدلل عيني اي وقت", "هلا بيك، احنا بالخدمة", "العفو خوية، تامر امر",
           "على راحتك عيني، احنا موجودين", "تدلل، اي شي تحتاجه اني هنا",
           "الله يحفظك، بانتظارك"]
TRAP_GREET = ["هلو، ", "سلام عليكم، ", "مرحبا، ", "هلا اخوية، ", ""]


def first_price_pair(p, pr):
    q = random.choice(FIRST_Q).format(p=p)
    a = random.choice(FIRST_A).format(o=random.choice(OPENERS), p=p, pr=fmt(pr))
    return q, a


def second_price_pair(p, pr):
    q = random.choice(SECOND_Q).format(p=p)
    a = random.choice(SECOND_A).format(p=p, pr=fmt(pr))
    return q, a


def assemble(catalog_text, trap_q, trap_a, products, category, direction):
    """يبني محادثة: سؤال الفخ بموقع عشوائي (أول / بعد سعر / بعد سعرين)."""
    pos = random.choice([0, 1, 1, 2])
    turns = []
    if pos >= 1:
        turns.append(first_price_pair(products[0][0], products[0][1]))
    if pos >= 2 and len(products) > 1:
        turns.append(second_price_pair(products[1][0], products[1][1]))
    if pos == 0:
        turns.append((random.choice(TRAP_GREET) + trap_q, trap_a))
    else:
        turns.append((trap_q, trap_a))
    if random.random() < 0.35:
        turns.append((random.choice(CLOSE_U), random.choice(CLOSE_A)))
    msgs = [{"role": "system", "content": SYSTEM_TMPL.format(items=catalog_text)}]
    for u, a in turns:
        msgs.append({"role": "user", "content": u})
        msgs.append({"role": "assistant", "content": a})
    return {"messages": msgs, "category": category, "direction": direction,
            "dialect": "iraqi", "source_file": SOURCE}


def catalog_lines(products, suffix_first=""):
    lines = []
    for i, (nm, pr) in enumerate(products):
        lines.append(f"- {nm}: {fmt(pr)} دينار" + (suffix_first if i == 0 else ""))
    return lines


# ============================================================
# الفئة 1: تفصيلة داخل موضوع مرخّص
# ============================================================
DURS = ["سنتين", "سنة وحدة", "ثلاث سنوات", "سنة ونص", "18 شهر"]

WARR_DETAIL_QS = [
    "الضمان يشمل الكومبريسر لو لا؟",
    "ضمانكم يغطي الكسر؟",
    "اذا وگع وانكسر، الضمان يمشي عليه؟",
    "اذا دخله ماي وخرب، الضمان يشمله؟",
    "قطع الغيار داخلة بالضمان لو اشتريها؟",
    "اكو استبدال جديد اذا طلع بيه عيب من اول اسبوع؟",
    "شنو الحالات اللي تلغي الضمان عدكم؟",
    "الضمان يشمل الشاشة اذا خربت؟",
    "الكارت الالكتروني داخل بالضمان؟",
    "التصليح بفترة الضمان ياخذون عليه فلوس؟",
    "المحرك مشمول بالضمان لو بس القطع الخارجية؟",
    "الريموت والملحقات عليها ضمان هم؟",
]
WARR_REFER_A = [
    "الضمان {dur} عيني، بس هاي التفصيلة ما مكتوبة عندي، {t}",
    "المكتوب عندي الضمان {dur} بس، وتفاصيل الشمول ما موجودة، {t}",
    "اللي أعرفه الضمان {dur}، أما هاي بالذات ما أگدر أجزم بيها، {t}",
    "عيني الضمان {dur} أكيد، بس سؤالك هذا أدق من المكتوب عندي، {t}",
    "الضمان {dur}، هذا الموجود بالقائمة، والباقي {t}",
    "ضمانه {dur} خوية، وهاي النقطة بالذات {t}",
]
WARR_ANSWER_SETS = [
    ("، ضمان {dur}، الضمان يشمل الكومبريسر وما يشمل الكسر",
     ["الضمان يشمل الكومبريسر؟", "الكومبريسر داخل بالضمان لو لا؟", "شنو يغطي الضمان بالضبط؟ الكومبريسر؟"],
     "إي عيني، الضمان {dur} ويشمل الكومبريسر، بس الكسر ما يشمله"),
    ("، ضمان {dur}، الضمان يشمل قطع الغيار وما يغطي ضرر الماي",
     ["قطع الغيار داخلة بالضمان؟", "الضمان يشمل قطع الغيار عدكم؟", "اذا احتاج قطعة غيار، الضمان يغطيها؟"],
     "إي خوية، الضمان {dur} ويشمل قطع الغيار، بس ضرر الماي ما يغطيه"),
    ("، ضمان {dur} ويا استبدال جديد اذا بيه عيب مصنعي بأول اسبوع",
     ["اذا طلع خربان اول اسبوع تبدلوه؟", "اكو استبدال اذا بيه عيب من البداية؟", "عيب المصنع شنو حله عدكم؟ تبديل؟"],
     "اكيد عيني، اذا بيه عيب مصنعي بأول اسبوع اكو استبدال جديد، والضمان {dur}"),
]

DELIV_AREAS = ["ابو غريب", "المحمودية", "التاجي", "الحسينية", "النهروان",
               "الراشدية", "اليوسفية", "سبع البور", "الطارمية", "المدائن"]
DELIV_REFER_QS = ["توصلون لـ{area}؟", "التوصيل يوصل لـ{area} لو لا؟",
                  "اني ساكن بـ{area}، توصيلكم يشملها؟", "منطقة {area} داخلة بتوصيلكم؟"]
DELIV_REFER_A = [
    "التوصيل داخل بغداد مجاني عيني، بس {area} بالضبط ما موضحة عندي، {t}",
    "المكتوب عندي التوصيل داخل بغداد مجاني، أما {area} تحديداً {t}",
    "داخل بغداد التوصيل مجاني، بس اذا {area} محسوبة داخل لو لا، {t}",
]
INST_REFER_QS = ["التركيب شامل المواد والبايبات؟", "تركيبكم يشمل البريكيت والمواد؟",
                 "التركيب ياخذون اضافي عالطوابق العالية؟", "مواد التركيب عليّ لو عليكم؟"]
INST_REFER_A = [
    "التركيب {inst} للجهاز عيني، بس المواد اذا داخلة بيه لو لا ما مكتوب عندي، {t}",
    "أجرة التركيب {inst} هاي المكتوبة، أما تفاصيل المواد {t}",
    "المكتوب عندي التركيب {inst} دينار بس، وهاي التفصيلة {t}",
]
CONS_REFER_QS = ["شكد يصرف كهرباء بالشهر تقريباً؟", "يعني شكد تجيني فلوس كهرباء بالشهر عليه؟",
                 "عالمولدة شكد ياخذ امبير؟", "استهلاكه بالليل الكامل شكد يطلع؟"]
CONS_REFER_A = [
    "المكتوب عندي استهلاكه ~{x} كيلوواط بالساعة، بس حسبة {what} ما أگدر أظبطهالك، {t}",
    "استهلاكه ~{x} كيلوواط/ساعة هذا الموجود، أما {what} بالضبط {t}",
]


def gen_cat1():
    convs = []
    # ضمان — إحالة (48)
    for _ in range(48):
        dur = random.choice(DURS)
        prods = pick_products(2)
        cat = "\n".join(catalog_lines(prods, f"، ضمان {dur}"))
        q = random.choice(WARR_DETAIL_QS)
        a = random.choice(WARR_REFER_A).format(dur=dur, t=tail())
        convs.append((cat, q, a, prods, "cat1_warranty_detail", "refer"))
    # ضمان — إجابة (32)
    for _ in range(32):
        dur = random.choice(DURS)
        suffix_t, qs, a_t = random.choice(WARR_ANSWER_SETS)
        prods = pick_products(2)
        cat = "\n".join(catalog_lines(prods, suffix_t.format(dur=dur)))
        convs.append((cat, random.choice(qs), a_t.format(dur=dur), prods,
                      "cat1_warranty_detail", "answer"))
    # توصيل — إحالة (20)
    for _ in range(20):
        prods = pick_products(2)
        cat = "\n".join(catalog_lines(prods) + ["- التوصيل داخل بغداد: مجاني"])
        area = random.choice(DELIV_AREAS)
        q = random.choice(DELIV_REFER_QS).format(area=area)
        a = random.choice(DELIV_REFER_A).format(area=area, t=tail())
        convs.append((cat, q, a, prods, "cat1_delivery_detail", "refer"))
    # توصيل — إجابة (12)
    for _ in range(12):
        prods = pick_products(2)
        a1, a2 = random.sample(DELIV_AREAS, 2)
        fee = fmt(random.choice([10_000, 15_000]))
        cat = "\n".join(catalog_lines(prods) +
                        [f"- التوصيل: داخل بغداد مجاني، وأطراف بغداد ({a1} و{a2}): {fee} دينار"])
        q = random.choice(DELIV_REFER_QS).format(area=a1)
        a = f"إي عيني نوصل لـ{a1}، أطراف بغداد التوصيل بـ{fee} دينار، وداخل بغداد مجاني"
        convs.append((cat, q, a, prods, "cat1_delivery_detail", "answer"))
    # تركيب — إحالة (16)
    for _ in range(16):
        prods = pick_products(2, ["ac"])
        inst = fmt(random.choice([40_000, 50_000, 60_000]))
        cat = "\n".join(catalog_lines(prods) + [f"- التركيب: {inst} دينار للجهاز"])
        q = random.choice(INST_REFER_QS)
        a = random.choice(INST_REFER_A).format(inst=inst, t=tail())
        convs.append((cat, q, a, prods, "cat1_install_detail", "refer"))
    # تركيب — إجابة (12)
    for _ in range(12):
        prods = pick_products(2, ["ac"])
        inst = fmt(random.choice([40_000, 50_000, 60_000]))
        cat = "\n".join(catalog_lines(prods) +
                        [f"- التركيب: {inst} دينار شامل المواد حتى 3 متر بايب"])
        q = random.choice(["التركيب شامل المواد؟", "مواد التركيب عليّ لو عليكم؟",
                           "البايبات داخلة بسعر التركيب؟"])
        a = f"إي عيني، التركيب {inst} وشامل المواد حتى 3 متر بايب"
        convs.append((cat, q, a, prods, "cat1_install_detail", "answer"))
    # استهلاك — إحالة (12)
    for _ in range(12):
        prods = pick_products(2, ["ac"])
        x = random.choice(["0.9", "1.0", "1.2", "1.5", "1.8"])
        cat = "\n".join(catalog_lines(prods, f"، استهلاك ~{x} كيلوواط/ساعة"))
        q = random.choice(CONS_REFER_QS)
        what = random.choice(["الشهر", "الامبير عالمولدة", "الليلة الكاملة"])
        a = random.choice(CONS_REFER_A).format(x=x, what=what, t=tail())
        convs.append((cat, q, a, prods, "cat1_consumption_detail", "refer"))
    # استهلاك — إجابة (8)
    for _ in range(8):
        prods = pick_products(2, ["ac"])
        x = random.choice(["1.0", "1.2", "1.5"])
        m = random.choice(["5", "8", "10"])
        cat = "\n".join(catalog_lines(prods, f"، استهلاك ~{x} كيلوواط/ساعة (حوالي {m} أمبير)"))
        q = random.choice(["شكد امبير ياخذ عالمولدة؟", "استهلاكه شكد امبير؟",
                           "عالمولدة شگد يسحب امبير؟"])
        a = f"ياخذ حوالي {m} أمبير عيني، واستهلاكه ~{x} كيلوواط بالساعة"
        convs.append((cat, q, a, prods, "cat1_consumption_detail", "answer"))
    return convs


# ============================================================
# الفئة 2: المواصفات غير المذكورة — إحالة بلا تهرب
# ============================================================
SPEC_SETS = [
    dict(key="لون", clause="الألوان",
         refer_qs=["شنو الوانه الموجوده؟", "اكو منه لون اسود؟", "الالوان شنو المتوفر عدكم؟",
                   "عدكم منه ابيض؟", "اريده رصاصي، اكو؟"],
         ans_line="- الألوان المتوفرة: أبيض وفضي",
         ans_qs=["شنو الالوان الموجوده؟", "اكو الوان غير الابيض؟"],
         ans_a="الموجود عدنا أبيض وفضي عيني، اختار اللي يعجبك"),
    dict(key="وزن", clause="الوزن",
         refer_qs=["شكد وزنه؟", "ثگيل لو خفيف؟ شكد يوزن", "وزنه شكد حتى اعرف اشلون انقله"],
         ans_line="- الوزن: 45 كغم",
         ans_qs=["شكد وزنه هذا؟", "شگد يوزن الجهاز؟"],
         ans_a="وزنه 45 كغم عيني، مكتوب عندي بالقائمة"),
    dict(key="ابعاد", clause="الأبعاد بالضبط",
         refer_qs=["شكد ابعاده؟ عندي مكان ضيگ", "شكد عرضه بالضبط؟", "ارتفاعه شكد؟ المطبخ عندي صغير"],
         ans_line="- الأبعاد: عرض 60 سم وارتفاع 185 سم",
         ans_qs=["شكد ابعاده؟", "عرضه وارتفاعه شكد؟"],
         ans_a="عرضه 60 سم وارتفاعه 185 سم عيني، قيسها عندك"),
    dict(key="ضجيج", clause="مستوى الصوت",
         refer_qs=["صوته عالي لو هادي؟", "يزعج بالليل لو لا؟ شكد ضجيجه", "شگد مستوى الصوت ماله؟"],
         ans_line="- مستوى الصوت: 42 ديسبل",
         ans_qs=["صوته شكد؟ عالي؟", "مستوى الضجيج ماله شكد؟"],
         ans_a="مستوى صوته 42 ديسبل عيني، يعني هادي"),
    dict(key="منشأ", clause="بلد المنشأ",
         refer_qs=["صناعة وين هذا؟", "بلد المنشأ شنو؟", "صناعه صيني لو تايلندي؟"],
         ans_line="- بلد المنشأ: تايلند",
         ans_qs=["صناعة وين؟", "منشأه شنو؟"],
         ans_a="صناعة تايلند عيني، مكتوبة عندي بالقائمة"),
    dict(key="غاز", clause="نوع الغاز",
         refer_qs=["شنو غاز التبريد ماله؟", "الغاز ماله شنو نوعه؟", "غازه من النوع الجديد لو القديم؟"],
         ans_line="- غاز التبريد: R410a",
         ans_qs=["شنو نوع الغاز ماله؟", "غاز التبريد شنو بيه؟"],
         ans_a="غازه R410a عيني، هذا المكتوب بالقائمة"),
]
SPEC_REFER_A = [
    "{clause} ما مكتوبة عندي بالقائمة، {t}",
    "{lead}، {clause} ما موضحة عندي، {t}",
    "سؤالك بمحله عيني، بس {clause} ما عندي عليها معلومة مكتوبة، {t}",
    "{clause} صدگ ما أعرفها بالضبط، {t}",
    "هاي {t}، لأن {clause} مو موجودة بالقائمة اللي عندي",
]


def gen_cat2():
    convs = []
    for spec in SPEC_SETS:
        for _ in range(12):  # إحالة
            prods = pick_products(2, ["ac"] if spec["key"] == "غاز" else None)
            cat = "\n".join(catalog_lines(prods))
            q = random.choice(spec["refer_qs"])
            a = random.choice(SPEC_REFER_A).format(clause=spec["clause"], lead=lead(), t=tail())
            convs.append((cat, q, a, prods, "cat2_spec_deflection", "refer"))
        for _ in range(8):  # إجابة
            prods = pick_products(2, ["ac"] if spec["key"] == "غاز" else None)
            cat = "\n".join(catalog_lines(prods) + [spec["ans_line"]])
            convs.append((cat, random.choice(spec["ans_qs"]), spec["ans_a"], prods,
                          "cat2_spec_deflection", "answer"))
    return convs


# ============================================================
# الفئة 3: سياسات المحل — ممنوع النفي الواثق
# ============================================================
POLICY_SETS = [
    dict(clause="التقسيط",
         refer_qs=["عدكم تقسيط؟", "اگدر اخذه اقساط؟", "تسوون بيع بالاقساط لو لازم كاش؟",
                   "اكو تقسيط بدون فوايد؟", "شهري شكد يطلع اذا قسطتوه؟"],
         ans_line="- التقسيط: متوفر على 6 أشهر بمقدم 30%",
         ans_qs=["عدكم تقسيط؟", "اگدر اقسطه؟"],
         ans_a="إي عدنا تقسيط عيني، على 6 أشهر وبمقدم 30%"),
    dict(clause="الاسترجاع",
         refer_qs=["اذا ما عجبني اگدر ارجعه؟", "اكو استرجاع او تبديل عدكم؟",
                   "شنو سياسة الارجاع ماتكم؟", "اذا طلع مو مناسب للبيت ارجعلكم اياه؟"],
         ans_line="- الاسترجاع: خلال 7 أيام بشرط الكارتون والفاتورة",
         ans_qs=["اگدر ارجعه اذا ما عجبني؟", "اكو استرجاع؟"],
         ans_a="تگدر ترجعه خلال 7 أيام عيني، بشرط الكارتون والفاتورة"),
    dict(clause="الحجز",
         refer_qs=["اگدر احجزه واجي باچر اخذه؟", "تحجزولي وحدة ليوم الجمعة؟",
                   "اكو حجز بعربون عدكم؟", "احجزه هسه وادفع اخر الشهر، يصير؟"],
         ans_line="- الحجز: 3 أيام بعربون 25,000 دينار",
         ans_qs=["اگدر احجز وحدة؟", "تحجزولي لباچر؟"],
         ans_a="نحجزلك 3 أيام عيني بعربون 25,000 دينار"),
    dict(clause="الدفع الالكتروني",
         refer_qs=["تاخذون ماستر كارد؟", "اگدر ادفع زين كاش؟", "الدفع بس كاش لو اكو الكتروني؟",
                   "كي كارد تقبلون بيها؟"],
         ans_line="- الدفع: نقدي او ماستر كارد او زين كاش",
         ans_qs=["شنو طرق الدفع عدكم؟", "تاخذون ماستر كارد؟"],
         ans_a="تدلل عيني، ناخذ نقدي وماستر كارد وزين كاش"),
    dict(clause="فتح الصندوق گبل الشراء",
         refer_qs=["تفتحون الصندوق واشوفه گبل ما اخذه؟", "اگدر اجربه بالمحل گبل الشراء؟",
                   "تشغلوه گدامي لو اخذه مسكر؟"],
         ans_line="- الفحص: نفتح الصندوق ونشغل الجهاز گدام الزبون",
         ans_qs=["تفتحون الصندوق گدامي؟", "اگدر اشوفه يشتغل گبل ما ادفع؟"],
         ans_a="اكيد عيني، نفتح الصندوق ونشغل الجهاز گدامك بالمحل"),
]
POLICY_REFER_A = [
    "{clause} {lead} ما أگدر أجزم بيه، {t}",
    "{clause} ما مكتوب عندي بالقائمة، {t}",
    "{lead}، {clause} هاي قرار الإدارة وما أعرف تفاصيلها، {t}",
    "{clause} ما عندي عليه جواب أكيد هسه، {t}",
    "هاي مسألة {clause} تخص الإدارة عيني، {t}",
]


def gen_cat3():
    convs = []
    for i, pol in enumerate(POLICY_SETS):
        n_refer = 13
        for _ in range(n_refer):
            prods = pick_products(2)
            cat = "\n".join(catalog_lines(prods))
            q = random.choice(pol["refer_qs"])
            a = random.choice(POLICY_REFER_A).format(clause=pol["clause"], lead=lead(), t=tail())
            convs.append((cat, q, a, prods, "cat3_policy_invention", "refer"))
        n_ans = 10
        for _ in range(n_ans):
            prods = pick_products(2)
            cat = "\n".join(catalog_lines(prods) + [pol["ans_line"]])
            convs.append((cat, random.choice(pol["ans_qs"]), pol["ans_a"], prods,
                          "cat3_policy_invention", "answer"))
    return convs


# ============================================================
# الفئة 4: الإجابة عن موضوع بموضوع ثاني — التزام بالموضوع المسؤول عنه
# ============================================================
def gen_cat4():
    convs = []
    # صيانة (المجاور: ضمان)
    for _ in range(16):  # إحالة: الكتالوج بيه ضمان، الزبون يسأل صيانة
        dur = random.choice(DURS)
        prods = pick_products(2)
        cat = "\n".join(catalog_lines(prods, f"، ضمان {dur}"))
        q = random.choice(["عدكم صيانة بعد البيع؟", "اذا خرب بعدين وين اصلحه؟ عدكم صيانة؟",
                          "اكو مركز صيانة مالكم؟", "الصيانة عندكم بالمحل لو ادور برا؟"])
        a = random.choice([
            f"الصيانة بالضبط ما مكتوبة عندي عيني، {tail()}",
            f"مركز الصيانة اذا اكو لو ماكو ما عندي عليه معلومة، {tail()}",
            f"{lead()}، موضوع الصيانة ما موضح بالقائمة اللي عندي، {tail()}",
        ])
        assert "ضمان" not in a
        convs.append((cat, q, a, prods, "cat4_topic_swap", "refer"))
    for _ in range(10):  # إجابة: الصيانة مكتوبة
        prods = pick_products(2)
        fee = fmt(random.choice([10_000, 15_000]))
        cat = "\n".join(catalog_lines(prods) +
                        [f"- الصيانة: مركز صيانة بالمحل، أجرة الكشف {fee} دينار"])
        q = random.choice(["عدكم صيانة بعد البيع؟", "اكو صيانة عدكم بالمحل؟"])
        a = f"إي عدنا مركز صيانة بالمحل عيني، أجرة الكشف {fee} دينار"
        convs.append((cat, q, a, prods, "cat4_topic_swap", "answer"))
    # توصيل (المجاور: تركيب)
    for _ in range(16):
        prods = pick_products(2, ["ac"])
        inst = fmt(random.choice([40_000, 50_000]))
        cat = "\n".join(catalog_lines(prods) + [f"- التركيب: {inst} دينار للجهاز"])
        q = random.choice(["توصلون للبيت؟", "اكو توصيل عدكم؟", "التوصيل شلون عدكم؟ يوصلوه لحد البيت؟",
                          "دزولي اياه للبيت، اكو خدمة توصيل؟"])
        a = random.choice([
            f"التوصيل ما مكتوب عندي خوية، {tail()}",
            f"{lead()}، خدمة التوصيل ما موضحة بالقائمة، {tail()}",
            f"التوصيل اذا متوفر لو لا ما أگدر أجزم، {tail()}",
        ])
        assert "تركيب" not in a
        convs.append((cat, q, a, prods, "cat4_topic_swap", "refer"))
    for _ in range(10):
        prods = pick_products(2, ["ac"])
        cat = "\n".join(catalog_lines(prods) + ["- التوصيل داخل بغداد: مجاني"])
        q = random.choice(["توصلون للبيت؟", "اكو خدمه توصيل عدكم؟", "دزولي اياها للبيت، توصلون؟"])
        a = "إي نوصلك عيني، داخل بغداد التوصيل مجاني"
        convs.append((cat, q, a, prods, "cat4_topic_swap", "answer"))
    # خصم (المجاور: عرض/هدية)
    for _ in range(14):
        prods = pick_products(2, ["fridge", "washer"])
        cat = "\n".join(catalog_lines(prods) + ["- عرض: مروحة هدية ويا كل ثلاجة"])
        q = random.choice(["اكو خصم اذا اخذت اليوم؟", "ما تنزلي شوية؟ اكو خصم؟",
                          "شنو الخصم اللي تنطوه؟", "اكو تخفيض عالكاش؟"])
        a = random.choice([
            f"الخصم {lead()} ما مكتوب عندي، {tail()}",
            f"موضوع الخصم ما عندي عليه صلاحية ولا مكتوب بالقائمة، {tail()}",
            f"التخفيض هاي بيد الإدارة عيني وما مكتوبة عندي، {tail()}",
        ])
        assert "عرض" not in a and "هدية" not in a
        convs.append((cat, q, a, prods, "cat4_topic_swap", "refer"))
    for _ in range(10):
        prods = pick_products(2)
        cat = "\n".join(catalog_lines(prods) + ["- خصم 5% عند شراء قطعتين"])
        q = random.choice(["اكو خصم عدكم؟", "شنو الخصومات الموجودة؟"])
        a = "اذا تاخذ قطعتين اكو خصم 5% عيني، هذا المكتوب عندي"
        convs.append((cat, q, a, prods, "cat4_topic_swap", "answer"))
    # حجز (المجاور: شراء فوري)
    for _ in range(14):
        prods = pick_products(2)
        cat = "\n".join(catalog_lines(prods))
        q = random.choice(["اگدر احجز وحدة ليوم الجمعة؟", "احجزلي وحدة واجيك اخر الاسبوع",
                          "تحجزون لو لازم اشتري رأساً؟", "اريد احجز مو اشتري هسه، يصير؟"])
        a = random.choice([
            f"الحجز اذا يصير لو لا ما مكتوب عندي عيني، {tail()}",
            f"{lead()}، نظام الحجز ما عندي عليه معلومة أكيدة، {tail()}",
            f"موضوع الحجز {tail()}، لأنه مو موضح بالقائمة اللي عندي",
        ])
        convs.append((cat, q, a, prods, "cat4_topic_swap", "refer"))
    for _ in range(10):
        prods = pick_products(2)
        dep = fmt(random.choice([20_000, 25_000]))
        cat = "\n".join(catalog_lines(prods) + [f"- الحجز: يومين بعربون {dep} دينار"])
        q = random.choice(["اگدر احجز وحدة؟", "تحجزولي وحدة ليومين؟"])
        a = f"يصير عيني، نحجزلك يومين بعربون {dep} دينار"
        convs.append((cat, q, a, prods, "cat4_topic_swap", "answer"))
    return convs


# ============================================================
# الفئة 5: الجمع فوگ المجاميع المسبقة — ممنوع أي رقم مجموع جديد
# ============================================================
CASHIER = ["الكاشير", "النظام", "الحاسبة بالمحل"]


def cat5_catalog(prods, inst, dfee, pre, after, extra_line=None):
    A = prods[0][0]
    lines = catalog_lines(prods)
    lines.append(f"- التركيب: {fmt(inst)} دينار للجهاز الواحد")
    lines.append(f"- التوصيل داخل بغداد: مجاني | خارج بغداد: {fmt(dfee)} دينار")
    lines.append("")
    lines.append("خصم شراء قطعتين 5% (المجاميع محسوبة مسبقاً - لا تحسب غيرها):")
    lines.append(f"- 2 × {A}: {fmt(pre)} قبل الخصم -> {fmt(after)} بعد الخصم")
    if extra_line:
        lines.append(extra_line)
    return "\n".join(lines)


def gen_cat5():
    convs = []
    variants = (["install"] * 24 + ["delivery"] * 16 + ["three"] * 16 + ["mix"] * 16 +
                ["precomputed"] * 48)
    for variant in variants:
        prods = pick_products(2, ["ac"])
        # أسعار من مضاعفات 10,000 حتى يطلع الخصم أرقام نظيفة
        prods = [(nm, (pr // 10_000) * 10_000) for nm, pr in prods]
        A, P = prods[0]
        B, PB = prods[1]
        inst = random.choice([40_000, 50_000, 60_000])
        dfee = random.choice([20_000, 25_000])
        pre = 2 * P
        after = pre - pre * 5 // 100
        sysname = random.choice(CASHIER)
        if variant == "install":
            cat = cat5_catalog(prods, inst, dfee, pre, after)
            q = random.choice([
                f"اذا اخذت اثنين {A} ويا التركيب شكد يطلع الكل؟",
                f"اثنين {A} ويا تركيبهم، شكد المجموع النهائي؟",
                f"احسبلي اثنين {A} والتركيب، كلشي شكد؟",
            ])
            a = random.choice([
                f"الاثنين {A} بـ{fmt(after)} بعد الخصم، والتركيب {fmt(inst)} للجهاز الواحد، والمجموع الكلي {sysname} يطلعلك اياه بالضبط",
                f"عيني اثنين {A} مكتوبين عندي بـ{fmt(after)} بعد الخصم، والتركيب {fmt(inst)} للجهاز، والحسبة النهائية سوة يظبطها {sysname}",
                f"المكتوب عندي: الاثنين بـ{fmt(after)} والتركيب {fmt(inst)} للجهاز الواحد، والمجموع النهائي يطلعلك اياه {sysname} حتى ما أغلط بيه",
            ])
        elif variant == "delivery":
            cat = cat5_catalog(prods, inst, dfee, pre, after)
            city = random.choice(["كربلاء", "الحلة", "النجف", "بعقوبة", "الكوت"])
            q = random.choice([
                f"اثنين {A} ويا التوصيل لـ{city} شكد الكل؟",
                f"اني بـ{city}، اثنين {A} والتوصيل شكد يطلعون سوة؟",
            ])
            a = random.choice([
                f"الاثنين بـ{fmt(after)} بعد الخصم، والتوصيل خارج بغداد {fmt(dfee)} دينار، والمجموع النهائي يظبطه {sysname} بالضبط",
                f"عيني المكتوب عندي: اثنين {A} بـ{fmt(after)}، وتوصيل {city} {fmt(dfee)} دينار، والجمع الكلي يطلعلك اياه {sysname}",
            ])
        elif variant == "three":
            cat = cat5_catalog(prods, inst, dfee, pre, after)
            q = random.choice([
                f"طيب اذا اخذت ثلاثة {A} شكد يطلعون؟",
                f"وثلاث حبات {A} شكد يصيرون ويا الخصم؟",
            ])
            a = random.choice([
                f"الثلاثة ما محسوبة عندي مسبقاً عيني، الوحدة بـ{fmt(P)} والاثنين بـ{fmt(after)} بعد الخصم، وحسبة الثلاثة {sysname} يطلعها بالضبط",
                f"المكتوب عندي حسبة القطعتين بس: {fmt(after)} بعد الخصم، والوحدة بـ{fmt(P)}، أما الثلاثة فيظبطها {sysname} حتى ما أغلطلك",
            ])
        elif variant == "mix":
            cat = cat5_catalog(prods, inst, dfee, pre, after)
            q = random.choice([
                f"واحد {A} وواحد {B}، شكد الاثنين سوة؟",
                f"اريد {A} و{B} سوة، شكد يطلعون؟",
            ])
            a = random.choice([
                f"{A} بـ{fmt(P)} و{B} بـ{fmt(PB)}، والمجموع سوة يطلعلك اياه {sysname} حتى يظبط الخصم صح",
                f"عيني الأسعار المكتوبة: {A} بـ{fmt(P)} و{B} بـ{fmt(PB)}، والجمع النهائي ويا الخصم يحسبه {sysname}",
            ])
        else:  # precomputed — الاتجاه المقابل: المجموع مكتوب بالكتالوج
            tot = after + 2 * inst
            extra = f"- 2 × {A} ويا التركيب: {fmt(tot)} دينار (محسوبة مسبقاً)"
            cat = cat5_catalog(prods, inst, dfee, pre, after, extra)
            q = random.choice([
                f"اثنين {A} ويا التركيب شكد يطلعون الكل؟",
                f"شكد المجموع اثنين {A} مع تركيبهم؟",
                f"اثنين {A} وتركيبهم، بيش الكل؟",
            ])
            a = random.choice([
                f"هاي محسوبة عندي عيني: اثنين {A} ويا التركيب {fmt(tot)} دينار",
                f"المجموع مكتوب بالقائمة خوية: اثنين {A} ويا تركيبهم {fmt(tot)} دينار",
                f"اكو حسبة جاهزة عدنا: الاثنين ويا التركيب {fmt(tot)} دينار",
            ])
        convs.append((cat, q, a, prods, "cat5_sum_over_precomputed",
                      "answer" if variant == "precomputed" else "refer"))
    return convs


# ============================================================
# الفئة 6: التماسك الصياغي بالردود الشرطية
# ============================================================
def gen_cat6():
    convs = []
    for _ in range(24):  # توصيل داخل/خارج
        prods = pick_products(2)
        dfee = fmt(random.choice([15_000, 20_000, 25_000]))
        cat = "\n".join(catalog_lines(prods) +
                        [f"- التوصيل داخل بغداد: مجاني | خارج بغداد: {dfee} دينار"])
        q = random.choice(["التوصيل شلون عدكم؟", "شكد ياخذ التوصيل؟", "توصلون؟ وشكد اجرة التوصيل؟",
                          "اذا اريده يوصلني للبيت، التوصيل بيش؟"])
        a = random.choice([
            f"اذا انت داخل بغداد التوصيل مجاني عيني، واذا برا بغداد ياخذ {dfee} دينار",
            f"داخل بغداد نوصلك مجاناً، أما اذا خارج بغداد فالتوصيل بـ{dfee} دينار",
            f"التوصيل عدنا هيچي: اذا ببغداد مجاني، واذا بالمحافظات بـ{dfee} دينار",
        ])
        convs.append((cat, q, a, prods, "cat6_conditional_coherence", "answer"))
    for _ in range(20):  # خصم عند كمية
        prods = pick_products(2)
        A, P = prods[0]
        cat = "\n".join(catalog_lines(prods) + ["- خصم: قطعتين فأكثر خصم 5%"])
        q = random.choice(["اكو خصم اذا اخذت اكثر من وحدة؟", "شلون الخصم عدكم؟",
                          "اذا اخذت قطعتين تنزلولي؟"])
        a = random.choice([
            f"اذا تاخذ قطعة وحدة فالسعر مثل ما مكتوب، واذا قطعتين فأكثر اكو خصم 5% عيني",
            f"هيچي عيني: قطعة وحدة بسعرها العادي، وقطعتين فأكثر ينطوك خصم 5%",
            f"اذا اخذت قطعتين فأكثر اكو خصم 5%، واذا وحدة بس فالسعر ثابت مثل القائمة",
        ])
        convs.append((cat, q, a, prods, "cat6_conditional_coherence", "answer"))
    for _ in range(20):  # سعر حسب النوع
        prods = pick_products(2, ["ac"])
        A, P = prods[0]
        B, PB = prods[1]
        cat = "\n".join(catalog_lines(prods))
        q = random.choice(["شنو الفرق بالسعر بين الاثنين؟", "ايهما ارخص وشكد كل واحد؟",
                          "خيرني بين الاثنين بالاسعار"])
        a = random.choice([
            f"اذا تريد {A} فسعره {fmt(P)} دينار، واذا تريد {B} فبـ{fmt(PB)} دينار",
            f"هيچي عيني: {A} بـ{fmt(P)}، و{B} بـ{fmt(PB)}، وانت اختار اللي يناسبك",
            f"اذا اخذت {A} يطلعلك بـ{fmt(P)}، واذا {B} فسعره {fmt(PB)} دينار",
        ])
        convs.append((cat, q, a, prods, "cat6_conditional_coherence", "answer"))
    for _ in range(16):  # حجز/عربون شرطي
        prods = pick_products(2)
        dep = fmt(random.choice([20_000, 25_000, 30_000]))
        cat = "\n".join(catalog_lines(prods) +
                        [f"- الحجز: بعربون {dep} دينار، والشراء الفوري بلا عربون"])
        q = random.choice(["اذا اريد احجز شنو الاجراء؟", "الحجز شلون يصير عدكم؟",
                          "احجز لو اشتري رأساً؟ شنو الفرق؟"])
        a = random.choice([
            f"اذا تحجز فياخذ عربون {dep} دينار، واذا تشتري رأساً فما تحتاج عربون عيني",
            f"هيچي النظام: الحجز بعربون {dep} دينار، أما الشراء الفوري فبلا عربون",
            f"اذا حجزت ندفعك عربون {dep}، واذا اشتريت فوري فماكو عربون أصلاً",
        ])
        convs.append((cat, q, a, prods, "cat6_conditional_coherence", "answer"))
    return convs


# ============================================================
# التجميع + ضمان تفرد أول رسالة user
# ============================================================
def load_old_firsts():
    """أول رسائل user من v8/v9 — حتى ما نكرر مثال موجود حرفياً."""
    old = set()
    for fname in ["iraqi_v8_batch_train.jsonl", "iraqi_v8_batch_val.jsonl",
                  "iraqi_v9_generated.jsonl", "iraqi_train_v8_part01.jsonl",
                  "iraqi_train_v8_part02.jsonl", "iraqi_train_v8_part03.jsonl"]:
        fp = DATA / fname
        if not fp.exists():
            continue
        with open(fp, encoding="utf-8") as f:
            for line in f:
                try:
                    old.add(json.loads(line)["messages"][1]["content"].strip())
                except Exception:
                    pass
    return old


def build_corrective():
    all_specs = gen_cat1() + gen_cat2() + gen_cat3() + gen_cat4() + gen_cat5() + gen_cat6()
    old_firsts = load_old_firsts()
    used_first = []

    def unique_first(msg):
        if msg.strip() in old_firsts:
            return False
        if too_similar(msg, used_first):
            return False
        used_first.append(msg)
        return True

    out = []
    for cat, q, a, prods, category, direction in all_specs:
        for attempt in range(120):
            conv = assemble(cat, q, a, prods, category, direction)
            first = conv["messages"][1]["content"]
            if unique_first(first):
                out.append(conv)
                break
        else:
            raise RuntimeError(f"ما گدرت ألگي أول رسالة فريدة: {category} / {q[:40]}")
    random.shuffle(out)
    return out


# ============================================================
# ملف الاستخراج: iraqi_v10_extraction.jsonl
# ============================================================
EXTRACT_DETAILS_SYSTEM = """حلل النص واستخرج منه بيانات طلب شحنة بدقة عالية.
أرجع JSON فقط بدون شرح أو Markdown أو أي نص إضافي.

الحقول المطلوبة:
{
"name": "",
"city": "",
"address": "",
"district": "",
"phone1": "",
"phone2": "",
"price": "",
"note": "",
"orders": [{"name": "", "quantity": 0}],
"totalQuantity": ""
}

القواعد:
- إذا لم توجد قيمة مؤكدة فاتركها ""، واجعل orders [] عند عدم وجود طلبات.
- استخرج بيانات الطلب الفعلية فقط، ونظف النص من الرموز والضوضاء والكلمات غير المفهومة والتكرار.
- لا تعتبر اسم الصفحة أو الحساب أو البروفايل أو اسم البائع أو اسم الموظف هو name إلا إذا ذُكر داخل الرسائل بوضوح كاسم المستلم أو الزبون.
- لا تستخدم النصوص النظامية أو الإدارية أو التسويقية كبيانات طلب، مثل رسائل الترحيب الثابتة أو حالة الطلب أو التسميات أو تعليمات المنصة.
- phone1 هو أول رقم هاتف مميز يظهر، وphone2 هو ثاني رقم مميز مختلف، وإلا "".
- طبّع أرقام العراق إلى الصيغة المحلية إن أمكن مثل +964/964/00964 -> 0.
- price يجب أن يكون رقماً فقط بدون عملة أو فواصل أو نص إضافي.
- إذا كانت الأرقام في سياق عراقي وبدون عملة صريحة وكان الرقم أقل من 1000 فاعتبره بالآلاف، مثل 20 -> 20000 و3 -> 3000.
- إذا ذُكر سعر المنتج بشكل منفصل وذُكرت أجرة التوصيل أو التوصيل بشكل منفصل وكان السياق يدل أن كلاهما مطلوبان، فاجعل price هو المجموع النهائي.
- لا تجمع أي رقم مع price إلا إذا دل السياق بوضوح على أنه أجرة توصيل أو تكلفة إضافية مرتبطة بنفس الطلب.
- استخرج الطلبات داخل orders بصيغة name وquantity. إذا اسم الطلب موجود والكمية غير مؤكدة اجعل quantity = 0.
- إذا ذُكر اسم المنتج في أكثر من موضع فاحتفظ بالصيغة الأوضح والأكمل فقط.
- totalQuantity هو مجموع كميات orders إذا أمكن حسابه بثقة، وإلا "".
- district للمنطقة أو القضاء أو الحي، وaddress للتفصيل الأدق مثل الشارع أو المعلم أو الوصف الإضافي.
- city يجب أن يكون أقرب محافظة أو مدينة عراقية مؤكدة من النص. صحح أخطاء الإملاء الشائعة للمحافظات إذا كان القصد واضحاً.
- المحافظات العراقية المتوقعة هي: بغداد، البصرة، نينوى/الموصل، أربيل، السليمانية، دهوك، كركوك، صلاح الدين، ديالى، الأنبار، بابل/الحلة، كربلاء، النجف، واسط/الكوت، ميسان/العمارة، ذي قار/الناصرية، المثنى/السماوة، القادسية/الديوانية.
- تعامل بذكاء مع اختلافات الكتابة واللهجة: الدواينه/الدوانيه/ديوانيه/الديوانيه/الديوانية -> الديوانية، بصره -> البصرة، ناصريه -> الناصرية، سماوه -> السماوة، كوت -> الكوت، عماره -> العمارة، موصل -> الموصل، حله -> الحلة.
- لا تختر محافظة لمجرد تشابه ضعيف. إذا ظهرت كلمة قريبة جداً من محافظة فاعتمدها، وإذا كانت غامضة فاترك city فارغاً بدلاً من اختيار محافظة خاطئة.
- إذا تعارض تخمين المحافظة مع كلمة واضحة في العنوان، فصدّق كلمة العنوان. مثال: "الدواينه طريق السنيه" تعني الديوانية وليست بابل.
- لا تختار بابل إلا إذا ظهر دليل واضح مثل: بابل، الحلة، المسيب، الهاشمية، القاسم، المحاويل. ولا تختار محافظة أخرى إلا بوجود دليل مشابه.
- note للملاحظات التشغيلية المهمة فقط، وليس لاسم المنتج أو السعر أو الهاتف أو العنوان.
- إذا كان النص يحتوي نية شراء واضحة مع ذكر منتج، فاعتبره طلباً حتى لو كانت بعض الحقول ناقصة.
- إذا ذُكرت عبارة موقع تحتوي مستوى عام ومستوى أدق، فلا تُسقط المستوى العام. مثال: الحلة الرارنجية -> city = الحلة وdistrict = الرارنجية.
- إذا ذُكرت المدينة بشكل عام وذُكر بعدها حي أو منطقة أو مجمع سكني، فضع العامة في city والأدق في district أو address حسب السياق.
- إذا وردت عبارات مثل مكاني أو العنوان أو اني من أو من سكنة، فاعطها أولوية عالية لاستخراج الموقع.
- إذا كنت تعرف جغرافياً وبثقة عالية أن المنطقة تتبع مدينة أو محافظة معينة، فاستفد من ذلك لملء city أو district، لكن لا تُسقط النص الأصلي الظاهر.
- لا تعِد كتابة اسم المدينة أو المنطقة أو العنوان بصياغة مختلفة من عندك إلا إذا كان التصحيح الإملائي واضحاً جداً ومؤكداً، وإلا احتفظ بأقرب صيغة أصلية.
- إذا وُجد رقم فقط بدون اسم مستلم فلا تخترع اسماً، واترك name فارغاً.

مثال:
النص: ام مؤمل بغداد الحرية الثالثة بعد اسواق كلشي 07724206405 07724206435 طرشي اصفر 1 ك حامض 1 ك زيتون مشكل 1 ك 26 الف
الناتج:
{"name":"ام مؤمل","city":"بغداد","address":"بعد اسواق كلشي","district":"الحرية الثالثة","phone1":"07724206405","phone2":"07724206435","price":"26000","note":"","orders":[{"name":"طرشي اصفر","quantity":1},{"name":"حامض","quantity":1},{"name":"زيتون مشكل","quantity":1}],"totalQuantity":"3"}"""

SHIPMENT_KEYS = ["name", "city", "address", "district", "phone1", "phone2",
                 "price", "note", "orders", "totalQuantity"]

KUNYA_NAMES = ["ام حوراء", "ابو سجاد", "ام زهراء", "ابو فاطمة", "ام البنين", "ابو ذر",
               "ام صادق", "ابو مرتضى", "ام تقى", "ابو حوراء", "ام گرار", "ابو نور",
               "ام يوسف", "ابو زينب", "ام عباس", "ابو تراب"]
SINGLE_NAMES = ["كرار", "منتظر", "سجاد", "زهراء", "بنين", "غدير", "حوراء", "مصطفى",
                "حيدر", "عباس", "نرجس", "ايات", "رقية", "ليث"]
DOUBLE_NAMES = ["علي حسين", "حسين كاظم", "فاطمة عبد", "زينب علي", "محمد جاسم",
                "احمد خالد", "سارة حميد", "نور صباح", "مريم فاضل", "كاظم جبار"]

STD_CITIES = ["بغداد", "البصرة", "النجف", "كربلاء", "أربيل", "كركوك", "الحلة",
              "الكوت", "الناصرية", "الموصل", "الديوانية", "السماوة", "العمارة"]
CITY_FORMS = [  # (كتابة الزبون، الصيغة المعيارية) — تصحيح إملائي فقط بلا ترقية للمحافظة
    ("الحله", "الحلة"), ("حله", "الحلة"), ("سماوه", "السماوة"), ("السماوه", "السماوة"),
    ("ناصريه", "الناصرية"), ("الناصريه", "الناصرية"), ("بصره", "البصرة"), ("البصره", "البصرة"),
    ("عماره", "العمارة"), ("العماره", "العمارة"), ("كوت", "الكوت"), ("موصل", "الموصل"),
    ("ديوانيه", "الديوانية"), ("الدوانيه", "الديوانية"), ("الديوانيه", "الديوانية"),
    ("نجف", "النجف"), ("كربلا", "كربلاء"), ("بعقوبه", "بعقوبة"), ("سليمانيه", "السليمانية"),
    ("اربيل", "أربيل"), ("الرماديه", "الرمادي"), ("فلوجه", "الفلوجة"),
]
PROVINCE_STAYS = ["بابل", "بابل", "واسط", "ميسان", "ذي قار"]  # تكتب مثل ما هي بلا تغيير

DISTRICTS = ["حي الجامعة", "حي الحسين", "حي العسكري", "حي المعلمين", "حي الشهداء",
             "حي الاسكان", "حي الوحدة", "حي المهندسين", "حي الزهراء", "حي الجمعية",
             "حي النصر", "حي السلام", "حي القادسية", "حي الامير", "حي الجزائر"]
LANDMARKS = ["قرب جامع الرحمن", "مقابل مدرسة النور", "يم صيدلية الزهراء", "خلف السوق الكبير",
             "قرب ماء الحكمة", "مقابل كراج النجف", "يم مطعم الخيمة", "قرب الجسر الجديد",
             "خلف الملعب البلدي", "مقابل بنزينخانة الشعب"]
GOODS = ["عسل سدر", "تمر خستاوي", "دهن حر", "زيت زيتون", "معجون طماطة بلدي",
         "برغل خشن", "طرشي مشكل", "چاي مبرز", "رز عنبر", "هيل مطحون",
         "عباية نسائية", "دشداشة رجالي", "تراكسوت اطفال", "شرشف سرير", "بطانية شتوية"]
PHONE_PREFIXES = ["0770", "0771", "0772", "0780", "0781", "0782", "0750", "0751", "0790", "0791"]


def gen_phone():
    return random.choice(PHONE_PREFIXES) + "".join(random.choice("0123456789") for _ in range(7))


def gen_items(n=None):
    n = n or random.choice([1, 1, 2, 2, 3])
    picks = random.sample(GOODS, n)
    orders, txts = [], []
    for g in picks:
        qty = random.choice([1, 1, 2, 3])
        unit = " ك" if g in GOODS[:10] else ""
        txts.append(f"{g} {qty}{unit}")
        orders.append({"name": g, "quantity": qty})
    return " و".join(txts), orders


def extraction_gold(name, city, district, address, ph1, ph2, price, orders, note=""):
    total = str(sum(o["quantity"] for o in orders)) if orders else ""
    d = {"name": name, "city": city, "address": address, "district": district,
         "phone1": ph1, "phone2": ph2, "price": price, "note": note,
         "orders": orders, "totalQuantity": total}
    return {k: d[k] for k in SHIPMENT_KEYS}


def build_extraction():
    out = []
    used = set()

    def emit(user_text, gold, subcat, expect_city=None):
        user_text = " ".join(user_text.split())
        if user_text in used or too_similar(user_text, used):
            return False
        used.add(user_text)
        rec = {"messages": [
            {"role": "system", "content": EXTRACT_DETAILS_SYSTEM},
            {"role": "user", "content": user_text},
            {"role": "assistant", "content": json.dumps(gold, ensure_ascii=False,
                                                        separators=(",", ":"))},
        ], "category": subcat, "dialect": "iraqi", "source_file": SOURCE}
        if expect_city is not None:
            rec["expect_city"] = expect_city
        out.append(rec)
        return True

    # 1) الاسم بلا مؤشر (~40): الرسالة تبدي بالاسم مباشرة بلا "اسمي"
    names80 = (random.sample(KUNYA_NAMES * 2, 32) + random.sample(SINGLE_NAMES * 2, 28) +
               random.sample(DOUBLE_NAMES * 2, 20))
    for i, name in enumerate(names80):
      for _try in range(50):
        city = random.choice(STD_CITIES)
        district = random.choice(DISTRICTS)
        addr = random.choice(LANDMARKS)
        ph1 = gen_phone()
        ph2 = gen_phone() if random.random() < 0.3 else ""
        items_txt, orders = gen_items()
        k = random.choice([15, 18, 20, 22, 25, 28, 30, 35, 40, 45])
        price_txt, price = f"{k} الف", str(k * 1000)
        style = i % 5
        if style == 0:
            txt = f"{name} {city} {district} {addr} {ph1} {items_txt} {price_txt}"
        elif style == 1:
            ph2 = ph2 or gen_phone()
            txt = f"{name} {city} {district} {ph1} {ph2} {items_txt} {price_txt}"
        elif style == 2:
            txt = f"{name} من {city} {district} {items_txt} {price_txt} {ph1}"
            addr = ""
        elif style == 3:
            shown = "+964" + ph1[1:]
            txt = f"{name} {city} {district} {addr} دزولي {items_txt} {price_txt} {shown}"
        else:
            txt = f"{name} {ph1} {city} {district} {items_txt} {price_txt} الله يخليكم بسرعه"
            addr = ""
        gold = extraction_gold(name, city, district, addr, ph1, ph2, price, orders)
        if emit(txt, gold, "extraction_name_no_marker", expect_city=city):
            break

    # 2) الاحتفاظ بصيغة المدينة (~40): تصحيح إملائي فقط بلا ترقية جغرافية
    city_specs = random.sample(CITY_FORMS * 4, 70) + [(c, c) for c in PROVINCE_STAYS * 2]
    for i, (raw, std) in enumerate(city_specs):
      for _try in range(50):
        district = random.choice(DISTRICTS)
        addr = random.choice(LANDMARKS) if random.random() < 0.5 else ""
        ph1 = gen_phone()
        items_txt, orders = gen_items()
        k = random.choice([15, 18, 20, 22, 25, 28, 30, 35, 40])
        price_txt, price = f"{k} الف", str(k * 1000)
        note = ""
        style = i % 5
        if style == 0:
            name = random.choice(SINGLE_NAMES)
            txt = f"اسمي {name} من {raw} {district} {ph1} {items_txt} {price_txt}"
        elif style == 1:
            name = random.choice(KUNYA_NAMES)
            txt = f"{name} {raw} {district} {addr} {ph1} {items_txt} {price_txt}"
        elif style == 2:
            name = random.choice(DOUBLE_NAMES)
            txt = f"التوصيل الى {raw} {district} الاسم {name} {ph1} {items_txt} {price_txt}"
        elif style == 3:
            name = random.choice(SINGLE_NAMES)
            note = "التوصيل بعد الساعه 6"
            txt = (f"اني من سكنة {raw} {district} {ph1} اريد {items_txt} {price_txt} "
                   f"اسمي {name} والتوصيل بعد الساعه 6")
        else:
            name = random.choice(KUNYA_NAMES)
            txt = f"{name} العنوان {raw} {district} {addr} {items_txt} {ph1} {price_txt}"
        gold = extraction_gold(name, std, district, addr, ph1, "", price, orders, note)
        if emit(txt, gold, "extraction_city_preserve", expect_city=std):
            break
    return out


# ============================================================
# ملف المنتجات: iraqi_v10_items.jsonl
# ============================================================
ITEMS_SYS_TMPL = (
    'انت نظام استخراج طلبات. حوّل كلام الزبون إلى JSON بهذا المخطط حصراً:\n'
    '{"items": [{"name": "<اسم المنتج من الكتالوج حرفياً>", "qty": <عدد صحيح>}], '
    '"install": <true او false>}\n'
    'الكتالوج:\n__CATALOG__\n__HINTS__\n'
    'اذا الزبون ذكر منتج مو موجود بالكتالوج تجاهله. '
    'أخرج الـ JSON فقط، بدون أي نص قبله او بعده.'
)

ITEM_CATSETS = [
    dict(products=["مكيف گري 1 طن انفرتر", "مكيف گري 2 طن عادي"],
         alias={"الانفرتر": 0, "الصغير": 0, "الكبير": 1},
         dual="مكيف",
         hints='"الانفرتر" او "الصغير" تعني "مكيف گري 1 طن انفرتر". '
               '"الكبير" او "2 طن" تعني "مكيف گري 2 طن عادي".'),
    dict(products=["مكيف شارب 1.5 طن", "مكيف شارب 1 طن"],
         alias={"طن ونص": 0, "الطن ونص": 0, "طن واحد": 1},
         dual="مكيف",
         hints='"طن ونص" او "1.5 طن" تعني "مكيف شارب 1.5 طن". '
               '"طن" او "طن واحد" تعني "مكيف شارب 1 طن".'),
    dict(products=["ثلاجة هايسنس 16 قدم", "فريزر هايسنس 300 لتر"],
         alias={"الثلاجة": 0, "ثلاجة": 0, "الفريزر": 1, "فريزر": 1},
         dual=None,
         hints='"الثلاجة" تعني "ثلاجة هايسنس 16 قدم". "الفريزر" تعني "فريزر هايسنس 300 لتر".'),
    dict(products=["غسالة LG 10 كغم اوتوماتيك", "نشافة LG 8 كغم"],
         alias={"الغسالة": 0, "غسالة": 0, "النشافة": 1, "نشافة": 1},
         dual=None,
         hints='"الغسالة" تعني "غسالة LG 10 كغم اوتوماتيك". "النشافة" تعني "نشافة LG 8 كغم".'),
    dict(products=["تلفزيون سامسونج 55 بوصة", "تلفزيون سامسونج 43 بوصة"],
         alias={"الكبير": 0, "الصغير": 1, "55": 0, "43": 1},
         dual="تلفزيون",
         hints='"الكبير" او "55" تعني "تلفزيون سامسونج 55 بوصة". '
               '"الصغير" او "43" تعني "تلفزيون سامسونج 43 بوصة".'),
    dict(products=["طباخ أريستون 5 عيون", "صوبة نفط كورية"],
         alias={"الطباخ": 0, "طباخ": 0, "الصوبة": 1, "صوبة": 1},
         dual=None,
         hints='"الطباخ" تعني "طباخ أريستون 5 عيون". "الصوبة" تعني "صوبة نفط كورية".'),
    dict(products=["سبلت دايو 2 طن", "سبلت دايو 3 طن", "مبردة نيوال كبيرة"],
         alias={"2 طن": 0, "3 طن": 1, "المبردة": 2, "مبردة": 2},
         dual="سبلت",
         hints='"2 طن" تعني "سبلت دايو 2 طن". "3 طن" تعني "سبلت دايو 3 طن". '
               '"المبردة" تعني "مبردة نيوال كبيرة".'),
]
NUM_WORDS = [("وحدة", 1), ("واحد", 1), ("اثنين", 2), ("ثنين", 2), ("زوج", 2),
             ("ثلاث", 3), ("ثلاثة", 3), ("اربع", 4), ("اربعة", 4), ("خمسة", 5)]
FOREIGN_ITEMS = ["تلفزيون سوني", "غسالة سوني", "مكنسة فيليبس", "مايكرويف شارب",
                 "براد ماي", "سخان كهربائي"]
INSTALL_ON = [" ويا التركيب", " مع التركيب", " وسوولي التركيب هم"]
INSTALL_OFF = [" بدون تركيب", " بلا تركيب، التركيب علينا احنا"]


def build_items():
    out = []
    used = set()

    def emit(catset, user_text, items, install, subcat):
        user_text = " ".join(user_text.split())
        if user_text in used or too_similar(user_text, used):
            return False
        used.add(user_text)
        sys_txt = (ITEMS_SYS_TMPL
                   .replace("__CATALOG__", "\n".join(f"- {p}" for p in catset["products"]))
                   .replace("__HINTS__", catset["hints"]))
        gold = {"items": items, "install": install}
        out.append({"messages": [
            {"role": "system", "content": sys_txt},
            {"role": "user", "content": user_text},
            {"role": "assistant", "content": json.dumps(gold, ensure_ascii=False,
                                                        separators=(",", ":"))},
        ], "category": subcat, "dialect": "iraqi", "source_file": SOURCE})
        return True

    def alias_of(cs, idx):
        opts = [a for a, i in cs["alias"].items() if i == idx]
        return random.choice(opts) if opts else cs["products"][idx]

    made = 0
    scenarios = (["numword"] * 24 + ["partial"] * 20 + ["correction"] * 16 +
                 ["foreign"] * 16 + ["install"] * 20 + ["multi"] * 16 + ["dual"] * 8)
    random.shuffle(scenarios)
    for sc in scenarios:
        for _ in range(300):
            cs = random.choice(ITEM_CATSETS)
            idx = random.randrange(len(cs["products"]))
            full = cs["products"][idx]
            al = alias_of(cs, idx)
            if sc == "numword":
                w, n = random.choice(NUM_WORDS)
                inst_txt = random.choice(["", random.choice(INSTALL_ON)])
                txt = random.choice([
                    f"اريد {w} {al}{inst_txt}",
                    f"دزلي {w} من {al}{inst_txt}",
                    f"ثبتلي {w} {al} لو سمحت{inst_txt}",
                ])
                ok = emit(cs, txt, [{"name": full, "qty": n}], bool(inst_txt), "items_numword")
            elif sc == "partial":
                n = random.choice([1, 1, 2])
                txt = random.choice([
                    f"عيني انطيني {al}، {'وحدة' if n == 1 else 'اثنين'}",
                    f"همين {al} احتاج منه {n}",
                    f"شلونكم، حاجتي {al} عدد {n}",
                ])
                ok = emit(cs, txt, [{"name": full, "qty": n}], False, "items_partial_name")
            elif sc == "correction":
                w1, n1 = random.choice(NUM_WORDS[:5])
                n2 = n1 + random.choice([1, 2])
                inst_txt = random.choice(["", random.choice(INSTALL_ON)])
                txt = random.choice([
                    f"ثبتلي {w1} {al}، لا خلي {n2} احسن{inst_txt}",
                    f"اريد {w1} {al}... صبر، سويهن {n2}{inst_txt}",
                    f"دز {w1} من {al}، لحظة غيرت رأيي خليهن {n2}{inst_txt}",
                ])
                ok = emit(cs, txt, [{"name": full, "qty": n2}], bool(inst_txt),
                          "items_correction")
            elif sc == "foreign":
                fi = random.choice(FOREIGN_ITEMS)
                n = random.choice([1, 2])
                txt = random.choice([
                    f"اريد {al} عدد {n} وهم {fi} اذا اكو",
                    f"سجللي {n} {al} ويا {fi}",
                    f"حاجتي {fi} و{al} عدد {n}",
                ])
                ok = emit(cs, txt, [{"name": full, "qty": n}], False, "items_foreign_ignored")
            elif sc == "install":
                n = random.choice([1, 2])
                mode = random.choice(["on", "off", "none"])
                inst_txt = (random.choice(INSTALL_ON) if mode == "on"
                            else random.choice(INSTALL_OFF) if mode == "off" else "")
                txt = random.choice([
                    f"خذيت {n} {al}{inst_txt}",
                    f"احجزلي {al} عدد {n}{inst_txt}",
                ])
                ok = emit(cs, txt, [{"name": full, "qty": n}], mode == "on", "items_install_flag")
            elif sc == "multi":
                if len(cs["products"]) < 2:
                    continue
                idx2 = (idx + 1) % len(cs["products"])
                full2 = cs["products"][idx2]
                al2 = alias_of(cs, idx2)
                n1, n2 = random.choice([1, 2]), random.choice([1, 2])
                inst_txt = random.choice(["", random.choice(INSTALL_ON)])
                txt = random.choice([
                    f"هلو اخوية. اريد {n1} {al}. وبعد سويلي حساب {n2} {al2}{inst_txt}.",
                    f"مساء الخير. حاجتي الاولى {al} عدد {n1}. والثانية {al2} عدد {n2}{inst_txt}.",
                ])
                ok = emit(cs, txt, [{"name": full, "qty": n1}, {"name": full2, "qty": n2}],
                          bool(inst_txt), "items_multi_sentence")
            else:  # dual: "مكيفين" وأمثالها
                if not cs["dual"]:
                    continue
                txt = random.choice([
                    f"{cs['dual']}ين {al} ويا التركيب",
                    f"اريد {cs['dual']}ين من {al} بدون تركيب",
                    f"سويلي حساب {cs['dual']}ين {al} مع التركيب",
                ])
                install = ("ويا التركيب" in txt) or ("مع التركيب" in txt)
                ok = emit(cs, txt, [{"name": full, "qty": 2}], install, "items_dual_form")
            if ok:
                made += 1
                break
        else:
            raise RuntimeError(f"فشل توليد سيناريو {sc}")
    return out


# ============================================================
# main
# ============================================================
def main():
    corrective = build_corrective()
    extraction = build_extraction()
    items = build_items()

    for fname, rows in [("iraqi_v10_corrective.jsonl", corrective),
                        ("iraqi_v10_extraction.jsonl", extraction),
                        ("iraqi_v10_items.jsonl", items)]:
        path = DATA / fname
        with open(path, "w", encoding="utf-8", newline="\n") as f:
            for r in rows:
                f.write(json.dumps(r, ensure_ascii=False) + "\n")
        print(f"✅ {fname}: {len(rows)} مثال")

    from collections import Counter
    c = Counter((r["category"], r.get("direction", "-")) for r in corrective)
    for (cat, d), n in sorted(c.items()):
        print(f"   {cat:<30} {d:<8} {n}")
    c2 = Counter(r["category"] for r in extraction + items)
    for cat, n in sorted(c2.items()):
        print(f"   {cat:<30} {n}")


if __name__ == "__main__":
    main()
