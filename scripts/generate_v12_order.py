# -*- coding: utf-8 -*-
"""
توليد داتا v12 — الفجوات الثلاث المتبقية بعد v11 (250 مثال).

الأساس القياسي (مقيس فعلياً على الداتا قبل الكتابة، مو مقدّر):
  - [ORDER_READY]  : صفر مثال بكل ملفات data/ (~530 ألف سطر). العلامة
                     **ما انتدربت أبداً** — مو «الموديل ينساها».
  - نتيجة أداة فارغة: صفر مثال من 12,000 محادثة أداة.
  - وسيط status    : صفر. وسيط all: صفر. (كلها order_id/phone حصراً)
  - الحالات الخمس المعروفة بنتائج الأداة: تم التسليم، جاهز للاستلام،
    بالطريق، مؤجل، قيد التجهيز.

التوزيع المستهدف:
  ord1_marker_positive     40   العلامة تنكتب — بعد اكتمال الحقول وتأكيد صريح
  ord2_marker_withheld     55   **سالبة**: تأكيد أو شبه تأكيد بلا اكتمال → بلا علامة
  ord3_confirm_gate        30   ملخّص + سؤال تأكيد، والعلامة **ما تنكتب** بنفس الرد
  ord4_submit_refusal      45   «ثبتلي» صراحة وحقل ناقص → رفض التثبيت وسؤال الحقل
  ord5_tool_empty          40   نتيجة أداة فارغة → نفي صريح، صفر اختراع
  ord6_tool_status_args    40   استعلام بالحالة/الجرد → status/all + صياغة قائمة

═══════════════════════════════════════════════════════════════
المبدأ الحاكم — العلامة سلوك مشروط، مو زينة نهاية رد:
═══════════════════════════════════════════════════════════════
الخطر الأكبر بتدريب علامة من الصفر هو أن يتعلمها الموديل كـ«زينة ختام»
فيكتبها بأي رد ودّي. لذلك السالب هنا **أكثر من الموجب عمداً**
(55+30+45 = 130 بلا علامة  مقابل  40 بيها = نسبة 3.25:1).

الشرط المُعلَّم بدقة — العلامة تنكتب إذا وفقط إذا اجتمع الثلاثة:
    (1) الحقول الأربعة كلها موجودة **بكلام الزبون** حرفياً
    (2) البائع لخّص وسأل تأكيد
    (3) الزبون أكد تأكيداً صريحاً لا لبس فيه

ينكسر أي شرط → صفر علامة. وأخطر حالة مغطاة بـ ord2: كلام **يشبه**
التأكيد وهو مو تأكيد («اكيد هذا غالي!»، «نعم بس خلي أفكر») — لأن
«نعم/اكيد» لحالها لو ارتبطت بالعلامة بالتدريب، تصير مفتاحاً لفظياً
يفتح طلباً ناقصاً.

قاعدة العنوان (سبب وجود ord4 أصلاً): البائع ما يملأ حقلاً ما گاله
الزبون. ولا مثال هنا يذكر محافظة أو منطقة أو اسماً ما جاء برسالة
الزبون حرفياً — والفحص الذاتي يرفض الملف إذا صار.

الإخراج: data/iraqi_v12_order.jsonl
"""
import difflib
import json
import random
import re
import sys
from collections import Counter
from pathlib import Path

sys.stdout.reconfigure(encoding="utf-8")
random.seed(20260727)
DATA = Path(__file__).resolve().parent.parent / "data"
SOURCE = "generate_v12_order.py"

fmt = lambda n: f"{n:,}"
MARKER = "[ORDER_READY]"

# ============================================================
# قوالب الـ system — تمتد من v11 بإضافة عقد العلامة صراحةً
# ============================================================
ORDER_SYSTEM_TMPL = (
    "أنت موظف مبيعات بمحل عراقي.\n\nالموجود حالياً:\n{items}\n\n"
    "انسخ الأسعار والأسماء حرفياً من القائمة. إذا وافق الزبون على الشراء، اجمع "
    "منه هذي الحقول وحدة وحدة: الاسم، رقم الهاتف، المحافظة، العنوان بالتفصيل. "
    "اسأل عن الناقص بس — لا تعيد سؤال حقل انطاك اياه، ولا تخترع رقم ولا عنوان "
    "ولا اسم ما گاله الزبون.\n"
    "لمن تكتمل الحقول الأربعة، لخّص الطلب واسأله يأكد. وبعد ما يأكد صراحةً، "
    "اختم ردك بسطر مستقل فيه " + MARKER + " ولا شي بعده. "
    "إذا ناقص حقل أو ما أكد صراحةً — لا تكتب العلامة أبداً."
)

TOOL_SYSTEM = (
    "أنت وكيل دعم عراقي بمتجر أجهزة كهربائية.\n\n"
    "عندك أداة واحدة:\n"
    "- get_order_status: ترجع حالة الطلبات. المدخلات: order_id (رقم الطلب) أو "
    "phone (رقم الهاتف) أو status (حالة معينة) أو all (كل الطلبات).\n\n"
    "صيغة الاستدعاء (سطر واحد بدون أي نص قبله أو بعده):\n"
    '[TOOL_CALL]{"tool": "get_order_status", "args": {...}}[/TOOL_CALL]\n\n'
    "قواعد:\n"
    "- إذا سأل الزبون عن حالة طلب أو عن الطلبات، استدعِ الأداة — لا تخمّن الحالة أبداً.\n"
    "- بعد وصول نتيجة الأداة، صِغ نفس البيانات حرفياً باللهجة العراقية بدون تغيير "
    "أو إضافة أي معلومة.\n"
    "- إذا رجعت النتيجة فارغة، گول ماكو بصراحة — ممنوع تذكر أي طلب أو رقم مو بالنتيجة."
)

CONVS = []

