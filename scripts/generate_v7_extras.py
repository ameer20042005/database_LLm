# -*- coding: utf-8 -*-
"""
توليد بيانات v7 — سد الفجوات السلوكية الثلاث المقاسة باختبار الإنتاج لموديل v6 + فئة رابعة ثانوية:

1. persistence_refusal   (3,000) — ثبات الرفض تحت إصرار الزبون (الفشل: انقلب البائع بعد الضغط)
2. ataakadlak_expanded   (2,500) — «أتأكدلك» لصفة غير مكتوبة + 20% تباينية (الصفة موجودة فتُنسخ)
3. json_fixed_schema     (3,000) — إخراج طلب JSON صالح بمخطط ثابت وأرقام صحيحة بدون فواصل
4. praise_no_upsell        (800) — رد على المدح بدون أي عرض بيعي أو رقم

المبدأ المعماري: الشخصية باللأوزان، الحقائق بالـ system prompt حصراً — كل رقم برد البائع
منسوخ من كتالوج المثال أو من كلام الزبون (استثناء: حسابات JSON بالفئة 3، تُتحقق حسابياً).

الفلاتر مستوردة من prepare_v6_data.py (لا تُعاد كتابتها)، والكتالوجات من بنك v5 عبر
generate_v6_extras.build_catalog. التقسيم train/val على مستوى هيكل المحادثة (85/15) بلا تسريب.

الناتج: data/iraqi_v7_extras_train.jsonl + data/iraqi_v7_extras_val.jsonl
"""
import json
import random
import re
from collections import Counter, defaultdict

import prepare_v6_data as p6
from generate_v6_extras import build_catalog, missing_product, QTY_WORDS, SELLER_SYSTEM_TMPL

random.seed(777)

N_PERSISTENCE = 3000
N_ATAAKAD = 2500
N_JSON = 3000
N_PRAISE = 800
VAL_FRACTION = 0.15
MAX_PER_SKELETON = 3

DUR_WORDS = ["سنتين", "سنة", "أشهر", "اشهر", "شهر", "أسبوع", "اسبوع", "أيام", "ايام", "يوم"]

# ============================================================
# الفئة 1: ثبات الرفض تحت الإصرار
# ============================================================
ASK_MISSING = ["هلا، عندكم {p}؟", "شلونكم، اكو {p}؟", "مرحبا، تبيعون {p}؟", "هلو، أدور على {p} عدكم؟"]

PRESSURE = {
    "false_cert": ["اكيد عندكم، شفته بالواجهة قبل أسبوع", "لا تگلي ماكو، آني شفته عندكم",
                   "اكيد اكو بالمخزن، دور زين"],
    "competitors": ["كل المحلات عدها، شلون انتو ماكو؟", "المحل اليم منكم عنده، انتو ليش لا؟",
                    "غريبة، كل السوق يبيعه غيركم"],
    "emotional": ["دخيلك محتاجه اليوم ضروري", "الله يخليك دبرلي ياه، عندي مناسبة باچر",
                  "أرجوك شوفلي حل، ما أگدر أنطر"],
    "price_trap": ["زين بيش تبيعه؟", "ماشي، بس گلي سعره شكد لو توفر؟", "بيش يطلع لو أخذته منكم؟"],
    "doubt": ["شلون محل كبير مثلكم ما عنده؟", "غريبة والله، محل معروف وماكو عنده؟",
              "يعني شلون ما عندكم؟ هذا شي أساسي"],
    "pay_more": ["ادفعلك زيادة بس دبرلي ياه", "خلي يكلف أكثر، المهم توفره", "أعطيك فوق السعر، بس جيبه"],
}

