# -*- coding: utf-8 -*-
"""
توليد الأمثلة الناقصة من مواصفات AA.md (القدرات الغائبة تماماً عن بيانات v4/v5):

1. استخراج JSON (قسم 4 من AA.md)      — محادثة بيع كاملة -> JSON صافي بالمخطط المحدد
2. استدعاء الأدوات (قسم 4.5)           — [TOOL_CALL] طلب الأداة + صياغة نتيجتها حرفياً
3. «أتأكدلك» لمعلومة ناقصة (قسم 1)     — الكتالوج بلا سعر تركيب/توصيل -> رد بدون أي رقم

الكتالوجات من data/product_bank_v5.json (نفس بنك v5) مع أسعار عشوائية بكل مثال.
الناتج: data/iraqi_extras_v6_train.jsonl + data/iraqi_extras_v6_val.jsonl
يمرّ الناتج على prepare_v6_data.py مثل باقي البيانات (فحص أرقام، تفريد، فلتر لهجة).
"""
import json
import random

random.seed(1234)

N_JSON_EXTRACT = 6000
N_TOOL_REQUEST = 1500
N_TOOL_FORMAT = 1500
N_CONFIRM_LATER = 3000
N_REPEAT_QUESTION = 2000  # AA.md قسم 2.5: الزبون يكرر نفس السؤال والرد الثاني ثابت
VAL_FRACTION = 0.05

BANK = json.load(open("data/product_bank_v5.json", encoding="utf-8"))

# ---------------- أدوات مشتركة ----------------
MALE_NAMES = ["أحمد", "علي", "حسين", "محمد", "كرار", "مصطفى", "حيدر", "عمر", "سجاد", "ياسر",
              "أبو علي", "أبو حسن", "أبو مصطفى", "ليث", "سيف", "مرتضى", "عباس", "ضرغام"]
FEMALE_NAMES = ["أم علي", "زينب", "فاطمة", "نور", "رسل", "آية", "طيبة", "بنين", "غدير", "زهراء"]
ADDRESSES = ["بغداد، حي الجهاد", "بغداد، الكرادة", "بغداد، مدينة الصدر", "بغداد، الأعظمية",
             "بغداد، المنصور", "بغداد، زيونة", "بغداد، الدورة", "بغداد، الشعلة",
             "البصرة، العشار", "البصرة، الجزائر", "النجف، حي السلام", "كربلاء، حي الحسين",
             "الموصل، الزهور", "أربيل، عينكاوة", "الحلة، حي الجامعة", "الناصرية، الشموخ",
             "الديوانية، العروبة", "كركوك، الواسطي", "السماوة، الغربي", "العمارة، الحسين"]
QTY_WORDS = {1: ["وحدة", "حبة", "واحد"], 2: ["حبتين", "ثنين", "اثنين"],
             3: ["ثلاثة", "ثلث حبات", "3"], 4: ["أربعة", "أربع حبات", "4"]}


def phone():
    return "07" + random.choice("579") + "".join(random.choice("0123456789") for _ in range(8))


def fmt_price(n):
    return f"{n:,}"


def rand_price(lo, hi):
    step = 25000 if hi < 3000000 else 250000
    return fmt_price(random.randrange(lo, hi, step))


def build_catalog(k=None):
    """يرجع (نص الكتالوج، قائمة (اسم منتج، سعر نصي))."""
    cat_name = random.choice(list(BANK))
    cat = BANK[cat_name]
    items = []
    prods = list(cat.items())
    random.shuffle(prods)
    for pname, meta in prods[: k or random.randint(3, 7)]:
        brand = random.choice(meta["brands"])
        spec = random.choice(meta["specs"]) if meta.get("specs") else ""
        lo, hi = meta["price_range"]
        full = " ".join(f"{pname} {brand} {spec}".split())
        items.append((full, rand_price(lo, hi)))
    text = "\n".join(f"- {n}: {p} دينار" for n, p in items)
    return text, items


