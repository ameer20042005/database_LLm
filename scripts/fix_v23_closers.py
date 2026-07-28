# -*- coding: utf-8 -*-
"""
v23 — نزع خواتم الوداع من المواضع غير المناسبة.

═══════════════════════════════════════════════════════════════
المشكلة
═══════════════════════════════════════════════════════════════
«وياك الخير» و«دام عزك» و«بيتك عامر» **خواتم وداع**، مو مجاملات عامة
تنلصق بأي جملة. المقيس على المصدر: **1,268 حالة** بسياق مو وداع،
941 منها بآخر الرد:

    U: «عدك مثل عن الصديق؟»
    A: «الصديق وقت الضيق، هذا أشهر مثل عدنا **وياك الخير**»   ← مثل + وداع

    U: «شنو سويت اليوم؟»
    A: «شغل وروحة وجية، الروتين المعتاد **وياك الخير**»        ← سوالف + وداع

    U: «وين رايح؟»
    A: «للبيت، خلصت شغلي **وياك الخير**»

هذي **مو من حقني بـv22** — شلتهن من مخزون الاستبدال هناك، بس الحالات
موروثة من `diversify_phrasings.py` القديم اللي چان يركّب
«افتتاحية × جوهر × ذيل» بلا وعي بالسياق.

الخطأ اللي وقعت بيه: حسبت المشكلة محلولة لأني منعت **حقن** جديد،
وما فحصت الموروث. الفحص النهائي كشف 574 حالة بالملفات النهائية.

═══════════════════════════════════════════════════════════════
المعالجة
═══════════════════════════════════════════════════════════════
الخاتمة تنشال إذا السياق مو وداع/شكر. وتنبقى إذا:
  • الزبون شكر أو ودّع بالدور السابق
  • الرد نفسه فيه وداع («بالسلامة»، «نشوفك»)

بعد النزع، الجملة تنتهي طبيعياً — ما نحط بديلاً، لأن الخاتمة كانت
حشواً أصلاً لا جزءاً من المعنى.
"""
import json
import re
import sys
from collections import Counter
from pathlib import Path

sys.stdout.reconfigure(encoding="utf-8")

ROOT = Path(__file__).resolve().parent.parent
SRC = ROOT / "data" / "v16"
VAL_FILES = ["iraqi_val_v8.jsonl", "iraqi_val_v13.jsonl",
             "iraqi_v16_val_extra.jsonl", "iraqi_v17_val_extra.jsonl",
             "iraqi_v19_val_extra.jsonl", "iraqi_v20_val_extra.jsonl"]

CLOSER = re.compile(r"\s*،?\s*(وياك الخير|دام عزك|بيتك عامر)\s*")
# سياق يبرّر الخاتمة: شكر أو وداع
CLOSING_CTX = re.compile(
    r"تسلم|شكرا|شكراً|مشكور|الله يخليك|فمان الله|بالسلامة|نشوفك|"
    r"مع السلامة|تشرفنا|يعطيك العافية|اتفقنا|هاي الفلوس|بالعافية|"
    r"الله يعافيك|ممنون|تعبناك")


def strip_closer(text):
    out = CLOSER.sub(" ", text)
    out = re.sub(r"\s{2,}", " ", out)
    out = re.sub(r"\s+([،.؟!])", r"\1", out)
    out = re.sub(r"،\s*،", "،", out)
    return out.strip(" ،-—")


def process(path, stats):
    rows, changed = [], False
    for line in path.open(encoding="utf-8"):
        d = json.loads(line)
        ms = d["messages"]
        out = []
        for i, m in enumerate(ms):
            if m["role"] != "assistant" or not CLOSER.search(m["content"]):
                out.append(m)
                continue
            prev = ms[i - 1]["content"] if i else ""
            if CLOSING_CTX.search(prev) or CLOSING_CTX.search(m["content"]):
                stats["kept_valid_context"] += 1
                out.append(m)
                continue
            t = strip_closer(m["content"])
            if t and t != m["content"]:
                stats["closer_removed"] += 1
                changed = True
                out.append({**m, "content": t})
            else:
                out.append(m)
        d["messages"] = out
        rows.append(d)
    if changed:
        with path.open("w", encoding="utf-8") as fh:
            for r in rows:
                fh.write(json.dumps(r, ensure_ascii=False) + "\n")


def main():
    stats = Counter()
    for f in sorted(SRC.glob("*.jsonl")):
        process(f, stats)
    for name in VAL_FILES:
        p = ROOT / "data" / name
        if p.exists():
            process(p, stats)

    print("=" * 56)
    print("v23 — خواتم الوداع")
    print("=" * 56)
    for k, v in stats.most_common():
        print(f"  {k:<24}{v:>8,}")


if __name__ == "__main__":
    main()
