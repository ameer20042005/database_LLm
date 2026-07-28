# -*- coding: utf-8 -*-
"""
v16 — إصلاح التناقضات اللي كشفها القياس، لا إضافة أمثلة فوقها.

═══════════════════════════════════════════════════════════════
لماذا إصلاح لا إضافة
═══════════════════════════════════════════════════════════════
الفحص طلع 8/11 و17/25. الفحوص الفاشلة مو «فجوات» تنسدّ بأمثلة جديدة —
هي **تناقضات مقيسة بالداتا نفسها**: الموديل تعلّم بالضبط اللي درّبناه
عليه، والقياس يعاقبه عليه. إضافة دفعة v16 فوق التناقض تخلي الموديل
يشوف السلوكين بنفس الوزن. فالعلاج حذف/إصلاح المصدر.

التشخيص المقيس (سكربت التحليل، مو تقدير):

  ١. `grounded_catalog_reject` — 1,283 من 1,785 دور رفض (72%) بيه سعر.
     النمط السائد: «ماكو X، بس أكو Y بـسعر». القياس (س4) يعتبر أي رقم
     برد الرفض اختراعاً. الداتا تعلّم عكس المطلوب حرفياً.

  ٢. `order_total_no_number` — 217 من 232 (94%) يطلع رقم محسوب، مع إن
     اسم الفئة «no_number». الفئة تناقض تسميتها، وهي سبب حساب 1/5.
     وتتصادم مباشرة مع `cat5_sum_over_precomputed` (129) اللي تعلّم
     الإحالة للمحسوب مسبقاً.

  ٣. `cat1_warranty_detail` — 408 من 408 رسالة نظام بيها «ضمان». يعني
     «جاوب بالمدة» دايماً مؤسَّس. الموديل عمّم على الحالة اللي **ما**
     بيها ضمان بالنظام (س8).

  ٤. اللهجة — 10,533 من 12,458 دور تحية/سواليف (84.5%) بيه أقل من
     ماركرين عراقيين، و202 بس بيه 3+. `diversify_phrasings.py` صحّح
     تراكم الخواتم لكنه صفّى الماركرات من الأدوار القصيرة اللي يقيسها
     الفحص.

  ٥. المقارنة — 740 سؤال مقارنة، 2 بس ينحال. بينما
     `cat2_spec_deflection` يحيل 43 من 131 (33%). إشارة مختلطة.

المخرجات تنكتب بـ`data/v16/` — ملفات المصدر ما تتمس.
"""
import json
import random
import re
import shutil
import sys
from collections import Counter, defaultdict
from pathlib import Path

sys.stdout.reconfigure(encoding="utf-8")
random.seed(20260728)

ROOT = Path(__file__).resolve().parent.parent
DATA = ROOT / "data"
OUT = DATA / "v16"

# الملفات المصدر اللي نصلحها (نفس مصادر build_final_dataset)
SRC_GLOBS = ["iraqi_train_v8_part*.jsonl", "iraqi_v9_generated*.jsonl",
             "iraqi_v10_*.jsonl", "iraqi_v11_gaps.jsonl",
             "iraqi_v12_order.jsonl", "iraqi_v13_scope.jsonl",
             "iraqi_v14_expand.jsonl", "iraqi_v15_behavioral.jsonl"]

NUM = re.compile(r"\d[\d,]{2,}")
# «ما أكو» كانت ناقصة بأول تشغيلة فنجت 351 رد رفض مسعّر من الإصلاح.
REJECT_CUE = re.compile(
    r"ماكو|ما عدنا|مو موجود|ما نشتغل|ما عندنا|ما أكو|ما اكو|مو متوفر|ما متوفر")
DEFER_CUE = re.compile(r"أتأكد|اتأكد|ما مكتوب|ما عندي|مو موضح|ما موضح|أسأل وأرجعلك")
WARRANTY_Q = re.compile(r"ضمان|كفالة")
DURATION = re.compile(r"(سنة|سنتين|ثلاث سنوات|سنوات|شهر|أشهر|اشهر)")


