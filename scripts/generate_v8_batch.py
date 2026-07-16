# -*- coding: utf-8 -*-
"""
دفعة v8 صغيرة مركزة — نفس مولدات وبوابات جودة v7 لكن بأعداد وأولويات جديدة:

1. ataakadlak_expanded   (200) — الأولوية القصوى: «أتأكدلك» بكتالوجات متنوعة، مع صفتين
                                  جديدتين: الأبعاد وبرامج الغسيل (كانتا ناقصتين من v7)
2. json_fixed_schema     (150) — JSON صارم بكميات مختلطة إجبارياً (~70% طلبات متعددة البنود
                                  بكميات مختلفة) + أمثلة تعديل الطلب
3. persistence_refusal   (100) — مقاومة الضغط: 50 إصرار على منتج غير متوفر (اكيد عندكم)
                                  + 50 ضغط خصم متكرر على منتج متوفر (نزللي السعر) —
                                  الثانية جديدة: v5 عندها مساومة بدور واحد فقط
4. praise_no_upsell       (50) — رد مدح بلا أي عرض بيعي
5. order_no_upsell        (50) — الزبون يطلب منتجاً والبائع يلبي بدون اقتراح إضافات

الناتج: data/iraqi_v8_batch_train.jsonl + data/iraqi_v8_batch_val.jsonl
"""
import json
import os
import random
import sys
from collections import Counter, defaultdict

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

import generate_v7_extras as v7  # noqa: E402
from generate_v7_extras import (  # noqa: E402
    gen_persistence, gen_ataakad, gen_json_fixed, gen_praise,
    gen_many, skeleton, check,
)
from generate_v6_extras import build_catalog, SELLER_SYSTEM_TMPL  # noqa: E402

random.seed(888)

N_ATAAKAD = 160
N_ATAAKAD_NEW = 40  # الأبعاد + برامج الغسيل
N_JSON = 150
N_PERSIST_MISSING = 50
N_PERSIST_HAGGLE = 50
N_PRAISE = 50
N_ORDER_NO_UPSELL = 50
VAL_FRACTION = 0.15
MIXED_QTY_TARGET = 0.7  # نسبة أمثلة JSON المطلوب فيها بندان+ بكميات مختلفة

# ---- الصفتان الناقصتان من v7: الأبعاد وبرامج الغسيل ----
# مولد مخصص (مو حقن بـ ATTRS العامة) حتى ترتبط الصفة بمنتج منطقي فقط:
# أبعاد -> أجهزة/أثاث، برامج غسيل -> غسالة/جلاية. الأرقام < 4 خانات فآمنة من فلتر التأريض.
DIM_KEYWORDS = ("ثلاجة", "فريزر", "غسالة", "جلاية", "مكيف", "طاولة", "تلفزيون", "دولاب",
                "كنبة", "سرير", "بوتاجاز", "مايكرويف", "فرن", "مبردة", "سبلت", "ميز")
WASH_KEYWORDS = ("غسالة", "جلاية")
NEW_ATTRS = {
    "الأبعاد": (DIM_KEYWORDS,
                ["شكد أبعاده؟", "قياساته شنو؟ يطب بمطبخي؟", "عرضه وطوله شكد؟",
                 "حجمه شگد يحتاج مساحة؟"],
                lambda: "الأبعاد " + random.choice(["60×60×85 سم", "55×60×145 سم", "70×75×180 سم"])),
    "برامج الغسيل": (WASH_KEYWORDS,
                     ["شكد برنامج غسيل بيه؟", "بيه برنامج غسيل سريع؟", "برامج الغسيل شنو عنده؟"],
                     lambda: random.choice(["14 برنامج غسيل منها سريع 15 دقيقة",
                                            "12 برنامج غسيل مع بخار",
                                            "16 برنامج غسيل منها صوف وستائر"])),
}