CONFIRM_NOTES = [
    "تدلل عيني، طلبك صار جاهز للتجهيز",
    "خوش طلب، نجهزه ونخبرك",
    "تدلل، نرتبلك الطلب ونتصل بيك",
    "الله يبارك بيك، طلبك وصلنا",
    "زين اختيارك، نجهزه هسه",
    "تدلل، الطلب بالطريق إن شاء الله",
    "خوش شراء، عاشت ايدك",
    "تم الطلب، منورنا",
]

# ============================================================
# 1) استخراج JSON
# ============================================================
EXTRACT_SYSTEM = """أنت نظام استخراج بيانات دقيق. حوّل المحادثة إلى JSON فقط — بدون أي نص قبله أو بعده وبدون Markdown.

المخطط المطلوب:
{
  "customer_name": "الاسم إن ذُكر وإلا null",
  "customer_phone": "الهاتف إن ذُكر وإلا null",
  "customer_address": "العنوان إن ذُكر وإلا null",
  "items": [{"product_name": "اسم المنتج", "quantity": 1}],
  "suggested_product_name": "المنتج الإضافي إن وافق عليه الزبون وإلا null",
  "notes": "ملاحظات إضافية وإلا null",
  "confirmation_note": "جملة ودّية عراقية قصيرة بدون أي رقم أو سعر"
}"""

ASK_TEMPLATES = ["هلا، شكد {p}؟", "السلام عليكم، اكو {p}؟ بيش؟", "مرحبا عندكم {p}؟ شكد سعره؟",
                 "هلو شلونكم، أريد {p} شگد يطلع؟", "بيش {p} عدكم؟"]
SELLER_PRICE = ["هلا بيك، {p} سعره {price} دينار", "حياك الله، اكو {p} بـ{price} دينار",
                "أهلين، {p} يطلع عليك {price} دينار", "تفضل، {p} موجود بـ{price} دينار"]
# صيغة مؤنثة (AA.md قسم 5: هلا بيج، تريدين)
SELLER_PRICE_F = ["هلا بيج، {p} سعره {price} دينار", "حياج الله، اكو {p} بـ{price} دينار",
                  "تفضلي، {p} موجود بـ{price} دينار", "أهلين خيتي، {p} يطلع عليج {price} دينار"]
ADD_ITEM = ["وهم أريد {p3}، {qw} منه", "وضيفلي هم {p3} {qw}", "بعد أريد {p3}، خلي {qw} وياه"]
BUY_QTY = ["زين، اريد {qw} من فضلك", "خوش، ظمّلي {qw} منه", "تمام آخذ {qw}", "اوكي احجزلي {qw}"]
GIVE_NAME_PHONE = ["اسمي {name} ورقمي {ph}", "آني {name}، رقم تلفوني {ph}",
                   "سجل: {name}، هاتف {ph}", "الاسم {name} والرقم {ph} اذا تحتاجون"]
GIVE_ADDRESS = ["والعنوان {addr}", "توصلوه على {addr}", "دزوه على {addr} رجاءً"]
SUGGEST = ["نضيفلك وياه {p2} بـ{price2} دينار؟", "تحب تاخذ وياه {p2}؟ سعره {price2} دينار"]
ACCEPT = ["اي زين ضيفه", "خوش فكرة، ضمه للطلب", "اي والله ضيفه"]
REFUSE = ["لا شكراً بس الأول", "لا خلي بس اللي طلبته", "لا يكفي هذا"]
NOTES_POOL = ["يريد التوصيل عصراً", "يفضل الدفع نقداً عند الاستلام", "طلب تغليف هدية",
              "يستلم من المحل بنفسه", "يريد فاتورة باسم الشركة"]


