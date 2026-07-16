# -*- coding: utf-8 -*-
"""
تنظيف وتقليص بيانات التدريب: v4 + v5  ->  v6

المشاكل المعالجة (مقاسة على البيانات الفعلية):
- 42.6% تكرار هياكل محادثات (نفس رسائل الزبون حرفياً)
- 3,344 محادثة مكررة 100% في v5
- 438 مثال validation موجودة حرفياً في train (تلوث يكذّب eval_loss)
- حجم مفرط (223 ألف مثال أحادي النمط = جرعة نسيان كارثي)

الناتج: ~50 ألف مثال متوازن -> data/iraqi_train_v6_part01..03.jsonl
        + data/iraqi_val_v6.jsonl (منظّف من التكرار والتلوث)
"""
import json
import glob
import hashlib
import random
import re
from collections import Counter, defaultdict

random.seed(42)

# ---------------- الأهداف ----------------
# سقف الأمثلة لكل فئة v4 (20 فئة × 1600 ≈ 32 ألف)
V4_CAP_PER_CATEGORY = 1600
# سقوف فئات v5 (الكتالوج المؤرضن) — نحافظ على تنوعها لكن نكسر هيمنة copy
V5_CAPS = {
    "grounded_catalog_copy": 7000,
    "grounded_catalog_reject": 4000,
    "grounded_catalog_memory": 2500,
    "grounded_catalog_resist": 2500,
    # فئات clarify والتحيات قليلة أصلاً — نأخذها كلها
}
V5_DEFAULT_CAP = 10**9
# أقصى تكرار لنفس هيكل رسائل الزبون
MAX_PER_SKELETON_V4 = 1   # v4: الهيكل المكرر لا يضيف شيئاً
MAX_PER_SKELETON_V5 = 3   # v5: نفس الأسئلة مع كتالوجات مختلفة = تعليم القراءة من السياق (مقصود)

NUM_RE = re.compile(r"\d{1,3}(?:,\d{3})+|\d{4,}")

# تعبيرات غير عراقية (خليجي/مصري/شامي) — ممنوعة بردود البائع حسب AA.md قسم 3
# القياس الفعلي: «لا يخالف» 320 مرة، «خالص» 313، «أبشر» 228 بردود v4/v5
DIALECT_LEAKS = [
    "لا يخالف", "يخالف عليك", "أبشر", "ابشر ", "طال عمرك", "يا طويل العمر",  # خليجي
    "إزيك", "ازيك", "خالص", "قوي جدا", "ايوه يا", "مافيش", "عايز",           # مصري
    "هلق", "منيح", "شو بدك", "بدك ", "كتير حلو", "لك شو",                     # شامي
]
# «شو» الشامية منفصلة (لا تلمس: شوية، شوف، شوكت، شوارب...)
SHU_RE = re.compile(r"(^|\s)شو(\s|؟|$)")

# AA.md قسم 2: ممنوع ادعاء مخزون/ندرة/وعود توفير بردود البائع
STOCK_CLAIMS = [
    "باقي حبتين", "باقي حبة", "مبيعة من", "انباعت", "خلصت من الأسبوع",
    "أوفرلك", "أدبرلك", "أوصيلك عليه", "أوصيلك عليها", "نوفره ", "راح يجينا", "يوصلنا قريب",
]


def load_jsonl(paths):
    rows = []
    for p in paths:
        with open(p, encoding="utf-8") as f:
            for line in f:
                line = line.strip()
                if line:
                    rows.append(json.loads(line))
    return rows


def conv_key(r):
    """بصمة المحادثة كاملة (للتكرار الحرفي والتلوث مع val)."""
    payload = json.dumps([(m["role"], m["content"]) for m in r["messages"]], ensure_ascii=False)
    return hashlib.md5(payload.encode()).hexdigest()


def skeleton_key(r):
    """بصمة رسائل الزبون فقط (لكشف القوالب المكررة)."""
    payload = json.dumps([m["content"] for m in r["messages"] if m["role"] == "user"], ensure_ascii=False)
    return hashlib.md5(payload.encode()).hexdigest()


def structure_ok(r):
    ms = r.get("messages") or []
    if not ms:
        return False
    core = [m for m in ms if m["role"] != "system"]
    if not core or core[0]["role"] != "user" or core[-1]["role"] != "assistant":
        return False
    for a, b in zip(core, core[1:]):
        if a["role"] == b["role"]:
            return False
    return all(isinstance(m.get("content"), str) and m["content"].strip() for m in ms)


def dialect_clean(r):
    """ردود البائع/الوكيل عراقية صافية — أي تعبير خليجي/مصري/شامي يسقط المثال.
    (كلام الزبون خارج الفحص — تنوعه واقعي ومقصود)"""
    for m in r["messages"]:
        if m["role"] != "assistant":
            continue
        for w in DIALECT_LEAKS + STOCK_CLAIMS:
            if w in m["content"]:
                return False
        if SHU_RE.search(m["content"]):
            return False
    return True


def numbers_grounded(r):
    """لأمثلة الكتالوج: كل رقم بردود البائع لازم يكون موجوداً حرفياً بالـ system prompt."""
    ms = r["messages"]
    if not ms or ms[0]["role"] != "system":
        return True  # بدون كتالوج — لا شيء نتحقق منه
    context = ms[0]["content"]
    for m in ms:
        if m["role"] != "assistant":
            # كلام الزبون وأرقام الهاتف وغيرها خارج الفحص، لكن نضيفها للسياق
            # حتى لا نرفض رداً يكرر رقماً ذكره الزبون نفسه
            context += "\n" + m["content"]
            continue
        for num in NUM_RE.findall(m["content"]):
            if num not in context:
                return False
        context += "\n" + m["content"]
    return True


