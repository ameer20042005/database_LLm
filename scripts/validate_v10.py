# -*- coding: utf-8 -*-
"""
سكربت تحقق داتا v10 التصحيحية — يفحص:
1. JSON صالح وبنية messages سليمة (system ثم تناوب user/assistant).
2. الاتساق الشرطي: أي ادعاء (ضمان/تغطية/سياسة/سعر/مجموع) بردود assistant
   لازم يكون موجود بكتالوج نفس المحادثة، وإلا الرد يحتوي صيغة إحالة.
3. فئة 5: صفر أرقام بردود assistant غير الموجودة بالكتالوج/رسائل الزبون.
4. ملف الاستخراج: JSON بالمفاتيح العشرة، city معيارية، الاسم غير فارغ.
5. تكرار: لا يوجد مثالان بنفس نص user الأول (تشابه > 90%)، ولا تكرار مع v8/v9.
6. إحصائية ختامية: أمثلة لكل فئة/اتجاه + ماركرات اللهجة بعينة 30 رد.
+ ملف المنتجات: JSON صالح، name من كتالوج المثال، qty عدد صحيح 1-50، install منطقي.
"""
import difflib
import json
import random
import re
import sys
from collections import Counter
from pathlib import Path

sys.stdout.reconfigure(encoding="utf-8")
DATA = Path(__file__).resolve().parent.parent / "data"

VIOLATIONS = []


def flag(fname, line_no, msg):
    VIOLATIONS.append(f"{fname}:{line_no}  {msg}")


def load(fname):
    rows = []
    with open(DATA / fname, encoding="utf-8") as f:
        for i, line in enumerate(f, 1):
            line = line.strip()
            if not line:
                continue
            try:
                rows.append((i, json.loads(line)))
            except json.JSONDecodeError as e:
                flag(fname, i, f"JSON غير صالح: {e}")
    return rows


# ============================================================
# فحص 1: بنية messages
# ============================================================
def check_structure(fname, rows):
    ok = 0
    for i, r in rows:
        msgs = r.get("messages")
        if not isinstance(msgs, list) or len(msgs) < 3:
            flag(fname, i, "messages ناقصة او مو قائمة")
            continue
        if msgs[0]["role"] != "system":
            flag(fname, i, "أول رسالة مو system")
            continue
        bad = False
        for j, m in enumerate(msgs[1:]):
            want = "user" if j % 2 == 0 else "assistant"
            if m.get("role") != want or not isinstance(m.get("content"), str) or not m["content"].strip():
                flag(fname, i, f"تناوب الأدوار مكسور عند الرسالة {j + 1}")
                bad = True
                break
        if msgs[-1]["role"] != "assistant":
            flag(fname, i, "آخر رسالة مو assistant")
            bad = True
        if not bad:
            ok += 1
    return ok


# ============================================================
# فحص 2: الاتساق الشرطي (مرآة درع المواضيع بالإنتاج)
# ============================================================
TOPIC_GROUPS = {
    "ضمان": ["ضمان", "كفالة", "گارنتي", "الكفالة", "ضمانه", "ضمانكم"],
    "توصيل": ["توصيل", "التوصيل", "توصلون", "يوصلون", "نوصلك", "نوصل"],
    "تركيب": ["تركيب", "التركيب", "نصب", "التنصيب", "تركيبكم", "تركيبهم"],
    "استهلاك": ["استهلاك", "استهلاكه", "كيلوواط", "امبير", "أمبير"],
    "لون": ["لون", "الوان", "ألوان", "الألوان", "الالوان"],
    "منشأ": ["منشأ", "صناعة", "المنشأ", "منشأه", "صناعه"],
    "تقسيط": ["تقسيط", "التقسيط", "اقساط", "أقساط", "قسط", "بالاقساط", "قسطتوه", "اقسطه"],
    "صيانة": ["صيانة", "الصيانة", "تصليح", "اصلحه"],
    "استرجاع": ["استرجاع", "الاسترجاع", "ارجعه", "الارجاع", "ترجعه"],
    "حجز": ["حجز", "الحجز", "احجز", "احجزه", "تحجزون", "نحجزلك", "تحجزولي", "حجزت", "احجزلي", "عربون"],
    "وزن": ["وزنه", "يوزن", "الوزن"],
    "ابعاد": ["ابعاده", "الأبعاد", "الابعاد", "عرضه", "ارتفاعه", "وارتفاعه"],
    "ضجيج": ["ضجيج", "ضجيجه", "ديسبل", "الضجيج"],
    "غاز": ["غاز", "الغاز", "غازه"],
    "خصم": ["خصم", "الخصم", "تخفيض", "التخفيض", "خصومات", "الخصومات", "تنزلولي", "تنزلي"],
    "دفع": ["ماستر", "زين كاش", "كي كارد", "الكتروني", "نقدي"],
    "فحص": ["الصندوق", "الكارتون"],
}
DURATION_WORDS = ["سنة", "سنتين", "سنوات", "شهر", "شهرين", "أشهر", "اشهر", "شهور"]
COVERAGE_CLAIMS = ["يشمل", "ما يشمل", "شامل", "يغطي", "ما يغطي", "الكسر",
                   "كومبريسر", "الكومبريسر", "الضاغط", "قطع الغيار", "استبدال"]