def gen_ataakad_new():
    """نفس منطق gen_ataakad بـ v7 لكن للصفتين الجديدتين وبمنتج منطقي للصفة حصراً."""
    attr = random.choice(list(NEW_ATTRS))
    kws, questions, info_fn = NEW_ATTRS[attr]
    match = []
    for _ in range(60):
        text_cat, items = build_catalog()
        match = [it for it in items if any(k in it[0] for k in kws)]
        if match:
            break
    if not match:
        return gen_ataakad()
    p1, price1 = random.choice(match)
    question = random.choice(questions)
    contrastive = random.random() < 0.2

    if contrastive:
        info = info_fn()
        text_cat = text_cat.replace(f"- {p1}: {price1} دينار", f"- {p1}: {price1} دينار ({info})")
        reply = random.choice(v7.COPY_PREFIX) + info
    else:
        reply = random.choice(v7.ATAAKAD_REPLIES)

    sys_prompt = SELLER_SYSTEM_TMPL.format(catalog=text_cat)
    msgs = [{"role": "system", "content": sys_prompt}]
    if random.random() < 0.6:
        msgs.append({"role": "user", "content": random.choice(v7.ASK_PRICE_FIRST).format(p=p1)})
        msgs.append({"role": "assistant",
                     "content": random.choice(v7.SELLER_PRICE_V7).format(p=p1, price=price1)})
        msgs.append({"role": "user", "content": "زين، و" + question})
    else:
        msgs.append({"role": "user", "content": f"هلا، بخصوص {p1}، " + question})
    msgs.append({"role": "assistant", "content": reply})

    return {"messages": msgs, "category": "ataakadlak_expanded",
            "dialect": "iraqi", "source_file": "generate_v8_batch.py"}


def _final_qtys(r):
    """كميات آخر كتلة JSON برد البائع (المصدر الموثوق بعد أي تعديل)."""
    for m in reversed(r["messages"]):
        if m["role"] == "assistant" and "{" in m["content"]:
            c = m["content"]
            obj = json.loads(c[c.index("{"): c.rindex("}") + 1])
            return [it["qty"] for it in obj["order"]["items"]]
    return []


def gen_json_mixed():
    """gen_json_fixed مع فرض الكميات المختلطة: ~70% من الأمثلة فيها بندان أو أكثر بكميات مختلفة."""
    want_mixed = random.random() < MIXED_QTY_TARGET
    r = gen_json_fixed()
    for _ in range(120):
        q = _final_qtys(r)
        if want_mixed:
            if len(q) >= 2 and len(set(q)) >= 2:
                return r
        elif q:
            return r
        r = gen_json_fixed()
    return r


# ============================================================
# ضغط الخصم المتكرر: الزبون يلح على تنزيل السعر والبائع يثبت
# (السعر الوحيد بردود البائع هو سعر الكتالوج حرفياً — لا رقم خصم مخترع)
# ============================================================
HAGGLE_ASK = ["هلا، شكد {p}؟", "بيش {p} عدكم؟", "مرحبا، سعر {p} شكد؟"]
HAGGLE_QUOTE = ["هلا بيك، {p} سعره {price} دينار", "حياك الله، {p} بـ{price} دينار",
                "تفضل عيني، {p} موجود بـ{price} دينار"]