# ============================================================
# مولّد المنتجات — منقول حرفياً من v11 حتى تتجانس الكتالوجات
# ============================================================
BRANDS = ["شارب", "گري", "سامسونج", "LG", "هايسنس", "ميديا", "توشيبا", "بيكو",
          "سيمفر", "دينكا", "هيتاشي", "الحافظ", "كونكورد", "نيكاي"]


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
    prods, guard = {}, 0
    while len(prods) < n and guard < 500:
        nm, pr = make_product(kinds)
        prods[nm] = pr
        guard += 1
    return list(prods.items())


def catalog_lines(products):
    return [f"- {nm}: {fmt(pr)} دينار" for nm, pr in products]


def conv(category, subtype, sys_text, turns, direction="answer", has_marker=False):
    """turns: قائمة (user, assistant) — تُبنى بالتناوب مع system أول."""
    msgs = [{"role": "system", "content": sys_text}]
    for u, a in turns:
        msgs.append({"role": "user", "content": u})
        msgs.append({"role": "assistant", "content": a})
    CONVS.append({"messages": msgs, "category": category, "subtype": subtype,
                  "direction": direction, "dialect": "iraqi",
                  "has_marker": has_marker, "source_file": SOURCE})


OPENERS = ["هلا بيك", "حياك الله", "هلا وغلا", "اهلين عيني", "تدلل خوية",
           "نورتنا", "حياك عيني", "يا هلا بيك", "اهلا بيك", "ميت هلا"]

# صيغ أول رسالة — مغايرة عمداً لصيغ v11 حتى ما يفشل فحص التفرد
FIRST_Q = [
    "خوية اريد اسأل عن {p}، بيش؟",
    "لو سمحت شكد تحسبون {p}",
    "عمي شنو سعر {p} عندكم اليوم",
    "استاذ، {p} بيش يجي",
    "سلام، محتاج {p} — شكد سعره",
    "اخوي شكد صاير سعر {p}",
    "دگيقة، {p} شكد تبيعونه",
    "هاي {p} شكد سعرها عندكم",
    "ابو الشباب، بيش {p} عندك",
    "سؤال بس، {p} شكد يكلف",
    "مرحبا اخوية، محتاج اعرف سعر {p}",
    "هلو، {p} شكد حاطينه",
]
FIRST_A = [
    "{o}، {p} عدنا بـ{pr} دينار",
    "{o}، اكو {p} بـ{pr} دينار",
    "{o}، سعر {p} {pr} دينار",
    "{o}، {p} يطلعلك بـ{pr} دينار",
    "{o}، موجود عيني، {p} بـ{pr} دينار",
]


OUT_NAME = "iraqi_v12_order.jsonl"


def _load_old_firsts():
    """أوائل رسائل كل الداتا السابقة — عدا مخرَج هذا السكربت نفسه، وإلا
    قارن التشغيلُ الثاني الملفَ بنسخته السابقة وطلع كله 'مكرر'."""
    old = set()
    for p in sorted(DATA.glob("*.jsonl")):
        if p.name == OUT_NAME:
            continue
        try:
            with open(p, encoding="utf-8") as fh:
                for line in fh:
                    try:
                        old.add(json.loads(line)["messages"][1]["content"].strip())
                    except Exception:
                        pass
        except OSError:
            pass
    return old


OLD_FIRSTS = _load_old_firsts()
USED_FIRSTS = []


def _is_fresh(text):
    text = text.strip()
    if text in OLD_FIRSTS:
        return False
    for prev in USED_FIRSTS:
        if abs(len(text) - len(prev)) > max(len(text), len(prev)) * 0.3:
            continue
        r = max(difflib.SequenceMatcher(None, text, prev).ratio(),
                difflib.SequenceMatcher(None, prev, text).ratio())
        if r > 0.85:
            return False
    return True


def claim_first(text):
    USED_FIRSTS.append(text.strip())


def fresh_price_pair(kinds=None, n=2):
    """يرجع (products, (q, a)) بأول رسالة متفردة مضمونة ضد كل داتا سابقة."""
    for _ in range(6000):
        prods = pick_products(n, kinds)
        p, pr = prods[0]
        q = random.choice(FIRST_Q).format(p=p)
        if _is_fresh(q):
            claim_first(q)
            a = random.choice(FIRST_A).format(o=random.choice(OPENERS), p=p, pr=fmt(pr))
            return prods, (q, a)
    raise RuntimeError("تعذر توليد أول رسالة متفردة")


# ============================================================
# بنك الحقول — القيم كلها تجي من كلام الزبون حصراً
# ============================================================
NAMES = ["حيدر الجبوري", "مصطفى كريم", "علي حسن", "أحمد الساعدي", "كرار عبد",
         "سجاد محمد", "زيد الدليمي", "عمار فاضل", "نور الهدى", "زينب علي",
         "رسل حسين", "مريم قاسم", "امير وسام", "حسنين طالب", "ليث الركابي",
         "غيث سلمان", "براء نعيم", "تبارك جاسم"]
PHONES = ["07701234567", "07811122233", "07501239876", "07711998877",
          "07901456321", "07733221100", "07512348899", "07809988776",
          "07725553311", "07901122334", "07514477882", "07736669900",
          "07802255441", "07907788112", "07719003366", "07526611447"]
CITIES = ["بغداد", "البصرة", "كربلاء", "الناصرية", "النجف", "الموصل",
          "بابل", "ديالى", "السماوة", "العمارة", "كركوك", "الكوت",
          "الديوانية", "تكريت", "الرمادي", "اربيل"]
ADDRESSES = ["الكرادة محلة 909 زقاق 15", "حي الجامعة قرب الجامع",
             "المنصور شارع 14 رمضان", "الحسينية محلة 3",
             "حي الحسين قرب المدرسة", "شارع الاطباء محلة 12",
             "حي الرسالة زقاق 7", "المعقل شارع الكورنيش",
             "حي العسكري محلة 5", "الجزائر قرب السوق",
             "حي الصحة زقاق 22", "شارع الجمهورية محلة 8",
             "حي النصر زقاق 4", "الحبيبية محلة 17",
             "حي الوحدة قرب المستشفى", "الكفاءات شارع 60"]

