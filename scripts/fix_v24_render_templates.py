# -*- coding: utf-8 -*-
"""
v24 — تصيير قوالب `{pick([...])}` اللي تسرّبت خام لداتا التدريب.

═══════════════════════════════════════════════════════════════
الخلل
═══════════════════════════════════════════════════════════════
مولّد قديم چان يكتب القالب حرفياً بدل ما ينفّذه، فوصلت للتدريب ردود
فيها **كود بايثون خام**:

    «لازم تجيب تقرير طبي رسمي من {pick(['مستشفى حكومي','طبيب معترف
     به','عيادة مرخصة'])}»

    «هذا غلط منا. نعطيك {pick(['خصم','حصة مجانية','مشروب مجاني'])}
     تعويضاً»

لو تدرّب الموديل عليها راح يتعلم يطلع `{pick([...])}` بردوده — وهذا
أسوأ من أي هلوسة لأنه يكشف آلية التوليد للزبون.

اكتُشف بالصدفة أثناء فحص وعود المجانية (v24): ثلاث حالات ما انحلّت،
وطلع سببها إن «حصة مجانية» و«مشروب مجاني» **داخل قالب** لا داخل جملة.

═══════════════════════════════════════════════════════════════
المعالجة
═══════════════════════════════════════════════════════════════
القالب ينفّذ فعلياً: تُقرأ القائمة بـ`ast.literal_eval` ويُختار منها
عشوائياً. ولأن «حصة مجانية» و«مشروب مجاني» **وعود مجانية غير مؤسَّسة**،
تنشال من القوائم قبل الاختيار — يبقى «خصم» وهو الوحيد اللي ما يلزم
المحل بمجانية.

يشتغل على كل ملفات `data/v16/` وملفات التقييم.
"""
import ast
import json
import random
import re
import sys
from collections import Counter
from pathlib import Path

sys.stdout.reconfigure(encoding="utf-8")
random.seed(20260805)

ROOT = Path(__file__).resolve().parent.parent
SRC = ROOT / "data" / "v16"
VAL_FILES = ["iraqi_val_v8.jsonl", "iraqi_val_v13.jsonl",
             "iraqi_v16_val_extra.jsonl", "iraqi_v17_val_extra.jsonl",
             "iraqi_v19_val_extra.jsonl", "iraqi_v20_val_extra.jsonl"]

PICK = re.compile(r"\{pick\((\[[^\]]*\])\)\}")
# خيارات تلزم المحل بمجانية — تنشال من القائمة قبل الاختيار
FREE_OPT = re.compile(r"مجان|بلاش|بلا مقابل")


def render(text):
    def sub(m):
        try:
            opts = ast.literal_eval(m.group(1))
        except Exception:
            return ""
        safe = [o for o in opts if not FREE_OPT.search(str(o))]
        return random.choice(safe or opts)
    out = PICK.sub(sub, text)
    return re.sub(r"\s{2,}", " ", out).strip()


def process(path, stats):
    rows, changed = [], False
    for line in path.open(encoding="utf-8"):
        d = json.loads(line)
        ms = []
        for m in d["messages"]:
            if PICK.search(m["content"]):
                m = {**m, "content": render(m["content"])}
                stats["rendered"] += 1
                changed = True
            ms.append(m)
        d["messages"] = ms
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
    print("=" * 50)
    print(f"v24 — قوالب مُصيَّرة: {stats['rendered']:,}")
    print("=" * 50)


if __name__ == "__main__":
    main()
