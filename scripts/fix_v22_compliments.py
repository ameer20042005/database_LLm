# -*- coding: utf-8 -*-
"""
v22 — توسيع المجاملات وموازنتها، وحذف وعود المجانية غير المؤسَّسة.

═══════════════════════════════════════════════════════════════
١. «ببلاش» — وعد غير مؤسَّس، ينشال
═══════════════════════════════════════════════════════════════
المقيس: 35 رداً يعد بخدمة مجانية، و**35 منها (100%) رسالة النظام ما
تذكر أي مجانية**:

    «جيبها نفحصها ببلاش، وبعدين أگلك يستاهل التصليح لو لا»
    «بنكة عمودية بـ50,000 دينار، ونغلفها ببلاش»

هذا نفس صنف اختراع مدة الضمان: البائع يلتزم بشي **ما خوّله النظام
بيه**. الفرق إن كلفته مباشرة — الزبون يجي متوقعاً فحصاً مجانياً.

«على حسابي» ما موجودة أصلاً بالداتا (فحصتها)، بس تنضاف للقائمة
الممنوعة وقائياً.

═══════════════════════════════════════════════════════════════
٢. المجاملات — موجودة بس مائلة التوزيع
═══════════════════════════════════════════════════════════════
المقيس: 24.8% من ردود المساعد فيها مجاملة، بس التوزيع مركّز بثلاث:

    تدلل 7.3% · حياك الله 6.8% · صدگني 4.9%
    ...
    تامر أمر 0.3% · من ذوقك 0.04%   ← شبه معدومة

وناقصات صيغ عراقية أصيلة كثيرة. التوسيع يضيف تنوعاً **بلا ما يرفع
الكثافة**: القاعدة من v16 تبقى — **مجاملة وحدة بالرد بالأكثر**، وما
نلمس رداً فيه مجاملة أصلاً.

الاستبدال يستهدف **الصيغ الثلاث المهيمنة** بس، ويوزّعها على المخزون
الأوسع. النتيجة توزيع أسطح بلا زيادة بالحشو.
"""
import json
import random
import re
import sys
from collections import Counter
from pathlib import Path

sys.stdout.reconfigure(encoding="utf-8")
random.seed(20260803)

ROOT = Path(__file__).resolve().parent.parent
SRC = ROOT / "data" / "v16"
VAL_FILES = ["iraqi_val_v8.jsonl", "iraqi_val_v13.jsonl",
             "iraqi_v16_val_extra.jsonl", "iraqi_v17_val_extra.jsonl",
             "iraqi_v19_val_extra.jsonl", "iraqi_v20_val_extra.jsonl"]

# ════════════ ١) وعود المجانية غير المؤسَّسة ════════════
# الاستبدال يحافظ على الخدمة وينزع الوعد المجاني.
FREE_FIXES = [
    (re.compile(r"جيبها\s+نفحصها\s+ببلاش"), "جيبها نفحصها"),
    (re.compile(r"جيبه\s+نفحصه\s+ببلاش"), "جيبه نفحصه"),
    (re.compile(r"الفحص\s+ببلاش\s*،?\s*و?"), "الفحص عدنا، و"),
    (re.compile(r"\s*،?\s*ونغلفها\s+ببلاش"), "، ونغلفها الك"),
    (re.compile(r"\s*،?\s*ونغلفه\s+ببلاش"), "، ونغلفه الك"),
    (re.compile(r"\s*ببلاش"), ""),          # أي بقية
]
BANNED_FREE = re.compile(
    r"ببلاش|على حسابي|عالحسابي|ع حسابي|هدية مني|مجاناً مني|خلي عليّ|"
    r"خليها علي|خليها عليّ")

# ════════════ ٢) مخزون المجاملات ════════════
# الصيغ المهيمنة اللي تنستبدل جزئياً
DOMINANT = {
    "تدلل": re.compile(r"\bتدلل\b"),
    "حياك الله": re.compile(r"حياك الله"),
    "صدگني": re.compile(r"\bصدگني\b"),
}
# البدائل — عراقية أصيلة، مصنّفة حسب الموقع بالجملة
OPENERS = [
    "على العين", "على راسي", "من عيوني", "أمرك عيني", "تامر أمر",
    "ميت هلا", "هلا بيك", "نورتنا", "شرفتنا", "دلالك",
    "حياك", "أهلا وسهلا", "عيونك الحلوة", "أمر عيني",
]
# ⚠️ الذيل ما يقبل أي مجاملة: «وياك الخير» و«دام عزك» و«بيتك عامر»
# **خواتم وداع**، فلصقها بآخر أي جملة ينتج:
#   «الجنة تحت أقدام الأمهات وياك الخير»      (مثل + وداع)
#   «وهو ناسي اسم أمه دام عزك»                 (نكتة + دعاء)
# الذيل يقتصر على **النداءات والتوكيدات** اللي تنلصق بأي سياق.
TAILS = [
    " عيني", " خوية", " والله", " حبيبي", " تسلم",
]
# خواتم الوداع تنستعمل بردود الشكر/الوداع بس.
# ⚠️ «وياك الخير» و«دام عزك» و«بيتك عامر» انشالن من مخزون الاستبدال
# نهائياً: حتى داخل «سياق الوداع» طلعن بمواضع غلط —
#   U: «شربت چاي؟»  A: «تعال نشرب سوية وياك الخير»
#   U: «سلملي على الأهل»  A: «توصل إن شاء الله ... وياك الخير»
# لأن كشف السياق بالكلمات ما يميّز الوداع الفعلي من ذكر عابر. الصيغ
# هذي موجودة أصلاً بالداتا بشكل طبيعي، فما تحتاج حقناً.
CLOSERS = [
    "الله يخليك", "الله يبارك بيك", "تكرم عينك", "الله يحفظك",
]
# سياق يقبل خاتمة وداع: شكر أو وداع من الزبون
CLOSING_CTX = re.compile(
    r"تسلم|شكرا|شكراً|مشكور|الله يخليك|فمان الله|بالسلامة|نشوفك|"
    r"وداعا|مع السلامة|تشرفنا|يعطيك العافية")