GIVE_NAME = ["اسمي {v}", "{v}", "اكتب {v}", "سجلها باسم {v}", "اسمي {v} عيني"]
GIVE_PHONE = ["رقمي {v}", "{v}", "اكتب {v}", "هاتفي {v}", "دز على {v}"]
GIVE_CITY = ["من {v}", "{v}", "اني من {v}", "محافظتي {v}", "احنا بـ{v}"]
GIVE_ADDR = ["{v}", "العنوان {v}", "بيتنا بـ{v}", "اكتب {v}"]

# ملاحظة صياغة: صيغ ASK **بلا** إقرار افتتاحي (زين/تمام/على العين)، لأن
# الكود يركّب الإقرار قبلها عند التسلسل. لو حملت الصيغة إقرارها بنفسها
# يطلع ازدواج ركيك («زين عيني، زين، شنو اسمك») — وهو نمط لو دخل التدريب
# يتعلمه الموديل كأسلوب.
ASK = {
    "name": ["شنو اسمك حتى أسجل الطلب؟",
             "انطيني اسمك أول شي حتى أثبت الطلب",
             "شنو أكتب اسم صاحب الطلب؟"],
    "phone": ["انطيني رقم هاتفك حتى نتصل بيك ونتفق عالباقي",
              "شنو رقمك حتى يكون عدنا بالطلب؟",
              "دزلي رقم هاتفك حتى نكدر نوصلك"],
    "city": ["من اي محافظة انت حتى أثبتها بالطلب؟",
             "شنو محافظتك؟",
             "من وين انت حتى أسجل المحافظة؟"],
    "address": ["انطيني العنوان بالتفصيل حتى يلگاك المندوب",
                "وين عنوانك بالضبط؟ محلة وزقاق",
                "شنو العنوان بالتفصيل؟"],
}
FIELD_ORDER = ["name", "phone", "city", "address"]
FIELD_AR = {"name": "الاسم", "phone": "رقم الهاتف",
            "city": "المحافظة", "address": "العنوان"}
BUY_LINES = ["زين خذيته، ثبتلي وحدة", "اوكي اريده، سجل الطلب",
             "تمام، احجزلي وحدة منه", "زين نستلمه، سويلي الطلب",
             "خلص اخذه، ثبت الطلب عيني", "اريده، سجلي الطلب"]
ACK = ["تدلل عيني", "زين عيني", "على العين", "تمام عيني"]


def give(field, val):
    tmpl = {"name": GIVE_NAME, "phone": GIVE_PHONE,
            "city": GIVE_CITY, "address": GIVE_ADDR}[field]
    return random.choice(tmpl).format(v=val)


def summary_line(p, pr, vals):
    """ملخّص الطلب — كل قيمة منسوخة حرفياً من كلام الزبون."""
    return (f"خوش، هذا هو طلبك: {p} عدد 1 بـ{fmt(pr)} دينار، باسم {vals['name']} "
            f"ورقم هاتفك {vals['phone']}، التوصيل لـ{vals['city']} — {vals['address']}. "
            "أثبتلك الطلب؟")


CONFIRMS = ["نعم اكد", "اي ثبته", "اكد الطلب", "زين ثبته عيني",
            "صح، ثبته", "اي صحيح كله، سجله", "تمام اكده", "اي ثبتلي اياه"]

DONE_REPLIES = [
    "تم تثبيت طلبك عيني، وياتك بأقرب وقت ان شاء الله.",
    "ثبتّه عيني، ونتواصل وياك عالرقم اللي انطيتنا اياه.",
    "زين، سجلت الطلب — نتصل بيك قبل ما نوصله.",
    "تمام عيني، الطلب انثبت وراح نخبرك بالتفاصيل.",
]


def build_full_conv(idx):
    """يبني محادثة كاملة الحقول بترتيب عشوائي للأسئلة، ويرجع كل القطع."""
    prods, pp = fresh_price_pair()
    p, pr = prods[0]
    vals = {"name": NAMES[idx % len(NAMES)],
            "phone": PHONES[idx % len(PHONES)],
            "city": CITIES[idx % len(CITIES)],
            "address": ADDRESSES[idx % len(ADDRESSES)]}
    turns = [pp]
    # أول طلب شراء → يسأل أول حقل
    turns.append((random.choice(BUY_LINES),
                  f"{ACK[idx % len(ACK)]}، " + ASK["name"][idx % 3]))
    # باقي الحقول واحد واحد
    for k, f in enumerate(FIELD_ORDER[1:], start=1):
        turns.append((give(FIELD_ORDER[k - 1], vals[FIELD_ORDER[k - 1]]),
                      f"{random.choice(ACK)}، " + ASK[f][(idx + k) % 3]))
    return prods, p, pr, vals, turns


# ════════════════════════════════════════════════════════════
# 1) ord1 — العلامة تنكتب: اكتمال + ملخّص + تأكيد صريح (40)
# ════════════════════════════════════════════════════════════
def gen_ord1():
    made = 0
    for i in range(40):
        prods, p, pr, vals, turns = build_full_conv(i)
        cat = "\n".join(catalog_lines(prods))
        sys_text = ORDER_SYSTEM_TMPL.format(items=cat)
        # آخر حقل ينعطى → ملخّص وسؤال تأكيد (بلا علامة)
        turns.append((give("address", vals["address"]), summary_line(p, pr, vals)))
        # تأكيد صريح → العلامة بسطر مستقل، ولا حرف بعدها
        turns.append((CONFIRMS[i % len(CONFIRMS)],
                      DONE_REPLIES[i % len(DONE_REPLIES)] + "\n" + MARKER))
        conv("ord1_marker_positive", f"full_then_confirm_{i % 8}",
             sys_text, turns, has_marker=True)
        made += 1
    return made


