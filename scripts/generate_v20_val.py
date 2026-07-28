# -*- coding: utf-8 -*-
"""v20 — تقييم الكوزمتك وهوية البائع، بقوائم حصرية وبذرة مختلفة."""
import json
import random
import sys
from collections import Counter
from pathlib import Path

sys.stdout.reconfigure(encoding="utf-8")
sys.path.insert(0, str(Path(__file__).resolve().parent))

import generate_v20_cosmetics_identity as G          # noqa: E402

DATA = Path(__file__).resolve().parent.parent / "data"

# ── قوائم حصرية ما تظهر بالتدريب ──
G.COSMETICS = [
    ("كريم ليلي مغذي 60 مل", 16000),
    ("تونر منعش للبشرة", 10500),
    ("سيروم حمض الهيالورونيك", 26000),
    ("شامبو ضد القشرة 300 مل", 9500),
    ("عطر شرقي 75 مل", 55000),
    ("ماسك شعر بالكيراتين", 13000),
]
G.APPLIANCES = [
    ("ثلاجة كونكورد 18 قدم", 640000),
    ("غسالة توشيبا 8 كغم", 520000),
    ("مكيف جنرال 2 طن سبلت", 780000),
    ("تلفزيون شارب 55 بوصة", 700000),
]
G.OFF_Q = [
    ("شنو رايك بسعر صرف الدولار؟", "اسأل صراف أو مختص اقتصاد"),
    ("عندي خلاف بالإرث، شنو أسوي؟", "راجع محامي مختص بالأحوال"),
    ("سقف البيت يرشح، شنو الحل؟", "خلي أسطة بناء يعاينه"),
    ("ولدي ما يحچي لعمره سنتين، طبيعي؟", "راجع طبيب أطفال"),
    ("أريد أسافر، شنو أوراق الفيزا؟", "راجع مكتب سفر أو السفارة"),
    ("حاسوبي بطيء هواي", "وديه لفني صيانة حاسبات"),
]
G.SKIN_Q = [
    "بشرتي جافة هواي بالشتاء، هذا ينفع؟",
    "عندي تهيج بعد الحلاقة، شنو أستعمل؟",
    "شعري متقصف، الماسك يصلحه؟",
]


def main():
    random.seed(66004)
    rows, seen = [], set()
    for fn, n in ((G.gen_normal_sale, 130), (G.gen_therapeutic_edge, 80),
                  (G.gen_seller_identity, 130)):
        kept = 0
        for r in fn(n * 5):
            if kept >= n:
                break
            k = json.dumps(r["messages"], ensure_ascii=False, sort_keys=True)
            if k in seen:
                continue
            seen.add(k)
            rows.append(r)
            kept += 1

    p = DATA / "iraqi_v20_val_extra.jsonl"
    with p.open("w", encoding="utf-8") as fh:
        for r in rows:
            fh.write(json.dumps(r, ensure_ascii=False) + "\n")
    print(f"✅ {len(rows)} مثال تقييم -> {p.name}")
    for k, v in Counter(r["category"] for r in rows).most_common():
        print(f"   {k:<32}{v:>5}")


if __name__ == "__main__":
    main()
