"""Generate v5 grounded-catalog training data (Iraqi Arabic) — Category A/C.

Every v5 example carries a "system" message with a randomized product catalog
(3-6 items, prices/names drawn from a combinatorial bank) plus a services
block (delivery/install/discount) and a fixed "قواعد صارمة" rules block. The
assistant's reply is only ever allowed to state names/prices/warranty/service
numbers that literally appear in that system prompt — this teaches
copy-from-context behavior instead of memorizing/hallucinating numbers.

This module owns the shared building blocks (bank loading, catalog/services/
system-prompt construction, wordbank pools) reused by every other v5
generator (`generate_v5_clarify_data.py`, `generate_v5_memory_data.py`,
`generate_v5_drift_data.py`, `generate_v5_calc_data.py`,
`generate_v5_greet_data.py`), plus its own two categories:

  A. copy   - customer asks about catalog items, assistant quotes them verbatim
              across a deterministic ~10-turn arc (greeting -> 2-3 item price
              Qs -> comparison -> warranty -> negotiate -> delivery -> closing)
  C. reject - customer asks for something NOT satisfiable by the catalog, in
              one of three ways (off-catalog product / below price floor /
              off-topic entirely); the alternative offered is always computed
              as the catalog's actual cheapest item, never picked at random
  (brand-substitution "resist" is the other half of Category C)
  chat      - plain greetings/small talk, no catalog (sampled from the
              existing curated greetings_smalltalk_only.jsonl)

Run standalone (debug-only mix; the real build uses generate_v5.py):
    python generate_v5_grounded_data.py --n 20000
"""
import argparse
import json
import random
from pathlib import Path

ROOT = Path(__file__).parent
DATA_DIR = ROOT / "data"
BANK_PATH = DATA_DIR / "product_bank_v5.json"
GREETINGS_PATH = DATA_DIR / "greetings_smalltalk_only.jsonl"

CUSTOMER_NAMES = [
    "أبو حسن", "أبو علي", "أبو كرار", "أبو تراب", "أبو زيد", "أبو مصطفى",
    "أبو محمد", "أبو سجاد", "أم حسن", "أم علي", "أم زهراء", "أم إبراهيم",
    "أم كرار", "أم مصطفى", "حيدر", "سيف", "زينب", "رغد", "دعاء", "مصطفى",
    "أحمد", "علي", "فاطمة", "زهراء", "مريم", "عمار", "سارة", "نور",
]

FOREIGN_BRAND_POOL = [
    "سوني", "باناسونيك", "وايرلبول", "دايكن", "يورك", "فريجيدير",
    "ميتاگ", "هيتاچي", "بوش", "سيمنس", "اليكترولوكس", "شارپ", "فيليبس",
]

# ---- shop-domain labels for the system-prompt intro line ----
DOMAIN_SHOP_LABEL = {
    "تبريد": "مكيفات وتبريد",
    "غسيل": "غسالات ونشافات",
    "مطبخ": "أدوات مطبخ",
    "إلكترونيات": "إلكترونيات وموبايلات",
    "أثاث": "أثاث منزلي",
    "تنظيف_وتدفئة": "أدوات تنظيف وتدفئة",
    "خدمات": "صيانة وخدمات فنية",
    "مواد_غذائية": "مواد غذائية",
    "ملابس": "ملابس",
    "سيارات": "سيارات",
    "عقارات": "عقارات",
}

# ---- which services make sense per domain (you don't "install" a kilo of rice) ----
SERVICE_PROFILES = {
    "appliance": {"delivery": True, "install": True, "discount": True, "extra": None},
    "مواد_غذائية": {"delivery": True, "install": False, "discount": True, "extra": "توصيل خلال نفس اليوم"},
    "ملابس": {"delivery": True, "install": False, "discount": True, "extra": "استبدال خلال 3 أيام لو المقاس مو مناسب"},
    "سيارات": {"delivery": True, "install": False, "discount": False, "extra": "فحص فني مجاني قبل البيع"},
    "عقارات": {"delivery": False, "install": False, "discount": False, "extra": "نساعد بإجراءات التسجيل العقاري"},
}

NOTES_POOL = ["الكمية محدودة", "أحدث موديل", "متوفر بألوان متعددة", "الأكثر مبيعاً", "عرض لفترة محدودة"]