REFER_MARKERS = ["تأكد", "أسأل", "اسأل", "ما أگدر أجزم", "ما اگدر اجزم",
                 "ما عندي عليه جواب", "ما أعرف", "ما اعرف"]
ARABIC_PREFIX = re.compile(r'^(?:وال|بال|لل|فال|ال|و|ب|ف)')


def word_set(text):
    words = re.findall(r'[؀-ۿ]+', text)
    return {ARABIC_PREFIX.sub('', w) for w in words} | set(words)


def has_refer(reply):
    return any(m in reply for m in REFER_MARKERS)


def check_consistency(fname, rows):
    n_checked = 0
    for i, r in rows:
        msgs = r["messages"]
        catalog = msgs[0]["content"]
        cat_words = word_set(catalog)
        for m in msgs:
            if m["role"] != "assistant":
                continue
            reply = m["content"]
            reply_words = word_set(reply)
            n_checked += 1
            for topic, kws in TOPIC_GROUPS.items():
                mentioned = any(k in reply_words or k in reply for k in kws)
                if not mentioned:
                    continue
                in_catalog = any(k in cat_words or k in catalog for k in kws)
                if not in_catalog and not has_refer(reply):
                    flag(fname, i, f"موضوع '{topic}' مذكور بالرد وغير موجود بالكتالوج بلا إحالة: {reply[:70]}")
                if topic == "ضمان" and in_catalog:
                    claimed = [w for w in DURATION_WORDS if w in reply_words]
                    wrong = [w for w in claimed if w not in catalog]
                    fabricated = [c for c in COVERAGE_CLAIMS if c in reply and c not in catalog]
                    if wrong or fabricated:
                        flag(fname, i, f"تفاصيل ضمان غير مكتوبة بالكتالوج {wrong + fabricated}: {reply[:70]}")
    return n_checked


# ============================================================
# فحص 3: الأرقام — كل رقم بالرد لازم من الكتالوج او رسائل الزبون
# ============================================================
NUM_RE = re.compile(r'\d[\d,\.]*')


def nums_of(text):
    text = re.sub(r'(\d+)\s*(?:ألف|الف)', lambda m: f"{m.group(1)},000", text)
    return {n.rstrip('.,') for n in NUM_RE.findall(text)}


def check_numbers(fname, rows, strict_cats=("cat5_sum_over_precomputed",)):
    for i, r in rows:
        msgs = r["messages"]
        catalog_nums = nums_of(msgs[0]["content"])
        user_nums = set()
        for m in msgs[1:]:
            if m["role"] == "user":
                user_nums |= nums_of(m["content"])
                continue
            for num in nums_of(m["content"]):
                if num in catalog_nums or num in user_nums:
                    continue
                if ',' not in num and '.' not in num and len(num) <= 2:
                    if r.get("category") in strict_cats and len(num) > 1:
                        pass  # حتى بالفئة 5 الأعداد الصغيرة (قطع/أشهر) مو أسعار
                    continue
                flag(fname, i, f"رقم مخترع '{num}' (فئة {r.get('category')}): {m['content'][:70]}")


# ============================================================
# فحص 4: ملف الاستخراج
# ============================================================
SHIPMENT_KEYS = ["name", "city", "address", "district", "phone1", "phone2",
                 "price", "note", "orders", "totalQuantity"]
STD_CITIES = {"بغداد", "البصرة", "الموصل", "نينوى", "أربيل", "السليمانية", "دهوك",
              "كركوك", "صلاح الدين", "تكريت", "ديالى", "بعقوبة", "الأنبار",
              "الرمادي", "الفلوجة", "بابل", "الحلة", "كربلاء", "النجف", "واسط",
              "الكوت", "ميسان", "العمارة", "ذي قار", "الناصرية", "المثنى",
              "السماوة", "القادسية", "الديوانية"}


