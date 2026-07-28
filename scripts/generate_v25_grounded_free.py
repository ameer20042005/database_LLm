# -*- coding: utf-8 -*-
"""
v25 — المجانية المؤسَّسة: يستعملها لمن النظام يخوّله.

═══════════════════════════════════════════════════════════════
المشكلة اللي خلّفتها v24
═══════════════════════════════════════════════════════════════
v24 نزعت 748 وعد مجانية غير مؤسَّس — وهذا صح. بس التغطية المقابلة
**ضعيفة جداً**:

    محادثات فيها رسالة نظام:            20,527
      النظام يذكر مجانية:                  252  (1.2%)
        والمساعد يستعملها فعلاً:            23  (0.1%)

يعني الموديل يشوف «لا تعد بمجانية» بـ748 مثالاً، ويشوف «استعملها لمن
تكون مكتوبة» بـ23 مثالاً بس. النسبة 32:1 تعلّمه **قاعدة مطلقة خاطئة**:
«ما تگول بلاش أبداً» بدل «گولها إذا النظام يخوّلك».

وهذا يضر البيع: زبون داخل بغداد يسأل عن التوصيل، والنظام يگول «داخل
بغداد: مجاني»، والموديل يتهرب أو يحيل — بينما الجواب الصح موجود
گدامه.

═══════════════════════════════════════════════════════════════
المعالجة
═══════════════════════════════════════════════════════════════
دفعة أمثلة **النظام فيها مجانية صريحة، والمساعد ينقلها حرفياً**:

  • توصيل مجاني داخل مدينة معينة
  • تركيب مجاني مع الشراء
  • فحص مجاني قبل التصليح
  • توصيل مجاني فوق مبلغ معين

وحالة الحدّ المهمة: **الزبون يسأل عن مجانية مو مذكورة** بنفس النظام
اللي يذكر غيرها — «التوصيل مجاني، بس التركيب؟» — الجواب: ينقل المؤسَّس
ويحيل بالباقي. هذا يعلّم **التمييز** لا القاعدة المطلقة.
"""
import json
import random
import re
import sys
from collections import Counter
from pathlib import Path

sys.stdout.reconfigure(encoding="utf-8")
random.seed(20260806)

DATA = Path(__file__).resolve().parent.parent / "data" / "v16"

PRODUCTS = [
    ("ثلاجة بيكو 16 قدم", 730000), ("غسالة هاير 9 كغم اوتوماتيك", 495000),
    ("مكيف سبلت 1.5 طن انفرتر", 550000), ("تلفزيون هايسنس 43 بوصة", 680000),
    ("فريزر زانوسي 400 لتر", 585000), ("طباخ بيكو 5 عيون", 295000),
    ("سخان كهربائي 80 لتر", 165000), ("مكيف ألتون 2 طن سبلت", 815000),
]
CITIES = ["بغداد", "البصرة", "أربيل", "الموصل", "النجف", "كربلاء"]
OUT_FEE = [15000, 20000, 25000, 10000]


def money(n):
    return f"{n:,}"


# ── أنواع المجانية المؤسَّسة ──
def sys_delivery(city, fee):
    (p1, v1), (p2, v2) = random.sample(PRODUCTS, 2)
    return (f"""أنت موظف مبيعات بمحل عراقي.

الموجود حالياً:
- {p1}: {money(v1)} دينار
- {p2}: {money(v2)} دينار
- التوصيل داخل {city}: مجاني | خارج {city}: {money(fee)} دينار

انسخ الأسعار والأسماء حرفياً من القائمة. إذا انسألت عن معلومة مو مكتوبة بالقائمة گول أتأكدلك وأرد عليك — لا تخترع رقم ولا تعد بشي مو مكتوب.""",
            (p1, v1), (p2, v2))


def sys_install(city):
    (p1, v1), (p2, v2) = random.sample(PRODUCTS, 2)
    return (f"""أنت موظف مبيعات بمحل عراقي.

الموجود حالياً:
- {p1}: {money(v1)} دينار
- {p2}: {money(v2)} دينار
- التركيب: مجاني مع الشراء داخل {city}

انسخ الأسعار والأسماء حرفياً من القائمة. إذا انسألت عن معلومة مو مكتوبة بالقائمة گول أتأكدلك وأرد عليك — لا تخترع رقم ولا تعد بشي مو مكتوب.""",
            (p1, v1), (p2, v2))