# ════════════════════════════════════════════════════════════════════
# ١. الرفض بلا سعر — يقص الارتداد المسعّر من دور الرفض
# ════════════════════════════════════════════════════════════════════
# «ماكو X، بس أكو Y بـ495,000» -> «ماكو X، بس أكو عدنا Y — تحب تشوفه؟»
# السعر ينحذف من دور الرفض بس. الارتداد للبديل يبقى (سلوك بيع صحيح)،
# لكن بلا رقم — لأن الزبون ما سأل عن سعر البديل بعد.
# الذيول محايدة جنسياً — «تشوفه» مع «عباية نسائية» غلط نحوي. الصيغة
# اللي ما تشير للمنتج بضمير تشتغل مع المذكر والمؤنث سوا.
ALT_TAILS = ["— تحب تشوف؟", "— شوف وگلي رأيك", "— يعجبك لو أجيبلك غيره؟",
             "— تحب أفصّللك أكثر؟", "— اگدر أعرضلك اياه"]


def strip_price_from_reject(text):
    """يشيل السعر من دور الرفض ويخلي الارتداد بلا رقم."""
    if not REJECT_CUE.search(text) or not NUM.search(text):
        return text, False
    # يقص من أول «بـ<رقم>» أو «<رقم> دينار» للنهاية. الترتيب مهم:
    # بعض الردود تحط السعر بجملة ثانية، فالقص لازم يبدأ من أول ظهور
    # للرقم لا من نمط بعينه.
    m = NUM.search(text)
    t = text[:m.start()]
    # يشيل «بـ» أو «سعره» المعلّقة اللي سبقت الرقم
    t = re.sub(r"\s*(بـ|ب|سعره|سعرها|يطلعلك|بسعر)\s*$", "", t).rstrip(" ،,-—:")
    if not t or len(t) < 8:
        return text, False
    if NUM.search(t):                     # بقى رقم -> ما ننضمن، نتركها
        return text, False
    return f"{t} {random.choice(ALT_TAILS)}", True


# ════════════════════════════════════════════════════════════════════
# ٢. الاجمالي — إحالة للحاسبة بلا رقم مخترع
# ════════════════════════════════════════════════════════════════════
# `order_total_no_number` تسميتها تگول بلا رقم وسلوكها يحسب. نخليها
# تطابق اسمها: تنقل سعر الوحدة (مؤسَّس بالكتالوج) وتحيل المجموع.
TOTAL_DEFER = [
    "{name} بـ{price} دينار للوحدة عيني، والمجموع النهائي أحسبه بالحاسبة وأگلك بالضبط",
    "سعر الوحدة {price} دينار لـ{name}، خليني أضربها بالحاسبة حتى ما أغلط بالمجموع",
    "{name} الواحدة بـ{price} دينار، والاجمالي أطلعه من الحاسبة وأرد عليك حالاً",
    "الوحدة بـ{price} دينار من {name}، المجموع أدگه بالحاسبة عيني حتى يطلع مضبوط",
]


def fix_total_turn(text):
    """يحوّل رد فيه مجموع محسوب إلى نقل سعر الوحدة + إحالة."""
    m = re.match(r"^(.*?)\s*بـ?\s*(\d[\d,]*)\s*دينار\s*للوحدة", text)
    if not m:
        return text, False
    name, price = m.group(1).strip(), m.group(2)
    name = re.sub(r"^(اهلين|هلا|حياك|تدلل|زين|خوش)\s+(عيني|الله|حبيبي)?\s*،?\s*", "", name).strip()
    if not name or not price:
        return text, False
    return random.choice(TOTAL_DEFER).format(name=name, price=price), True