# ════════════════════════════════════════════════════════════
# 2) ord2 — العلامة تُحجب (55). أخطر فئة بالملف كله.
# ════════════════════════════════════════════════════════════
# ثلاث عائلات: (أ) تأكيد صريح بس حقل ناقص، (ب) كلام يشبه التأكيد وهو
# مو تأكيد، (ج) تردد/تأجيل. كلها صفر علامة.
FAKE_CONFIRMS = [
    ("اكيد هذا غالي!", "أفتهمك عيني، بس السعر مكتوب عندي {pr} دينار وما أگدر أغيره"),
    ("نعم بس خلي أفكر", "على راحتك عيني، ما ثبتت شي — خبرني لمن تقرر"),
    ("اي، شكد قلت سعره؟", "{p} بـ{pr} دينار عيني"),
    ("اكيد اكيد، بس قبل شوي سألتك عن الثاني", "زين عيني، {p2} بـ{pr2} دينار"),
    ("صح هذا اللي گلتلك عليه", "اي هو نفسه عيني، {p} بـ{pr} دينار"),
    ("نعم صحيح السعر غالي شوية", "هو السعر المكتوب عندي عيني، {pr} دينار"),
    ("اي والله زين المنتج", "نورتنا عيني، تحب نكمل الطلب؟"),
    ("اكيد راح أفكر بيه", "على راحتك عيني، احنا موجودين"),
    ("نعم سمعتك، بس خل أسأل زوجتي", "تدلل عيني، على راحتك — خبرني لمن تحسم"),
    ("اي هيچي كلش زين", "زين عيني، تريد نثبت الطلب لو بعدك تفكر؟"),
]

HESITATE = [
    ("خل أفكر شوي وأرجعلك", "على راحتك عيني، ما سجلت شي — احنا هنا"),
    ("بعدين أخبرك", "تدلل عيني، خبرني اي وقت"),
    ("ممكن باچر أرد عليك", "زين عيني، ننتظر خبرك"),
    ("لسه ما قررت", "على راحتك، ما ثبتت شي لحد ما تقرر"),
    ("خل أشوف الاسعار بمحلات ثانية", "على راحتك عيني، احنا موجودين اي وقت"),
]


def gen_ord2():
    made = 0
    # (أ) تأكيد صريح لكن حقل ناقص → يسأل الحقل، صفر علامة — 24
    for i in range(24):
        missing = FIELD_ORDER[i % 4]
        have = [f for f in FIELD_ORDER if f != missing]
        prods, pp = fresh_price_pair()
        p, pr = prods[0]
        cat = "\n".join(catalog_lines(prods))
        sys_text = ORDER_SYSTEM_TMPL.format(items=cat)
        vals = {"name": NAMES[(i + 3) % len(NAMES)],
                "phone": PHONES[(i + 5) % len(PHONES)],
                "city": CITIES[(i + 7) % len(CITIES)],
                "address": ADDRESSES[(i + 2) % len(ADDRESSES)]}
        # الزبون ينطي الحقول الموجودة دفعة وحدة، ثم يأكد صراحةً
        blob = "، ".join(give(f, vals[f]) for f in have)
        turns = [pp,
                 (f"{random.choice(BUY_LINES)}. {blob}",
                  f"{random.choice(ACK)}، " + ASK[missing][i % 3]),
                 (CONFIRMS[i % len(CONFIRMS)],
                  f"أمرك عيني، بس محتاج {FIELD_AR[missing]} أول حتى أگدر أثبت الطلب — "
                  + ASK[missing][(i + 1) % 3])]
        conv("ord2_marker_withheld", f"explicit_confirm_missing_{missing}",
             sys_text, turns, has_marker=False)
        made += 1
    # (ب) كلام يشبه التأكيد وهو مو تأكيد — 20
    for i in range(20):
        u, a = FAKE_CONFIRMS[i % len(FAKE_CONFIRMS)]
        prods, pp = fresh_price_pair()
        (p, pr), (p2, pr2) = prods[0], prods[1]
        cat = "\n".join(catalog_lines(prods))
        sys_text = ORDER_SYSTEM_TMPL.format(items=cat)
        turns = [pp, (u, a.format(p=p, pr=fmt(pr), p2=p2, pr2=fmt(pr2)))]
        conv("ord2_marker_withheld", f"pseudo_confirm_{i % 10}",
             sys_text, turns, has_marker=False)
        made += 1
    # (ج) تردد وتأجيل — 11
    for i in range(11):
        u, a = HESITATE[i % len(HESITATE)]
        prods, pp = fresh_price_pair()
        cat = "\n".join(catalog_lines(prods))
        sys_text = ORDER_SYSTEM_TMPL.format(items=cat)
        turns = [pp,
                 (random.choice(BUY_LINES),
                  f"{ACK[i % len(ACK)]}، " + ASK["name"][i % 3]),
                 (u, a)]
        conv("ord2_marker_withheld", f"hesitate_{i % 5}",
             sys_text, turns, has_marker=False)
        made += 1
    return made


# ════════════════════════════════════════════════════════════
# 3) ord3 — بوابة التأكيد: ملخّص وسؤال، والعلامة ما تنكتب بنفس الرد (30)
# ════════════════════════════════════════════════════════════
def gen_ord3():
    made = 0
    for i in range(30):
        prods, p, pr, vals, turns = build_full_conv(i + 40)
        cat = "\n".join(catalog_lines(prods))
        sys_text = ORDER_SYSTEM_TMPL.format(items=cat)
        turns.append((give("address", vals["address"]), summary_line(p, pr, vals)))
        conv("ord3_confirm_gate", f"summary_awaits_confirm_{i % 6}",
             sys_text, turns, has_marker=False)
        made += 1
    return made