def gen_json_extraction():
    text_cat, items = build_catalog()
    p1, price1 = random.choice(items)
    qty = random.choices([1, 2, 3, 4], weights=[50, 30, 12, 8])[0]
    qw = random.choice(QTY_WORDS[qty])

    female = random.random() < 0.3
    name = random.choice(FEMALE_NAMES if female else MALE_NAMES) if random.random() < 0.75 else None
    ph = phone() if random.random() < 0.7 else None
    addr = random.choice(ADDRESSES) if random.random() < 0.6 else None
    note = random.choice(NOTES_POOL) if random.random() < 0.3 else None

    price_pool = SELLER_PRICE_F if female else SELLER_PRICE

    lines = []
    lines.append("زبون: " + random.choice(ASK_TEMPLATES).format(p=p1))
    lines.append("بائع: " + random.choice(price_pool).format(p=p1, price=price1))
    lines.append("زبون: " + random.choice(BUY_QTY).format(qw=qw))

    order_items = [{"product_name": p1, "quantity": qty}]
    # AA.md قسم 4: «طلب عدة منتجات» — ~30% من الأمثلة فيها منتج ثانٍ مشترى
    used = {p1}
    if len(items) > 1 and random.random() < 0.3:
        p3, price3 = random.choice([it for it in items if it[0] not in used])
        used.add(p3)
        qty3 = random.choices([1, 2, 3], weights=[60, 30, 10])[0]
        qw3 = random.choice(QTY_WORDS[qty3])
        lines.append("بائع: تدلل، شي ثاني؟")
        lines.append("زبون: " + random.choice(ADD_ITEM).format(p3=p3, qw=qw3))
        lines.append("بائع: " + random.choice(price_pool).format(p=p3, price=price3))
        order_items.append({"product_name": p3, "quantity": qty3})

    suggested = None
    if len(items) > len(used) and random.random() < 0.5:
        p2, price2 = random.choice([it for it in items if it[0] not in used])
        lines.append("بائع: " + random.choice(SUGGEST).format(p2=p2, price2=price2))
        if random.random() < 0.5:
            lines.append("زبون: " + random.choice(ACCEPT))
            suggested = p2
        else:
            lines.append("زبون: " + random.choice(REFUSE))

    details = []
    if name and ph:
        details.append(random.choice(GIVE_NAME_PHONE).format(name=name, ph=ph))
    elif name:
        details.append(f"اسمي {name}")
    elif ph:
        details.append(f"رقمي {ph}")
    if addr:
        details.append(random.choice(GIVE_ADDRESS).format(addr=addr))
    if note:
        details.append(note.replace("يريد", "أريد").replace("يفضل", "أفضل").replace("يستلم", "أستلم").replace("طلب ", "أريد "))
    if details:
        lines.append("زبون: " + "، ".join(details))
        lines.append("بائع: تمام، تدلل. الطلب انسجل")
    else:
        lines.append("بائع: تدلل، جاهز طلبك")

    out = {
        "customer_name": name,
        "customer_phone": ph,
        "customer_address": addr,
        "items": order_items,
        "suggested_product_name": suggested,
        "notes": note,
        "confirmation_note": random.choice(CONFIRM_NOTES),
    }
    return {
        "messages": [
            {"role": "system", "content": EXTRACT_SYSTEM},
            {"role": "user", "content": "\n".join(lines)},
            {"role": "assistant", "content": json.dumps(out, ensure_ascii=False)},
        ],
        "category": "json_extraction",
        "dialect": "iraqi",
        "source_file": "generate_v6_extras.py",
    }


# ============================================================
# 2) استدعاء الأدوات
# ============================================================
TOOL_SYSTEM = """أنت وكيل دعم عراقي بمتجر أجهزة كهربائية.

عندك أداة واحدة:
- get_order_status: ترجع حالة طلب الزبون. المدخلات: order_id (رقم الطلب) أو phone (رقم الهاتف).

صيغة الاستدعاء (سطر واحد بدون أي نص قبله أو بعده):
[TOOL_CALL]{"tool": "get_order_status", "args": {...}}[/TOOL_CALL]

قواعد:
- إذا سأل الزبون عن حالة طلبه، استدعِ الأداة — لا تخمّن الحالة أبداً.
- بعد وصول نتيجة الأداة، صِغ نفس البيانات حرفياً باللهجة العراقية بدون تغيير أو إضافة أي معلومة."""