REFUSE_FIRST = ["والله هذا ماكو عدنا هسه", "ماكو عدنا هسه والله", "صدگ ماكو عدنا هسه"]
REFUSE_STAY = [
    "والله ما موجود عدنا هسه، صدگني",
    "صدگني لو عندي چان بعتلك ياه",
    "ما أگدر أوعدك بشي مو موجود عدنا",
    "والله ماكو، وما أحب أگلك اكو وأغشك",
    "عيني آني ما أبيع شي مو موجود، هذا مبدأ المحل",
    "اللي أگدر أسويه أتأكدلك إذا يتوفر وأخبرك",
]
# رد خاص لفخ السعر: طلب سعر لمنتج مرفوض — ممنوع اختلاق رقم
REFUSE_PRICE_TRAP = [
    "ما أگدر أگلك سعر لشي مو موجود عدنا",
    "والله ما عندي سعر إله لأنه أصلاً ماكو عدنا",
    "شلون أسعرلك شي مو موجود؟ إذا توفر أخبرك بسعره",
]
# رد خاص لعرض دفع أكثر
REFUSE_PAY_MORE = [
    "مو قضية فلوس عيني، الشي مو موجود عدنا أصلاً",
    "حتى لو تدفع ضعف، ما أگدر أبيعك شي ماكو",
]
REFUSE_ALT = ["، بس اكو عدنا {alt} بـ{price} دينار إذا يفيدك", "، والموجود عدنا {alt} بـ{price} دينار تحب تشوفه؟"]


def _missing_same_type(items):
    """منتج بنفس نوع أحد بنود الكتالوج لكن بماركة/مواصفة غير موجودة — البديل المنطقي هو بند الكتالوج."""
    from generate_v6_extras import BANK
    for _ in range(30):
        full, price = random.choice(items)
        for cat in BANK.values():
            for pname, meta in cat.items():
                if full.startswith(pname):
                    brand = random.choice(meta["brands"])
                    spec = random.choice(meta["specs"]) if meta.get("specs") else ""
                    cand = " ".join(f"{pname} {brand} {spec}".split())
                    if all(cand != n for n, _ in items):
                        return cand, (full, price)
    return None, (None, None)


def gen_persistence():
    text_cat, items = build_catalog()
    sys_prompt = SELLER_SYSTEM_TMPL.format(catalog=text_cat)
    msgs = [{"role": "system", "content": sys_prompt}]

    # AA.md قسم 2: البديل يُعرض فقط إذا منطقي فعلاً — نفس نوع المنتج بماركة/مواصفة أخرى.
    # 50% طلب نفس النوع (بديل مسموح)، 50% طلب من فئة أخرى (رفض نظيف بلا بديل).
    same_type = random.random() < 0.5
    if same_type:
        p_missing, (alt_name, alt_price) = _missing_same_type(items)
    else:
        p_missing, alt_name = None, None
    if p_missing is None:
        p_missing, alt_name = missing_product(items), None

    msgs.append({"role": "user", "content": random.choice(ASK_MISSING).format(p=p_missing)})
    first = random.choice(REFUSE_FIRST)
    alt_used = 0
    if alt_name and random.random() < 0.7:  # بديل ببعض الردود لا كلها
        first += random.choice(REFUSE_ALT).format(alt=alt_name, price=alt_price)
        alt_used += 1
    msgs.append({"role": "assistant", "content": first})

    n_pressure = random.randint(2, 4)
    styles = random.sample(list(PRESSURE), n_pressure)
    if random.random() < 0.5 and "price_trap" not in styles:  # الفخ الذي سقط فيه v6 — غطّه بكثافة
        styles[random.randrange(n_pressure)] = "price_trap"

    for style in styles:
        msgs.append({"role": "user", "content": random.choice(PRESSURE[style])})
        if style == "price_trap":
            reply = random.choice(REFUSE_PRICE_TRAP)
        elif style == "pay_more":
            reply = random.choice(REFUSE_PAY_MORE)
        else:
            reply = random.choice(REFUSE_STAY)
        if alt_name and alt_used < 1 and random.random() < 0.4:
            reply += random.choice(REFUSE_ALT).format(alt=alt_name, price=alt_price)
            alt_used += 1
        msgs.append({"role": "assistant", "content": reply})

    return {"messages": msgs, "category": "persistence_refusal",
            "dialect": "iraqi", "source_file": "generate_v7_extras.py"}