# ════════════════════════════════════════════════════════════
# 4) ord4 — «ثبتلي» صراحة وحقل ناقص → رفض التثبيت (45)
# ════════════════════════════════════════════════════════════
# هاي الفئة تعالج بالضبط لقطة «العنوان الوهمي»: الزبون انطى الاسم بس،
# والبائع ثبّت واخترع عنواناً. هنا البائع **يرفض** ويسأل.
SUBMIT_PUSH = [
    "ثبتلي الطلب",
    "خلص سجله ودزه",
    "ثبته هسه ولا تسأل بعد",
    "سجل الطلب وخلصنا",
    "دزه على العنوان المعتاد",
    "ثبته وانته تعرف الباقي",
    "سجله بسرعة، مستعجل",
    "ثبتلي اياه بلا اسئلة",
    "خلص اكتبه وكافي",
]
REFUSE_TMPL = [
    "أمرك عيني، بس ما أگدر أثبته و{f} ناقص — {ask}",
    "على العين، بس محتاج {f} قبل التثبيت — {ask}",
    "تدلل، بس بلا {f} ما ينثبت الطلب — {ask}",
    "زين عيني، بس لازم {f} أول حتى أسجله — {ask}",
]
# ردود على ضغط «انته تعرف» / «العنوان المعتاد» — البائع ما يخترع
NO_INVENT = [
    "ما عندي عنوان مسجل الك عيني، انطيني اياه حتى ما يضيع الطلب",
    "والله ما أگدر أحزر العنوان، گلي اياه بالتفصيل",
    "ما أگدر أكتب شي ما گلته عيني، انطيني العنوان الصحيح",
]


def gen_ord4():
    made = 0
    # (أ) حقل واحد ناقص × ضغط تثبيت — 24
    for i in range(24):
        missing = FIELD_ORDER[i % 4]
        have = [f for f in FIELD_ORDER if f != missing]
        prods, pp = fresh_price_pair()
        cat = "\n".join(catalog_lines(prods))
        sys_text = ORDER_SYSTEM_TMPL.format(items=cat)
        vals = {"name": NAMES[(i + 1) % len(NAMES)],
                "phone": PHONES[(i + 9) % len(PHONES)],
                "city": CITIES[(i + 4) % len(CITIES)],
                "address": ADDRESSES[(i + 6) % len(ADDRESSES)]}
        blob = "، ".join(give(f, vals[f]) for f in have)
        turns = [pp,
                 (f"{random.choice(BUY_LINES)}. {blob}",
                  f"{random.choice(ACK)}، " + ASK[missing][i % 3]),
                 (SUBMIT_PUSH[i % len(SUBMIT_PUSH)],
                  REFUSE_TMPL[i % 4].format(f=FIELD_AR[missing],
                                            ask=ASK[missing][(i + 2) % 3]))]
        conv("ord4_submit_refusal", f"push_missing_{missing}",
             sys_text, turns, has_marker=False)
        made += 1
    # (ب) ضغط «انته تعرف العنوان» → رفض الاختراع صراحةً — 9
    for i in range(9):
        prods, pp = fresh_price_pair()
        cat = "\n".join(catalog_lines(prods))
        sys_text = ORDER_SYSTEM_TMPL.format(items=cat)
        nm = NAMES[(i + 11) % len(NAMES)]
        turns = [pp,
                 (f"{random.choice(BUY_LINES)}. {give('name', nm)}",
                  f"{random.choice(ACK)}، " + ASK["phone"][i % 3]),
                 (random.choice(["دزه على العنوان المعتاد",
                                 "ثبته وانته تعرف وين اسكن",
                                 "العنوان عندكم من قبل، سجله"]),
                  NO_INVENT[i % 3])]
        conv("ord4_submit_refusal", "refuse_invent_address",
             sys_text, turns, has_marker=False)
        made += 1
    # (ج) «ثبتلي طلب» بلا منتج محدد → يسأل أي منتج — 12
    NOPROD = ["ثبتلي طلب", "اريد اسجل طلب", "سويلي طلب عيني",
              "احجزلي شي", "ثبت طلب باسمي", "سجل طلب وخلص",
              "خوية اريد اطلب شي منكم", "ممكن تسجلي طلب؟",
              "استاذ ثبتلي حجز", "اريد اشتري، سجل الطلب",
              "دزلي طلب على العنوان", "افتحلي طلب جديد"]
    for i in range(12):
        prods = pick_products(2)
        (p1, pr1), (p2, pr2) = prods[0], prods[1]
        cat = "\n".join(catalog_lines(prods))
        sys_text = ORDER_SYSTEM_TMPL.format(items=cat)
        u = NOPROD[i % len(NOPROD)]
        claim_first(u)
        a = (f"تدلل عيني، بس اي منتج تريد؟ عدنا {p1} بـ{fmt(pr1)} دينار "
             f"و{p2} بـ{fmt(pr2)} دينار")
        conv("ord4_submit_refusal", "no_product_specified",
             sys_text, [(u, a)], has_marker=False)
        made += 1
    return made


# ════════════════════════════════════════════════════════════
# 5) ord5 — نتيجة أداة فارغة → نفي صريح (40)
# ════════════════════════════════════════════════════════════
# صفر مثال من هذا النوع بـ 12,000 محادثة أداة. والاختراع يصير بالضبط
# لمن ما تجي نتيجة — فهاي أهم فئة بقسم الأدوات.
STATUSES = ["تم التسليم", "جاهز للاستلام", "بالطريق", "مؤجل", "قيد التجهيز"]

EMPTY_BY_ID = [
    "دورت على الرقم هذا وما لگيت اي طلب بيه عيني، تأكدلي من رقم الطلب؟",
    "ماكو طلب مسجل بهذا الرقم عيني — راجع الرقم وخبرني",
    "ما طلع عندي اي طلب بهذا المعرّف، ممكن تتأكد من الرقم؟",
]
EMPTY_BY_PHONE = [
    "ماكو اي طلب مسجل على هذا الرقم عيني، تأكد من رقم الهاتف؟",
    "دورت بالرقم وما لگيت طلبات مسجلة بيه — ممكن يكون مسجل برقم ثاني؟",
    "ما عندي طلبات على هذا الهاتف عيني، تريد تتأكد من الرقم؟",
]
EMPTY_BY_STATUS = [
    "ماكو طلبات بهذي الحالة حالياً عيني",
    "ما عندي اي طلب بهذي الحالة هسه",
    "دورت وما لگيت ولا طلب بهذي الحالة حالياً",
]


def _tool_call(args):
    return ('[TOOL_CALL]{"tool": "get_order_status", "args": '
            + json.dumps(args, ensure_ascii=False) + "}[/TOOL_CALL]")