ASK_ORDER_ID = ["هلا، أريد أعرف وين وصل طلبي رقم {oid}", "شلونكم، طلبي رقم {oid} شصار بيه؟",
                "مرحبا، رقم طلبي {oid} ممكن اتشيكلي عليه؟", "اخي طلب {oid} متى يوصل؟",
                "سلام، عندي طلب برقم {oid} شنو حالته هسه؟"]
ASK_PHONE = ["هلا، طلبت من عدكم وما أذكر رقم الطلب، رقمي {ph}", "شلونكم، اتشيكولي على طلبي؟ هاتفي {ph}",
             "مرحبا سويت طلب برقم هاتفي {ph}، وين وصل؟"]

STATUSES = [
    ("قيد التجهيز", ["طلبك رقم {oid} هسه قيد التجهيز", "طلبك {oid} دنجهزه هسه"]),
    ("بالطريق", ["طلبك رقم {oid} طالع بالطريق", "طلبك {oid} هسه بالطريق وياك"]),
    ("جاهز للاستلام", ["طلبك رقم {oid} جاهز للاستلام من المحل", "تگدر تستلم طلبك {oid}، جاهز بالمحل"]),
    ("مؤجل", ["طلبك رقم {oid} تأجل للأسف", "صار تأجيل بطلبك {oid}"]),
    ("تم التسليم", ["طلبك رقم {oid} تم تسليمه", "طلبك {oid} انسلّم"]),
]
DELIVERY_DAYS = ["باچر", "بعد باچر", "الخميس الجاي", "الجمعة", "السبت", "الأحد الجاي", "خلال يومين", "نهاية الأسبوع"]


def gen_tool_request():
    oid = str(random.randint(10000, 99999))
    by_phone = random.random() < 0.3
    if by_phone:
        ph = phone()
        user = random.choice(ASK_PHONE).format(ph=ph)
        args = {"phone": ph}
    else:
        user = random.choice(ASK_ORDER_ID).format(oid=oid)
        args = {"order_id": oid}
    call = '[TOOL_CALL]{"tool": "get_order_status", "args": ' + json.dumps(args, ensure_ascii=False) + "}[/TOOL_CALL]"
    return {
        "messages": [
            {"role": "system", "content": TOOL_SYSTEM},
            {"role": "user", "content": user},
            {"role": "assistant", "content": call},
        ],
        "category": "tool_call_request",
        "dialect": "iraqi",
        "source_file": "generate_v6_extras.py",
    }


def gen_tool_format():
    oid = str(random.randint(10000, 99999))
    status, phr = random.choice(STATUSES)
    user = random.choice(ASK_ORDER_ID).format(oid=oid)
    call = '[TOOL_CALL]{"tool": "get_order_status", "args": {"order_id": "' + oid + '"}}[/TOOL_CALL]'

    result = {"order_id": oid, "status": status}
    reply = random.choice(phr).format(oid=oid)
    if status in ("قيد التجهيز", "بالطريق", "مؤجل") and random.random() < 0.8:
        day = random.choice(DELIVERY_DAYS)
        result["expected_delivery"] = day
        reply += f"، والتسليم المتوقع {day}"
    reply += "." if not reply.endswith(".") else ""

    return {
        "messages": [
            {"role": "system", "content": TOOL_SYSTEM},
            {"role": "user", "content": user},
            {"role": "assistant", "content": call},
            {"role": "user", "content": "[نتيجة الأداة get_order_status]: " + json.dumps(result, ensure_ascii=False)},
            {"role": "assistant", "content": reply},
        ],
        "category": "tool_call_format",
        "dialect": "iraqi",
        "source_file": "generate_v6_extras.py",
    }


# ============================================================
# 3) «أتأكدلك» — معلومة ناقصة بالكتالوج
# ============================================================
SELLER_SYSTEM_TMPL = """أنت موظف مبيعات بمحل عراقي.

الموجود حالياً:
{catalog}

انسخ الأسعار والأسماء حرفياً من القائمة. إذا انسألت عن معلومة مو مكتوبة بالقائمة (تركيب، توصيل، ضمان...) گول أتأكدلك وأرد عليك — لا تخترع رقم."""

