# -*- coding: utf-8 -*-
"""
v24 — وعود المجانية تتقيّد بالسستم.

═══════════════════════════════════════════════════════════════
القاعدة
═══════════════════════════════════════════════════════════════
«بلاش» **مو خطأ بحد ذاته** — البائع العراقي يگولها طبيعياً. الخطأ إنه
يعد بمجانية **ما خوّله النظام بيها**. فالقاعدة: الوعد يبقى إذا رسالة
النظام تذكره، وينشال إذا لا.

**المقيس (تدريب + تقييم):**

    ردود فيها وعد مجانية:        777
      مؤسَّسة بالنظام:             29   ← «التوصيل داخل بغداد: مجاني»
      غير مؤسَّسة:                748   ← التزام ما خوّله النظام بيه

فحص v22 چان ناقصاً: مسك «ببلاش» بالباء بس، ففات «بلاش» و«مجاني»
و«بالمجان» و«مجانية». الحالات موزّعة على 14 فئة:

    «الاستشارة مجانية دايم عندنا»          (services)
    «الفحص مجاني، الأجرة على التصليح بس»   (qa_repair services)
    «التوصيل داخل بغداد بلاش»              (qa_delivery)
    «نحطهم بكيس هدية بالمجان»              (sales_clothes)

═══════════════════════════════════════════════════════════════
إيجابيات كاذبة لازم تُستثنى
═══════════════════════════════════════════════════════════════
  • **«البلاشر»** = المصابيح، مو «بلاش» — «خلي البلاشر يشتغل»
  • **«بث مجاني»** بفئة `sports_entertainment` — وصف خدمة خارجية
    (يوتيوب/موقع الاتحاد) لا التزام من المحل
  • رسالة النظام نفسها — ما تنلمس أبداً

═══════════════════════════════════════════════════════════════
المعالجة
═══════════════════════════════════════════════════════════════
الوعد غير المؤسَّس ينبدل بصيغة **ما تلتزم برقم ولا بمجانية**، وتحيل
للمحل للتأكيد — نفس منطق «أتأكدلك» بالضمان:

    «الفحص مجاني»  ->  «الفحص عدنا، وأجرته أتأكدلك بيها»
    «التوصيل بلاش» ->  «التوصيل عدنا، وأجرته حسب المنطقة»

الجملة تبقى بيعية وودودة، بس بلا التزام مخترع.
"""
import json
import random
import re
import sys
from collections import Counter
from pathlib import Path

sys.stdout.reconfigure(encoding="utf-8")
random.seed(20260804)

ROOT = Path(__file__).resolve().parent.parent
SRC = ROOT / "data" / "v16"
VAL_FILES = ["iraqi_val_v8.jsonl", "iraqi_val_v13.jsonl",
             "iraqi_v16_val_extra.jsonl", "iraqi_v17_val_extra.jsonl",
             "iraqi_v19_val_extra.jsonl", "iraqi_v20_val_extra.jsonl"]

# ── كشف الوعد ──
# «البلاشر» (المصابيح) مستثناة بـlookahead: بلاش ما يتبعها «ر»
FREE = re.compile(r"ببلاش|بلاش(?!ر)|مجان(ي|ية|اً|ا)?\b|بالمجان|بلا مقابل|"
                  r"على حسابنا|على حسابي")
SYS_FREE = re.compile(r"مجان|بلاش|بلا مقابل|على حسابنا")
# خدمة خارجية لا التزام من المحل
EXTERNAL = re.compile(r"يوتيوب|موقع|تطبيق|قناة|الاتحاد|النت|الانترنت|"
                      r"جوجل|فيسبوك|تلگرام")

# ── بدائل حسب نوع الخدمة ──
REPLACE = [
    # (نمط الوعد، البدائل)
    (re.compile(r"الفحص\s+مجاني\s*،?\s*"),
     ["الفحص عدنا، ", "نفحصه عدنا، ", "الفحص متوفر، "]),
    (re.compile(r"الاستشار[ةه]\s+مجاني[ةه]\s*(دايم\s*)?(عندنا)?\s*"),
     ["نستشيرك بالموجود عدنا", "تدلل نساعدك بالمتوفر عدنا",
      "احنه بالخدمة بالموجود"]),
    (re.compile(r"\s*،?\s*وإذا\s+الطلبي[ةه]\s+كبير[ةه]\s+نوصلها\s+بلاش\s*\.?"),
     ["، وإذا الطلبية كبيرة نتفاهم على الأجرة."]),
    (re.compile(r"التوصيل\s+داخل\s+بغداد\s+بلاش\s*،?\s*"),
     ["التوصيل داخل بغداد أجرته حسب المنطقة، "]),
    (re.compile(r"نوصلها\s+بلاش"), ["نتفاهم على أجرة التوصيل"]),
    (re.compile(r"نوصله\s+بلاش"), ["نتفاهم على أجرة التوصيل"]),
    # «نبدله على حسابنا» — التزام بتحمّل الكلفة، والنظام ما يخوّله.
    # البديل يبقي الاعتذار والاستبدال، وينقل قرار الكلفة للمحل.
    (re.compile(r"ونبدلها\s+على\s+حسابنا"),
     ["ونشوف الحل المناسب الك", "ونعالجها ويّاك بالمحل"]),
    (re.compile(r"ونبدله\s+على\s+حسابنا"),
     ["ونشوف الحل المناسب الك", "ونعالجها ويّاك بالمحل"]),
    (re.compile(r"\s*على\s+حسابنا"), [""]),
    (re.compile(r"\s*بالمجان"), [""]),
    (re.compile(r"\s*مجاناً"), [""]),
    (re.compile(r"\s*ببلاش"), [""]),
    (re.compile(r"\s*بلاش(?!ر)"), [""]),
    (re.compile(r"\s*مجاني[ةه]?\b"), [""]),
]


def defuse(text):
    """ينزع الالتزام المجاني ويخلي الجملة سليمة."""
    out = text
    for rx, opts in REPLACE:
        if rx.search(out):
            out = rx.sub(random.choice(opts), out, count=1)
    out = re.sub(r"\s{2,}", " ", out)
    out = re.sub(r"\s+([،.؟!])", r"\1", out)
    out = re.sub(r"،\s*،", "،", out)
    out = re.sub(r"،\s*\.", ".", out)
    return out.strip(" ،-—")


def process(path, stats):
    rows, changed = [], False
    for line in path.open(encoding="utf-8"):
        d = json.loads(line)
        sysm = " ".join(m["content"] for m in d["messages"]
                        if m["role"] == "system")
        grounded = bool(SYS_FREE.search(sysm))
        msgs = []
        for m in d["messages"]:
            if m["role"] != "assistant" or not FREE.search(m["content"]):
                msgs.append(m)
                continue
            if grounded:
                stats["kept_grounded"] += 1
                msgs.append(m)
                continue
            if EXTERNAL.search(m["content"]):
                stats["kept_external_service"] += 1
                msgs.append(m)
                continue
            t = defuse(m["content"])
            if t and t != m["content"] and not FREE.search(t):
                stats["defused"] += 1
                changed = True
                msgs.append({**m, "content": t})
            else:
                stats["UNRESOLVED"] += 1
                msgs.append(m)
        d["messages"] = msgs
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

    print("=" * 58)
    print("v24 — وعود المجانية تتقيّد بالسستم")
    print("=" * 58)
    for k, v in stats.most_common():
        print(f"  {k:<26}{v:>8,}")


if __name__ == "__main__":
    main()