def _tool_result(payload):
    return ("[نتيجة الأداة get_order_status]: "
            + json.dumps(payload, ensure_ascii=False))


def gen_ord5():
    made = 0
    ASK_ID = ["سلام، شنو حالة طلبي رقم {v}؟",
              "عمي دگق على الطلب رقم {v}",
              "اريد اعرف وين وصل طلبي {v}",
              "الطلب رقم {v} شصار بيه؟",
              "خوية شيكلي على الطلب {v}",
              "استاذ، وين صار الطلب رقم {v}",
              "ممكن تشوف الطلب {v} شنو وضعه",
              "هلو، عندي طلب مرقم {v} — شنو اخباره؟",
              "دگيقة، الطلب {v} تحرك لو باقي؟",
              "لو سمحت افتحلي الطلب رقم {v}",
              "مرحبا، اتابع طلبي {v} شنو حالته",
              "اخوي الطلب {v} خلص لو بعده؟",
              "شوفلي وضع الطلب {v} رجاءً",
              "عندي رقم طلب {v}، شنو يطلع بيه؟",
              "سؤال، الطلب {v} وين وصل هسه؟"]
    ASK_PH = ["دور على طلباتي برقمي {v}",
              "شيك على الطلبات المسجلة على {v}",
              "رقمي {v}، شنو عندي طلبات؟",
              "هاتفي {v} — اكو شي مسجل الي؟",
              "ابحثلي بالرقم {v} عن طلباتي",
              "خوية شوف شنو عندي على {v}",
              "على الرقم {v} اكو طلبات لو لا؟",
              "استاذ دگق على {v} شنو مسجل بيه",
              "ممكن تشوف طلباتي على هاتف {v}؟",
              "الرقم {v} مالتي، عندي طلبات؟",
              "افحصلي {v} شنو طلبات عليه",
              "لو سمحت الرقم {v} شنو يطلع بيه",
              "اتابع طلباتي، رقمي هو {v}"]
    # (أ) معرّف مو موجود — 15
    for i in range(15):
        oid = str(10000 + (i * 7717) % 89999)
        u = ASK_ID[i % len(ASK_ID)].format(v=oid)
        claim_first(u)
        turns = [(u, _tool_call({"order_id": oid})),
                 (_tool_result({"error": "ماكو طلب بهذا الرقم"}),
                  EMPTY_BY_ID[i % 3])]
        conv("ord5_tool_empty", "empty_by_order_id", TOOL_SYSTEM, turns,
             direction="refer")
        made += 1
    # (ب) هاتف بلا طلبات — 13
    for i in range(13):
        ph = PHONES[(i + 2) % len(PHONES)]
        u = ASK_PH[i % len(ASK_PH)].format(v=ph)
        claim_first(u)
        turns = [(u, _tool_call({"phone": ph})),
                 (_tool_result({"error": "ماكو طلبات على هذا الرقم"}),
                  EMPTY_BY_PHONE[i % 3])]
        conv("ord5_tool_empty", "empty_by_phone", TOOL_SYSTEM, turns,
             direction="refer")
        made += 1
    # (ج) حالة بلا نتائج — 12
    # ملاحظة: صيغ هذي الفئة لازم تكون ≥ عددها، لأن الحالة الواحدة تتكرر
    # عبر الدورة — صيغة واحدة لكل مثال، بلا لواحق تمييز مصطنعة.
    ASK_ST = ["اكو طلبات {v} هسه؟", "شنو الطلبات اللي {v}؟",
              "عندك شي {v} اليوم؟", "دورلي على الطلبات {v}",
              "هل اكو شي بحالة {v}؟", "شوفلي اذا اكو {v}",
              "عدك طلبات وضعها {v}؟", "بالنظام اكو {v} لو ماكو؟",
              "افحصلي شنو {v} حالياً", "گلي اذا باقي شي {v}",
              "اطلعلي على اللي {v} هسه", "شكد صار عدنا {v} اليوم؟"]
    for i in range(12):
        st = STATUSES[i % len(STATUSES)]
        u = ASK_ST[i % len(ASK_ST)].format(v=st)
        claim_first(u)
        turns = [(u, _tool_call({"status": st})),
                 (_tool_result({"error": "ماكو طلبات بهذي الحالة"}),
                  EMPTY_BY_STATUS[i % 3])]
        conv("ord5_tool_empty", "empty_by_status", TOOL_SYSTEM, turns,
             direction="refer")
        made += 1
    return made


# ════════════════════════════════════════════════════════════
# 6) ord6 — وسيطا status/all + صياغة قائمة نتائج (40)
# ════════════════════════════════════════════════════════════
def _fmt_list(rows):
    """يعدّد النتائج كلها بلا حذف ولا إضافة، بنفس المعرّفات والحالات."""
    parts = [f"الطلب {r['order_id']} {r['status']}" for r in rows]
    return "، و".join(parts) if len(parts) > 1 else parts[0]