EXTRA_FLAVOR = [
    "دوامنا من الساعة 9 الصبح لين 9 الليل، كل يوم إلا الجمعة.",
    "نگبل الدفع نقد أو كارتة، وتقدر تدفع بالتقسيط لو حبيت.",
    "المحل بالسوق المركزي، قريب من الموقف العام.",
    "عدنا خدمة زبائن لأي استفسار حتى بعد البيع.",
]

STORE_STORY_LONG = [
    "المحل موجود بالسوق من أكثر من عشر سنين، وأغلب الزبائن يعرفونه بالاسم مباشرة.",
    "بلشنا المحل صغير وهسه توسعنا لصالة كاملة بسبب الإقبال الزين من الزبائن.",
    "المحل معروف بالمنطقة، وأغلب البضاعة تجينا مباشرة من الوكيل الرسمي.",
]

FAQ_BLOCK_LONG = (
    "أسئلة شائعة:\n"
    "- الدفع: نقبل نقد أو كارتة مصرفية، وتكدر تدفع بالتقسيط لأغلب المنتجات.\n"
    "- الدوام: من الساعة 9 الصبح لين 9 الليل، كل يوم إلا الجمعة نسكر الظهر.\n"
    "- الموقع: المحل بالسوق المركزي، قريب من الموقف العام وباب المحل لونه أزرق.\n"
    "- الإرجاع: تكدر ترجع المنتج خلال أسبوع لو بيه عيب من المصنع.\n"
    "- الفحص: كل البضاعة مفحوصة قبل ما تنزل للمعرض، ما نبيع شي مستعمل أو مجدد."
)

RULES_BLOCK = (
    "قواعد صارمة:\n"
    "1. جاوب باللهجة العراقية الأصيلة.\n"
    "2. جاوب قصير ومباشر، جملة أو جملتين بس.\n"
    "3. الأسعار والأرقام والماركات من القائمة أعلاه فقط.\n"
    "4. إذا الزبون طلب منتج مو بالقائمة، گله ماكو واعرض البديل.\n"
    "5. تذكر تفاصيل الزبون (اسمه، شنو يريد) واستعملها."
)

RULES_EXTRA_LONG = (
    "\n6. لو الزبون غاضب أو مستعجل، خليك هادئ ومختصر أكثر.\n"
    "7. اذكر التوصيل أو التركيب بس اذا الزبون سأل عنه.\n"
    "8. ما تعطي معلومات عن زبائن ثانين.\n"
    "9. لو طلب فاتورة، وجهه للكاشير مباشرة."
)

# ---- price question templates ----
Q_GENERIC = [
    "هلا، عندكم {plural}؟",
    "شنو عندكم من {plural}؟",
    "أدور {plural}، أكو عدكم؟",
    "عندكم {plural} زينة؟",
]
Q_TYPE = [
    "شكد سعر {type}؟",
    "بيش {type}؟",
    "عندكم {type}؟",
    "أريد {type}، شنو المتوفر؟",
]
Q_FULL = [
    "شكد سعر {name}؟",
    "بيش {name}؟",
    "عندكم {name}؟",
    "أريد أشتري {name}",
]

A_ANSWER_WARR = [
    "إي عندنا {name} بـ{price} دينار، ضمان {warranty}",
    "{name} متوفر عدنا بـ{price} دينار وعليه ضمان {warranty}",
    "اكو {name} بـ{price} دينار، ضمان {warranty}",
    "زين، تفضل، {name} سعره {price} دينار، ضمان {warranty}",
]
A_ANSWER_NOWARR = [
    "إي عندنا {name} بـ{price} دينار",
    "{name} متوفر عدنا بـ{price} دينار",
    "اكو {name} بـ{price} دينار",
    "زين، تفضل، {name} سعره {price} دينار",
]

Q_COMPARE = [
    "شنو الفرق بين {name_a} و{name_b}؟",
    "أيهم أحسن، {name_a} لو {name_b}؟",
    "شنو تنصحني، {name_a} أو {name_b}؟",
]
A_COMPARE = [
    "زين، {name_a} بـ{price_a} و{name_b} بـ{price_b}",
    "الفرق بالسعر بس، {name_a} بـ{price_a} و{name_b} بـ{price_b}",
    "بس فرق بالسعر، {name_a} بـ{price_a} و{name_b} بـ{price_b}",
]

Q_STOCK = ["أكو بالمخزن هسه؟", "متوفر حالياً؟", "أكدر آخذه اليوم؟"]
A_STOCK = ["إي أكو بالمخزن، تكدر تجيه اليوم", "متوفر عدنا، جاهز للتسليم", "إي، جاهز عدنا هسه"]