# ============================================================
# الفئة 2: «أتأكدلك» موسّعة على الصفات + أمثلة تباينية
# ============================================================
# (الوزن، أسئلة الزبون، معلومة الكتالوج للحالة التباينية)
ATTRS = {
    "الضمان": (25, ["الضمان شكد؟", "بيه ضمان؟ شگد مدته؟", "شنو ضمانه؟", "عليه ضمان لو لا؟"],
               lambda: "ضمان " + random.choice(["سنة", "سنتين", "6 أشهر"])),
    "التوصيل": (13, ["التوصيل شكد يكلف؟", "توصلون لمنطقتي؟ بيش؟", "بيش التوصيل عدكم؟"],
                lambda: "التوصيل داخل بغداد " + random.choice(["5,000", "10,000", "15,000"]) + " دينار"),
    "المنشأ": (10, ["منشؤه شنو؟", "صناعة وين هذا؟", "بلد الصنع شنو؟"],
               lambda: "منشأ " + random.choice(["تركي", "صيني", "كوري", "تايلندي"])),
    "الألوان": (10, ["شنو الألوان المتوفرة؟", "اكو منه لون ثاني؟", "الألوان شنو عدكم؟"],
                lambda: "الألوان المتوفرة: " + random.choice(["أبيض وأسود", "فضي ورصاصي", "أبيض بس"])),
    "التقسيط": (8, ["اكو تقسيط عدكم؟", "تسوون أقساط؟ شلون؟", "أگدر آخذه أقساط؟"],
                lambda: "اكو تقسيط " + random.choice(["6 أشهر", "12 شهر"]) + " بدون فوائد"),
    "قطع الغيار": (8, ["قطع غياره متوفرة؟", "إذا خرب، الصيانة وين؟", "اكو صيانة وقطع غيار إله؟"],
                   lambda: "قطع الغيار والصيانة متوفرة بالمحل"),
    "استهلاك الكهرباء": (8, ["استهلاكه للكهرباء شلون؟", "ياكل كهرباء هواي؟", "اقتصادي بالكهرباء لو لا؟"],
                         lambda: "استهلاك اقتصادي صنف A+"),
    "بضاعة جديدة": (9, ["شوكت توصلكم بضاعة جديدة؟", "متى تجيكم موديلات جديدة؟"],
                    lambda: "البضاعة الجديدة توصل كل خميس"),
    "الاستبدال": (9, ["أگدر أبدله إذا ما عجبني؟", "اكو استبدال عدكم؟", "شنو سياسة الاستبدال؟"],
                  lambda: "استبدال خلال أسبوع بشرط الكارتون"),
}

ATAAKAD_REPLIES = [
    "والله ما أعرف بالضبط، أتأكدلك وأرد عليك",
    "خلي أراجع وأخبرك",
    "ما أحب أگلك شي مو متأكد منه، أتأكدلك",
    "هاي مو مكتوبة عندي، أتأكدلك من الإدارة وأرد عليك",
    "صراحة لازم أتأكد أول، أتأكدلك وأرجعلك بالجواب",
    "ما عندي جواب أكيد هسه، أتأكدلك وأخبرك",
]
COPY_PREFIX = ["إي، ", "نعم عيني، ", "إي عيني، ", ""]

ASK_PRICE_FIRST = ["هلا، شكد {p}؟", "مرحبا عندكم {p}؟ شكد سعره؟", "بيش {p} عدكم؟"]
SELLER_PRICE_V7 = ["هلا بيك، {p} سعره {price} دينار", "حياك الله، اكو {p} بـ{price} دينار",
                   "تفضل، {p} موجود بـ{price} دينار"]

_ATTR_NAMES = list(ATTRS)
_ATTR_WEIGHTS = [ATTRS[a][0] for a in _ATTR_NAMES]


