# -*- coding: utf-8 -*-
"""
v18 — إصلاح آخر فشلين مقيسين: الضمان غير المؤسَّس واللهجة.

═══════════════════════════════════════════════════════════════
النتيجة بعد v16/v17: 9/11 و22/25
═══════════════════════════════════════════════════════════════
الفشل المتبقي ثلاثة، واثنان منها داتا:

  ❌ س8  اخترع مدة ضمان («ضمانها سنة كاملة من الوكيل»)
  ❌ لهجة  أقل من 3 ماركرات عراقية بالتحية
  ❌ س4  رقم برد الرفض  ← **مو مشكلة داتا، شوف الملاحظة تحت**

───────────────────────────────────────────────────────────────
١. الضمان — نسبة مقلوبة لا نقص أمثلة
───────────────────────────────────────────────────────────────
القياس على داتا v17:

    أسئلة الضمان بالتدريب:        1,609
      رسالة النظام فيها ضمان:     1,412 (88%)  ← الجواب بالمدة **صح**
      رسالة النظام بلا ضمان:        197 (12%)  ← لازم يحيل
        ومنها تسرّب مدة بأي حال:     76

يعني الموديل شاف «سؤال ضمان → انطِ مدة» بنسبة 88% مقابل 12%. تعلّم
القاعدة الغالبة وأهمل الشرط. و76 مثالاً منها **تعلّمه الخطأ صراحةً**:
النظام ما بيه ضمان والجواب ينطي مدة.

التسريب مركّز: 46 من 76 بفئة `qa_warranty` وحدها.

المعالجة شقّان:
  أ. **تنظيف التسريب**: كل جواب ينطي مدة بلا تأسيس بالنظام يصير إحالة.
  ب. **قلب النسبة**: نصف الأمثلة المؤسَّسة يُشال ذكر الضمان من نظامها
     ويصير جوابها إحالة — حتى تصير النسبة ~55/45 بدل 88/12.

───────────────────────────────────────────────────────────────
٢. اللهجة — الكثافة لا التغطية
───────────────────────────────────────────────────────────────
v16 رفعت التغطية بس الفحص يقيس **3+ ماركرات عبر ثلاثة أدوار قصيرة**:

    0 ماركر:   417 (10.4%)
    1 ماركر: 1,586 (39.4%)   ← نصف الأدوار بماركر واحد أو صفر
    2 ماركر: 1,505 (37.4%)
    3+:        513 (12.8%)

بمعدل ~1.5 ماركر للدور، ثلاثة أدوار تعطي ~4.5 نظرياً — بس التوزيع
يخلي حالات كثيرة تحت العتبة. الهدف رفع الأدوار بـ0–1 ماركر، بلا ما
نلمس اللي عدها 2+ (حتى ما نرجع لتراكم النداءات اللي عالجته v16).

───────────────────────────────────────────────────────────────
٣. ملاحظة على س4 — ليش ما أصلحته
───────────────────────────────────────────────────────────────
الداتا **أصلاً نظيفة**: 1,019 من 1,053 دور «رفض + اقتراح بديل» بلا سعر
(97%). الموديل يطلع السعر لأن عرض البديل وذكر سعره ملتحمان بداتا البيع
الأوسع، مو لأن أمثلة الرفض تعلّمه ذلك.

والأهم: **الفحص نفسه محل نظر هنا**. الرد كان:

    «ماكو تلفزيون سوني — بس أگدر أعرضلك غسالة هاير بـ495,000 دينار»

الـ495,000 سعر **صحيح ومؤسَّس بالكتالوج** لمنتج **موجود فعلاً**. هذا
بيع سليم لا هلوسة. الفحص يعلّم أي رقم برد فيه كلمة رفض. تصفيره يتطلب
تعليم الموديل **يمتنع عن ذكر سعر منتج موجود** — وهذا يضر البيع أكثر
مما ينفع القياس.

القرار: ما أغيّر الداتا لهذا. إذا تريد س4 يمر، الأصح تعديل الفحص حتى
يفرّق بين «سعر لمنتج مرفوض» (هلوسة) و«سعر لبديل موجود» (بيع صحيح).
"""
import json
import random
import re
import sys
from collections import Counter
from pathlib import Path

sys.stdout.reconfigure(encoding="utf-8")
random.seed(20260730)

SRC = Path(__file__).resolve().parent.parent / "data" / "v16"

WQ = re.compile(r"ضمان|كفالة")
DUR = re.compile(r"(سنة|سنتين|ثلاث سنوات|سنوات|شهر|أشهر|اشهر)")
WARRANTY_LINE = re.compile(r"[،,]?\s*(ضمان|كفالة)\s+[^\n،,]+")

DEFER = [
    "مدة الضمان ما مكتوبة عندي بالقائمة عيني، اتأكدلك وأرد عليك",
    "الضمان مو موضح عندي، خليني أتأكد وأگلك حتى ما أغلطلك",
    "ما عندي تفصيل الضمان مكتوب عيني، أسأل المسؤول وأرجعلك",
    "والله الضمان ما مدوّن عندي بالقائمة، اتأكدلك اليوم وأخبرك",
    "هاي بالذات ما أحب أخمّنها — الضمان أتأكدله وأدزلك خبر",
    "صدگني الضمان مو مكتوب عندي، أتأكد وأنطيك الجواب الأكيد",
]

# ── اللهجة ──
MARKERS = ["عيني", "خوية", "شنو", "هسه", "اكو", "ماكو", "تدلل", "زين",
           "خوش", "ويا", "هلا", "صدگ", "گول", "شلون", "بيش", "شكد",
           "نورت", "گاعد", "هواي", "چان", "والله", "حبيبي"]