Q_NEGOTIATE = ["ماكو أرخص؟", "ما تنزل شوية؟", "غالي شوي، تقدر تخفض؟", "آخر سعر شكد؟"]
A_HOLD_PRICE = [
    "هذا آخر سعر والله، بس البضاعة تستاهل",
    "ما أكدر أنزل أكثر من هيچي، هذا سعرنا الصافي",
    "والله ما بيه ربح كثير، ما أگدر أنزل",
    "هذا سعر مدروس، ما أكدر أعطيك أوطى من هيچي",
]

Q_WARRANTY = ["والضمان؟", "شكد الضمان؟", "أكو ضمان عليه؟"]
A_WARRANTY = ["زين، ضمان {warranty} كامل", "اكو، عليه ضمان {warranty}", "{warranty} ضمان رسمي، تفضل"]

REJECT_PHRASES = [
    "والله {plural} ماكو عدنا هسه",
    "ما أكو {plural} حالياً",
    "آسف، {plural} ما تتوفر عدنا بهاي الفترة",
    "لا، {plural} خلصت عدنا، ننتظر شحنة جديدة",
    "والله ما عدنا {plural} هسه",
    "{plural} مو موجودة حالياً، جرب تسأل الأسبوع الجاي",
    "عذراً، ما نبيع {plural} هسه",
    "هذا الصنف ماكو عدنا خالص",
    "لا يخالف، بس {plural} مو من أصناف محلنا",
    "ماكو {plural} عدنا، بس عندنا بدائل زينة",
    "تأسف، نفذت الكمية من {plural} هسه",
    "والله {plural} مو متوفرة، خلي أعرضلك شي ثاني",
    "لسه ما وصلتنا {plural}، بس تعال شوف الموجود",
]
REJECT_OFFER = [
    "بس أكو {name} بـ{price} دينار",
    "بس عندنا {name} بـ{price} دينار",
    "بس أگدر أعرضلك {name} بـ{price} دينار",
]

Q_PRICE_FLOOR = ["أكو شي بـ{n} ألف؟", "عندكم شي أرخص من {n} ألف؟", "أريد شي رخيص، بـ{n} ألف يصير؟"]
A_PRICE_FLOOR = [
    "ماكو بهالسعر، بس أرخص شي عدنا {name} بـ{price} دينار",
    "والله ماكو أوطى من هيچي، أرخص موجود عدنا {name} بـ{price} دينار",
    "ما وصلنا بهالسعر، أرخص شي عدنا {name} بـ{price} دينار",
]

OFFTOPIC_POOL = [
    ("سيارات", "تبيعون سيارات؟"),
    ("عقارات", "عندكم بيوت للبيع؟"),
    ("مواد_غذائية", "عندكم لحم غنم؟"),
    ("ملابس", "عندكم عبايات نسائية؟"),
    ("طبي", "تسوون فحص طبي؟"),
    ("تعليم", "تدرسون دروس خصوصية؟"),
]
A_OFFTOPIC = ["لا والله، هذا مو من اختصاصنا", "آسف، ما نسوي هيچي هنا", "لا يخالف بس هذا مو عدنا خالص"]

RESIST_PHRASES = [
    "{brand} ماكو عدنا، الموجود {name} بـ{price} دينار",
    "والله {brand} ما نجيب، بس عندنا {name} بجودة زينة بـ{price} دينار",
    "ما نتعامل بـ{brand}، أفضل شي عدنا {name} بـ{price} دينار",
    "{brand} مو متوفرة عدنا، جرب {name} بدلها بـ{price} دينار",
    "آسف، {brand} مو موجودة عدنا، الموجود {name} بـ{price} دينار",
]
Q_BRAND_ASK = ["عندكم {brand}؟", "أريد {type} {brand}", "أكو {brand}؟", "تبيعون {brand}؟"]

GREET_PREFIX = ["هلو، ", "هلا، ", "السلام عليكم، ", "مساء الخير، ", ""]
GREET_OPEN = ["مرحبا", "السلام عليكم"]
GREET_OPEN_REPLY = ["وعليكم السلام، هلا وغلا", "هلا بيك، تفضل"]