def sys_threshold(limit, fee):
    (p1, v1), (p2, v2) = random.sample(PRODUCTS, 2)
    return (f"""أنت موظف مبيعات بمحل عراقي.

الموجود حالياً:
- {p1}: {money(v1)} دينار
- {p2}: {money(v2)} دينار
- التوصيل: {money(fee)} دينار، ومجاني إذا المشتريات فوق {money(limit)} دينار

انسخ الأسعار والأسماء حرفياً من القائمة. إذا انسألت عن معلومة مو مكتوبة بالقائمة گول أتأكدلك وأرد عليك — لا تخترع رقم ولا تعد بشي مو مكتوب.""",
            (p1, v1), (p2, v2))


def rec(cat, msgs):
    return {"category": cat, "messages": msgs}


# ════════ ١) توصيل مجاني داخل المدينة ════════
Q_IN = ["التوصيل لـ{c} شكد؟", "توصلون لـ{c}؟ وبيش؟",
        "أني من {c}، التوصيل عليه أجرة؟", "شكد أجرة التوصيل لـ{c}؟"]
A_IN = ["داخل {c} التوصيل مجاني عيني",
        "إي نوصلك، وداخل {c} التوصيل مجاني",
        "تدلل، داخل {c} ما عليك أجرة توصيل — مجاني",
        "داخل {c} مجاني عيني، هذا المكتوب عندي"]
Q_OUT = ["أني من {o}، التوصيل شكد؟", "توصلون لـ{o}؟ بيش الأجرة؟"]
A_OUT = ["خارج {c} التوصيل بـ{f} دينار عيني",
        "لـ{o} الأجرة {f} دينار، أما داخل {c} فمجاني",
        "برّه {c} يطلع {f} دينار عيني"]


def gen_delivery(n):
    out = []
    for _ in range(n):
        city = random.choice(CITIES)
        fee = random.choice(OUT_FEE)
        sysm, (p1, v1), _ = sys_delivery(city, fee)
        if random.random() < 0.6:
            msgs = [
                {"role": "system", "content": sysm},
                {"role": "user", "content": f"شكد سعر {p1}؟"},
                {"role": "assistant", "content": f"{p1} بـ{money(v1)} دينار عيني"},
                {"role": "user", "content": random.choice(Q_IN).format(c=city)},
                {"role": "assistant", "content": random.choice(A_IN).format(c=city)},
            ]
        else:
            other = random.choice([c for c in CITIES if c != city])
            msgs = [
                {"role": "system", "content": sysm},
                {"role": "user", "content": random.choice(Q_OUT).format(o=other)},
                {"role": "assistant",
                 "content": random.choice(A_OUT).format(c=city, o=other, f=money(fee))},
            ]
        out.append(rec("grounded_free_delivery", msgs))
    return out


# ════════ ٢) تركيب مجاني ════════
Q_INST = ["التركيب عليه أجرة؟", "شكد التركيب؟", "تركبونه؟ وبيش؟",
          "التركيب محسوب لو زيادة؟"]
A_INST = ["التركيب مجاني مع الشراء داخل {c} عيني",
          "لا عيني، التركيب مجاني إذا تشتري منا وانت داخل {c}",
          "تدلل، التركيب مجاني مع الشراء داخل {c}"]


def gen_install(n):
    out = []
    for _ in range(n):
        city = random.choice(CITIES)
        sysm, (p1, v1), _ = sys_install(city)
        out.append(rec("grounded_free_install", [
            {"role": "system", "content": sysm},
            {"role": "user", "content": f"بيش {p1}؟"},
            {"role": "assistant", "content": f"{p1} بـ{money(v1)} دينار عيني"},
            {"role": "user", "content": random.choice(Q_INST)},
            {"role": "assistant", "content": random.choice(A_INST).format(c=city)},
        ]))
    return out