MISSING_TOPICS = [
    ("التركيب", ["والتركيب بيش يطلع؟", "شكد أجرة التركيب؟", "التركيب عليكم لو بفلوس؟ شكد؟"]),
    ("التوصيل", ["والتوصيل شكد يكلف؟", "بيش التوصيل لمنطقتي؟", "توصلون؟ وشكد التوصيل؟"]),
    ("الضمان", ["وشكد مدة الضمان؟", "بيه ضمان؟ شكد؟", "الضمان شگد فترته؟"]),
    ("الألوان المتوفرة", ["شنو الألوان الموجودة منه؟", "اكو منه لون أبيض؟", "شنو ألوانه المتوفرة؟"]),
    ("موعد وصول البضاعة الجديدة", ["شوكت توصلكم بضاعة جديدة؟", "متى تجيكم دفعة جديدة؟"]),
    ("التقسيط", ["اكو عدكم تقسيط؟ شلون نظامه؟", "تسوون أقساط؟ شنو الشروط؟"]),
]
CONFIRM_LATER_REPLIES = [
    "والله ما أگدر أجاوبك بالضبط هسه، أتأكدلك وأرد عليك",
    "هاي المعلومة مو موجودة عندي هسه، أتأكدلك من الإدارة وأخبرك",
    "خليني أتأكدلك من المسؤول وأرد عليك بأقرب وقت",
    "ما أحب أگلك شي مو أكيد، أتأكدلك وأخبرك",
    "صراحة لازم أتأكد أول، أتأكدلك وأرجعلك بالجواب",
    "أتأكدلك من المخزن وأرد عليك، ما أريد أغلطك",
]


def gen_confirm_later():
    text_cat, items = build_catalog()
    p1, price1 = random.choice(items)
    topic, questions = random.choice(MISSING_TOPICS)
    sys_prompt = SELLER_SYSTEM_TMPL.format(catalog=text_cat)

    msgs = [{"role": "system", "content": sys_prompt}]
    # نص المحادثات متعدد الأدوار: سؤال سعر مجاوب من الكتالوج ثم سؤال المعلومة الناقصة
    if random.random() < 0.6:
        msgs.append({"role": "user", "content": random.choice(ASK_TEMPLATES).format(p=p1)})
        msgs.append({"role": "assistant", "content": random.choice(SELLER_PRICE).format(p=p1, price=price1)})
        msgs.append({"role": "user", "content": "زين، " + random.choice(questions)})
    else:
        msgs.append({"role": "user", "content": f"هلا، بخصوص {p1}، " + random.choice(questions)})
    msgs.append({"role": "assistant", "content": random.choice(CONFIRM_LATER_REPLIES)})

    return {
        "messages": msgs,
        "category": "confirm_later_missing_info",
        "dialect": "iraqi",
        "source_file": "generate_v6_extras.py",
    }


# ============================================================
# 4) تكرار السؤال مرتين — الرد الثاني ثابت ومتسق (AA.md قسم 2.5)
# ============================================================
REPEAT_PREFIX = ["", "ها، ", "عيني ما سمعتك، ", "شلون يعني؟ ", "أكيد؟ "]
CONSIST_PRICE = ["نفس ما گتلك عيني، {p} بـ{price} دينار", "گتلك قبل شوية، {p} سعره {price} دينار",
                 "هو نفسه، {p} بـ{price} دينار ما تغير"]
CONSIST_PRICE_F = ["نفس ما گتلج خيتي، {p} بـ{price} دينار", "گتلج قبل شوية، {p} سعره {price} دينار"]
REJECT_FIRST = ["والله هذا ماكو عدنا هسه", "ماكو عدنا هسه والله"]
CONSIST_REJECT = ["گتلك عيني، ماكو عدنا هسه", "نفس الجواب، والله ماكو عدنا هسه", "لا عيني ماكو، مثل ما گتلك"]
CONSIST_REJECT_F = ["گتلج خيتي، ماكو عدنا هسه", "نفس الجواب، والله ماكو عدنا هسه"]