# ---- follow-up scenes used to chain conversations into longer sessions ----
REGIONS = [
    "الكرادة", "المنصور", "الجادرية", "الكاظمية", "الأعظمية", "الحارثية",
    "الدورة", "الزعفرانية", "الشعلة", "حي الرشيد", "زيونة", "الغزالية",
]
Q_DELIVERY_ASK = ["توصلون البيت؟", "أكو توصيل؟", "تجيبونه لعندي؟", "توصلون لو أروح أستلم؟"]
A_DELIVERY_CLARIFY = [
    "إي نوصل، بس لأي منطقة تريد التوصيل؟",
    "أكيد نوصل، گلي وين منطقتك؟",
    "نوصل، بس خبرني المنطقة أول",
]
Q_REGION_ANSWER = ["{region}", "أني من {region}", "منطقتي {region}"]
A_DELIVERY_CONFIRM = [
    "إي نوصل لمنطقة {region} إن شاء الله",
    "ماكو مشكلة، نوصلها لمنطقة {region}",
    "زين، توصيل لمنطقة {region} متوفر",
]

Q_CLOSING = ["ماشي، آخذه", "زين، اتفقنا", "خلص، بيه", "تمام، راح آخذه", "ماشي، هاي الفلوس"]
A_CLOSING = ["الله يعطيك العافية، تفضل", "ماشي، تكرم عينك", "الله يبارك فيك، تسلم، تفضل بالسلامة", "زين، جاهزلك الفاتورة"]


def load_bank():
    with open(BANK_PATH, encoding="utf-8") as f:
        return json.load(f)


def flatten_types(bank):
    """[(domain, type_name, config), ...]"""
    out = []
    for domain, types in bank.items():
        for type_name, cfg in types.items():
            out.append((domain, type_name, cfg))
    return out


# domains that plausibly coexist in one shop's catalog. The original 6
# appliance-ish domains are a realistic Iraqi appliance megastore (plus
# repair "خدمات"); the domains extracted from v4 (food/clothes/cars/real
# estate) are each their own separate business and must not mix together
# or with appliances.
DOMAIN_GROUPS = [
    {"تبريد", "غسيل", "مطبخ", "إلكترونيات", "أثاث", "تنظيف_وتدفئة", "خدمات"},
    {"مواد_غذائية"},
    {"ملابس"},
    {"سيارات"},
    {"عقارات"},
]


def domain_group_of(domain):
    for group in DOMAIN_GROUPS:
        if domain in group:
            return group
    return {domain}


def round_price(n):
    return int(round(n / 1000.0)) * 1000


def fmt_price(n):
    return f"{n:,}"


def pick_price(price_range, rng):
    lo, hi = price_range
    return round_price(rng.randint(lo, hi))


def join_name(*parts):
    """Join type/brand/spec into a display name, collapsing blanks (some v5
    bank entries — e.g. single-product domains extracted from v4 — carry an
    empty brand or spec since there's no combinatorial variation)."""
    return " ".join(p for p in parts if p)


def make_item(type_name, cfg, rng, exclude_brand=None, domain=None):
    brands = [b for b in cfg["brands"] if b != exclude_brand] or cfg["brands"]
    brand = rng.choice(brands)
    spec = rng.choice(cfg["specs"])
    name = join_name(type_name, brand, spec)
    price = pick_price(cfg["price_range"], rng)
    warranty = rng.choice(cfg["warranty"]) if cfg["warranty"] else None
    return {"type": type_name, "brand": brand, "spec": spec, "name": name,
            "price": price, "warranty": warranty, "plural": cfg["plural"], "domain": domain}


def build_catalog(all_types, rng, k=None):
    k = k or rng.randint(3, 6)
    # keep one catalog within one plausible shop (single domain group).
    present_domains = {t[0] for t in all_types}
    candidate_groups = [g for g in DOMAIN_GROUPS if g & present_domains] or [present_domains]
    group = rng.choice(candidate_groups)
    pool = [t for t in all_types if t[0] in group]
    chosen_types = rng.sample(pool, min(k, len(pool)))
    items = [make_item(t, cfg, rng, domain=d) for d, t, cfg in chosen_types]
    return items


def catalog_text(items, rng, note_prob=0.3):
    lines = []
    for it in items:
        line = f"- {it['name']}: {fmt_price(it['price'])} دينار"
        if it["warranty"]:
            line += f"، ضمان {it['warranty']}"
        if rng.random() < note_prob:
            line += f"، {rng.choice(NOTES_POOL)}"
        lines.append(line)
    return "\n".join(lines)


def shop_label_of(items):
    domains = [it.get("domain") for it in items if it.get("domain")]
    if not domains:
        return "أدوات كهربائية ومنزلية"
    distinct = set(domains)
    if len(distinct) == 1:
        return DOMAIN_SHOP_LABEL.get(domains[0], domains[0])
    return "أدوات كهربائية ومنزلية"