def gen_ataakad():
    text_cat, items = build_catalog()
    p1, price1 = random.choice(items)
    attr = random.choices(_ATTR_NAMES, weights=_ATTR_WEIGHTS)[0]
    _, questions, info_fn = ATTRS[attr]
    question = random.choice(questions)
    contrastive = random.random() < 0.2  # الصفة موجودة بالكتالوج → تُنسخ حرفياً

    if contrastive:
        info = info_fn()
        # نلحق المعلومة بسطر المنتج بالكتالوج
        text_cat = text_cat.replace(f"- {p1}: {price1} دينار", f"- {p1}: {price1} دينار ({info})")
        reply = random.choice(COPY_PREFIX) + info
    else:
        reply = random.choice(ATAAKAD_REPLIES)

    sys_prompt = SELLER_SYSTEM_TMPL.format(catalog=text_cat)
    msgs = [{"role": "system", "content": sys_prompt}]
    if random.random() < 0.6:  # متعدد الأدوار: سؤال سعر مجاوب ثم سؤال الصفة
        msgs.append({"role": "user", "content": random.choice(ASK_PRICE_FIRST).format(p=p1)})
        msgs.append({"role": "assistant", "content": random.choice(SELLER_PRICE_V7).format(p=p1, price=price1)})
        msgs.append({"role": "user", "content": "زين، و" + question})
    else:
        msgs.append({"role": "user", "content": f"هلا، بخصوص {p1}، " + question})
    msgs.append({"role": "assistant", "content": reply})

    return {"messages": msgs, "category": "ataakadlak_expanded",
            "dialect": "iraqi", "source_file": "generate_v7_extras.py"}


def duration_grounded(r):
    """فلتر الفئة 2 (نصي): أي مدة زمنية أو ادعاء ضمان برد البائع لازم يكون بنص كتالوج المثال."""
    sys_content = r["messages"][0]["content"]
    for m in r["messages"]:
        if m["role"] != "assistant":
            continue
        for w in DUR_WORDS:
            if w in m["content"] and w not in sys_content:
                return False
    return True


# ============================================================
# الفئة 3: استخراج JSON بمخطط ثابت
# ============================================================
JSON_SYSTEM_SUFFIX = """

عند تأكيد الزبون طلبه، أخرج الطلب بكتلة JSON واحدة بهذا المخطط بالضبط
(الأسعار والكميات أعداد صحيحة بدون فواصل آلاف وبدون تنصيص، وأسماء المنتجات كما بالقائمة حرفياً):
{"order": {"items": [{"product": "اسم المنتج", "qty": 1, "unit_price": 0}], "total": 0}}"""

QTY_WORDS_V7 = {1: QTY_WORDS[1], 2: QTY_WORDS[2] + ["زوج"], 3: QTY_WORDS[3], 4: QTY_WORDS[4]}
ORDER_LEAD = ["أريد {p}، {qw}", "ظمّلي {p} {qw}", "آخذ {p}، خلي {qw}"]
JSON_INTRO = ["تم، هذا طلبك:", "خوش، هذا طلبك:", "تدلل، سجلتلك الطلب:", "زين، صار طلبك:", ""]
CONFIRM_ORDER = ["تمام أكّد الطلب", "اي ثبّته", "زين سجّله", "اوكي أكده"]


def _order_json(order_items):
    total = sum(q * up for _, q, up in order_items)
    return json.dumps({"order": {"items": [
        {"product": p, "qty": q, "unit_price": up} for p, q, up in order_items
    ], "total": total}}, ensure_ascii=False)


def _json_reply(order_items, intro=None):
    intro = random.choice(JSON_INTRO) if intro is None else intro
    block = _order_json(order_items)
    return (intro + "\n" + block).strip()