HAGGLE_PRESSURE = {
    "expensive": ["غالي هواي، نزلي شوية", "لا والله غالي، خفض شوي", "هذا سعر عالي، سويلي أحسن سعر"],
    "competitor": ["المحل الثاني يبيعه أرخص منكم", "شفته بالسوق أرخص، نزلولي مثلهم",
                   "غيركم ينزل بالسعر، انتو ليش لا؟"],
    "loyal": ["آني زبون قديم عدكم، سويلي خصم", "دايماً أشتري منكم، ما يصير تنزلولي؟",
              "خاطر الزبائن القدامى، خلي بينا وبينك"],
    "last_price": ["زين آخر سعر شكد؟", "خلي آخر كلام، بيش تنطيه؟", "گلي آخر سعر وأحسمها"],
    "buy_now": ["نزلي وآخذه هسه فد مرة", "خفضلي وأدفع كاش حالاً", "لو تنزلي شوية أشتريه من هسه"],
}
HAGGLE_HOLD = [
    "والله هذا آخر سعر، بس البضاعة تستاهل",
    "ما أگدر أنزل عيني، هذا سعرنا الصافي",
    "سعرنا واحد للكل، ما نفرق بين زبون وزبون",
    "لو أگدر أنزل چان نزلتلك، بس صدگني هذا السعر الثابت",
    "والله ما بيه مجال، السعر هذا نهائي",
    "عيني السعر مدروس وما بيه ربح زايد، ما أگدر أخفض",
]
HAGGLE_HOLD_PRICE = [
    "سعره {price} دينار وهذا سعرنا الثابت، ما أگدر أنزل",
    "آخر سعر هو {price} دينار نفسه، ما بيه مجال",
]


def gen_haggle():
    text_cat, items = build_catalog()
    sys_prompt = SELLER_SYSTEM_TMPL.format(catalog=text_cat)
    p, price = random.choice(items)
    msgs = [{"role": "system", "content": sys_prompt},
            {"role": "user", "content": random.choice(HAGGLE_ASK).format(p=p)},
            {"role": "assistant", "content": random.choice(HAGGLE_QUOTE).format(p=p, price=price)}]
    styles = random.sample(list(HAGGLE_PRESSURE), random.randint(2, 3))
    for i, style in enumerate(styles):
        msgs.append({"role": "user", "content": random.choice(HAGGLE_PRESSURE[style])})
        if style == "last_price" or (i == len(styles) - 1 and random.random() < 0.4):
            reply = random.choice(HAGGLE_HOLD_PRICE).format(price=price)
        else:
            reply = random.choice(HAGGLE_HOLD)
        msgs.append({"role": "assistant", "content": reply})
    return {"messages": msgs, "category": "persistence_refusal",
            "dialect": "iraqi", "source_file": "generate_v8_batch.py"}


# ============================================================
# تلبية الطلب بلا upselling: طلب منتج واحد -> تأكيد بدون اقتراح أي إضافة
# ============================================================
ORDER_ASK = ["هلا، أريد {p}", "مرحبا، ظمّلي {p}", "شلونكم، آخذ {p} من عدكم", "هلو، احجزلي {p}"]
ORDER_FULFIL = [
    "تم عيني، {p} سعره {price} دينار، دزلي عنوانك ورقمك",
    "حاضر، سجلتلك {p} بـ{price} دينار، ننطرك بالمحل أو نوصله",
    "تدلل، {p} جاهز إلك بـ{price} دينار",
    "خوش، ثبتلك {p} بسعر {price} دينار، شلون تحب تستلمه؟",
]
UPSELL_PHRASES = ["تحب هم", "أنصحك", "اكو هم عدنا", "ضيفلك", "وياه ياخذون", "ما تاخذ وياه",
                  "عرض خاص", "يمشي وياه", "أكمللك"]


def gen_order_no_upsell():
    text_cat, items = build_catalog()
    sys_prompt = SELLER_SYSTEM_TMPL.format(catalog=text_cat)
    p, price = random.choice(items)
    msgs = [{"role": "system", "content": sys_prompt},
            {"role": "user", "content": random.choice(ORDER_ASK).format(p=p)},
            {"role": "assistant", "content": random.choice(ORDER_FULFIL).format(p=p, price=price)}]
    return {"messages": msgs, "category": "order_no_upsell",
            "dialect": "iraqi", "source_file": "generate_v8_batch.py"}