def service_profile_for(items):
    domains = {it.get("domain") for it in items if it.get("domain")}
    for key in ("عقارات", "سيارات", "ملابس", "مواد_غذائية"):
        if key in domains:
            return SERVICE_PROFILES[key]
    return SERVICE_PROFILES["appliance"]


def build_services(rng, profile):
    """Returns (services_dict, rendered_text). services_dict carries the
    structured numbers (delivery fee, install fee, discount rate) so
    Category D/E generators can assert their assistant text reuses the exact
    same figures that appear in the system prompt."""
    services = {"delivery_fee": None, "install_fee": None, "discount_rate": None}
    lines = []
    if profile["delivery"]:
        if rng.random() < 0.35:
            services["delivery_fee"] = 0
            lines.append("توصيل مجاني للمحافظة")
        else:
            fee = round_price(rng.randint(10000, 40000))
            services["delivery_fee"] = fee
            lines.append(f"توصيل بـ{fmt_price(fee)} دينار")
    if profile["install"]:
        if rng.random() < 0.3:
            services["install_fee"] = 0
            lines.append("تركيب مجاني")
        else:
            fee = round_price(rng.randint(10000, 50000))
            services["install_fee"] = fee
            lines.append(f"تركيب بـ{fmt_price(fee)} دينار")
    if profile["discount"]:
        rate = rng.choice([3, 5, 10])
        services["discount_rate"] = rate
        lines.append(f"خصم {rate}% عند شراء قطعتين")
    if profile["extra"]:
        lines.append(profile["extra"])
    if not lines:
        lines.append("نتابع وياك بأي طلب خاص")
    text = "\n".join(f"- {l}" for l in lines)
    return services, text


def build_system(items, services_text, rng, shop_label=None, long=None):
    """Exact production-tested template:
        أنت بائع عراقي محترف بمحل {shop_label}.

        المنتجات المتوفرة حالياً (هذي القائمة حصراً، التزم بيها):
        {catalog}

        خدمات:
        {services}

        [قواعد صارمة numbered rules block]
    Token length naturally varies ~150-500 with catalog size (3-6 items);
    `long=True` (used by Category B) forces the upper 300-800 range via an
    extra flavor paragraph; `long=None` rolls it in ~30% of the time so every
    category sees some long-system-prompt examples, not just memory.
    """
    if long is None:
        long = rng.random() < 0.3
    shop_label = shop_label or shop_label_of(items)
    intro = f"أنت بائع عراقي محترف بمحل {shop_label}."
    note_prob = 0.85 if long else 0.3
    catalog_block = "المنتجات المتوفرة حالياً (هذي القائمة حصراً، التزم بيها):\n" + catalog_text(items, rng, note_prob=note_prob)
    services_block = "خدمات:\n" + services_text
    parts = [intro, catalog_block, services_block]
    if long:
        n_story = min(2, len(STORE_STORY_LONG))
        parts.append(" ".join(rng.sample(STORE_STORY_LONG, n_story)))
        parts.append(FAQ_BLOCK_LONG)
        parts.append(rng.choice(EXTRA_FLAVOR))
        parts.append(RULES_BLOCK + RULES_EXTRA_LONG)
    else:
        parts.append(RULES_BLOCK)
    return "\n\n".join(parts)


def user_ask_item(item, rng, no_prefix=False):
    style = rng.choice(["generic", "type", "full"])
    prefix = "" if no_prefix else rng.choice(GREET_PREFIX)
    if style == "generic":
        t = rng.choice(Q_GENERIC).format(plural=item["plural"])
    elif style == "type":
        t = rng.choice(Q_TYPE).format(type=item["type"])
    else:
        t = rng.choice(Q_FULL).format(name=item["name"])
    return prefix + t


def assistant_answer_item(item, rng):
    if item["warranty"]:
        t = rng.choice(A_ANSWER_WARR).format(name=item["name"], price=fmt_price(item["price"]), warranty=item["warranty"])
    else:
        t = rng.choice(A_ANSWER_NOWARR).format(name=item["name"], price=fmt_price(item["price"]))
    return t


_realestate_types = None


def is_realestate(item):
    """"region"/delivery scene makes no sense for property sales (you don't
    deliver an apartment) — check the item's type against the real-estate
    domain, lazily loaded once."""
    global _realestate_types
    if _realestate_types is None:
        try:
            _realestate_types = set(load_bank().get("عقارات", {}).keys())
        except Exception:
            _realestate_types = set()
    return item.get("type") in _realestate_types


