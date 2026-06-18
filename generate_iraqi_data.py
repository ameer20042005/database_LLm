#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Iraqi Arabic Dialect LLM Training Data Generator
مولّد بيانات التدريب - اللهجة العراقية
10 files x 1000 conversations each
"""

import json
import random
import os

random.seed(2024)

# ============================================================
# LOAD WORD BANK FROM word.json
# ============================================================

def _load_words():
    path = os.path.join(os.path.dirname(__file__), "word.json")
    with open(path, encoding="utf-8") as f:
        data = json.load(f)
    cats = {}
    for cat in data:
        cats[cat["category"]] = [item["word"] for item in cat["items"]]
    return cats

_W = _load_words()

def _cat(name):
    return _W.get(name, [])

# ============================================================
# SHARED DATA BANKS
# ============================================================

MALE_CUSTOMERS = [
    "أبو علي","أبو أحمد","أبو محمد","أبو حسين","أبو جعفر",
    "حجي عبدالله","حاجي كريم","حجي ياسر","عمو صالح","عمو رضا",
    "أستاذ علي","الحاج عدنان","أبو يوسف","أبو سعد","أبو عمر",
    "أبو زيد","حجي فلاح","حجي قاسم","عمو جابر","أبو ليث",
    "أبو مصطفى","أبو ناصر","حجي سعيد","أبو رعد","أبو كرار",
    "عمو خليل","أبو تقي","أبو صادق","حجي وداد","أبو بلال",
]

FEMALE_CUSTOMERS = [
    "أم علي","أم أحمد","أم محمد","باجي فاطمة","باجي زينب",
    "حجية أم حسين","أم جعفر","باجي رهام","أم يوسف","باجي سارة",
    "أم عمر","حجية أم كريم","باجي شيماء","أم رعد","باجي نور",
    "أم ليث","باجي علا","حجية أم صالح","أم سعد","باجي ريم",
    "باجي مروة","أم تقي","باجي ياسمين","أم بلال","باجي دينا",
]

SELLERS = [
    "أبو خضر","أبو صباح","حجي جواد","أستاذ حيدر","عمو ثامر",
    "أبو طاهر","حجي منير","أستاذ عباس","أبو فراس","حجي وليد",
    "أبو فؤاد","أستاذ لقمان","عمو تحسين","أبو غسان","حجي نجم",
]

# Paired greetings: (customer, seller_response)
GREET_PAIRS = [
    ("السلام عليكم",          "وعليكم السلام، هلا وغلا! كيف أكدر أساعدك؟"),
    ("السلام عليكم",          "وعليكم السلام ورحمة الله! تفضل أخوي"),
    ("السلام عليكم",          "وعليكم السلام! أهلاً وسهلاً تفضل"),
    ("يا أستاذ، السلام عليكم","وعليكم السلام، هلا بيك! شنو تريد؟"),
    ("هلو",                   "هلا، أهلاً وسهلاً! تفضل شنو تريد؟"),
    ("هلو",                   "هلا هلا! تفضل يا عمو شنو تبي؟"),
    ("مرحبا",                 "مرحبا، هلا وغلا! تفضل"),
    ("مرحبا",                 "مرحبتين! شنو أكدر أساعدك؟"),
    ("أهلاً",                 "أهلاً وسهلاً يا حجي! كيف شلونك؟"),
    ("هلا",                   "هلا بيك! تفضل شتريد؟"),
    ("صباح الخير",            "صباح النور! هلا وغلا تفضل"),
    ("صباح الخير",            "صباح النور يا حجي، شنو تريد؟"),
    ("مساء الخير",            "مساء النور! هلا وسهلاً تفضل"),
    ("مساء الخير",            "مساء النور يا أخوي، أهلاً"),
    ("سلام",                  "هلا بيك! تفضل"),
]

def greet_pair():
    g, r = pick(GREET_PAIRS)
    return g, r

# Keep these for backwards compat where only one is needed
GREET_C = [p[0] for p in GREET_PAIRS]
GREET_S = [p[1] for p in GREET_PAIRS]
SHORT_GREET = [
    "هلو","مرحبا","هلا","صباح الخير","مساء الخير","سلام","هلا بيك",
] + _cat("التحية")[:8]

EXPENSIVE = [
    "هذا غالي هواي","غالي مو طبيعي","والله هذا ما ينفع",
    "هاي زيادة هواي","مو معقول هالسعر","كلش غالي",
    "هذا يطيح منه","ما عندي هالفلوس","صعب شوية على السعر",
    "هاي أكثر مما توقعت","ما تحط سعر أرخص؟",
    "غالي هواي والله","هذا مو معقول أبد","كلش غالي مو طبيعي",
]

DISC_REQ = [
    "تنزل شوية؟","ما تحط سعر أحسن؟","ما تعطيني تخفيض؟",
    "ما تحسن السعر شوية؟","ما تنزل علي؟",
    "ما أكو خصم؟","گول سعر ثاني",
    "ما تعطيني بسعر زين؟","عندك خصم للزبون المعميل؟",
    "نزل السعر شوية","ما أكو عرض؟","سعر خاص ما أكو؟",
]

DISC_YES = [
    "ما أكدر بعد، أنزل عليك شوية بس هاي آخر سعر",
    "لأنك أنت، أنزل بالسعر بس هاي آخر سعر والله",
    "زين، على خاطرك نزل شوي",
    "ماشي بس ما أكدر أنزل أكثر من هيچي",
    "فدوة الك، بس هذا آخر سعر",
    "والله على خاطرك، هذا آخر سعر",
    "ماشي يا حجي، على خاطرك",
    "حاضر، على العين والرأس، بس هذا آخر سعر",
    "تمام، على خاطرك نزلت عليك",
]

DISC_NO = [
    "والله أخوي هذا آخر سعر، ما أكدر أنزل",
    "هذا سعر نار، ما أكدر أنزل عليه",
    "والله ما أكدر، رأس مالي موجود",
    "هذا سعر التكلفة، صعب أنزل عليه",
    "هالسعر ما موجود في السوق، أرخص ما أكو",
    "صدك والله ما أكدر، هذا آخر سعر",
    "مو ممكن أنزل أكثر، هذا آخر سعر",
    "ما يصير أخوي، هذا سعر التكلفة",
]

CLOSE = [
    "الله يبارك فيك، مشكور على التعامل",
    "مبارك عليك، إن شاء الله تنبسط",
    "الله يوفقك، تفضل",
    "مشكور يا حاجي، تعال مرة ثانية",
    "بالعافية عليك، أي شي تريده تعال",
    "مبارك، الله يخليك",
    "الله يوفقك، تسلم",
    "شكراً على تعاملك، تعال مرة ثانية",
    "تسلم وتغنم، حياك الله",
    "ما قصرت، الله يوفقك",
    "يدوم عزك، تفضل",
    "بالتوفيق، تعال بأي وقت",
] + _cat("الوداع") + _cat("عبارات شائعة")[:6]

THINK = [
    "بفكر شوية وأرجع","لازم أستشير","راح أفكر وأرجع إن شاء الله",
    "خلني أشوف أول","محتاج وقت للتفكير","راح أتصل وأعوّد",
    "خليني أفكر","مو هسه، بعدين أقررها",
]

COME_BACK = [
    "ماشي، شوكت تقرر تعال نكمل","تفضل أخوي في أي وقت",
    "باب المحل مفتوح، تعال بأي وقت","حياك الله بأي وقت",
    "تفضل، ولا يهمك","ماشي، أنا موجود",
]

# بنوك إضافية من word.json
PRAISE      = _cat("المدح")
BLAME       = _cat("الذم")
EMOTIONS    = _cat("المشاعر")
DAILY_WORDS = _cat("كلمات يومية شائعة")
CONFIRM     = _cat("الردود")
REJECT      = _cat("الرفض")
TRADE_WORDS = _cat("التجارة والبيع")
SYMPATHY    = _cat("التعاطف والمواساة")
YOUTH_WORDS = _cat("كلمات الشباب")
COMMANDS    = _cat("أوامر")

def pick(lst):
    return random.choice(lst)

def vp(price, lo=0.93, hi=1.07):
    return f"{int(price * random.uniform(lo, hi) / 1000) * 1000:,}"

def howmuch():
    return random.choice(["بيش", "شكد السعر", "بيش سعره", "شكد"])

def praise_word():
    return pick(PRAISE) if PRAISE else "زين"

def daily_filler():
    """كلمة يومية عراقية عشوائية للتنويع"""
    return pick(DAILY_WORDS) if DAILY_WORDS else "والله"

def youth_word():
    return pick(YOUTH_WORDS) if YOUTH_WORDS else "كفو"

def sympathy_phrase():
    return pick(SYMPATHY) if SYMPATHY else "الله يوفقك"

# ============================================================
# FILE 1 - ELECTRONICS SALES
# ============================================================

PHONES = [
    {"n":"موبايل سامسونج S24","p":750000,"f":["كاميرا 50 ميگاپيكسل","ذاكرة 256 گيگا","بطارية 5000"]},
    {"n":"موبايل سامسونج A54","p":350000,"f":["كاميرا 64 ميگا","ذاكرة 128 گيگا","شاشة AMOLED"]},
    {"n":"آيفون 15","p":1200000,"f":["شريحة A16 بيونيك","كاميرا برو ماكس","Dynamic Island"]},
    {"n":"آيفون 14","p":900000,"f":["شريحة A15","كاميرا ممتازة","وجه ID"]},
    {"n":"موبايل شاومي 13","p":280000,"f":["كاميرا Leica","شحن 67 واط","ذاكرة 128 گيگا"]},
    {"n":"موبايل أوپو Reno 10","p":320000,"f":["زوم 3x","كاميرا 64 ميگا","شاشة 6.7 إنش"]},
    {"n":"موبايل ريلمي 11 Pro","p":220000,"f":["كاميرا 200 ميگا","شحن 67 واط","شاشة 120Hz"]},
    {"n":"موبايل تكنو Spark 20","p":150000,"f":["كاميرا 50 ميگا","بطارية 5000","ذاكرة 128 گيگا"]},
    {"n":"موبايل هواوي P60","p":600000,"f":["كاميرا Leica Pro","شاشة OLED","معالج سريع"]},
    {"n":"موبايل إنفينيكس Hot 30","p":130000,"f":["بطارية 6000 ملي","شاشة 90Hz","ذاكرة 128 گيگا"]},
    {"n":"موبايل فيفو V29","p":300000,"f":["كاميرا 50 ميگا","شحن فلاش 80 واط","شاشة AMOLED"]},
    {"n":"موبايل نوكيا G60","p":180000,"f":["أندرويد نظيف","بطارية 4500","ذاكرة 128 گيگا"]},
]

LAPTOPS = [
    {"n":"لابتوب HP Core i5","p":650000,"f":["رام 8 گيگا","SSD 256 گيگا","شاشة 15.6 إنش"]},
    {"n":"لابتوب Dell Core i7","p":850000,"f":["رام 16 گيگا","SSD 512 گيگا","گارد مستقل"]},
    {"n":"لابتوب Lenovo Core i5","p":580000,"f":["رام 8 گيگا","هارد 1 تيرا","شاشة فول HD"]},
    {"n":"لابتوب Asus Core i7","p":920000,"f":["رام 16 گيگا","SSD 512 گيگا","گارد RTX 3050"]},
    {"n":"ماك بوك Air M2","p":1500000,"f":["شريحة M2","رام 8 گيگا","SSD 256 گيگا"]},
    {"n":"لابتوب Acer Core i5","p":520000,"f":["رام 8 گيگا","SSD 256 گيگا","ويندوز 11"]},
]

TVS = [
    {"n":"تلفزيون سامسونج 55 إنش","p":800000,"f":["4K UHD","سمارت TV","HDR10"]},
    {"n":"تلفزيون LG OLED 55","p":1200000,"f":["OLED","4K","ThinQ AI"]},
    {"n":"تلفزيون TCL 65 إنش","p":700000,"f":["4K","سمارت","Dolby Audio"]},
    {"n":"تلفزيون هايسينس 50 إنش","p":450000,"f":["4K","سمارت TV","واي فاي مدمج"]},
    {"n":"تلفزيون سوني 55 إنش","p":950000,"f":["4K OLED","Google TV","Bravia XR"]},
]

ALL_ELEC = PHONES + LAPTOPS + TVS

def gen_elec(i):
    p = pick(ALL_ELEC)
    p2 = pick(ALL_ELEC)
    while p2["n"] == p["n"]:
        p2 = pick(ALL_ELEC)
    cust = pick(MALE_CUSTOMERS + FEMALE_CUSTOMERS)
    tpl = random.randint(1, 25)

    if tpl == 1:
        _gc, _gs = greet_pair()
        msgs = [
            {"role":"user","content":_gc},
            {"role":"assistant","content":_gs},
            {"role":"user","content":f"أريد {p['n']}، عندكم؟"},
            {"role":"assistant","content":f"إي أكو، {p['n']} جديد وبالكرتون. سعره {vp(p['p'])} دينار. {p['f'][0]} و{p['f'][1]}"},
            {"role":"user","content":f"{pick(EXPENSIVE)}"},
            {"role":"assistant","content":f"{pick(DISC_NO)}"},
            {"role":"user","content":"زين، هاي الفلوس"},
            {"role":"assistant","content":f"{pick(CLOSE)}"},
        ]
    elif tpl == 2:
        _gc, _gs = greet_pair()
        msgs = [
            {"role":"user","content":_gc},
            {"role":"assistant","content":_gs},
            {"role":"user","content":f"{howmuch()} {p['n']}؟"},
            {"role":"assistant","content":f"{p['n']} بـ{vp(p['p'])} دينار يا أخوي. {p['f'][0]}"},
            {"role":"user","content":f"{pick(DISC_REQ)}"},
            {"role":"assistant","content":f"{pick(DISC_YES)}"},
            {"role":"user","content":"اتفقنا، اخذ"},
            {"role":"assistant","content":f"{pick(CLOSE)}"},
        ]
    elif tpl == 3:
        _gc, _gs = greet_pair()
        msgs = [
            {"role":"user","content":_gc},
            {"role":"assistant","content":_gs},
            {"role":"user","content":f"شنو الفرق بين {p['n']} و{p2['n']}؟"},
            {"role":"assistant","content":f"{p['n']} بـ{vp(p['p'])} وعنده {p['f'][0]}. أما {p2['n']} بـ{vp(p2['p'])} وعنده {p2['f'][0]}"},
            {"role":"user","content":"يا واحد أحسن؟"},
            {"role":"assistant","content":f"والله لو بيدي أنصحك بـ{p['n']} لأن {p['f'][0]} وسعره معقول"},
            {"role":"user","content":f"زين، أاخذ {p['n']}"},
            {"role":"assistant","content":f"{pick(CLOSE)}"},
        ]
    elif tpl == 4:
        _gc, _gs = greet_pair()
        msgs = [
            {"role":"user","content":_gc},
            {"role":"assistant","content":_gs},
            {"role":"user","content":f"{p['n']} عنده ضمان؟"},
            {"role":"assistant","content":f"إي، {p['n']} عنده ضمان سنة كاملة. أي عطل نصلحه بالمجان"},
            {"role":"user","content":"وسعره بيش؟"},
            {"role":"assistant","content":f"سعره {vp(p['p'])} دينار. {p['f'][0]} و{p['f'][1]}"},
            {"role":"user","content":f"{pick(DISC_REQ)}"},
            {"role":"assistant","content":f"{pick(DISC_YES)}"},
            {"role":"user","content":"ماشي، خذ الفلوس"},
            {"role":"assistant","content":f"{pick(CLOSE)}"},
        ]
    elif tpl == 5:
        _gc, _gs = greet_pair()
        msgs = [
            {"role":"user","content":_gc},
            {"role":"assistant","content":_gs},
            {"role":"user","content":f"أشوف {p['n']} بس"},
            {"role":"assistant","content":f"تفضل، هاي {p['n']}. {p['f'][0]} و{p['f'][1]} و{p['f'][2] if len(p['f'])>2 else p['f'][0]}"},
            {"role":"user","content":f"{howmuch()}؟"},
            {"role":"assistant","content":f"{vp(p['p'])} دينار"},
            {"role":"user","content":f"{pick(THINK)}"},
            {"role":"assistant","content":f"{pick(COME_BACK)}"},
        ]
    elif tpl == 6:
        msgs = [
            {"role":"user","content":f"{pick(SHORT_GREET)}، أريد {p['n']} بس ما عندي ناقص فلوس"},
            {"role":"assistant","content":f"بيش عندك؟ سعره {vp(p['p'])} دينار"},
            {"role":"user","content":"عندي نص السعر تقريباً"},
            {"role":"assistant","content":"والله أخوي ما عندنا تقسيط بس لو تجيب كمالة الفلوس الأمر لك"},
            {"role":"user","content":"زين، راح أكمل وأجي"},
            {"role":"assistant","content":"حياك الله بأي وقت، البضاعة موجودة"},
        ]
    elif tpl == 7:
        msgs = [
            {"role":"user","content":f"مرحبا، أريد {p['n']} هدية لولدي"},
            {"role":"assistant","content":f"هلا، {p['n']} هدية زينة! سعره {vp(p['p'])} دينار وعنده {p['f'][0]}"},
            {"role":"user","content":"يعني جيد إنه هدية؟"},
            {"role":"assistant","content":f"إي والله، {p['n']} ممتاز. ولدك راح ينبسط هواي"},
            {"role":"user","content":f"{pick(DISC_REQ)}"},
            {"role":"assistant","content":f"{pick(DISC_YES)}"},
            {"role":"user","content":"الله يخليك، خذ"},
            {"role":"assistant","content":f"{pick(CLOSE)}"},
        ]
    elif tpl == 8:
        msgs = [
            {"role":"user","content":f"هلو، عندكم {p['n']} جديد ولا مستعمل؟"},
            {"role":"assistant","content":f"عندنا جديد بالكرتون بـ{vp(p['p'])} دينار، ومستعمل بحالة زينة بـ{vp(int(p['p']*0.6))} دينار"},
            {"role":"user","content":"شنو الفرق الجديد والمستعمل؟"},
            {"role":"assistant","content":f"الجديد معه ضمان سنة وعلبته مگفلة. المستعمل شغال زين بس بدون ضمان"},
            {"role":"user","content":"أاخذ الجديد"},
            {"role":"assistant","content":f"خيار زين! {pick(CLOSE)}"},
        ]
    elif tpl == 9:
        msgs = [
            {"role":"user","content":f"{pick(SHORT_GREET)}، موبايلي انكسر، أريد بديل"},
            {"role":"assistant","content":f"هلا، شنو موبايلك القديم؟ وشنو ميزانيتك؟"},
            {"role":"user","content":"كان سامسونج قديم، ميزانيتي 300 ألف دينار تقريباً"},
            {"role":"assistant","content":f"عندنا {p['n']} بـ{vp(min(p['p'], 300000))} دينار. {p['f'][0]} وجيد للاستخدام اليومي"},
            {"role":"user","content":"هاي مناسب، أاخذه"},
            {"role":"assistant","content":f"{pick(CLOSE)}"},
        ]
    elif tpl == 10:
        _gc, _gs = greet_pair()
        msgs = [
            {"role":"user","content":_gc},
            {"role":"assistant","content":_gs},
            {"role":"user","content":f"شنو أحسن {p['n']} عندكم؟"},
            {"role":"assistant","content":f"أحسن واحد عندنا هو {p['n']} بـ{vp(p['p'])} دينار. {p['f'][0]} و{p['f'][1]}"},
            {"role":"user","content":f"{pick(DISC_REQ)}"},
            {"role":"assistant","content":f"{pick(DISC_NO)}"},
            {"role":"user","content":"زين ماشي"},
            {"role":"assistant","content":f"{pick(CLOSE)}"},
        ]
    elif tpl == 11:
        msgs = [
            {"role":"user","content":f"هلو، عندكم كفر أو سماعة لـ{p['n']}؟"},
            {"role":"assistant","content":f"إي عندنا ملحقات أصلية لـ{p['n']}. الكفر بـ{vp(10000)} والسماعة بـ{vp(20000)} دينار"},
            {"role":"user","content":"الكفر أصلي ولا تقليد؟"},
            {"role":"assistant","content":"أصلي من الشركة، مو تقليد. ضمانه 6 أشهر"},
            {"role":"user","content":"أاخذ الكفر والسماعة مع بعض"},
            {"role":"assistant","content":f"{vp(28000)} دينار الاثنين مع بعض. {pick(CLOSE)}"},
        ]
    elif tpl == 12:
        p3 = pick(ALL_ELEC)
        while p3["n"] in [p["n"], p2["n"]]:
            p3 = pick(ALL_ELEC)
        msgs = [
            {"role":"user","content":f"عندكم 3 خيارات لـ{p['n']}؟ أريد أقارن"},
            {"role":"assistant","content":f"تفضل:\n1. {p['n']} بـ{vp(p['p'])} دينار\n2. {p2['n']} بـ{vp(p2['p'])} دينار\n3. {p3['n']} بـ{vp(p3['p'])} دينار"},
            {"role":"user","content":"أيهم تنصحني؟"},
            {"role":"assistant","content":f"الأفضل حسب الميزانية. لو ميزانيتك عالية: {p['n']}. لو متوسطة: {p2['n']}"},
            {"role":"user","content":f"خذ، اخذ {p2['n']}"},
            {"role":"assistant","content":f"{pick(CLOSE)}"},
        ]
    elif tpl == 13:
        msgs = [
            {"role":"user","content":f"أريد {p['n']} هدية عرس لأخوي"},
            {"role":"assistant","content":f"مبارك! {p['n']} هدية ممتازة. عندنا بالكرتون مع كيس هدية وورقة تهنئة"},
            {"role":"user","content":"كم يطلع؟"},
            {"role":"assistant","content":f"{vp(p['p'])} دينار شامل التغليف"},
            {"role":"user","content":f"{pick(DISC_REQ)}"},
            {"role":"assistant","content":f"{pick(DISC_YES)}"},
            {"role":"user","content":"الله يخلي أخوي، هاي"},
            {"role":"assistant","content":f"مبارك بالعرس! {pick(CLOSE)}"},
        ]
    elif tpl == 14:
        qty_bulk = random.randint(3, 10)
        msgs = [
            {"role":"user","content":f"هلو، أريد أشتري {qty_bulk} حبات {p['n']} لمحلي"},
            {"role":"assistant","content":f"بالجملة؟ ماشي، سعر القطعة {vp(p['p'])} دينار بس لو {qty_bulk} قطع نعطيك خصم"},
            {"role":"user","content":"شكد الخصم؟"},
            {"role":"assistant","content":f"10% خصم، يعني {vp(p['p']*0.9)} للقطعة. الكل {vp(p['p']*0.9*qty_bulk)} دينار"},
            {"role":"user","content":"ماشي، أشتري"},
            {"role":"assistant","content":f"{pick(CLOSE)}"},
        ]
    elif tpl == 15:
        msgs = [
            {"role":"user","content":f"عندي {p['n']} معطل، تشترونه؟"},
            {"role":"assistant","content":"إي نشتري مستعمل. شنو المشكلة؟"},
            {"role":"user","content":"الشاشة مكسورة بس الباقي شغال"},
            {"role":"assistant","content":f"نقدر نشتريه بـ{vp(int(p['p']*0.3))} دينار كعطلان. أو تبدله بـ{p2['n']} جديد وتدفع الفرق"},
            {"role":"user","content":"شكد الفرق؟"},
            {"role":"assistant","content":f"{vp(p2['p'] - int(p['p']*0.3))} دينار تكمّل"},
        ]
    elif tpl == 16:
        msgs = [
            {"role":"user","content":f"أريد {p['n']} بس أريده يوصلني للبيت"},
            {"role":"assistant","content":"إي عندنا توصيل. وين تسكن؟"},
            {"role":"user","content":"الكرادة"},
            {"role":"assistant","content":f"التوصيل للكرادة 5000 دينار. الكل {vp(p['p'] + 5000)} دينار"},
            {"role":"user","content":"ماشي"},
            {"role":"assistant","content":"زين، أعطيني رقمك والعنوان ونوصل خلال ساعتين"},
        ]
    elif tpl == 17:
        msgs = [
            {"role":"user","content":f"أريد {p['n']} بس أريد أعرف تفاصيل الكاميرا"},
            {"role":"assistant","content":f"{p['n']} عنده {p['f'][0]}. كاميرا خلفية ممتازة للتصوير في الضوء الخافت"},
            {"role":"user","content":"والفيديو؟"},
            {"role":"assistant","content":"يسجل 4K و60 فريم بالثانية"},
            {"role":"user","content":"هذا كافي، بيش؟"},
            {"role":"assistant","content":f"{vp(p['p'])} دينار. وعنده ضمان سنة"},
        ]
    elif tpl == 18:
        msgs = [
            {"role":"user","content":f"أريد {p['n']} بس أريد ذاكرة أكبر، عندكم {p['f'][1] if len(p['f'])>1 else '256 گيگا'}؟"},
            {"role":"assistant","content":f"إي عندنا نسخة أكبر. {p['n']} {p['f'][1] if len(p['f'])>1 else '256 گيگا'} بـ{vp(int(p['p']*1.15))} دينار"},
            {"role":"user","content":"الفرق شكد؟"},
            {"role":"assistant","content":f"{vp(int(p['p']*0.15))} دينار إضافة للذاكرة الأكبر"},
            {"role":"user","content":"يستاهل؟"},
            {"role":"assistant","content":"إي والله، الذاكرة الكبيرة توفر عليك المشاكل"},
        ]
    elif tpl == 19:
        msgs = [
            {"role":"user","content":f"هلو، {p['n']} يشتغل على شبكات العراق؟"},
            {"role":"assistant","content":f"إي، {p['n']} يشتغل على 4G العراق. زين وايز وأورانج كلهم يشتغلون"},
            {"role":"user","content":"ومحتاج إعدادات خاصة؟"},
            {"role":"assistant","content":"لا، تركيب الشريحة وبشتغل حالاً. بس نبدل إعداد APN بسيط"},
            {"role":"user","content":"ماشي، هذا مهم. هاي الفلوس"},
            {"role":"assistant","content":f"{pick(CLOSE)}"},
        ]
    elif tpl == 20:
        msgs = [
            {"role":"user","content":f"هلو، شنو الفرق بين {p['n']} الإصدار القديم والجديد؟"},
            {"role":"assistant","content":f"الجديد تحسنت به الكاميرا وأسرع وبطاريته أكبر. القديم أرخص بـ{vp(int(p['p']*0.2))} دينار"},
            {"role":"user","content":"الجديد يستاهل الفرق؟"},
            {"role":"assistant","content":"لو تستخدمه للكاميرا والألعاب، إي يستاهل. لو للمكالمات بس، القديم كافي"},
            {"role":"user","content":"أاخذ الجديد"},
            {"role":"assistant","content":f"{pick(CLOSE)}"},
        ]
    elif tpl == 21:
        msgs = [
            {"role":"user","content":f"أريد فاتورة رسمية مع {p['n']}"},
            {"role":"assistant","content":"إي نعطيك فاتورة من المحل مع بيانات الضمان"},
            {"role":"user","content":"وضمان الشركة؟"},
            {"role":"assistant","content":f"ضمان الشركة سنة كاملة. الفاتورة عليها رقم المنتج وتاريخ الشراء"},
            {"role":"user","content":"ممتاز، هاي الفلوس"},
            {"role":"assistant","content":f"{pick(CLOSE)}"},
        ]
    elif tpl == 22:
        msgs = [
            {"role":"user","content":f"لو {p['n']} يخرب بعد الضمان، شنو؟"},
            {"role":"assistant","content":"عندنا مركز صيانة خاص بيتا. أجرة الصيانة معقولة"},
            {"role":"user","content":"وقطع الغيار موجودة؟"},
            {"role":"assistant","content":"إي، قطع غيار أصلية موجودة لأغلب الأجهزة"},
            {"role":"user","content":"زين، هذا مريح. أاخذه"},
            {"role":"assistant","content":f"{pick(CLOSE)}"},
        ]
    elif tpl == 23:
        installment = vp(p['p'] // 12)
        msgs = [
            {"role":"user","content":f"أريد {p['n']} بالتقسيط"},
            {"role":"assistant","content":f"إي عندنا تقسيط. مقدم {vp(int(p['p']*0.25))} والباقي 12 شهر"},
            {"role":"user","content":"شكد القسط الشهري؟"},
            {"role":"assistant","content":f"حوالي {installment} دينار شهرياً"},
            {"role":"user","content":"فائدة؟"},
            {"role":"assistant","content":"8% فائدة سنوية"},
            {"role":"user","content":"ماشي، أبدأ التقسيط"},
            {"role":"assistant","content":"زين، جيب هوية وتوقيع على العقد"},
        ]
    elif tpl == 24:
        msgs = [
            {"role":"user","content":f"هلو، {p['n']} بيه ألوان متعددة؟"},
            {"role":"assistant","content":f"إي عندنا {p['n']} بألوان: أسود، أبيض، وأزرق. أيهم تحب؟"},
            {"role":"user","content":"أريد الأسود"},
            {"role":"assistant","content":f"الأسود متوفر. {vp(p['p'])} دينار"},
            {"role":"user","content":f"{pick(DISC_REQ)}"},
            {"role":"assistant","content":f"{pick(DISC_YES)}"},
            {"role":"user","content":"ماشي خذ"},
            {"role":"assistant","content":f"{pick(CLOSE)}"},
        ]
    else:
        msgs = [
            {"role":"user","content":f"مرحبا، أريد {p['n']} لشركتي، عندكم فاتورة رسمية؟"},
            {"role":"assistant","content":f"إي عندنا. {p['n']} بـ{vp(p['p'])} دينار مع فاتورة رسمية"},
            {"role":"user","content":"نريد 5 حبات"},
            {"role":"assistant","content":f"بالجملة الكل {vp(p['p']*5*0.9)} دينار مع خصم 10%"},
            {"role":"user","content":"ماشي، اتفقنا"},
            {"role":"assistant","content":f"{pick(CLOSE)}"},
        ]

    return {"id":f"elec_{i:04d}","category":"sales_electronics","dialect":"iraqi_arabic","messages":msgs}

# ============================================================
# FILE 2 - FOOD & GROCERY SALES
# ============================================================

FOOD_ITEMS = [
    {"n":"رز عنبر","unit":"كيلو","p":5000,"u":"دينار"},
    {"n":"رز بسمتي","unit":"كيلو","p":8000,"u":"دينار"},
    {"n":"دهن نباتي","unit":"كيلو","p":6000,"u":"دينار"},
    {"n":"زيت طعام","unit":"لتر","p":7000,"u":"دينار"},
    {"n":"سكر","unit":"كيلو","p":2500,"u":"دينار"},
    {"n":"طحين","unit":"كيلو","p":2000,"u":"دينار"},
    {"n":"شاي أحمر","unit":"علبة","p":8000,"u":"دينار"},
    {"n":"شاي أخضر","unit":"علبة","p":6000,"u":"دينار"},
    {"n":"حليب حليمة","unit":"كرتون","p":12000,"u":"دينار"},
    {"n":"ماء معدني","unit":"كرتون 12","p":5000,"u":"دينار"},
    {"n":"معكرونة","unit":"كيلو","p":3000,"u":"دينار"},
    {"n":"طماطة","unit":"كيلو","p":3500,"u":"دينار"},
    {"n":"بصل","unit":"كيلو","p":2000,"u":"دينار"},
    {"n":"بطاطا","unit":"كيلو","p":2500,"u":"دينار"},
    {"n":"دجاج","unit":"كيلو","p":9000,"u":"دينار"},
    {"n":"لحم عجل","unit":"كيلو","p":25000,"u":"دينار"},
    {"n":"سمك مسگوف","unit":"كيلو","p":30000,"u":"دينار"},
    {"n":"كيك جاهز","unit":"قطعة","p":5000,"u":"دينار"},
    {"n":"خبز تنور","unit":"رقيفة","p":500,"u":"دينار"},
    {"n":"بيض","unit":"طبق 30","p":10000,"u":"دينار"},
]

FOOD_TEMPLATES_EXTRA = [
    "شنو عندكم طازج اليوم؟",
    "كيلو {n} {howmuch()}؟",
    "أريد {qty} كيلو {n}",
    "هذا {n} طازج؟",
    "{n} من وين جاي؟",
    "عندكم {n} بيشيات؟",
]

def gen_food(i):
    item = pick(FOOD_ITEMS)
    item2 = pick(FOOD_ITEMS)
    qty = random.randint(1, 10)
    tpl = random.randint(1, 25)

    if tpl == 1:
        _gc, _gs = greet_pair()
        msgs = [
            {"role":"user","content":_gc},
            {"role":"assistant","content":_gs},
            {"role":"user","content":f"{howmuch()} كيلو {item['n']}؟"},
            {"role":"assistant","content":f"{item['n']} بـ{vp(item['p'])} دينار الكيلو"},
            {"role":"user","content":f"أريد {qty} كيلو"},
            {"role":"assistant","content":f"ماشي، {qty} كيلو = {vp(item['p']*qty)} دينار"},
            {"role":"user","content":"هاي الفلوس، شكراً"},
            {"role":"assistant","content":f"{pick(CLOSE)}"},
        ]
    elif tpl == 2:
        msgs = [
            {"role":"user","content":f"{pick(SHORT_GREET)}، هاي {item['n']} طازج؟"},
            {"role":"assistant","content":f"إي والله، جاي اليوم من الصباح. {item['n']} طازج هواي"},
            {"role":"user","content":f"{howmuch()}؟"},
            {"role":"assistant","content":f"{vp(item['p'])} دينار الـ{item['unit']}"},
            {"role":"user","content":f"{pick(DISC_REQ)}"},
            {"role":"assistant","content":f"{pick(DISC_YES)}"},
            {"role":"user","content":f"زين، أريد {qty} {item['unit']}"},
            {"role":"assistant","content":f"تفضل، {pick(CLOSE)}"},
        ]
    elif tpl == 3:
        msgs = [
            {"role":"user","content":f"مرحبا، عندكم {item['n']} و{item2['n']}؟"},
            {"role":"assistant","content":f"إي عندنا. {item['n']} بـ{vp(item['p'])} والـ{item2['n']} بـ{vp(item2['p'])} دينار"},
            {"role":"user","content":f"أريد كيلوين {item['n']} وكيلو {item2['n']}"},
            {"role":"assistant","content":f"كيلوين {item['n']} = {vp(item['p']*2)} وكيلو {item2['n']} = {vp(item2['p'])}. الكل {vp(item['p']*2 + item2['p'])} دينار"},
            {"role":"user","content":"مشكور، هاي الفلوس"},
            {"role":"assistant","content":f"{pick(CLOSE)}"},
        ]
    elif tpl == 4:
        msgs = [
            {"role":"user","content":"هلو، أريد أطلب بضاعة"},
            {"role":"assistant","content":"تفضل، شنو تريد؟"},
            {"role":"user","content":f"أريد {qty} كيلو {item['n']} و{qty+1} كيلو {item2['n']}"},
            {"role":"assistant","content":f"ماشي، {item['n']} بـ{vp(item['p'])} و{item2['n']} بـ{vp(item2['p'])}. الكل {vp(item['p']*qty + item2['p']*(qty+1))} دينار"},
            {"role":"user","content":"زين، هاي الفلوس"},
            {"role":"assistant","content":f"{pick(CLOSE)}"},
        ]
    elif tpl == 5:
        msgs = [
            {"role":"user","content":f"{pick(SHORT_GREET)}، عندكم {item['n']} بالجملة؟"},
            {"role":"assistant","content":f"إي عندنا. لو تاخذ 10 كيلو فأكثر أعطيك سعر خاص"},
            {"role":"user","content":"شنو السعر بالجملة؟"},
            {"role":"assistant","content":f"{vp(item['p']*0.85)} دينار الكيلو بدل {vp(item['p'])}"},
            {"role":"user","content":"زين، أاخذ 20 كيلو"},
            {"role":"assistant","content":f"الكل {vp(item['p']*0.85*20)} دينار. الله يبارك فيك"},
        ]
    elif tpl == 6:
        msgs = [
            {"role":"user","content":"شنو عندكم طازج اليوم؟"},
            {"role":"assistant","content":f"عندنا {item['n']} و{item2['n']} طازجين. {item['n']} بـ{vp(item['p'])} و{item2['n']} بـ{vp(item2['p'])}"},
            {"role":"user","content":f"أاخذ كيلو {item['n']}"},
            {"role":"assistant","content":f"تفضل، {vp(item['p'])} دينار"},
            {"role":"user","content":"مشكور"},
            {"role":"assistant","content":f"{pick(CLOSE)}"},
        ]
    elif tpl == 7:
        msgs = [
            {"role":"user","content":f"أم علي، {item['n']} هسه غالي هواي"},
            {"role":"assistant","content":"والله هالأيام الأسعار صعدت كلها، مو بيدي"},
            {"role":"user","content":f"كيلو {howmuch()}؟"},
            {"role":"assistant","content":f"{vp(item['p'])} دينار، أرخص ما أكو"},
            {"role":"user","content":"زين، أاخذ نص كيلو"},
            {"role":"assistant","content":f"تفضل، {vp(item['p']//2)} دينار"},
        ]
    elif tpl == 8:
        msgs = [
            {"role":"user","content":f"{pick(SHORT_GREET)}، عندكم {item['n']} صالح للأكل؟ ما فيه شي منتهي الصلاحية؟"},
            {"role":"assistant","content":f"والله عندنا بضاعتنا دايماً طازجة. {item['n']} جاي هذا الأسبوع"},
            {"role":"user","content":"ماشي، أاخذ كميات"},
            {"role":"assistant","content":f"تفضل، كيلو بـ{vp(item['p'])} دينار. لو تاخذ كميات أعطيك سعر أحسن"},
        ]
    elif tpl == 9:
        msgs = [
            {"role":"user","content":"هلو، عندكم خضار طازج؟"},
            {"role":"assistant","content":f"إي عندنا. {item['n']} بـ{vp(item['p'])} و{item2['n']} بـ{vp(item2['p'])}"},
            {"role":"user","content":"أريد طماطة وبصل"},
            {"role":"assistant","content":"طماطة بـ3,500 دينار والبصل بـ2,000 دينار الكيلو"},
            {"role":"user","content":"أريد كيلوين طماطة وكيلو بصل"},
            {"role":"assistant","content":f"الكل {vp(3500*2+2000)} دينار. تفضل"},
        ]
    elif tpl == 10:
        msgs = [
            {"role":"user","content":f"مرحبا، عندكم {item['n']}؟"},
            {"role":"assistant","content":f"إي عندنا، بـ{vp(item['p'])} دينار الـ{item['unit']}"},
            {"role":"user","content":f"أريد {qty} {item['unit']}"},
            {"role":"assistant","content":f"الكل {vp(item['p']*qty)} دينار"},
            {"role":"user","content":"هاي"},
            {"role":"assistant","content":f"{pick(CLOSE)}"},
        ]
    elif tpl == 11:
        msgs = [
            {"role":"user","content":f"صباح الخير، أريد أطلب مشتريات من البيت"},
            {"role":"assistant","content":"أهلاً، تفضل شنو تريد؟"},
            {"role":"user","content":f"أريد {qty} كيلو {item['n']} و{qty+1} كيلو {item2['n']}"},
            {"role":"assistant","content":f"ماشي. هل تريد توصيل؟"},
            {"role":"user","content":"إي أريد توصيل"},
            {"role":"assistant","content":f"الكل {vp(item['p']*qty + item2['p']*(qty+1))} دينار زيادة 3000 توصيل"},
        ]
    elif tpl == 12:
        meals = ["قيمة","مرق عدس","تشريب","دولمة","بريانية"]
        msg = pick(meals)
        msgs = [
            {"role":"user","content":f"أريد أسوي {msg}، شنو المواد المطلوبة؟"},
            {"role":"assistant","content":f"للـ{msg} تريد: {item['n']} و{item2['n']} وبهارات. كلها موجودة عندنا"},
            {"role":"user","content":f"{howmuch()} الكل؟"},
            {"role":"assistant","content":f"حوالي {vp(item['p']*2 + item2['p']*2)} دينار لكميات معقولة"},
            {"role":"user","content":"ماشي، أجيكم"},
            {"role":"assistant","content":"حياك الله"},
        ]
    elif tpl == 13:
        msgs = [
            {"role":"user","content":f"هلو، {item['n']} من وين؟ محلي ولا مستورد؟"},
            {"role":"assistant","content":f"محلي عراقي أصلي. {item['n']} من المزارع العراقية"},
            {"role":"user","content":"والمستورد عندكم؟"},
            {"role":"assistant","content":f"عندنا إي، المستورد بـ{vp(int(item['p']*1.3))} بس المحلي أطعم"},
            {"role":"user","content":"آخذ المحلي"},
            {"role":"assistant","content":f"خيار زين. {vp(item['p'])} دينار الكيلو"},
        ]
    elif tpl == 14:
        festival = pick(["عيد الأضحى","رمضان","عيد الفطر","الأعراس"])
        msgs = [
            {"role":"user","content":f"أريد كميات كبيرة ليش {festival}"},
            {"role":"assistant","content":f"مبارك! تفضل، شنو تريد؟"},
            {"role":"user","content":f"أريد 20 كيلو {item['n']} و15 كيلو {item2['n']}"},
            {"role":"assistant","content":f"بالكميات هذي نعطيك سعر خاص. الكل {vp(item['p']*0.85*20 + item2['p']*0.85*15)} دينار"},
            {"role":"user","content":"ممتاز، ماشي"},
            {"role":"assistant","content":"الله يبارك فيك، نجهز طلبك خلال ساعة"},
        ]
    elif tpl == 15:
        msgs = [
            {"role":"user","content":f"هلو، {item['n']} تاريخ انتهاء صلاحيته؟"},
            {"role":"assistant","content":f"{item['n']} صلاحيته {random.randint(3,12)} أشهر. كلشي طازج"},
            {"role":"user","content":"ماشي. وعندكم {item2['n']}؟"},
            {"role":"assistant","content":f"إي، {item2['n']} بـ{vp(item2['p'])} دينار الكيلو"},
            {"role":"user","content":f"أاخذ {qty} من كل واحد"},
            {"role":"assistant","content":f"الكل {vp(item['p']*qty + item2['p']*qty)} دينار"},
        ]
    elif tpl == 16:
        msgs = [
            {"role":"user","content":"هلو، عندكم تخفيضات اليوم؟"},
            {"role":"assistant","content":f"إي عندنا عرض اليوم: {item['n']} بـ{vp(int(item['p']*0.8))} بدل {vp(item['p'])}"},
            {"role":"user","content":"وشي ثاني بالعرض؟"},
            {"role":"assistant","content":f"{item2['n']} أيضاً بخصم 15%"},
            {"role":"user","content":"زين، أاخذ من الاثنين"},
            {"role":"assistant","content":f"تفضل، الكل {vp(int(item['p']*0.8*qty) + int(item2['p']*0.85*qty))} دينار"},
        ]
    elif tpl == 17:
        msgs = [
            {"role":"user","content":f"مرحبا، {item['n']} عندكم من نوعين؟"},
            {"role":"assistant","content":f"إي عندنا نوعين: محلي بـ{vp(item['p'])} ومستورد بـ{vp(int(item['p']*1.25))}"},
            {"role":"user","content":"الفرق شنو؟"},
            {"role":"assistant","content":"المستورد أكبر حجماً وأجود، المحلي طازج وطعمه أحسن"},
            {"role":"user","content":"آخذ المحلي"},
            {"role":"assistant","content":f"ماشي، {qty} كيلو = {vp(item['p']*qty)} دينار"},
        ]
    elif tpl == 18:
        msgs = [
            {"role":"user","content":f"هلو، أريد {item['n']} بس ما أعرف كيف أختار الجيد"},
            {"role":"assistant","content":f"انتبه على اللون والرائحة. {item['n']} الجيد لونه زاهي وشمه طيب"},
            {"role":"user","content":"وهذا الموجود عندكم زين؟"},
            {"role":"assistant","content":f"إي والله، طازج من اليوم الصباح"},
            {"role":"user","content":"ماشي، شكراً. أاخذ كيلو"},
            {"role":"assistant","content":f"{vp(item['p'])} دينار. {pick(CLOSE)}"},
        ]
    elif tpl == 19:
        msgs = [
            {"role":"user","content":"هلو، أريد قائمة مشتريات كاملة للأسبوع"},
            {"role":"assistant","content":"تفضل، قولها واحد واحد ونجهزها"},
            {"role":"user","content":f"أريد {item['n']} و{item2['n']} وبيض وطحين"},
            {"role":"assistant","content":f"{item['n']} بـ{vp(item['p'])}, {item2['n']} بـ{vp(item2['p'])}, بيض 10,000, طحين 2,000 الكيلو"},
            {"role":"user","content":"جيب الكل"},
            {"role":"assistant","content":f"ماشي، أجمع الكل وأعطيك الحساب"},
        ]
    elif tpl == 20:
        msgs = [
            {"role":"user","content":"عندكم أكل جاهز للطلب؟"},
            {"role":"assistant","content":f"إي عندنا {pick(['دجاج مشوي','مسگوف','تشريب دجاج','قيمة'])} جاهز"},
            {"role":"user","content":"بيش الوجبة؟"},
            {"role":"assistant","content":f"{vp(random.randint(10000,25000))} دينار مع الخبز"},
            {"role":"user","content":"طلب واحد مع توصيل"},
            {"role":"assistant","content":"ماشي، التوصيل 3000 دينار، أعطيني عنوانك"},
        ]
    elif tpl == 21:
        msgs = [
            {"role":"user","content":f"هلو، أريد {item['n']} بس لا أريد بالكيلو، بالحزمة؟"},
            {"role":"assistant","content":f"إي عندنا بالحزمة. حزمة {item['n']} بـ{vp(item['p']*3)} دينار"},
            {"role":"user","content":"شكد تحتوي الحزمة؟"},
            {"role":"assistant","content":"3 كيلو، موفر عليك من الفردي"},
            {"role":"user","content":"ماشي آخذ حزمتين"},
            {"role":"assistant","content":f"{vp(item['p']*6)} دينار. {pick(CLOSE)}"},
        ]
    elif tpl == 22:
        msgs = [
            {"role":"user","content":"هلو، عندكم منتجات عضوية؟"},
            {"role":"assistant","content":f"إي عندنا {item['n']} عضوي، بدون مبيدات"},
            {"role":"user","content":"أغلى من العادي؟"},
            {"role":"assistant","content":f"شوية، بـ{vp(int(item['p']*1.4))} بدل {vp(item['p'])}"},
            {"role":"user","content":"يستاهل للصحة، آخذ"},
            {"role":"assistant","content":f"{pick(CLOSE)}"},
        ]
    elif tpl == 23:
        msgs = [
            {"role":"user","content":f"هلو، أريد فاتورة كاملة على المشتريات"},
            {"role":"assistant","content":"تفضل، نسوي الفاتورة. شنو اشتريت؟"},
            {"role":"user","content":f"{qty} كيلو {item['n']} و{qty} كيلو {item2['n']}"},
            {"role":"assistant","content":f"{item['n']}: {vp(item['p']*qty)} + {item2['n']}: {vp(item2['p']*qty)} = {vp((item['p']+item2['p'])*qty)} دينار"},
            {"role":"user","content":"ماشي، مشكور"},
            {"role":"assistant","content":f"{pick(CLOSE)}"},
        ]
    elif tpl == 24:
        msgs = [
            {"role":"user","content":"هلو، عندكم توصيل للبيوت؟"},
            {"role":"assistant","content":"إي عندنا توصيل لكل بغداد. الطلب الأدنى 20,000 دينار"},
            {"role":"user","content":f"زين، أريد {item['n']} و{item2['n']}"},
            {"role":"assistant","content":f"الكل {vp(item['p']*2 + item2['p']*2)} دينار زيادة 5000 توصيل"},
            {"role":"user","content":"ماشي"},
            {"role":"assistant","content":"أعطيني العنوان والتوصيل خلال ساعة"},
        ]
    else:
        msgs = [
            {"role":"user","content":f"صباح الخير، عندكم {item['n']} و{item2['n']}؟"},
            {"role":"assistant","content":f"صباح النور! إي موجودين. {item['n']} بـ{vp(item['p'])} و{item2['n']} بـ{vp(item2['p'])}"},
            {"role":"user","content":"أريد من الاثنين"},
            {"role":"assistant","content":f"كيلو من كل واحد؟"},
            {"role":"user","content":"إي كيلو من كل"},
            {"role":"assistant","content":f"الكل {vp(item['p']+item2['p'])} دينار. {pick(CLOSE)}"},
        ]

    return {"id":f"food_{i:04d}","category":"sales_food","dialect":"iraqi_arabic","messages":msgs}

# ============================================================
# FILE 3 - CLOTHES SALES
# ============================================================

CLOTHES = [
    {"n":"دشداشة رجالي","p":35000,"f":"قماش ممتاز، مقاسات متوفرة"},
    {"n":"بدلة رسمية","p":150000,"f":"قماش تركي، لون أسود وكحلي"},
    {"n":"بنطلون جينز","p":45000,"f":"ماركة ليفي، مقاسات 28 لـ42"},
    {"n":"تيشرت","p":15000,"f":"قطن 100%، ألوان متنوعة"},
    {"n":"عباية نسائية","p":60000,"f":"قماش كريب، تطريز يدوي"},
    {"n":"فستان سهرة","p":120000,"f":"قماش ساتان، مقاسات S لـXL"},
    {"n":"كنزة شتوية","p":40000,"f":"صوف فاخر، دافية"},
    {"n":"جاكيت جلد","p":200000,"f":"جلد طبيعي، ضد الماء"},
    {"n":"شماغ","p":25000,"f":"قطن عراقي أصيل"},
    {"n":"عقال","p":15000,"f":"صوف طبيعي"},
    {"n":"حذاء جلد","p":80000,"f":"جلد طبيعي، مريح"},
    {"n":"حذاء رياضي","p":65000,"f":"نايك أصل، مقاسات متوفرة"},
    {"n":"صندل نسائي","p":35000,"f":"ماركة إيطالية"},
    {"n":"حقيبة نسائية","p":70000,"f":"جلد PU، ألوان متنوعة"},
    {"n":"ستارة غرفة","p":90000,"f":"قماش فاخر، بمقاس 3 متر"},
]

SIZES = ["S","M","L","XL","XXL","38","40","42","44","46"]
COLORS = ["أبيض","أسود","كحلي","رمادي","بيج","أخضر زيتي","بني","خمري","أزرق","أحمر"]

def gen_clothes(i):
    item = pick(CLOTHES)
    size = pick(SIZES)
    color = pick(COLORS)
    tpl = random.randint(1, 25)

    if tpl == 1:
        _gc, _gs = greet_pair()
        msgs = [
            {"role":"user","content":_gc},
            {"role":"assistant","content":_gs},
            {"role":"user","content":f"أريد {item['n']}، عندكم؟"},
            {"role":"assistant","content":f"إي عندنا، {item['f']}. سعره {vp(item['p'])} دينار"},
            {"role":"user","content":f"عندكم مقاس {size}؟"},
            {"role":"assistant","content":f"إي عندنا مقاس {size}. تريد تجرب؟"},
            {"role":"user","content":"إي"},
            {"role":"assistant","content":"تفضل الغرفة"},
            {"role":"user","content":"زين، ماخذه"},
            {"role":"assistant","content":f"{pick(CLOSE)}"},
        ]
    elif tpl == 2:
        msgs = [
            {"role":"user","content":f"هلو، عندكم {item['n']} بلون {color}؟"},
            {"role":"assistant","content":f"إي عندنا بلون {color}، {item['f']}"},
            {"role":"user","content":f"{howmuch()}؟"},
            {"role":"assistant","content":f"{vp(item['p'])} دينار"},
            {"role":"user","content":f"{pick(DISC_REQ)}"},
            {"role":"assistant","content":f"{pick(DISC_YES)}"},
            {"role":"user","content":"ماشي، هذا"},
            {"role":"assistant","content":f"{pick(CLOSE)}"},
        ]
    elif tpl == 3:
        msgs = [
            {"role":"user","content":f"أريد {item['n']} هدية لزوجتي"},
            {"role":"assistant","content":f"هلا، {item['n']} هدية زينة. عندنا ألوان حلوة. {howmuch()} ميزانيتك؟"},
            {"role":"user","content":"حوالي 100 ألف دينار"},
            {"role":"assistant","content":f"عندنا {item['n']} بـ{vp(min(item['p'],100000))} دينار. {item['f']}"},
            {"role":"user","content":"حلو والله، أاخذه"},
            {"role":"assistant","content":f"{pick(CLOSE)}"},
        ]
    elif tpl == 4:
        msgs = [
            {"role":"user","content":f"{pick(SHORT_GREET)}، عندكم ملابس للعيد؟"},
            {"role":"assistant","content":"إي عندنا كولكشن العيد جديد. تشوف شنو تريد؟"},
            {"role":"user","content":f"أريد {item['n']}"},
            {"role":"assistant","content":f"{item['n']} موجود، {item['f']}. بـ{vp(item['p'])} دينار"},
            {"role":"user","content":f"{pick(EXPENSIVE)}"},
            {"role":"assistant","content":f"هذا سعر العيد يا حاجي، قماش ممتاز. {pick(DISC_YES)}"},
            {"role":"user","content":"زين، خذ"},
            {"role":"assistant","content":f"مبارك عليك العيد! {pick(CLOSE)}"},
        ]
    elif tpl == 5:
        msgs = [
            {"role":"user","content":"عندكم ملابس أطفال؟"},
            {"role":"assistant","content":"إي عندنا قسم أطفال. شنو عمر الطفل؟"},
            {"role":"user","content":"سنتين ونص"},
            {"role":"assistant","content":f"عندنا {item['n']} مناسب لعمره. بـ{vp(item['p']*0.6)} دينار"},
            {"role":"user","content":"حلو، أاخذ واحد أبيض وواحد أزرق"},
            {"role":"assistant","content":f"الاثنين = {vp(item['p']*0.6*2)} دينار. {pick(CLOSE)}"},
        ]
    elif tpl == 6:
        msgs = [
            {"role":"user","content":f"باجي، {item['n']} هذا أصل ولا تقليد؟"},
            {"role":"assistant","content":f"والله أخوي عندنا أصل وتقليد. الأصل بـ{vp(item['p'])} والتقليد بـ{vp(int(item['p']*0.5))}"},
            {"role":"user","content":"شنو الفرق؟"},
            {"role":"assistant","content":f"الأصل {item['f']}، جودة أحسن ويدوم أكثر"},
            {"role":"user","content":"أاخذ الأصل"},
            {"role":"assistant","content":f"خيار زين! {pick(CLOSE)}"},
        ]
    elif tpl == 7:
        msgs = [
            {"role":"user","content":f"عندكم {item['n']} بالجملة؟"},
            {"role":"assistant","content":"إي عندنا جملة. شكد قطعة تريد؟"},
            {"role":"user","content":"أريد 10 قطع"},
            {"role":"assistant","content":f"10 قطع بسعر {vp(item['p']*0.8)} قطعة. الكل {vp(item['p']*0.8*10)} دينار"},
            {"role":"user","content":"ماشي، أاخذها"},
            {"role":"assistant","content":f"{pick(CLOSE)}"},
        ]
    elif tpl == 8:
        msgs = [
            {"role":"user","content":f"{pick(SHORT_GREET)}، ما عندكم {item['n']} بمقاس {size}"},
            {"role":"assistant","content":f"هسه ما أكو مقاس {size} بس راح يجي الأسبوع الجاي. تسوي طلب؟"},
            {"role":"user","content":"إي ماشي، سجل اسمي"},
            {"role":"assistant","content":"ماشي، اسمك وتلفونك؟"},
            {"role":"user","content":"أبو علي، 07801234567"},
            {"role":"assistant","content":"تسلم، لما يجي نتصل فيك"},
        ]
    elif tpl == 9:
        msgs = [
            {"role":"user","content":f"مرحبا، أريد أرجع {item['n']} اشتريته امبارح، مو مناسب"},
            {"role":"assistant","content":"شنو المشكلة فيه؟"},
            {"role":"user","content":"المقاس كبير علي"},
            {"role":"assistant","content":f"ماشي، تبدله بمقاس أصغر ولا ترجع الفلوس؟"},
            {"role":"user","content":"أبدله بمقاس أصغر"},
            {"role":"assistant","content":"تفضل، جرب هذا المقاس"},
        ]
    elif tpl == 10:
        _gc, _gs = greet_pair()
        msgs = [
            {"role":"user","content":_gc},
            {"role":"assistant","content":_gs},
            {"role":"user","content":f"شنو عندكم جديد؟"},
            {"role":"assistant","content":f"عندنا كولكشن جديد. {item['n']} بـ{vp(item['p'])} دينار، {item['f']}"},
            {"role":"user","content":f"يعجبني، أاخذه"},
            {"role":"assistant","content":f"{pick(CLOSE)}"},
        ]
    elif tpl == 11:
        msgs = [
            {"role":"user","content":f"هلو، عندكم ملابس رياضية؟"},
            {"role":"assistant","content":f"إي عندنا. {item['n']} رياضي بـ{vp(item['p'])} دينار"},
            {"role":"user","content":"نايك ولا أديداس؟"},
            {"role":"assistant","content":"عندنا الاثنين. نايك أغلى شوية بس أجود"},
            {"role":"user","content":"أاخذ نايك"},
            {"role":"assistant","content":f"نايك بـ{vp(int(item['p']*1.2))} دينار. {pick(CLOSE)}"},
        ]
    elif tpl == 12:
        msgs = [
            {"role":"user","content":f"مرحبا، أريد أطلب {item['n']} بالأون لاين"},
            {"role":"assistant","content":"إي عندنا طلبيات أون لاين. شنو المقاس واللون؟"},
            {"role":"user","content":f"مقاس {size} ولون {color}"},
            {"role":"assistant","content":f"موجود. البضاعة توصلك خلال يومين بـ{vp(item['p'])} دينار زيادة 3000 شحن"},
            {"role":"user","content":"أكدر أرجعه لو ما يناسب؟"},
            {"role":"assistant","content":"إي، سياسة الإرجاع 7 أيام مع الفاتورة"},
        ]
    elif tpl == 13:
        msgs = [
            {"role":"user","content":f"عندكم ملابس للمناسبات؟"},
            {"role":"assistant","content":f"إي عندنا قسم مناسبات. {item['n']} مناسب للأفراح والمناسبات. بـ{vp(item['p'])} دينار"},
            {"role":"user","content":"وعندكم تفصيل؟"},
            {"role":"assistant","content":"إي عندنا خياط. التفصيل يجهز خلال أسبوع"},
            {"role":"user","content":"شكد التفصيل؟"},
            {"role":"assistant","content":f"التفصيل 30,000 دينار إضافة على القماش"},
        ]
    elif tpl == 14:
        msgs = [
            {"role":"user","content":f"هلو، {item['n']} من تركيا ولا صيني؟"},
            {"role":"assistant","content":f"عندنا تركي وصيني. التركي بـ{vp(item['p'])} والصيني بـ{vp(int(item['p']*0.55))}"},
            {"role":"user","content":"الجودة شنو؟"},
            {"role":"assistant","content":"التركي أجود وأدوم، الصيني رخيص بس جودته أقل"},
            {"role":"user","content":"آخذ التركي"},
            {"role":"assistant","content":f"خيار ممتاز! {pick(CLOSE)}"},
        ]
    elif tpl == 15:
        msgs = [
            {"role":"user","content":f"عندكم {item['n']} بلون {color} ومقاس {size}؟"},
            {"role":"assistant","content":f"هسه عندنا {color} بس مقاس {size} نافذ. عندنا {pick(SIZES)} متوفر"},
            {"role":"user","content":"ما يصير، لازم مقاس {size}"},
            {"role":"assistant","content":"ماشي، نطلبها لك من المستودع. تجي خلال 3 أيام"},
            {"role":"user","content":"زين، سجل اسمي"},
            {"role":"assistant","content":"اسمك وتلفونك؟"},
        ]
    elif tpl == 16:
        msgs = [
            {"role":"user","content":f"مرحبا، أريد {item['n']} من ماركة معينة"},
            {"role":"assistant","content":"شنو الماركة؟"},
            {"role":"user","content":"Zara أو H&M"},
            {"role":"assistant","content":f"عندنا ملابس تشبه H&M بجودة ممتازة. {item['n']} بـ{vp(item['p'])} دينار"},
            {"role":"user","content":"أشوفه؟"},
            {"role":"assistant","content":"تفضل، هذا هو"},
        ]
    elif tpl == 17:
        msgs = [
            {"role":"user","content":f"هلو، عندكم {item['n']} للسفر؟"},
            {"role":"assistant","content":f"إي، عندنا {item['n']} مناسب للسفر. {item['f']}"},
            {"role":"user","content":"وزنه خفيف؟"},
            {"role":"assistant","content":"إي خفيف وسهل الغسيل، مناسب للسفر الطويل"},
            {"role":"user","content":"آخذ اثنين"},
            {"role":"assistant","content":f"اثنين = {vp(item['p']*2)} دينار. {pick(CLOSE)}"},
        ]
    elif tpl == 18:
        msgs = [
            {"role":"user","content":f"صباح الخير، أريد ملابس لشغل الدوام"},
            {"role":"assistant","content":f"أهلاً، عندنا {item['n']} رسمي مناسب للدوام. {item['f']}"},
            {"role":"user","content":f"{howmuch()}؟"},
            {"role":"assistant","content":f"{vp(item['p'])} دينار"},
            {"role":"user","content":"عندكم أكثر من لون؟"},
            {"role":"assistant","content":f"إي، عندنا {color} وأبيض وكحلي"},
            {"role":"user","content":"آخذ الكحلي"},
            {"role":"assistant","content":f"{pick(CLOSE)}"},
        ]
    elif tpl == 19:
        msgs = [
            {"role":"user","content":f"مرحبا، ما عجبني {item['n']} اللي اشتريته، يلطع بالغسيل؟"},
            {"role":"assistant","content":"والله هذا مو من عندنا لو اتبعت تعليمات الغسيل"},
            {"role":"user","content":"شنو التعليمات؟"},
            {"role":"assistant","content":"غسيل بارد 30 درجة، ولا تحط بالنشافة"},
            {"role":"user","content":"زين، شكراً على المعلومة"},
            {"role":"assistant","content":"حياك، لو عندك أي مشكلة تعال"},
        ]
    elif tpl == 20:
        season = pick(["الصيف","الشتاء","الربيع","الخريف"])
        msgs = [
            {"role":"user","content":f"أريد ملابس لـ{season}"},
            {"role":"assistant","content":f"عندنا كولكشن {season} جديد. {item['n']} مناسب هواي"},
            {"role":"user","content":f"{howmuch()}؟"},
            {"role":"assistant","content":f"{vp(item['p'])} دينار"},
            {"role":"user","content":"واشتريت قبل خصم؟"},
            {"role":"assistant","content":f"إي عندنا خصم {season} الأسبوع هذا 10%"},
        ]
    elif tpl == 21:
        msgs = [
            {"role":"user","content":f"هلو، عندكم {item['n']} بالتقسيط؟"},
            {"role":"assistant","content":f"إي عندنا. المبلغ {vp(item['p'])} دينار، تدفع نصه هسه والباقي بعد شهر"},
            {"role":"user","content":"أكدر شهرين؟"},
            {"role":"assistant","content":"ماشي، 3 أقساط بدون فائدة"},
            {"role":"user","content":"الله يخليك، ماشي"},
            {"role":"assistant","content":f"{pick(CLOSE)}"},
        ]
    elif tpl == 22:
        msgs = [
            {"role":"user","content":f"مرحبا، أريد أشتري مجموعة هدايا: {item['n']} و{pick(CLOTHES)['n']}"},
            {"role":"assistant","content":"هلا! للهدايا نحطهم بكيس هدية بالمجان"},
            {"role":"user","content":"الكل بيش؟"},
            {"role":"assistant","content":f"تقريباً {vp(item['p'] * 2)} دينار للمجموعة"},
            {"role":"user","content":"ماشي، الله يسلمك"},
            {"role":"assistant","content":f"{pick(CLOSE)}"},
        ]
    elif tpl == 23:
        msgs = [
            {"role":"user","content":f"هلو، عندكم ملابس بلون {color}؟ ما أشوف"},
            {"role":"assistant","content":f"إي عندنا {color} بس في الداخل. تعال أوريك"},
            {"role":"user","content":"ماشي"},
            {"role":"assistant","content":f"هاي {item['n']} بلون {color}، {item['f']}"},
            {"role":"user","content":f"{howmuch()}؟"},
            {"role":"assistant","content":f"{vp(item['p'])} دينار فقط"},
            {"role":"user","content":"آخذه"},
            {"role":"assistant","content":f"{pick(CLOSE)}"},
        ]
    elif tpl == 24:
        msgs = [
            {"role":"user","content":f"مساء الخير، كيف أعرف المقاس المناسب لـ{item['n']}؟"},
            {"role":"assistant","content":"لو تعطيني طولك ووزنك أساعدك تختار"},
            {"role":"user","content":"طولي 175 ووزني 80"},
            {"role":"assistant","content":f"مقاس L أو XL مناسب لك. {item['n']} متوفر بالمقاسين"},
            {"role":"user","content":"أجرب L أول"},
            {"role":"assistant","content":"تفضل الغرفة، اجربه"},
        ]
    else:
        msgs = [
            {"role":"user","content":f"هلو، عندكم تشكيلة جديدة للشباب؟"},
            {"role":"assistant","content":f"إي وصل كولكشن جديد. {item['n']} {item['f']} بـ{vp(item['p'])} دينار"},
            {"role":"user","content":f"عندكم بلون {color}؟"},
            {"role":"assistant","content":f"إي عندنا {color}"},
            {"role":"user","content":"أاخذه"},
            {"role":"assistant","content":f"{pick(CLOSE)}"},
        ]

    return {"id":f"clothes_{i:04d}","category":"sales_clothes","dialect":"iraqi_arabic","messages":msgs}

# ============================================================
# FILE 4 - CARS SALES
# ============================================================

CARS = [
    {"n":"كيا سبورتاج","year":2023,"p":35000000,"f":"فل كامل، بانوراما"},
    {"n":"هيونداي توسان","year":2022,"p":30000000,"f":"فل كامل، أوتوماتيك"},
    {"n":"تويوتا كامري","year":2023,"p":45000000,"f":"SE، فل كامل"},
    {"n":"تويوتا كورولا","year":2022,"p":28000000,"f":"أوتوماتيك، فل كامل"},
    {"n":"نيسان صني","year":2023,"p":22000000,"f":"فيس ليفت، اقتصادي"},
    {"n":"هوندا سيفيك","year":2022,"p":32000000,"f":"سبورت، فل كامل"},
    {"n":"مرسيدس C200","year":2021,"p":70000000,"f":"AMG لاين، بانوراما"},
    {"n":"بي إم دبليو 520","year":2022,"p":85000000,"f":"M باكيج، فل كامل"},
    {"n":"شيفروليه ماليبو","year":2023,"p":25000000,"f":"LT، كاميرا خلفية"},
    {"n":"MG ZS","year":2023,"p":18000000,"f":"فل كامل، كفالة"},
    {"n":"تويوتا راف فور","year":2023,"p":55000000,"f":"هجين، فل كامل"},
    {"n":"كيا K5","year":2022,"p":38000000,"f":"سبورت، شاشة كبيرة"},
    {"n":"هيونداي سوناتا","year":2023,"p":40000000,"f":"فل كامل، لي إضاءة"},
    {"n":"فولكسواكن باسات","year":2021,"p":42000000,"f":"TSI، فل كامل"},
    {"n":"نيسان باترول","year":2022,"p":90000000,"f":"بلاتينيوم، فل كامل"},
    {"n":"جيب رانغلر","year":2022,"p":80000000,"f":"سبورت، 4x4"},
    {"n":"شيفروليه تاهو","year":2023,"p":110000000,"f":"بريمير، فل كامل"},
    {"n":"كيا ستينگر","year":2022,"p":60000000,"f":"GT لاين، توربو"},
]

def gen_cars(i):
    car = pick(CARS)
    car2 = pick(CARS)
    while car2["n"] == car["n"]:
        car2 = pick(CARS)
    tpl = random.randint(1, 25)

    if tpl == 1:
        msgs = [
            {"role":"user","content":f"{pick(SHORT_GREET)}، أريد {car['n']} موديل {car['year']}"},
            {"role":"assistant","content":f"هلا، {car['n']} {car['year']} موجود. {car['f']}. سعره {vp(car['p'])} دينار"},
            {"role":"user","content":"يعني بالدولار شكد؟"},
            {"role":"assistant","content":f"حسب سعر الصرف اليوم، تقريباً {vp(car['p']//1300)} دولار"},
            {"role":"user","content":f"{pick(DISC_REQ)}"},
            {"role":"assistant","content":f"{pick(DISC_NO)}"},
            {"role":"user","content":"زين، افكر و ارجعلك"},
            {"role":"assistant","content":"حياك الله، السيارة موجودة"},
        ]
    elif tpl == 2:
        msgs = [
            {"role":"user","content":f"هلو، شنو الفرق بين {car['n']} و{car2['n']}؟"},
            {"role":"assistant","content":f"{car['n']} بـ{vp(car['p'])} دينار، {car['f']}. {car2['n']} بـ{vp(car2['p'])} دينار، {car2['f']}"},
            {"role":"user","content":"يا واحد أوفر؟"},
            {"role":"assistant","content":f"لو تسألني، {car['n']} أوفر لأن {car['f']}"},
            {"role":"user","content":f"زين، أاخذ تجربة على الـ{car['n']}"},
            {"role":"assistant","content":"ماشي، تعال أي وقت وتجرب"},
        ]
    elif tpl == 3:
        msgs = [
            {"role":"user","content":f"{pick(SHORT_GREET)}، عندكم {car['n']} مستعمل؟"},
            {"role":"assistant","content":f"إي عندنا {car['n']} موديل {car['year']-1} مستعمل بحالة ممتازة"},
            {"role":"user","content":f"{howmuch()}؟"},
            {"role":"assistant","content":f"بـ{vp(car['p']*0.75)} دينار. ماشيه شكد؟"},
            {"role":"user","content":"وين السيارة؟"},
            {"role":"assistant","content":"موجودة في المعرض، تعال تشوفها"},
        ]
    elif tpl == 4:
        msgs = [
            {"role":"user","content":f"أريد {car['n']}، هل تكدر تقسط؟"},
            {"role":"assistant","content":f"إي عندنا تقسيط. {car['n']} بـ{vp(car['p'])}، تدفع مقدم 25% والباقي أقساط"},
            {"role":"user","content":"شكد المقدم؟"},
            {"role":"assistant","content":f"المقدم {vp(car['p']*0.25)} دينار والباقي على 3 سنين"},
            {"role":"user","content":"القسط الشهري شكد؟"},
            {"role":"assistant","content":f"تقريباً {vp(car['p']*0.75/36)} دينار شهري"},
        ]
    elif tpl == 5:
        msgs = [
            {"role":"user","content":f"{pick(SHORT_GREET)}، {car['n']} هذا عنده كفالة؟"},
            {"role":"assistant","content":f"إي، {car['n']} الجديد معه كفالة 3 سنين من الوكالة"},
            {"role":"user","content":"والصيانة؟"},
            {"role":"assistant","content":"أول 3 صيانات مجانية من الوكالة"},
            {"role":"user","content":"زين، هذا يجلب"},
            {"role":"assistant","content":f"سعره {vp(car['p'])} دينار. شوكت تريد تأخذه؟"},
        ]
    elif tpl == 6:
        msgs = [
            {"role":"user","content":f"هلو، أريد {car['n']} لكن ميزانيتي محدودة"},
            {"role":"assistant","content":"شنو ميزانيتك تقريباً؟"},
            {"role":"user","content":"حوالي 20 مليون دينار"},
            {"role":"assistant","content":f"عندنا {car2['n']} بـ{vp(min(car2['p'],20000000))} دينار. {car2['f']}"},
            {"role":"user","content":"هذا يصلح؟"},
            {"role":"assistant","content":"إي والله، سيارة ممتازة وبسعر مناسب لميزانيتك"},
        ]
    elif tpl == 7:
        msgs = [
            {"role":"user","content":f"مرحبا، شنو أحسن سيارة عندكم بسعر 30 مليون؟"},
            {"role":"assistant","content":f"بهالسعر، {car['n']} موديل {car['year']} أفضل خيار. {car['f']}"},
            {"role":"user","content":"عنده بانوراما؟"},
            {"role":"assistant","content":f"إي، {car['n']} فيه بانوراما وكاميرا 360 وشاشة كبيرة"},
            {"role":"user","content":"زين، شوكت أكدر آجي أشوفه؟"},
            {"role":"assistant","content":"أي وقت، المعرض مفتوح من 9 الصبح لـ7 المسا"},
        ]
    elif tpl == 8:
        msgs = [
            {"role":"user","content":f"{pick(SHORT_GREET)}، {car['n']} بنزين ولا هجين؟"},
            {"role":"assistant","content":f"{car['n']} موديل {car['year']} متوفر بنزين وهجين"},
            {"role":"user","content":f"الهجين {howmuch()}؟"},
            {"role":"assistant","content":f"الهجين أغلى شوية، بـ{vp(car['p']*1.15)} دينار بس يوفر بالبنزين"},
            {"role":"user","content":"والبنزين؟"},
            {"role":"assistant","content":f"البنزين بـ{vp(car['p'])} دينار"},
        ]
    elif tpl == 9:
        msgs = [
            {"role":"user","content":f"أريد أبيع سيارتي وأشتري {car['n']}. تشتري مني؟"},
            {"role":"assistant","content":"إي نشتري سيارات مستعملة. شنو سيارتك؟"},
            {"role":"user","content":"عندي كيا سبورتاج 2019"},
            {"role":"assistant","content":"ماشيه شكد؟"},
            {"role":"user","content":"حوالي 80 ألف كيلو"},
            {"role":"assistant","content":f"نشتريها بحوالي {vp(20000000)} دينار، والـ{car['n']} الجديد بـ{vp(car['p'])}. الفرق {vp(car['p']-20000000)}"},
        ]
    elif tpl == 10:
        _gc, _gs = greet_pair()
        msgs = [
            {"role":"user","content":_gc},
            {"role":"assistant","content":_gs},
            {"role":"user","content":f"أريد {car['n']}"},
            {"role":"assistant","content":f"{car['n']} موجود، {car['f']}. بـ{vp(car['p'])} دينار"},
            {"role":"user","content":f"{pick(DISC_REQ)}"},
            {"role":"assistant","content":f"{pick(DISC_NO)}"},
            {"role":"user","content":"زين افكر"},
            {"role":"assistant","content":"حياك الله، تعال بأي وقت"},
        ]
    elif tpl == 11:
        msgs = [
            {"role":"user","content":f"هلو، {car['n']} موديل {car['year']} أكو فيه مشاكل معروفة؟"},
            {"role":"assistant","content":f"لا والله، {car['n']} {car['year']} من أوثق السيارات. ما فيه مشاكل مشهورة"},
            {"role":"user","content":"وقطع الغيار موجودة بالعراق؟"},
            {"role":"assistant","content":"إي، قطع الغيار وفيرة وأسعارها معقولة"},
            {"role":"user","content":"زين، هذا مهم. هاي الفلوس"},
            {"role":"assistant","content":f"{pick(CLOSE)}"},
        ]
    elif tpl == 12:
        msgs = [
            {"role":"user","content":f"أريد {car['n']} بس أريده بلون أبيض"},
            {"role":"assistant","content":f"الأبيض موجود هسه. {car['n']} {car['year']}، {car['f']}"},
            {"role":"user","content":"والرمادي عندكم؟"},
            {"role":"assistant","content":"الرمادي يوصل الأسبوع الجاي"},
            {"role":"user","content":"آخذ الأبيض الموجود"},
            {"role":"assistant","content":f"{vp(car['p'])} دينار. {pick(CLOSE)}"},
        ]
    elif tpl == 13:
        msgs = [
            {"role":"user","content":f"مرحبا، عندكم {car['n']} للتأجير؟"},
            {"role":"assistant","content":f"إي عندنا تأجير. {car['n']} بـ{vp(car['p']//300)} دينار يومياً"},
            {"role":"user","content":"أسبوع كامل؟"},
            {"role":"assistant","content":f"أسبوع بـ{vp(car['p']//45)} دينار، يشمل التأمين"},
            {"role":"user","content":"هل تحتاج رهينة؟"},
            {"role":"assistant","content":"إي، نأخذ نسخة من الهوية وكفيل"},
        ]
    elif tpl == 14:
        msgs = [
            {"role":"user","content":f"هلو، {car['n']} استهلاك البنزين شكد؟"},
            {"role":"assistant","content":f"{car['n']} يستهلك تقريباً 8 لتر لكل 100 كيلو بالطريق السريع"},
            {"role":"user","content":"والمدينة؟"},
            {"role":"assistant","content":"بالمدينة حوالي 11-12 لتر"},
            {"role":"user","content":"معقول، زين. السعر؟"},
            {"role":"assistant","content":f"{vp(car['p'])} دينار، {car['f']}"},
        ]
    elif tpl == 15:
        msgs = [
            {"role":"user","content":f"هلو، أريد {car['n']} فاخر، عندكم؟"},
            {"role":"assistant","content":f"إي، {car['n']} فاخر بـ{vp(car['p'])} دينار. {car['f']}"},
            {"role":"user","content":"شاشة الملاحة موجودة؟"},
            {"role":"assistant","content":"إي، شاشة لمسية 12 إنش مع GPS وأندرويد أوتو وكارپلاي"},
            {"role":"user","content":"والنظام الصوتي؟"},
            {"role":"assistant","content":"Bose ثمانية مكبرات، صوته جنان"},
        ]
    elif tpl == 16:
        msgs = [
            {"role":"user","content":f"عندي سيارة قديمة، ما تبدلها بـ{car['n']} جديد؟"},
            {"role":"assistant","content":"إي نشتري مستعملة ونجيبك جديد. شنو سيارتك؟"},
            {"role":"user","content":"تويوتا كورولا 2018"},
            {"role":"assistant","content":f"نشتريها بـ{vp(15000000)} دينار، والـ{car['n']} بـ{vp(car['p'])}. الفرق {vp(car['p']-15000000)}"},
            {"role":"user","content":"ماشي، اتفقنا"},
            {"role":"assistant","content":"زين، نسوي الأوراق"},
        ]
    elif tpl == 17:
        msgs = [
            {"role":"user","content":f"هلو، {car['n']} بيها كاميرا 360؟"},
            {"role":"assistant","content":f"نعم، {car['n']} {car['year']} عنده كاميرا 360 درجة وشاشات جانبية"},
            {"role":"user","content":"وحساسات الركن؟"},
            {"role":"assistant","content":"إي، أمامية وخلفية، وتنبيه تلقائي لو اقتربت من شي"},
            {"role":"user","content":"زين، هذا يجلب"},
            {"role":"assistant","content":f"سعره {vp(car['p'])} دينار. شوكت تأخذه؟"},
        ]
    elif tpl == 18:
        msgs = [
            {"role":"user","content":f"مرحبا، أريد {car['n']} بس ما أريد يكون مستعمل من المعارض"},
            {"role":"assistant","content":"إي عندنا وارد مباشر من الوكالة. جديد وبالكرتون تقريباً"},
            {"role":"user","content":"الوثائق الجمركية موجودة؟"},
            {"role":"assistant","content":"إي، بيان الجمارك وإجازة الاستيراد كلها موجودة"},
            {"role":"user","content":"ممتاز، شنو السعر؟"},
            {"role":"assistant","content":f"{vp(car['p'])} دينار شامل كل الرسوم"},
        ]
    elif tpl == 19:
        msgs = [
            {"role":"user","content":f"هلو، {car['n']} أمانه زينة؟"},
            {"role":"assistant","content":f"إي، {car['n']} حاصل على 5 نجوم في تقييمات السلامة الأوروبية"},
            {"role":"user","content":"وعنده ABS وairbag؟"},
            {"role":"assistant","content":"إي، 6 وسادات هوائية وABS وESC وتحذير خروج المسار"},
            {"role":"user","content":"ممتاز، عيلتي سلامتها مهمة"},
            {"role":"assistant","content":f"هذا الخيار الأفضل للعيلة. بـ{vp(car['p'])} دينار"},
        ]
    elif tpl == 20:
        msgs = [
            {"role":"user","content":f"هلو، أريد {car['n']} ألوانه شنو؟"},
            {"role":"assistant","content":f"{car['n']} متوفر بأبيض وأسود ورمادي وأزرق وأحمر"},
            {"role":"user","content":"أيهم أكثر مبيع؟"},
            {"role":"assistant","content":"الأبيض والأسود الأكثر طلب، بس الأزرق خاص"},
            {"role":"user","content":"آخذ الأزرق، أحب شي نادر"},
            {"role":"assistant","content":f"ذوق راقي! {vp(car['p'])} دينار. {pick(CLOSE)}"},
        ]
    elif tpl == 21:
        msgs = [
            {"role":"user","content":f"مساء الخير، أريد فحص {car['n']} قبل الشراء"},
            {"role":"assistant","content":"ماشي، نرسله مع فني لأي كراج تختاره"},
            {"role":"user","content":"يعني تسمحون بالفحص؟"},
            {"role":"assistant","content":"إي طبعاً، السيارة ما عندها شي نخفيه"},
            {"role":"user","content":"ممتاز، أرسله لكراج صاحبي"},
            {"role":"assistant","content":"تفضل، نرسله معك أو مع السواق"},
        ]
    elif tpl == 22:
        msgs = [
            {"role":"user","content":f"هلو، كيف تنقل {car['n']} بعد الشراء؟"},
            {"role":"assistant","content":"تقدر تسوق بنفسك أو نوصله لعندك"},
            {"role":"user","content":"التوصيل بكم؟"},
            {"role":"assistant","content":"داخل بغداد مجاناً. خارج بغداد 50,000 دينار"},
            {"role":"user","content":"أسكن في الديوانية"},
            {"role":"assistant","content":"ماشي، نوصله الديوانية بـ50,000 دينار زيادة"},
        ]
    elif tpl == 23:
        msgs = [
            {"role":"user","content":f"هلو، {car['n']} عنده أوبشن ما ذكرته؟"},
            {"role":"assistant","content":f"{car['n']} {car['year']} {car['f']}. زيادة: فتحة سقف، كراسي جلد، تبريد مقاعد"},
            {"role":"user","content":"والشاحن اللاسلكي؟"},
            {"role":"assistant","content":"إي موجود، شحن لاسلكي Qi Standard"},
            {"role":"user","content":"هذا كافي، آخذه"},
            {"role":"assistant","content":f"{pick(CLOSE)}"},
        ]
    elif tpl == 24:
        msgs = [
            {"role":"user","content":f"أريد {car['n']} بس أريد أفاوض على السعر"},
            {"role":"assistant","content":f"هلا، سعره {vp(car['p'])} دينار. شنو تقترح؟"},
            {"role":"user","content":f"أعطيك {vp(int(car['p']*0.88))} دينار"},
            {"role":"assistant","content":f"والله صعب، بس على خاطرك نوصل {vp(int(car['p']*0.93))} وهذا آخر سعر"},
            {"role":"user","content":"اتفقنا على هذا"},
            {"role":"assistant","content":"ممتاز، نسوي الأوراق"},
        ]
    else:
        msgs = [
            {"role":"user","content":f"هلو، أريد سيارة عائلية، شنو تنصحني؟"},
            {"role":"assistant","content":f"{car['n']} {car['year']} ممتاز للعائلة. {car['f']}"},
            {"role":"user","content":"المقاعد شكد؟"},
            {"role":"assistant","content":"5 مقاعد، كراسي خلفية واسعة وكراج واسع"},
            {"role":"user","content":"السعر؟"},
            {"role":"assistant","content":f"{vp(car['p'])} دينار"},
        ]

    return {"id":f"cars_{i:04d}","category":"sales_cars","dialect":"iraqi_arabic","messages":msgs}

# ============================================================
# FILE 5 - REAL ESTATE
# ============================================================

PROPERTIES = [
    {"n":"بيت سكني","area":"الكرادة","size":"200 متر","p":300000000,"f":"3 غرف وصالة وحديقة"},
    {"n":"شقة","area":"المنصور","size":"150 متر","p":180000000,"f":"3 غرف وبلكونة"},
    {"n":"قطعة أرض","area":"الدورة","size":"400 متر","p":120000000,"f":"على شارعين"},
    {"n":"بيت قديم","area":"الكاظمية","size":"180 متر","p":150000000,"f":"قابل للهدم والبناء"},
    {"n":"شقة فندقية","area":"العرصات","size":"80 متر","p":250000000,"f":"فرشة كاملة، مسبح"},
    {"n":"بيت حديث","area":"حي بابل","size":"250 متر","p":500000000,"f":"طابقين، كلادينج"},
    {"n":"محل تجاري","area":"السيدية","size":"50 متر","p":200000000,"f":"على شارع رئيسي"},
    {"n":"عمارة","area":"الزعفرانية","size":"600 متر","p":800000000,"f":"4 طوابق، 8 شقق"},
    {"n":"فيلا","area":"المعلف","size":"350 متر","p":900000000,"f":"مسبح وحديقة وكراج"},
    {"n":"شقة","area":"الأعظمية","size":"120 متر","p":140000000,"f":"طابق ثالث، إطلالة على الشارع"},
    {"n":"بيت","area":"الحارثية","size":"230 متر","p":380000000,"f":"4 غرف وصالة كبيرة"},
    {"n":"محل تجاري","area":"الشعب","size":"80 متر","p":160000000,"f":"زاوية، على شارعين"},
    {"n":"شقة","area":"الجادرية","size":"170 متر","p":220000000,"f":"3 غرف، قرب الجامعة"},
    {"n":"بيت شعبي","area":"الشعلة","size":"150 متر","p":100000000,"f":"غرفتان وحوش كبير"},
    {"n":"قطعة أرض","area":"حي الرشيد","size":"300 متر","p":90000000,"f":"على شارع رئيسي، مسورة"},
    {"n":"طابق كامل","area":"الكرخ","size":"200 متر","p":350000000,"f":"4 شقق صغيرة، إيجار جاهز"},
]

def gen_realestate(i):
    prop = pick(PROPERTIES)
    tpl = random.randint(1, 25)

    if tpl == 1:
        msgs = [
            {"role":"user","content":f"{pick(SHORT_GREET)}، أريد {prop['n']} بـ{prop['area']}"},
            {"role":"assistant","content":f"هلا، عندنا {prop['n']} بـ{prop['area']}. {prop['size']}، {prop['f']}. سعره {vp(prop['p'])} دينار"},
            {"role":"user","content":"يعني بالدولار؟"},
            {"role":"assistant","content":f"حوالي {vp(prop['p']//1300)} دولار"},
            {"role":"user","content":"أكدر أشوفه؟"},
            {"role":"assistant","content":"إي طبعاً، شوكت تريد نرتب موعد"},
        ]
    elif tpl == 2:
        msgs = [
            {"role":"user","content":f"هلو، عندكم {prop['n']} للإيجار بـ{prop['area']}؟"},
            {"role":"assistant","content":f"إي عندنا، الإيجار الشهري {vp(prop['p']//300)} دينار شهري"},
            {"role":"user","content":"هذا غالي، ما أكو أرخص؟"},
            {"role":"assistant","content":f"هذا سعر المنطقة يا أخوي. بس لو تريد أبعد شوية عندنا بـ{vp(prop['p']//400)} دينار"},
            {"role":"user","content":"أريد أشوف الخيارين"},
            {"role":"assistant","content":"ماشي، نرتب موعد هذا الأسبوع"},
        ]
    elif tpl == 3:
        msgs = [
            {"role":"user","content":f"أريد أبيع {prop['n']} عندي"},
            {"role":"assistant","content":"أهلاً، في يا منطقة وشنو المساحة؟"},
            {"role":"user","content":f"بـ{prop['area']}، {prop['size']}"},
            {"role":"assistant","content":f"منطقة زينة. سعر السوق الحالي للمنطقة هذي حوالي {vp(prop['p'])} دينار"},
            {"role":"user","content":"أريد أكثر من هذا"},
            {"role":"assistant","content":"ماشي، نشوف ونفاوض على السعر. شنو أقل سعر تقبله؟"},
        ]
    elif tpl == 4:
        msgs = [
            {"role":"user","content":f"{pick(SHORT_GREET)}، ميزانيتي 200 مليون دينار، ما تنصحني بيه؟"},
            {"role":"assistant","content":f"بهالميزانية عندنا {prop['n']} بـ{prop['area']}. {prop['size']}، {prop['f']}"},
            {"role":"user","content":"السند طابو ولا عقد عرفي؟"},
            {"role":"assistant","content":"السند طابو رسمي، لا تعب"},
            {"role":"user","content":"زين هذا يجلب، شوكت أكدر أشوفه؟"},
            {"role":"assistant","content":"تفضل غداً الصبح إن شاء الله"},
        ]
    elif tpl == 5:
        msgs = [
            {"role":"user","content":f"هلو، {prop['n']} بـ{prop['area']} قريب من المدارس؟"},
            {"role":"assistant","content":f"إي، على بعد 500 متر من مدرسة"},
            {"role":"user","content":"والمستشفى؟"},
            {"role":"assistant","content":"قريب من مركز صحي وعلى بعد 2 كيلو من مستشفى"},
            {"role":"user","content":"زين، السعر؟"},
            {"role":"assistant","content":f"{vp(prop['p'])} دينار كلشي"},
        ]
    elif tpl == 6:
        msgs = [
            {"role":"user","content":f"مرحبا، عندكم {prop['n']} للبيع بالتقسيط؟"},
            {"role":"assistant","content":"إي عندنا تقسيط. شكد مقدم تكدر تدفع؟"},
            {"role":"user","content":"أكدر أدفع 30% مقدم"},
            {"role":"assistant","content":f"المقدم {vp(prop['p']*0.30)} دينار والباقي على 5 سنين"},
            {"role":"user","content":"فائدة عليه؟"},
            {"role":"assistant","content":"10% سنوي، وهذا سعر معقول للسوق"},
        ]
    elif tpl == 7:
        msgs = [
            {"role":"user","content":f"{pick(SHORT_GREET)}، أريد {prop['n']} بس ما أعرف المنطقة زينة ولا لا"},
            {"role":"assistant","content":f"{prop['area']} منطقة هادية، خدمات كاملة وأمنية زينة"},
            {"role":"user","content":"الجيران شلونهم؟"},
            {"role":"assistant","content":"عوايل محترمة، هادية"},
            {"role":"user","content":"زين، أجيك بكره أشوف"},
            {"role":"assistant","content":"حياك الله، أنا موجود"},
        ]
    elif tpl == 8:
        msgs = [
            {"role":"user","content":f"هلو، {prop['n']} هذا عنده مشاكل قانونية؟"},
            {"role":"assistant","content":"لا والله، كلشي نظيف. طابو رسمي وما عليه ديون"},
            {"role":"user","content":"أكدر أشوف الوثائق؟"},
            {"role":"assistant","content":"إي طبعاً، تعال أي وقت وأريك كل الأوراق"},
            {"role":"user","content":"ماشي، أجي بكره"},
            {"role":"assistant","content":"تفضل، بانتظارك"},
        ]
    elif tpl == 9:
        msgs = [
            {"role":"user","content":f"أريد {prop['n']} لكن مو للسكن، للاستثمار"},
            {"role":"assistant","content":f"ممتاز، {prop['n']} بـ{prop['area']} استثمار زين. الإيجار الشهري {vp(prop['p']//300)} دينار"},
            {"role":"user","content":"يعني العائد السنوي شكد؟"},
            {"role":"assistant","content":f"حوالي 8-10% سنوياً، هذا عائد ممتاز"},
            {"role":"user","content":"زين، أفكر وأجيك"},
            {"role":"assistant","content":"حياك الله بأي وقت"},
        ]
    elif tpl == 10:
        _gc, _gs = greet_pair()
        msgs = [
            {"role":"user","content":_gc},
            {"role":"assistant","content":_gs},
            {"role":"user","content":f"أريد {prop['n']} بـ{prop['area']}"},
            {"role":"assistant","content":f"عندنا {prop['n']} بـ{prop['area']}، {prop['f']}. بـ{vp(prop['p'])} دينار"},
            {"role":"user","content":"أشوفه؟"},
            {"role":"assistant","content":"تفضل أي وقت"},
        ]
    elif tpl == 11:
        msgs = [
            {"role":"user","content":f"أريد {prop['n']} بـ{prop['area']} للطلاب، بكري أو بدون عائلة؟"},
            {"role":"assistant","content":f"عندنا {prop['n']} {prop['size']} بـ{prop['area']}، مناسب للطلاب. إيجاره {vp(prop['p']//350)} دينار"},
            {"role":"user","content":"شو الشروط؟"},
            {"role":"assistant","content":"عقد لسنة، مقدم شهرين، ما في مشكلة طلاب"},
            {"role":"user","content":"تعجبني، أجيكم أشوف"},
            {"role":"assistant","content":"حياك، الباب مفتوح أي يوم"},
        ]
    elif tpl == 12:
        msgs = [
            {"role":"user","content":f"أريد مكتب تجاري بـ{prop['area']}"},
            {"role":"assistant","content":f"عندنا {prop['n']} {prop['size']} يصلح مكتب. {prop['f']}. بـ{vp(prop['p'])} دينار"},
            {"role":"user","content":"التيار والماء نظامي؟"},
            {"role":"assistant","content":"إي، كلشي رسمي، كهرباء وطنية وماء شبكة"},
            {"role":"user","content":"أكدر أعمل واجهة؟"},
            {"role":"assistant","content":"إي ممكن، المكان يسمح بواجهة تجارية"},
        ]
    elif tpl == 13:
        budget1 = vp(random.randint(100, 200) * 1000000)
        budget2 = vp(random.randint(200, 400) * 1000000)
        msgs = [
            {"role":"user","content":f"شو الفرق بين {prop['area']} ومنطقة المنصور؟"},
            {"role":"assistant","content":f"{prop['area']} أسعارها معقولة، هادية وخدمات كاملة. المنصور أغلى بس أرقى"},
            {"role":"user","content":f"ميزانيتي بين {budget1} و{budget2} دينار"},
            {"role":"assistant","content":f"بهالميزانية {prop['area']} خيار ممتاز. عندنا {prop['n']} {prop['size']}"},
            {"role":"user","content":"نرتب موعد مشاهدة؟"},
            {"role":"assistant","content":"إي تفضل، نرتب الأسبوع الياي"},
        ]
    elif tpl == 14:
        msgs = [
            {"role":"user","content":f"هلو، {prop['n']} بـ{prop['area']} قريب من الباص والسرفيس؟"},
            {"role":"assistant","content":f"إي، على بعد دقيقتين من خط السرفيس الرئيسي"},
            {"role":"user","content":"ومحطة الباص السريع؟"},
            {"role":"assistant","content":"5 دقايق مشي من محطة BRT"},
            {"role":"user","content":"زين، هذا مهم لينا. شكد السعر؟"},
            {"role":"assistant","content":f"{vp(prop['p'])} دينار، وتقدر تفاوض بعد المشاهدة"},
        ]
    elif tpl == 15:
        msgs = [
            {"role":"user","content":f"هلو، شلون البنية التحتية بـ{prop['area']}؟"},
            {"role":"assistant","content":f"كهرباء وطنية 12 ساعة يومياً، ماء شبكة منتظم، صرف صحي كامل"},
            {"role":"user","content":"والشوارع؟"},
            {"role":"assistant","content":"معبدة وواسعة، ما فيها ازدحام"},
            {"role":"user","content":"زين، عندكم {prop['n']} بهاي المنطقة؟"},
            {"role":"assistant","content":f"إي، {prop['n']} {prop['size']}، {prop['f']}. بـ{vp(prop['p'])} دينار"},
        ]
    elif tpl == 16:
        msgs = [
            {"role":"user","content":f"أريد {prop['n']} كبير، عيلتي كبيرة"},
            {"role":"assistant","content":f"عندنا {prop['n']} {prop['size']} بـ{prop['area']}، {prop['f']}. يسع عيلة كبيرة"},
            {"role":"user","content":"الحوش واسع؟"},
            {"role":"assistant","content":"إي، فيه حوش ومنطقة خضراء"},
            {"role":"user","content":"يعجبني. كيف نرتب المشاهدة؟"},
            {"role":"assistant","content":"تعطيني رقمك وأتصل بيك لنرتب موعد مناسب"},
        ]
    elif tpl == 17:
        msgs = [
            {"role":"user","content":f"أريد أهدم البيت وأبني من جديد. {prop['n']} بـ{prop['area']} مناسب؟"},
            {"role":"assistant","content":f"إي، {prop['n']} قابل للهدم والبناء. {prop['size']}، البلدية تسمح ببناء طابقين"},
            {"role":"user","content":"الجيران ما يصيرون مشكلة؟"},
            {"role":"assistant","content":"لا، المنطقة معتادة على البناء"},
            {"role":"user","content":"شكد السعر؟"},
            {"role":"assistant","content":f"{vp(prop['p'])} دينار، وسعر الأرض لوحدها يستاهل"},
        ]
    elif tpl == 18:
        msgs = [
            {"role":"user","content":f"تريد تشارك بمشروع سكني بـ{prop['area']}؟"},
            {"role":"assistant","content":"ممكن، شنو الفكرة؟"},
            {"role":"user","content":f"أشتري {prop['n']} وأبني عليه عمارة، تشارك بالتمويل"},
            {"role":"assistant","content":"فكرة زينة. اللي عندنا الأرض وإنتو التمويل نكتب عقد واضح"},
            {"role":"user","content":"موافق من مبدأ. نرتب اجتماع؟"},
            {"role":"assistant","content":"إي، نرتب قريب مع المحامي والمهندس"},
        ]
    elif tpl == 19:
        msgs = [
            {"role":"user","content":f"هلو، {prop['n']} بـ{prop['area']} مفروش؟"},
            {"role":"assistant","content":"إي فيه مفروش وغير مفروش، تريد أيش؟"},
            {"role":"user","content":"مفروش، كامل؟"},
            {"role":"assistant","content":f"الإصدار المفروش فيه كلشي: كنبة وغرف نوم وأجهزة. الإيجار {vp(prop['p']//250)} دينار"},
            {"role":"user","content":"والغير مفروش؟"},
            {"role":"assistant","content":f"{vp(prop['p']//350)} دينار، ووفر على الفرشة"},
        ]
    elif tpl == 20:
        msgs = [
            {"role":"user","content":f"أريد أتأكد من الصكوك قبل الشراء"},
            {"role":"assistant","content":"صح، هذا واجب. عندنا طابو رسمي بالكوادستر"},
            {"role":"user","content":"أكدر أروح أتحقق بنفسي؟"},
            {"role":"assistant","content":"إي طبعاً، معك رقم الصك وتروح دائرة التسجيل العقاري"},
            {"role":"user","content":"زين، شو رقم الصك؟"},
            {"role":"assistant","content":"أعطيك نسخة من الصك الأصلي لما تجيك للمشاهدة"},
        ]
    elif tpl == 21:
        msgs = [
            {"role":"user","content":f"أريد تقييم {prop['n']} عندي بـ{prop['area']}"},
            {"role":"assistant","content":"ماشي، شنو المساحة وعمر البناء؟"},
            {"role":"user","content":f"{prop['size']}، بنيت قبل 10 سنين"},
            {"role":"assistant","content":f"بناءً على سعر السوق بـ{prop['area']}، تقييمه الأولي {vp(prop['p'])} دينار"},
            {"role":"user","content":"أريد مقيّم رسمي؟"},
            {"role":"assistant","content":"إي نقدر نرسل مقيّم معتمد خلال يومين"},
        ]
    elif tpl == 22:
        msgs = [
            {"role":"user","content":"هلو، في بيوت بالتقسيط الحكومي؟"},
            {"role":"assistant","content":f"إي، فيه مبادرة الإسكان الحكومية. عندنا {prop['n']} بـ{prop['area']} مشمول بالبرنامج"},
            {"role":"user","content":"الشروط شنو؟"},
            {"role":"assistant","content":"راتب حكومي أو تقاعد، وما تملك دار قبل"},
            {"role":"user","content":"مناسب ليا، شو الخطوة الجاية؟"},
            {"role":"assistant","content":"تعال بالوثائق الرسمية ونبدأ التقديم معك"},
        ]
    elif tpl == 23:
        commission = vp(prop['p'] * 0.02)
        msgs = [
            {"role":"user","content":f"إنتو وسطاء ولا أصحاب الملك؟"},
            {"role":"assistant","content":"وسطاء معتمدين، نمثل صاحب الملك بالكامل"},
            {"role":"user","content":"العمولة شكد؟"},
            {"role":"assistant","content":f"2% من قيمة البيع، يعني {commission} دينار على {prop['n']} هذا"},
            {"role":"user","content":"أكدر أتفاوض على العمولة؟"},
            {"role":"assistant","content":"هذا السعر الأدنى، بس نشوف لو الصفقة كبيرة"},
        ]
    elif tpl == 24:
        monthly_rent = vp(prop['p'] // 300)
        annual_return = vp(prop['p'] * 10 // 100)
        msgs = [
            {"role":"user","content":f"أريد أعرف العائد الإيجاري بالتفصيل لـ{prop['n']} بـ{prop['area']}"},
            {"role":"assistant","content":f"الإيجار الشهري {monthly_rent} دينار، يعني سنوياً {annual_return} دينار"},
            {"role":"user","content":"وبعد خمس سنين، السعر يرتفع؟"},
            {"role":"assistant","content":f"متوقع ارتفاع 15-20% على الأقل في {prop['area']} بسبب المشاريع الحكومية القادمة"},
            {"role":"user","content":"استثمار ممتاز، فكر أشتري"},
            {"role":"assistant","content":"صح، ولا تتردد كثير لأن الطلب على المنطقة يزيد"},
        ]
    else:
        msgs = [
            {"role":"user","content":f"مرحبا، أريد أسأل عن {prop['n']} بـ{prop['area']}"},
            {"role":"assistant","content":f"أهلاً وسهلاً، {prop['n']} بـ{prop['area']}، {prop['size']}، {prop['f']}"},
            {"role":"user","content":"السعر كامل؟"},
            {"role":"assistant","content":f"إي، {vp(prop['p'])} دينار شامل كل التكاليف"},
            {"role":"user","content":"زين، أتفكر وأجيك"},
            {"role":"assistant","content":"حياك، أنا موجود"},
        ]

    return {"id":f"re_{i:04d}","category":"sales_realestate","dialect":"iraqi_arabic","messages":msgs}

# ============================================================
# FILE 6 - FURNITURE & HOME
# ============================================================

FURNITURE = [
    {"n":"غرفة نوم كاملة","p":2500000,"f":"خشب زان، تصميم حديث، 5 قطع"},
    {"n":"صالون","p":1800000,"f":"قماش مخمل، 7 مقاعد، ألوان متنوعة"},
    {"n":"طاولة سفرة","p":600000,"f":"زجاج وستيل، 6 كراسي"},
    {"n":"كنبة","p":800000,"f":"جلد طبيعي، 3+1+1"},
    {"n":"مطبخ ألمنيوم","p":3000000,"f":"هايگلوس، أدراج ناعمة"},
    {"n":"تكييف سبليت","p":750000,"f":"18 آلاف BTU، انفرتر"},
    {"n":"ثلاجة","p":650000,"f":"نو فروست، 450 لتر"},
    {"n":"غسالة","p":400000,"f":"9 كيلو، فرونت لودر"},
    {"n":"ميكرويف","p":150000,"f":"30 لتر، شاشة ديجيتال"},
    {"n":"فرن غاز","p":350000,"f":"5 شعلات، فرن كبير"},
    {"n":"جهاز بخار","p":120000,"f":"للملابس والمنزل"},
    {"n":"مروحة سقف","p":90000,"f":"بريموتكونترول، ضمان سنتين"},
]

def gen_furniture(i):
    item = pick(FURNITURE)
    tpl = random.randint(1, 25)

    if tpl == 1:
        msgs = [
            {"role":"user","content":f"{pick(SHORT_GREET)}، أريد {item['n']}"},
            {"role":"assistant","content":f"هلا، {item['n']} عندنا. {item['f']}. سعره {vp(item['p'])} دينار"},
            {"role":"user","content":f"{pick(EXPENSIVE)}"},
            {"role":"assistant","content":f"هذا سعر الجودة، {item['f']}. مو غالي والله"},
            {"role":"user","content":f"{pick(DISC_REQ)}"},
            {"role":"assistant","content":f"{pick(DISC_YES)}"},
            {"role":"user","content":"ماشي، خذ"},
            {"role":"assistant","content":f"{pick(CLOSE)}"},
        ]
    elif tpl == 2:
        msgs = [
            {"role":"user","content":f"هلو، أريد تأثيث بيت جديد، شنو عندكم؟"},
            {"role":"assistant","content":"أهلاً، عندنا كل شي للبيت. تريد تبدأ بيا غرفة؟"},
            {"role":"user","content":"من غرفة النوم"},
            {"role":"assistant","content":f"غرفة نوم كاملة عندنا بـ{vp(2500000)} دينار. خشب زان وتصميم حديث"},
            {"role":"user","content":"وإذا اشتريت كل شي، تعطيني خصم؟"},
            {"role":"assistant","content":"إي طبعاً، لو اشتريت كل شي بالمرة نعطيك 15% خصم"},
        ]
    elif tpl == 3:
        msgs = [
            {"role":"user","content":f"مرحبا، {item['n']} يجي بالتوصيل؟"},
            {"role":"assistant","content":"إي، عندنا توصيل وتركيب مجاني داخل بغداد"},
            {"role":"user","content":"وخارج بغداد؟"},
            {"role":"assistant","content":"خارج بغداد بأجرة حسب المسافة"},
            {"role":"user","content":"أنا بالنجف"},
            {"role":"assistant","content":f"النجف بـ50 ألف دينار توصيل. و{item['n']} بـ{vp(item['p'])} دينار"},
        ]
    elif tpl == 4:
        msgs = [
            {"role":"user","content":f"{pick(SHORT_GREET)}، {item['n']} هذا من يا بلد؟"},
            {"role":"assistant","content":"صناعة تركية ممتازة"},
            {"role":"user","content":"الصيني والتركي شنو الفرق؟"},
            {"role":"assistant","content":"التركي جودته أحسن وأصمد، الصيني أرخص بس ما يدوم"},
            {"role":"user","content":"زين، أاخذ التركي"},
            {"role":"assistant","content":f"خيار زين! بـ{vp(item['p'])} دينار. {pick(CLOSE)}"},
        ]
    elif tpl == 5:
        msgs = [
            {"role":"user","content":f"أريد {item['n']} بس ميزانيتي محدودة"},
            {"role":"assistant","content":"شنو ميزانيتك؟"},
            {"role":"user","content":"500 ألف دينار"},
            {"role":"assistant","content":f"عندنا {item['n']} بـ{vp(min(item['p'],500000))} دينار. بسيط بس زين"},
            {"role":"user","content":"أشوفه؟"},
            {"role":"assistant","content":"تفضل هنا"},
        ]
    elif tpl == 6:
        msgs = [
            {"role":"user","content":f"هلو، {item['n']} عنده ضمان؟"},
            {"role":"assistant","content":f"إي، {item['n']} عنده ضمان سنتين ضد عيوب الصناعة"},
            {"role":"user","content":"وإذا انكسر؟"},
            {"role":"assistant","content":"نجي نصلحه بالمجان خلال الضمان"},
            {"role":"user","content":"زين، هذا يجلب"},
            {"role":"assistant","content":f"بـ{vp(item['p'])} دينار. {pick(CLOSE)}"},
        ]
    elif tpl == 7:
        msgs = [
            {"role":"user","content":f"مرحبا، {item['n']} عندكم بالتقسيط؟"},
            {"role":"assistant","content":"إي، تقسيط بدون فائدة على 6 أشهر"},
            {"role":"user","content":"القسط الشهري شكد؟"},
            {"role":"assistant","content":f"السعر {vp(item['p'])} دينار. على 6 أشهر = {vp(item['p']//6)} شهري"},
            {"role":"user","content":"ماشي، أاخذه بالتقسيط"},
            {"role":"assistant","content":"تفضل، نكمل الأوراق"},
        ]
    elif tpl == 8:
        msgs = [
            {"role":"user","content":f"{pick(SHORT_GREET)}، ما عجبني ـ{item['n']} اشتريته من عندكم"},
            {"role":"assistant","content":"شنو المشكلة؟"},
            {"role":"user","content":"لون مو نفس اللي شفته بالصورة"},
            {"role":"assistant","content":"هسه نحله، إذا عندنا اللون تبدله وإذا ما أكو نرجع الفلوس"},
            {"role":"user","content":"ماشي، شوف عندكم لون أبيض"},
            {"role":"assistant","content":"عندنا، تعال نبدله"},
        ]
    elif tpl == 9:
        msgs = [
            {"role":"user","content":f"سلام، أريد {item['n']} بس أريد أشوف عينات القماش"},
            {"role":"assistant","content":"تفضل، عندنا عينات أكثر من 20 لون ونوع قماش"},
            {"role":"user","content":"يا لون يناسب غرفة بيضاء؟"},
            {"role":"assistant","content":"للغرفة البيضاء، الرمادي أو البيج يطلع حلو هواي"},
            {"role":"user","content":"أاخذ الرمادي"},
            {"role":"assistant","content":f"ممتاز! {vp(item['p'])} دينار. {pick(CLOSE)}"},
        ]
    elif tpl == 10:
        msgs = [
            {"role":"user","content":f"{pick(SHORT_GREET)}، شنو عندكم من {item['n']}؟"},
            {"role":"assistant","content":f"عندنا {item['n']} ممتاز. {item['f']}. بـ{vp(item['p'])} دينار"},
            {"role":"user","content":f"{pick(DISC_REQ)}"},
            {"role":"assistant","content":f"{pick(DISC_YES)}"},
            {"role":"user","content":"ماشي"},
            {"role":"assistant","content":f"{pick(CLOSE)}"},
        ]
    elif tpl == 11:
        msgs = [
            {"role":"user","content":f"هلو، أريد {item['n']} بس مو نفس اللون، عندكم ألوان ثانية؟"},
            {"role":"assistant","content":f"إي، {item['n']} متوفر بـ5 ألوان: أبيض، رمادي، بيج، أسود، وخشبي"},
            {"role":"user","content":"أريد البيج"},
            {"role":"assistant","content":f"البيج موجود. {vp(item['p'])} دينار مع التوصيل"},
            {"role":"user","content":"شكراً، متى توصل؟"},
            {"role":"assistant","content":"خلال يومين، نتصل فيك قبل التوصيل"},
        ]
    elif tpl == 12:
        msgs = [
            {"role":"user","content":f"مرحبا، أريد أفرش غرفتين بنفس الوقت، كم يكلف؟"},
            {"role":"assistant","content":f"زين، {item['n']} لغرفتين = {vp(item['p']*2)} دينار. مع خصم 10% لأنك تاخذ اثنين"},
            {"role":"user","content":"والتوصيل والتركيب؟"},
            {"role":"assistant","content":"توصيل وتركيب مجاني إذا اشتريت أكثر من مليون دينار"},
            {"role":"user","content":"ممتاز، هذا مناسب"},
            {"role":"assistant","content":f"{pick(CLOSE)}"},
        ]
    elif tpl == 13:
        msgs = [
            {"role":"user","content":f"عندكم {item['n']} مستعمل؟"},
            {"role":"assistant","content":f"إي عندنا قسم مستعمل. {item['n']} بحالة زينة بـ{vp(int(item['p']*0.5))} دينار"},
            {"role":"user","content":"ليش مستعمل؟"},
            {"role":"assistant","content":"زبون غيّر ديكور بيته. بحالة ممتازة"},
            {"role":"user","content":"أشوفه؟"},
            {"role":"assistant","content":"تفضل، موجود بالمستودع"},
        ]
    elif tpl == 14:
        msgs = [
            {"role":"user","content":f"أريد {item['n']} بالأبعاد اللي أريدها، تصنعون حسب الطلب؟"},
            {"role":"assistant","content":"إي عندنا خدمة الصنع حسب الطلب. شنو الأبعاد؟"},
            {"role":"user","content":"العرض 2 متر والطول 3 متر"},
            {"role":"assistant","content":f"المصنوع حسب الطلب بـ{vp(int(item['p']*1.4))} دينار ويستغرق أسبوعين"},
            {"role":"user","content":"ماشي، كيف أطلب؟"},
            {"role":"assistant","content":"تعطيني القياسات بالتفصيل وتدفع نص مقدم"},
        ]
    elif tpl == 15:
        msgs = [
            {"role":"user","content":f"هلو، أريد أشوف {item['n']} بالكاتالوج"},
            {"role":"assistant","content":"تفضل، هذا كاتالوجنا. فيه أكثر من 50 تصميم"},
            {"role":"user","content":"هذا التصميم يعجبني، شكد سعره؟"},
            {"role":"assistant","content":f"هذا الموديل بـ{vp(item['p'])} دينار. يجي بألوان مختلفة"},
            {"role":"user","content":"عندكم بالأبيض؟"},
            {"role":"assistant","content":"إي، الأبيض متوفر. تريد تطلب؟"},
        ]
    elif tpl == 16:
        msgs = [
            {"role":"user","content":f"مساء الخير، أريد {item['n']} وعندي ديكور معين"},
            {"role":"assistant","content":"ماشي، صفلي ديكورك وأنصحك بالتصميم المناسب"},
            {"role":"user","content":"ديكوري أبيض وخشبي مع لمسات ذهبية"},
            {"role":"assistant","content":f"عندنا {item['n']} بتصميم كلاسيكي بخشب فاتح وتفاصيل ذهبية. بـ{vp(int(item['p']*1.2))} دينار"},
            {"role":"user","content":"يناسب، أشوفه في المعرض؟"},
            {"role":"assistant","content":"إي تفضل، المعرض مفتوح من الصبح"},
        ]
    elif tpl == 17:
        msgs = [
            {"role":"user","content":f"هلو، {item['n']} هذا يوصل للطابق الثالث؟"},
            {"role":"assistant","content":"إي، عندنا فريق متخصص بالتوصيل لأي طابق"},
            {"role":"user","content":"اسانسير ما أكو بالبناية"},
            {"role":"assistant","content":"ما يهم، فريقنا متعود على الشلالة. بس قد يكون في رسوم إضافية صغيرة"},
            {"role":"user","content":"شكد الرسوم؟"},
            {"role":"assistant","content":"5000 دينار إضافية لكل طابق فوق الثالث"},
        ]
    elif tpl == 18:
        msgs = [
            {"role":"user","content":f"مرحبا، أريد أعرف فترة تسليم {item['n']}"},
            {"role":"assistant","content":"المتوفر بالمخزن: خلال يومين. المصنوع حسب الطلب: أسبوعين"},
            {"role":"user","content":"وإذا ما وصل بالموعد؟"},
            {"role":"assistant","content":"نكفل التسليم بالموعد وإلا نعوضك 5% خصم"},
            {"role":"user","content":"زين، ضمانة واضحة"},
            {"role":"assistant","content":f"طبعاً، التزامنا بالزبون أولاً. بـ{vp(item['p'])} دينار"},
        ]
    elif tpl == 19:
        msgs = [
            {"role":"user","content":f"هلو، عندكم تنظيف {item['n']} بعد التوصيل؟"},
            {"role":"assistant","content":"إي، فريق التوصيل يركب ويمسح ويترك الغرفة نظيفة"},
            {"role":"user","content":"والكراتين؟"},
            {"role":"assistant","content":"نشيل الكراتين ونرمهم. ما تتعب بشي"},
            {"role":"user","content":"هذا ممتاز، آخذ"},
            {"role":"assistant","content":f"{pick(CLOSE)}"},
        ]
    elif tpl == 20:
        msgs = [
            {"role":"user","content":f"عندكم {item['n']} بالإيجار للمناسبات؟"},
            {"role":"assistant","content":"إي عندنا إيجار. اليوم الواحد بـ{vp(int(item['p']//30))} دينار"},
            {"role":"user","content":"3 أيام لعرس؟"},
            {"role":"assistant","content":f"3 أيام بـ{vp(int(item['p']//10))} دينار مع التوصيل والاستلام"},
            {"role":"user","content":"ماشي، متفق"},
            {"role":"assistant","content":"نحتاج وديعة 100 ألف ترجع بعد الاستلام"},
        ]
    elif tpl == 21:
        msgs = [
            {"role":"user","content":f"أريد {item['n']} بس الكراج ضيق، يدخل؟"},
            {"role":"assistant","content":"شنو أبعاد الكراج؟"},
            {"role":"user","content":"باب الكراج عرضه 90 سم"},
            {"role":"assistant","content":f"عندنا {item['n']} بعرض 85 سم يدخل. أو نركب المتقطع: تدخله قطعة قطعة"},
            {"role":"user","content":"المتقطع أفضل"},
            {"role":"assistant","content":"ماشي، هذا خيار زين"},
        ]
    elif tpl == 22:
        msgs = [
            {"role":"user","content":f"هلو، عندكم كتالوج أون لاين أشوف {item['n']} منه؟"},
            {"role":"assistant","content":"إي عندنا صفحة إنستغرام وتيك توك فيها كل منتجاتنا"},
            {"role":"user","content":"المنتج اللي شفته بالإنستغرام موجود؟"},
            {"role":"assistant","content":f"إي متوفر. {item['n']} بـ{vp(item['p'])} دينار"},
            {"role":"user","content":"أطلب أون لاين؟"},
            {"role":"assistant","content":"إي، ترسل رسالة على الواتساب ونكمل"},
        ]
    elif tpl == 23:
        msgs = [
            {"role":"user","content":f"مرحبا، {item['n']} عنده ضمان ضد الحشرات؟"},
            {"role":"assistant","content":"إي، الأخشاب عندنا مطلية بطارد حشرات ومانع رطوبة"},
            {"role":"user","content":"لمدة كم؟"},
            {"role":"assistant","content":"الطلاء يدوم 5 سنين على الأقل"},
            {"role":"user","content":"ممتاز، هذا مهم بالعراق"},
            {"role":"assistant","content":f"صح، اهتمينا بهذا الموضوع. بـ{vp(item['p'])} دينار"},
        ]
    elif tpl == 24:
        msgs = [
            {"role":"user","content":f"هلو، ما أدري شأختار {item['n']} ولا شي ثاني"},
            {"role":"assistant","content":"قولي شنو اللي تبحث عنه وأساعدك تختار"},
            {"role":"user","content":"أريد شي عملي ومريح وبسعر معقول"},
            {"role":"assistant","content":f"{item['n']} مثالي: {item['f']}. بـ{vp(item['p'])} دينار"},
            {"role":"user","content":"يبدو مناسب، آخذه"},
            {"role":"assistant","content":f"{pick(CLOSE)}"},
        ]
    else:
        msgs = [
            {"role":"user","content":f"هلو، أريد أفرش شقتي الجديدة"},
            {"role":"assistant","content":"مبارك على الشقة! نحن متخصصين بتأثيث البيوت الجديدة"},
            {"role":"user","content":f"ابدأ بـ{item['n']}، شكد؟"},
            {"role":"assistant","content":f"{item['n']} بـ{vp(item['p'])} دينار. {item['f']}"},
            {"role":"user","content":"زين، أريد أشوف الكتالوج كامل"},
            {"role":"assistant","content":"تفضل، الكتالوج كامل وفيه كل الغرف"},
        ]

    return {"id":f"furn_{i:04d}","category":"sales_furniture","dialect":"iraqi_arabic","messages":msgs}

# ============================================================
# FILE 7 - SERVICES (REPAIRS, ETC.)
# ============================================================

SERVICES = [
    {"n":"تصليح سيارة","f":"كراج متخصص","p":150000},
    {"n":"تركيب تكييف","f":"كهربائي معتمد","p":100000},
    {"n":"تصليح موبايل","f":"فتح شاشة ولحام","p":50000},
    {"n":"صبغ جدران","f":"عامل مهني","p":200000},
    {"n":"تصليح أنابيب","f":"سباك متخصص","p":75000},
    {"n":"تركيب كاميرات","f":"نظام مراقبة","p":500000},
    {"n":"تصليح غسالة","f":"تقنية متخصصة","p":80000},
    {"n":"تصليح ثلاجة","f":"تقنية متخصصة","p":70000},
    {"n":"قص شعر","f":"حلاق ماهر","p":10000},
    {"n":"دهان سيارة","f":"ورشة متخصصة","p":300000},
    {"n":"تصليح لابتوب","f":"فني كمبيوتر متخصص","p":60000},
    {"n":"تنظيف مكيفات","f":"تقني معتمد","p":40000},
    {"n":"تركيب باب حديد","f":"نجار متخصص","p":250000},
    {"n":"تصليح شبكة كهرباء","f":"كهربائي ماهر","p":120000},
    {"n":"تصليح شاشة تلفزيون","f":"فني إلكترونيات","p":90000},
    {"n":"خدمة توصيل","f":"سائق موثوق","p":15000},
    {"n":"تصميم غرافيك","f":"مصمم محترف","p":50000},
    {"n":"تصليح مضخة ماء","f":"فني متخصص","p":100000},
]

def gen_services(i):
    svc = pick(SERVICES)
    tpl = random.randint(1, 25)

    if tpl == 1:
        msgs = [
            {"role":"user","content":f"{pick(SHORT_GREET)}، أريد {svc['n']}"},
            {"role":"assistant","content":f"هلا، {svc['f']}. أگدر أساعدك. شنو المشكلة بالضبط؟"},
            {"role":"user","content":"المشكلة موجودة من يومين"},
            {"role":"assistant","content":f"ماشي، نشوف المشكلة أول وبعدين نحدد السعر. تقريباً {vp(svc['p'])} دينار"},
            {"role":"user","content":f"{pick(DISC_REQ)}"},
            {"role":"assistant","content":f"{pick(DISC_YES)}"},
            {"role":"user","content":"زين، شوكت تكدر تجي؟"},
            {"role":"assistant","content":"غداً الصبح إن شاء الله"},
        ]
    elif tpl == 2:
        msgs = [
            {"role":"user","content":f"هلو، شكد تاخذ على {svc['n']}؟"},
            {"role":"assistant","content":f"حسب المشكلة، بس تقريباً بين {vp(svc['p']*0.8)} لـ{vp(svc['p']*1.2)} دينار"},
            {"role":"user","content":"يعني ما تكدر تعطيني سعر ثابت؟"},
            {"role":"assistant","content":"لازم أشوف أول. لو مشكلة بسيطة أقل، لو معقدة أكثر"},
            {"role":"user","content":"ماشي، تعال شوف"},
            {"role":"assistant","content":"تفضل بعطيك عنواني"},
        ]
    elif tpl == 3:
        msgs = [
            {"role":"user","content":f"موبايلي انكسرت شاشته، شكد التصليح؟"},
            {"role":"assistant","content":"شنو نوع الموبايل؟"},
            {"role":"user","content":"سامسونج A54"},
            {"role":"assistant","content":"شاشة سامسونج A54 بـ80 ألف دينار تقريباً، وبيد ساعتين"},
            {"role":"user","content":f"{pick(EXPENSIVE)}"},
            {"role":"assistant","content":"هذا سعر القطعة الأصل، التقليد أرخص بس ما يستاهل"},
            {"role":"user","content":"زين، أجيك"},
            {"role":"assistant","content":"حياك الله"},
        ]
    elif tpl == 4:
        msgs = [
            {"role":"user","content":"تكييفي ما يبرد، شنو المشكلة؟"},
            {"role":"assistant","content":"شكد نوعه وعمره؟"},
            {"role":"user","content":"سامسونج، من 3 سنين"},
            {"role":"assistant","content":"غالباً محتاج غاز أو في مشكلة بالكومپريسور. نجي نكشف أول"},
            {"role":"user","content":"شكد أجرة الكشف؟"},
            {"role":"assistant","content":"الكشف مجاني، بس التصليح بيكلف حسب المشكلة"},
        ]
    elif tpl == 5:
        msgs = [
            {"role":"user","content":"أريد أصبغ بيتي، شكد تاخذ؟"},
            {"role":"assistant","content":"شكد غرفة عندك؟"},
            {"role":"user","content":"3 غرف وصالة وكوريدور"},
            {"role":"assistant","content":f"تقريباً {vp(400000)} دينار شامل الصبغ والعمالة"},
            {"role":"user","content":"غالي، ما تنزل؟"},
            {"role":"assistant","content":"هذا سعر نار والله. بس لو دفعت نص مقدم أخفف شوية"},
        ]
    elif tpl == 6:
        msgs = [
            {"role":"user","content":"أريد أركب كاميرات مراقبة للبيت"},
            {"role":"assistant","content":"شكد كاميرا تريد وشنو نوع البيت؟"},
            {"role":"user","content":"4 كاميرات، بيت طابقين"},
            {"role":"assistant","content":f"4 كاميرات HD مع DVR بـ{vp(500000)} دينار، شامل التركيب"},
            {"role":"user","content":"تشتغل على الموبايل؟"},
            {"role":"assistant","content":"إي، تشوف البيت من موبايلك أي مكان"},
        ]
    elif tpl == 7:
        msgs = [
            {"role":"user","content":"عندي تسريب ماء بالحمام"},
            {"role":"assistant","content":"من وين يطلع الماء؟"},
            {"role":"user","content":"من تحت المرحاض"},
            {"role":"assistant","content":f"غالباً فلنجة الغلق. نجي نصلحها بـ{vp(40000)} دينار"},
            {"role":"user","content":"شوكت تكدر تجي؟"},
            {"role":"assistant","content":"هسه إذا تريد، أو بكره الصبح"},
        ]
    elif tpl == 8:
        msgs = [
            {"role":"user","content":"أريد أحلق شعري"},
            {"role":"assistant","content":"أهلاً، تفضل. شنو تريد؟"},
            {"role":"user","content":"قصة عصرية"},
            {"role":"assistant","content":"ماشي، اجلس"},
            {"role":"user","content":"وشكد الحلاقة؟"},
            {"role":"assistant","content":"10 ألف دينار"},
        ]
    elif tpl == 9:
        msgs = [
            {"role":"user","content":"غسالتي ما تدور، شكد التصليح؟"},
            {"role":"assistant","content":"شنو ماركتها وشنو اللي يصير بالضبط؟"},
            {"role":"user","content":"LG، تدور شوية وتوقف"},
            {"role":"assistant","content":"غالباً كربون الموتور. بـ60 ألف دينار تقريباً"},
            {"role":"user","content":"ماشي، شوكت تجي؟"},
            {"role":"assistant","content":"بعد الظهر إن شاء الله"},
        ]
    elif tpl == 10:
        msgs = [
            {"role":"user","content":f"{pick(SHORT_GREET)}، أريد {svc['n']}"},
            {"role":"assistant","content":f"هلا، تفضل. شنو المشكلة؟"},
            {"role":"user","content":"مشكلة بسيطة بس محتاجة تصليح"},
            {"role":"assistant","content":f"ماشي، نشوف. تقريباً {vp(svc['p'])} دينار"},
            {"role":"user","content":"شوكت؟"},
            {"role":"assistant","content":"غداً إن شاء الله"},
        ]
    elif tpl == 11:
        msgs = [
            {"role":"user","content":f"هلو، أريد {svc['n']} بس بسرعة"},
            {"role":"assistant","content":"ممكن. ما هو وقت المناسب لك؟"},
            {"role":"user","content":"هسه إذا ممكن"},
            {"role":"assistant","content":f"ماشي، بكم ساعة وأكون عندك. تقريباً {vp(svc['p'])} دينار"},
            {"role":"user","content":"ممتاز، عطيك عنوان"},
            {"role":"assistant","content":"تفضل"},
        ]
    elif tpl == 12:
        msgs = [
            {"role":"user","content":f"مرحبا، عندي {svc['n']} مزمن، صارله أسبوع"},
            {"role":"assistant","content":"وصفلي المشكلة بالتفصيل حتى أقدر أجهز"},
            {"role":"user","content":"الجهاز يشتغل شوية ويتوقف"},
            {"role":"assistant","content":f"غالباً مشكلة بـ{pick(['الكهرباء','الموتور','الضاغط'])}. أجي أكشف أول"},
            {"role":"user","content":"ماشي، شكد الكشف؟"},
            {"role":"assistant","content":"الكشف مجاني، السعر بعد التشخيص"},
        ]
    elif tpl == 13:
        msgs = [
            {"role":"user","content":f"هلو، عندكم ضمان على {svc['n']}؟"},
            {"role":"assistant","content":"إي، نضمن الشغل 3 أشهر. لو رجعت المشكلة نصلحها بالمجان"},
            {"role":"user","content":"زين، هذا مهم"},
            {"role":"assistant","content":f"التصليح بـ{vp(svc['p'])} دينار مع الضمان"},
            {"role":"user","content":"ماشي، متى تجي؟"},
            {"role":"assistant","content":"غداً الصبح إن شاء الله، حوالي 9"},
        ]
    elif tpl == 14:
        msgs = [
            {"role":"user","content":f"هلو، أريد {svc['n']} بس ما أعرف إذا يستاهل التصليح أو أشتري جديد"},
            {"role":"assistant","content":"قولي عمره وشنو المشكلة وأعطيك رأيي"},
            {"role":"user","content":"عمره 5 سنين والمشكلة في الموتور"},
            {"role":"assistant","content":"بعمر 5 سنين التصليح يستاهل. الموتور بـ50 ألف، الجهاز الجديد بـ300 ألف"},
            {"role":"user","content":"صح، صلح الموتور"},
            {"role":"assistant","content":"ماشي، نجي ونصلحه"},
        ]
    elif tpl == 15:
        msgs = [
            {"role":"user","content":f"مساء الخير، أريد {svc['n']} للمحل التجاري"},
            {"role":"assistant","content":"للمحلات عندنا سعر خاص للشركات"},
            {"role":"user","content":"شكد؟"},
            {"role":"assistant","content":f"{vp(int(svc['p']*0.85))} دينار مع فاتورة رسمية"},
            {"role":"user","content":"ماشي، نريد عقد صيانة سنوي"},
            {"role":"assistant","content":"ممكن، عقد السنة بـ{vp(svc['p']*10)} دينار شامل الزيارات الدورية"},
        ]
    elif tpl == 16:
        msgs = [
            {"role":"user","content":f"هلو، لابتوبي ما يشتغل، {svc['n']}؟"},
            {"role":"assistant","content":"شنو اللي يصير بالضبط؟ يفتح ولا ما يفتح؟"},
            {"role":"user","content":"يفتح بس الشاشة سوداء"},
            {"role":"assistant","content":"غالباً المشكلة بالكارد أو الرامات. أجيبه وأشوف"},
            {"role":"user","content":"شكد التصليح؟"},
            {"role":"assistant","content":"لو الكارد بـ80 ألف. لو الرامات بـ30 ألف. بعد الفحص نعرف"},
        ]
    elif tpl == 17:
        msgs = [
            {"role":"user","content":f"أريد {svc['n']} للبيت كامل"},
            {"role":"assistant","content":"شنو عدد الغرف وشنو المطلوب بالضبط؟"},
            {"role":"user","content":"4 غرف وصالة"},
            {"role":"assistant","content":f"للبيت كامل حوالي {vp(svc['p']*4)} دينار شامل المواد والعمالة"},
            {"role":"user","content":"ومدة التنفيذ؟"},
            {"role":"assistant","content":"يومين إلى 3 أيام حسب الحجم"},
        ]
    elif tpl == 18:
        msgs = [
            {"role":"user","content":f"هلو، {svc['n']} عندكم بالأقساط؟"},
            {"role":"assistant","content":"للمشاريع الكبيرة نقدر نقسط. كم يكلف مشروعك؟"},
            {"role":"user","content":"حوالي مليون دينار"},
            {"role":"assistant","content":"ماشي، نص مقدم والباقي بعد الانتهاء"},
            {"role":"user","content":"زين، متفق"},
            {"role":"assistant","content":"نرتب موعد للمعاينة أولاً"},
        ]
    elif tpl == 19:
        msgs = [
            {"role":"user","content":f"مرحبا، أريد معرفة أسعار {svc['n']} عندكم"},
            {"role":"assistant","content":f"تفضل:\n- مشكلة بسيطة: {vp(int(svc['p']*0.5))} دينار\n- متوسطة: {vp(svc['p'])} دينار\n- معقدة: {vp(int(svc['p']*1.5))} دينار"},
            {"role":"user","content":"وإذا احتاج قطع غيار؟"},
            {"role":"assistant","content":"القطع بالسعر الأصلي من السوق بدون ربح من عندنا"},
            {"role":"user","content":"عدل، شكراً"},
            {"role":"assistant","content":"أي وقت تحتاج تتصل فينا"},
        ]
    elif tpl == 20:
        msgs = [
            {"role":"user","content":f"هلو، {svc['n']} شنو الوقت المناسب؟"},
            {"role":"assistant","content":"نشتغل من 8 الصبح لـ8 المساء، 7 أيام"},
            {"role":"user","content":"حتى الجمعة؟"},
            {"role":"assistant","content":"إي، الجمعة بعد الصلاة نشتغل"},
            {"role":"user","content":"ماشي، أتصل فيكم يوم الجمعة"},
            {"role":"assistant","content":"حياك، رقمنا دايم مفتوح"},
        ]
    elif tpl == 21:
        msgs = [
            {"role":"user","content":f"هلو، تجون للمنطقة بعيدة؟ أنا بالمحمودية"},
            {"role":"assistant","content":"إي نجي. بس يكون في رسوم تنقل إضافية"},
            {"role":"user","content":"شكد الرسوم؟"},
            {"role":"assistant","content":"30 ألف دينار إضافية للمناطق خارج بغداد"},
            {"role":"user","content":"زين، ماشي"},
            {"role":"assistant","content":"ماشي، نتفق على الموعد"},
        ]
    elif tpl == 22:
        msgs = [
            {"role":"user","content":f"هلو، قبل ما تجي لـ{svc['n']}، أريد تقدير بالسعر"},
            {"role":"assistant","content":"ممكن. وصفلي المشكلة بالتفصيل وأعطيك تقدير أولي"},
            {"role":"user","content":"المشكلة صارت من أسبوع ومزمنة"},
            {"role":"assistant","content":f"تقدير أولي بين {vp(svc['p'])} و{vp(int(svc['p']*1.3))} دينار. الدقة بعد المعاينة"},
            {"role":"user","content":"معقول، تعال"},
            {"role":"assistant","content":"ماشي، نترتب موعد"},
        ]
    elif tpl == 23:
        msgs = [
            {"role":"user","content":f"مرحبا، جيت قبل من عندكم وما حليتوا المشكلة"},
            {"role":"assistant","content":"آسفين على الإزعاج. شنو المشكلة بالضبط؟"},
            {"role":"user","content":"نفس المشكلة رجعت بعد أسبوع"},
            {"role":"assistant","content":"ماشي، نجي مرة ثانية بالمجان. هذا ضمن ضماننا"},
            {"role":"user","content":"شكراً على الالتزام"},
            {"role":"assistant","content":"واجبنا، شوكت تريد نجي؟"},
        ]
    elif tpl == 24:
        msgs = [
            {"role":"user","content":f"هلو، عندكم خدمة طوارئ لـ{svc['n']}؟"},
            {"role":"assistant","content":"إي، عندنا خدمة طوارئ 24 ساعة"},
            {"role":"user","content":"سعر الطوارئ غالي؟"},
            {"role":"assistant","content":f"زيادة 30% على السعر الطبيعي. يعني {vp(int(svc['p']*1.3))} دينار"},
            {"role":"user","content":"ماشي، الوضع ما يحتمل تأخير"},
            {"role":"assistant","content":"حاضر، نجيك خلال ساعة"},
        ]
    else:
        msgs = [
            {"role":"user","content":f"هلو، أحتاج {svc['n']} اليوم"},
            {"role":"assistant","content":f"تفضل. {svc['f']}. شنو المشكلة؟"},
            {"role":"user","content":"المشكلة واضحة، متى تكدر تجي؟"},
            {"role":"assistant","content":"هسه أو بعد الظهر؟"},
            {"role":"user","content":"بعد الظهر أحسن"},
            {"role":"assistant","content":f"ماشي، بكم. السعر {vp(svc['p'])} دينار تقريباً"},
        ]

    return {"id":f"svc_{i:04d}","category":"services","dialect":"iraqi_arabic","messages":msgs}

# ============================================================
# FILE 8 - DAILY LIFE CONVERSATIONS
# ============================================================

DAILY_TOPICS = [
    "الطقس","الأكل","العمل","المدرسة","الصحة","المواصلات","الكهرباء","الماء","الأخبار","الرياضة"
]

# جمل إضافية موثقة من word.json لاستخدامها في المحادثات
_GREET_DAILY   = ["شلونك؟","شخبارك؟","شلون الأحوال؟","شكو ماكو؟","شلون الصحة؟"]
_REPLY_GOOD    = ["الحمد لله بخير","تمام التمام","بخير والحمد لله","زين الحمد لله"]
_TIME_WORDS    = ["هسه","هالأيام","من شوية","باچر","هالأسبوع","ورا شوي"]
_AGREE         = ["إي والله","أكيد","صح","عدل","إي صدك","والله صح"]
_HEALTH_WORDS  = _cat("الصحة والمرض")
_WORK_WORDS    = _cat("العمل والمهنة")
_STUDY_WORDS   = _cat("التعليم والدراسة")
_WEATHER_WORDS = _cat("الطقس")
_PLACE_WORDS   = _cat("الأماكن")
_FOOD_WORDS    = _cat("الطعام والشراب")
_TRANS_WORDS   = _cat("المواصلات")

_DAILY_FOODS  = ["دولمة","كباب","مسگوف","قيمة","باچة","تشريب","مرق دجاج","رز+مرق","بريانية","فطيرة"]
_DAILY_PLACES = ["سوق شورجة","كورنيش أبو نواس","شارع المتنبي","حديقة الزوراء","سوق العلاوي","منطقة الكرادة"]

def gen_daily(i):
    _dfood  = pick(_DAILY_FOODS)
    _dplace = pick(_DAILY_PLACES)
    _dname  = pick(_MALE_NAMES_S + _FEMALE_NAMES_S)
    tpl = random.randint(1, 40)

    if tpl == 1:
        msgs = [
            {"role":"user","content":"شلونك؟ شنو أخبارك؟"},
            {"role":"assistant","content":"الحمد لله، بخير. وأنت؟ شنو أخبارك أنت؟"},
            {"role":"user","content":"بخير والحمد لله. شنو طبخت اليوم؟"},
            {"role":"assistant","content":"طبخت مرق دجاج ورز. وأنت؟"},
            {"role":"user","content":"طبخت كباب، تعال تاكل معي"},
            {"role":"assistant","content":"الله يخليك، بس أنا اكلت. شكراً"},
        ]
    elif tpl == 2:
        msgs = [
            {"role":"user","content":"الكهرباء اليوم كلش مو زينة"},
            {"role":"assistant","content":"إي والله، من الصبح ما اجه إلا ساعتين"},
            {"role":"user","content":"مولدي عطلان وما أدري شسوي"},
            {"role":"assistant","content":"اصلحه عند أبو رياض، أحسن ميكانيكي بالحارة"},
            {"role":"user","content":"وين بيته؟"},
            {"role":"assistant","content":"على الشارع الرئيسي، بعد الجامع بمية متر"},
        ]
    elif tpl == 3:
        msgs = [
            {"role":"user","content":"طيارة الراصيد اليوم ضربت"},
            {"role":"assistant","content":"شفت! والله شغلة تكسر الخاطر"},
            {"role":"user","content":"الفريق ما لعب زين"},
            {"role":"assistant","content":"آني عارف، المدرب لازم يغير التشكيلة"},
            {"role":"user","content":"من رأيك مين أحسن لاعب؟"},
            {"role":"assistant","content":"يوسف بالمقدمة ما عليه شي، بس الدفاع مو زين"},
        ]
    elif tpl == 4:
        msgs = [
            {"role":"user","content":"ولدي رسب بالامتحان، مو عارف شسوي"},
            {"role":"assistant","content":"كلش انصدمت، شنو صار؟"},
            {"role":"user","content":"ما ذاكر زين وانشغل بالموبايل"},
            {"role":"assistant","content":"هذي مشكلة جيل هالأيام. لازم تأخذ منه الموبايل وقت المذاكرة"},
            {"role":"user","content":"صح، هذا اللي بفكر فيه"},
            {"role":"assistant","content":"وأعطيه مكافأة لو مذاكر زين، هذا يحمسه"},
        ]
    elif tpl == 5:
        msgs = [
            {"role":"user","content":"الحر هالسنة مو طبيعي"},
            {"role":"assistant","content":"إي والله، 50 درجة! شلون نعيش"},
            {"role":"user","content":"والكهرباء مو موجودة"},
            {"role":"assistant","content":"والله الحكومة لازم تحل هالمشكلة"},
            {"role":"user","content":"كل سنة نفس الكلام"},
            {"role":"assistant","content":"صح، ما أكو حل قريب للأسف"},
        ]
    elif tpl == 6:
        msgs = [
            {"role":"user","content":"وين أحسن مطعم بالمدينة؟"},
            {"role":"assistant","content":"مطعم أبو نواس على الكورنيش، أكله طازج وسعره معقول"},
            {"role":"user","content":"وين بالضبط؟"},
            {"role":"assistant","content":"على جانب الرصافة، قرب جسر الأئمة"},
            {"role":"user","content":"تعزمني معاهم اليوم؟"},
            {"role":"assistant","content":"إي ماشي، ساعة 7 المسا"},
        ]
    elif tpl == 7:
        msgs = [
            {"role":"user","content":"أريد أسافر لبيروت، شتشوف؟"},
            {"role":"assistant","content":"بيروت حلوة بس الأوضاع هناك صعبة هالأيام"},
            {"role":"user","content":"يعني ما تنصحني؟"},
            {"role":"assistant","content":"لو سفر سياحي روح على عمان أو إسطنبول أحسن"},
            {"role":"user","content":"إسطنبول فكرة زينة"},
            {"role":"assistant","content":"إسطنبول ممتازة، طعام حلو وأسعار معقولة"},
        ]
    elif tpl == 8:
        msgs = [
            {"role":"user","content":"شلون أوصل للمطار؟"},
            {"role":"assistant","content":"من وين أنت هسه؟"},
            {"role":"user","content":"من الكرادة"},
            {"role":"assistant","content":"اخذ تاكسي مباشرة، حوالي 15 ألف دينار. أو شنو تاكسي من التطبيق"},
            {"role":"user","content":"التطبيق يوصلني؟"},
            {"role":"assistant","content":"إي، كرنلجي أو زاجل، يوصلونك المطار بأمان"},
        ]
    elif tpl == 9:
        msgs = [
            {"role":"user","content":"وين أحسن دكتور للأطفال؟"},
            {"role":"assistant","content":"دكتور حسن الخفاجي بالعرصات، أفضل طفلية بالمنطقة"},
            {"role":"user","content":"عيادته وين؟"},
            {"role":"assistant","content":"بشارع 52 بالعرصات، عيادته اسمها عيادة الأطفال التخصصية"},
            {"role":"user","content":"ساعات الدوام؟"},
            {"role":"assistant","content":"من 5 لـ9 المسا، وأحياناً بالصبح"},
        ]
    elif tpl == 10:
        msgs = [
            {"role":"user","content":"الراتب ما يكفي هالأيام"},
            {"role":"assistant","content":"صدگ، كل شي غالي وصار"},
            {"role":"user","content":"أفكر أشتغل شغلة ثانية"},
            {"role":"assistant","content":"فكرة زينة. شنو اختصاصك؟"},
            {"role":"user","content":"حاسوب ومعلوماتية"},
            {"role":"assistant","content":"تدريس خصوصي أو برمجة فري لانس، يجلب فلوس زين"},
        ]
    elif tpl == 11:
        msgs = [
            {"role":"user","content":"ابني يريد يدرس طب، شنو رأيك؟"},
            {"role":"assistant","content":"الطب شاطر بس صعب وطويل. 6 سنين دراسة"},
            {"role":"user","content":"عارف، بس هو شاطر"},
            {"role":"assistant","content":"إذا هو راغب وذكي، لا تحيله. الطب مستقبله زين"},
            {"role":"user","content":"بس قبول يريد درجات عالية"},
            {"role":"assistant","content":"إي، لازم 95 فأكثر. شفله مدرس خصوصي"},
        ]
    elif tpl == 12:
        msgs = [
            {"role":"user","content":"شلون تطبخ قوزي؟"},
            {"role":"assistant","content":"القوزي يحتاج خروف كامل، أرز، بهارات، ومكسرات"},
            {"role":"user","content":"أول شي شسوي؟"},
            {"role":"assistant","content":"يشلح الخروف أول بالبهارات، بعدين يطبخ على نار هادية 3-4 ساعات"},
            {"role":"user","content":"والأرز؟"},
            {"role":"assistant","content":"الأرز يطبخ بمرق الخروف، بيطلع طعمه هواي حلو"},
        ]
    elif tpl == 13:
        msgs = [
            {"role":"user","content":"عندكم تجمعات إيش بالمنطقة؟"},
            {"role":"assistant","content":"إي، كل جمعة أكو لقاء بالمسجد"},
            {"role":"user","content":"وللشباب؟"},
            {"role":"assistant","content":"في ملعب كرة قدم، الشباب يلعبون كل يوم عصراً"},
            {"role":"user","content":"أجي معاهم؟"},
            {"role":"assistant","content":"أكيد، كلهم أهل طيبين"},
        ]
    elif tpl == 14:
        msgs = [
            {"role":"user","content":"وين أشتري بذور للحديقة؟"},
            {"role":"assistant","content":"سوق الشورجة فيه محلات بذور وزراعة"},
            {"role":"user","content":"بعيد؟"},
            {"role":"assistant","content":"وسط بغداد، بتاكل ساعة تقريباً لو من الكرادة"},
            {"role":"user","content":"ما أكو أقرب؟"},
            {"role":"assistant","content":"في محل صغير بشارع فلسطين، يبيع بذور أيضاً"},
        ]
    elif tpl == 15:
        msgs = [
            {"role":"user","content":"الماء مقطوع من ثلاثة أيام"},
            {"role":"assistant","content":"والله اتصل ببلدية المنطقة، يجي واحد يصلح"},
            {"role":"user","content":"اتصلت بس ما ردوا"},
            {"role":"assistant","content":"روح شخصياً للبلدية وقدم شكوى رسمية"},
            {"role":"user","content":"وين البلدية؟"},
            {"role":"assistant","content":"قرب دائرة المرور، اسأل عن قسم الماء والصرف"},
        ]
    elif tpl == 16:
        msgs = [
            {"role":"user","content":"أنصحني بفيلم عراقي حلو"},
            {"role":"assistant","content":"شفت فيلم حرب الخليج؟ قديم بس حلو"},
            {"role":"user","content":"إي شفته. أريد جديد"},
            {"role":"assistant","content":"في مسلسلات عراقية حلوة على اليوتيوب"},
            {"role":"user","content":"مثل شنو؟"},
            {"role":"assistant","content":"ذيب وذيب، أو خالي الروح. كوميدية وحلوة"},
        ]
    elif tpl == 17:
        msgs = [
            {"role":"user","content":"أريد أتعلم لغة إنگليزية، من وين أبدأ؟"},
            {"role":"assistant","content":"ابدأ بتطبيق Duolingo، مجاني وممتاز للمبتدئين"},
            {"role":"user","content":"وبعدين؟"},
            {"role":"assistant","content":"خذ كورس يوتيوب، فيه كثير مجاني ومفيد"},
            {"role":"user","content":"شكد وقت لازم أتعلم؟"},
            {"role":"assistant","content":"لو تذاكر يومياً ساعة، بـ6 أشهر تحكي أساسيات"},
        ]
    elif tpl == 18:
        msgs = [
            {"role":"user","content":"وين المستشفى الأقرب؟"},
            {"role":"assistant","content":"مستشفى الكندي على بعد 2 كيلو من هنا"},
            {"role":"user","content":"يقبل تأمين صحي؟"},
            {"role":"assistant","content":"إي، يقبل معظم شركات التأمين"},
            {"role":"user","content":"ساعات العمل؟"},
            {"role":"assistant","content":"طوارئ 24 ساعة، عيادات من 8 صباح لـ4 عصراً"},
        ]
    elif tpl == 19:
        msgs = [
            {"role":"user","content":"أريد أبدل وظيفتي، شنو رأيك؟"},
            {"role":"assistant","content":"لماذا تريد تبدل؟"},
            {"role":"user","content":"راتبي قليل ومديري مو زين"},
            {"role":"assistant","content":"الراتب قابل للتفاوض، بس المدير مشكلة أكبر"},
            {"role":"user","content":"صح، مو طايگه"},
            {"role":"assistant","content":"دور على وظيفة أحسن أول، ثم اترك"},
        ]
    elif tpl == 20:
        # طقس + كلمات word.json
        w1 = pick(_WEATHER_WORDS) if _WEATHER_WORDS else "حار"
        msgs = [
            {"role":"user","content":f"شلون الجو {pick(_TIME_WORDS)}؟"},
            {"role":"assistant","content":f"والله {w1} هواي، ما أكدر أطلع برا"},
            {"role":"user","content":"إي والله، كلش صعب"},
            {"role":"assistant","content":f"{pick(_AGREE)}، هالسنة الجو مو طبيعي أبد"},
            {"role":"user","content":"الله يستر على المستقبل"},
            {"role":"assistant","content":"الله كريم، إن شاء الله يتحسن"},
        ]
    elif tpl == 21:
        # صحة + word.json
        hw = pick(_HEALTH_WORDS) if _HEALTH_WORDS else "وجع"
        msgs = [
            {"role":"user","content":f"أنا عندي {hw} من أمس"},
            {"role":"assistant","content":"سلامات! روحت للدكتور؟"},
            {"role":"user","content":"لا بعد، بفكر أروح"},
            {"role":"assistant","content":"لازم تروح، ما تهاون بصحتك"},
            {"role":"user","content":"زين، راح أروح العيادة الضهر"},
            {"role":"assistant","content":"الله يشفيك ويعافيك، تسلم"},
        ]
    elif tpl == 22:
        # عمل + word.json
        ww = pick(_WORK_WORDS) if _WORK_WORDS else "وظيفة"
        msgs = [
            {"role":"user","content":f"شخبارك؟ شلون الـ{ww}؟"},
            {"role":"assistant","content":f"الحمد لله، الـ{ww} ماشي بس تعبان هواي"},
            {"role":"user","content":"تعبان ليش؟ شصار؟"},
            {"role":"assistant","content":"الدوام طويل والضغط كثير هالأيام"},
            {"role":"user","content":"الله يعينك، الصبر مفتاح الفرج"},
            {"role":"assistant","content":"إن شاء الله، شكراً على الكلام الزين"},
        ]
    elif tpl == 23:
        # دراسة + word.json
        sw = pick(_STUDY_WORDS) if _STUDY_WORDS else "امتحان"
        msgs = [
            {"role":"user","content":f"عندي {sw} باچر وما ذاكرت كافي"},
            {"role":"assistant","content":"والله! ليش تأجلت؟"},
            {"role":"user","content":"كنت مشغول والله"},
            {"role":"assistant","content":"هسه اشتغل على أهم المواضيع وخلك مركز"},
            {"role":"user","content":"صح، يلا أروح أذاكر"},
            {"role":"assistant","content":"بالتوفيق، الله يوفقك"},
        ]
    elif tpl == 24:
        # مواصلات + word.json
        tw = pick(_TRANS_WORDS) if _TRANS_WORDS else "سيارة"
        msgs = [
            {"role":"user","content":f"الـ{tw} تعبت اليوم بالطريق"},
            {"role":"assistant","content":"شصار فيها؟"},
            {"role":"user","content":"ما أدري، فجأة وقفت"},
            {"role":"assistant","content":"روحها عند الكراج، شوفها قبل ما يكبر الموضوع"},
            {"role":"user","content":"إي ماشي، هسه أتصل بالسطحة"},
            {"role":"assistant","content":"زين، الله يسهل عليك"},
        ]
    elif tpl == 25:
        # أكل + word.json
        fw = pick(_FOOD_WORDS) if _FOOD_WORDS else "دولمة"
        msgs = [
            {"role":"user","content":f"اليوم طبخنا {fw}، تعال تاكل"},
            {"role":"assistant","content":f"والله؟ {fw}! كلش أحب هاي الأكلة"},
            {"role":"user","content":"تعال هسه، الأكل جاهز"},
            {"role":"assistant","content":"يلا، جاي. الله يخليكم"},
            {"role":"user","content":"حياك، والعيش والملح"},
            {"role":"assistant","content":"الله يبارك فيكم"},
        ]
    elif tpl == 26:
        # تقنية + شباب
        yw = pick(YOUTH_WORDS) if YOUTH_WORDS else "كفو"
        msgs = [
            {"role":"user","content":"شفت الڤيديو اللي نشرته على التيك توك؟"},
            {"role":"assistant","content":f"إي شفته! {yw} والله، كلش حلو"},
            {"role":"user","content":"شكراً، حاولت أسوي شي مختلف"},
            {"role":"assistant","content":"نجحت والله، الناس كلهم عجبهم"},
            {"role":"user","content":"يسعدك، تشجيعك يحمسني أكثر"},
            {"role":"assistant","content":"كمل، أنت على المسار الصح"},
        ]
    elif tpl == 27:
        # مشاعر + word.json
        em = pick(EMOTIONS) if EMOTIONS else "فرحان"
        msgs = [
            {"role":"user","content":f"أنا {em} هالأيام، مو عارف ليش"},
            {"role":"assistant","content":"شنو اللي صاير؟ حچيلي"},
            {"role":"user","content":"الضغط كثير، الشغل والبيت والكل يريد شي"},
            {"role":"assistant","content":"إي والله، الحياة هالأيام تعبانة. لازم تاخذ وقت لروحك"},
            {"role":"user","content":"صح، ما أخذت إجازة من زمان"},
            {"role":"assistant","content":"خذ إجازة حتى لو يوم وحد، ارتاح. الله يوفقك"},
        ]
    elif tpl == 28:
        msgs = [
            {"role":"user","content":f"{pick(_GREET_DAILY)}"},
            {"role":"assistant","content":f"{pick(_REPLY_GOOD)}. وأنت؟"},
            {"role":"user","content":"بخير والحمد لله. شنو أخبارك؟"},
            {"role":"assistant","content":"الحمد لله، ماكو شي جديد"},
            {"role":"user","content":"الله يحفظك"},
            {"role":"assistant","content":"الله يخليك، حياك الله"},
        ]
    elif tpl == 29:
        msgs = [
            {"role":"user","content":"شلونك؟ شنو طبخت اليوم؟"},
            {"role":"assistant","content":f"طبخت {pick(['دولمة','قيمة','تشريب','كباب','مسگوف','باچة'])}. وأنت؟"},
            {"role":"user","content":"أنا طبخت مرق دجاج"},
            {"role":"assistant","content":"حلو، مرق الدجاج يفتح الشهية"},
            {"role":"user","content":"هههه تعال تاكل معي"},
            {"role":"assistant","content":"بالمجان والله! شكد الساعة؟"},
        ]
    elif tpl == 30:
        msgs = [
            {"role":"user","content":"وين كنت؟ أتصلت فيك ما ردّيت"},
            {"role":"assistant","content":"آسف، كنت بالسوق وما سمعت"},
            {"role":"user","content":"لا تهم، بس كنت أبيك تجي معي على الدكتور"},
            {"role":"assistant","content":"شنو الموضوع؟ كلشي بخير؟"},
            {"role":"user","content":"إي، بس تعب بسيط"},
            {"role":"assistant","content":"الله يعافيك، لازم تفحص. أجيك"},
        ]
    elif tpl == 31:
        weather = pick(["حارة هواي","بردانة","شتوية","غيوم","ربيعية"])
        msgs = [
            {"role":"user","content":f"الجو اليوم {weather}"},
            {"role":"assistant","content":f"إي والله، الجو {weather} هالأيام كلش"},
            {"role":"user","content":"ما تحب هذا الجو؟"},
            {"role":"assistant","content":"أفضل الجو المعتدل. حار ولا بارد كلاهم صعب"},
            {"role":"user","content":"ذوقك صح"},
            {"role":"assistant","content":"هههه، الجو الربيعي أحسن شي"},
        ]
    elif tpl == 32:
        msgs = [
            {"role":"user","content":"شتسوي هالعطلة؟"},
            {"role":"assistant","content":"أفكر أروح للعائلة بالموصل. وأنت؟"},
            {"role":"user","content":"أنا ناوي أرتاح بالبيت"},
            {"role":"assistant","content":"راحة البيت ما تعوضها شي"},
            {"role":"user","content":"إي، أحياناً البيت أحسن سفرة"},
            {"role":"assistant","content":"صح والله، خصوصاً لو عندك شغل متراكم"},
        ]
    elif tpl == 33:
        msgs = [
            {"role":"user","content":"شفت المباراة امبارح؟"},
            {"role":"assistant","content":"إي شفتها! أحلى مباراة شفتها من زمان"},
            {"role":"user","content":"الهدف الثالث كان روعة"},
            {"role":"assistant","content":"والله، الحارس ما أكو ما يعمله شي"},
            {"role":"user","content":"المنتخب هالمرة زين"},
            {"role":"assistant","content":"إي ربي يوفقهم، ونأمل نتأهل"},
        ]
    elif tpl == 34:
        msgs = [
            {"role":"user","content":"الأسعار هالأيام مو طبيعية"},
            {"role":"assistant","content":"إي والله، كل شي صعد"},
            {"role":"user","content":"كيلو الطماطة وصل 5000"},
            {"role":"assistant","content":"مو معقول، قبل شهر كان بـ2000"},
            {"role":"user","content":"مو عارف شسوي"},
            {"role":"assistant","content":"الله يفرجها، الوضع صعب على الكل"},
        ]
    elif tpl == 35:
        msgs = [
            {"role":"user","content":"عندي مقابلة عمل بكره، ادعيلي"},
            {"role":"assistant","content":"الله يوفقك إن شاء الله! وين المقابلة؟"},
            {"role":"user","content":"شركة برمجيات بالمنصور"},
            {"role":"assistant","content":"إن شاء الله يقبلونك. استعد زين واروح بثياب رسمية"},
            {"role":"user","content":"شكراً على النصيحة"},
            {"role":"assistant","content":"ربي يفتحها عليك. نروح نحتفل لما تقبل"},
        ]
    elif tpl == 36:
        msgs = [
            {"role":"user","content":"الدوام هالأيام مرهق والله"},
            {"role":"assistant","content":"شنو يصير؟ ضغط شغل؟"},
            {"role":"user","content":"إي، المشاريع كثرت والوقت ما يكفي"},
            {"role":"assistant","content":"حاول تنظم وقتك، حدد أهمية كل شغلة"},
            {"role":"user","content":"صح، بس صعب"},
            {"role":"assistant","content":"ثلاث أشياء بالأولوية كل يوم، مو أكثر"},
        ]
    elif tpl == 37:
        msgs = [
            {"role":"user","content":"ابني يريد آيفون وأنا ما عندي ميزانية"},
            {"role":"assistant","content":"كم عمره؟"},
            {"role":"user","content":"14 سنة"},
            {"role":"assistant","content":"ما يحتاج آيفون بعمره. اشتريه موبايل بسعر معقول"},
            {"role":"user","content":"بس الأولاد كلهم عندهم"},
            {"role":"assistant","content":"فهمه إن القيمة مو بالماركة. ياه علمه إدارة الفلوس"},
        ]
    elif tpl == 38:
        msgs = [
            {"role":"user","content":"أريد أتعلم قيادة سيارة، من أين أبدأ؟"},
            {"role":"assistant","content":"ابدأ بمدرسة سياقة معتمدة. تعلم النظري أول"},
            {"role":"user","content":"المدة شكد؟"},
            {"role":"assistant","content":"شهر تقريباً للمبتدئين"},
            {"role":"user","content":"والرخصة؟"},
            {"role":"assistant","content":"بعد اجتياز الاختبار تروح لمديرية المرور وتسوي رخصتك"},
        ]
    elif tpl == 39:
        msgs = [
            {"role":"user","content":"أريد أتعلم لغة إنجليزية، شنو تنصحني؟"},
            {"role":"assistant","content":"ابدأ بتطبيق دوولينگو يومياً، وشوف أفلام إنجليزية"},
            {"role":"user","content":"مدرسة أحسن؟"},
            {"role":"assistant","content":"لو عندك وقت، المدرسة أسرع. بس الأهم الممارسة اليومية"},
            {"role":"user","content":"شكراً، أبدأ هالأسبوع"},
            {"role":"assistant","content":"الله يوفقك، اللغة تفتح آفاق"},
        ]
    else:
        msgs = [
            {"role":"user","content":"شلونك أخوي؟ ما شفناك من زمان"},
            {"role":"assistant","content":"بخير والحمد لله، مشغول بالشغل"},
            {"role":"user","content":"اللي يشغل يبارك فيه"},
            {"role":"assistant","content":"هههه، صح. وأنت شنو أخبارك؟"},
            {"role":"user","content":"كلشي تمام الحمد لله"},
            {"role":"assistant","content":"الحمد لله، ربي يديم النعمة"},
        ]

    return {"id":f"daily_{i:04d}","category":"daily_life","dialect":"iraqi_arabic","messages":msgs}

# ============================================================
# FILE 9 - SOCIAL & FAMILY CONVERSATIONS
# ============================================================

_FAMILY_WORDS = _cat("العلاقات والعائلة")
_SYMPATHY_W   = _cat("التعاطف والمواساة")
_PROBLEM_W    = _cat("المشاكل والشكاوى")
_RELIGION_W   = _cat("الدين والمناسبات")

_IRAQI_CITIES   = ["الموصل","البصرة","النجف","كربلاء","الكوت","الديوانية","السماوة","عمارة","الرمادي","تكريت","الحلة","كركوك"]
_MALE_NAMES_S   = ["علي","حسين","محمد","أحمد","عمر","جعفر","كرار","رعد","مصطفى","ليث","صادق","فراس"]
_FEMALE_NAMES_S = ["فاطمة","زينب","نور","رهام","سارة","ريم","مروة","ياسمين","شيماء","بشرى"]
_JOBS_S         = ["مهندس","دكتور","معلم","محاسب","مبرمج","تاجر","ضابط","طبيب","محامي","مدير"]
_FOODS_S        = ["دولمة","مسگوف","قوزي","كباب","مندي","باچة","تشريب","بريانية","قيمة","برياني"]

def gen_social(i):
    _city  = pick(_IRAQI_CITIES)
    _mname = pick(_MALE_NAMES_S)
    _fname = pick(_FEMALE_NAMES_S)
    _job   = pick(_JOBS_S)
    _food  = pick(_FOODS_S)
    tpl = random.randint(1, 60)

    if tpl == 1:
        msgs = [
            {"role":"user","content":"إيش تفتكر بموضوع الزواج المبكر؟"},
            {"role":"assistant","content":"زواج المبكر مشكلة كبيرة، الشاب لازم يكمل دراسته أول"},
            {"role":"user","content":"بس الأهل يضغطون"},
            {"role":"assistant","content":"لازم تفهمهم إن الزواج يحتاج نضج وإمكانيات"},
            {"role":"user","content":"وإذا الأهل ما يفهمون؟"},
            {"role":"assistant","content":"اطلب وساطة شخص يحترمونه يشرح لهم"},
        ]
    elif tpl == 2:
        msgs = [
            {"role":"user","content":"أمي مريضة ومحتاجة عملية"},
            {"role":"assistant","content":"الله يشفيها، شنو العملية؟"},
            {"role":"user","content":"عملية قلب مفتوح"},
            {"role":"assistant","content":"خذها لمستشفى ابن البيطار أو الصدر، أحسن مستشفيات قلب"},
            {"role":"user","content":"غالية هالعمليات؟"},
            {"role":"assistant","content":"في حكومي مجاني بس الانتظار طويل، وخصوصي بـ5-10 مليون دينار"},
        ]
    elif tpl == 3:
        msgs = [
            {"role":"user","content":"أخي يريد يسافر للخارج للشغل"},
            {"role":"assistant","content":"وين يريد يروح؟"},
            {"role":"user","content":"ألمانيا أو كندا"},
            {"role":"assistant","content":"كندا أسهل من ناحية الإقامة والهجرة"},
            {"role":"user","content":"بس بعيدة"},
            {"role":"assistant","content":"الغربة صعبة، بس لو الفرصة زينة يستاهل"},
        ]
    elif tpl == 4:
        msgs = [
            {"role":"user","content":"عزيمة عندي بكره، شنو أطبخ؟"},
            {"role":"assistant","content":"شكد نفر؟"},
            {"role":"user","content":"عشرة أشخاص"},
            {"role":"assistant","content":"طبخي قوزي أو دولمة، أكلة عراقية أصيلة للضيوف"},
            {"role":"user","content":"الدولمة صعبة؟"},
            {"role":"assistant","content":"تحتاج صبر بس ما تحتاج خبرة كبيرة"},
        ]
    elif tpl == 5:
        msgs = [
            {"role":"user","content":"ابنتي تبي تدرس برا البلد"},
            {"role":"assistant","content":"يا بلد تبي تروح؟"},
            {"role":"user","content":"تركيا أو ماليزيا"},
            {"role":"assistant","content":"ماليزيا أرخص وجامعاتها معترف فيها دولياً"},
            {"role":"user","content":"أمانة على بناتنا؟"},
            {"role":"assistant","content":"إذا بنت مؤدبة ومسؤولة ما في مشكلة، الدراسة شيء مهم"},
        ]
    elif tpl == 6:
        msgs = [
            {"role":"user","content":"جاري يزعجني هواي"},
            {"role":"assistant","content":"شنو يسوي؟"},
            {"role":"user","content":"يرفع الموسيقى بالليل ويحرك السيارة قدام بيتي"},
            {"role":"assistant","content":"كلمه بهدوء أول، لو ما أثر اشكه للبلدية"},
            {"role":"user","content":"خايف يتعصب"},
            {"role":"assistant","content":"كلمه بلطف وبالنهار، ومعظم الناس يفهمون"},
        ]
    elif tpl == 7:
        msgs = [
            {"role":"user","content":"أريد أصالح أخوي بعد خلاف"},
            {"role":"assistant","content":"شنو صار بينكم؟"},
            {"role":"user","content":"خلاف على إرث"},
            {"role":"assistant","content":"مشاكل الإرث صعبة، احسن تجيب وسيط من الأهل يحل"},
            {"role":"user","content":"وإذا ما يقبل الوساطة؟"},
            {"role":"assistant","content":"الصبر والدعاء، والتواصل يجلب نتيجة في النهاية"},
        ]
    elif tpl == 8:
        msgs = [
            {"role":"user","content":"ولدي يبكي هواي، ما أدري شسوي"},
            {"role":"assistant","content":"عمره شكد؟"},
            {"role":"user","content":"سنتين"},
            {"role":"assistant","content":"في هالعمر طبيعي، ممكن أسنان أو مغص أو يريد انتباه"},
            {"role":"user","content":"شلون أعرف؟"},
            {"role":"assistant","content":"شوف إذا حرارة، وإذا ما أكو حرارة شيله ولعب معه"},
        ]
    elif tpl == 9:
        msgs = [
            {"role":"user","content":"زوجتي ومي ما يتفاهمون"},
            {"role":"assistant","content":"هذي مشكلة شايعة، لازم تكون وسيط"},
            {"role":"user","content":"كيف؟"},
            {"role":"assistant","content":"ما تحكي لواحدة عن الثانية، وكون عادل بالوقت"},
            {"role":"user","content":"بس أمي دايماً تتدخل"},
            {"role":"assistant","content":"بهدوء وباحترام، فهمها إن الزوجة تحتاج خصوصية"},
        ]
    elif tpl == 10:
        msgs = [
            {"role":"user","content":"خطيبتي تريد خاتم غالي، ما أكدر"},
            {"role":"assistant","content":"كلمها بصراحة عن إمكانياتك"},
            {"role":"user","content":"أخاف ما يعجبك"},
            {"role":"assistant","content":"اللي تحبك تفهمك. الخاتم البسيط أحلى من الدين"},
            {"role":"user","content":"صح، بكلمها"},
            {"role":"assistant","content":"توفيق إن شاء الله"},
        ]
    elif tpl == 11:
        msgs = [
            {"role":"user","content":"عيد الأم جاي، شنو هدية أشتري لأمي؟"},
            {"role":"assistant","content":"أحسن هدية وقتك معها. بس لو تبي شي مادي، عطرها المفضل"},
            {"role":"user","content":"وشنو هدية من الأولاد الصغار؟"},
            {"role":"assistant","content":"رسمة مرسومة باليد أو كارت مكتوب فيه كلمة حلوة أغلى من أي هدية"},
            {"role":"user","content":"فكرة حلوة والله"},
            {"role":"assistant","content":"الأمهات يحبون من القلب أكثر من المادة"},
        ]
    elif tpl == 12:
        msgs = [
            {"role":"user","content":"شنو رأيك بالعمل من البيت؟"},
            {"role":"assistant","content":"له مزايا وعيوب. راحة أكثر بس تحتاج انضباط"},
            {"role":"user","content":"أنا ما أكدر أركز بالبيت"},
            {"role":"assistant","content":"حدد وقت ومكان للشغل، وأطفئ الإشعارات خلال الشغل"},
            {"role":"user","content":"وإذا الأطفال يزعجون؟"},
            {"role":"assistant","content":"اشتغل بعد ما يناموا أو اتفق مع زوجتك على وقت هادي"},
        ]
    elif tpl == 13:
        msgs = [
            {"role":"user","content":"أريد أخسر وزن، شنو أسوي؟"},
            {"role":"assistant","content":"أول شي قلل السكر والكربوهيدرات"},
            {"role":"user","content":"والرياضة؟"},
            {"role":"assistant","content":"مشي 30 دقيقة يوميا كافي للبداية"},
            {"role":"user","content":"وشنو آكل؟"},
            {"role":"assistant","content":"خضار وبروتين. قلل الأرز والخبز الأبيض"},
        ]
    elif tpl == 14:
        msgs = [
            {"role":"user","content":"أبي مريض والدكتور يريد يدخله مستشفى"},
            {"role":"assistant","content":"الله يشفيه. شنو عنده؟"},
            {"role":"user","content":"ضغط وسكر مرتفع"},
            {"role":"assistant","content":"هذا يحتاج متابعة مكثفة، التنويم ضروري"},
            {"role":"user","content":"خايف عليه"},
            {"role":"assistant","content":"الله يحفظه، الدكاترة يعرفون الأحسن. توكل على الله"},
        ]
    elif tpl == 15:
        msgs = [
            {"role":"user","content":"عندي امتحان بكره وما ذاكرت"},
            {"role":"assistant","content":"وين الامتحان وشنو المادة؟"},
            {"role":"user","content":"رياضيات جامعة"},
            {"role":"assistant","content":"ذاكر الأسئلة المتكررة وأهم المواضيع أول"},
            {"role":"user","content":"ما عندي وقت أخلص الكل"},
            {"role":"assistant","content":"ركز على 70% من المنهج اللي يطلع أكثر"},
        ]
    elif tpl == 16:
        msgs = [
            {"role":"user","content":"بيتنا صغير وعائلتي كبيرة"},
            {"role":"assistant","content":"شكد شخص؟"},
            {"role":"user","content":"ثمانية أشخاص ببيت غرفتين"},
            {"role":"assistant","content":"هذا صعب. تفكر تأجر بيت أكبر؟"},
            {"role":"user","content":"الإيجار غالي"},
            {"role":"assistant","content":"دور في أطراف المدينة، أرخص بكثير"},
        ]
    elif tpl == 17:
        msgs = [
            {"role":"user","content":"وين أشتري هدايا العيد؟"},
            {"role":"assistant","content":"سوق العلاوي فيه كل شي وأسعاره معقولة"},
            {"role":"user","content":"ما أريد أروح سوق، تعبان"},
            {"role":"assistant","content":"اطلب أونلاين من تطبيق فاست ديليفري"},
            {"role":"user","content":"أمين هذي التطبيقات؟"},
            {"role":"assistant","content":"إي، فيه تقييمات وكثير ناس يستخدمونها"},
        ]
    elif tpl == 18:
        msgs = [
            {"role":"user","content":"ابني يلعب بالجيمز كثير هواي"},
            {"role":"assistant","content":"شكد وقت يومياً يلعب؟"},
            {"role":"user","content":"من 6 لـ8 ساعات"},
            {"role":"assistant","content":"هذا كثير هواي، يأثر على دراسته وصحته"},
            {"role":"user","content":"شلون أوقفه؟"},
            {"role":"assistant","content":"حدد له وقت محدد، مثلاً ساعتين بعد الدراسة فقط"},
        ]
    elif tpl == 19:
        msgs = [
            {"role":"user","content":"أريد أعزم أصدقائي على عشاء، شنو أحضر؟"},
            {"role":"assistant","content":"شكد نفر؟"},
            {"role":"user","content":"خمسة أصدقاء"},
            {"role":"assistant","content":"مسگوف على النار أحلى عشاء تكدر تعزم فيه"},
            {"role":"user","content":"صعب أسويه بالبيت؟"},
            {"role":"assistant","content":"تشتريه جاهز من أبو نواس، أو تطلب كاترينگ"},
        ]
    elif tpl == 20:
        # مناسبة دينية
        rw = pick(_RELIGION_W) if _RELIGION_W else "عيد مبارك"
        msgs = [
            {"role":"user","content":f"{rw}!"},
            {"role":"assistant","content":"الله يبارك فيك، كل عام وأنت بخير"},
            {"role":"user","content":"الله يخليك، شلون العيد وياكم؟"},
            {"role":"assistant","content":"الحمد لله، اجتمعنا بالعيلة وانبسطنا هواي"},
            {"role":"user","content":"هاي أحلى شي بالعيد"},
            {"role":"assistant","content":"إي والله، الاجتماع بالأهل لا يعوضه شي"},
        ]
    elif tpl == 21:
        # تعاطف + word.json
        sp = pick(_SYMPATHY_W) if _SYMPATHY_W else "الله يوفقك"
        msgs = [
            {"role":"user","content":"صاحبي توفي الليلة الماضية"},
            {"role":"assistant","content":"إنا لله وإنا إليه راجعون. عظم الله أجرك"},
            {"role":"user","content":"والله صدمت، ما صدگت"},
            {"role":"assistant","content":f"{sp}، الله يرحمه ويغفر له"},
            {"role":"user","content":"آمين. كان إنسان طيب والله"},
            {"role":"assistant","content":"الله يرحمه، ويصبر أهله"},
        ]
    elif tpl == 22:
        # علاقات عائلة + word.json
        fw = pick(_FAMILY_WORDS) if _FAMILY_WORDS else "أخوية"
        msgs = [
            {"role":"user","content":f"يا {fw}، تعال نتغدى سوا"},
            {"role":"assistant","content":"حاضر، وين؟"},
            {"role":"user","content":"البيت، أمي طبخت دولمة"},
            {"role":"assistant","content":"والله؟ دولمة أمك؟ جاي هسه هسه!"},
            {"role":"user","content":"هههه، يلا استعجل"},
            {"role":"assistant","content":"بالطريق، ثانيتين"},
        ]
    elif tpl == 23:
        # مشكلة + word.json
        pw = pick(_PROBLEM_W) if _PROBLEM_W else "مشكلة"
        msgs = [
            {"role":"user","content":f"عندي {pw} مع جاري"},
            {"role":"assistant","content":"شنو صار بينكم؟"},
            {"role":"user","content":"يرفع الصوت بالليل ويزعجنا"},
            {"role":"assistant","content":"كلمه بهدوء أول، لو ما سمع اشكه للبلدية"},
            {"role":"user","content":"خايف يزعل"},
            {"role":"assistant","content":"أحسن تحل بالكلام الطيب، معظم الناس يفهمون"},
        ]
    elif tpl == 24:
        # مدح + word.json
        pr = pick(PRAISE) if PRAISE else "كفو"
        msgs = [
            {"role":"user","content":"ولدي اليوم نجح بالامتحان بدرجة عالية"},
            {"role":"assistant","content":f"{pr}! الله يبارك فيه"},
            {"role":"user","content":"إي والله، فرحنا هواي"},
            {"role":"assistant","content":"يستاهل، هذا ثمرة تعبه ومذاكرته"},
            {"role":"user","content":"الحمد لله، ربي يكمل عليه"},
            {"role":"assistant","content":"إن شاء الله دايماً يفرحكم"},
        ]
    elif tpl == 25:
        msgs = [
            {"role":"user","content":"شلون حال أم محمد؟"},
            {"role":"assistant","content":"بخير الحمد لله، وين أنت؟ ما شفناك"},
            {"role":"user","content":"كنت مسافر"},
            {"role":"assistant","content":"أهلاً وسهلاً برجوعك، الله يسلمك"},
            {"role":"user","content":"الله يخليك"},
            {"role":"assistant","content":"تفضل اشرب چاي معنا"},
        ]
    elif tpl == 26:
        msgs = [
            {"role":"user","content":"أخوي يبي يشوف منجمة، تنصحه؟"},
            {"role":"assistant","content":"المنجمة وشكوى القدر مو صح دينياً. أنصحه يتوكل على الله"},
            {"role":"user","content":"بس يحب يعرف مستقبله"},
            {"role":"assistant","content":"المستقبل بيد الله. والإنسان بجهده يصنع مستقبله"},
            {"role":"user","content":"صح، شكراً على التوضيح"},
            {"role":"assistant","content":"ربي يهديه ويوفقه"},
        ]
    elif tpl == 27:
        msgs = [
            {"role":"user","content":"عندي مشكلة مع زميلي بالشغل"},
            {"role":"assistant","content":"شنو صار بينكم؟"},
            {"role":"user","content":"أخذ كريدتي قدام المدير"},
            {"role":"assistant","content":"هذا شي مو صح. لازم تكلمه أول بأول"},
            {"role":"user","content":"وإذا ما نفع؟"},
            {"role":"assistant","content":"راجع المدير بهدوء واشرح الموضوع بالأدلة"},
        ]
    elif tpl == 28:
        msgs = [
            {"role":"user","content":"أهلي يريدون أرجع أسكن وياهم بعد الزواج"},
            {"role":"assistant","content":"وأنت إيش تريد؟"},
            {"role":"user","content":"أريد استقلالية بس ما أريد أجرح مشاعرهم"},
            {"role":"assistant","content":"شرحلهم بلطف إنك تحتاج خصوصية بس ستبقى قريب منهم"},
            {"role":"user","content":"صعب"},
            {"role":"assistant","content":"مو صعب لو جاء بالكلام الطيب والاحترام"},
        ]
    elif tpl == 29:
        msgs = [
            {"role":"user","content":"عندي صديقة تعبانة نفسياً، كيف أساعدها؟"},
            {"role":"assistant","content":"أول شي، اسمعيها بدون ما تحكمين عليها"},
            {"role":"user","content":"وإذا كانت بحالة صعبة؟"},
            {"role":"assistant","content":"حثيها تزور طبيب نفسي. الصحة النفسية مهمة"},
            {"role":"user","content":"خايفة تزعل"},
            {"role":"assistant","content":"قوليها إنك تحبيها وتريدين ليها الأفضل"},
        ]
    elif tpl == 30:
        msgs = [
            {"role":"user","content":"أريد أنقل للبصرة للشغل، شنو رأيك؟"},
            {"role":"assistant","content":"البصرة فيها فرص شغل زينة خصوصاً بقطاع النفط"},
            {"role":"user","content":"بس بعيدة عن أهلي"},
            {"role":"assistant","content":"الغربة صعبة بالأول، بس الإنسان يتأقلم"},
            {"role":"user","content":"وإيجارات البيوت؟"},
            {"role":"assistant","content":"معقولة أكثر من بغداد، وفيه أحياء هادية"},
        ]
    elif tpl == 31:
        msgs = [
            {"role":"user","content":"صديقي ما يصلي وأنا خايف عليه"},
            {"role":"assistant","content":"أنصحه بالكلام اللطيف والقدوة الحسنة"},
            {"role":"user","content":"وإذا ما قبل؟"},
            {"role":"assistant","content":"ادعيله وخليك قدوة. ما تكدر تجبر أحد على شي"},
            {"role":"user","content":"صح، الدعاء أقوى شي"},
            {"role":"assistant","content":"إي والله، الله يهدينا ويهديه"},
        ]
    elif tpl == 32:
        msgs = [
            {"role":"user","content":"أريد أعزم أهل زوجتي للعشاء، أول مرة"},
            {"role":"assistant","content":"هذي مناسبة زينة! طبخ الأم دايماً أحسن انطباع"},
            {"role":"user","content":"شنو أطبخ؟"},
            {"role":"assistant","content":"قوزي أو مندي، أكلات للضيوف ومقبولة"},
            {"role":"user","content":"وإذا ما تطلع كويسة؟"},
            {"role":"assistant","content":"اطلب من مطعم زين وقدمه. ما أحد يلاحظ"},
        ]
    elif tpl == 33:
        msgs = [
            {"role":"user","content":"عندي دين مال على صاحب وما يرده"},
            {"role":"assistant","content":"شكد المبلغ؟"},
            {"role":"user","content":"مليون دينار، من سنة"},
            {"role":"assistant","content":"كلمه مباشرة وذكره، وإذا ما نفع استعمل وساطة"},
            {"role":"user","content":"خايف تنكسر العلاقة"},
            {"role":"assistant","content":"حقك مهم. العلاقة الحقيقية تتحمل المطالبة بالحق"},
        ]
    elif tpl == 34:
        msgs = [
            {"role":"user","content":"ولدي الكبير صار عنده مشكلة بالدراسة"},
            {"role":"assistant","content":"شنو صاير؟"},
            {"role":"user","content":"ما يركز ودرجاته نزلت"},
            {"role":"assistant","content":"ابحث عن السبب: مشكلة مع الأصحاب؟ ضغط؟ مادة صعبة؟"},
            {"role":"user","content":"ما أدري"},
            {"role":"assistant","content":"كلمه بهدوء وبدون إدانة، واسمعه"},
        ]
    elif tpl == 35:
        msgs = [
            {"role":"user","content":"أختي أخذت موعد زواجها بس أنا قلقانة عليها"},
            {"role":"assistant","content":"ليش قلقانة؟"},
            {"role":"user","content":"الشاب ما أعرفه كثير"},
            {"role":"assistant","content":"العيلة مسؤولة تسأل وتتحرى. لا تتسرعون"},
            {"role":"user","content":"صح، أكلم أهلي"},
            {"role":"assistant","content":"إي، الاطمئنان مهم قبل الخطوة الكبيرة"},
        ]
    elif tpl == 36:
        msgs = [
            {"role":"user","content":"أريد أبدأ مشروع صغير، تنصحني بشي؟"},
            {"role":"assistant","content":"شنو مجالك وشنو عندك من خبرة؟"},
            {"role":"user","content":"أطبخ زين وكل الناس تمدحني"},
            {"role":"assistant","content":"إذن ابدأ بمطبخ بيتي أو باعة أكل. الطلب عليه كثير"},
            {"role":"user","content":"وين أبدأ؟"},
            {"role":"assistant","content":"من الواتساب والإنستغرام، رحل صورة ووصفة يومياً"},
        ]
    elif tpl == 37:
        msgs = [
            {"role":"user","content":"أحس إن أهلي ما يفهمون جيلنا"},
            {"role":"assistant","content":"هذا حاصل مع كثير. الفجوة بين الأجيال طبيعية"},
            {"role":"user","content":"بس يصعبون كل شي"},
            {"role":"assistant","content":"حاول تفهم منطقهم أول. هم خايفين عليك، مو ضدك"},
            {"role":"user","content":"شنو أسوي؟"},
            {"role":"assistant","content":"تكلمهم بهدوء واشرحلهم وجهة نظرك بالدليل"},
        ]
    elif tpl == 38:
        msgs = [
            {"role":"user","content":"صاحبي يبي يسافر للخارج ويتركنا"},
            {"role":"assistant","content":"مو بده تروح، بده يحسن حياته"},
            {"role":"user","content":"صح بس الصداقة تنقطع"},
            {"role":"assistant","content":"الصداقة الحقيقية تبقى حتى عن بعد، والتواصل هالأيام سهل"},
            {"role":"user","content":"صح والله، تفاءلت"},
            {"role":"assistant","content":"الله يوفقه ويوفقكم"},
        ]
    elif tpl == 39:
        msgs = [
            {"role":"user","content":"أريد أتصالح مع قريب بيني وبينه خلاف من سنين"},
            {"role":"assistant","content":"قرار زين! صلة الرحم واجبة"},
            {"role":"user","content":"بس من يبدأ؟"},
            {"role":"assistant","content":"الأفضل أنت تبدأ، صاحب المبادرة له الأجر"},
            {"role":"user","content":"يمكن يرفض"},
            {"role":"assistant","content":"مسؤوليتك تمد يدك. رده حساب بينه وبين الله"},
        ]
    elif tpl == 40:
        msgs = [
            {"role":"user","content":"شلونكم كلكم؟ العيلة بخير؟"},
            {"role":"assistant","content":"الحمد لله كلنا بخير. وأنتم؟"},
            {"role":"user","content":"كلنا تمام الحمد لله"},
            {"role":"assistant","content":"الله يديم النعمة على الجميع"},
            {"role":"user","content":"آمين، متى تجون تزورونا؟"},
            {"role":"assistant","content":"قريب إن شاء الله، ما يأخذ وقت"},
        ]
    elif tpl == 41:
        msgs = [
            {"role":"user","content":f"أبو {_mname} روح {_city}، كيف السفر؟"},
            {"role":"assistant","content":f"إلى {_city}؟ بالسيارة أحسن، سفر الباص طويل"},
            {"role":"user","content":"شكد الطريق؟"},
            {"role":"assistant","content":f"حوالي {random.randint(2,6)} ساعات بالسيارة من بغداد"},
            {"role":"user","content":"والأمن بالطريق؟"},
            {"role":"assistant","content":"الله يسلمكم، الطريق مأمون هالأيام"},
        ]
    elif tpl == 42:
        budget = random.randint(5,25) * 100000
        msgs = [
            {"role":"user","content":f"أريد أعزم العيلة على أكل {_food}"},
            {"role":"assistant","content":f"{_food}! أكلة العراقيين الأصيلة. وين تريد؟"},
            {"role":"user","content":"مطعم أو نطبخ؟"},
            {"role":"assistant","content":f"لو عندك وقت اطبخ بالبيت أحلى، وإلا مطعم أبو نواس أحسن {_food} ببغداد"},
            {"role":"user","content":f"ميزانيتي {budget:,} دينار"},
            {"role":"assistant","content":"كافية والله، المطعم الكويس بـ200 ألف للعيلة"},
        ]
    elif tpl == 43:
        msgs = [
            {"role":"user","content":f"أم {_fname} تعبانة وما تقدر تطبخ"},
            {"role":"assistant","content":"وش صاير فيها؟ الله يعافيها"},
            {"role":"user","content":"ضغط دم وتعب عام"},
            {"role":"assistant","content":"لازم ترتاح. روحوا اطلبوا أكل أو كلوا من المطعم"},
            {"role":"user","content":"الله يشفيها"},
            {"role":"assistant","content":"إن شاء الله تقوم بالسلامة"},
        ]
    elif tpl == 44:
        msgs = [
            {"role":"user","content":f"{_mname} صاحبي يبي يفتح مشروع {_job}"},
            {"role":"assistant","content":"فكرة زينة! شنو المشروع بالضبط؟"},
            {"role":"user","content":f"مكتب {_job} مستقل"},
            {"role":"assistant","content":"يحتاج ترخيص وموقع زين وشبكة علاقات"},
            {"role":"user","content":"من وين يبدأ؟"},
            {"role":"assistant","content":"يسجل بالغرفة التجارية ويشوف متطلبات الترخيص"},
        ]
    elif tpl == 45:
        amt = random.randint(1,10) * 500000
        msgs = [
            {"role":"user","content":f"أريد أبعث {_mname} بـ{_city} فلوس"},
            {"role":"assistant","content":"كيف تبعث؟ حوالة ولا موبايل؟"},
            {"role":"user","content":f"أريد أبعث {amt:,} دينار"},
            {"role":"assistant","content":"استخدم تطبيق زين كاش أو آسيا حوالة، سريعين وأمينين"},
            {"role":"user","content":"الأجرة شكد؟"},
            {"role":"assistant","content":"تقريباً 1-2% من المبلغ"},
        ]
    elif tpl == 46:
        msgs = [
            {"role":"user","content":f"أم {_fname} تبي تزور قبر الإمام بـ{pick(['النجف','كربلاء'])}"},
            {"role":"assistant","content":"زيارة مباركة. متى تروحون؟"},
            {"role":"user","content":"ليلة الجمعة"},
            {"role":"assistant","content":"إن شاء الله ترجعون بالسلامة والقبول"},
            {"role":"user","content":"آمين، ادعيلنا"},
            {"role":"assistant","content":"الله يقبل زيارتكم ويوفقكم"},
        ]
    elif tpl == 47:
        msgs = [
            {"role":"user","content":f"ولدي نجح بالدراسة وراح يشتغل {_job}"},
            {"role":"assistant","content":"مبارك! الله يبارك فيه ويوفقه"},
            {"role":"user","content":"فرحان هواي والله"},
            {"role":"assistant","content":"يستاهل، تعب وحصل"},
            {"role":"user","content":"ربي يكمل عليه"},
            {"role":"assistant","content":"إن شاء الله دايماً يفرحكم ويكون سند لكم"},
        ]
    elif tpl == 48:
        msgs = [
            {"role":"user","content":f"أخوي يشتغل بـ{_city} وما يجي يزورنا"},
            {"role":"assistant","content":"الشغل يشغل الواحد، بس لازم يجي يزور"},
            {"role":"user","content":"من سنة ما شفناه"},
            {"role":"assistant","content":"كلمه وذكره بأهمية العيلة"},
            {"role":"user","content":"أخاف يزعل"},
            {"role":"assistant","content":"العيلة ما تزعل من بعض. كلمه بصراحة"},
        ]
    elif tpl == 49:
        msgs = [
            {"role":"user","content":f"أريد أسوي حفلة لبنتي {_fname} سابعتها"},
            {"role":"assistant","content":"مبارك! حفلة السابع زينة. شكد تنوي تعزم؟"},
            {"role":"user","content":"حوالي 50 شخص"},
            {"role":"assistant","content":"تعزم بقاعة ولا بالبيت؟"},
            {"role":"user","content":"بالبيت أحلى بس ما فيه مكان"},
            {"role":"assistant","content":"اجعلها بقاعة صغيرة، أنيق وريح باله"},
        ]
    elif tpl == 50:
        msgs = [
            {"role":"user","content":f"زميلي {_mname} ترقى ولم أترقى أنا"},
            {"role":"assistant","content":"شنو شعورك؟"},
            {"role":"user","content":"والله زعلان بس ما أريد أظهر"},
            {"role":"assistant","content":"طبيعي تحس بهذا. بس ركز على شغلك واسأل مديرك شنو ينقصك"},
            {"role":"user","content":"صح، لازم أتطور"},
            {"role":"assistant","content":"ربي يوفقك، الإصرار ينجح"},
        ]
    elif tpl == 51:
        msgs = [
            {"role":"user","content":f"أريد أتزوج من بنت من {_city}، أهلها يقبلون؟"},
            {"role":"assistant","content":"الناس بـ{_city} محترمون. المهم الرجل يكون كفؤاً"},
            {"role":"user","content":"أخاف الفرق الجغرافي يكون مشكلة"},
            {"role":"assistant","content":"مو مشكلة إذا الاثنين راضيين وفاهمين"},
            {"role":"user","content":"صح، الموضوع بالتفاهم"},
            {"role":"assistant","content":"ربي يوفقك ويسهل أمورك"},
        ]
    elif tpl == 52:
        meals_num = random.randint(20, 100)
        msgs = [
            {"role":"user","content":f"عندي عرس، شنو أطبخ لـ{meals_num} شخص؟"},
            {"role":"assistant","content":f"لـ{meals_num} شخص تحتاج كميات كبيرة. {_food} خيار ممتاز للأعراس"},
            {"role":"user","content":"بقدر أطبخ بيتياً؟"},
            {"role":"assistant","content":"للأعداد الكبيرة أفضل طباخ أعراس متخصص"},
            {"role":"user","content":"شكد يكلف؟"},
            {"role":"assistant","content":f"تقريباً {random.randint(3,8)}000 دينار للشخص الواحد"},
        ]
    elif tpl == 53:
        msgs = [
            {"role":"user","content":f"أريد أختار هدية ليوم ميلاد {_fname}"},
            {"role":"assistant","content":"شكد عمرها وشنو تحب؟"},
            {"role":"user","content":f"عمرها {random.randint(15,35)} وتحب العطور"},
            {"role":"assistant","content":"عطر فاخر هدية ممتازة. روحي على محلات العطورات بالمنصور"},
            {"role":"user","content":"شكد الميزانية المناسبة؟"},
            {"role":"assistant","content":f"بين {random.randint(1,3)*50000} و{random.randint(2,5)*100000} دينار خيار زين"},
        ]
    elif tpl == 54:
        msgs = [
            {"role":"user","content":f"ابن {_mname} سلب موبايله بالشارع"},
            {"role":"assistant","content":"الله يحفظه! إيش صار بالضبط؟"},
            {"role":"user","content":"كان ماشي بالليل وجاه شخص على موتور وسلبه"},
            {"role":"assistant","content":"روحوا تبلغوا الشرطة بأسرع وقت"},
            {"role":"user","content":"وفائدة التبليغ؟"},
            {"role":"assistant","content":"أحياناً يلقوهم. والأهم توثيق الحادثة"},
        ]
    elif tpl == 55:
        msgs = [
            {"role":"user","content":"الجيران الجدد ما أعرفهم، كيف أتعرف عليهم؟"},
            {"role":"assistant","content":"روح قدمهم بنفسك، هذا أحسن ابتداء"},
            {"role":"user","content":"يمكن ما يحبون أحد يتدخل"},
            {"role":"assistant","content":"كلمهم ببساطة بالباب، بدون تطفل"},
            {"role":"user","content":"صح، أروح بكره"},
            {"role":"assistant","content":"الله يوفقك، الجار قبل الدار"},
        ]
    elif tpl == 56:
        msgs = [
            {"role":"user","content":f"أريد أكمل دراستي وعمري {random.randint(30,45)} سنة"},
            {"role":"assistant","content":"ما في عمر للتعليم، العلم في أي سن مفيد"},
            {"role":"user","content":"بس ما أقدر أنافس الشباب"},
            {"role":"assistant","content":"خبرتك تعوضك، والجامعات المسائية مناسبة للكبار"},
            {"role":"user","content":"فكرة زينة"},
            {"role":"assistant","content":"الله يوفقك، القرار الصح"},
        ]
    elif tpl == 57:
        msgs = [
            {"role":"user","content":"عندي خلاف مع أختي على ميراث"},
            {"role":"assistant","content":"الميراث موضوع حساس. شنو طبيعة الخلاف؟"},
            {"role":"user","content":"تريد أكثر من حقها الشرعي"},
            {"role":"assistant","content":"لازم ترجعون لمحكمة الأحوال الشخصية، حقوقكم محفوظة"},
            {"role":"user","content":"ما أريد نخسر بعض"},
            {"role":"assistant","content":"وساطة شخص مؤثر في العيلة قد تحل بدون محكمة"},
        ]
    elif tpl == 58:
        msgs = [
            {"role":"user","content":f"أريد أتبرع لجمعية خيرية، وين أروح بـ{_city}؟"},
            {"role":"assistant","content":"إن شاء الله تقبل. في جمعيات كثيرة، ابحث عن المعتمدة منها"},
            {"role":"user","content":"شنو أفضل نوع تبرع؟"},
            {"role":"assistant","content":"الكفالة اليتيم دايمة ومتواصلة. أو الأرامل المحتاجين"},
            {"role":"user","content":"زين، أبحث ومتصل فيك"},
            {"role":"assistant","content":"الله يبارك فيك ويضاعف أجرك"},
        ]
    elif tpl == 59:
        msgs = [
            {"role":"user","content":f"أبو {_mname} يعاني من وحدة بعد وفاة زوجته"},
            {"role":"assistant","content":"الله يرحمها ويصبره. الوحدة صعبة بعد السنين"},
            {"role":"user","content":"شنو نسوي له؟"},
            {"role":"assistant","content":"خليه يشارك بمجالس أو نشاطات اجتماعية. الزيارة المتكررة مهمة"},
            {"role":"user","content":"والتلفون؟"},
            {"role":"assistant","content":"علمه يستخدم واتساب، الفيديو كول يفرق هواي"},
        ]
    else:
        msgs = [
            {"role":"user","content":f"أهلنا بـ{_city} ما زارونا من زمان"},
            {"role":"assistant","content":"الناس مشغولين هالأيام بالحياة"},
            {"role":"user","content":"بس مشتاقين لهم"},
            {"role":"assistant","content":"اتصل فيهم وعزمهم أو زورهم أنتم"},
            {"role":"user","content":"صح، نروح نزورهم بالعطلة"},
            {"role":"assistant","content":"الله يجمعكم على خير"},
        ]

    return {"id":f"social_{i:04d}","category":"social_family","dialect":"iraqi_arabic","messages":msgs}

# ============================================================
# FILE 10 - MIXED (Sales + General)
# ============================================================

def gen_mixed(i):
    choice = random.randint(1, 6)
    if choice == 1:
        return gen_elec(i)
    elif choice == 2:
        return gen_food(i)
    elif choice == 3:
        return gen_clothes(i)
    elif choice == 4:
        return gen_daily(i)
    elif choice == 5:
        return gen_social(i)
    else:
        return gen_services(i)

# ============================================================
# GENERATOR DISPATCHER
# ============================================================

FILES_CONFIG = [
    ("iraqi_train_01_electronics.json", gen_elec, "electronics_sales"),
    ("iraqi_train_02_food.json", gen_food, "food_sales"),
    ("iraqi_train_03_clothes.json", gen_clothes, "clothes_sales"),
    ("iraqi_train_04_cars.json", gen_cars, "cars_sales"),
    ("iraqi_train_05_realestate.json", gen_realestate, "realestate_sales"),
    ("iraqi_train_06_furniture.json", gen_furniture, "furniture_sales"),
    ("iraqi_train_07_services.json", gen_services, "services"),
    ("iraqi_train_08_daily.json", gen_daily, "daily_life"),
    ("iraqi_train_09_social.json", gen_social, "social_family"),
    ("iraqi_train_10_mixed.json", gen_mixed, "mixed"),
]

def main():
    output_dir = os.path.join(os.path.dirname(__file__), "iraqi_training_data")
    os.makedirs(output_dir, exist_ok=True)

    for fname, gen_fn, category in FILES_CONFIG:
        print(f"Generating {fname} ...")
        convs = []
        for i in range(10000):
            c = gen_fn(i)
            c["id"] = f"{category}_{i+1:04d}"
            # ensure valid structure
            if "messages" in c and len(c["messages"]) >= 2:
                convs.append(c)
            else:
                convs.append({"id": c["id"], "category": category,
                               "dialect": "iraqi_arabic", "messages": [
                                   {"role":"user","content":"هلو"},
                                   {"role":"assistant","content":"هلا وغلا، كيف أساعدك؟"}
                               ]})

        path = os.path.join(output_dir, fname)
        with open(path, "w", encoding="utf-8") as f:
            json.dump(convs, f, ensure_ascii=False, indent=2)
        print(f"  -> Saved {len(convs)} conversations to {path}")

    print("\nDone! All 10 files generated.")

if __name__ == "__main__":
    main()