def order_no_upsell_clean(r):
    """رد التلبية: لا اسم منتج آخر من الكتالوج ولا عبارة عرض إضافي."""
    import re
    sys_content = r["messages"][0]["content"]
    ordered = None
    for m in r["messages"]:
        if m["role"] == "user":
            ordered = m["content"]
    names = re.findall(r"^- (.+?): [\d,]+ دينار", sys_content, re.M)
    reply = r["messages"][-1]["content"]
    if any(ph in reply for ph in UPSELL_PHRASES):
        return False
    return not any(n in reply and n not in ordered for n in names)


def gen_many_extra(fn, n, tag, rejects, extra_check):
    """مثل gen_many لكن بفحص إضافي خاص بالفئة."""
    out, skels = [], Counter()
    attempts = 0
    while len(out) < n and attempts < n * 40:
        attempts += 1
        r = fn()
        why = check(r)
        if why is None and not extra_check(r):
            why = "extra"
        if why:
            rejects[f"{tag}/{why}"] += 1
            continue
        k = skeleton(r)
        if skels[k] >= 3:
            rejects[f"{tag}/skeleton_dup"] += 1
            continue
        skels[k] += 1
        out.append(r)
    return out


def main():
    rejects = Counter()
    rows = (
        gen_many(gen_ataakad, N_ATAAKAD, "ataakad", rejects)
        + gen_many(gen_ataakad_new, N_ATAAKAD_NEW, "ataakad_new", rejects)
        + gen_many(gen_json_mixed, N_JSON, "json", rejects)
        + gen_many(gen_persistence, N_PERSIST_MISSING, "persistence", rejects)
        + gen_many_extra(gen_haggle, N_PERSIST_HAGGLE, "haggle", rejects, lambda r: True)
        + gen_many(gen_praise, N_PRAISE, "praise", rejects)
        + gen_many_extra(gen_order_no_upsell, N_ORDER_NO_UPSELL, "order", rejects, order_no_upsell_clean)
    )
    for r in rows:
        r["source_file"] = "generate_v8_batch.py"

    # تقسيم 85/15 على مستوى هيكل المحادثة — بلا تسريب بين الطرفين
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

    train_path = os.path.join(ROOT, "data", "iraqi_v8_batch_train.jsonl")
    val_path = os.path.join(ROOT, "data", "iraqi_v8_batch_val.jsonl")
    with open(train_path, "w", encoding="utf-8") as f:
        for r in train:
            f.write(json.dumps(r, ensure_ascii=False) + "\n")
    with open(val_path, "w", encoding="utf-8") as f:
        for r in val:
            f.write(json.dumps(r, ensure_ascii=False) + "\n")

    print(f"إجمالي: train={len(train)}  val={len(val)}")
    print("\nحسب الفئة:")
    for split_name, split in (("train", train), ("val", val)):
        c = Counter(r["category"] for r in split)
        print(f"  {split_name}: " + "  ".join(f"{k}={v}" for k, v in sorted(c.items())))

    mixed = sum(1 for r in rows if r["category"] == "json_fixed_schema"
                and len(set(_final_qtys(r))) >= 2 and len(_final_qtys(r)) >= 2)
    n_json = sum(1 for r in rows if r["category"] == "json_fixed_schema")
    print(f"\nكميات مختلطة بفئة JSON: {mixed}/{n_json}")

    print("\nالمرفوضون (السبب/العدد):")
    for k, v in sorted(rejects.items()):
        print(f"  {k}: {v}")
    if not rejects:
        print("  لا شيء")

    print("\n================ عينات للمراجعة اليدوية (2 لكل فئة) ================")
    for cat in ("ataakadlak_expanded", "json_fixed_schema", "persistence_refusal",
                "praise_no_upsell", "order_no_upsell"):
        pool = [r for r in train if r["category"] == cat]
        print(f"\n########## {cat} ##########")
        for r in random.sample(pool, min(2, len(pool))):
            for m in r["messages"][1:]:
                print(f"  [{m['role']}] {m['content']}")
            print("  " + "-" * 50)


if __name__ == "__main__":
    main()