def chain_followups(messages, items, chosen, rng, exclude=None):
    """Append 0-3 extra scenes (+ optional closing) to lengthen a session,
    reusing the catalog already injected in the system prompt — no new
    catalog, same context, just more turns for the model to track."""
    if rng.random() < 0.15:
        return messages  # keep some sessions short for distribution diversity

    exclude = set(exclude) if exclude else set()
    if is_realestate(chosen):
        exclude.add("region")
    pool = [s for s in ["negotiate", "warranty", "second_item", "region"] if s not in exclude]
    if not chosen.get("warranty"):
        pool = [s for s in pool if s != "warranty"]
    other_items = [it for it in items if it is not chosen]
    if not other_items:
        pool = [s for s in pool if s != "second_item"]
    if not pool:
        return messages

    n = rng.randint(1, min(3, len(pool)))
    for scene in rng.sample(pool, n):
        if scene == "negotiate":
            messages.append({"role": "user", "content": rng.choice(Q_NEGOTIATE)})
            messages.append({"role": "assistant", "content": rng.choice(A_HOLD_PRICE)})
        elif scene == "warranty":
            messages.append({"role": "user", "content": rng.choice(Q_WARRANTY)})
            messages.append({"role": "assistant", "content": rng.choice(A_WARRANTY).format(warranty=chosen["warranty"])})
        elif scene == "second_item":
            nxt = rng.choice(other_items)
            messages.append({"role": "user", "content": user_ask_item(nxt, rng)})
            messages.append({"role": "assistant", "content": assistant_answer_item(nxt, rng)})
        elif scene == "region":
            messages.append({"role": "user", "content": rng.choice(Q_DELIVERY_ASK)})
            messages.append({"role": "assistant", "content": rng.choice(A_DELIVERY_CLARIFY)})
            region = rng.choice(REGIONS)
            messages.append({"role": "user", "content": rng.choice(Q_REGION_ANSWER).format(region=region)})
            messages.append({"role": "assistant", "content": rng.choice(A_DELIVERY_CONFIRM).format(region=region)})

    if rng.random() < 0.6:
        messages.append({"role": "user", "content": rng.choice(Q_CLOSING)})
        messages.append({"role": "assistant", "content": rng.choice(A_CLOSING)})
    return messages


def gen_copy(idx, all_types, rng):
    """Category A: deterministic ~10-turn arc so every example walks the full
    greeting -> price Qs (2-3 items) -> comparison -> warranty -> negotiate ->
    delivery -> closing sequence the spec describes, instead of the old
    random 0-3-scene sampler."""
    items = build_catalog(all_types, rng)
    profile = service_profile_for(items)
    services, services_text = build_services(rng, profile)
    system = build_system(items, services_text, rng)
    messages = [{"role": "system", "content": system}]

    messages.append({"role": "user", "content": rng.choice(GREET_OPEN)})
    messages.append({"role": "assistant", "content": rng.choice(GREET_OPEN_REPLY)})

    n_targets = min(len(items), rng.choice([2, 2, 3]))
    targets = rng.sample(items, n_targets)
    for i, it in enumerate(targets):
        messages.append({"role": "user", "content": user_ask_item(it, rng, no_prefix=(i == 0))})
        messages.append({"role": "assistant", "content": assistant_answer_item(it, rng)})

    if len(targets) >= 2:
        a, b = targets[0], targets[1]
        # long car/real-estate names + 8-9 digit prices can push the reply
        # past the 60-token production-reply ceiling - skip the comparison
        # scene rather than risk an overlong turn.
        if len(a["name"]) + len(b["name"]) < 40:
            messages.append({"role": "user", "content": rng.choice(Q_COMPARE).format(name_a=a["name"], name_b=b["name"])})
            messages.append({"role": "assistant", "content": rng.choice(A_COMPARE).format(
                name_a=a["name"], price_a=fmt_price(a["price"]), name_b=b["name"], price_b=fmt_price(b["price"]))})

    target = targets[0]
    if target["warranty"] and rng.random() < 0.7:
        messages.append({"role": "user", "content": rng.choice(Q_WARRANTY)})
        messages.append({"role": "assistant", "content": rng.choice(A_WARRANTY).format(warranty=target["warranty"])})

    if rng.random() < 0.5:
        messages.append({"role": "user", "content": rng.choice(Q_STOCK)})
        messages.append({"role": "assistant", "content": rng.choice(A_STOCK)})

    messages.append({"role": "user", "content": rng.choice(Q_NEGOTIATE)})
    messages.append({"role": "assistant", "content": rng.choice(A_HOLD_PRICE)})

    if not is_realestate(target):
        messages.append({"role": "user", "content": rng.choice(Q_DELIVERY_ASK)})
        messages.append({"role": "assistant", "content": rng.choice(A_DELIVERY_CLARIFY)})
        region = rng.choice(REGIONS)
        messages.append({"role": "user", "content": rng.choice(Q_REGION_ANSWER).format(region=region)})
        messages.append({"role": "assistant", "content": rng.choice(A_DELIVERY_CONFIRM).format(region=region)})

    messages.append({"role": "user", "content": rng.choice(Q_CLOSING)})
    messages.append({"role": "assistant", "content": rng.choice(A_CLOSING)})

    return messages, "grounded_catalog_copy"


