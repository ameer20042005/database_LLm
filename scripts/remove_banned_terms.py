# -*- coding: utf-8 -*-
"""
إزالة مصطلحات ممنوعة من داتا التدريب.

═══════════════════════════════════════════════════════════════
«أهل البيت» — ممنوعة بطلب المالك
═══════════════════════════════════════════════════════════════
اللفظة تظهر باستعمالين مختلفين بالداتا:

  ١. **عامّي** — بمعنى العائلة/أهل الدار:
       «ما عجب أهل البيت»  ·  «أهل البيت انبسطوا»
       «لأهل البيت أرشحلك تلفزيون...»

  ٢. **ديني** — بفئة `religious_occasions`، إشارة لآل النبي.

الاثنان ينشالان، والبديل **«العائلة»** بكل الحالات.

**مبدأ التنفيذ:** الاستبدال يراعي اللواصق («لأهل البيت» → «للعائلة»،
«وأهل البيت» → «والعائلة»)، لأن الاستبدال الأعمى للمفردة ينتج
«ل العائلة» و«و العائلة» — لام وواو معلّقتين.

⚠️ **درس تنفيذي:** أول نسخة استعملت `\\b` (حدّ الكلمة) بنمط انكتب
بسياق غير خام، فانحوّل لحرف backspace فعلي (0x08) بدل حدّ الكلمة.
النتيجة إن ولا نمط طابق، والسكربت طبع «161 حالة متبقية» بلا ما يبدّل
شي — فشل صامت لولا فحص `STILL_PRESENT`. الحدود مو ضرورية أصلاً لأن
العبارة مركّبة من كلمتين ولا تلتبس بغيرها.

يشتغل على `data/v16/` (المصدر المصلَّح) وعلى ملفات التقييم.
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
             "iraqi_v16_val_extra.jsonl", "iraqi_v17_val_extra.jsonl"]

SP = r"\s+"
RULES = [
    # اللواصق أولاً — لازم تسبق المفردة
    ("آل" + SP + "البيت", "العائلة"),
    ("لأهل" + SP + "البيت", "للعائلة"),
    ("وأهل" + SP + "البيت", "والعائلة"),
    ("بأهل" + SP + "البيت", "بالعائلة"),
    ("لاهل" + SP + "البيت", "للعائلة"),
    ("واهل" + SP + "البيت", "والعائلة"),
    ("من" + SP + "أهل" + SP + "البيت", "من العائلة"),
    ("على" + SP + "أهل" + SP + "البيت", "على العائلة"),
    # المفردة بالآخر، بصيغتيها الإملائيتين
    ("أهل" + SP + "البيت", "العائلة"),
    ("اهل" + SP + "البيت", "العائلة"),
]
COMPILED = [(re.compile(p), r) for p, r in RULES]

BANNED_CHECK = re.compile("أهل" + SP + "البيت|اهل" + SP + "البيت|آل" + SP + "البيت")


def clean(text):
    out = text
    for rx, rep in COMPILED:
        out = rx.sub(rep, out)
    out = re.sub(r"\s{2,}", " ", out).strip()
    return out


def process(path, stats):
    rows, changed = [], False
    for line in path.open(encoding="utf-8"):
        d = json.loads(line)
        msgs = []
        for m in d["messages"]:
            t = m["content"]
            if BANNED_CHECK.search(t):
                t2 = clean(t)
                if t2 != t:
                    stats[f"replaced_{m['role']}"] += 1
                    changed = True
                    t = t2
                if BANNED_CHECK.search(t):
                    stats["STILL_PRESENT"] += 1
            msgs.append({**m, "content": t})
        d["messages"] = msgs
        rows.append(d)
    if changed:
        with path.open("w", encoding="utf-8") as fh:
            for r in rows:
                fh.write(json.dumps(r, ensure_ascii=False) + "\n")


def main():
    # فحص ذاتي: يكشف فشل الأنماط قبل ما يمر صامتاً
    probe = "طلعت خوش شي وأهل البيت انبسطوا"
    assert "العائلة" in clean(probe) and "أهل البيت" not in clean(probe), (
        "❌ الأنماط ما تشتغل — راجع RULES")

    stats = Counter()
    for f in sorted(SRC.glob("*.jsonl")):
        process(f, stats)
    for name in VAL_FILES:
        p = ROOT / "data" / name
        if p.exists():
            process(p, stats)

    print("=" * 56)
    print("إزالة المصطلحات الممنوعة")
    print("=" * 56)
    for k, v in stats.most_common():
        print(f"  {k:<24}{v:>8,}")
    print(f"\n  {'✅ صفر حالة متبقية' if not stats['STILL_PRESENT'] else '❌ بقت حالات'}")


if __name__ == "__main__":
    main()