def gen_json_fixed():
    text_cat, items = build_catalog(random.randint(4, 7))
    sys_prompt = SELLER_SYSTEM_TMPL.format(catalog=text_cat) + JSON_SYSTEM_SUFFIX
    msgs = [{"role": "system", "content": sys_prompt}]
    price_of = {n: int(p.replace(",", "")) for n, p in items}

    n_items = min(random.choices([1, 2, 3], weights=[50, 32, 18])[0], len(items))
    chosen = random.sample(items, n_items)
    order = []
    parts = []
    for name, price in chosen:
        qty = random.choices([1, 2, 3, 4], weights=[55, 27, 12, 6])[0]
        parts.append(random.choice(ORDER_LEAD).format(p=name, qw=random.choice(QTY_WORDS_V7[qty])))
        order.append((name, qty, price_of[name]))

    variant = random.choices(["simple", "edit", "unavailable"], weights=[60, 20, 20])[0]

    if variant == "unavailable":
        miss = missing_product(items)
        parts.append(random.choice(ORDER_LEAD).format(p=miss, qw=random.choice(QTY_WORDS_V7[1])))
        random.shuffle(parts)
        msgs.append({"role": "user", "content": "هلا، " + " و".join(parts)})
        intro = f"«{miss}» ماكو عدنا هسه، سجلتلك الباقي:"
        msgs.append({"role": "assistant", "content": _json_reply(order, intro=intro)})
    else:
        msgs.append({"role": "user", "content": "هلا، " + " و".join(parts)})
        if random.random() < 0.4:  # دور تأكيد وسيط
            msgs.append({"role": "assistant", "content": "تدلل، أأكد الطلب؟"})
            msgs.append({"role": "user", "content": random.choice(CONFIRM_ORDER)})
        msgs.append({"role": "assistant", "content": _json_reply(order)})

        if variant == "edit":  # تعديل الطلب وإعادة إخراج JSON كاملاً
            editable = [it for it in items if it[0] not in {n for n, _, _ in order}]
            edited = False
            if editable and (len(order) < 2 or random.random() < 0.5):
                # إضافة بند
                name, price = random.choice(editable)
                qty = random.choices([1, 2], weights=[70, 30])[0]
                msgs.append({"role": "user", "content": "وضيفلي هم " + random.choice(ORDER_LEAD).format(
                    p=name, qw=random.choice(QTY_WORDS_V7[qty]))})
                order.append((name, qty, price_of[name]))
                edited = True
            elif len(order) >= 2:
                # حذف بند
                removed = order.pop(random.randrange(len(order)))
                msgs.append({"role": "user", "content": f"لا عيني، شيل {removed[0]} من الطلب"})
                edited = True
            if edited:
                msgs.append({"role": "assistant", "content": _json_reply(order, intro="تم التعديل، هذا طلبك:")})

    return {"messages": msgs, "category": "json_fixed_schema",
            "dialect": "iraqi", "source_file": "generate_v7_extras.py"}


def order_json_valid(r):
    """بوابة الجودة الإلزامية للفئة 3: json.loads + total حسابياً + أسماء من الكتالوج + أعداد صحيحة."""
    sys_content = r["messages"][0]["content"]
    catalog_names = set(re.findall(r"^- (.+?): [\d,]+ دينار", sys_content, re.M))
    price_of = {n: int(p.replace(",", "")) for n, p in
                re.findall(r"^- (.+?): ([\d,]+) دينار", sys_content, re.M)}
    found_block = False
    for m in r["messages"]:
        if m["role"] != "assistant" or "{" not in m["content"]:
            continue
        found_block = True
        c = m["content"]
        try:
            obj = json.loads(c[c.index("{"): c.rindex("}") + 1])
        except Exception:
            return False
        if set(obj) != {"order"} or set(obj["order"]) != {"items", "total"}:
            return False
        total = 0
        for it in obj["order"]["items"]:
            if set(it) != {"product", "qty", "unit_price"}:
                return False
            if not (isinstance(it["qty"], int) and isinstance(it["unit_price"], int)):
                return False
            if it["product"] not in catalog_names or price_of[it["product"]] != it["unit_price"]:
                return False
            total += it["qty"] * it["unit_price"]
        if obj["order"]["total"] != total or not isinstance(obj["order"]["total"], int):
            return False
    return found_block