# ════════ ٣) مجانية فوق حدّ ════════
def gen_threshold(n):
    out = []
    for _ in range(n):
        limit = random.choice([200000, 300000, 500000])
        fee = random.choice(OUT_FEE)
        sysm, (p1, v1), _ = sys_threshold(limit, fee)
        above = v1 > limit
        q = random.choice(["التوصيل شكد؟", "أجرة التوصيل بيش؟",
                           "توصلون؟ وشكد الأجرة؟"])
        if above:
            a = (f"مشترياتك فوق {money(limit)} دينار، فالتوصيل مجاني عيني")
        else:
            a = (f"التوصيل {money(fee)} دينار عيني، ويصير مجاني إذا "
                 f"مشترياتك فوق {money(limit)} دينار")
        out.append(rec("grounded_free_threshold", [
            {"role": "system", "content": sysm},
            {"role": "user", "content": f"شكد {p1}؟"},
            {"role": "assistant", "content": f"{p1} بـ{money(v1)} دينار"},
            {"role": "user", "content": q},
            {"role": "assistant", "content": a},
        ]))
    return out


# ════════ ٤) حالة الحدّ: مجانية مذكورة وأخرى لا ════════
# هذي الأهم — تعلّم **التمييز** لا القاعدة المطلقة.
EDGE_Q = [("التركيب مجاني هم؟", "التركيب"),
          ("والضمان مجاني؟", "الضمان"),
          ("التغليف مجاني؟", "التغليف"),
          ("الصيانة مجانية؟", "الصيانة")]
EDGE_A = [
    "التوصيل داخل {c} مجاني هذا مكتوب عندي، أما {t} فما مذكور — أتأكدلك وأرد عليك",
    "المكتوب عندي التوصيل مجاني داخل {c} بس، و{t} ما عندي عليه معلومة — أسأل وأرجعلك",
    "داخل {c} التوصيل مجاني إي، بس {t} مو موضح عندي عيني، اتأكدلك",
]


def gen_edge(n):
    out = []
    for _ in range(n):
        city = random.choice(CITIES)
        fee = random.choice(OUT_FEE)
        sysm, (p1, v1), _ = sys_delivery(city, fee)
        q, topic = random.choice(EDGE_Q)
        out.append(rec("grounded_free_edge", [
            {"role": "system", "content": sysm},
            {"role": "user", "content": f"شكد {p1}؟ والتوصيل؟"},
            {"role": "assistant",
             "content": f"{p1} بـ{money(v1)} دينار، وداخل {city} التوصيل مجاني عيني"},
            {"role": "user", "content": q},
            {"role": "assistant",
             "content": random.choice(EDGE_A).format(c=city, t=topic)},
        ]))
    return out


def main():
    rows, seen = [], set()
    plan = [(gen_delivery, 340), (gen_install, 200),
            (gen_threshold, 200), (gen_edge, 260)]
    counts = {}
    for fn, n in plan:
        kept = []
        for r in fn(n * 4):
            if len(kept) >= n:
                break
            k = json.dumps(r["messages"], ensure_ascii=False, sort_keys=True)
            if k in seen:
                continue
            seen.add(k)
            kept.append(r)
        counts[kept[0]["category"]] = len(kept)
        rows.extend(kept)

    random.shuffle(rows)
    p = DATA / "iraqi_v25_grounded_free.jsonl"
    with p.open("w", encoding="utf-8") as fh:
        for r in rows:
            fh.write(json.dumps(r, ensure_ascii=False) + "\n")

    # تحقق: كل رد فيه مجانية لازم نظامه يذكرها
    SYSF = re.compile(r"مجان")
    FREE = re.compile(r"مجان|بلاش")
    bad = 0
    for r in rows:
        sysm = " ".join(m["content"] for m in r["messages"]
                        if m["role"] == "system")
        for m in r["messages"]:
            if m["role"] == "assistant" and FREE.search(m["content"]) \
                    and not SYSF.search(sysm):
                bad += 1
    print("=" * 58)
    print("v25 — المجانية المؤسَّسة")
    print("=" * 58)
    for k, v in counts.items():
        print(f"  {k:<30}{v:>6}")
    print(f"\n  {'✅' if not bad else '❌'} كل مجانية مؤسَّسة بالنظام: "
          f"{len(rows)-bad}/{len(rows)}")
    print(f"  📁 {p.name}")


if __name__ == "__main__":
    main()
