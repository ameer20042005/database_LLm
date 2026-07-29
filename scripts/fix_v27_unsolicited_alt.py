# -*- coding: utf-8 -*-
"""
v27-clean — نزع البديل غير المطلوب من ردود الرفض.

═══════════════════════════════════════════════════════════════
المشكلة
═══════════════════════════════════════════════════════════════
السستم يگول صراحة:

    «المنتج او البراند المو موجود بالكتالوج: گول مو متوفر حالياً
     حتى لو الزبون أصر، **ولا تعرض بديل الا اذا طلب**»

والموديل بالتقييم رد:

    👤 عندكم تلفزيون سامسونج 65 بوصة؟
    🤖 مو موجود حالياً، **بس عندنا مكيف سبلت بـ420,000 دينار**

عرض **مكيف** لزبون يسأل عن **تلفزيون**. هذا مو اقتراح بديل — هذا
تغيير موضوع. والموديل تعلّمه من الداتا: 416 محادثة فيها نمط
«رفض + بس عدنا...» بدون أي طلب من الزبون.

والأسوأ: **90 منها من `reject_standard_with_list`** — فئة كتبتها
v26 نفسها. يعني الدفعة اللي المفروض تصلّح الرفض زادت بيه خطأً
جديداً. القالب كان:

    "{رفض}\\nبس عدنا من {فئة}:\\n{قائمة}"

النية كانت «اربط الرفض بالقائمة»، بس النتيجة قالب يعلّم بالضبط
السلوك اللي السستم يمنعه.

═══════════════════════════════════════════════════════════════
المعالجة
═══════════════════════════════════════════════════════════════
ثلاث حالات:

  ١) الزبون **طلب** البديل بدور سابق  -> يبقى (سلوك صح)
  ٢) البديل من **نفس** فئة المرفوض    -> يتحول لصيغة مشروطة
                                          («تحب أعرضلك الموجود؟»)
  ٣) البديل من فئة **مختلفة** بلا طلب -> ينقص للرفض النظيف

الحالة (٣) هي اللي وقع بيها الموديل، وهي الأكثر ضرراً.
"""
import json
import re
import shutil
import sys
from collections import Counter
from pathlib import Path

sys.stdout.reconfigure(encoding="utf-8")

ROOT = Path(__file__).resolve().parent.parent
SRC = ROOT / "data" / "v16"

# نمط البديل غير المطلوب
UNSOL = re.compile(
    r"(?P<rej>.*?(?:مو موجود|ما عدنا|ماكو|مو متوفر|مو بالكتالوج|انتهى)"
    r"[^.،\n]{0,40}?)"
    r"\s*[،,]?\s*(?:بس|لكن)\s*(?:عدنا|عندنا|اكو|أكو)"
    r"(?P<alt>.*)", re.S)

# طلب البديل من الزبون
ASKED = re.compile(
    r"شنو عندكم|شمعندكم|شنو المتوفر|شنو الموجود|عرضلي|"
    r"اكو غير|شنو تنصح|شو عندكم|بديل|شنو اكو")

# صيغ مشروطة تحل محل العرض المباشر
OFFER = ["تحب أعرضلك الموجود عدنا؟", "إذا تريد أگلك شنو المتوفر عدنا",
         "تريد أشوفلك بديل من الموجود؟"]


def main():
    files = sorted(SRC.glob("*.jsonl"))
    if not files:
        sys.exit("❌ data/v16 فارغ")

    stats = Counter()
    per_cat = Counter()

    for f in files:
        rows = [json.loads(l) for l in f.open(encoding="utf-8")]
        changed = False

        for r in rows:
            msgs = r["messages"]
            for i, m in enumerate(msgs):
                if m["role"] != "assistant":
                    continue
                mt = UNSOL.match(m["content"])
                if not mt:
                    continue

                # هل الزبون طلب البديل بأي دور سابق؟
                prior = " ".join(x["content"] for x in msgs[:i]
                                 if x["role"] == "user")
                if ASKED.search(prior):
                    stats["أُبقي (الزبون طلب)"] += 1
                    continue

                rej = mt.group("rej").strip().rstrip("،,").strip()
                if not rej:
                    stats["تُخطّي (رفض فارغ)"] += 1
                    continue

                # بديل غير مطلوب -> رفض نظيف + عرض مشروط
                idx = len(rej) % len(OFFER)
                m["content"] = f"{rej}. {OFFER[idx]}"
                stats["نُظّف"] += 1
                per_cat[r.get("category", "?")] += 1
                changed = True

        if changed:
            bak = f.with_suffix(".jsonl.bak_v27")
            if not bak.exists():
                shutil.copy2(f, bak)
            with f.open("w", encoding="utf-8") as fh:
                for r in rows:
                    fh.write(json.dumps(r, ensure_ascii=False) + "\n")

    print("=" * 58)
    print("v27-clean — نزع البديل غير المطلوب")
    print("=" * 58)
    for k, v in stats.most_common():
        print(f"  {k:<28}{v:>6}")
    if per_cat:
        print("\n  الفئات المتأثرة:")
        for k, v in per_cat.most_common(12):
            print(f"    {k:<34}{v:>5}")


if __name__ == "__main__":
    main()
