"""Generate v5 grounded-catalog training data (Iraqi Arabic).

Unlike v4 (free-form sales dialogue), every v5 example carries a "system"
message with a small product catalog (2-5 items, random prices/names drawn
from a combinatorial bank), and the assistant's reply is only allowed to
state names/prices/warranty that literally appear in that catalog. This
teaches copy-from-context behavior instead of memorizing/hallucinating
numbers.

Five patterns, mixed by ratio:
  1. copy    (50%) - customer asks about a catalog item, assistant quotes it verbatim
  2. reject  (20%) - customer asks for something NOT in the catalog
  3. resist  (10%) - customer names a brand not in the catalog; assistant
                     declines it and offers the catalog's actual item
  4. memory  (10%) - customer gives their name; assistant uses it while
                     answering from the catalog
  5. chat    (10%) - plain greetings/small talk, no catalog (sampled from
                     the existing curated greetings_smalltalk_only.jsonl)

Run:
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

RATIOS = {"copy": 0.50, "reject": 0.20, "resist": 0.10, "memory": 0.10, "chat": 0.10}

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

PERSONA_INTROS = [
    "أنت بائع عراقي.",
    "انت بياع بمحل عراقي.",
    "أنت بائع عراقي، تحچي بلهجة عراقية.",
    "أنت موظف مبيعات بمحل عراقي.",
    "انت بائع بسوق عراقي، ردودك مختصرة وبالعراقي.",
]

CATALOG_HEADERS = [
    "المتوفر حصراً:",
    "عدنا فقط:",
    "الموجود حالياً:",
    "قائمة الأسعار المتوفرة:",
    "الأصناف الموجودة بالمحل:",
]

GROUNDING_FOOTERS = [
    "انسخ الأسعار والأسماء حرفياً من القائمة. إذا طلب منتج مو موجود گله ماكو عدنا.",
    "لا تختلق أسعار أو منتجات غير موجودة بالقائمة. لو الزبون سأل عن شي مو مذكور گله ماكو عدنا هسه.",
    "استخدم فقط الأسماء والأسعار المذكورة أعلاه بالضبط. أي منتج مو بالقائمة جاوب ماكو عدنا.",
    "ممنوع تخترع سعر أو منتج غير موجود أعلاه. انسخ الأرقام والأسماء كما هي.",
]

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
    "أكيد، {name} بـ{price} دينار، ضمان {warranty}",
    "تفضل، {name} سعره {price} دينار، ضمان {warranty}",
]
A_ANSWER_NOWARR = [
    "إي عندنا {name} بـ{price} دينار",
    "{name} متوفر عدنا بـ{price} دينار",
    "أكيد، {name} بـ{price} دينار",
    "تفضل، {name} سعره {price} دينار",
]

Q_NEGOTIATE = ["ماكو أرخص؟", "ما تنزل شوية؟", "غالي شوي، تقدر تخفض؟", "آخر سعر شكد؟"]
A_HOLD_PRICE = [
    "هذا آخر سعر والله، بس البضاعة تستاهل",
    "ما أكدر أنزل أكثر من هيچي، هذا سعرنا الصافي",
    "والله ما بيه ربح كثير، ما أگدر أنزل",
    "هذا سعر مدروس، ما أكدر أعطيك أوطى من هيچي",
]

Q_WARRANTY = ["والضمان؟", "شكد الضمان؟", "أكو ضمان عليه؟"]
A_WARRANTY = ["ضمان {warranty} كامل", "عليه ضمان {warranty}", "{warranty} ضمان رسمي"]

REJECT_PHRASES = [
    "والله {plural} ماكو عدنا هسه",
    "ما أكو {plural} حالياً",
    "آسف، {plural} ما تتوفر عدنا بهاي الفترة",
    "لا، {plural} خلصت عدنا، ننتظر شحنة جديدة",
    "والله ما عدنا {plural} هسه",
    "{plural} مو موجودة حالياً، جرب تسأل الأسبوع الجاي",
    "عذراً، ما نبيع {plural}",
    "هذا الصنف ماكو عدنا خالص",
    "لا يخالف، بس {plural} مو من أصناف محلنا",
    "ماكو {plural} عدنا، بس عندنا بدائل زينة",
    "تأسف، نفذت الكمية من {plural}",
    "والله {plural} مو متوفرة، خلي أعرضلك شي ثاني",
    "لسه ما وصلتنا {plural}، بس تعال شوف الموجود",
]
REJECT_OFFER = [
    "بس أكو {name} بـ{price} دينار",
    "بس عندنا {name} بـ{price} دينار",
    "بس أگدر أعرضلك {name} بـ{price} دينار",
]

RESIST_PHRASES = [
    "{brand} ماكو عدنا، الموجود {name} بـ{price} دينار",
    "والله {brand} ما نجيب، بس عندنا {name} بجودة زينة بـ{price} دينار",
    "ما نتعامل بـ{brand}، أفضل شي عدنا {name} بـ{price} دينار",
    "{brand} مو متوفرة عدنا، جرب {name} بدلها بـ{price} دينار",
    "آسف، {brand} خارج تشكيلتنا، الموجود {name} بـ{price} دينار",
]
Q_BRAND_ASK = ["عندكم {brand}؟", "أريد {type} {brand}", "أكو {brand}؟", "تبيعون {brand}؟"]

GREET_PREFIX = ["هلو، ", "هلا، ", "السلام عليكم، ", "مساء الخير، ", ""]

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
    "تمام، توصيل لمنطقة {region} متوفر",
]

Q_CLOSING = ["ماشي، آخذه", "زين، اتفقنا", "خلص، بيه", "تمام، راح آخذه", "ماشي، هاي الفلوس"]
A_CLOSING = ["الله يعطيك العافية، تفضل", "ماشي، تكرم عينك", "الله يبارك فيك، تفضل بالسلامة", "زين، جاهزلك الفاتورة"]


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


def make_item(type_name, cfg, rng, exclude_brand=None):
    brands = [b for b in cfg["brands"] if b != exclude_brand] or cfg["brands"]
    brand = rng.choice(brands)
    spec = rng.choice(cfg["specs"])
    name = join_name(type_name, brand, spec)
    price = pick_price(cfg["price_range"], rng)
    warranty = rng.choice(cfg["warranty"]) if cfg["warranty"] else None
    return {"type": type_name, "brand": brand, "spec": spec, "name": name,
            "price": price, "warranty": warranty, "plural": cfg["plural"]}


def build_catalog(all_types, rng, k=None):
    k = k or rng.randint(2, 5)
    # keep one catalog within one plausible shop (single domain group).
    # Only roll among groups actually present in the (possibly
    # pre-filtered) input — rolling an absent group and falling back to
    # the full unfiltered input would silently mix unrelated shops.
    present_domains = {t[0] for t in all_types}
    candidate_groups = [g for g in DOMAIN_GROUPS if g & present_domains] or [present_domains]
    group = rng.choice(candidate_groups)
    pool = [t for t in all_types if t[0] in group]
    chosen_types = rng.sample(pool, min(k, len(pool)))
    items = [make_item(t, cfg, rng) for _, t, cfg in chosen_types]
    return items


def catalog_text(items, rng):
    lines = []
    for it in items:
        line = f"- {it['name']}: {fmt_price(it['price'])} دينار"
        if it["warranty"]:
            line += f"، ضمان {it['warranty']}"
        lines.append(line)
    return "\n".join(lines)


def build_system(items, rng):
    intro = rng.choice(PERSONA_INTROS)
    header = rng.choice(CATALOG_HEADERS)
    footer = rng.choice(GROUNDING_FOOTERS)
    return f"{intro}\n\n{header}\n" + catalog_text(items, rng) + f"\n\n{footer}"


def user_ask_item(item, rng):
    style = rng.choice(["generic", "type", "full"])
    prefix = rng.choice(GREET_PREFIX)
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
    items = build_catalog(all_types, rng)
    target = rng.choice(items)
    system = build_system(items, rng)
    messages = [{"role": "system", "content": system}]
    messages.append({"role": "user", "content": user_ask_item(target, rng)})
    messages.append({"role": "assistant", "content": assistant_answer_item(target, rng)})
    chain_followups(messages, items, target, rng)
    return messages, "grounded_catalog_copy"


def gen_reject(idx, bank, all_types, rng):
    items = build_catalog(all_types, rng)
    used_types = {it["type"] for it in items}
    candidates = [(d, t, c) for d, t, c in all_types if t not in used_types]
    if not candidates:
        candidates = all_types
    _, absent_type, absent_cfg = rng.choice(candidates)
    system = build_system(items, rng)
    messages = [{"role": "system", "content": system}]
    prefix = rng.choice(GREET_PREFIX)
    ask = rng.choice(Q_GENERIC).format(plural=absent_cfg["plural"])
    messages.append({"role": "user", "content": prefix + ask})
    reject = rng.choice(REJECT_PHRASES).format(plural=absent_cfg["plural"])
    offer_item = rng.choice(items)
    offer = rng.choice(REJECT_OFFER).format(name=offer_item["name"], price=fmt_price(offer_item["price"]))
    messages.append({"role": "assistant", "content": f"{reject}، {offer}"})
    chain_followups(messages, items, offer_item, rng)
    return messages, "grounded_catalog_reject"


def gen_resist(idx, all_types, rng):
    # brand-substitution only makes sense for domains with a real brand
    # concept (e.g. appliances) — not single-product domains like real
    # estate/food/services extracted from v4, which have brands=[""]
    branded_types = [(d, t, c) for d, t, c in all_types if len(c["brands"]) >= 2] or all_types
    domain, type_name, cfg = rng.choice(branded_types)
    catalog_item = make_item(type_name, cfg, rng)
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
    system = build_system(items, rng)
    messages = [{"role": "system", "content": system}]
    prefix = rng.choice(GREET_PREFIX)
    ask = rng.choice(Q_BRAND_ASK).format(brand=absent_brand, type=type_name)
    messages.append({"role": "user", "content": prefix + ask})
    reply = rng.choice(RESIST_PHRASES).format(brand=absent_brand, name=catalog_item["name"], price=fmt_price(catalog_item["price"]))
    messages.append({"role": "assistant", "content": reply})
    chain_followups(messages, items, catalog_item, rng)
    return messages, "grounded_catalog_resist"


def gen_memory(idx, all_types, rng):
    items = build_catalog(all_types, rng, k=rng.randint(2, 4))
    target = rng.choice(items)
    name = rng.choice(CUSTOMER_NAMES)
    system = build_system(items, rng)
    messages = [{"role": "system", "content": system}]
    intro_templates = [
        f"هلو، اسمي {name} وأدور {target['type']}",
        f"هلا، أني {name}، عندكم {target['plural']}؟",
        f"سلام، أني {name}، أريد {target['type']}",
    ]
    messages.append({"role": "user", "content": rng.choice(intro_templates)})
    greet_reply = [
        f"هلا {name}، عندنا {target['name']} بـ{fmt_price(target['price'])} دينار",
        f"أهلين {name}، إي أكو {target['name']} بـ{fmt_price(target['price'])} دينار",
    ]
    if target["warranty"]:
        greet_reply = [g + f"، ضمان {target['warranty']}" for g in greet_reply]
    messages.append({"role": "assistant", "content": rng.choice(greet_reply)})
    messages.append({"role": "user", "content": "زين، والضمان؟" if target["warranty"] else "زين، ما بيه خصم؟"})
    if target["warranty"]:
        followup = [f"{target['warranty']} كاملة {name}", f"ضمان {target['warranty']} يا {name}"]
    else:
        followup = [f"والله هذا آخر سعر {name}، بس البضاعة تستاهل", f"ما أكدر أنزل أكثر {name}، هذا السعر الصافي"]
    messages.append({"role": "assistant", "content": rng.choice(followup)})
    chain_followups(messages, items, target, rng, exclude={"warranty", "negotiate"})
    return messages, "grounded_catalog_memory"


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

    counts = {k: round(args.n * v) for k, v in RATIOS.items()}
    # fix rounding drift on the largest bucket
    drift = args.n - sum(counts.values())
    counts["copy"] += drift

    records = []
    counters = {k: 0 for k in RATIOS}

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
    for _ in range(counts["memory"]):
        msgs, cat = gen_memory(0, all_types, rng)
        records.append({"id": next_id("memory"), "category": cat, "dialect": "iraqi_arabic",
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
