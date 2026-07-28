# -*- coding: utf-8 -*-
"""
v21 — تنظيف ثلاثة أخطاء كشفها تدقيق ردود الرفض بعد v20.

═══════════════════════════════════════════════════════════════
الأخطاء الثلاثة (مقيسة على داتا v20)
═══════════════════════════════════════════════════════════════

**١. تقمّص طبي متبقٍ — 45 حالة، وهي الأخطر**

    U: «ما راجعت، كنت آخذ دواء من الصيدلية»
    A: «هذا غلط يا حجي، لازم تراجع دكتور. **خليني أفحصك**»

الرد داخل `off_topic_medical_strict` — الفئة اللي المفروض تمنع التقمّص
تماماً. `is_roleplay` بـv19 ما مسكتها لأنها تفحص التشخيص والوصفة
والتاريخ المرضي، و«خليني أفحصك» مو أي واحد منهن: هي **عرض إجراء
طبي**، محور رابع ما چان مغطّى.

**٢. ذيل بعد سؤال ختامي — 60 حالة**

    «هاي مو مجالي، أني بس بائع — تأمر بشي من المحل؟ — الأفضل تسأل مختص»

حقن v20 يضيف الذيل بالآخر دايماً، بلا ما ينتبه إن الرد ينتهي بسؤال
ارتداد للبيع. النتيجة ترتيب مقلوب: السؤال الختامي ما عاد ختامياً.

**٣. نصيحة عامة حشو — 443 حالة**

    «شغلي بالمحل بس — استشير واحد مختص وهو يفيدك»   (سؤال عن المذهب)
    «اسأل عالم — الأفضل تسأل مختص بهاي»              (تكرار)

«مختص» بلا تحديد ما تضيف معلومة. وأسوأ منها لمن الرد أصلاً يحيل لجهة
محددة («اسأل عالم») فيصير التذييل تكراراً.

═══════════════════════════════════════════════════════════════
المعالجة
═══════════════════════════════════════════════════════════════
١. «خليني أفحصك» وأخواتها -> إحالة نظيفة (نفس ردود v19 الصارمة).
٢. الذيل ينحط **قبل** السؤال الختامي لا بعده.
٣. النصيحة العامة تنشال إذا الرد أصلاً يحيل لجهة محددة، وإلا تنبدل
   بواحدة **محددة** حسب موضوع السؤال.
"""
import json
import random
import re
import sys
from collections import Counter
from pathlib import Path

sys.stdout.reconfigure(encoding="utf-8")
sys.path.insert(0, str(Path(__file__).resolve().parent))
random.seed(20260802)

from fix_v20_topic_expert_match import topic_of      # noqa: E402

SRC = Path(__file__).resolve().parent.parent / "data" / "v16"

# ── ١) تقمّص طبي: عرض إجراء طبي ──
# محور رابع ما چان بـv19: مو تشخيص ولا وصفة ولا تاريخ — عرض فحص.
ROLEPLAY_ACT = re.compile(
    r"خليني\s+أفحصك|خليني\s+افحصك|تعال\s+أفحصك|أفحصك|افحصك|نفحصك|"
    r"عيادتي|أشوفك\s+بالعياد[ةه]|وصفتلك|راح\s+أكتبلك|أكتبلك\s+وصف|"
    r"تعال\s+هسه\s+لا\s+تتأخر|أقيسلك\s+الضغط|نسويلك\s+تحليل")

MED_REFER = [
    "ما أگدر أنصحك بأمور صحية عيني، لازم تراجع دكتور أو صيدلية",
    "هاي أمور طبية ما أفهم بيها عيني — راجع دكتور، هو اللي يگلك الصح",
    "سلامتك عيني، بس أي دواء بلا فحص ممكن يضرك — راجع مختص",
    "الله يعافيك، بس هذا سؤال لأهل الطب مو إلي — روح للصيدلية أو العيادة",
    "أني بائع عيني، ما أفتي بالصحة — الدكتور هو المرجع بهيچ أمور",
]