# ============================================================
# الفئة 4: الرد على المدح بدون عرض بيعي
# ============================================================
# مدخلات الزبون تُركَّب من (افتتاحية × جملة أساس × خاتمة) لتنويع هيكلي كافٍ
PRAISE_OPENERS = ["", "هلا، ", "والله ", "صدگ ", "عيني ", "أخي ", "حجي ", "أستاذ "]
PRAISE_BODIES = {
    "praise_after_buy": ["اشتريت من عدكم وعجبتني البضاعة هواي", "الغراض اللي أخذتها منكم طلعت ممتازة",
                         "البضاعة اللي اشتريتها خوش بضاعة", "الجهاز اللي أخذته منكم شغال ميه ميه",
                         "الأغراض وصلت سليمة وعجبت الأهل كلهم", "من اشتريت منكم وآني مرتاح للبضاعة"],
    "general_thanks": ["شكراً على التعامل الحلو", "تسلمون، خدمتكم حلوة", "ممنون منكم، تعاملكم راقي",
                       "أشكركم على الأمانة بالتعامل", "تعاملكم يفرّح، تسلمون"],
    "farewell": ["زين، فمان الله", "خلص، مع السلامة", "يالله بالعافية، أشوفكم على خير",
                 "أجازة طيبة، فمان الله", "توادعنا، الله وياكم"],
    "dua": ["الله يوفقكم ويرزقكم", "ربي يبارك بمحلكم", "الله يزيدها نعمة عليكم",
            "الله يوفق شغلكم ويبارك بيه", "ربي يحفظكم ويخلي محلكم عامر"],
}
PRAISE_CLOSERS = ["", "، شكراً", "، تسلمون", "، الله يخليكم", "، ممنون", " والله", "، عاشت ايدكم"]
PRAISE_REPLIES = {
    "praise_after_buy": ["تدلل عيني، بالعافية عليك", "فرحتنا هاي، خدمتك واجب", "الله يهنيك، منورنا دائماً",
                         "بالعافية عليك، ونحن بالخدمة"],
    "general_thanks": ["العفو عيني، هذا واجبنا", "تدلل، خدمتك شرف النا", "الله يخليك، منورنا"],
    "farewell": ["فمان الله عيني، بالخدمة دائماً", "مع السلامة، منورنا", "الله وياك، تشرفنا"],
    "dua": ["ويوفقك يا رب، تسلم", "آمين ويوفقك، الله يخليك", "تسلم عيني، ربي يحفظك"],
}


def gen_praise():
    text_cat, items = build_catalog()
    sys_prompt = SELLER_SYSTEM_TMPL.format(catalog=text_cat)
    kind = random.choice(list(PRAISE_BODIES))
    user_msg = random.choice(PRAISE_OPENERS) + random.choice(PRAISE_BODIES[kind]) + random.choice(PRAISE_CLOSERS)
    msgs = [{"role": "system", "content": sys_prompt},
            {"role": "user", "content": user_msg},
            {"role": "assistant", "content": random.choice(PRAISE_REPLIES[kind])}]
    return {"messages": msgs, "category": "praise_no_upsell",
            "dialect": "iraqi", "source_file": "generate_v7_extras.py"}


def praise_clean(r):
    """رد المدح: لا رقم ولا اسم منتج من الكتالوج."""
    sys_content = r["messages"][0]["content"]
    names = re.findall(r"^- (.+?): [\d,]+ دينار", sys_content, re.M)
    reply = r["messages"][-1]["content"]
    if any(ch.isdigit() for ch in reply):
        return False
    return not any(n in reply for n in names)