# ════════════════════════════════════════════════════════════════════
# ٣. الضمان — نصف الأمثلة بلا ضمان بالنظام
# ════════════════════════════════════════════════════════════════════
# المشكلة إن 100% من رسائل النظام بيها ضمان، فـ«جاوب» دايماً صح.
# نحذف سطر الضمان من نصف الأمثلة، ونبدّل الرد للإحالة — حتى يتعلم
# الشرط لا الجواب.
WARRANTY_DEFER = [
    "مدة الضمان ما مكتوبة عندي بالقائمة عيني، اتأكدلك وأرد عليك",
    "الضمان مو موضح عندي، خليني أتأكد وأگلك حتى ما أغلطلك",
    "ما عندي تفصيل الضمان مكتوب، أسأل المسؤول وأرجعلك بالجواب",
    "والله الضمان ما مدوّن عندي بالقائمة، اتأكدلك اليوم وأخبرك",
]
WARRANTY_LINE = re.compile(r"[،,]?\s*ضمان\s+[^\n،,]+")


def make_warranty_ungrounded(msgs):
    """يشيل ذكر الضمان من رسالة النظام ويخلي **رد الضمان** إحالة.

    الرد اللي يتبدّل لازم يكون اللي جاوب على سؤال الضمان، مو آخر رد
    بالمحادثة. أول تشغيلة بدّلت الأخير عمياً فصارت محادثة تجاوب بالمدة
    بالدور الثالث وتنفي وجودها بالخامس — تناقض داخل نفس المحادثة.
    """
    out = [dict(m) for m in msgs]
    touched = False
    for m in out:
        if m["role"] == "system" and "ضمان" in m["content"]:
            m["content"] = WARRANTY_LINE.sub("", m["content"])
            touched = True
    if not touched:
        return msgs, False

    # نلگه رد المساعد اللي يعقب سؤال ضمان من الزبون
    idx = None
    for i, m in enumerate(out):
        if m["role"] == "user" and WARRANTY_Q.search(m["content"]):
            if i + 1 < len(out) and out[i + 1]["role"] == "assistant":
                idx = i + 1
    if idx is None:
        return msgs, False
    out[idx]["content"] = random.choice(WARRANTY_DEFER)

    # أي رد لاحق يذكر مدة ضمان يصير متناقضاً -> نقص المحادثة عند الإحالة
    for j in range(idx + 1, len(out)):
        if out[j]["role"] == "assistant" and DURATION.search(out[j]["content"]) \
                and WARRANTY_Q.search(out[j]["content"]):
            return out[:idx + 1], True
    return out, True


# ════════════════════════════════════════════════════════════════════
# ٤. اللهجة — إعادة ماركر عراقي للأدوار الاجتماعية القصيرة
# ════════════════════════════════════════════════════════════════════
# القاعدة القديمة («خاتمة واحدة بالأكثر») صحيحة ضد التراكم، بس طبّقت
# على أدوار أصلاً بلا أي ماركر فصفّتها. هنا نضيف ماركر **واحد** للأدوار
# اللي عدها صفر أو واحد، وما نلمس اللي عدها ٢+.
MARKERS = ["عيني", "خوية", "شنو", "هسه", "اكو", "ماكو", "تدلل", "زين",
           "خوش", "ويا", "هلا", "صدگ", "گول", "شلون", "بيش", "شكد",
           "نورت", "گاعد", "هواي", "چان"]
SOCIAL_OPEN = ["هلا بيك، ", "أهلين، ", "تدلل، ", "هلا والله، ", "نورتنا، "]
SOCIAL_TAIL = [" عيني", " خوية", " حبيبي", " والله", " صدگني"]
SOCIAL_CATS = {"greetings", "smalltalk", "greetings_chat", "jokes_banter",
               "greetings_sys", "smalltalk_sys", "greetings_chat_sys",
               "jokes_banter_sys", "praise_expressions", "praise_expressions_sys",
               "greetings_smalltalk", "proverbs_sayings", "proverbs_sayings_sys"}
VOCATIVE = re.compile(r"عيني|خوية|حبيبي|خويه|عمي|استاذ")
# «والله» قسم لا نداء، لكنه ينراكم بنفس الشكل: «اشتقتلك والله ... والله»
OATH = re.compile(r"والله|صدگني")
# نهايات ما تقبل ذيل: سؤال، تعجب، نداء أو قسم بالآخر
NO_TAIL_END = re.compile(r"(؟|!|\?|عيني|خوية|حبيبي|خويه|والله|صدگني)\s*$")