def gen_reject(idx, bank, all_types, rng):
    """Category C (product/price-floor/off-topic sub-modes). The alternative
    offered is always the catalog's actual cheapest item, computed here, not
    picked at random."""
    items = build_catalog(all_types, rng)
    profile = service_profile_for(items)
    services, services_text = build_services(rng, profile)
    system = build_system(items, services_text, rng)
    messages = [{"role": "system", "content": system}]
    cheapest = min(items, key=lambda it: it["price"])

    mode = rng.choices(["product", "price_floor", "offtopic"], weights=[0.4, 0.3, 0.3])[0]

    if mode == "product":
        used_types = {it["type"] for it in items}
        candidates = [(d, t, c) for d, t, c in all_types if t not in used_types]
        if not candidates:
            candidates = all_types
        _, absent_type, absent_cfg = rng.choice(candidates)
        prefix = rng.choice(GREET_PREFIX)
        ask = rng.choice(Q_GENERIC).format(plural=absent_cfg["plural"])
        messages.append({"role": "user", "content": prefix + ask})
        reject = rng.choice(REJECT_PHRASES).format(plural=absent_cfg["plural"])
        offer = rng.choice(REJECT_OFFER).format(name=cheapest["name"], price=fmt_price(cheapest["price"]))
        messages.append({"role": "assistant", "content": f"{reject}، {offer}"})
    elif mode == "price_floor":
        floor = max(10000, round_price(int(cheapest["price"] * rng.uniform(0.3, 0.8))))
        messages.append({"role": "user", "content": rng.choice(Q_PRICE_FLOOR).format(n=floor // 1000)})
        messages.append({"role": "assistant", "content": rng.choice(A_PRICE_FLOOR).format(
            name=cheapest["name"], price=fmt_price(cheapest["price"]))})
    else:  # offtopic
        present_domains = {it.get("domain") for it in items}
        candidates = [(tag, q) for tag, q in OFFTOPIC_POOL if tag not in present_domains]
        if not candidates:
            candidates = OFFTOPIC_POOL
        _, ask = rng.choice(candidates)
        messages.append({"role": "user", "content": ask})
        messages.append({"role": "assistant", "content": rng.choice(A_OFFTOPIC)})

    chain_followups(messages, items, cheapest, rng)
    return messages, f"grounded_catalog_reject_{mode}"


def gen_resist(idx, all_types, rng):
    # brand-substitution only makes sense for domains with a real brand
    # concept (e.g. appliances) — not single-product domains like real
    # estate/food/services extracted from v4, which have brands=[""]
    branded_types = [(d, t, c) for d, t, c in all_types if len(c["brands"]) >= 2] or all_types
    domain, type_name, cfg = rng.choice(branded_types)
    catalog_item = make_item(type_name, cfg, rng, domain=domain)
    # distractors are mandatory: sample only from *other* types, restricted
    # to the same domain group as the anchor item, so the catalog can never
    # collapse to a single item AND never mixes unrelated shops (a car next
    # to an AC) — see spec: "مشتّتات إلزامية"
    anchor_group = domain_group_of(domain)
    other_types = [t for t in all_types if t[1] != type_name and t[0] in anchor_group]
    k = rng.randint(1, min(3, len(other_types)))
    extra_items = build_catalog(other_types, rng, k=k)
    items = [catalog_item] + extra_items
    rng.shuffle(items)
    absent_candidates = [b for b in FOREIGN_BRAND_POOL if b not in cfg["brands"]] or FOREIGN_BRAND_POOL
    absent_brand = rng.choice(absent_candidates)
    profile = service_profile_for(items)
    services, services_text = build_services(rng, profile)
    system = build_system(items, services_text, rng)
    messages = [{"role": "system", "content": system}]
    prefix = rng.choice(GREET_PREFIX)
    ask = rng.choice(Q_BRAND_ASK).format(brand=absent_brand, type=type_name)
    messages.append({"role": "user", "content": prefix + ask})
    reply = rng.choice(RESIST_PHRASES).format(brand=absent_brand, name=catalog_item["name"], price=fmt_price(catalog_item["price"]))
    messages.append({"role": "assistant", "content": reply})
    chain_followups(messages, items, catalog_item, rng)
    return messages, "grounded_catalog_resist"


_greetings_pool = None


def gen_chat(idx, rng):
    global _greetings_pool
    if _greetings_pool is None:
        rows = []
        with open(GREETINGS_PATH, encoding="utf-8") as f:
            for line in f:
                line = line.strip()
                if line:
                    rows.append(json.loads(line))
        rng.shuffle(rows)
        _greetings_pool = rows
    row = _greetings_pool[idx % len(_greetings_pool)]
    return row["messages"], row.get("category", "greetings_chat")


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--n", type=int, default=20000, help="total examples to generate")
    ap.add_argument("--seed", type=int, default=42)
    ap.add_argument("--val-ratio", type=float, default=0.05)
    ap.add_argument("--out-train-prefix", default=str(DATA_DIR / "iraqi_train_v5_part"))
    ap.add_argument("--out-val", default=str(DATA_DIR / "iraqi_val_v5.jsonl"))
    ap.add_argument("--train-shards", type=int, default=3)
    args = ap.parse_args()

    rng = random.Random(args.seed)
    bank = load_bank()
    all_types = flatten_types(bank)

    ratios = {"copy": 0.55, "reject": 0.25, "resist": 0.10, "chat": 0.10}
    counts = {k: round(args.n * v) for k, v in ratios.items()}
    drift = args.n - sum(counts.values())
    counts["copy"] += drift

    records = []
    counters = {k: 0 for k in ratios}

    def next_id(pattern):
        counters[pattern] += 1
        return f"v5_{pattern}_{counters[pattern]:05d}"

    for _ in range(counts["copy"]):
        msgs, cat = gen_copy(0, all_types, rng)
        records.append({"id": next_id("copy"), "category": cat, "dialect": "iraqi_arabic",
                         "messages": msgs, "source_file": "generate_v5_grounded_data.py"})
    for _ in range(counts["reject"]):
        msgs, cat = gen_reject(0, bank, all_types, rng)
        records.append({"id": next_id("reject"), "category": cat, "dialect": "iraqi_arabic",
                         "messages": msgs, "source_file": "generate_v5_grounded_data.py"})
    for _ in range(counts["resist"]):
        msgs, cat = gen_resist(0, all_types, rng)
        records.append({"id": next_id("resist"), "category": cat, "dialect": "iraqi_arabic",
                         "messages": msgs, "source_file": "generate_v5_grounded_data.py"})
    for i in range(counts["chat"]):
        msgs, cat = gen_chat(i, rng)
        records.append({"id": next_id("chat"), "category": cat, "dialect": "iraqi_arabic",
                         "messages": msgs, "source_file": "generate_v5_grounded_data.py (sampled from greetings_smalltalk_only.jsonl)"})

    rng.shuffle(records)
    n_val = int(len(records) * args.val_ratio)
    val_records = records[:n_val]
    train_records = records[n_val:]

    import math
    shard_size = math.ceil(len(train_records) / args.train_shards)
    train_paths = []
    for i in range(args.train_shards):
        shard = train_records[i * shard_size:(i + 1) * shard_size]
        if not shard:
            continue
        path = f"{args.out_train_prefix}{i + 1:02d}.jsonl"
        with open(path, "w", encoding="utf-8") as f:
            for r in shard:
                f.write(json.dumps(r, ensure_ascii=False) + "\n")
        train_paths.append((path, len(shard)))

    with open(args.out_val, "w", encoding="utf-8") as f:
        for r in val_records:
            f.write(json.dumps(r, ensure_ascii=False) + "\n")

    print(f"total: {len(records)}  (train {len(train_records)} / val {len(val_records)})")
    print("by pattern:", counts)
    for path, n in train_paths:
        print(f"train -> {path} ({n} records)")
    print(f"val   -> {args.out_val}")


if __name__ == "__main__":
    main()