def gen_ord6():
    made = 0
    # 25 صيغة لـ25 مثال — واحدة لكل مثال، حتى ما نحتاج لواحق تمييز
    ASK_ST = ["شنو الطلبات {v}؟", "اكو طلبات {v} عندك؟",
              "عطني الطلبات اللي {v}", "شكد طلب {v} هسه؟",
              "دورلي كل الطلبات {v}", "منو الطلبات {v} حالياً؟",
              "اعرضلي اللي {v}", "شوفلي الطلبات بحالة {v}",
              "خوية شنو عدنا {v}؟", "استاذ اطلعلي على {v}",
              "بالنظام شنو {v} اليوم؟", "گلي الطلبات {v} شكد صارت",
              "افحصلي كل شي {v}", "ممكن قائمة بالطلبات {v}؟",
              "شنو اللي وضعه {v} هسه؟", "اريد اشوف الطلبات {v}",
              "لو سمحت عطني {v} كلها", "دگق شنو عدنا {v}",
              "هاي {v} شكد طلب؟", "اجمعلي الطلبات {v}",
              "سؤال، شنو {v} عندكم؟", "طلع القائمة مال {v}",
              "شوف شنو باقي {v}", "عدد الطلبات {v} شكد؟",
              "اريد تقرير بكل {v}"]
    ASK_ALL = ["شنو كل الطلبات المسجلة هسه؟",
               "عطني جرد بكل الطلبات",
               "شكد طلب عدنا بالمجموع؟",
               "اعرضلي الطلبات كلها",
               "شنو الموجود بالنظام من طلبات؟",
               "اريد قائمة كاملة بالطلبات",
               "طلعلي كل شي مسجل عدنا",
               "خوية شنو عدنا طلبات اليوم كلها؟",
               "دگق على النظام وعطني الكل",
               "ممكن جرد شامل للطلبات؟",
               "اجمعلي كل الطلبات الموجودة",
               "شوفلي شنو مسجل بالنظام كله",
               "استاذ اريد اشوف الطلبات جميعها",
               "اعطني ملخص بكل الطلبات المسجلة",
               "شنو عدنا بالسجل من طلبات؟"]
    # (أ) استعلام بالحالة → status + تعداد النتائج — 25
    for i in range(25):
        st = STATUSES[i % len(STATUSES)]
        u = ASK_ST[i % len(ASK_ST)].format(v=st)
        claim_first(u)
        n = 1 + (i % 3)
        rows = [{"order_id": str(20000 + (i * 313 + k * 37) % 79999), "status": st}
                for k in range(n)]
        turns = [(u, _tool_call({"status": st})),
                 (_tool_result({"orders": rows, "count": n}),
                  f"عدنا {_fmt_list(rows)}")]
        conv("ord6_tool_status_args", f"query_by_status_{n}", TOOL_SYSTEM, turns)
        made += 1
    # (ب) جرد شامل → all — 15
    for i in range(15):
        u = ASK_ALL[i % len(ASK_ALL)]
        claim_first(u)
        n = 2 + (i % 3)
        rows = [{"order_id": str(30000 + (i * 911 + k * 53) % 69999),
                 "status": STATUSES[(i + k) % len(STATUSES)]} for k in range(n)]
        turns = [(u, _tool_call({"all": True})),
                 (_tool_result({"orders": rows, "count": n}),
                  f"عدنا {n} طلبات: {_fmt_list(rows)}")]
        conv("ord6_tool_status_args", f"query_all_{n}", TOOL_SYSTEM, turns)
        made += 1
    return made


# ════════════════════════════════════════════════════════════
# الفحص الذاتي — يمتد فحص v11 بقواعد العلامة والأدوات
# ════════════════════════════════════════════════════════════
NUM_RE = re.compile(r'\d[\d,\.]*')
FUSHA_FLAGS = ["يمكنني", "بالتأكيد", "يسعدني", "سوف ", "هل ترغب", "أستطيع أن"]
FLATTERY = ["سؤال ممتاز", "سؤال حلو", "سؤال رائع", "منور", "ذوقك", "اختيار موفق",
            "انت محق تماما", "عندك حق تماما", "كلامك صحيح 100"]
FOREIGN_DIALECT = ["شو ", "هلق", "منيح", "إزيك", "خالص كده", "لا يخالف", "دلوقتي"]


def nums_of(text):
    text = re.sub(r'(\d+)\s*(?:ألف|الف)', lambda m: f"{m.group(1)},000", text)
    return {n.rstrip('.,') for n in NUM_RE.findall(text)}