def dedupe_oath(text):
    """يخلي «والله» مرة وحدة بالرد.

    خلل موروث من الداتا المصدر لا من تعريقي: «والله ما يهم. فاهم وضعك
    والله، ولذيج عندي حل» — قسمين بجملة وحدة. نبقي الأول ونشيل الباقي.
    """
    if text.count("والله") < 2:
        return text, False
    first = text.index("والله")
    head, tail = text[:first + 5], text[first + 5:]
    tail = re.sub(r"\s*،?\s*والله\b", "", tail)
    t = (head + tail)
    t = re.sub(r"\s{2,}", " ", t).replace(" ،", "،").strip()
    return t, True


def marker_count(t):
    return sum(1 for k in MARKERS if k in t)


def boost_dialect(text):
    """يضيف ماركر واحد بس — بلا تراكم نداءات ولا قسمين.

    قاعدة صارمة: إما افتتاحية أو ذيل، وما نضيف ذيل على جملة تنتهي
    بنداء/قسم/علامة استفهام. «شلونك؟ حبيبي» و«والله...والله» طلعن من
    أول تشغيلة لأن الشرط كان يفحص وجود النداء لا موقعه.
    """
    # الفحص يطلب 3+ ماركرات عبر محادثة قصيرة (3 أدوار)، يعني ماركر
    # واحد لكل دور مو كافي — العتبة 2 لكل دور. نوسّع للأدوار الأطول هم
    # لأن التحية العراقية تتحمل نداء بجملة 18 كلمة بلا ثقل.
    n = marker_count(text)
    if n >= 2 or len(text.split()) > 18:
        return text, False
    has_open = bool(re.match(r"^(هلا|أهلين|اهلين|تدلل|نورت|حياك|ميت هلا)", text))
    can_tail = not NO_TAIL_END.search(text)
    # القسم موجود بأي مكان -> ما نضيف قسم ثاني بالذيل
    tails = [t for t in SOCIAL_TAIL if not (OATH.search(text) and OATH.search(t))]

    if has_open:                          # عنده افتتاحية -> ذيل بس إذا يصح
        if can_tail and tails:
            return text.rstrip(" .،") + random.choice(tails), True
        return text, False
    if can_tail and tails and random.random() < 0.5:
        return text.rstrip(" .،") + random.choice(tails), True
    return random.choice(SOCIAL_OPEN) + text, True


# ════════════════════════════════════════════════════════════════════
# ٥. المقارنة — جواب مؤسَّس بدل إحالة عمياء
# ════════════════════════════════════════════════════════════════════
# لمن الفرق بين منتجين **مذكور بالنظام** (السعر/الاسم)، الجواب الصح
# مقارنة بالمذكور لا «اتأكدلك». نصلح أدوار المقارنة اللي تحيل رغم إن
# النظام فيه المعلومة.
COMPARE_Q = re.compile(r"الفرق بين|شنو الفرق|ايهما|أيهما|أحسن لو|احسن لو|أفضل لو")


def catalog_items(sysmsg):
    """يستخرج (اسم, سعر) من أسطر الكتالوج برسالة النظام."""
    items = []
    for line in sysmsg.splitlines():
        m = re.match(r"^\s*-\s*(.+?)\s*:\s*(\d[\d,]*)\s*دينار", line)
        if m:
            items.append((m.group(1).strip(), m.group(2)))
    return items


def fix_comparison(msgs):
    """إذا سؤال مقارنة وانحال رغم إن السعرين بالنظام -> جواب مؤسَّس."""
    sysmsg = " ".join(m["content"] for m in msgs if m["role"] == "system")
    items = catalog_items(sysmsg)
    if len(items) < 2:
        return msgs, False
    out = [dict(m) for m in msgs]
    changed = False
    for i, m in enumerate(out):
        if m["role"] != "user" or not COMPARE_Q.search(m["content"]):
            continue
        if i + 1 >= len(out) or out[i + 1]["role"] != "assistant":
            continue
        nxt = out[i + 1]["content"]
        if not DEFER_CUE.search(nxt):
            continue
        (n1, p1), (n2, p2) = items[0], items[1]
        out[i + 1]["content"] = (
            f"الفرق بالسعر عيني: {n1} بـ{p1} دينار و{n2} بـ{p2} دينار. "
            f"باقي التفاصيل ما مكتوبة عندي، اتأكدلك وأرد عليك"
        )
        changed = True
    return out, changed


