# -*- coding: utf-8 -*-
"""v28 — تقييم وعد الحساب النظيف + كثافة اللهجة، بكتالوج وعبارات حصرية وبذرة مختلفة."""
import json
import random
import sys
from collections import Counter
from pathlib import Path

sys.stdout.reconfigure(encoding="utf-8")
sys.path.insert(0, str(Path(__file__).resolve().parent))

import generate_v28_promise_dialect as G          # noqa: E402

DATA = Path(__file__).resolve().parent.parent / "data"

# أزواج غامضة حصرية — ولا واحد منها بالتدريب
G.PAIRS = [
    ("مكيف شباك 2 طن نوع اول (ديجيتال)", 460000,
     "مكيف شباك 2 طن نوع ثاني (عادي)", 350000, "مكيف"),
    ("فرن غاز 5 عيون نوع اول (ستانلس)", 410000,
     "فرن غاز 5 عيون نوع ثاني (عادي)", 320000, "فرن"),
    ("مكنسة كهربائية نوع اول (بلا كيس)", 195000,
     "مكنسة كهربائية نوع ثاني (بكيس)", 140000, "مكنسة"),
]
G.INSTALL_FEE = 30000

# عبارات مجاملة/وداع حصرية — ولا وحدة منها بالتدريب
G.GREET_OPEN = [
    ("هاي، شلون الصحة؟", "هلا وغلا عيني، الحمدلله زين هواي، شلونك انته خويه؟"),
    ("مساء الورد", "مسا الفل عيني، شلون حالك هسه صدگ؟"),
    ("هلو، اشحالكم اليوم", "اهلين خويه، الحمدلله هواي طيبين، شكو ماكو عندك؟"),
]
G.COMPLIMENT_TURN = [
    ("والله خدمة ممتازة، ما گصرتوا وياي",
     "الله يخليكم عيني، هذا واجبنا الك هواي خويه صدگ"),
    ("عجبتني البضاعة كلش، تسلم ايدينكم",
     "الله يسلمك عيني، خدمتك تشرفنا هواي خويه"),
]
G.FAREWELL_TURN = [
    ("زين هسه، الله معك، سلامتكم",
     "الله معاك عيني، تعال بأي وكت هواي خويه"),
    ("يلا فمان الله، اشوفكم بعدين",
     "فمان الله عيني، بانتظارك دايماً خويه هواي"),
]
G.THANKS_SOLO = [
    ("مشكورين هواي على كل شي", "العفو عيني، هواي فرحانين بخدمتك خويه صدگ"),
    ("الله يعطيكم العافية على التعامل", "الله يعافيك عيني، انته اهل الطيبة هواي خويه"),
]


def main():
    random.seed(77028)
    rows, seen = [], set()
    plan = [
        (G.gen_compound_clean_promise,      140),
        (G.gen_direct_clean_promise,         90),
        (G.gen_casual_dialect_dense,         12),
        (G.gen_casual_dialect_dense_short,    2),
    ]
    for fn, n in plan:
        kept = 0
        for r in fn(n * 6):
            if kept >= n:
                break
            k = json.dumps(r["messages"], ensure_ascii=False, sort_keys=True)
            if k in seen:
                continue
            seen.add(k)
            rows.append(r)
            kept += 1

    errs = G.validate(rows)
    p = DATA / "iraqi_v28_val_extra.jsonl"
    with p.open("w", encoding="utf-8") as fh:
        for r in rows:
            fh.write(json.dumps(r, ensure_ascii=False) + "\n")

    print(f"{'✅' if not errs else '❌'} {len(rows)} مثال تقييم -> {p.name}")
    for k, v in Counter(r["category"] for r in rows).most_common():
        print(f"   {k:<32}{v:>5}")
    if errs:
        for k, v in errs.most_common():
            print(f"   ❌ {k:<44}{v:>5}")


if __name__ == "__main__":
    main()