# ── ٣) نصائح عامة حشو، وبدائلها المحددة ──
VAGUE_TAIL = re.compile(
    r"\s*—\s*(الأفضل تسأل مختص بهاي|أهل الاختصاص أدرى بيها|"
    r"استشير واحد مختص وهو يفيدك)\s*$")
# الرد أصلاً يحيل لجهة محددة؟
HAS_SPECIFIC = re.compile(
    r"رجل دين|عالم دين|عالم\b|أهل العلم|شيخ|طبيب|دكتور|صيدلي|صيدلية|"
    r"عياد[ةه]|محامي|محكم[ةه]|مهندس|محاسب|مرشد|كهربائي|ميكانيكي|"
    r"النشر[ةه]|مكتب سفر|صراف|أسط[ةه]|فني")
SPECIFIC_BY_TOPIC = {
    "دين": [" — اسأل رجل دين وهو يفتيك", " — أهل العلم أولى بجوابها"],
    "سياسة": ["", ""],           # السياسة ما تحتاج إحالة، الرفض يكفي
    "طب": [" — راجع طبيب أو صيدلية", " — دكتور يفيدك أكثر"],
    "قانون": [" — راجع محامي", " — محامي يفهم بيها أكثر"],
    "معلومة": [" — دور بمصدر موثوق", ""],
}

# ── ٢) ذيل بعد سؤال ختامي ──
TAIL_AFTER_Q = re.compile(r"(؟)\s*(—\s*[^—]+)$")


def fix_tail_order(text):
    """ينقل الذيل قبل السؤال الختامي بدل ما يجي بعده."""
    m = TAIL_AFTER_Q.search(text)
    if not m:
        return text, False
    tail = m.group(2).strip()
    head = text[:m.start()].rstrip()
    # الجملة قبل السؤال الختامي
    parts = re.split(r"\s*—\s*", head)
    q = parts[-1].strip()
    body = " — ".join(p.strip() for p in parts[:-1]) if len(parts) > 1 else ""
    if body:
        return f"{body} {tail} — {q}؟", True
    return f"{q}؟ {tail}".replace("؟ —", "؟"), True


def main():
    stats = Counter()
    for f in sorted(SRC.glob("*.jsonl")):
        rows = []
        for line in f.open(encoding="utf-8"):
            d = json.loads(line)
            cat = str(d.get("category", ""))
            msgs = [dict(m) for m in d["messages"]]

            # موضوع السؤال — لاختيار الإحالة المحددة
            topic = None
            for m in msgs:
                if m["role"] == "user":
                    topic = topic_of(m["content"]) or topic

            for i, m in enumerate(msgs):
                if m["role"] != "assistant":
                    continue
                t = m["content"]

                # ١) تقمّص طبي — بأي فئة، لأنه خطر بكل مكان
                if ROLEPLAY_ACT.search(t):
                    msgs[i]["content"] = random.choice(MED_REFER)
                    stats["roleplay_fixed"] += 1
                    continue

                if not cat.startswith("off_topic"):
                    continue

                # ٣) نصيحة عامة حشو
                mv = VAGUE_TAIL.search(t)
                if mv:
                    base = t[:mv.start()].rstrip(" .،")
                    if HAS_SPECIFIC.search(base):
                        t = base            # أصلاً يحيل -> نشيل الحشو
                        stats["vague_removed"] += 1
                    else:
                        opts = SPECIFIC_BY_TOPIC.get(topic or "", [""])
                        t = base + random.choice(opts)
                        stats["vague_specified"] += 1

                # ٢) ترتيب الذيل والسؤال الختامي
                t2, ok = fix_tail_order(t)
                if ok:
                    t = t2
                    stats["tail_reordered"] += 1

                t = re.sub(r"\s{2,}", " ", t).strip()
                msgs[i]["content"] = t

            d["messages"] = msgs
            rows.append(d)

        with f.open("w", encoding="utf-8") as fh:
            for r in rows:
                fh.write(json.dumps(r, ensure_ascii=False) + "\n")

    print("=" * 58)
    print("v21 — تنظيف ردود الرفض")
    print("=" * 58)
    for k, v in stats.most_common():
        print(f"  {k:<24}{v:>8,}")


if __name__ == "__main__":
    main()