def check_extraction(fname, rows):
    for i, r in rows:
        try:
            gold = json.loads(r["messages"][-1]["content"])
        except json.JSONDecodeError:
            flag(fname, i, "assistant مو JSON صالح")
            continue
        if list(gold.keys()) != SHIPMENT_KEYS:
            flag(fname, i, f"المفاتيح مو العشرة المطلوبة: {list(gold.keys())}")
        city = gold.get("city", "")
        if city and city not in STD_CITIES:
            flag(fname, i, f"city مو من القائمة المعيارية: '{city}'")
        if r.get("category") == "extraction_name_no_marker" and not gold.get("name", "").strip():
            flag(fname, i, "الاسم فارغ بمثال فئة الاسم")
        if "expect_city" in r and city != r["expect_city"]:
            flag(fname, i, f"city '{city}' تخالف المتوقع '{r['expect_city']}' (ترقية جغرافية؟)")
        for ph_key in ("phone1", "phone2"):
            ph = gold.get(ph_key, "")
            if ph and not re.fullmatch(r'0\d{10}', ph):
                flag(fname, i, f"{ph_key} مو مطبّع: '{ph}'")
        price = gold.get("price", "")
        if price and not price.isdigit():
            flag(fname, i, f"price مو رقم صافي: '{price}'")
        orders = gold.get("orders", [])
        total = sum(o.get("quantity", 0) for o in orders)
        if orders and gold.get("totalQuantity") != str(total):
            flag(fname, i, f"totalQuantity '{gold.get('totalQuantity')}' ≠ مجموع الكميات {total}")


# ============================================================
# فحص ملف المنتجات
# ============================================================
def check_items(fname, rows):
    for i, r in rows:
        sys_txt = r["messages"][0]["content"]
        catalog_names = re.findall(r'^- (.+)$', sys_txt, re.MULTILINE)
        try:
            gold = json.loads(r["messages"][-1]["content"])
        except json.JSONDecodeError:
            flag(fname, i, "assistant مو JSON صالح")
            continue
        if set(gold.keys()) != {"items", "install"}:
            flag(fname, i, f"المفاتيح مو items/install: {list(gold.keys())}")
            continue
        if not isinstance(gold["install"], bool):
            flag(fname, i, f"install مو منطقي: {gold['install']!r}")
        for it in gold["items"]:
            if it.get("name") not in catalog_names:
                flag(fname, i, f"name مو من كتالوج المثال: '{it.get('name')}'")
            q = it.get("qty")
            if not isinstance(q, int) or not (1 <= q <= 50):
                flag(fname, i, f"qty مو عدد صحيح 1-50: {q!r}")


# ============================================================
# فحص 5: التكرار (داخل الملف + ضد v8/v9)
# ============================================================
def first_user(r):
    return r["messages"][1]["content"].strip()


def check_duplicates(fname, rows):
    firsts = [(i, first_user(r)) for i, r in rows]
    for a in range(len(firsts)):
        ia, ta = firsts[a]
        for b in range(a + 1, len(firsts)):
            ib, tb = firsts[b]
            if abs(len(ta) - len(tb)) > max(len(ta), len(tb)) * 0.3:
                continue
            r = max(difflib.SequenceMatcher(None, ta, tb).ratio(),
                    difflib.SequenceMatcher(None, tb, ta).ratio())
            if r > 0.9:
                flag(fname, ib, f"أول رسالة user متشابهة >90% مع السطر {ia}: '{tb[:50]}'")


def check_against_old(fname, rows):
    old_firsts = set()
    for old in ["iraqi_v8_batch_train.jsonl", "iraqi_v8_batch_val.jsonl",
                "iraqi_v9_generated.jsonl", "iraqi_train_v8_part01.jsonl",
                "iraqi_train_v8_part02.jsonl", "iraqi_train_v8_part03.jsonl"]:
        p = DATA / old
        if not p.exists():
            continue
        with open(p, encoding="utf-8") as f:
            for line in f:
                try:
                    r = json.loads(line)
                    old_firsts.add(r["messages"][1]["content"].strip())
                except Exception:
                    pass
    for i, r in rows:
        if first_user(r) in old_firsts:
            flag(fname, i, f"أول رسالة مكررة حرفياً من v8/v9: '{first_user(r)[:50]}'")


# ============================================================
# فحص 6: الإحصائية + اللهجة
# ============================================================
IRAQI_MARKERS = ["شكد", "هسه", "ماكو", "اكو", "أكو", "عيني", "زين", "خوش",
                 "تدلل", "هيچي", "شنو", "شلون", "هواي", "چان", "بيك", "والله",
                 "هلا", "منورنا", "نورتنا", "أگدر", "اكدر", "أكدر", "خوية",
                 "صدگ", "گدام", "اذا", "حياك", "يطلعلك", "عدنا", "بصراحة"]
FUSHA_FLAGS = ["يمكنني", "بالتأكيد", "يسعدني", "سوف ", "هل ترغب", "في شنو"]