# ============================================================
# الفحص الموحد + حلقة التوليد مع إعادة المحاولة
# ============================================================
def check(r):
    """يرجع سبب الرفض أو None. الفلاتر العامة من prepare_v6_data + فحوصات الفئة."""
    if not p6.structure_ok(r):
        return "structure"
    if not p6.dialect_clean(r):
        return "dialect"
    cat = r["category"]
    if cat == "json_fixed_schema":
        if not order_json_valid(r):
            return "json"
    elif not p6.numbers_grounded(r):
        return "numbers"
    if cat == "ataakadlak_expanded" and not duration_grounded(r):
        return "duration"
    if cat == "persistence_refusal":
        # لا دور بائع يتراجع عن الرفض: أي ادعاء توفر للمنتج المرفوض ممنوع
        for m in r["messages"][2:]:
            if m["role"] == "assistant" and any(w in m["content"] for w in ("موجود طبعاً", "اكو عدنا ياه", "نورت المحل، موجود")):
                return "retreat"
    if cat == "praise_no_upsell" and not praise_clean(r):
        return "upsell"
    return None


def skeleton(r):
    return tuple(m["content"] for m in r["messages"] if m["role"] == "user")


def gen_many(fn, n, tag, rejects):
    out, skel_count, attempts = [], Counter(), 0
    while len(out) < n and attempts < n * 40:
        attempts += 1
        r = fn()
        reason = check(r)
        if reason:
            rejects[f"{tag}/{reason}"] += 1
            continue
        k = skeleton(r)
        if skel_count[k] >= MAX_PER_SKELETON:
            rejects[f"{tag}/skeleton_dup"] += 1
            continue
        skel_count[k] += 1
        out.append(r)
    return out


def main():
    rejects = Counter()
    rows = (
        gen_many(gen_persistence, N_PERSISTENCE, "persistence", rejects)
        + gen_many(gen_ataakad, N_ATAAKAD, "ataakad", rejects)
        + gen_many(gen_json_fixed, N_JSON, "json", rejects)
        + gen_many(gen_praise, N_PRAISE, "praise", rejects)
    )

    # تقسيم 85/15 على مستوى هيكل المحادثة — نفس تسلسل الأسئلة لا يظهر بالطرفين إطلاقاً
    groups = defaultdict(list)
    for r in rows:
        groups[skeleton(r)].append(r)
    keys = list(groups)
    random.shuffle(keys)
    val, train, target_val = [], [], int(len(rows) * VAL_FRACTION)
    for k in keys:
        (val if len(val) < target_val else train).extend(groups[k])
    random.shuffle(train)
    random.shuffle(val)

    with open("data/iraqi_v7_extras_train.jsonl", "w", encoding="utf-8") as f:
        for r in train:
            f.write(json.dumps(r, ensure_ascii=False) + "\n")
    with open("data/iraqi_v7_extras_val.jsonl", "w", encoding="utf-8") as f:
        for r in val:
            f.write(json.dumps(r, ensure_ascii=False) + "\n")

    # ---------------- التقرير النهائي ----------------
    print(f"إجمالي: train={len(train)}  val={len(val)}")
    print("\nحسب الفئة:")
    for split_name, split in (("train", train), ("val", val)):
        c = Counter(r["category"] for r in split)
        print(f"  {split_name}: " + "  ".join(f"{k}={v}" for k, v in sorted(c.items())))
    print("\nالمرفوضون (السبب/العدد):")
    for k, v in sorted(rejects.items()):
        print(f"  {k}: {v}")
    if not rejects:
        print("  لا شيء")
    print("\n================ عينات للمراجعة اليدوية (3 لكل فئة) ================")
    for cat in ("persistence_refusal", "ataakadlak_expanded", "json_fixed_schema", "praise_no_upsell"):
        pool = [r for r in train if r["category"] == cat]
        print(f"\n########## {cat} ##########")
        for r in random.sample(pool, 3):
            for m in r["messages"][1:]:
                print(f"  [{m['role']}] {m['content']}")
            print("  " + "-" * 50)


if __name__ == "__main__":
    main()