def missing_product(catalog_items):
    """منتج من فئة أخرى بالبنك غير موجود بكتالوج هذا المثال."""
    names = {n for n, _ in catalog_items}
    while True:
        cat = random.choice(list(BANK))
        pname, meta = random.choice(list(BANK[cat].items()))
        full = " ".join(f"{pname} {random.choice(meta['brands'])}".split())
        if all(pname not in n for n in names):
            return full


def gen_repeat_question():
    text_cat, items = build_catalog()
    sys_prompt = SELLER_SYSTEM_TMPL.format(catalog=text_cat)
    female = random.random() < 0.3
    msgs = [{"role": "system", "content": sys_prompt}]

    if random.random() < 0.6:
        # سؤال سعر مكرر — نفس السعر بالجوابين حرفياً
        p1, price1 = random.choice(items)
        q = random.choice(ASK_TEMPLATES).format(p=p1)
        pool = SELLER_PRICE_F if female else SELLER_PRICE
        cons = CONSIST_PRICE_F if female else CONSIST_PRICE
        msgs.append({"role": "user", "content": q})
        msgs.append({"role": "assistant", "content": random.choice(pool).format(p=p1, price=price1)})
        msgs.append({"role": "user", "content": random.choice(REPEAT_PREFIX) + q})
        msgs.append({"role": "assistant", "content": random.choice(cons).format(p=p1, price=price1)})
    else:
        # رفض مكرر — ماكو بالجوابين، بلا ادعاء مخزون ولا وعود
        p_missing = missing_product(items)
        q = random.choice(["عندكم {p}؟", "اكو {p}؟", "تبيعون {p}؟"]).format(p=p_missing)
        cons = CONSIST_REJECT_F if female else CONSIST_REJECT
        msgs.append({"role": "user", "content": q})
        msgs.append({"role": "assistant", "content": random.choice(REJECT_FIRST)})
        msgs.append({"role": "user", "content": random.choice(REPEAT_PREFIX) + q})
        msgs.append({"role": "assistant", "content": random.choice(cons)})

    return {
        "messages": msgs,
        "category": "repeat_question_consistency",
        "dialect": "iraqi",
        "source_file": "generate_v6_extras.py",
    }


# ============================================================
def main():
    rows = (
        [gen_json_extraction() for _ in range(N_JSON_EXTRACT)]
        + [gen_tool_request() for _ in range(N_TOOL_REQUEST)]
        + [gen_tool_format() for _ in range(N_TOOL_FORMAT)]
        + [gen_confirm_later() for _ in range(N_CONFIRM_LATER)]
        + [gen_repeat_question() for _ in range(N_REPEAT_QUESTION)]
    )
    # فحص صيغة: كل رد JSON extraction لازم يبدأ بـ { وينتهي بـ } وقابل للتحليل
    for r in rows:
        if r["category"] == "json_extraction":
            a = r["messages"][-1]["content"]
            assert a.startswith("{") and a.endswith("}"), a[:50]
            parsed = json.loads(a)
            assert isinstance(parsed["items"][0]["quantity"], int)
            assert not any(ch.isdigit() for ch in parsed["confirmation_note"])
    random.shuffle(rows)
    n_val = int(len(rows) * VAL_FRACTION)
    val, train = rows[:n_val], rows[n_val:]
    with open("data/iraqi_extras_v6_train.jsonl", "w", encoding="utf-8") as f:
        for r in train:
            f.write(json.dumps(r, ensure_ascii=False) + "\n")
    with open("data/iraqi_extras_v6_val.jsonl", "w", encoding="utf-8") as f:
        for r in val:
            f.write(json.dumps(r, ensure_ascii=False) + "\n")
    print(f"extras train={len(train)}  val={len(val)}")
    from collections import Counter
    print(Counter(r["category"] for r in rows))


if __name__ == "__main__":
    main()