def self_check():
    errs = []
    firsts = []
    for idx, r in enumerate(CONVS, 1):
        msgs = r["messages"]
        is_tool = r["category"].startswith(("ord5", "ord6"))
        if msgs[0]["role"] != "system" or msgs[-1]["role"] != "assistant":
            errs.append(f"[{idx}] بنية مكسورة")
        for j, m in enumerate(msgs[1:]):
            want = "user" if j % 2 == 0 else "assistant"
            if m["role"] != want or not m["content"].strip():
                errs.append(f"[{idx}] تناوب مكسور عند {j + 1}")
                break
        # ---- أرقام: كل رقم برد البائع من الكتالوج أو رسائل الزبون ----
        cat_nums = nums_of(msgs[0]["content"])
        user_nums = set()
        for m in msgs[1:]:
            if m["role"] == "user":
                user_nums |= nums_of(m["content"])
                continue
            for num in nums_of(m["content"]):
                if num in cat_nums or num in user_nums:
                    continue
                if ',' not in num and '.' not in num and len(num) <= 2:
                    continue
                errs.append(f"[{idx}] رقم مخترع '{num}': {m['content'][:60]}")
        # ---- لهجة + إطراء ----
        for m in msgs:
            if m["role"] != "assistant":
                continue
            for fl in FUSHA_FLAGS:
                if fl in m["content"]:
                    errs.append(f"[{idx}] فصحى ممنوعة '{fl}': {m['content'][:60]}")
            for fl in FLATTERY:
                if fl in m["content"]:
                    errs.append(f"[{idx}] إطراء متودد '{fl}': {m['content'][:60]}")
            for fl in FOREIGN_DIALECT:
                if fl in m["content"]:
                    errs.append(f"[{idx}] لهجة غير عراقية '{fl}': {m['content'][:60]}")
        # ---- ازدواج الإقرار الافتتاحي ----
        # («زين عيني، زين، شنو اسمك») — ركاكة تتعلّم كأسلوب لو دخلت.
        for m in msgs:
            if m["role"] != "assistant":
                continue
            head = m["content"][:40]
            hits = [w for w in ("زين", "تمام", "على العين", "تدلل") if w in head]
            if len(hits) >= 2 or any(head.count(w) >= 2 for w in hits):
                errs.append(f"[{idx}] ازدواج إقرار: {head}")
        # ---- انضباط العلامة ----
        marked = [m for m in msgs if m["role"] == "assistant" and MARKER in m["content"]]
        if r["has_marker"]:
            if len(marked) != 1:
                errs.append(f"[{idx}] متوقع علامة وحدة، لگيت {len(marked)}")
            elif marked[0] is not msgs[-1]:
                errs.append(f"[{idx}] العلامة مو بالرد الأخير")
            elif not msgs[-1]["content"].rstrip().endswith(MARKER):
                errs.append(f"[{idx}] اكو نص بعد العلامة")
            elif "\n" + MARKER not in msgs[-1]["content"]:
                errs.append(f"[{idx}] العلامة مو بسطر مستقل")
            # لازم يسبقها تأكيد صريح من الزبون
            if msgs[-2]["content"].strip() not in CONFIRMS:
                errs.append(f"[{idx}] علامة بلا تأكيد صريح: '{msgs[-2]['content'][:40]}'")
        elif marked:
            errs.append(f"[{idx}] علامة ما تنراد بفئة {r['category']}")
        # ---- استخراج الحقول: ولا قيمة ما گالها الزبون ----
        if r["category"].startswith(("ord1", "ord3")):
            said = " ".join(m["content"] for m in msgs if m["role"] == "user")
            for m in msgs:
                if m["role"] != "assistant":
                    continue
                for city in CITIES:
                    if city in m["content"] and city not in said:
                        errs.append(f"[{idx}] محافظة مخترعة '{city}'")
                for nm in NAMES:
                    if nm in m["content"] and nm not in said:
                        errs.append(f"[{idx}] اسم مخترع '{nm}'")
        # ---- الأدوات ----
        if is_tool:
            calls = [m for m in msgs if m["role"] == "assistant" and "TOOL_CALL" in m["content"]]
            if len(calls) != 1 or calls[0] is not msgs[2]:
                errs.append(f"[{idx}] استدعاء الأداة مو بالرد الأول")
            else:
                c = calls[0]["content"].strip()
                if not (c.startswith("[TOOL_CALL]") and c.endswith("[/TOOL_CALL]")):
                    errs.append(f"[{idx}] صيغة منحرفة: نص قبل/بعد الاستدعاء")
                try:
                    json.loads(c[len("[TOOL_CALL]"):-len("[/TOOL_CALL]")])
                except Exception:
                    errs.append(f"[{idx}] JSON مكسور بالاستدعاء")
            # الرد النهائي: كل معرّف يذكره لازم يجي من نتيجة الأداة
            res = [m for m in msgs if m["role"] == "user" and "نتيجة الأداة" in m["content"]]
            if res:
                res_nums = nums_of(res[-1]["content"])
                for num in nums_of(msgs[-1]["content"]):
                    if len(num) >= 4 and num not in res_nums:
                        errs.append(f"[{idx}] رقم مو بنتيجة الأداة '{num}'")
                # نتيجة فارغة → ممنوع ذكر أي معرّف
                if "error" in res[-1]["content"]:
                    if any(len(n) >= 4 for n in nums_of(msgs[-1]["content"])
                           if n not in nums_of(" ".join(
                               m["content"] for m in msgs if m["role"] == "user"))):
                        errs.append(f"[{idx}] اختراع طلب عند نتيجة فارغة")
        firsts.append((idx, msgs[1]["content"].strip()))
    # ---- تفرّد أول رسالة داخلياً ----
    for a in range(len(firsts)):
        ia, ta = firsts[a]
        for b in range(a + 1, len(firsts)):
            ib, tb = firsts[b]
            if abs(len(ta) - len(tb)) > max(len(ta), len(tb)) * 0.3:
                continue
            if difflib.SequenceMatcher(None, ta, tb).ratio() > 0.9:
                errs.append(f"[{ib}] أول رسالة متشابهة >90% مع [{ia}]: '{tb[:45]}'")
    # ---- تفرّد ضد كل الداتا القديمة ----
    for idx, t in firsts:
        if t in OLD_FIRSTS:
            errs.append(f"[{idx}] أول رسالة مكررة حرفياً من داتا قديمة: '{t[:45]}'")
    return errs


def main():
    gen_ord1()
    gen_ord2()
    gen_ord3()
    gen_ord4()
    gen_ord5()
    gen_ord6()

    errs = self_check()
    if errs:
        print(f"❌ {len(errs)} مخالفة بالفحص الذاتي — ما انكتب الملف:")
        for e in errs[:40]:
            print("   " + e)
        sys.exit(1)

    out = DATA / OUT_NAME
    with open(out, "w", encoding="utf-8", newline="\n") as f:
        for r in CONVS:
            f.write(json.dumps(r, ensure_ascii=False) + "\n")

    print(f"✅ iraqi_v12_order.jsonl: {len(CONVS)} مثال")
    c = Counter(r["category"] for r in CONVS)
    target = {"ord1_marker_positive": 40, "ord2_marker_withheld": 55,
              "ord3_confirm_gate": 30, "ord4_submit_refusal": 45,
              "ord5_tool_empty": 40, "ord6_tool_status_args": 40}
    print(f"\n{'الفئة':<28}{'المتحقق':>8}{'المستهدف':>10}")
    for cat in target:
        n = c.get(cat, 0)
        print(f"{cat:<28}{n:>8}{target[cat]:>10}  {'✔' if n == target[cat] else '✘'}")
    print(f"{'المجموع':<28}{len(CONVS):>8}{sum(target.values()):>10}")
    pos = sum(1 for r in CONVS if r["has_marker"])
    neg = sum(1 for r in CONVS
              if not r["has_marker"] and r["category"].startswith(("ord1", "ord2", "ord3", "ord4")))
    print(f"\nالعلامة: موجب {pos} | سالب {neg} | النسبة 1:{neg / pos:.2f}")
    print(f"توزيع الأدوار: " + "، ".join(
        f"{k} دور={v}" for k, v in sorted(Counter(len(r['messages']) // 2 for r in CONVS).items())))
    print("🟢 الفحص الذاتي عدّ: صفر رقم مخترع، صفر عنوان/اسم مخترع، "
          "صفر علامة بلا تأكيد، صفر اختراع عند نتيجة فارغة، صفر تكرار.")


if __name__ == "__main__":
    main()