def strip_free(text):
    out = text
    for rx, rep in FREE_FIXES:
        out = rx.sub(rep, out)
    out = re.sub(r"\s{2,}", " ", out)
    out = re.sub(r"\s+([،.])", r"\1", out)
    out = re.sub(r"،\s*،", "،", out).strip(" ،")
    return out


# ── تنظيف ما بعد الاستبدال ──
# ⚠️ بعض الافتتاحيات **تحوي نداءً أصلاً** («أمرك عيني»، «من عيوني»)،
# فلمن تنحط قبل جملة تبدي بنداء يطلع «أمرك عيني عيني». حارس التراكم
# العام ما يمسكها لأنه يفحص النداءات المجردة المتجاورة بس.
DUP_VOC = re.compile(
    r"(أمرك عيني|أمر عيني|من عيوني|على راسي|على العين|عيونك الحلوة|"
    r"تامر أمر|دلالك)\s*،?\s*(عيني|خوية|حبيبي)\b")


def dedupe_oath(text):
    """قسم «والله» مرة وحدة — الذيل ممكن يضيف ثانياً."""
    if text.count("والله") < 2:
        return text
    i = text.index("والله")
    head, tail = text[:i + 5], text[i + 5:]
    tail = re.sub(r"\s*،?\s*والله\b", "", tail)
    out = re.sub(r"\s{2,}", " ", head + tail).replace(" ،", "،")
    return out.strip(" .،")


def polish(text):
    """ينظّف التراكم الناتج عن الاستبدال."""
    out = DUP_VOC.sub(r"\1", text)
    out = dedupe_oath(out)
    return re.sub(r"\s{2,}", " ", out).strip()


def rebalance(text, is_closing=False):
    """يبدّل صيغة مهيمنة بأخرى من المخزون — بلا زيادة الكثافة.

    القاعدة: استبدال **واحد** بالأكثر لكل رد، والبديل من **نفس الموقع**
    (افتتاحية مقابل افتتاحية) حتى ما تنكسر الجملة. وخواتم الوداع
    تنستعمل بسياق الشكر/الوداع بس.
    """
    for name, rx in DOMINANT.items():
        m = rx.search(text)
        if not m:
            continue
        if m.start() <= 2:                      # افتتاحية
            pool = OPENERS + (CLOSERS if is_closing else [])
            return text[:m.start()] + random.choice(pool) + text[m.end():], True
        if m.end() >= len(text) - 2:            # ذيل
            pool = CLOSERS if is_closing else [t.strip() for t in TAILS]
            return text[:m.start()] + random.choice(pool) + text[m.end():], True
        return text, False
    return text, False


def process(path, stats, rebalance_rate):
    rows, changed = [], False
    for line in path.open(encoding="utf-8"):
        d = json.loads(line)
        msgs = []
        for _i, m in enumerate(d["messages"]):
            if m["role"] != "assistant":
                msgs.append(m)
                continue
            # سياق الوداع يتحدد من كلام الزبون السابق ومن الرد نفسه
            _prev = d["messages"][_i - 1]["content"] if _i else ""
            _closing = bool(CLOSING_CTX.search(_prev)
                            or CLOSING_CTX.search(m["content"]))
            t = m["content"]

            if BANNED_FREE.search(t):
                t2 = strip_free(t)
                if t2 != t:
                    stats["free_promise_removed"] += 1
                    changed = True
                    t = t2

            if random.random() < rebalance_rate:
                t2, ok = rebalance(t, _closing)
                if ok:
                    stats["compliment_varied"] += 1
                    changed = True
                    t = t2

            # تنظيف التراكم الناتج عن الاستبدال — لازم بعده مباشرةً
            t2 = polish(t)
            if t2 != t:
                stats["stacking_cleaned"] += 1
                changed = True
                t = t2

            msgs.append({**m, "content": t})
        d["messages"] = msgs
        rows.append(d)
    if changed:
        with path.open("w", encoding="utf-8") as fh:
            for r in rows:
                fh.write(json.dumps(r, ensure_ascii=False) + "\n")


def main():
    stats = Counter()
    # 45% من الحالات المهيمنة تتنوّع — يكفي لتسطيح التوزيع بلا مسخ اللهجة
    for f in sorted(SRC.glob("*.jsonl")):
        process(f, stats, 0.45)
    for name in VAL_FILES:
        p = ROOT / "data" / name
        if p.exists():
            process(p, stats, 0.45)

    print("=" * 58)
    print("v22 — المجاملات ووعود المجانية")
    print("=" * 58)
    for k, v in stats.most_common():
        print(f"  {k:<26}{v:>8,}")


if __name__ == "__main__":
    main()