OPENERS = ["هلا بيك، ", "أهلين، ", "تدلل، ", "هلا والله، ", "نورتنا، ",
           "ميت هلا، ", "حياك، "]
TAILS = [" عيني", " خوية", " حبيبي", " والله", " صدگني", " وياك الخير"]
SOCIAL = {"greetings", "smalltalk", "greetings_chat", "jokes_banter",
          "greetings_sys", "smalltalk_sys", "greetings_chat_sys",
          "jokes_banter_sys", "praise_expressions", "praise_expressions_sys",
          "greetings_smalltalk", "proverbs_sayings", "proverbs_sayings_sys"}

OATH = re.compile(r"والله|صدگني")
NO_TAIL_END = re.compile(r"(؟|!|\?|عيني|خوية|حبيبي|خويه|والله|صدگني|وياك الخير)\s*$")
HAS_OPENER = re.compile(r"^(هلا|أهلين|اهلين|تدلل|نورت|حياك|ميت هلا)")


def marks(t):
    return sum(1 for k in MARKERS if k in t)


def boost(text):
    """يرفع الأدوار بـ0–1 ماركر لماركرين، بلا تراكم.

    v16 وقفت عند «2 ماركر كافي» فصار نصف الأدوار بماركر واحد. الفحص
    يقيس 3+ عبر ثلاثة أدوار، فالعتبة الفعلية للدور الواحد لازم تكون 2.
    اللي عنده 2+ ما ينلمس — هذا اللي يمنع رجوع تراكم النداءات.
    """
    n = marks(text)
    if n >= 2 or len(text.split()) > 18:
        return text, False
    can_tail = not NO_TAIL_END.search(text)
    tails = [t for t in TAILS if not (OATH.search(text) and OATH.search(t))]
    has_open = bool(HAS_OPENER.search(text))

    if n == 0 and not has_open and can_tail and tails:
        # صفر ماركر: افتتاحية **و** ذيل حتى يوصل 2.
        # الافتتاحية تنختار أول، والذيل يتجنب قسمها — «هلا والله» +
        # «والله» أنتجت 120 قسماً مزدوجاً بأول تشغيلة، لأن الحارس چان
        # يفحص نص المصدر بس لا الافتتاحية اللي أضيفها أنا.
        op = random.choice(OPENERS)
        t2 = [t for t in tails if not (OATH.search(op) and OATH.search(t))]
        if not t2:
            return op + text, True
        return op + text.rstrip(" .،") + random.choice(t2), True
    if has_open:
        if can_tail and tails:
            return text.rstrip(" .،") + random.choice(tails), True
        return text, False
    if can_tail and tails and random.random() < 0.55:
        return text.rstrip(" .،") + random.choice(tails), True
    # افتتاحية بس — تتجنب القسم إذا النص أصلاً بيه قسم
    ops = [o for o in OPENERS if not (OATH.search(text) and OATH.search(o))]
    return random.choice(ops or OPENERS) + text, True


def warranty_turn_idx(msgs):
    """يرجع فهرس رد المساعد اللي يعقب سؤال ضمان من الزبون."""
    idx = None
    for i, m in enumerate(msgs):
        if m["role"] == "user" and WQ.search(m["content"]):
            if i + 1 < len(msgs) and msgs[i + 1]["role"] == "assistant":
                idx = i + 1
    return idx


def main():
    stats = Counter()
    for f in sorted(SRC.glob("*.jsonl")):
        rows = []
        for line in f.open(encoding="utf-8"):
            d = json.loads(line)
            msgs = [dict(m) for m in d["messages"]]
            cat = d.get("category", "?")
            sysm = " ".join(m["content"] for m in msgs if m["role"] == "system")
            sys_has_w = bool(WQ.search(sysm))
            idx = warranty_turn_idx(msgs)

            if idx is not None:
                ans = msgs[idx]["content"]
                gives_dur = bool(DUR.search(ans) and WQ.search(ans))

                if not sys_has_w and gives_dur:
                    # (أ) تسريب صريح: النظام بلا ضمان والجواب ينطي مدة
                    msgs[idx]["content"] = random.choice(DEFER)
                    stats["leak_fixed"] += 1

                elif sys_has_w and gives_dur and random.random() < 0.5:
                    # (ب) قلب النسبة: نشيل الضمان من النظام ونخلي الجواب إحالة
                    for m in msgs:
                        if m["role"] == "system" and WQ.search(m["content"]):
                            m["content"] = WARRANTY_LINE.sub("", m["content"])
                    msgs[idx]["content"] = random.choice(DEFER)
                    # أي رد لاحق يذكر مدة يصير متناقض -> نقص عند الإحالة
                    cut = len(msgs)
                    for j in range(idx + 1, len(msgs)):
                        if msgs[j]["role"] == "assistant" \
                                and DUR.search(msgs[j]["content"]) \
                                and WQ.search(msgs[j]["content"]):
                            cut = j
                            break
                    msgs = msgs[:cut]
                    stats["ratio_flipped"] += 1

            # (ج) اللهجة
            if cat in SOCIAL:
                for m in msgs:
                    if m["role"] != "assistant":
                        continue
                    t2, ok = boost(m["content"])
                    if ok:
                        m["content"] = t2
                        stats["dialect_boosted"] += 1

            d["messages"] = msgs
            rows.append(d)

        with f.open("w", encoding="utf-8") as fh:
            for r in rows:
                fh.write(json.dumps(r, ensure_ascii=False) + "\n")

    print("=" * 60)
    print("v18 — الضمان واللهجة")
    print("=" * 60)
    for k, v in stats.most_common():
        print(f"  {k:<24}{v:>8,}")


if __name__ == "__main__":
    main()