def main():
    v4 = load_jsonl(sorted(glob.glob("data/iraqi_train_v4_part*.jsonl")))
    v5 = load_jsonl(sorted(glob.glob("data/iraqi_train_v5_part*.jsonl")))
    val = load_jsonl(["data/iraqi_val_v4.jsonl", "data/iraqi_val_v5.jsonl"])
    # القدرات الغائبة (استخراج JSON، أدوات، أتأكدلك) — ناتج generate_v6_extras.py
    extras = load_jsonl(sorted(glob.glob("data/iraqi_extras_v6_train.jsonl")))
    val += load_jsonl(sorted(glob.glob("data/iraqi_extras_v6_val.jsonl")))
    print(f"مدخلات: v4={len(v4)}  v5={len(v5)}  extras={len(extras)}  val={len(val)}")

    stats = Counter()

    # ---- 1) تنظيف val أولاً: بنية + تكرار داخلي ----
    val_clean, val_keys = [], set()
    for r in val:
        if not structure_ok(r):
            stats["val_bad_structure"] += 1
            continue
        if not dialect_clean(r):
            stats["val_dialect_leak"] += 1
            continue
        k = conv_key(r)
        if k in val_keys:
            stats["val_exact_dup"] += 1
            continue
        val_keys.add(k)
        val_clean.append(r)

    # ---- 2) تنظيف train: بنية + أرقام مؤرضنة + تكرار حرفي + استبعاد ما يطابق val ----
    def clean(rows, tag):
        out, seen = [], set()
        for r in rows:
            if not structure_ok(r):
                stats[f"{tag}_bad_structure"] += 1
                continue
            if not dialect_clean(r):
                stats[f"{tag}_dialect_leak"] += 1
                continue
            if not numbers_grounded(r):
                stats[f"{tag}_ungrounded_number"] += 1
                continue
            k = conv_key(r)
            if k in seen:
                stats[f"{tag}_exact_dup"] += 1
                continue
            if k in val_keys:
                stats[f"{tag}_val_leak"] += 1
                continue
            seen.add(k)
            out.append(r)
        return out

    v4, v5, extras = clean(v4, "v4"), clean(v5, "v5"), clean(extras, "extras")

    # ---- 3) كسر تكرار الهياكل (نفس أسئلة الزبون حرفياً) ----
    def dedup_skeleton(rows, max_per, tag):
        random.shuffle(rows)
        count, out = Counter(), []
        for r in rows:
            k = skeleton_key(r)
            if count[k] >= max_per:
                stats[f"{tag}_skeleton_dup"] += 1
                continue
            count[k] += 1
            out.append(r)
        return out

    v4 = dedup_skeleton(v4, MAX_PER_SKELETON_V4, "v4")
    v5 = dedup_skeleton(v5, MAX_PER_SKELETON_V5, "v5")
    extras = dedup_skeleton(extras, MAX_PER_SKELETON_V4, "extras")
    print(f"بعد التنظيف والتفريد: v4={len(v4)}  v5={len(v5)}  extras={len(extras)}")

    # ---- 4) موازنة الفئات وتقليص الحجم ----
    def cap_categories(rows, cap_fn, tag):
        by_cat = defaultdict(list)
        for r in rows:
            by_cat[r.get("category", "unknown")].append(r)
        out = []
        for cat, items in sorted(by_cat.items()):
            cap = cap_fn(cat)
            if len(items) > cap:
                items = random.sample(items, cap)
            out.extend(items)
            print(f"  [{tag}] {cat}: {len(items)}")
        return out

    print("\nتوزيع v4 النهائي:")
    v4 = cap_categories(v4, lambda c: V4_CAP_PER_CATEGORY, "v4")
    print("\nتوزيع v5 النهائي:")
    v5 = cap_categories(v5, lambda c: V5_CAPS.get(c, V5_DEFAULT_CAP), "v5")

    train = v4 + v5 + extras
    random.shuffle(train)
    print(f"\nإجمالي train v6: {len(train)}  (v4={len(v4)}, v5={len(v5)}, extras={len(extras)})")
    print(f"إجمالي val v6: {len(val_clean)}")
    print("\nإحصائيات الحذف:")
    for k, v in sorted(stats.items()):
        print(f"  {k}: {v}")

    # ---- 5) الكتابة: 3 أجزاء train + val ----
    n = len(train)
    thirds = [train[: n // 3], train[n // 3 : 2 * n // 3], train[2 * n // 3 :]]
    for i, part in enumerate(thirds, 1):
        path = f"data/iraqi_train_v6_part{i:02d}.jsonl"
        with open(path, "w", encoding="utf-8") as f:
            for r in part:
                f.write(json.dumps(r, ensure_ascii=False) + "\n")
        print(f"كتب {path}: {len(part)} سطر")
    with open("data/iraqi_val_v6.jsonl", "w", encoding="utf-8") as f:
        for r in val_clean:
            f.write(json.dumps(r, ensure_ascii=False) + "\n")
    print(f"كتب data/iraqi_val_v6.jsonl: {len(val_clean)} سطر")


if __name__ == "__main__":
    main()