# ════════════════════════════════════════════════════════════════════
# ٦. سؤال الحقل الناقص — يبني أمثلة الحقل الناقص فعلاً
# ════════════════════════════════════════════════════════════════════
# س1 فشل لأن `gap3_slot_questions` تسأل عن **أول** حقل، وما اكو أمثلة
# الزبون ينطي اسم+محافظة+عنوان بدفعة وحدة فيلزم السؤال عن الهاتف بس.
# نبني الحالات الأربعة صراحةً من نفس الأمثلة الموجودة.
FIELD_ASK = {
    "phone": ["بس انطيني رقم هاتفك حتى نكدر نوصلك",
              "ناقص رقم هاتفك بس عيني، دزه لو سمحت",
              "خوش، بقى رقم الهاتف حتى يتصل بيك المندوب",
              "تمام، شنو رقم هاتفك حتى نثبت الطلب؟"],
    "name": ["بس انطيني اسمك حتى أسجل الطلب",
             "ناقص اسمك بس عيني",
             "خوش، شنو اسمك الكريم حتى أثبته؟"],
    "province": ["بس گلي من أي محافظة حتى أسجل التوصيل",
                 "ناقص المحافظة بس، من وين انت عيني؟",
                 "خوش، أي محافظة حتى نحسب التوصيل؟"],
    "address": ["بس انطيني العنوان بالتفصيل حتى ما يضيع المندوب",
                "ناقص العنوان المفصل بس عيني",
                "خوش، وين العنوان بالضبط حتى يلگاك المندوب؟"],
}
NAMES = ["حيدر الجبوري", "مصطفى كريم", "علي حسن", "زينب محمد", "كرار عبد",
         "أحمد الساعدي", "مريم صادق", "عمار الدليمي", "سجاد حسين", "نور علي"]
PHONES = ["07701234567", "07811234567", "07751234567", "07901234567",
          "07723456789", "07812345678", "07767764454", "07740421723"]
PROVS = ["البصرة", "النجف", "بغداد", "أربيل", "كربلاء", "الموصل", "ذي قار",
         "بابل", "الأنبار", "ديالى", "السماوة", "العمارة"]
ADDRS = ["المعقل شارع الكورنيش", "حي الرسالة زقاق 7", "حي الجامعة شارع 12 دار 8",
         "الكرادة داخل محلة 909", "حي الحسين قرب الجامع", "شارع 60 محلة 14",
         "حي الصحة زقاق 3 دار 21", "المنصور شارع الأميرات"]


def build_missing_field_examples(base_rows, n_per_field=140):
    """يبني أمثلة: الزبون ينطي 3 حقول والمساعد يسأل عن الرابع بس."""
    pool = [r for r in base_rows
            if r.get("category") in ("gap3_slot_questions", "ord3_confirm_gate",
                                     "ord2_marker_withheld")
            and any(m["role"] == "system" for m in r["messages"])]
    if not pool:
        return []
    made = []
    for field in ("phone", "name", "province", "address"):
        for _ in range(n_per_field):
            src = random.choice(pool)
            sysmsg = next(m["content"] for m in src["messages"] if m["role"] == "system")
            items = catalog_items(sysmsg)
            if not items:
                continue
            name_p, price = random.choice(items)
            cn, ph = random.choice(NAMES), random.choice(PHONES)
            pv, ad = random.choice(PROVS), random.choice(ADDRS)

            # الزبون ينطي كل الحقول إلا الناقص
            parts = []
            if field != "name":
                parts.append(f"اسمي {cn}")
            if field != "phone":
                parts.append(f"رقمي {ph}")
            if field != "province":
                parts.append(f"اني من {pv}")
            if field != "address":
                parts.append(ad)
            given = "، ".join(parts)

            made.append({
                "category": "gap7_missing_field_ask",
                "messages": [
                    {"role": "system", "content": sysmsg},
                    {"role": "user", "content": f"شكد سعر {name_p}؟"},
                    {"role": "assistant",
                     "content": f"{name_p} سعره {price} دينار عيني"},
                    {"role": "user", "content": f"زين اريدها، ثبتلي الطلب. {given}"},
                    {"role": "assistant",
                     "content": random.choice(FIELD_ASK[field])},
                ],
            })
    return made