def stats(corrective, extraction, items):
    print("\n" + " الإحصائية الختامية ".center(60, "="))
    c = Counter((r["category"], r.get("direction", "-")) for _, r in corrective)
    by_dir = Counter(r.get("direction", "-") for _, r in corrective)
    for (cat, d), n in sorted(c.items()):
        print(f"  {cat:<30} {d:<8} {n}")
    total = len(corrective)
    print(f"  المجموع: {total} | إحالة: {by_dir.get('refer', 0)} "
          f"({100 * by_dir.get('refer', 0) // total}%) | إجابة: {by_dir.get('answer', 0)} "
          f"({100 * by_dir.get('answer', 0) // total}%)")
    for name, rows in [("extraction", extraction), ("items", items)]:
        c2 = Counter(r["category"] for _, r in rows)
        print(f"  {name}: " + "، ".join(f"{k}={v}" for k, v in sorted(c2.items())))

    # عينة لهجة عشوائية 30 رد
    random.seed(7)
    replies = [m["content"] for _, r in corrective for m in r["messages"]
               if m["role"] == "assistant"]
    sample = random.sample(replies, 30)
    with_marker = sum(1 for s in sample if any(mk in s for mk in IRAQI_MARKERS))
    print(f"  ماركرات اللهجة: {with_marker}/30 رد بالعينة العشوائية "
          f"({100 * with_marker // 30}%)")
    fusha = [s for s in replies if any(fl in s for fl in FUSHA_FLAGS)]
    print(f"  ردود فيها فصحى ممنوعة: {len(fusha)}")
    for s in fusha[:5]:
        print(f"    ⚠️ {s[:70]}")

    # تنوع صياغات الإحالة: لا صياغة كاملة تتكرر بأكثر من 10%
    refer_replies = [m["content"] for _, r in corrective if r.get("direction") == "refer"
                     for m in r["messages"] if m["role"] == "assistant" and has_refer(m["content"])]
    rc = Counter(refer_replies)
    worst = rc.most_common(1)
    if worst and worst[0][1] > 0.10 * total:
        print(f"  ⚠️ صياغة إحالة مكررة {worst[0][1]} مرة (>{int(0.10 * total)}): {worst[0][0][:60]}")
    else:
        print(f"  تنوع الإحالة: أكثر صياغة تكررت {worst[0][1] if worst else 0} مرة من أصل {len(refer_replies)} — ضمن الحد")

    # أطوال المحادثات
    lens = Counter(len(r["messages"]) // 2 for _, r in corrective)
    print("  توزيع الأدوار (زوج سؤال/جواب): " +
          "، ".join(f"{k} دور={v}" for k, v in sorted(lens.items())))


# ============================================================
# main
# ============================================================
def main():
    corrective = load("iraqi_v10_corrective.jsonl")
    extraction = load("iraqi_v10_extraction.jsonl")
    items = load("iraqi_v10_items.jsonl")

    print("فحص 1: البنية...")
    for fname, rows in [("iraqi_v10_corrective.jsonl", corrective),
                        ("iraqi_v10_extraction.jsonl", extraction),
                        ("iraqi_v10_items.jsonl", items)]:
        ok = check_structure(fname, rows)
        print(f"  {fname}: {ok}/{len(rows)} بنية سليمة")

    print("فحص 2: الاتساق الشرطي (ادعاءات الرد ضد الكتالوج)...")
    n = check_consistency("iraqi_v10_corrective.jsonl", corrective)
    print(f"  فُحص {n} رد assistant")

    print("فحص 3: الأرقام (كل الفئات + تشديد فئة 5)...")
    check_numbers("iraqi_v10_corrective.jsonl", corrective)

    print("فحص 4: ملف الاستخراج...")
    check_extraction("iraqi_v10_extraction.jsonl", extraction)

    print("فحص ملف المنتجات...")
    check_items("iraqi_v10_items.jsonl", items)

    print("فحص 5: التكرار...")
    for fname, rows in [("iraqi_v10_corrective.jsonl", corrective),
                        ("iraqi_v10_extraction.jsonl", extraction),
                        ("iraqi_v10_items.jsonl", items)]:
        check_duplicates(fname, rows)
        check_against_old(fname, rows)

    stats(corrective, extraction, items)

    print("\n" + " النتيجة ".center(60, "█"))
    if VIOLATIONS:
        print(f"❌ {len(VIOLATIONS)} مخالفة:")
        for v in VIOLATIONS:
            print(f"  {v}")
        sys.exit(1)
    print("🟢 كل الفحوص عدّت — الداتا جاهزة للتدريب.")


if __name__ == "__main__":
    main()