# ════════════════════════════════════════════════════════════════════
# التشغيل
# ════════════════════════════════════════════════════════════════════
def main():
    OUT.mkdir(exist_ok=True)
    stats = Counter()
    all_rows = []

    for g in SRC_GLOBS:
        for f in sorted(DATA.glob(g)):
            rows = []
            for line in f.open(encoding="utf-8"):
                d = json.loads(line)
                d.setdefault("category", "?")
                cat = d["category"]
                msgs = d["messages"]

                # ٣) الضمان — نصف الأمثلة تصير غير مؤسَّسة
                if cat == "cat1_warranty_detail" and random.random() < 0.5:
                    msgs, ok = make_warranty_ungrounded(msgs)
                    stats["warranty_ungrounded"] += ok

                # ٥) المقارنة
                if len(msgs) > 2:
                    msgs, ok = fix_comparison(msgs)
                    stats["comparison_grounded"] += ok

                new = []
                for m in msgs:
                    if m["role"] != "assistant":
                        new.append(m)
                        continue
                    t = m["content"]

                    # ١) الرفض بلا سعر
                    # `json_fixed_schema` مستثناة عمداً: الرفض هناك يسمي
                    # الصنف الناقص ثم يطلع JSON لباقي الأصناف اللي طلبها
                    # الزبون فعلاً — أسعارها مؤسَّسة بالكتالوج، مو اختراعاً.
                    if cat in ("grounded_catalog_reject", "off_topic_refusal_general",
                               "sequential_refusal", "persistence_refusal",
                               "grounded_catalog_resist", "gap4_alternatives_phrasing",
                               "qa_price inquiry", "qa_recommendation"):
                        t2, ok = strip_price_from_reject(t)
                        if ok:
                            t = t2
                            stats["reject_price_stripped"] += 1

                    # ٢) الاجمالي بلا رقم مخترع
                    if cat == "order_total_no_number":
                        t2, ok = fix_total_turn(t)
                        if ok:
                            t = t2
                            stats["total_deferred"] += 1

                    # ٤) اللهجة بالأدوار الاجتماعية
                    if cat in SOCIAL_CATS:
                        t2, ok = boost_dialect(t)
                        if ok:
                            t = t2
                            stats["dialect_boosted"] += 1

                    # ٧) قسم مكرر — على كل الفئات، بعد التعريق
                    t2, ok = dedupe_oath(t)
                    if ok:
                        t = t2
                        stats["oath_deduped"] += 1

                    new.append({**m, "content": t})

                d["messages"] = new
                rows.append(d)

            all_rows.extend(rows)
            with (OUT / f.name).open("w", encoding="utf-8") as fh:
                for r in rows:
                    fh.write(json.dumps(r, ensure_ascii=False) + "\n")

    # ٦) أمثلة الحقل الناقص — دفعة جديدة
    extra = build_missing_field_examples(all_rows)
    with (OUT / "iraqi_v16_missing_field.jsonl").open("w", encoding="utf-8") as fh:
        for r in extra:
            fh.write(json.dumps(r, ensure_ascii=False) + "\n")
    stats["missing_field_built"] = len(extra)

    print("=" * 66)
    print("v16 — إصلاح التناقضات")
    print("=" * 66)
    for k, v in stats.most_common():
        print(f"  {k:<28}{v:>8,}")
    print(f"\n  📁 {OUT}")


if __name__ == "__main__":
    main()
