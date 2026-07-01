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
HOME_WORDS  = _cat("البيت والمنزل")

# ============================================================
# سلوك بشري طبيعي وأنماط البيع المتقدمة
# ============================================================

HESITATE = [
    "والله مو عارف صراحة...", "شايف بس مو مقرر",
    "مردد هواي على الموضوع", "قاعد أفكر فيها من زمان",
    "مو واثق 100%", "الصراحة مترددين",
    "مو بس أنا، حتى أهلي مترددين", "خليني أفكر بصوت عالي",
]

EXCITED = [
    "والله هذا حلو!", "وااو ممتاز!", "لا! هذا شي ما توقعت!",
    "صح صح! هذا اللي أريد بالضبط!", "هاي هاي! كفو!",
    "جان ما أعرف هذا موجود!", "هذا يجنن والله!",
    "الله الله! ما شاء الله عليه!",
]

DISAPPOINTED = [
    "هاه... ما يصير يعني...", "آه والله، مؤسف",
    "خسارة والله...", "بس ما عندي كافي",
    "مشكلة هذي...", "آسف، ما ينفع",
    "صعبة عليا هالمرة...",
]

SCARCITY_LINES = [
    "والله هذا آخر قطعة عندنا، طلب هواي عليها",
    "هذا الموديل ما يجي ثاني بعد هالكمية",
    "اليوم صارت ثلاث زبائن يسألون عليه، ما نضمن بكره",
    "هالسعر لحد نهاية اليوم بس، بكره يرجع للسعر الأصلي",
    "عندنا قطعتين بس وعندنا حجز عليهم",
    "ما أريدك تجي بكره وتندم",
]

SOCIAL_PROOF_LINES = [
    "هذا أكثر شي يبيع عندنا، الكل يمدحه",
    "كل الزبائن اللي اخذوه راضين 100%",
    "طلبته ثلاث عائلات هالأسبوع بس",
    "أبو علي صاحبنا اخذ هذا وراح يجيب ثاني لأخوه",
    "نبيع منه أكثر من 50 قطعة بالشهر",
    "حتى أنا عندي واحد بيتي وأنا راضي عليه",
]

EMPATHY_SELL_LINES = [
    "أفهم قصدك، ولهذا أريد أساعدك تلاقي الأحسن",
    "فاهم وضعك والله، ولذيج عندي حل تمام ليك",
    "أعرف شعورك، بس تعال أريك شي يرضيك",
    "ما تحتاج تتسرع، أنا أساعدك تختار بهدوء",
    "الكيف عندك مهم، ما أريدك تاخذ شي ما يناسبك",
]

ALT_OFFER_INTROS = [
    "ماشي، بس خليني أريك شي ثاني قد يعجبك أكثر",
    "طيب، عندي فكرة ثانية ممكن أنسب",
    "لا تروح هسه! عندي بديل ما خطر على بالك",
    "صبر شوية يا أخوي، عندي شي ثاني يمكن أنسب",
    "بس قبل ما تروح، شوف هذا الموديل الثاني",
    "ماشي، بس اسمعني ثانية واحدة",
    "حجي، تعال شوف هذا قبل ما تقرر",
    "طيب طيب، عندي بديل تفكر فيه",
]

ALT_OFFER_BRIDGE = [
    "هذا أرخص وعنده نفس الميزات",
    "هذا أقوى وبسعر أقرب لميزانيتك",
    "ناس كثير يفضلون هذا على الأول",
    "هذا جديد وصل وما شافه ناس كثير بعد",
    "ضمانه أطول وخدمة ما بعد البيع أحسن",
]

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
    tpl = random.randint(1, 40)

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
    elif tpl == 25:
        msgs = [
            {"role":"user","content":f"مرحبا، أريد {p['n']} لشركتي، عندكم فاتورة رسمية؟"},
            {"role":"assistant","content":f"إي عندنا. {p['n']} بـ{vp(p['p'])} دينار مع فاتورة رسمية"},
            {"role":"user","content":"نريد 5 حبات"},
            {"role":"assistant","content":f"بالجملة الكل {vp(p['p']*5*0.9)} دينار مع خصم 10%"},
            {"role":"user","content":"ماشي، اتفقنا"},
            {"role":"assistant","content":f"{pick(CLOSE)}"},
        ]
    elif tpl == 26:
        # خيبة أمل + تعاطف + بديل
        msgs = [
            {"role":"user","content":f"{pick(DISAPPOINTED)}، جيت أشتري {p['n']} بس الفلوس ما كملت"},
            {"role":"assistant","content":f"والله ما يهم يا أخوي. {pick(EMPATHY_SELL_LINES)}. بيش عندك تقريباً؟"},
            {"role":"user","content":f"عندي حوالي {vp(int(p['p']*0.68))} دينار"},
            {"role":"assistant","content":f"ماشي، {pick(ALT_OFFER_INTROS)}. عندنا {p2['n']} بـ{vp(int(p2['p']*0.8))} دينار. {p2['f'][0]}"},
            {"role":"user","content":"هذا زين؟"},
            {"role":"assistant","content":f"إي والله، {pick(SOCIAL_PROOF_LINES)}. وعليه ضمان سنة كاملة"},
            {"role":"user","content":"يا سلام، ماخذه"},
            {"role":"assistant","content":f"{pick(CLOSE)}"},
        ]
    elif tpl == 27:
        # رفض السعر → فهم الحاجة → عرض مناسب
        msgs = [
            {"role":"user","content":f"هلو، بيش {p['n']}؟"},
            {"role":"assistant","content":f"{vp(p['p'])} دينار. {p['f'][0]}"},
            {"role":"user","content":f"{pick(EXPENSIVE)}"},
            {"role":"assistant","content":"أفهمك. طيب، شنو بالضبط تحتاجه؟ للشغل ولا للترفيه؟"},
            {"role":"user","content":"للاستخدام اليومي بس، مو شي ثقيل"},
            {"role":"assistant","content":f"بهالحالة {p2['n']} أنسب لك وبسعر {vp(p2['p'])} دينار. {p2['f'][0]} وما تحتاج أكثر"},
            {"role":"user","content":"هذا يكفيني؟"},
            {"role":"assistant","content":f"إي والله، {pick(SOCIAL_PROOF_LINES)}"},
            {"role":"user","content":"ماشي، آخذه"},
            {"role":"assistant","content":f"{pick(CLOSE)}"},
        ]
    elif tpl == 28:
        # رفض → مستعمل بحالة ممتازة + ندرة
        msgs = [
            {"role":"user","content":f"أريد {p['n']} بس غالي"},
            {"role":"assistant","content":f"{pick(ALT_OFFER_INTROS)}، عندنا {p['n']} مستعمل بحالة ممتازة بـ{vp(int(p['p']*0.58))} دينار"},
            {"role":"user","content":"مستعمل؟ ما فيه مشاكل؟"},
            {"role":"assistant","content":"فحصناه عندنا وشغال زين 100%. وعليه ضمان 3 أشهر منا"},
            {"role":"user","content":f"{pick(HESITATE)}"},
            {"role":"assistant","content":f"طبيعي تتردد. بس {pick(SCARCITY_LINES)}"},
            {"role":"user","content":"زين، آخذه"},
            {"role":"assistant","content":f"{pick(CLOSE)}"},
        ]
    elif tpl == 29:
        # ثلاث محاولات: رفض → بديل → رفض → بديل ثالث → قبول
        p3 = pick(ALL_ELEC)
        while p3["n"] in [p["n"], p2["n"]]:
            p3 = pick(ALL_ELEC)
        msgs = [
            {"role":"user","content":f"هلو، أريد {p['n']}"},
            {"role":"assistant","content":f"هلا، بـ{vp(p['p'])} دينار. {p['f'][0]}"},
            {"role":"user","content":f"{pick(EXPENSIVE)}"},
            {"role":"assistant","content":f"{pick(ALT_OFFER_INTROS)}. {p2['n']} بـ{vp(p2['p'])} دينار. {p2['f'][0]}"},
            {"role":"user","content":f"هذا كمان غالي"},
            {"role":"assistant","content":f"ماشي، آخر عرض: {p3['n']} بـ{vp(p3['p'])} دينار. {p3['f'][0]}. ومعه ضمان إضافي"},
            {"role":"user","content":"هذا معقول، آخذه"},
            {"role":"assistant","content":f"{pick(CLOSE)}"},
        ]
    elif tpl == 30:
        # Bundle: شراء المنتجين بخصم
        msgs = [
            {"role":"user","content":f"أريد {p['n']}"},
            {"role":"assistant","content":f"هلا، {p['n']} بـ{vp(p['p'])} دينار. {p['f'][0]}"},
            {"role":"user","content":"زين، هاي الفلوس"},
            {"role":"assistant","content":f"قبل ما تدفع، لو تاخذ معه {p2['n']} بـ{vp(p2['p'])} دينار أعطيك خصم خاص. توفر {vp(int((p['p']+p2['p'])*0.12))} دينار"},
            {"role":"user","content":"يعني أوفر؟"},
            {"role":"assistant","content":f"إي، بدل {vp(p['p']+p2['p'])} يصير {vp(int((p['p']+p2['p'])*0.88))} بس"},
            {"role":"user","content":"والله عرض مغري، خذ الاثنين"},
            {"role":"assistant","content":f"{pick(CLOSE)}"},
        ]
    elif tpl == 31:
        # ندرة لتحفيز الشراء
        msgs = [
            {"role":"user","content":f"هلو، أشوف {p['n']}"},
            {"role":"assistant","content":f"تفضل، هاي {p['n']}. {p['f'][0]}. بـ{vp(p['p'])} دينار"},
            {"role":"user","content":f"{pick(THINK)}"},
            {"role":"assistant","content":f"بس خليني أقولك، {pick(SCARCITY_LINES)}"},
            {"role":"user","content":"يعني لازم أقرر هسه؟"},
            {"role":"assistant","content":"ما أجبرك أخوي، بس ما أريدك تجي بكره وما تلاقيه"},
            {"role":"user","content":"زين والله، آخذه"},
            {"role":"assistant","content":f"{pick(CLOSE)}"},
        ]
    elif tpl == 32:
        # إثبات اجتماعي بقصة زبون
        msgs = [
            {"role":"user","content":f"مرحبا، {p['n']} يستاهل؟"},
            {"role":"assistant","content":f"والله زبوني أبو جعفر اخذه الأسبوع الماضي وهسه جاي يجيب ثاني لأخوه. {pick(SOCIAL_PROOF_LINES)}"},
            {"role":"user","content":"يعني تعيد الشراء؟"},
            {"role":"assistant","content":f"إي، هذا دليل على جودته. {p['f'][0]} وضمان سنة"},
            {"role":"user","content":"ماشي، هذا قرار"},
            {"role":"assistant","content":f"بـ{vp(p['p'])} دينار. {pick(CLOSE)}"},
        ]
    elif tpl == 33:
        # Upsell: ارفع الزبون لمنتج أعلى
        cheap = p if p['p'] <= p2['p'] else p2
        expensive = p2 if p['p'] <= p2['p'] else p
        diff = expensive['p'] - cheap['p']
        msgs = [
            {"role":"user","content":f"أريد {cheap['n']}، بيش؟"},
            {"role":"assistant","content":f"{cheap['n']} بـ{vp(cheap['p'])} دينار. {cheap['f'][0]}"},
            {"role":"user","content":"ماشي"},
            {"role":"assistant","content":f"قبل ما تقرر، بـ{vp(diff)} دينار زيادة بس تاخذ {expensive['n']} اللي {expensive['f'][0]}. فرق بسيط وفايدته كبيرة"},
            {"role":"user","content":"فرق بسيط حقيقة؟"},
            {"role":"assistant","content":f"إي والله، و{expensive['n']} يستاهل الفرق بكثير"},
            {"role":"user","content":"صح، آخذ الأقوى"},
            {"role":"assistant","content":f"{pick(CLOSE)}"},
        ]
    elif tpl == 34:
        # بيع استشاري: البائع يسأل قبل يوصي
        msgs = [
            {"role":"user","content":f"هلو، أريد أشتري {p['n']} بس ما أعرف أختار"},
            {"role":"assistant","content":"أساعدك. أول شي، للشغل ولا شخصي؟"},
            {"role":"user","content":"شخصي، أحب الألعاب والتصوير"},
            {"role":"assistant","content":"زين. ميزانيتك حوالي شكد؟"},
            {"role":"user","content":f"حوالي {vp(p['p'])} دينار"},
            {"role":"assistant","content":f"ممتاز! بهالميزانية {p['n']} هو الخيار المثالي. {p['f'][0]} للتصوير"},
            {"role":"user","content":f"{pick(EXCITED)}"},
            {"role":"assistant","content":"وعليه ضمان سنة. تاخذه؟"},
            {"role":"user","content":"إي، هذا بالضبط اللي أريد"},
            {"role":"assistant","content":f"{pick(CLOSE)}"},
        ]
    elif tpl == 35:
        # زبون قديم + علاقة شخصية + سعر خاص
        msgs = [
            {"role":"user","content":"هلو أخوي، ما اشترينا من زمان"},
            {"role":"assistant","content":"هلا وغلا! والله مشتاقين لكم. كيف صحتك وأهلك؟"},
            {"role":"user","content":f"بخير الحمد لله. جيت أشوف {p['n']}"},
            {"role":"assistant","content":f"وصل موديل جديد! {p['n']} هالمرة أحسن من السابق. {p['f'][0]}"},
            {"role":"user","content":"وبيش؟"},
            {"role":"assistant","content":f"لأنك زبون أمين، بـ{vp(int(p['p']*0.94))} بدل {vp(p['p'])}"},
            {"role":"user","content":"الله يخليك يا أخوي، ماخذه"},
            {"role":"assistant","content":f"دايماً حياك. {pick(CLOSE)}"},
        ]
    elif tpl == 36:
        # تردد طويل + حوار ودي + قناعة تدريجية
        msgs = [
            {"role":"user","content":f"هلو... {pick(HESITATE)} على {p['n']}"},
            {"role":"assistant","content":"طبيعي تتردد، هذا قرار مهم. شنو اللي يردك بالضبط؟"},
            {"role":"user","content":f"مو واثق من {p['f'][0]}"},
            {"role":"assistant","content":f"سؤال ذكي. {p['f'][0]} يعني إنك راح تستفيد أكثر مما تتوقع"},
            {"role":"user","content":"آه فاهم الحين، يعني فايدة حقيقية؟"},
            {"role":"assistant","content":f"إي والله. وزيادة، {pick(SOCIAL_PROOF_LINES)}"},
            {"role":"user","content":f"{pick(EXCITED)}"},
            {"role":"assistant","content":f"ماشي؟ تاخذ الـ{p['n']}؟"},
            {"role":"user","content":"آخذه"},
            {"role":"assistant","content":f"{pick(CLOSE)}"},
        ]
    elif tpl == 37:
        # مفاوضة شرسة + تسوية ذكية
        final_price = int(p['p'] * 0.92)
        msgs = [
            {"role":"user","content":f"أريد {p['n']} بس أريد أفاوض"},
            {"role":"assistant","content":f"تفضل. سعره {vp(p['p'])} دينار"},
            {"role":"user","content":f"أعطيك {vp(int(p['p']*0.80))}"},
            {"role":"assistant","content":"والله ما أكدر، هذا دون رأس المال"},
            {"role":"user","content":f"ماشي {vp(int(p['p']*0.85))}؟"},
            {"role":"assistant","content":f"أخوي، أنزل لك {vp(final_price)} وهذا آخر سعر، والله يشهد"},
            {"role":"user","content":"اتفقنا"},
            {"role":"assistant","content":f"ممتاز! {pick(CLOSE)}"},
        ]
    elif tpl == 38:
        # رفض → تقسيط بلا فائدة + هدية مجانية
        msgs = [
            {"role":"user","content":f"أريد {p['n']} بس غالي علي"},
            {"role":"assistant","content":f"{pick(ALT_OFFER_INTROS)}، عندنا تقسيط بدون فائدة على 3 أشهر"},
            {"role":"user","content":"يعني أدفع شكد بالشهر؟"},
            {"role":"assistant","content":f"مقدم {vp(int(p['p']*0.34))} والباقي قسطين متساويين"},
            {"role":"user","content":"وعليه هدية مع الشراء؟"},
            {"role":"assistant","content":f"إي! معه كفر وسماعة بالمجان، العرض هالأسبوع بس"},
            {"role":"user","content":"هذا جميل والله، آخذه"},
            {"role":"assistant","content":f"{pick(CLOSE)}"},
        ]
    elif tpl == 39:
        # أسلوب واتساب / رسائل قصيرة
        msgs = [
            {"role":"user","content":f"{p['n']} موجود؟"},
            {"role":"assistant","content":f"إي موجود. بـ{vp(p['p'])} دينار"},
            {"role":"user","content":"ألوان شنو؟"},
            {"role":"assistant","content":"أسود، أبيض، رمادي"},
            {"role":"user","content":"الأسود متوفر؟"},
            {"role":"assistant","content":"إي"},
            {"role":"user","content":"توصيل؟"},
            {"role":"assistant","content":"إي، 5000 دينار لبغداد"},
            {"role":"user","content":"ماشي، أريد أسود مع التوصيل"},
            {"role":"assistant","content":f"الكل {vp(p['p']+5000)} دينار. أعطيني عنوانك"},
        ]
    else:
        # رفض متكرر → سعر VIP سري للزبائن القدام
        msgs = [
            {"role":"user","content":f"هلو، {p['n']} بيش؟"},
            {"role":"assistant","content":f"{vp(p['p'])} دينار"},
            {"role":"user","content":f"{pick(EXPENSIVE)}"},
            {"role":"assistant","content":f"{pick(ALT_OFFER_INTROS)}. {p2['n']} بـ{vp(p2['p'])} دينار"},
            {"role":"user","content":"هذا كمان غالي"},
            {"role":"assistant","content":"سؤال: أنت زبون قديم عندنا؟"},
            {"role":"user","content":"إي، من زبائنكم من سنين"},
            {"role":"assistant","content":f"عندنا سعر خاص للزبائن القدام. {p2['n']} بـ{vp(int(p2['p']*0.87))} دينار، مو للكل"},
            {"role":"user","content":"يا سلام! هذا معقول"},
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
    tpl = random.randint(1, 40)

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
    elif tpl == 25:
        msgs = [
            {"role":"user","content":f"صباح الخير، عندكم {item['n']} و{item2['n']}؟"},
            {"role":"assistant","content":f"صباح النور! إي موجودين. {item['n']} بـ{vp(item['p'])} و{item2['n']} بـ{vp(item2['p'])}"},
            {"role":"user","content":"أريد من الاثنين"},
            {"role":"assistant","content":f"كيلو من كل واحد؟"},
            {"role":"user","content":"إي كيلو من كل"},
            {"role":"assistant","content":f"الكل {vp(item['p']+item2['p'])} دينار. {pick(CLOSE)}"},
        ]
    elif tpl == 26:
        # ندرة: البضاعة الطازجة راح تخلص
        msgs = [
            {"role":"user","content":f"هلو، عندكم {item['n']}؟"},
            {"role":"assistant","content":f"إي عندنا، بس {pick(SCARCITY_LINES)}. بـ{vp(item['p'])} دينار الكيلو"},
            {"role":"user","content":"يعني لازم آخذ هسه؟"},
            {"role":"assistant","content":"بيدك، بس هذا طازج اليوم وما نضمن بكره"},
            {"role":"user","content":f"ماشي، أريد {qty} كيلو"},
            {"role":"assistant","content":f"الكل {vp(item['p']*qty)} دينار. {pick(CLOSE)}"},
        ]
    elif tpl == 27:
        # رفض السعر → شرح الجودة + عرض كمية أقل
        msgs = [
            {"role":"user","content":f"هلو، {item['n']} بيش؟"},
            {"role":"assistant","content":f"{vp(item['p'])} دينار الكيلو"},
            {"role":"user","content":f"{pick(EXPENSIVE)}"},
            {"role":"assistant","content":f"{pick(EMPATHY_SELL_LINES)}. هذا {item['n']} طازج من اليوم، جودته تستاهل"},
            {"role":"user","content":"ماشي، أاخذ نص كيلو"},
            {"role":"assistant","content":f"نص كيلو بـ{vp(item['p']//2)} دينار. {pick(CLOSE)}"},
        ]
    elif tpl == 28:
        # إثبات اجتماعي: زبائن كثير يشترون
        msgs = [
            {"role":"user","content":f"صباح الخير، {item['n']} من وين؟"},
            {"role":"assistant","content":f"محلي عراقي، طازج من المزرعة. {pick(SOCIAL_PROOF_LINES)}"},
            {"role":"user","content":"يعني ناس كثير يشترون منه؟"},
            {"role":"assistant","content":f"إي، ويرجعون كل يوم. بـ{vp(item['p'])} دينار الكيلو"},
            {"role":"user","content":f"أاخذ {qty} كيلو"},
            {"role":"assistant","content":f"الكل {vp(item['p']*qty)} دينار. {pick(CLOSE)}"},
        ]
    elif tpl == 29:
        # Bundle: مشتريات مجمعة بخصم
        msgs = [
            {"role":"user","content":f"هلو، أريد {item['n']}"},
            {"role":"assistant","content":f"تفضل، بـ{vp(item['p'])} دينار الكيلو"},
            {"role":"user","content":"ماشي"},
            {"role":"assistant","content":f"لو تاخذ معه {item2['n']} بـ{vp(item2['p'])} أعطيك خصم على الاثنين"},
            {"role":"user","content":"شكد الخصم؟"},
            {"role":"assistant","content":f"10% على المجموع. يعني {vp(int((item['p']*qty+item2['p']*qty)*0.9))} بدل {vp(item['p']*qty+item2['p']*qty)}"},
            {"role":"user","content":"والله مغري، آخذهم"},
            {"role":"assistant","content":f"{pick(CLOSE)}"},
        ]
    elif tpl == 30:
        # Upsell: نوع أحسن بفرق بسيط
        msgs = [
            {"role":"user","content":f"أريد {item['n']}، عندكم؟"},
            {"role":"assistant","content":f"إي عندنا. عندنا نوعين: عادي بـ{vp(item['p'])} ومميز بـ{vp(int(item['p']*1.3))}"},
            {"role":"user","content":"شنو الفرق؟"},
            {"role":"assistant","content":f"المميز أفضل جودة وطعمه أحلى، الفرق بس {vp(int(item['p']*0.3))} دينار"},
            {"role":"user","content":"يستاهل؟"},
            {"role":"assistant","content":"إي والله، ناس هواية يفضلون المميز"},
            {"role":"user","content":"ماشي، آخذ المميز"},
            {"role":"assistant","content":f"{pick(CLOSE)}"},
        ]
    elif tpl == 31:
        # زبون قديم + علاقة
        msgs = [
            {"role":"user","content":"أم علي! زمان ما اشترينا"},
            {"role":"assistant","content":"هلا وغلا! والله مشتاقين. كيف الأولاد؟"},
            {"role":"user","content":"بخير الحمد لله. شنو طازج اليوم؟"},
            {"role":"assistant","content":f"اليوم عندنا {item['n']} طازج من الصبح. {pick(SOCIAL_PROOF_LINES)}"},
            {"role":"user","content":"بيش الكيلو؟"},
            {"role":"assistant","content":f"لأنك أنت، {vp(int(item['p']*0.93))} بدل {vp(item['p'])}"},
            {"role":"user","content":"الله يخليج، أريد كيلوين"},
            {"role":"assistant","content":f"تفضلي، {pick(CLOSE)}"},
        ]
    elif tpl == 32:
        # تردد + حوار + إقناع
        msgs = [
            {"role":"user","content":f"{pick(HESITATE)}، {item['n']} يستاهل بهالسعر؟"},
            {"role":"assistant","content":f"والله {pick(EMPATHY_SELL_LINES)}. هذا طازج اليوم"},
            {"role":"user","content":"بس شايفه غالي شوية"},
            {"role":"assistant","content":f"الجودة تعكس السعر يا أخوي. {pick(SOCIAL_PROOF_LINES)}"},
            {"role":"user","content":"زين، هاتلي كيلو"},
            {"role":"assistant","content":f"{vp(item['p'])} دينار. {pick(CLOSE)}"},
        ]
    elif tpl == 33:
        # رفض → عرض بديل منتج آخر
        msgs = [
            {"role":"user","content":f"هلو، بيش {item['n']}؟"},
            {"role":"assistant","content":f"{vp(item['p'])} دينار الكيلو"},
            {"role":"user","content":f"{pick(EXPENSIVE)}"},
            {"role":"assistant","content":f"{pick(ALT_OFFER_INTROS)}. {item2['n']} بـ{vp(item2['p'])} دينار وجيد هواي"},
            {"role":"user","content":"هذا يصلح بديل؟"},
            {"role":"assistant","content":"إي والله، للطبخ نفس النتيجة وسعره أحسن"},
            {"role":"user","content":"ماشي، آخذ كيلو"},
            {"role":"assistant","content":f"{vp(item2['p'])} دينار. {pick(CLOSE)}"},
        ]
    elif tpl == 34:
        # بيع استشاري: ماذا تريد تطبخ؟
        meals = ["مرق عدس","قيمة","دولمة","تشريب","مسگوف","بريانية"]
        meal = pick(meals)
        msgs = [
            {"role":"user","content":f"هلو، أريد أطبخ {meal}، شنو أشتري؟"},
            {"role":"assistant","content":f"للـ{meal} تريد {item['n']} و{item2['n']} وبهارات. كلها موجودة عندنا"},
            {"role":"user","content":"الكل بيش؟"},
            {"role":"assistant","content":f"حوالي {vp(item['p']*2+item2['p']*2)} دينار لكميات معقولة"},
            {"role":"user","content":"ممتاز، جيبهم مع بعض"},
            {"role":"assistant","content":f"تفضل، {pick(CLOSE)}"},
        ]
    elif tpl == 35:
        # واتساب / رسائل قصيرة
        msgs = [
            {"role":"user","content":f"{item['n']} موجود؟"},
            {"role":"assistant","content":f"إي. {vp(item['p'])} الكيلو"},
            {"role":"user","content":"طازج؟"},
            {"role":"assistant","content":"إي من الصبح"},
            {"role":"user","content":"توصيل؟"},
            {"role":"assistant","content":"إي، 3000 دينار"},
            {"role":"user","content":f"أريد {qty} كيلو مع توصيل"},
            {"role":"assistant","content":f"الكل {vp(item['p']*qty+3000)} دينار. أعطيني عنوانك"},
        ]
    elif tpl == 36:
        # عرض اليوم محدود الوقت
        msgs = [
            {"role":"user","content":"هلو، عندكم عروض اليوم؟"},
            {"role":"assistant","content":f"إي! عرض اليوم: {item['n']} بـ{vp(int(item['p']*0.80))} بدل {vp(item['p'])}. {pick(SCARCITY_LINES)}"},
            {"role":"user","content":"وشي ثاني؟"},
            {"role":"assistant","content":f"{item2['n']} أيضاً بخصم 15% اليوم بس"},
            {"role":"user","content":"ماشي، آخذ من الاثنين"},
            {"role":"assistant","content":f"ذكاء! الكل {vp(int(item['p']*0.80*qty)+int(item2['p']*0.85*qty))} دينار"},
        ]
    elif tpl == 37:
        # خيبة أمل مالية + تعاطف + حل
        msgs = [
            {"role":"user","content":f"{pick(DISAPPOINTED)}، الراتب ما وصل وأريد أشتري مصاريف البيت"},
            {"role":"assistant","content":f"والله ما يهم. {pick(EMPATHY_SELL_LINES)}. شنو تحتاج أكثر؟"},
            {"role":"user","content":f"أحتاج {item['n']} و{item2['n']}"},
            {"role":"assistant","content":f"عندنا الاثنين. {item['n']} بـ{vp(item['p'])} و{item2['n']} بـ{vp(item2['p'])}"},
            {"role":"user","content":"أاخذ كميات أقل"},
            {"role":"assistant","content":f"ماشي، نص كيلو من كل واحد = {vp(item['p']//2+item2['p']//2)} دينار"},
        ]
    elif tpl == 38:
        # Upsell: محلي أحسن من مستورد
        msgs = [
            {"role":"user","content":f"هلو، عندكم {item['n']} مستورد؟"},
            {"role":"assistant","content":f"إي عندنا مستورد. بس المحلي أطعم وأطازج بـ{vp(item['p'])} بدل {vp(int(item['p']*1.2))} للمستورد"},
            {"role":"user","content":"المحلي أرخص؟"},
            {"role":"assistant","content":"إي وأطعم وأطازج، دايماً المحلي أحسن"},
            {"role":"user","content":"ماشي، آخذ المحلي"},
            {"role":"assistant","content":f"{qty} كيلو = {vp(item['p']*qty)} دينار. {pick(CLOSE)}"},
        ]
    elif tpl == 39:
        # رفض + عرض حزمة أسبوعية
        msgs = [
            {"role":"user","content":f"هلو، أشتري كل أسبوع من السوق، كثير يكلف"},
            {"role":"assistant","content":f"عندنا حزمة أسبوعية. {item['n']} و{item2['n']} وبضاعة متنوعة بسعر ثابت"},
            {"role":"user","content":"يعني توصيل أسبوعي؟"},
            {"role":"assistant","content":"إي، كل أسبوع يوصلك طلبك وتوفر على التنقل"},
            {"role":"user","content":"فكرة ممتازة، شنو السعر؟"},
            {"role":"assistant","content":f"حسب الكمية، بس تقريباً {vp(item['p']*3+item2['p']*3)} أسبوعياً"},
        ]
    else:
        # رفض السعر → مبرر الغلاء + تخفيض الكمية
        msgs = [
            {"role":"user","content":f"هلو، {item['n']} غالي هواي هالأيام"},
            {"role":"assistant","content":"والله هالأيام الأسعار صعدت بسبب الطلب والنقل، مو بيدي"},
            {"role":"user","content":"كيلو بيش؟"},
            {"role":"assistant","content":f"{vp(item['p'])} دينار، أرخص ما أكو"},
            {"role":"user","content":"ماشي، أاخذ نص كيلو"},
            {"role":"assistant","content":f"تفضل، {vp(item['p']//2)} دينار. {pick(CLOSE)}"},
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
    tpl = random.randint(1, 40)

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
    elif tpl == 25:
        msgs = [
            {"role":"user","content":f"هلو، عندكم تشكيلة جديدة للشباب؟"},
            {"role":"assistant","content":f"إي وصل كولكشن جديد. {item['n']} {item['f']} بـ{vp(item['p'])} دينار"},
            {"role":"user","content":f"عندكم بلون {color}؟"},
            {"role":"assistant","content":f"إي عندنا {color}"},
            {"role":"user","content":"أاخذه"},
            {"role":"assistant","content":f"{pick(CLOSE)}"},
        ]
    elif tpl == 26:
        # تردد على اللون + مساعدة ودية
        item2c = pick(CLOTHES)
        msgs = [
            {"role":"user","content":f"هلو، {pick(HESITATE)} بين {color} و{pick(COLORS)} لـ{item['n']}"},
            {"role":"assistant","content":f"الاثنين حلوين. بس لو سألتني، {color} أكثر تنوعاً مع الملابس الثانية"},
            {"role":"user","content":"يعني أنسب للبس اليومي؟"},
            {"role":"assistant","content":f"إي، والـ{item['n']} بـ{color} يطلع بأي كومبينيشن. {item['f']}"},
            {"role":"user","content":f"{pick(EXCITED)}، آخذه"},
            {"role":"assistant","content":f"ممتاز! بـ{vp(item['p'])} دينار. {pick(CLOSE)}"},
        ]
    elif tpl == 27:
        # رفض السعر → مقارنة أصل / تقليد بوضوح
        msgs = [
            {"role":"user","content":f"هلو، {item['n']} بيش؟"},
            {"role":"assistant","content":f"{vp(item['p'])} دينار. {item['f']}"},
            {"role":"user","content":f"{pick(EXPENSIVE)}"},
            {"role":"assistant","content":f"عندنا نوعين: الأصل بـ{vp(item['p'])} والبديل بـ{vp(int(item['p']*0.5))}"},
            {"role":"user","content":"شنو الفرق عملياً؟"},
            {"role":"assistant","content":f"الأصل {item['f']}، يدوم أكثر ويبقى لونه. البديل رخيص بس بعد غسلتين يتغير"},
            {"role":"user","content":"آخذ الأصل، يستاهل"},
            {"role":"assistant","content":f"خيار صح! {pick(CLOSE)}"},
        ]
    elif tpl == 28:
        # ندرة المقاس
        msgs = [
            {"role":"user","content":f"هلو، عندكم {item['n']} مقاس {size}؟"},
            {"role":"assistant","content":f"عندنا آخر قطعة مقاس {size}. {pick(SCARCITY_LINES)}"},
            {"role":"user","content":"بيش؟"},
            {"role":"assistant","content":f"{vp(item['p'])} دينار. {item['f']}"},
            {"role":"user","content":f"{pick(DISC_REQ)}"},
            {"role":"assistant","content":f"آخر قطعة ما نكدر ننزل عليها، بس على خاطرك {pick(DISC_YES)}"},
            {"role":"user","content":"ماشي، آخذها"},
            {"role":"assistant","content":f"{pick(CLOSE)}"},
        ]
    elif tpl == 29:
        # إثبات اجتماعي + موضة
        msgs = [
            {"role":"user","content":f"هلو، {item['n']} عصري؟"},
            {"role":"assistant","content":f"إي، {pick(SOCIAL_PROOF_LINES)}. هالموسم هذا الموديل أكثر شي يطلب"},
            {"role":"user","content":"وعندكم بلون {color}؟"},
            {"role":"assistant","content":f"إي موجود. {item['f']}"},
            {"role":"user","content":"آخذه"},
            {"role":"assistant","content":f"بـ{vp(item['p'])} دينار. {pick(CLOSE)}"},
        ]
    elif tpl == 30:
        # Bundle: طقم كامل بسعر خاص
        item2c = pick(CLOTHES)
        while item2c['n'] == item['n']:
            item2c = pick(CLOTHES)
        msgs = [
            {"role":"user","content":f"أريد {item['n']}"},
            {"role":"assistant","content":f"هلا، {item['n']} بـ{vp(item['p'])} دينار. {item['f']}"},
            {"role":"user","content":"ماشي"},
            {"role":"assistant","content":f"لو تاخذ معه {item2c['n']} بـ{vp(item2c['p'])} أعطيك خصم طقم. توفر {vp(int((item['p']+item2c['p'])*0.15))} دينار"},
            {"role":"user","content":"يعني طقم كامل؟"},
            {"role":"assistant","content":f"إي، الطقم بـ{vp(int((item['p']+item2c['p'])*0.85))} بدل {vp(item['p']+item2c['p'])}"},
            {"role":"user","content":"مغري والله، آخذهم"},
            {"role":"assistant","content":f"{pick(CLOSE)}"},
        ]
    elif tpl == 31:
        # Upsell: ماركة أفضل بفرق بسيط
        msgs = [
            {"role":"user","content":f"أريد {item['n']} رخيص"},
            {"role":"assistant","content":f"عندنا بـ{vp(int(item['p']*0.6))} دينار. بس لو تزيد {vp(int(item['p']*0.4))} دينار تاخذ ماركة {item['f']}"},
            {"role":"user","content":"الفرق يستاهل؟"},
            {"role":"assistant","content":f"إي، الماركة تدوم ضعف العمر. {pick(SOCIAL_PROOF_LINES)}"},
            {"role":"user","content":"ماشي، آخذ الأفضل"},
            {"role":"assistant","content":f"{pick(CLOSE)}"},
        ]
    elif tpl == 32:
        # زبون قديم + سعر خاص
        msgs = [
            {"role":"user","content":"هلو، ما اشترينا من فترة"},
            {"role":"assistant","content":"هلا وغلا! والله ناقصين. كيف الأحوال؟"},
            {"role":"user","content":f"بخير. جيت أشوف {item['n']}"},
            {"role":"assistant","content":f"وصل كولكشن جديد! {item['n']} {item['f']}. لأنك زبون قديم بـ{vp(int(item['p']*0.93))}"},
            {"role":"user","content":"الله يخليك، آخذه"},
            {"role":"assistant","content":f"{pick(CLOSE)}"},
        ]
    elif tpl == 33:
        # تردد + تجربة + قناعة
        msgs = [
            {"role":"user","content":f"هلو، أريد أشوف {item['n']} بس مو أعرف إذا يناسبني"},
            {"role":"assistant","content":"تفضل جرب! الغرفة موجودة"},
            {"role":"user","content":"جربته، يناسب بس السعر..."},
            {"role":"assistant","content":f"{pick(EMPATHY_SELL_LINES)}. بـ{vp(item['p'])} دينار وعليه ضمان الغسيل"},
            {"role":"user","content":f"{pick(HESITATE)}"},
            {"role":"assistant","content":f"خليني أقولك، {pick(SCARCITY_LINES)}"},
            {"role":"user","content":"زين، آخذه"},
            {"role":"assistant","content":f"{pick(CLOSE)}"},
        ]
    elif tpl == 34:
        # بيع استشاري: للمناسبة
        occasions = ["الفرح","الدوام","السفر","الزيارات","العيد"]
        occ = pick(occasions)
        msgs = [
            {"role":"user","content":f"هلو، أريد {item['n']} لـ{occ}"},
            {"role":"assistant","content":f"ممتاز! للـ{occ} عندنا {item['n']} {item['f']}. مناسب هواي"},
            {"role":"user","content":f"عندكم مقاس {size}؟"},
            {"role":"assistant","content":f"إي موجود. {vp(item['p'])} دينار"},
            {"role":"user","content":f"{pick(EXCITED)}، آخذه"},
            {"role":"assistant","content":f"مناسبات مباركة! {pick(CLOSE)}"},
        ]
    elif tpl == 35:
        # واتساب style
        msgs = [
            {"role":"user","content":f"{item['n']} عندكم؟"},
            {"role":"assistant","content":f"إي. {vp(item['p'])} دينار"},
            {"role":"user","content":f"مقاس {size}؟"},
            {"role":"assistant","content":"موجود"},
            {"role":"user","content":f"لون {color}؟"},
            {"role":"assistant","content":"إي"},
            {"role":"user","content":"توصيل؟"},
            {"role":"assistant","content":"3000 دينار لبغداد"},
            {"role":"user","content":"ماشي، أريده"},
            {"role":"assistant","content":f"الكل {vp(item['p']+3000)} دينار. أعطيني عنوانك"},
        ]
    elif tpl == 36:
        # رفض + بديل + قبول
        item2c = pick(CLOTHES)
        while item2c['n'] == item['n']:
            item2c = pick(CLOTHES)
        msgs = [
            {"role":"user","content":f"هلو، بيش {item['n']}؟"},
            {"role":"assistant","content":f"{vp(item['p'])} دينار"},
            {"role":"user","content":f"{pick(EXPENSIVE)}"},
            {"role":"assistant","content":f"{pick(ALT_OFFER_INTROS)}. {item2c['n']} بـ{vp(item2c['p'])} دينار. {item2c['f']}"},
            {"role":"user","content":"يشبهه؟"},
            {"role":"assistant","content":"نفس الجودة تقريباً بسعر أنسب"},
            {"role":"user","content":"ماشي، آخذه"},
            {"role":"assistant","content":f"{pick(CLOSE)}"},
        ]
    elif tpl == 37:
        # هدية + تغليف مجاني
        msgs = [
            {"role":"user","content":f"أريد {item['n']} هدية لشخص عزيز"},
            {"role":"assistant","content":"هلا! للهدايا نحطها بكيس هدية أنيق بالمجان"},
            {"role":"user","content":"والتغليف؟"},
            {"role":"assistant","content":"ورق هدية وريبون مجاني مع الشراء"},
            {"role":"user","content":f"وبيش {item['n']}؟"},
            {"role":"assistant","content":f"{vp(item['p'])} دينار مع التغليف"},
            {"role":"user","content":"ممتاز، آخذه"},
            {"role":"assistant","content":f"{pick(CLOSE)}"},
        ]
    elif tpl == 38:
        # تقسيط ملابس
        msgs = [
            {"role":"user","content":f"أريد {item['n']} بس ما عندي كامل الفلوس"},
            {"role":"assistant","content":f"{pick(EMPATHY_SELL_LINES)}. عندنا تقسيط بدون فائدة"},
            {"role":"user","content":"يعني أدفع شكد هسه؟"},
            {"role":"assistant","content":f"نص السعر هسه = {vp(item['p']//2)} والنص بعد شهر"},
            {"role":"user","content":"هذا كافي، ماشي"},
            {"role":"assistant","content":f"{pick(CLOSE)}"},
        ]
    elif tpl == 39:
        # موسمي + خصم وقت محدد
        season = pick(["الصيف","الشتاء","العيد","رمضان"])
        msgs = [
            {"role":"user","content":f"هلو، عندكم خصومات {season}؟"},
            {"role":"assistant","content":f"إي! خصومات {season} شغالة. {item['n']} بـ{vp(int(item['p']*0.80))} بدل {vp(item['p'])}"},
            {"role":"user","content":"لحد متى؟"},
            {"role":"assistant","content":f"لحد نهاية الأسبوع بس. {pick(SCARCITY_LINES)}"},
            {"role":"user","content":"ماشي، آخذ اثنين"},
            {"role":"assistant","content":f"اثنين = {vp(int(item['p']*0.80*2))} دينار. {pick(CLOSE)}"},
        ]
    else:
        # مفاوضة شرسة + تسوية
        msgs = [
            {"role":"user","content":f"أريد {item['n']} بأقل سعر عندك"},
            {"role":"assistant","content":f"هلا، سعره {vp(item['p'])} دينار"},
            {"role":"user","content":f"أعطيك {vp(int(item['p']*0.75))}"},
            {"role":"assistant","content":"والله ما أكدر، هذا دون رأس المال"},
            {"role":"user","content":f"ماشي {vp(int(item['p']*0.85))}؟"},
            {"role":"assistant","content":f"على خاطرك، {vp(int(item['p']*0.88))} وهذا آخر سعر والله"},
            {"role":"user","content":"اتفقنا"},
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
    tpl = random.randint(1, 40)

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
            {"role":"assistant","content":f"هذا الخيار الأفضل للعائلة. بـ{vp(car['p'])} دينار"},
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
    elif tpl == 25:
        msgs = [
            {"role":"user","content":f"هلو، أريد سيارة عائلية، شنو تنصحني؟"},
            {"role":"assistant","content":f"{car['n']} {car['year']} ممتاز للعائلة. {car['f']}"},
            {"role":"user","content":"المقاعد شكد؟"},
            {"role":"assistant","content":"5 مقاعد، كراسي خلفية واسعة وكراج واسع"},
            {"role":"user","content":"السعر؟"},
            {"role":"assistant","content":f"{vp(car['p'])} دينار"},
        ]
    elif tpl == 26:
        # ميزانية محدودة → سيارة أرخص + تعاطف
        msgs = [
            {"role":"user","content":f"{pick(DISAPPOINTED)}، أريد {car['n']} بس ميزانيتي ما تكفي"},
            {"role":"assistant","content":f"والله ما يهم. {pick(EMPATHY_SELL_LINES)}. شنو ميزانيتك؟"},
            {"role":"user","content":f"حوالي {vp(int(car['p']*0.65))} دينار"},
            {"role":"assistant","content":f"ماشي، {pick(ALT_OFFER_INTROS)}. {car2['n']} {car2['year']} بـ{vp(int(car2['p']*0.85))} دينار. {car2['f']}"},
            {"role":"user","content":"هذا يصلح؟"},
            {"role":"assistant","content":f"إي والله، {pick(SOCIAL_PROOF_LINES)}. وفيها كفالة"},
            {"role":"user","content":"ماشي، أجي أشوفها"},
            {"role":"assistant","content":"حياك الله بأي وقت"},
        ]
    elif tpl == 27:
        # رفض → سيارة مستعملة بحالة ممتازة
        msgs = [
            {"role":"user","content":f"أريد {car['n']} بس غالي"},
            {"role":"assistant","content":f"{pick(ALT_OFFER_INTROS)}. عندنا {car['n']} موديل {car['year']-1} مستعمل بحالة ممتازة"},
            {"role":"user","content":"مستعمل؟ شكد ماشيه؟"},
            {"role":"assistant","content":f"40 ألف كيلو بس. بـ{vp(int(car['p']*0.72))} دينار وعليها فحص كراج"},
            {"role":"user","content":f"{pick(HESITATE)}"},
            {"role":"assistant","content":"ندخلها أي كراج تختاره للفحص قبل الشراء"},
            {"role":"user","content":"زين، نفحصها أول"},
            {"role":"assistant","content":"ماشي، نرتب موعد الفحص"},
        ]
    elif tpl == 28:
        # ندرة: لون محدود الوجود
        msgs = [
            {"role":"user","content":f"أريد {car['n']} لون أبيض"},
            {"role":"assistant","content":f"الأبيض موجود هسه. {pick(SCARCITY_LINES)}"},
            {"role":"user","content":"يعني لازم أقرر هسه؟"},
            {"role":"assistant","content":f"لو تريد الأبيض نعزله باسمك. سعره {vp(car['p'])} دينار"},
            {"role":"user","content":"ماشي، اعزله باسمي"},
            {"role":"assistant","content":"زين، نحتاج مبلغ رمزي كعربون. شكد تكدر تدفع؟"},
        ]
    elif tpl == 29:
        # إثبات اجتماعي + أرقام مبيعات
        msgs = [
            {"role":"user","content":f"هلو، {car['n']} يستاهل؟"},
            {"role":"assistant","content":f"والله {pick(SOCIAL_PROOF_LINES)}. بعنا منها {random.randint(5,20)} سيارة هالشهر"},
            {"role":"user","content":"يعني مشهورة؟"},
            {"role":"assistant","content":f"إي، {car['f']} وكفالة {random.randint(2,4)} سنين من الوكالة"},
            {"role":"user","content":"ماشي، أجي أشوفها"},
            {"role":"assistant","content":"حياك الله، المعرض مفتوح من 9 لـ7"},
        ]
    elif tpl == 30:
        # Bundle: سيارة + تأمين + صيانة
        msgs = [
            {"role":"user","content":f"أريد {car['n']}"},
            {"role":"assistant","content":f"هلا، {car['n']} {car['year']} بـ{vp(car['p'])} دينار. {car['f']}"},
            {"role":"user","content":"ماشي"},
            {"role":"assistant","content":f"لو تاخذ معها باكج التأمين والصيانة السنوية أعطيك خصم {vp(int(car['p']*0.03))} دينار"},
            {"role":"user","content":"شنو يتضمن الباكج؟"},
            {"role":"assistant","content":"تأمين شامل سنة + 3 صيانات مجانية + غسيل شهري"},
            {"role":"user","content":"والله صفقة زينة، آخذ الباكج"},
            {"role":"assistant","content":"ممتاز! نكمل الأوراق"},
        ]
    elif tpl == 31:
        # Upsell: درجة أعلى بفرق معقول
        cheap_car = car if car['p'] <= car2['p'] else car2
        exp_car = car2 if car['p'] <= car2['p'] else car
        diff_c = exp_car['p'] - cheap_car['p']
        msgs = [
            {"role":"user","content":f"أريد {cheap_car['n']}"},
            {"role":"assistant","content":f"هلا، {cheap_car['n']} بـ{vp(cheap_car['p'])} دينار. {cheap_car['f']}"},
            {"role":"user","content":"ماشي، يعجبني"},
            {"role":"assistant","content":f"قبل ما تقرر، بـ{vp(diff_c)} دينار زيادة تاخذ {exp_car['n']} اللي {exp_car['f']}. فرق بسيط وفايدته كبيرة"},
            {"role":"user","content":"الفرق يستاهل؟"},
            {"role":"assistant","content":f"إي والله، {exp_car['n']} إعادة بيعها أحسن بكثير"},
            {"role":"user","content":"صح، آخذ الأفضل"},
            {"role":"assistant","content":"ممتاز! نسوي الأوراق"},
        ]
    elif tpl == 32:
        # زبون قديم + سعر خاص
        msgs = [
            {"role":"user","content":"هلو، اشترينا من عندكم قبل سنتين"},
            {"role":"assistant","content":"هلا وغلا! مشتاقين. كيف السيارة القديمة؟"},
            {"role":"user","content":"زينة والحمد لله. جيت أشوف سيارة جديدة"},
            {"role":"assistant","content":f"للزبائن القدام عندنا سعر خاص. {car['n']} {car['year']} بـ{vp(int(car['p']*0.95))} بدل {vp(car['p'])}"},
            {"role":"user","content":"الله يخليكم! هذا يجلب"},
            {"role":"assistant","content":"حياك الله، تعال نكمل الأوراق"},
        ]
    elif tpl == 33:
        # تردد + اختبار قيادة
        msgs = [
            {"role":"user","content":f"{pick(HESITATE)} على {car['n']}"},
            {"role":"assistant","content":"طبيعي تتردد على هالقرار. تريد تجربها وتقود؟"},
            {"role":"user","content":"ممكن؟"},
            {"role":"assistant","content":"إي طبعاً، تجربة القيادة مجانية"},
            {"role":"user","content":"جربتها والله تجنن"},
            {"role":"assistant","content":f"مبروك قرارك! {vp(car['p'])} دينار. نكمل؟"},
            {"role":"user","content":"آخذها"},
            {"role":"assistant","content":"ممتاز! نسوي الأوراق"},
        ]
    elif tpl == 34:
        # بيع استشاري: للعائلة أم للشغل؟
        msgs = [
            {"role":"user","content":"هلو، أريد سيارة بس ما أعرف أختار"},
            {"role":"assistant","content":"أساعدك. للعائلة ولا للشغل؟"},
            {"role":"user","content":"للعائلة، عندنا أطفال"},
            {"role":"assistant","content":"زين. ميزانيتك؟"},
            {"role":"user","content":f"حوالي {vp(car['p'])} دينار"},
            {"role":"assistant","content":f"{car['n']} {car['year']} مثالي للعائلة. {car['f']}، كراسي خلفية واسعة وأمانه 5 نجوم"},
            {"role":"user","content":f"{pick(EXCITED)}"},
            {"role":"assistant","content":"تعال تجربها وتشوف بنفسك"},
        ]
    elif tpl == 35:
        # واتساب style
        msgs = [
            {"role":"user","content":f"{car['n']} {car['year']} موجود؟"},
            {"role":"assistant","content":f"إي موجود. بـ{vp(car['p'])} دينار"},
            {"role":"user","content":"لون أبيض؟"},
            {"role":"assistant","content":"إي"},
            {"role":"user","content":"كيلو شكد؟"},
            {"role":"assistant","content":"0 كيلو، وارد جديد"},
            {"role":"user","content":"فحص ممكن؟"},
            {"role":"assistant","content":"إي، أي كراج تختاره"},
            {"role":"user","content":"ماشي، نرتب"},
            {"role":"assistant","content":"تفضل، رقمي موجود"},
        ]
    elif tpl == 36:
        # مفاوضة مطولة + تسوية
        final_car_price = int(car['p'] * 0.93)
        msgs = [
            {"role":"user","content":f"أريد {car['n']} وعندي {vp(int(car['p']*0.85))} دينار"},
            {"role":"assistant","content":f"سعره {vp(car['p'])} دينار، صعب هالسعر"},
            {"role":"user","content":"ما تنزل؟"},
            {"role":"assistant","content":f"أكثر ما أكدر أنزل {vp(final_car_price)} دينار، وهذا آخر سعر"},
            {"role":"user","content":"ماشي، اتفقنا"},
            {"role":"assistant","content":"ممتاز! نسوي الأوراق"},
        ]
    elif tpl == 37:
        # رهن سيارة قديمة + شراء جديدة
        msgs = [
            {"role":"user","content":f"عندي سيارة قديمة وأريد {car['n']}، تشتري مني؟"},
            {"role":"assistant","content":"إي نشتري. شنو سيارتك؟"},
            {"role":"user","content":f"عندي {car2['n']} موديل {car2['year']-2}"},
            {"role":"assistant","content":f"نشتريها بـ{vp(int(car2['p']*0.6))} دينار. والـ{car['n']} بـ{vp(car['p'])}. الفرق {vp(car['p']-int(car2['p']*0.6))} دينار"},
            {"role":"user","content":"معقول، اتفقنا"},
            {"role":"assistant","content":"زين، نسوي الأوراق وندفع لك الفرق"},
        ]
    elif tpl == 38:
        # رفض متكرر → تقسيط ميسر
        msgs = [
            {"role":"user","content":f"أريد {car['n']} بس الفلوس ما تكفي"},
            {"role":"assistant","content":f"{pick(ALT_OFFER_INTROS)}، عندنا تقسيط على 4 سنين"},
            {"role":"user","content":"المقدم شكد؟"},
            {"role":"assistant","content":f"20% مقدم = {vp(int(car['p']*0.20))} دينار والباقي أقساط شهرية"},
            {"role":"user","content":"القسط الشهري شكد؟"},
            {"role":"assistant","content":f"تقريباً {vp(int(car['p']*0.80/48))} دينار شهري"},
            {"role":"user","content":"معقول، ماشي"},
            {"role":"assistant","content":"ممتاز، نكمل الإجراءات"},
        ]
    elif tpl == 39:
        # فضول + سؤال + بيع
        msgs = [
            {"role":"user","content":f"هلو، سمعت عن {car['n']} هالموديل، شنو يميزه؟"},
            {"role":"assistant","content":f"سؤال ذكي! {car['n']} {car['year']} {car['f']}. ومن أكثر السيارات مبيعاً الفترة هذي"},
            {"role":"user","content":"ليش أكثر مبيعاً؟"},
            {"role":"assistant","content":f"لأنه يجمع الجودة والسعر المعقول. {pick(SOCIAL_PROOF_LINES)}"},
            {"role":"user","content":"ماشي، أجي أشوفها الأسبوع الجاي"},
            {"role":"assistant","content":"حياك الله، احجز موعد حتى تكون جاهزة"},
        ]
    else:
        # رفض + عرض VIP للزبائن القدام
        msgs = [
            {"role":"user","content":f"هلو، {car['n']} بيش؟"},
            {"role":"assistant","content":f"{vp(car['p'])} دينار. {car['f']}"},
            {"role":"user","content":f"{pick(EXPENSIVE)}"},
            {"role":"assistant","content":f"{pick(ALT_OFFER_INTROS)}. {car2['n']} بـ{vp(car2['p'])} دينار. {car2['f']}"},
            {"role":"user","content":"هذا كمان غالي"},
            {"role":"assistant","content":"أنت زبون قديم عندنا؟"},
            {"role":"user","content":"إي، اشتريت منكم قبل"},
            {"role":"assistant","content":f"عندنا سعر خاص للزبائن القدام. {car2['n']} بـ{vp(int(car2['p']*0.92))} دينار"},
            {"role":"user","content":"هذا أحسن، اتفقنا"},
            {"role":"assistant","content":"ممتاز! نسوي الأوراق"},
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
    prop2 = pick(PROPERTIES)
    while prop2["n"] == prop["n"] and prop2["area"] == prop["area"]:
        prop2 = pick(PROPERTIES)
    _gr   = pick(SHORT_GREET)
    _dr   = pick(DISC_REQ)
    _dy   = pick(DISC_YES)
    _exp  = pick(EXPENSIVE)
    _name = pick(_MALE_NAMES_S + _FEMALE_NAMES_S)
    _dist_sch = pick(["200 متر","500 متر","10 دقايق مشي","دقيقتين"])
    _dist_hos = pick(["1 كيلو","2 كيلو","5 دقايق","قريب"])
    _neigh    = pick(["هادية وعوايل محترمة","راقية وأمنية","شعبية ودافية","منظمة وخدماتها كاملة"])
    _floor    = pick(["طابق","طابقين","طابق ثالث","طابق رابع","أرضي"])
    _age_build= pick(["جديد كلياً","بني قبل 5 سنين","بني قبل 10 سنين","قديم بس متين"])
    _elec     = pick(["12 ساعة يومياً","16 ساعة","نظام متفق","مولدة مشتركة"])
    _rooms    = pick(["غرفتين","3 غرف","4 غرف","5 غرف"])
    _appt     = pick(["باچر الصبح","هذا العصر","نهاية الأسبوع","أي يوم يناسبك"])
    _invest_pct= pick([15,20,25,30])
    _down_pct = pick([20,25,30,40])
    _yrs      = pick([3,4,5,7,10])
    _budget   = vp(random.randint(100,500)*1000000)
    tpl = random.randint(1, 40)

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
            {"role":"user","content":f"{_gr}، ميزانيتي {_budget} دينار، ما تنصحني بيه؟"},
            {"role":"assistant","content":f"بهالميزانية عندنا {prop['n']} بـ{prop['area']}. {prop['size']}، {prop['f']}"},
            {"role":"user","content":"السند طابو ولا عقد عرفي؟"},
            {"role":"assistant","content":f"السند طابو رسمي، لا تعب. {_age_build}"},
            {"role":"user","content":"زين هذا يجلب، شوكت أكدر أشوفه؟"},
            {"role":"assistant","content":f"تفضل {_appt} إن شاء الله"},
        ]
    elif tpl == 5:
        msgs = [
            {"role":"user","content":f"هلو، {prop['n']} بـ{prop['area']} قريب من المدارس؟"},
            {"role":"assistant","content":f"إي، على بعد {_dist_sch} من مدرسة"},
            {"role":"user","content":"والمستشفى؟"},
            {"role":"assistant","content":f"قريب من مركز صحي وعلى بعد {_dist_hos} من مستشفى"},
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
            {"role":"user","content":f"{_gr}، أريد {prop['n']} بس ما أعرف المنطقة زينة ولا لا"},
            {"role":"assistant","content":f"{prop['area']} منطقة {_neigh}، خدمات كاملة"},
            {"role":"user","content":"الجيران شلونهم؟"},
            {"role":"assistant","content":f"{_neigh}"},
            {"role":"user","content":f"زين، أجيك {_appt} أشوف"},
            {"role":"assistant","content":"حياك الله، أنا موجود"},
        ]
    elif tpl == 8:
        msgs = [
            {"role":"user","content":f"هلو، {prop['n']} بـ{prop['area']} عنده مشاكل قانونية؟"},
            {"role":"assistant","content":f"لا والله، كلشي نظيف. طابو رسمي {_age_build} وما عليه ديون"},
            {"role":"user","content":"أكدر أشوف الوثائق؟"},
            {"role":"assistant","content":"إي طبعاً، تعال أي وقت وأريك كل الأوراق"},
            {"role":"user","content":f"ماشي، أجي {_appt}"},
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
            {"role":"assistant","content":f"إي، على بعد {_dist_sch} من خط السرفيس الرئيسي"},
            {"role":"user","content":"ومحطة الباص السريع؟"},
            {"role":"assistant","content":f"{_dist_hos} مشي من محطة BRT"},
            {"role":"user","content":"زين، هذا مهم لينا. شكد السعر؟"},
            {"role":"assistant","content":f"{vp(prop['p'])} دينار، وتقدر تفاوض بعد المشاهدة"},
        ]
    elif tpl == 15:
        msgs = [
            {"role":"user","content":f"هلو، شلون البنية التحتية بـ{prop['area']}؟"},
            {"role":"assistant","content":f"كهرباء وطنية {_elec}، ماء شبكة منتظم، صرف صحي كامل"},
            {"role":"user","content":"والشوارع؟"},
            {"role":"assistant","content":f"معبدة وواسعة، والمنطقة {_neigh}"},
            {"role":"user","content":f"زين، عندكم {prop['n']} بهاي المنطقة؟"},
            {"role":"assistant","content":f"إي، {prop['n']} {prop['size']}، {prop['f']}. بـ{vp(prop['p'])} دينار"},
        ]
    elif tpl == 16:
        msgs = [
            {"role":"user","content":f"أريد {prop['n']} كبير، عيلتنا {_rooms} ومحتاجين مساحة"},
            {"role":"assistant","content":f"عندنا {prop['n']} {prop['size']} بـ{prop['area']}، {prop['f']}. يسع عائلة كبيرة"},
            {"role":"user","content":"الحوش واسع؟"},
            {"role":"assistant","content":f"إي، {prop['f']}. والمنطقة {_neigh}"},
            {"role":"user","content":"يعجبني. كيف نرتب المشاهدة؟"},
            {"role":"assistant","content":f"تعطيني رقمك وأتصل بيك. أي وقت يناسبك {_appt}؟"},
        ]
    elif tpl == 17:
        msgs = [
            {"role":"user","content":f"أريد أهدم البيت وأبني من جديد. {prop['n']} بـ{prop['area']} مناسب؟"},
            {"role":"assistant","content":f"إي، {prop['n']} قابل للهدم والبناء. {prop['size']}، {_age_build}. البلدية تسمح ببناء {_floor}"},
            {"role":"user","content":"الجيران ما يصيرون مشكلة؟"},
            {"role":"assistant","content":f"لا، المنطقة {_neigh} ومعتادة على البناء"},
            {"role":"user","content":"شكد السعر؟"},
            {"role":"assistant","content":f"{vp(prop['p'])} دينار، وسعر الأرض لوحدها يستاهل"},
        ]
    elif tpl == 18:
        msgs = [
            {"role":"user","content":f"تريد تشارك بمشروع سكني بـ{prop['area']}؟"},
            {"role":"assistant","content":"ممكن، شنو الفكرة؟"},
            {"role":"user","content":f"أشتري {prop['n']} {prop['size']} وأبني عليه {_floor}، تشارك بالتمويل"},
            {"role":"assistant","content":f"فكرة زينة. اللي عندنا الأرض وإنتو التمويل نكتب عقد واضح. النسبة {_down_pct}% لكل طرف"},
            {"role":"user","content":"موافق من مبدأ. نرتب اجتماع؟"},
            {"role":"assistant","content":f"إي، نرتب {_appt} مع المحامي والمهندس"},
        ]
    elif tpl == 19:
        _hroom = pick(HOME_WORDS) if HOME_WORDS else "صالة"
        msgs = [
            {"role":"user","content":f"هلو، {prop['n']} بـ{prop['area']} مفروش؟"},
            {"role":"assistant","content":"إي فيه مفروش وغير مفروش، تريد أيش؟"},
            {"role":"user","content":"مفروش، كامل؟"},
            {"role":"assistant","content":f"الإصدار المفروش فيه كلشي: كنبة وغرف نوم وأجهزة. حتى الـ{_hroom} مجهزة. الإيجار {vp(prop['p']//250)} دينار"},
            {"role":"user","content":"والغير مفروش؟"},
            {"role":"assistant","content":f"{vp(prop['p']//350)} دينار، ووفر على الفراش"},
        ]
    elif tpl == 20:
        msgs = [
            {"role":"user","content":f"أريد أتأكد من صكوك {prop['n']} بـ{prop['area']} قبل الشراء"},
            {"role":"assistant","content":f"صح، هذا واجب. عندنا طابو رسمي بالكوادستر. {_age_build}"},
            {"role":"user","content":"أكدر أروح أتحقق بنفسي؟"},
            {"role":"assistant","content":"إي طبعاً، معك رقم الصك وتروح دائرة التسجيل العقاري"},
            {"role":"user","content":"زين، شو رقم الصك؟"},
            {"role":"assistant","content":f"أعطيك نسخة من الصك الأصلي لما تجيك {_appt} للمشاهدة"},
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
            {"role":"user","content":f"هلو، في بيوت بالتقسيط الحكومي بـ{prop['area']}؟"},
            {"role":"assistant","content":f"إي، فيه مبادرة الإسكان الحكومية. عندنا {prop['n']} بـ{prop['area']} مشمول بالبرنامج. {_down_pct}% مقدم"},
            {"role":"user","content":"الشروط شنو؟"},
            {"role":"assistant","content":f"راتب حكومي أو تقاعد، وما تملك دار قبل. التقسيط على {_yrs} سنين"},
            {"role":"user","content":"مناسب ليا، شو الخطوة الجاية؟"},
            {"role":"assistant","content":f"تعال بالوثائق الرسمية {_appt} ونبدأ التقديم معك"},
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
    elif tpl == 25:
        msgs = [
            {"role":"user","content":f"مرحبا، أريد أسأل عن {prop['n']} بـ{prop['area']}"},
            {"role":"assistant","content":f"أهلاً وسهلاً، {prop['n']} بـ{prop['area']}، {prop['size']}، {prop['f']}"},
            {"role":"user","content":"السعر كامل؟"},
            {"role":"assistant","content":f"إي، {vp(prop['p'])} دينار شامل كل التكاليف"},
            {"role":"user","content":"زين، أتفكر وأجيك"},
            {"role":"assistant","content":"حياك، أنا موجود"},
        ]
    elif tpl == 26:
        # ميزانية محدودة → منطقة أرخص
        msgs = [
            {"role":"user","content":f"{pick(DISAPPOINTED)}، أريد {prop['n']} بـ{prop['area']} بس ميزانيتي ما تكفي"},
            {"role":"assistant","content":f"والله ما يهم. {pick(EMPATHY_SELL_LINES)}. شنو ميزانيتك؟"},
            {"role":"user","content":f"حوالي {vp(int(prop['p']*0.60))} دينار"},
            {"role":"assistant","content":f"ماشي، {pick(ALT_OFFER_INTROS)}. عندنا {prop2['n']} بـ{prop2['area']} بـ{vp(int(prop2['p']*0.85))} دينار. {prop2['f']}"},
            {"role":"user","content":"المنطقة زينة؟"},
            {"role":"assistant","content":f"{prop2['area']} هادية وخدماتها كاملة. {pick(SOCIAL_PROOF_LINES)}"},
            {"role":"user","content":"ماشي، أجي أشوفه"},
            {"role":"assistant","content":"حياك، نرتب موعد"},
        ]
    elif tpl == 27:
        # رفض الشراء → إيجار بديل
        msgs = [
            {"role":"user","content":f"أريد أشتري {prop['n']} بس السعر ثقيل"},
            {"role":"assistant","content":f"{pick(ALT_OFFER_INTROS)}، ما تفكر بالإيجار أول؟"},
            {"role":"user","content":"الإيجار بكم؟"},
            {"role":"assistant","content":f"{vp(prop['p']//300)} دينار شهري. تسكن وتوفر فلوس"},
            {"role":"user","content":"وبعدين أقدر أشتري؟"},
            {"role":"assistant","content":"إي، وأحياناً يحتسبون الإيجار من الثمن"},
            {"role":"user","content":"فكرة مو بالها، ماشي"},
            {"role":"assistant","content":"نرتب عقد الإيجار ونبدأ"},
        ]
    elif tpl == 28:
        # ندرة: الأرض الأخيرة بالمنطقة
        msgs = [
            {"role":"user","content":f"هلو، عندكم {prop['n']} بـ{prop['area']}؟"},
            {"role":"assistant","content":f"إي عندنا. {pick(SCARCITY_LINES)}. {prop['size']}، {prop['f']}"},
            {"role":"user","content":"يعني لازم أقرر بسرعة؟"},
            {"role":"assistant","content":"ما أجبرك، بس الطلب على المنطقة يزيد وما نضمن السعر بعدين"},
            {"role":"user","content":"ماشي، أجي بكره أشوفه"},
            {"role":"assistant","content":"حياك، ساعد الصبح"},
        ]
    elif tpl == 29:
        # إثبات اجتماعي: مستثمرون يشترون
        msgs = [
            {"role":"user","content":f"هلو، {prop['n']} بـ{prop['area']} استثمار زين؟"},
            {"role":"assistant","content":f"إي والله، {pick(SOCIAL_PROOF_LINES)}. الأسعار ارتفعت 20% هالسنة"},
            {"role":"user","content":"يعني سريع يرتفع؟"},
            {"role":"assistant","content":f"مشاريع حكومية قادمة للمنطقة. مستثمرون كثير يشترون هالأيام"},
            {"role":"user","content":"ماشي، أريد أشوفه"},
            {"role":"assistant","content":"تفضل، نرتب موعد"},
        ]
    elif tpl == 30:
        # Bundle: عقار + ترميم
        msgs = [
            {"role":"user","content":f"أريد {prop['n']} بـ{prop['area']} بس محتاج ترميم"},
            {"role":"assistant","content":f"عندنا باكج: {prop['n']} + ترميم كامل بسعر مجمع"},
            {"role":"user","content":"شنو يتضمن الترميم؟"},
            {"role":"assistant","content":"صباغة وبلاط وسباكة وكهرباء، كلشي جديد"},
            {"role":"user","content":"والمجموع؟"},
            {"role":"assistant","content":f"{vp(int(prop['p']*1.20))} دينار شامل كل شي، وتوفر جهد ووقت كثير"},
            {"role":"user","content":"فكرة ممتازة، نشوف التفاصيل"},
            {"role":"assistant","content":"نرتب اجتماع مع المهندس"},
        ]
    elif tpl == 31:
        # Upsell: منطقة أفضل بفرق معقول
        msgs = [
            {"role":"user","content":f"أريد {prop2['n']} بـ{prop2['area']}"},
            {"role":"assistant","content":f"هلا، {prop2['n']} بـ{prop2['area']} بـ{vp(prop2['p'])} دينار. {prop2['f']}"},
            {"role":"user","content":"ماشي"},
            {"role":"assistant","content":f"قبل ما تقرر، بـ{vp(prop['p']-prop2['p'])} دينار زيادة عندنا {prop['n']} بـ{prop['area']} وهي أرقى وأسرع ارتفاعاً"},
            {"role":"user","content":"الفرق يستاهل؟"},
            {"role":"assistant","content":f"إي والله، {prop['area']} أسعارها كانت دايماً ترتفع أسرع"},
            {"role":"user","content":"ماشي، أشوف الأفضل"},
            {"role":"assistant","content":"نرتب جولة على الاثنين"},
        ]
    elif tpl == 32:
        # زبون قديم + عمولة مخفضة
        msgs = [
            {"role":"user","content":"هلو، اشترينا عقار من عندكم قبل"},
            {"role":"assistant","content":"هلا وغلا! مشتاقين. كيف العقار القديم؟"},
            {"role":"user","content":"بخير الحمد لله. أريد عقار ثاني للاستثمار"},
            {"role":"assistant","content":f"للزبائن القدام نخفض العمولة. عندنا {prop['n']} بـ{prop['area']} بـ{vp(prop['p'])} دينار"},
            {"role":"user","content":"العمولة؟"},
            {"role":"assistant","content":"1.5% بدل 2%، لأنك زبون قديم"},
            {"role":"user","content":"ممتاز، أجي أشوفه"},
            {"role":"assistant","content":"حياك الله"},
        ]
    elif tpl == 33:
        # تردد + مشاهدة ثانية + إقناع
        msgs = [
            {"role":"user","content":f"{pick(HESITATE)} على {prop['n']} اللي شفته"},
            {"role":"assistant","content":"طبيعي، هذا قرار كبير. شنو اللي يردك؟"},
            {"role":"user","content":"مو متأكد من المنطقة"},
            {"role":"assistant","content":f"{prop['area']} منطقة هادية، خدماتها كاملة. تعال نمشي فيها مع بعض"},
            {"role":"user","content":"زين، نروح مع بعض"},
            {"role":"assistant","content":"ماشي، نرتب موعد هذا الأسبوع"},
        ]
    elif tpl == 34:
        # بيع استشاري: للسكن أم للاستثمار؟
        _purpose = pick(["للسكن، عندنا عائلة","للاستثمار وتأجير","للسكن أولاً وبعدين نشوف"])
        _rooms_need = pick(["غرفتين","3 غرف وصالة","4 غرف","5 غرف مع حوش"])
        msgs = [
            {"role":"user","content":f"{_gr}، أريد أشتري عقار بـ{prop['area']} بس ما أعرف أختار"},
            {"role":"assistant","content":"أساعدك. للسكن ولا للاستثمار؟"},
            {"role":"user","content":f"{_purpose}"},
            {"role":"assistant","content":f"زين. كم غرفة تحتاج؟"},
            {"role":"user","content":f"{_rooms_need}"},
            {"role":"assistant","content":f"عندنا {prop['n']} بـ{prop['area']}، {prop['size']}، {prop['f']}. مناسب"},
            {"role":"user","content":"قرب المدارس؟"},
            {"role":"assistant","content":f"على بعد {_dist_sch} من مدرسة حكومية وخاصة"},
        ]
    elif tpl == 35:
        # واتساب style
        msgs = [
            {"role":"user","content":f"{prop['n']} بـ{prop['area']} موجود؟"},
            {"role":"assistant","content":f"إي. {vp(prop['p'])} دينار"},
            {"role":"user","content":"المساحة؟"},
            {"role":"assistant","content":prop['size']},
            {"role":"user","content":"الصك طابو؟"},
            {"role":"assistant","content":"إي، طابو رسمي"},
            {"role":"user","content":"مشاهدة ممكنة؟"},
            {"role":"assistant","content":"إي، أي وقت"},
            {"role":"user","content":"بكره الصبح"},
            {"role":"assistant","content":"ماشي، 10 الصبح. أعطيني رقمك"},
        ]
    elif tpl == 36:
        # مفاوضة + تسوية
        final_prop_price = int(prop['p'] * 0.93)
        msgs = [
            {"role":"user","content":f"أريد {prop['n']} بـ{prop['area']} وعندي {vp(int(prop['p']*0.85))} دينار"},
            {"role":"assistant","content":f"سعره {vp(prop['p'])} دينار، صعب هالسعر"},
            {"role":"user","content":"ما تنزل؟"},
            {"role":"assistant","content":f"أكثر ما أكدر {vp(final_prop_price)} دينار، وهذا آخر سعر"},
            {"role":"user","content":"اتفقنا"},
            {"role":"assistant","content":"زين، نسوي الأوراق"},
        ]
    elif tpl == 37:
        # رفض + تمويل بنكي
        msgs = [
            {"role":"user","content":f"أريد {prop['n']} بس ما عندي الكامل"},
            {"role":"assistant","content":f"{pick(ALT_OFFER_INTROS)}، تقدر تاخذ قرض بنكي"},
            {"role":"user","content":"البنك يعطي قرض للعقار؟"},
            {"role":"assistant","content":"إي، البنك الرافدين والرشيد عندهم قروض عقارية بفائدة معقولة"},
            {"role":"user","content":"الشروط شنو؟"},
            {"role":"assistant","content":"راتب حكومي أو تقاعد، ضمان الراتب، وما عليك قرض ثاني"},
            {"role":"user","content":"أنا موظف حكومي، يصلح"},
            {"role":"assistant","content":"ممتاز، نساعدك بالأوراق"},
        ]
    elif tpl == 38:
        # فضول + عرض استثماري
        msgs = [
            {"role":"user","content":f"هلو، سمعت إن {prop['area']} أسعارها رايحة تصعد"},
            {"role":"assistant","content":f"صح! المنطقة فيها مشاريع حكومية قادمة. {pick(SOCIAL_PROOF_LINES)}"},
            {"role":"user","content":"يعني لو اشتريت هسه ربح؟"},
            {"role":"assistant","content":f"متوقع ارتفاع 25-30% خلال سنتين. {prop['n']} {prop['size']} بـ{vp(prop['p'])} دينار هسه"},
            {"role":"user","content":"هذا استثمار ممتاز"},
            {"role":"assistant","content":"لا تتأخر، الأسعار ما تنتظر"},
        ]
    elif tpl == 39:
        # رفض + شراكة مع صاحب الملك
        msgs = [
            {"role":"user","content":f"أريد {prop['n']} بـ{prop['area']} بس غالي علي"},
            {"role":"assistant","content":f"{pick(ALT_OFFER_INTROS)}، شراكة مع صاحب الملك؟"},
            {"role":"user","content":"يعني شنو؟"},
            {"role":"assistant","content":"تدفع 40% وصاحب الملك 60%، وتتقاسمون الأرباح"},
            {"role":"user","content":"وإذا أريد أبيع؟"},
            {"role":"assistant","content":"بعد 3 سنين تقدر تبيع حصتك أو تشتري الباقي"},
            {"role":"user","content":"فكرة ما فكرت فيها، تفصيل أكثر"},
            {"role":"assistant","content":"نرتب اجتماع مع صاحب الملك والمحامي"},
        ]
    else:
        # ثلاث محاولات: رفض → بديل → رفض → بديل → قبول
        msgs = [
            {"role":"user","content":f"هلو، أريد {prop['n']} بـ{prop['area']}"},
            {"role":"assistant","content":f"هلا، بـ{vp(prop['p'])} دينار. {prop['f']}"},
            {"role":"user","content":f"{pick(EXPENSIVE)}"},
            {"role":"assistant","content":f"{pick(ALT_OFFER_INTROS)}. {prop2['n']} بـ{prop2['area']} بـ{vp(prop2['p'])} دينار"},
            {"role":"user","content":"هذا كمان غالي"},
            {"role":"assistant","content":f"ماشي، عندنا {prop2['n']} بالإيجار بـ{vp(prop2['p']//300)} شهري. خيار وسط"},
            {"role":"user","content":"الإيجار أنسب هسه"},
            {"role":"assistant","content":"ممتاز، نرتب عقد الإيجار"},
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
    item2f = pick(FURNITURE)
    while item2f['n'] == item['n']:
        item2f = pick(FURNITURE)
    tpl = random.randint(1, 40)

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
    elif tpl == 25:
        _hf1 = pick(HOME_WORDS) if HOME_WORDS else "صالة"
        _hf2 = pick(HOME_WORDS) if HOME_WORDS else "ديوان"
        msgs = [
            {"role":"user","content":f"هلو، أريد أفرش شقتي الجديدة"},
            {"role":"assistant","content":"مبارك على الشقة! نحن متخصصين بتأثيث البيوت الجديدة"},
            {"role":"user","content":f"ابدأ بـ{item['n']} للـ{_hf1}، شكد؟"},
            {"role":"assistant","content":f"{item['n']} بـ{vp(item['p'])} دينار. {item['f']}"},
            {"role":"user","content":f"وللـ{_hf2} شنو عندكم؟"},
            {"role":"assistant","content":"تفضل، الكتالوج كامل وفيه كل الغرف والصالات"},
        ]
    elif tpl == 26:
        # خيبة أمل + تعاطف + بديل أرخص
        msgs = [
            {"role":"user","content":f"{pick(DISAPPOINTED)}، أريد {item['n']} بس الميزانية ما تكفي"},
            {"role":"assistant","content":f"والله ما يهم. {pick(EMPATHY_SELL_LINES)}. بيش ميزانيتك؟"},
            {"role":"user","content":f"حوالي {vp(int(item['p']*0.6))} دينار"},
            {"role":"assistant","content":f"ماشي، {pick(ALT_OFFER_INTROS)}. عندنا {item2f['n']} بـ{vp(int(item2f['p']*0.85))} دينار. {item2f['f']}"},
            {"role":"user","content":"هذا يصلح؟"},
            {"role":"assistant","content":f"إي والله، {pick(SOCIAL_PROOF_LINES)}"},
            {"role":"user","content":"ماشي، آخذه"},
            {"role":"assistant","content":f"{pick(CLOSE)}"},
        ]
    elif tpl == 27:
        # رفض السعر → عرض مستعمل
        msgs = [
            {"role":"user","content":f"أريد {item['n']} بس غالي"},
            {"role":"assistant","content":f"{pick(ALT_OFFER_INTROS)}، عندنا {item['n']} مستعمل بحالة ممتازة بـ{vp(int(item['p']*0.5))} دينار"},
            {"role":"user","content":"مستعمل؟ بحالة زينة؟"},
            {"role":"assistant","content":"زبون غيّر ديكور بيته، الأثاث بحالة مثالية"},
            {"role":"user","content":f"{pick(HESITATE)}"},
            {"role":"assistant","content":f"تعال أشوفه بنفسك، {pick(SCARCITY_LINES)}"},
            {"role":"user","content":"زين، آخذه"},
            {"role":"assistant","content":f"{pick(CLOSE)}"},
        ]
    elif tpl == 28:
        # ندرة التصميم
        msgs = [
            {"role":"user","content":f"هلو، عندكم {item['n']} بتصميم كلاسيكي؟"},
            {"role":"assistant","content":f"إي عندنا. {pick(SCARCITY_LINES)}. {item['f']}"},
            {"role":"user","content":"بيش؟"},
            {"role":"assistant","content":f"{vp(item['p'])} دينار. وعليه ضمان سنتين"},
            {"role":"user","content":"يعني لازم أقرر هسه؟"},
            {"role":"assistant","content":"ما أجبرك، بس هذا التصميم ما يجي ثاني"},
            {"role":"user","content":"ماشي، آخذه"},
            {"role":"assistant","content":f"{pick(CLOSE)}"},
        ]
    elif tpl == 29:
        # إثبات اجتماعي
        msgs = [
            {"role":"user","content":f"هلو، {item['n']} يستاهل؟"},
            {"role":"assistant","content":f"والله {pick(SOCIAL_PROOF_LINES)}. {item['f']}"},
            {"role":"user","content":"يعني زبائن راضين؟"},
            {"role":"assistant","content":"إي، وعندنا تقييمات ممتازة. تجربتنا {random.randint(5,20)} سنة بالسوق"},
            {"role":"user","content":"هذا يريح. آخذه"},
            {"role":"assistant","content":f"بـ{vp(item['p'])} دينار. {pick(CLOSE)}"},
        ]
    elif tpl == 30:
        # Bundle: أثاث كامل للغرفة
        msgs = [
            {"role":"user","content":f"أريد {item['n']}"},
            {"role":"assistant","content":f"هلا، {item['n']} بـ{vp(item['p'])} دينار. {item['f']}"},
            {"role":"user","content":"ماشي"},
            {"role":"assistant","content":f"لو تاخذ معه {item2f['n']} بـ{vp(item2f['p'])} دينار نعطيك خصم غرفة كاملة. توفر {vp(int((item['p']+item2f['p'])*0.12))} دينار"},
            {"role":"user","content":"يعني أوفر بالمجموعة؟"},
            {"role":"assistant","content":f"إي، بدل {vp(item['p']+item2f['p'])} يصير {vp(int((item['p']+item2f['p'])*0.88))} بس"},
            {"role":"user","content":"مغري، آخذهم مع بعض"},
            {"role":"assistant","content":f"{pick(CLOSE)}"},
        ]
    elif tpl == 31:
        # Upsell: تركي بدل صيني
        msgs = [
            {"role":"user","content":f"أريد {item['n']} بأرخص سعر"},
            {"role":"assistant","content":f"عندنا صيني بـ{vp(int(item['p']*0.6))} دينار. بس لو تزيد {vp(int(item['p']*0.4))} دينار تاخذ التركي اللي {item['f']}"},
            {"role":"user","content":"الفرق يستاهل؟"},
            {"role":"assistant","content":f"إي، التركي يدوم ضعف عمر الصيني. {pick(SOCIAL_PROOF_LINES)}"},
            {"role":"user","content":"ماشي، آخذ الأفضل"},
            {"role":"assistant","content":f"{pick(CLOSE)}"},
        ]
    elif tpl == 32:
        # زبون قديم
        msgs = [
            {"role":"user","content":"هلو، اشترينا من عندكم سابق"},
            {"role":"assistant","content":"هلا وغلا! مشتاقين. كيف الأثاث القديم؟"},
            {"role":"user","content":"زين والحمد لله. جيت أشوف شي جديد"},
            {"role":"assistant","content":f"للزبائن القدام عندنا سعر خاص. {item['n']} بـ{vp(int(item['p']*0.93))} بدل {vp(item['p'])}"},
            {"role":"user","content":"الله يخليكم، ماخذه"},
            {"role":"assistant","content":f"{pick(CLOSE)}"},
        ]
    elif tpl == 33:
        # تردد + مشاهدة + قناعة
        msgs = [
            {"role":"user","content":f"{pick(HESITATE)} على {item['n']}"},
            {"role":"assistant","content":"طبيعي. تعال شوف الجودة بنفسك"},
            {"role":"user","content":"جبته ولمسته، يبدو زين بس السعر..."},
            {"role":"assistant","content":f"{pick(EMPATHY_SELL_LINES)}. وعليه ضمان سنتين"},
            {"role":"user","content":f"{pick(SCARCITY_LINES)}؟"},
            {"role":"assistant","content":"صح، هذا الموديل طلب عليه هواي"},
            {"role":"user","content":"زين، آخذه"},
            {"role":"assistant","content":f"{pick(CLOSE)}"},
        ]
    elif tpl == 34:
        # بيع استشاري: وصف البيت
        msgs = [
            {"role":"user","content":f"هلو، أريد {item['n']} بس ما أعرف أختار"},
            {"role":"assistant","content":"وصفلي البيت وأساعدك تختار"},
            {"role":"user","content":"ديكوري أبيض وخشبي مع لمسات ذهبية"},
            {"role":"assistant","content":f"عندنا {item['n']} كلاسيكي بخشب فاتح وتفاصيل ذهبية. مناسب هواي. {item['f']}"},
            {"role":"user","content":f"{pick(EXCITED)}"},
            {"role":"assistant","content":f"بـ{vp(item['p'])} دينار مع التوصيل والتركيب"},
            {"role":"user","content":"ماشي، آخذه"},
            {"role":"assistant","content":f"{pick(CLOSE)}"},
        ]
    elif tpl == 35:
        # واتساب style
        msgs = [
            {"role":"user","content":f"{item['n']} موجود؟"},
            {"role":"assistant","content":f"إي. {vp(item['p'])} دينار"},
            {"role":"user","content":"توصيل؟"},
            {"role":"assistant","content":"مجاني داخل بغداد"},
            {"role":"user","content":"تركيب؟"},
            {"role":"assistant","content":"مجاني مع التوصيل"},
            {"role":"user","content":"ألوان؟"},
            {"role":"assistant","content":"أبيض، رمادي، بيج، وخشبي"},
            {"role":"user","content":"أريد الرمادي"},
            {"role":"assistant","content":"ماشي، أعطيني العنوان"},
        ]
    elif tpl == 36:
        # رفض + بديل مختلف
        msgs = [
            {"role":"user","content":f"هلو، {item['n']} بيش؟"},
            {"role":"assistant","content":f"{vp(item['p'])} دينار. {item['f']}"},
            {"role":"user","content":f"{pick(EXPENSIVE)}"},
            {"role":"assistant","content":f"{pick(ALT_OFFER_INTROS)}. {item2f['n']} بـ{vp(item2f['p'])} دينار. {item2f['f']}"},
            {"role":"user","content":"هذا أنسب لميزانيتي؟"},
            {"role":"assistant","content":"إي، وجودته ممتازة أيضاً"},
            {"role":"user","content":"ماشي، آخذه"},
            {"role":"assistant","content":f"{pick(CLOSE)}"},
        ]
    elif tpl == 37:
        # تقسيط ميسر
        msgs = [
            {"role":"user","content":f"أريد {item['n']} بالتقسيط"},
            {"role":"assistant","content":f"إي عندنا. سعره {vp(item['p'])} دينار على 6 أشهر بدون فائدة"},
            {"role":"user","content":"القسط الشهري شكد؟"},
            {"role":"assistant","content":f"{vp(item['p']//6)} دينار شهري"},
            {"role":"user","content":"وبدون فائدة؟"},
            {"role":"assistant","content":"إي، تماماً بدون فائدة"},
            {"role":"user","content":"ماشي، آخذه"},
            {"role":"assistant","content":"ممتاز، نكمل الأوراق"},
        ]
    elif tpl == 38:
        # مفاوضة + تسوية
        final_furn_price = int(item['p'] * 0.91)
        msgs = [
            {"role":"user","content":f"أريد {item['n']} بأقل سعر"},
            {"role":"assistant","content":f"هلا، سعره {vp(item['p'])} دينار"},
            {"role":"user","content":f"أعطيك {vp(int(item['p']*0.78))}"},
            {"role":"assistant","content":"والله ما أكدر، هذا دون التكلفة"},
            {"role":"user","content":f"ماشي {vp(int(item['p']*0.85))}؟"},
            {"role":"assistant","content":f"على خاطرك {vp(final_furn_price)} وهذا آخر سعر"},
            {"role":"user","content":"اتفقنا"},
            {"role":"assistant","content":f"{pick(CLOSE)}"},
        ]
    elif tpl == 39:
        # عرض وقت محدد: خصم افتتاح
        msgs = [
            {"role":"user","content":"هلو، عندكم عروض الافتتاح؟"},
            {"role":"assistant","content":f"إي! خصم 20% على كل شي هالأسبوع. {item['n']} بـ{vp(int(item['p']*0.80))} بدل {vp(item['p'])}"},
            {"role":"user","content":"وشي ثاني بالعرض؟"},
            {"role":"assistant","content":f"{item2f['n']} أيضاً بـ{vp(int(item2f['p']*0.80))} بدل {vp(item2f['p'])}"},
            {"role":"user","content":"آخذهم مع بعض"},
            {"role":"assistant","content":f"ممتاز! الكل {vp(int((item['p']+item2f['p'])*0.80))} دينار. {pick(CLOSE)}"},
        ]
    else:
        # رفض متكرر → باكج تأثيث كامل بسعر خاص
        _hroom2 = pick(HOME_WORDS) if HOME_WORDS else "غرفة"
        msgs = [
            {"role":"user","content":f"هلو، أريد أفرش الـ{_hroom2} بس الأسعار كلها غالية"},
            {"role":"assistant","content":f"{pick(EMPATHY_SELL_LINES)}. عندنا باكج كامل بسعر خاص"},
            {"role":"user","content":"شنو يتضمن الباكج؟"},
            {"role":"assistant","content":f"{item['n']} + {item2f['n']} + توصيل وتركيب مجاني"},
            {"role":"user","content":"شكد المجموع؟"},
            {"role":"assistant","content":f"الباكج بـ{vp(int((item['p']+item2f['p'])*0.82))} دينار بدل {vp(item['p']+item2f['p'])}"},
            {"role":"user","content":"والله هذا عرض ما أكدر أرفضه"},
            {"role":"assistant","content":f"{pick(CLOSE)}"},
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
    svc  = pick(SERVICES)
    svc2 = pick(SERVICES)
    _gr   = pick(SHORT_GREET)
    _dr   = pick(DISC_REQ)
    _dy   = pick(DISC_YES)
    _exp  = pick(EXPENSIVE)
    _city = pick(_cat("المدن والأماكن العراقية") or ["الكرادة","الجادرية","المنصور","الكاظمية","الأعظمية","زيونة","البياع"])
    _city2= pick(_cat("المحافظات العراقية") or ["بغداد","البصرة","النجف","كربلاء","الموصل"])
    _name = pick(_MALE_NAMES_S + _FEMALE_NAMES_S)
    _part = pick(["الموتور","الكومبريسور","الضاغط","البورد","الثيرموستات","المحرك","اللحام","الضبط"])
    _brand= pick(["سامسونج","LG","ميديا","كاريير","شارپ","توشيبا","هيتاشي","باناسونيك"])
    _age  = pick(["سنتين","3 سنين","4 سنين","5 سنين","6 سنين","سبع سنين"])
    _nrooms= pick(["غرفتين","3 غرف","4 غرف","5 غرف"])
    _time = pick(["الصبح الباچر","بعد الظهر","العصر","العشية","عصر باچر"])
    _days = pick(["يومين","3 أيام","أسبوع","يوم واحد","ساعات"])
    _warrmonth = pick(["شهر","3 أشهر","6 أشهر","سنة"])
    _prob = pick(["ما تشتغل","تصدر صوت غريب","تحرق","ما تبرد","ما تسخن","تكسر"])
    _extra= pick(["مع فاتورة رسمية","مع ضمان","شامل القطع","مع متابعة لاحقة"])
    _pay  = pick(["كاش","فلوس جاهزة","بالكارت","أقساط شهرية"])
    _haircut = pick(["قصة عصرية","قصة شباب","حلاقة عادية","فيد قصير","قصة كلاسيك","تنظيف ولحية"])
    _mobile_brand = pick(["سامسونج","آيفون","هواوي","أوبو","ريدمي","تكنو","إنفينكس"])
    _mobile_model = pick(["A54","S23","14 Pro","Nova","Y90","Camon 30","Hot 40"])
    _screen_price = pick([60000,70000,80000,90000,100000,120000])
    _pipe_part= pick(["فلنجة الغلق","طوبة البلاستيك","مانع التسريب","المحبس","الخط الرئيسي"])
    _cam_num = pick([2,4,6,8])
    _cam_type= pick(["HD","Full HD","4K","Night Vision"])
    _cam_price=pick([300000,400000,500000,600000,700000])
    _elec_prob= pick(["خط كهرباء مقطوع","كاتش مايت خربان","تأريض مفقود","بريكر متعطل","بوردة قديمة"])
    _wash_brand= pick(["LG","سامسونج","وستنجهاوس","توشيبا","ميديا"])
    _wash_prob = pick(["ما تدور","تدور وتوقف","تصدر صوت","ما تملى ماي","ما تفضي"])
    _laptop_prob= pick(["شاشة سوداء","ما يفتح","يطفي لوحده","بطيء","شاشة مكسورة","كيبورد خربان"])
    _laptop_part= pick(["الكارد","الرامات","الهارد","المروحة","البطارية","الشاشة"])
    _fridge_prob= pick(["ما يبرد","يجمد كلشي","يصدر ضوضاء","ما يشتغل","يسرب ماي"])
    _paint_type = pick(["صبغ بلاستيك","صبغ زيت","ديكور فنچي","رول","بخاخ"])
    _disc_pct  = pick([5,10,15,20])
    _install_time = pick(["نص ساعة","ساعة","ساعتين","3 ساعات","يوم كامل"])
    _area = pick(["الباب","الشباك","الحمام","الطابق العلوي","الطابق السفلي","الغرفة الرئيسية"])
    _appt = pick(["هسه","بعد ساعة","بعد الظهر","باچر الصبح","عصر هذا اليوم","باچر العصر"])
    tpl = random.randint(1, 80)

    if tpl == 1:
        msgs = [
            {"role":"user","content":f"{_gr}، أريد {svc['n']}"},
            {"role":"assistant","content":f"هلا، {svc['f']}. أگدر أساعدك. شنو المشكلة بالضبط؟"},
            {"role":"user","content":f"المشكلة موجودة من {_days}"},
            {"role":"assistant","content":f"ماشي، نشوف المشكلة أول وبعدين نحدد السعر. تقريباً {vp(svc['p'])} دينار"},
            {"role":"user","content":f"{_dr}"},
            {"role":"assistant","content":f"{_dy}"},
            {"role":"user","content":"زين، شوكت تكدر تجي؟"},
            {"role":"assistant","content":f"إن شاء الله {_appt}"},
        ]
    elif tpl == 2:
        msgs = [
            {"role":"user","content":f"هلو، شكد تاخذ على {svc['n']}؟"},
            {"role":"assistant","content":f"حسب المشكلة، بس تقريباً بين {vp(int(svc['p']*0.8))} لـ{vp(int(svc['p']*1.2))} دينار"},
            {"role":"user","content":"يعني ما تكدر تعطيني سعر ثابت؟"},
            {"role":"assistant","content":f"لازم أشوف أول. لو مشكلة بسيطة أقل، لو معقدة أكثر. {_extra}"},
            {"role":"user","content":"ماشي، تعال شوف"},
            {"role":"assistant","content":f"حاضر، {_appt} إن شاء الله"},
        ]
    elif tpl == 3:
        msgs = [
            {"role":"user","content":"موبايلي انكسرت شاشته، شكد التصليح؟"},
            {"role":"assistant","content":"شنو نوع الموبايل؟"},
            {"role":"user","content":f"{_mobile_brand} {_mobile_model}"},
            {"role":"assistant","content":f"شاشة {_mobile_brand} {_mobile_model} بـ{vp(_screen_price)} دينار تقريباً، وبيد {_install_time}"},
            {"role":"user","content":f"{_exp}"},
            {"role":"assistant","content":"هذا سعر القطعة الأصل، التقليد أرخص بس ما يستاهل"},
            {"role":"user","content":"زين، أجيك"},
            {"role":"assistant","content":"حياك الله"},
        ]
    elif tpl == 4:
        msgs = [
            {"role":"user","content":f"تكييفي {_prob}، شنو المشكلة؟"},
            {"role":"assistant","content":"شنو نوعه وعمره؟"},
            {"role":"user","content":f"{_brand}، من {_age}"},
            {"role":"assistant","content":f"غالباً محتاج {_part}. نجي نكشف أول. الكشف بالمجان"},
            {"role":"user","content":"شكد لو احتاج تصليح؟"},
            {"role":"assistant","content":f"حسب المشكلة، تقريباً {vp(svc['p'])} دينار {_extra}"},
        ]
    elif tpl == 5:
        msgs = [
            {"role":"user","content":f"أريد أصبغ بيتي {_nrooms}، شكد تاخذ؟"},
            {"role":"assistant","content":f"شنو نوع الصبغ تريد؟ {_paint_type}؟"},
            {"role":"user","content":f"إي، {_paint_type}"},
            {"role":"assistant","content":f"تقريباً {vp(400000)} دينار شامل الصبغ والعمالة"},
            {"role":"user","content":f"{_exp}"},
            {"role":"assistant","content":f"هذا سعر نار والله. لو دفعت {_disc_pct*5}% مقدم أخفف شوية"},
        ]
    elif tpl == 6:
        msgs = [
            {"role":"user","content":f"أريد أركب {_cam_num} كاميرات مراقبة للبيت"},
            {"role":"assistant","content":"شكد كاميرا تريد وشنو نوع البيت؟"},
            {"role":"user","content":f"{_cam_num} كاميرات، {pick(['بيت طابق','بيت طابقين','فيلا','شقة'])}"},
            {"role":"assistant","content":f"{_cam_num} كاميرات {_cam_type} مع DVR بـ{vp(_cam_price)} دينار، شامل التركيب"},
            {"role":"user","content":"تشتغل على الموبايل؟"},
            {"role":"assistant","content":f"إي، تشوف البيت من موبايلك أي مكان. {_extra}"},
        ]
    elif tpl == 7:
        msgs = [
            {"role":"user","content":f"عندي تسريب ماء {pick(['بالحمام','بالمطبخ','بالسطح','بالصالة','بالغرفة'])}"},
            {"role":"assistant","content":"من وين يطلع الماء؟"},
            {"role":"user","content":f"من {_area}"},
            {"role":"assistant","content":f"غالباً {_pipe_part}. نجي نصلحها بـ{vp(40000)} دينار"},
            {"role":"user","content":"شوكت تكدر تجي؟"},
            {"role":"assistant","content":f"{_appt} إذا تريد"},
        ]
    elif tpl == 8:
        msgs = [
            {"role":"user","content":"أريد أحلق شعري، شنو عندكم؟"},
            {"role":"assistant","content":"أهلاً، تفضل. عندنا كل أنواع القصات"},
            {"role":"user","content":f"أريد {_haircut}"},
            {"role":"assistant","content":f"ماشي، اجلس. {_haircut} بـ{vp(10000)} دينار"},
            {"role":"user","content":f"{_dr}"},
            {"role":"assistant","content":f"هذا أرخص سعر بالمنطقة. {_dy}"},
        ]
    elif tpl == 9:
        msgs = [
            {"role":"user","content":f"غسالتي {_wash_prob}، شكد التصليح؟"},
            {"role":"assistant","content":"شنو ماركتها وشنو اللي يصير بالضبط؟"},
            {"role":"user","content":f"{_wash_brand}، {_wash_prob}"},
            {"role":"assistant","content":f"غالباً {_part}. بـ{vp(60000)} دينار تقريباً"},
            {"role":"user","content":"ماشي، شوكت تجي؟"},
            {"role":"assistant","content":f"{_appt} إن شاء الله"},
        ]
    elif tpl == 10:
        msgs = [
            {"role":"user","content":f"{_gr}، أريد {svc['n']}"},
            {"role":"assistant","content":"هلا، تفضل. شنو المشكلة؟"},
            {"role":"user","content":f"مشكلة {pick(['بسيطة','متوسطة','معقدة شوية'])} بس محتاجة تصليح"},
            {"role":"assistant","content":f"ماشي، نشوف. تقريباً {vp(svc['p'])} دينار {_extra}"},
            {"role":"user","content":"شوكت؟"},
            {"role":"assistant","content":f"{_appt} إن شاء الله"},
        ]
    elif tpl == 11:
        msgs = [
            {"role":"user","content":f"هلو، أريد {svc['n']} بس بسرعة"},
            {"role":"assistant","content":"ممكن. شنو الوقت المناسب لك؟"},
            {"role":"user","content":f"{_appt} إذا ممكن"},
            {"role":"assistant","content":f"ماشي، بـ{_install_time} وأكون عندك. تقريباً {vp(svc['p'])} دينار"},
            {"role":"user","content":"ممتاز، عطيك عنوان"},
            {"role":"assistant","content":"تفضل، وين منطقتك؟"},
        ]
    elif tpl == 12:
        msgs = [
            {"role":"user","content":f"مرحبا، عندي {svc['n']}، صارله {_days}"},
            {"role":"assistant","content":"وصفلي المشكلة بالتفصيل حتى أقدر أجهز"},
            {"role":"user","content":f"الجهاز {_prob}"},
            {"role":"assistant","content":f"غالباً مشكلة بـ{_part}. أجي أكشف أول. الكشف بالمجان"},
            {"role":"user","content":"ماشي، شكد لو احتاج تصليح؟"},
            {"role":"assistant","content":f"بعد الفحص نعرف، تقريباً {vp(svc['p'])} دينار {_extra}"},
        ]
    elif tpl == 13:
        msgs = [
            {"role":"user","content":f"هلو، عندكم ضمان على {svc['n']}؟"},
            {"role":"assistant","content":f"إي، نضمن الشغل {_warrmonth}. لو رجعت المشكلة نصلحها بالمجان"},
            {"role":"user","content":"زين، هذا مهم"},
            {"role":"assistant","content":f"التصليح بـ{vp(svc['p'])} دينار مع ضمان {_warrmonth}"},
            {"role":"user","content":"ماشي، متى تجي؟"},
            {"role":"assistant","content":f"{_appt} إن شاء الله"},
        ]
    elif tpl == 14:
        msgs = [
            {"role":"user","content":f"هلو، أريد {svc['n']} بس ما أعرف إذا يستاهل التصليح أو أشتري جديد"},
            {"role":"assistant","content":"قولي عمره وشنو المشكلة وأعطيك رأيي"},
            {"role":"user","content":f"عمره {_age} والمشكلة في {_part}"},
            {"role":"assistant","content":f"بعمر {_age} التصليح يستاهل. {_part} بـ{vp(int(svc['p']*0.4))}، الجهاز الجديد بـ{vp(svc['p']*3)}"},
            {"role":"user","content":"صح، صلح الموضوع"},
            {"role":"assistant","content":f"ماشي، نجي {_appt} إن شاء الله"},
        ]
    elif tpl == 15:
        msgs = [
            {"role":"user","content":f"مساء الخير، أريد {svc['n']} للمحل التجاري"},
            {"role":"assistant","content":"للمحلات عندنا سعر خاص"},
            {"role":"user","content":"شكد؟"},
            {"role":"assistant","content":f"{vp(int(svc['p']*0.85))} دينار {_extra}"},
            {"role":"user","content":"ماشي، نريد عقد صيانة"},
            {"role":"assistant","content":f"ممكن، عقد السنة بـ{vp(int(svc['p']*10))} دينار شامل الزيارات الدورية"},
        ]
    elif tpl == 16:
        msgs = [
            {"role":"user","content":f"هلو، لابتوبي {_laptop_prob}، شكد التصليح؟"},
            {"role":"assistant","content":"شنو اللي يصير بالضبط؟"},
            {"role":"user","content":f"{_laptop_prob}"},
            {"role":"assistant","content":f"غالباً المشكلة بـ{_laptop_part}. أجيبه وأشوف"},
            {"role":"user","content":"شكد التصليح؟"},
            {"role":"assistant","content":f"لو {_laptop_part} بـ{vp(svc['p'])} دينار. بعد الفحص نعرف بالضبط"},
        ]
    elif tpl == 17:
        msgs = [
            {"role":"user","content":f"أريد {svc['n']} للبيت كامل {_nrooms}"},
            {"role":"assistant","content":"شنو المطلوب بالضبط؟"},
            {"role":"user","content":f"{_nrooms} وصالة، {pick(['مشكلة قديمة','تجديد كامل','ضرورة عاجلة'])}"},
            {"role":"assistant","content":f"للبيت {_nrooms} حوالي {vp(int(svc['p']*4))} دينار شامل المواد والعمالة"},
            {"role":"user","content":"ومدة التنفيذ؟"},
            {"role":"assistant","content":f"{_days} حسب الحجم"},
        ]
    elif tpl == 18:
        msgs = [
            {"role":"user","content":f"هلو، {svc['n']} عندكم بالأقساط؟"},
            {"role":"assistant","content":"للمشاريع الكبيرة نقدر نقسط. كم يكلف مشروعك؟"},
            {"role":"user","content":f"حوالي {vp(int(svc['p']*8))} دينار"},
            {"role":"assistant","content":f"ماشي، {_disc_pct*5}% مقدم والباقي بعد الانتهاء {_extra}"},
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
            {"role":"user","content":f"هلو، {svc['n']} شنو أوقات الدوام؟"},
            {"role":"assistant","content":f"نشتغل من {pick(['7','8','9'])} الصبح لـ{pick(['7','8','9'])} المساء، 7 أيام"},
            {"role":"user","content":"حتى الجمعة؟"},
            {"role":"assistant","content":"إي، الجمعة بعد الصلاة نشتغل"},
            {"role":"user","content":f"ماشي، {_pay} جاهز"},
            {"role":"assistant","content":"حياك، نتفق على الموعد"},
        ]
    elif tpl == 21:
        msgs = [
            {"role":"user","content":f"هلو، تجون لمنطقة {_city}؟"},
            {"role":"assistant","content":"إي نجي. بس يكون في رسوم تنقل إضافية"},
            {"role":"user","content":"شكد الرسوم؟"},
            {"role":"assistant","content":f"{vp(30000)} دينار إضافية لمنطقة {_city}"},
            {"role":"user","content":"زين، ماشي"},
            {"role":"assistant","content":"ماشي، نتفق على الموعد"},
        ]
    elif tpl == 22:
        msgs = [
            {"role":"user","content":f"هلو، قبل ما تجي لـ{svc['n']}، أريد تقدير بالسعر"},
            {"role":"assistant","content":"ممكن. وصفلي المشكلة بالتفصيل وأعطيك تقدير أولي"},
            {"role":"user","content":f"المشكلة صارت من {_days} و{_prob}"},
            {"role":"assistant","content":f"تقدير أولي بين {vp(svc['p'])} و{vp(int(svc['p']*1.3))} دينار. الدقة بعد المعاينة"},
            {"role":"user","content":"معقول، تعال"},
            {"role":"assistant","content":f"حاضر، {_appt} إن شاء الله"},
        ]
    elif tpl == 23:
        msgs = [
            {"role":"user","content":f"مرحبا، جيت قبل وما حليتوا مشكلة {svc['n']}"},
            {"role":"assistant","content":"آسفين على الإزعاج. شنو المشكلة بالضبط اللي رجعت؟"},
            {"role":"user","content":f"نفس المشكلة رجعت بعد {_days}"},
            {"role":"assistant","content":f"ماشي، نجي مرة ثانية بالمجان. هذا ضمن ضمان {_warrmonth} عندنا"},
            {"role":"user","content":"شكراً على الالتزام"},
            {"role":"assistant","content":f"واجبنا، {_appt} نجي؟"},
        ]
    elif tpl == 24:
        msgs = [
            {"role":"user","content":f"هلو، عندكم خدمة طوارئ لـ{svc['n']}؟"},
            {"role":"assistant","content":"إي، عندنا خدمة طوارئ 24 ساعة"},
            {"role":"user","content":"سعر الطوارئ غالي؟"},
            {"role":"assistant","content":f"زيادة {_disc_pct+10}% على السعر الطبيعي. يعني {vp(int(svc['p']*1.3))} دينار"},
            {"role":"user","content":"ماشي، الوضع ما يحتمل تأخير"},
            {"role":"assistant","content":"حاضر، نجيك خلال ساعة"},
        ]
    elif tpl == 25:
        msgs = [
            {"role":"user","content":f"هلو، أحتاج {svc['n']} اليوم"},
            {"role":"assistant","content":f"تفضل. {svc['f']}. شنو المشكلة؟"},
            {"role":"user","content":f"المشكلة {_prob}، متى تكدر تجي؟"},
            {"role":"assistant","content":f"{_appt} أو وقت آخر يناسبك؟"},
            {"role":"user","content":f"{_appt} أحسن"},
            {"role":"assistant","content":f"ماشي، {_appt}. السعر {vp(svc['p'])} دينار تقريباً"},
        ]
    elif tpl == 26:
        msgs = [
            {"role":"user","content":f"{_gr}، عندي {svc['n']} مشكلة بـ{_part}"},
            {"role":"assistant","content":f"شنو بالضبط يصير بـ{_part}؟"},
            {"role":"user","content":f"من {_days} و{_prob}"},
            {"role":"assistant","content":f"فاهم. {_part} لو تعطل يسوي هذا. نصلحها بـ{vp(svc['p'])} دينار {_extra}"},
            {"role":"user","content":"شوكت تجي؟"},
            {"role":"assistant","content":f"متاح {_appt} إن شاء الله"},
        ]
    elif tpl == 27:
        msgs = [
            {"role":"user","content":f"صباح الخير، أريد {svc['n']} لبيتي بمنطقة {_city}"},
            {"role":"assistant","content":f"صباح النور. منطقة {_city} نغطيها. متى مناسبك؟"},
            {"role":"user","content":f"{_appt} إذا ممكن"},
            {"role":"assistant","content":f"ماشي، {_appt}. السعر تقريباً {vp(svc['p'])} دينار {_extra}"},
            {"role":"user","content":"ممتاز"},
            {"role":"assistant","content":"حاضر، عطني رقمك نتواصل"},
        ]
    elif tpl == 28:
        msgs = [
            {"role":"user","content":f"هلو، عندي {svc['n']} خربان وعندي ضيوف {_appt}"},
            {"role":"assistant","content":"والله وضع طارئ. أجي بأسرع وقت"},
            {"role":"user","content":f"تكدر {_appt} فعلاً؟"},
            {"role":"assistant","content":f"إي، حاضر {_appt}. السعر {vp(svc['p'])} دينار {_extra}"},
            {"role":"user","content":"الله يخليك، شكراً"},
            {"role":"assistant","content":"حاضر، نتصل قبل الوصول"},
        ]
    elif tpl == 29:
        msgs = [
            {"role":"user","content":f"مرحبا، {svc2['n']} و{svc['n']} كلهم يحتاجون تصليح"},
            {"role":"assistant","content":"كلهم معاً؟ شنو المشاكل بكل واحد؟"},
            {"role":"user","content":f"{svc2['n']} {_prob} و{svc['n']} {_prob}"},
            {"role":"assistant","content":f"للاثنين معاً بـ{vp(svc['p'] + svc2['p'])} دينار تقريباً. بعد الكشف نأكد"},
            {"role":"user","content":"وتعطي خصم للاثنين؟"},
            {"role":"assistant","content":f"إي، {_disc_pct}% خصم للاثنين مع بعض"},
        ]
    elif tpl == 30:
        msgs = [
            {"role":"user","content":f"هلو، أبي {_name} يتكلم معكم بخصوص {svc['n']}"},
            {"role":"assistant","content":f"أهلاً، {_name} مرحبا بيك"},
            {"role":"user","content":f"إي هذا {_name}. عندي مشكلة بـ{svc['n']} من {_days}"},
            {"role":"assistant","content":f"فاهمين يا {_name}. نجي نشوف ونحدد السعر"},
            {"role":"user","content":"شكد تقريباً؟"},
            {"role":"assistant","content":f"تقريباً {vp(svc['p'])} دينار {_extra}"},
        ]
    elif tpl == 31:
        msgs = [
            {"role":"user","content":f"هلو، فني {svc['n']} متاح؟"},
            {"role":"assistant","content":"إي، فنيينا متاحين الحين"},
            {"role":"user","content":f"أبي فني يجي لمنطقة {_city}"},
            {"role":"assistant","content":f"ماشي، فني ينطلق {_appt} لمنطقة {_city}"},
            {"role":"user","content":"وشكد؟"},
            {"role":"assistant","content":f"تقريباً {vp(svc['p'])} دينار {_extra}"},
        ]
    elif tpl == 32:
        msgs = [
            {"role":"user","content":f"{_gr}، سمعت عنكم بخصوص {svc['n']}، صحيح؟"},
            {"role":"assistant","content":"إي، متخصصين بهذا المجال من سنين"},
            {"role":"user","content":f"جيد، أبي {svc['n']} بمنطقة {_city}"},
            {"role":"assistant","content":f"منطقة {_city} نغطيها. بـ{vp(svc['p'])} دينار {_extra}"},
            {"role":"user","content":"ماشي، متى أتوقعكم؟"},
            {"role":"assistant","content":f"{_appt} إن شاء الله"},
        ]
    elif tpl == 33:
        msgs = [
            {"role":"user","content":f"هلو، أريد تقييم لـ{svc['n']} بيتي"},
            {"role":"assistant","content":"شنو تريد تشوف بالضبط؟"},
            {"role":"user","content":f"أبي أعرف إذا {svc['n']} بحاجة صيانة"},
            {"role":"assistant","content":f"نجي نكشف. الكشف بـ{vp(int(svc['p']*0.2))} دينار. لو صلحنا يُحسب من التصليح"},
            {"role":"user","content":"زين، هذا عدل"},
            {"role":"assistant","content":f"نترتب الموعد {_appt}؟"},
        ]
    elif tpl == 34:
        msgs = [
            {"role":"user","content":f"مرحبا، شلون تقدر تساعدني بـ{svc['n']}؟"},
            {"role":"assistant","content":f"{svc['f']}. وصفلي المشكلة"},
            {"role":"user","content":f"المشكلة بـ{_area} من {_days}"},
            {"role":"assistant","content":f"فاهمين. تقريباً {vp(svc['p'])} دينار {_extra}"},
            {"role":"user","content":f"{_dr}"},
            {"role":"assistant","content":f"{_dy}"},
        ]
    elif tpl == 35:
        msgs = [
            {"role":"user","content":f"هلو، ثلاجتي {_fridge_prob}، شكد التصليح؟"},
            {"role":"assistant","content":"شنو ماركتها وعمرها؟"},
            {"role":"user","content":f"{_brand}، من {_age}"},
            {"role":"assistant","content":f"غالباً {_part}. بـ{vp(70000)} دينار تقريباً {_extra}"},
            {"role":"user","content":"ماشي، شوكت تجي؟"},
            {"role":"assistant","content":f"{_appt} إن شاء الله"},
        ]
    elif tpl == 36:
        msgs = [
            {"role":"user","content":f"{_gr}، أريد {svc['n']} للمكتب"},
            {"role":"assistant","content":"للمكاتب عندنا باقة خاصة. شكد مكتب؟"},
            {"role":"user","content":f"مكتب {pick(['صغير','متوسط','كبير'])}، {pick(['3','5','8','10'])} موظفين"},
            {"role":"assistant","content":f"باقة المكتب بـ{vp(int(svc['p']*2))} دينار شهرياً {_extra}"},
            {"role":"user","content":"وفي عقد؟"},
            {"role":"assistant","content":"إي، عقد سنوي مع خصم إضافي"},
        ]
    elif tpl == 37:
        msgs = [
            {"role":"user","content":f"هلو، كهربائي تصلح {_elec_prob}؟"},
            {"role":"assistant","content":"إي، هذا تخصصنا. وين المشكلة؟"},
            {"role":"user","content":f"ببيتي بمنطقة {_city}، {_elec_prob}"},
            {"role":"assistant","content":f"ماشي، نجي نكشف. الكشف مجاني. لو التصليح بـ{vp(100000)} دينار تقريباً"},
            {"role":"user","content":"شوكت؟"},
            {"role":"assistant","content":f"{_appt} إن شاء الله"},
        ]
    elif tpl == 38:
        msgs = [
            {"role":"user","content":f"مرحبا، كم تاخذ على {svc['n']} للمشروع الكبير؟"},
            {"role":"assistant","content":"للمشاريع الكبيرة سعرنا خاص. شكد حجم المشروع؟"},
            {"role":"user","content":f"مشروع {pick(['متوسط','كبير','ضخم'])}، حوالي {pick([10,20,50])} وحدة"},
            {"role":"assistant","content":f"للمشاريع الكبيرة خصم {_disc_pct}%، يعني {vp(int(svc['p']*0.9))} دينار للوحدة"},
            {"role":"user","content":"معقول، نتفاهم أكثر"},
            {"role":"assistant","content":"حياك، نتفق على موعد اجتماع"},
        ]
    elif tpl == 39:
        msgs = [
            {"role":"user","content":f"هلو، عندي {svc['n']} من ماركة {_brand}، شكد الصيانة السنوية؟"},
            {"role":"assistant","content":"صيانة دورية مهمة. عندنا باقة سنوية"},
            {"role":"user","content":"شكد باقة السنة؟"},
            {"role":"assistant","content":f"باقة السنة بـ{vp(int(svc['p']*8))} دينار، تشمل {pick(['3','4','6'])} زيارات"},
            {"role":"user","content":"ويشمل القطع؟"},
            {"role":"assistant","content":"الزيارات والعمالة مشمولة، القطع بحسب السعر"},
        ]
    elif tpl == 40:
        msgs = [
            {"role":"user","content":f"صباح الخير، عندكم تصليح {svc['n']} ماركة {_brand}؟"},
            {"role":"assistant","content":f"صباح النور. نصلح {_brand} وكل الماركات"},
            {"role":"user","content":f"جيد، عندي مشكلة بـ{_part}"},
            {"role":"assistant","content":f"{_part} في {_brand} شيء شائع. بـ{vp(svc['p'])} دينار {_extra}"},
            {"role":"user","content":"وفي ضمان؟"},
            {"role":"assistant","content":f"إي، ضمان {_warrmonth}"},
        ]
    elif tpl == 41:
        msgs = [
            {"role":"user","content":f"هلو، أريد مقارنة سعر {svc['n']} عندكم بالسوق"},
            {"role":"assistant","content":"سعرنا تنافسي جداً. شنو سعر السوق اللي شفته؟"},
            {"role":"user","content":f"شفت بـ{vp(int(svc['p']*1.2))} دينار"},
            {"role":"assistant","content":f"عندنا بـ{vp(svc['p'])} دينار {_extra}. فرق {_disc_pct}% لصالحك"},
            {"role":"user","content":"تمام، عندكم أرخص"},
            {"role":"assistant","content":"إي، وجودة أحسن. متى نجي؟"},
        ]
    elif tpl == 42:
        msgs = [
            {"role":"user","content":f"{_gr}، أريد {svc['n']} بس أنا بمنطقة {_city}"},
            {"role":"assistant","content":f"منطقة {_city} مغطاة عندنا"},
            {"role":"user","content":"كم يكلف التنقل؟"},
            {"role":"assistant","content":f"التنقل لـ{_city} مجاني ضمن بغداد"},
            {"role":"user","content":"ممتاز، شكر"},
            {"role":"assistant","content":f"حاضر، {_appt} إن شاء الله"},
        ]
    elif tpl == 43:
        msgs = [
            {"role":"user","content":f"مرحبا، عندكم خدمة توصيل القطع الغيار لـ{svc['n']}؟"},
            {"role":"assistant","content":"إي، نجيب القطع ونركبها عندك"},
            {"role":"user","content":f"أريد قطعة {_part} لماركة {_brand}"},
            {"role":"assistant","content":f"القطعة الأصل بـ{vp(int(svc['p']*0.5))} دينار، نجيبها خلال {_days}"},
            {"role":"user","content":"والتركيب؟"},
            {"role":"assistant","content":f"التركيب بـ{vp(int(svc['p']*0.3))} دينار إضافية"},
        ]
    elif tpl == 44:
        msgs = [
            {"role":"user","content":f"هلو، {_name} أنا، اتصلت أمس بخصوص {svc['n']}"},
            {"role":"assistant","content":f"أهلاً {_name}، ذاكرين. شنو القرار؟"},
            {"role":"user","content":"قررت أصلح"},
            {"role":"assistant","content":f"ممتاز. نجي {_appt}؟ السعر {vp(svc['p'])} دينار {_extra}"},
            {"role":"user","content":"إي، ماشي"},
            {"role":"assistant","content":f"حاضر يا {_name}، نتصل قبل الوصول"},
        ]
    elif tpl == 45:
        msgs = [
            {"role":"user","content":f"هلو، {svc['n']} خربانة من {_days} وما تشتغل، طوارئ"},
            {"role":"assistant","content":"واضح إنه طارئ. وين منطقتك؟"},
            {"role":"user","content":f"منطقة {_city}"},
            {"role":"assistant","content":f"ماشي، فني ينطلق الحين. رسوم الطوارئ {vp(int(svc['p']*1.25))} دينار"},
            {"role":"user","content":"ماشي، فدوة السرعة"},
            {"role":"assistant","content":"حاضر، يوصل خلال ساعة"},
        ]
    elif tpl == 46:
        msgs = [
            {"role":"user","content":f"مرحبا، عندي {svc['n']} اشتريته من {_age} وما صلحته قط"},
            {"role":"assistant","content":"يحتاج فحص دوري. شنو حالته؟"},
            {"role":"user","content":f"يشتغل بس {_prob} أحياناً"},
            {"role":"assistant","content":f"هذا يدل على {_part} يحتاج صيانة. قبل ما يتعطل كامل نصلحه بـ{vp(int(svc['p']*0.6))} دينار"},
            {"role":"user","content":"ماشي، أحسن قبل ما يتكسر"},
            {"role":"assistant","content":f"صح. {_appt} نجي"},
        ]
    elif tpl == 47:
        msgs = [
            {"role":"user","content":f"هلو، أريد فاتورة رسمية لـ{svc['n']}"},
            {"role":"assistant","content":"إي، نقدر نصدر فاتورة رسمية"},
            {"role":"user","content":"وهل تقبلون بطاقة؟"},
            {"role":"assistant","content":f"إي، {_pay} كله مقبول عندنا"},
            {"role":"user","content":"ممتاز، شكراً"},
            {"role":"assistant","content":f"حاضر. السعر {vp(svc['p'])} دينار {_extra}"},
        ]
    elif tpl == 48:
        msgs = [
            {"role":"user","content":f"{_gr}، أريد تنظيف وصيانة {svc['n']}"},
            {"role":"assistant","content":"صيانة وقائية ممتازة. شنو الجهاز؟"},
            {"role":"user","content":f"{svc['n']} ماركة {_brand}"},
            {"role":"assistant","content":f"تنظيف وصيانة {_brand} بـ{vp(int(svc['p']*0.5))} دينار {_extra}"},
            {"role":"user","content":"شكد تاخذ؟"},
            {"role":"assistant","content":f"{_install_time} وخلاص"},
        ]
    elif tpl == 49:
        msgs = [
            {"role":"user","content":f"مرحبا، عندكم خبرة بـ{svc['n']} ماركة {_brand}؟"},
            {"role":"assistant","content":f"إي، {_brand} شيء شائع عندنا. فنيينا متخصصين"},
            {"role":"user","content":"كم سنة خبرة؟"},
            {"role":"assistant","content":f"أكثر من {pick(['5','7','10','12'])} سنين بهذا المجال"},
            {"role":"user","content":"عدل، أجيكم"},
            {"role":"assistant","content":f"حياك. السعر {vp(svc['p'])} دينار {_extra}"},
        ]
    elif tpl == 50:
        msgs = [
            {"role":"user","content":f"هلو، أريد {svc['n']} لكن بميزانية محدودة"},
            {"role":"assistant","content":"شكد ميزانيتك؟"},
            {"role":"user","content":f"حوالي {vp(int(svc['p']*0.7))} دينار"},
            {"role":"assistant","content":"ماشي، نشوف شلون نضبط الشغل بهذي الميزانية"},
            {"role":"user","content":"شكراً على الفهم"},
            {"role":"assistant","content":f"أهل وسهل. {_appt} نجي نكشف أول"},
        ]
    elif tpl == 51:
        msgs = [
            {"role":"user","content":f"{_gr}، عندي ضيف ويحتاج {svc['n']} بسرعة"},
            {"role":"assistant","content":"حاضر، هذا طارئ. وين المكان؟"},
            {"role":"user","content":f"بمنطقة {_city}"},
            {"role":"assistant","content":f"فني ينطلق {_appt} لـ{_city}. بـ{vp(svc['p'])} دينار {_extra}"},
            {"role":"user","content":"الله يخليك"},
            {"role":"assistant","content":"واجبنا، نتصل عند الوصول"},
        ]
    elif tpl == 52:
        msgs = [
            {"role":"user","content":f"هلو، قرأت تقييماتكم بخصوص {svc['n']}، زينة"},
            {"role":"assistant","content":"شكراً، نحاول دايم نكون الأحسن"},
            {"role":"user","content":f"أريد {svc['n']} لبيتي بمنطقة {_city}"},
            {"role":"assistant","content":f"ممتاز، {_city} مغطاة. بـ{vp(svc['p'])} دينار {_extra}"},
            {"role":"user","content":"ماشي، متى؟"},
            {"role":"assistant","content":f"{_appt} إن شاء الله"},
        ]
    elif tpl == 53:
        msgs = [
            {"role":"user","content":f"مرحبا، صاحبي نصحني بكم لـ{svc['n']}"},
            {"role":"assistant","content":"أهلاً، يحيي صاحبك على الثقة"},
            {"role":"user","content":"إي، قال سعركم منطقي وشغلكم زين"},
            {"role":"assistant","content":f"نحاول. {svc['n']} بـ{vp(svc['p'])} دينار {_extra}"},
            {"role":"user","content":"زين، نترتب موعد"},
            {"role":"assistant","content":f"{_appt} يناسبك؟"},
        ]
    elif tpl == 54:
        msgs = [
            {"role":"user","content":f"هلو، ما أعرف شكد يكلف {svc['n']}، أول مرة أطلب"},
            {"role":"assistant","content":"لا تحتار، نساعدك. شنو المشكلة بالضبط؟"},
            {"role":"user","content":f"الجهاز {_prob} من {_days}"},
            {"role":"assistant","content":f"هذا شيء عادي نصلحه. تقريباً {vp(svc['p'])} دينار {_extra}"},
            {"role":"user","content":"جيد، ما توقعت هالسعر"},
            {"role":"assistant","content":"سعرنا عدل. متى نجي؟"},
        ]
    elif tpl == 55:
        msgs = [
            {"role":"user","content":f"هلو، عندي {svc['n']} وأريد أبيعه بس خايف من مشاكل"},
            {"role":"assistant","content":"أحسن تفحصه أول قبل البيع"},
            {"role":"user","content":"كم يكلف الفحص؟"},
            {"role":"assistant","content":f"الفحص بـ{vp(int(svc['p']*0.15))} دينار، ونعطيك تقرير"},
            {"role":"user","content":"وإذا احتاج تصليح؟"},
            {"role":"assistant","content":f"التصليح بـ{vp(svc['p'])} دينار، الفحص يُحسب منها"},
        ]
    elif tpl == 56:
        msgs = [
            {"role":"user","content":f"{_gr}، شنو الفرق بين {svc['n']} الجديد والقديم؟"},
            {"role":"assistant","content":"الجديد أوفر كهرباء وأطول عمر، القديم تصليحه أرخص"},
            {"role":"user","content":f"عمر جهازي {_age}، يستاهل التصليح؟"},
            {"role":"assistant","content":f"بعمر {_age} التصليح يستاهل. نصلحه بـ{vp(svc['p'])} دينار {_extra}"},
            {"role":"user","content":"ماشي، صلحه"},
            {"role":"assistant","content":f"حاضر، {_appt} نجي"},
        ]
    elif tpl == 57:
        msgs = [
            {"role":"user","content":f"مرحبا، أريد {svc['n']} لأول مرة بحياتي"},
            {"role":"assistant","content":"أهلاً، نساعدك خطوة خطوة"},
            {"role":"user","content":"شنو أحتاج أجهز؟"},
            {"role":"assistant","content":f"بس تكون موجود بالبيت. نجيب كل شيء {_extra}"},
            {"role":"user","content":"ممتاز، متى؟"},
            {"role":"assistant","content":f"{_appt} إن شاء الله، بـ{vp(svc['p'])} دينار"},
        ]
    elif tpl == 58:
        msgs = [
            {"role":"user","content":f"هلو، {svc['n']} لمحلي خربت قبل العيد"},
            {"role":"assistant","content":"والله وضع صعب. نعطيك أولوية"},
            {"role":"user","content":"شكد يكلف بالأولوية؟"},
            {"role":"assistant","content":f"إضافة {_disc_pct}% على السعر الأصلي. بـ{vp(int(svc['p']*1.15))} دينار"},
            {"role":"user","content":"ماشي، المحل أهم"},
            {"role":"assistant","content":f"فني يطلع {_appt} إن شاء الله"},
        ]
    elif tpl == 59:
        msgs = [
            {"role":"user","content":f"{_gr}، هل تقدر تدرب عمالي على {svc['n']}؟"},
            {"role":"assistant","content":"إي، عندنا خدمة تدريب للعمالة"},
            {"role":"user","content":"شكد كلفة التدريب؟"},
            {"role":"assistant","content":f"تدريب {pick(['يوم','يومين','أسبوع'])} بـ{vp(int(svc['p']*3))} دينار"},
            {"role":"user","content":"وشهادة؟"},
            {"role":"assistant","content":"إي، شهادة حضور رسمية"},
        ]
    elif tpl == 60:
        msgs = [
            {"role":"user","content":f"مرحبا، عندي {svc['n']} خربان وما عندي وقت أنتظر"},
            {"role":"assistant","content":"نفهم وضعك. عندنا خدمة سريعة"},
            {"role":"user","content":"كم تاخذ للخدمة السريعة؟"},
            {"role":"assistant","content":f"الخدمة السريعة بـ{vp(int(svc['p']*1.2))} دينار {_extra}"},
            {"role":"user","content":"ماشي، أهم شيء ينتهي بسرعة"},
            {"role":"assistant","content":f"حاضر، {_appt} أكيد"},
        ]
    elif tpl == 61:
        msgs = [
            {"role":"user","content":f"هلو، شنو رأيكم بـ{svc['n']} ماركة {_brand}؟"},
            {"role":"assistant","content":f"{_brand} ماركة كويسة. متينة وقطعها موجودة"},
            {"role":"user","content":"وإذا تعطلت، شكد التصليح؟"},
            {"role":"assistant","content":f"تعتمد على المشكلة. في المعدل {vp(svc['p'])} دينار {_extra}"},
            {"role":"user","content":"منطقي، شكراً"},
            {"role":"assistant","content":"أي وقت تحتاج نحن موجودين"},
        ]
    elif tpl == 62:
        msgs = [
            {"role":"user","content":f"{_gr}، عندي {svc['n']} بس بالتقسيط، هل ممكن؟"},
            {"role":"assistant","content":"إي، نقدر نرتب تقسيط للمبالغ الكبيرة"},
            {"role":"user","content":f"المبلغ حوالي {vp(int(svc['p']*5))} دينار"},
            {"role":"assistant","content":f"ماشي، {_disc_pct*5}% مقدم والباقي {pick(['3','6'])} أقساط شهرية"},
            {"role":"user","content":"متفق"},
            {"role":"assistant","content":"نرتب موعد للمعاينة أولاً"},
        ]
    elif tpl == 63:
        msgs = [
            {"role":"user","content":"مرحبا، عندكم برنامج ولاء للزبائن؟"},
            {"role":"assistant","content":"إي، عندنا بطاقة زبون دائم"},
            {"role":"user","content":"شنو المزايا؟"},
            {"role":"assistant","content":f"خصم {_disc_pct}% على كل خدمة، وأولوية بالمواعيد"},
            {"role":"user","content":"ممتاز، أشترك"},
            {"role":"assistant","content":f"البطاقة بـ{vp(50000)} دينار سنوياً، توفر عليك أكثر"},
        ]
    elif tpl == 64:
        msgs = [
            {"role":"user","content":f"هلو، لازم أعيّر {svc['n']} الحين"},
            {"role":"assistant","content":"شنو المشكلة؟"},
            {"role":"user","content":f"{svc['n']} {_prob} فجأة"},
            {"role":"assistant","content":f"فني يطلع {_appt}. السعر {vp(svc['p'])} دينار {_extra}"},
            {"role":"user","content":"شكراً على السرعة"},
            {"role":"assistant","content":"حاضر، نتصل قبل الوصول"},
        ]
    elif tpl == 65:
        msgs = [
            {"role":"user","content":f"{_gr}، عندكم تأمين على الشغل؟"},
            {"role":"assistant","content":"إي، مؤمنون ومرخصون"},
            {"role":"user","content":"يعني لو صار ضرر من شغلكم؟"},
            {"role":"assistant","content":"نتحمل المسؤولية الكاملة، مؤمن على كل شيء"},
            {"role":"user","content":"هذا مهم والله"},
            {"role":"assistant","content":f"بنشتغل بأمان. السعر {vp(svc['p'])} دينار {_extra}"},
        ]
    elif tpl == 66:
        msgs = [
            {"role":"user","content":f"مرحبا، شنو أحسن وقت لـ{svc['n']}؟"},
            {"role":"assistant","content":"أحسن وقت الصبح لأن الجو أبرد"},
            {"role":"user","content":f"ماشي، متاح {_time}؟"},
            {"role":"assistant","content":f"إي، {_time} ممتاز. نرتب موعد؟"},
            {"role":"user","content":"إي"},
            {"role":"assistant","content":f"حاضر، {_time}. السعر {vp(svc['p'])} دينار"},
        ]
    elif tpl == 67:
        msgs = [
            {"role":"user","content":f"هلو، عندي {svc['n']} و{svc2['n']} يحتاجون صيانة"},
            {"role":"assistant","content":"للاثنين معاً عندنا سعر خاص"},
            {"role":"user","content":"شكد الخصم؟"},
            {"role":"assistant","content":f"خصم {_disc_pct}% للاثنين. إجمالي {vp(int((svc['p']+svc2['p'])*0.9))} دينار {_extra}"},
            {"role":"user","content":"ماشي، متفق"},
            {"role":"assistant","content":f"{_appt} نجي للاثنين"},
        ]
    elif tpl == 68:
        msgs = [
            {"role":"user","content":f"{_gr}، أريد رأيكم بـ{svc['n']} قبل أشتري"},
            {"role":"assistant","content":"أهلاً، نساعدك تختار الأنسب"},
            {"role":"user","content":f"بين {_brand} و{pick(['LG','ميديا','توشيبا','شارپ'])}، أيهم أحسن؟"},
            {"role":"assistant","content":f"{_brand} أفضل للاستخدام المنزلي. قطعها موفرة وصيانتها أرخص"},
            {"role":"user","content":f"شكراً، راح آخذ {_brand}"},
            {"role":"assistant","content":"خيار موفق، أي وقت تحتاج صيانة نحن موجودين"},
        ]
    elif tpl == 69:
        msgs = [
            {"role":"user","content":f"مرحبا، عندي {svc['n']} محتاج نظافة بس ما ينكسر"},
            {"role":"assistant","content":"تنظيف دوري مهم جداً"},
            {"role":"user","content":"كم يكلف التنظيف فقط؟"},
            {"role":"assistant","content":f"تنظيف {svc['n']} بـ{vp(int(svc['p']*0.3))} دينار {_extra}"},
            {"role":"user","content":f"{_appt} يناسبك؟"},
            {"role":"assistant","content":f"إي، {_appt} حاضر"},
        ]
    elif tpl == 70:
        msgs = [
            {"role":"user","content":f"هلو، {_name} أنا، سألت بالهاتف أمس عن {svc['n']}"},
            {"role":"assistant","content":f"أهلاً {_name}، ذاكرين استفسارك"},
            {"role":"user","content":"قررت أتفق. السعر كان كذا صح؟"},
            {"role":"assistant","content":f"إي صح، {vp(svc['p'])} دينار {_extra}"},
            {"role":"user","content":"ماشي، متفق"},
            {"role":"assistant","content":f"ممتاز يا {_name}، {_appt} نجيك"},
        ]
    elif tpl == 71:
        msgs = [
            {"role":"user","content":f"{_gr}، أريد استشارة مجانية عن {svc['n']}"},
            {"role":"assistant","content":"حياك، الاستشارة مجانية دايم عندنا"},
            {"role":"user","content":f"جهازي {_prob} من {_days}، شنو تتوقع؟"},
            {"role":"assistant","content":f"هذا غالباً {_part}. بس لازم كشف مباشر نأكد"},
            {"role":"user","content":"شكد لو احتاج تصليح؟"},
            {"role":"assistant","content":f"تقريباً {vp(svc['p'])} دينار {_extra}"},
        ]
    elif tpl == 72:
        msgs = [
            {"role":"user","content":f"مرحبا، شلون أصون {svc['n']} ماركة {_brand}؟"},
            {"role":"assistant","content":"أحسن صيانة هي الدورية"},
            {"role":"user","content":"شكد مرة بالسنة؟"},
            {"role":"assistant","content":f"مرتين بالسنة أفضل. كل صيانة بـ{vp(int(svc['p']*0.4))} دينار {_extra}"},
            {"role":"user","content":"ماشي، نرتب"},
            {"role":"assistant","content":"نضيفك لجدول صيانتنا الدوري"},
        ]
    elif tpl == 73:
        msgs = [
            {"role":"user","content":f"هلو، {svc['n']} لو اشتريت من عندكم، هل تركبونه؟"},
            {"role":"assistant","content":"إي، بيع وتركيب مع بعض"},
            {"role":"user","content":"وشكد؟"},
            {"role":"assistant","content":f"جهاز {_brand} جديد مع التركيب بـ{vp(int(svc['p']*5))} دينار {_extra}"},
            {"role":"user","content":"ويشمل ضمان؟"},
            {"role":"assistant","content":f"ضمان {_warrmonth} على الجهاز والتركيب"},
        ]
    elif tpl == 74:
        msgs = [
            {"role":"user","content":f"{_gr}، أريد {svc['n']} بس أبي الفني ماهر"},
            {"role":"assistant","content":"نفهم القلق. فنيينا كلهم مدربين ومعتمدين"},
            {"role":"user","content":"شكد خبرتهم؟"},
            {"role":"assistant","content":f"أقلهم {pick(['3','5','7'])} سنين خبرة"},
            {"role":"user","content":"ممتاز، هذا يطمن"},
            {"role":"assistant","content":f"اطمن. السعر {vp(svc['p'])} دينار {_extra}"},
        ]
    elif tpl == 75:
        msgs = [
            {"role":"user","content":f"مرحبا، أريد {svc['n']} بس أنا مشغول طول اليوم"},
            {"role":"assistant","content":"عندنا مواعيد مساء"},
            {"role":"user","content":"حتى الساعة كم؟"},
            {"role":"assistant","content":f"حتى الساعة {pick(['8','9','10'])} مساء"},
            {"role":"user","content":"ممتاز، نتفق على مساء"},
            {"role":"assistant","content":f"حاضر، {_time}. السعر {vp(svc['p'])} دينار {_extra}"},
        ]
    elif tpl == 76:
        msgs = [
            {"role":"user","content":f"هلو، {svc['n']} يصدر صوت غريب من {_days}"},
            {"role":"assistant","content":"شنو نوع الصوت؟ طقطقة أو هزهزة؟"},
            {"role":"user","content":f"{pick(['طقطقة','هزهزة','صفير','ضجيج'])}"},
            {"role":"assistant","content":f"هذا الصوت يدل على {_part} محتاج صيانة. بـ{vp(svc['p'])} دينار {_extra}"},
            {"role":"user","content":"متى تجي؟"},
            {"role":"assistant","content":f"{_appt} إن شاء الله"},
        ]
    elif tpl == 77:
        msgs = [
            {"role":"user","content":f"{_gr}، شنو الفرق بين {svc['n']} الأرخص والأغلى عندكم؟"},
            {"role":"assistant","content":"الفرق بالجودة والضمان"},
            {"role":"user","content":"وأيهم تنصح فيه؟"},
            {"role":"assistant","content":f"للاستخدام الاعتيادي، النوع بـ{vp(svc['p'])} كافي {_extra}"},
            {"role":"user","content":"ماشي، هذا ياخذ"},
            {"role":"assistant","content":f"خيار زين. {_appt} نجي"},
        ]
    elif tpl == 78:
        msgs = [
            {"role":"user","content":f"مرحبا، {svc['n']} بمنطقة {_city2} تغطون؟"},
            {"role":"assistant","content":f"إي، نغطي {_city2} وكل محافظات العراق"},
            {"role":"user","content":"والسعر نفسه؟"},
            {"role":"assistant","content":f"بغداد والضواحي نفس السعر. {_city2} قد يكون فيه رسوم تنقل صغيرة"},
            {"role":"user","content":"كم الرسوم؟"},
            {"role":"assistant","content":f"تقريباً {vp(20000)} دينار إضافية"},
        ]
    elif tpl == 79:
        msgs = [
            {"role":"user","content":f"هلو، {svc['n']} موسمي لازم أصلح قبل الصيف"},
            {"role":"assistant","content":"صح، أحسن تصلح قبل الموسم"},
            {"role":"user","content":"شكد وشوكت تكدر تجي؟"},
            {"role":"assistant","content":f"بـ{vp(svc['p'])} دينار {_extra}. {_appt} ماشي؟"},
            {"role":"user","content":"إي، متفق"},
            {"role":"assistant","content":"حاضر، الموسم قادم"},
        ]
    else:
        msgs = [
            {"role":"user","content":f"{_gr}، أريد {svc['n']} لبيتي"},
            {"role":"assistant","content":f"{svc['f']}. شنو المشكلة بالتفصيل؟"},
            {"role":"user","content":f"{svc['n']} {_prob} من {_days}"},
            {"role":"assistant","content":f"مفهوم. السعر {vp(svc['p'])} دينار {_extra}"},
            {"role":"user","content":f"{_dr}"},
            {"role":"assistant","content":f"{_dy}. {_appt} نجيك"},
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
_HOME_WORDS    = HOME_WORDS

_DAILY_FOODS  = ["دولمة","كباب","مسگوف","قيمة","باچة","تشريب","مرق دجاج","رز+مرق","بريانية","فطيرة"]
_DAILY_PLACES = ["سوق شورجة","كورنيش أبو نواس","شارع المتنبي","حديقة الزوراء","سوق العلاوي","منطقة الكرادة"]

def gen_daily(i):
    _dfood   = pick(_DAILY_FOODS)
    _dfood2  = pick(_DAILY_FOODS)
    _dplace  = pick(_DAILY_PLACES)
    _dplace2 = pick(_DAILY_PLACES)
    _dname   = pick(_MALE_NAMES_S + _FEMALE_NAMES_S)
    _dname2  = pick(_MALE_NAMES_S + _FEMALE_NAMES_S)
    _prov    = pick(_cat("المحافظات العراقية") or ["بغداد","البصرة","النجف","كربلاء"])
    _pfood   = pick(_cat("الأكلات الشعبية العراقية") or ["مسگوف","پاچة","دولمة"])
    _iplace  = pick(_cat("المدن والأماكن العراقية") or ["شارع المتنبي","كورنيش أبو نواس"])
    _hw      = pick(_HOME_WORDS) if _HOME_WORDS else "مولد"
    _ww      = pick(_WORK_WORDS) if _WORK_WORDS else "شغل"
    _sw      = pick(_STUDY_WORDS) if _STUDY_WORDS else "امتحان"
    _tw      = pick(_TRANS_WORDS) if _TRANS_WORDS else "سيارة"
    _fw      = pick(_FOOD_WORDS) if _FOOD_WORDS else "أكلة"
    _hltw   = pick(_HEALTH_WORDS) if _HEALTH_WORDS else "وجع"
    _em      = pick(EMOTIONS) if EMOTIONS else "فرحان"
    _yw      = pick(YOUTH_WORDS) if YOUTH_WORDS else "كفو"
    _job     = pick(_JOBS_S)
    _agree   = pick(_AGREE)
    _gr      = pick(_GREET_DAILY)
    _rg      = pick(_REPLY_GOOD)
    _num     = random.randint(1, 999)
    _num2    = random.randint(1, 50)
    _num3    = random.randint(100, 900) * 1000
    tpl = random.randint(1, 80)

    if tpl == 1:
        msgs = [{"role":"user","content":f"{_gr}، شنو طبخت اليوم؟"},{"role":"assistant","content":f"{_rg}. طبخت {_pfood}. وأنت {_dname}؟"},{"role":"user","content":f"طبخت {_dfood}، تعال تاكل"},{"role":"assistant","content":f"والله؟ {_pfood} وإلا {_dfood}؟ يلا جاي"},{"role":"user","content":"تعال هسه، الأكل جاهز"},{"role":"assistant","content":"الله يخليكم، بالطريق"}]
    elif tpl == 2:
        msgs = [{"role":"user","content":f"الكهرباء اليوم كلش مو زينة، الـ{_hw} عندنا عطلان"},{"role":"assistant","content":f"إي والله، من الصبح ما اجه. الـ{_hw} عطلان ليش؟"},{"role":"user","content":"ما أدري، فجأة وقف"},{"role":"assistant","content":f"روح لأبو رياض قرب {_dplace}، يصلح {_hw} بنص ساعة"},{"role":"user","content":"شكد يكلف؟"},{"role":"assistant","content":f"حوالي {random.randint(10,30)*1000:,} دينار"}]
    elif tpl == 3:
        msgs = [{"role":"user","content":f"المنتخب العراقي كسر الخاطر بالأمس، {_dname}"},{"role":"assistant","content":"والله شفت، الفريق ما لعب زين"},{"role":"user","content":"المدرب لازم يغير التشكيلة"},{"role":"assistant","content":f"صح، والجو بـ{_prov} حار يأثر على اللاعبين"},{"role":"user","content":"صح، المباراة القادمة إن شاء الله أحسن"},{"role":"assistant","content":"إن شاء الله، ربي يوفقهم"}]
    elif tpl == 4:
        msgs = [{"role":"user","content":f"ولدي رسب بالـ{_sw}، مو عارف شسوي {_dname}"},{"role":"assistant","content":"كلش انصدمت! شنو صار؟"},{"role":"user","content":f"انشغل بالجيمز وما ذاكر {_sw} كافي"},{"role":"assistant","content":"لازم تأخذ منه الموبايل وقت المذاكرة"},{"role":"user","content":"وإذا ما قبل؟"},{"role":"assistant","content":"أعطيه مكافأة لو نجح، هذا يحمسه أكثر"}]
    elif tpl == 5:
        msgs = [{"role":"user","content":f"الحر هالسنة مو طبيعي، حتى بـ{_prov}"},{"role":"assistant","content":f"إي والله، {_agree}. 50 درجة هالأيام"},{"role":"user","content":"والكهرباء مو موجودة"},{"role":"assistant","content":"والله الحكومة لازم تحل هالمشكلة قبل الصيف"},{"role":"user","content":"كل سنة نفس الكلام"},{"role":"assistant","content":"ربي يفرجها، الوضع صعب على الكل"}]
    elif tpl == 6:
        msgs = [{"role":"user","content":f"وين أحسن مطعم {_pfood} ببغداد؟"},{"role":"assistant","content":f"قرب {_iplace}، أكله طازج وسعره معقول"},{"role":"user","content":"شكد الأكل لشخصين؟"},{"role":"assistant","content":f"حوالي {random.randint(15,40)*1000:,} دينار"},{"role":"user","content":"تعزمني اليوم؟"},{"role":"assistant","content":"إي ماشي، ساعة 7 المسا"}]
    elif tpl == 7:
        msgs = [{"role":"user","content":f"أريد أسافر من {_prov} على إسطنبول، شتشوف؟"},{"role":"assistant","content":"إسطنبول ممتازة، طعام حلو وأسعار معقولة"},{"role":"user","content":"الطيران شكد من بغداد؟"},{"role":"assistant","content":f"حوالي {random.randint(200,450)*1000:,} دينار ذهاب وإياب"},{"role":"user","content":"فكرة زينة"},{"role":"assistant","content":"روح وانبسط، تستاهل"}]
    elif tpl == 8:
        msgs = [{"role":"user","content":f"شلون أوصل من {_dplace} للمطار؟"},{"role":"assistant","content":"تاكسي مباشرة أحسن"},{"role":"user","content":"شكد الأجرة؟"},{"role":"assistant","content":f"حوالي {random.randint(12,25)*1000:,} دينار"},{"role":"user","content":"أو تطبيق؟"},{"role":"assistant","content":"كرنلجي أو زاجل، يوصلونك بأمان وأحياناً أرخص"}]
    elif tpl == 9:
        msgs = [{"role":"user","content":f"وين أحسن دكتور أطفال قرب {_iplace}؟"},{"role":"assistant","content":"دكتور حسن الخفاجي، أفضل طفلية بالمنطقة"},{"role":"user","content":"ساعات الدوام؟"},{"role":"assistant","content":"من 5 لـ9 المسا"},{"role":"user","content":"الكشف بيش؟"},{"role":"assistant","content":f"{random.randint(20,40)*1000:,} دينار"}]
    elif tpl == 10:
        msgs = [{"role":"user","content":f"الـ{_ww} ما يكفي هالأيام، {_dname}"},{"role":"assistant","content":f"صدگ، كل شي غالي. وأنت {_dname2}؟"},{"role":"user","content":f"أفكر أشتغل شغلة {_job} ثانية"},{"role":"assistant","content":f"{_job} فري لانس فكرة ممتازة"},{"role":"user","content":"من وين أبدأ؟"},{"role":"assistant","content":"من الإنترنت وشبكة معارفك"}]
    elif tpl == 11:
        med_specialty = pick(["طب","هندسة","قانون","صيدلة","أسنان","محاسبة"])
        msgs = [{"role":"user","content":f"ابني {_dname} يريد يدرس {med_specialty} بـ{_prov}، شنو رأيك؟"},{"role":"assistant","content":f"{med_specialty} مستقبله زين بس صعب وطويل"},{"role":"user","content":"شكد سنين؟"},{"role":"assistant","content":f"بين {random.randint(3,6)} لـ{random.randint(7,8)} سنين"},{"role":"user","content":"يستاهل؟"},{"role":"assistant","content":"إذا هو راغب وذكي، يستاهل والله"}]
    elif tpl == 12:
        cook_tip = pick(["الملح أول","اشوي على نار هادية","اضيف بهارات عراقية","استخدم سمن بلدي"])
        msgs = [{"role":"user","content":f"شلون أطبخ {_pfood}؟ أول مرة أحاول بـ{_dplace}"},{"role":"assistant","content":f"{_pfood} يحتاج صبر بس ممكن"},{"role":"user","content":"أول شي شسوي؟"},{"role":"assistant","content":f"المكونات أول، و{cook_tip}"},{"role":"user","content":"شكراً على النصيحة"},{"role":"assistant","content":"بالتوفيق، إن شاء الله يطلع ممتاز"}]
    elif tpl == 13:
        msgs = [{"role":"user","content":f"عندكم تجمعات شباب بـ{_dplace}؟"},{"role":"assistant","content":"إي، كل جمعة لقاء بالمسجد"},{"role":"user","content":"وملعب كرة؟"},{"role":"assistant","content":f"إي، قرب {_iplace}، الشباب يلعبون كل عصر"},{"role":"user","content":"أجي معاهم؟"},{"role":"assistant","content":"أكيد، كلهم أهل طيبين"}]
    elif tpl == 14:
        msgs = [{"role":"user","content":f"وين أشتري بذور للحديقة؟ أنا من {_prov}"},{"role":"assistant","content":"سوق الشورجة ببغداد فيه كل شي"},{"role":"user","content":"ما أكو أقرب؟"},{"role":"assistant","content":f"في محل زراعة قرب {_dplace}"},{"role":"user","content":"شكراً"},{"role":"assistant","content":"الله يوفقك"}]
    elif tpl == 15:
        water_days = random.randint(1, 7)
        tanker_cost = random.randint(10, 40) * 1000
        msgs = [{"role":"user","content":f"الماء مقطوع من {water_days} أيام عندنا بـ{_dplace}"},{"role":"assistant","content":"اتصل ببلدية المنطقة وبلّغ"},{"role":"user","content":"بلغت بس ما ردوا"},{"role":"assistant","content":"جلب صهريج مؤقتاً، يكلف تقريباً {tanker_cost:,}"},{"role":"user","content":"وين البلدية؟"},{"role":"assistant","content":f"قرب {_dplace2}، اسأل عن قسم الماء"}]
    elif tpl == 16:
        series_genre = pick(["كوميدي","دراما","رومانسي","تاريخي","اجتماعي"])
        series_list = pick(["ذيب وذيب","خالي الروح","عمر وسلمى","ولد أبوي","العراقية"])
        msgs = [{"role":"user","content":f"أنصحني بمسلسل عراقي {series_genre} حلو، {_dname}"},{"role":"assistant","content":f"شفت {series_list}؟ {series_genre} وحلو"},{"role":"user","content":"شفته. أريد جديد"},{"role":"assistant","content":f"في مسلسلات جديدة على يوتيوب، {_yw}"},{"role":"user","content":"شكراً، أشوفه الليلة"},{"role":"assistant","content":"انبسط، هههه"}]
    elif tpl == 17:
        msgs = [{"role":"user","content":f"أريد أتعلم إنگليزي، {_dname} من وين أبدأ؟"},{"role":"assistant","content":"ابدأ بتطبيق Duolingo، مجاني وممتاز"},{"role":"user","content":"شكد وقت لازم؟"},{"role":"assistant","content":"ساعة يومياً لـ6 أشهر تحكي أساسيات"},{"role":"user","content":f"بدأ هالأسبوع من {_dplace}"},{"role":"assistant","content":"الله يوفقك، اللغة تفتح آفاق"}]
    elif tpl == 18:
        hosp_list = pick(["مستشفى الكندي","مستشفى اليرموك","مستشفى الشمول","المجمع الطبي"])
        consult_fee = random.randint(20, 60) * 1000
        msgs = [{"role":"user","content":f"وين أقرب مستشفى من {_iplace}؟ أريد {_hltw}"},{"role":"assistant","content":f"{hosp_list} على بعد كيلوين"},{"role":"user","content":"يقبل تأمين؟"},{"role":"assistant","content":f"إي، يقبل. الكشف {consult_fee:,} دينار"},{"role":"user","content":"ساعات العمل؟"},{"role":"assistant","content":"طوارئ 24 ساعة، عيادات من 8 الصبح"}]
    elif tpl == 19:
        msgs = [{"role":"user","content":f"أريد أبدل الـ{_ww}، {_dname} شنو رأيك؟"},{"role":"assistant","content":"ليش تبدل؟"},{"role":"user","content":f"الـ{_ww} قليل والمدير مو زين"},{"role":"assistant","content":"دور على وظيفة أحسن أول، ثم اترك"},{"role":"user","content":"صح، أبدأ أدور"},{"role":"assistant","content":"الله يوفقك"}]
    elif tpl == 20:
        msgs = [{"role":"user","content":f"شلون الجو هالأيام بـ{_prov}؟"},{"role":"assistant","content":f"والله {pick(['حار هواي','بارد كلش','ممتاز','غيوم وشتوي'])} هالأيام"},{"role":"user","content":"عندنا هنا نفس الشي"},{"role":"assistant","content":f"{_agree}، الجو مو طبيعي هالسنة"},{"role":"user","content":"الله يستر"},{"role":"assistant","content":"الله كريم، إن شاء الله يتحسن"}]
    elif tpl == 21:
        msgs = [{"role":"user","content":f"أنا عندي {_hltw} من أمس"},{"role":"assistant","content":"سلامات! روحت للدكتور؟"},{"role":"user","content":"لا بعد"},{"role":"assistant","content":f"لازم تروح، {_hltw} ما يتهاون فيها"},{"role":"user","content":f"راح أروح {_dplace} العيادة بالضهر"},{"role":"assistant","content":"الله يشفيك ويعافيك"}]
    elif tpl == 22:
        msgs = [{"role":"user","content":f"شخبارك؟ شلون الـ{_ww} هالأيام؟"},{"role":"assistant","content":f"الحمد لله، الـ{_ww} ماشي بس ضغط هواي"},{"role":"user","content":"تعبان ليش؟"},{"role":"assistant","content":f"المشاريع كثرت والوقت ما يكفي بـ{_prov}"},{"role":"user","content":"الله يعينك"},{"role":"assistant","content":"إن شاء الله، شكراً"}]
    elif tpl == 23:
        study_hrs = random.randint(3, 12)
        msgs = [{"role":"user","content":f"عندي {_sw} باچر وما ذاكرت كافي، عندي {study_hrs} ساعات"},{"role":"assistant","content":"والله! ليش تأجلت؟"},{"role":"user","content":f"كنت مشغول بالـ{_ww}"},{"role":"assistant","content":f"هسه اشتغل على أهم مواضيع الـ{_sw}"},{"role":"user","content":"صح، يلا أذاكر"},{"role":"assistant","content":"بالتوفيق، الله يوفقك"}]
    elif tpl == 24:
        msgs = [{"role":"user","content":f"الـ{_tw} تعبت اليوم بالطريق لـ{_dplace}"},{"role":"assistant","content":"شصار فيها؟"},{"role":"user","content":"فجأة وقفت ما أدري"},{"role":"assistant","content":f"روحها عند الكراج قرب {_iplace}"},{"role":"user","content":"هسه أتصل بالسطحة"},{"role":"assistant","content":"الله يسهل عليك"}]
    elif tpl == 25:
        msgs = [{"role":"user","content":f"اليوم طبخنا {_pfood}، تعال تاكل {_dname}"},{"role":"assistant","content":f"والله؟ {_pfood}! كلش أحب هاي الأكلة"},{"role":"user","content":"تعال هسه الأكل جاهز"},{"role":"assistant","content":f"يلا جاي، إن شاء الله من {_dplace} قريب"},{"role":"user","content":"حياك، والعيش والملح"},{"role":"assistant","content":"الله يبارك فيكم"}]
    elif tpl == 26:
        msgs = [{"role":"user","content":f"شفت الڤيديو اللي نشرته على التيك توك عن {_iplace}؟"},{"role":"assistant","content":f"إي شفته! {_yw} والله، كلش حلو"},{"role":"user","content":"شكراً، حاولت أسوي شي مختلف"},{"role":"assistant","content":"نجحت، الناس كلهم عجبهم"},{"role":"user","content":"تشجيعك يحمسني أكثر"},{"role":"assistant","content":"كمل، أنت على المسار الصح"}]
    elif tpl == 27:
        msgs = [{"role":"user","content":f"أنا {_em} هالأيام، مو عارف ليش"},{"role":"assistant","content":"شنو اللي صاير؟ حچيلي"},{"role":"user","content":f"الضغط كثير، الـ{_ww} والبيت وكل شي"},{"role":"assistant","content":"لازم تاخذ وقت لروحك"},{"role":"user","content":"صح، ما أخذت إجازة من زمان"},{"role":"assistant","content":"خذ إجازة حتى لو يوم وحد، الله يوفقك"}]
    elif tpl == 28:
        msgs = [{"role":"user","content":f"{_gr}، {_dname}"},{"role":"assistant","content":f"{_rg}. وأنت {_dname2}؟"},{"role":"user","content":"بخير الحمد لله. شنو أخبارك؟"},{"role":"assistant","content":"ماكو شي جديد، الحمد لله"},{"role":"user","content":"الله يحفظك"},{"role":"assistant","content":"الله يخليك، حياك الله"}]
    elif tpl == 29:
        meals = pick(["دولمة","قيمة","تشريب","كباب","مسگوف","باچة","برياني"])
        msgs = [{"role":"user","content":f"شلونك {_dname}؟ شنو طبخت اليوم؟"},{"role":"assistant","content":f"طبخت {meals}. وأنت؟"},{"role":"user","content":f"أنا طبخت {_dfood}"},{"role":"assistant","content":f"حلو، {_dfood} يفتح الشهية"},{"role":"user","content":"تعال تاكل معي"},{"role":"assistant","content":"شكد الساعة؟ بالطريق"}]
    elif tpl == 30:
        msgs = [{"role":"user","content":f"وين كنت {_dname}؟ أتصلت فيك ما ردّيت"},{"role":"assistant","content":f"آسف، كنت بـ{_dplace} ما سمعت"},{"role":"user","content":"أبيك تجي معي على الدكتور"},{"role":"assistant","content":"شنو الموضوع؟ كلشي بخير؟"},{"role":"user","content":"إي، بس تعب بسيط"},{"role":"assistant","content":"الله يعافيك، أجيك"}]
    elif tpl == 31:
        weather = pick(["حارة هواي","بردانة","شتوية","غيوم","ربيعية"])
        msgs = [{"role":"user","content":f"الجو اليوم {weather}، صح؟"},{"role":"assistant","content":f"إي والله، {weather} هالأيام"},{"role":"user","content":f"وبـ{_prov} نفس الشي؟"},{"role":"assistant","content":"إي، كل العراق نفس الجو"},{"role":"user","content":"أفضل الجو المعتدل"},{"role":"assistant","content":"هههه، كلنا نفس الرأي"}]
    elif tpl == 32:
        msgs = [{"role":"user","content":f"شتسوي هالعطلة {_dname}؟"},{"role":"assistant","content":f"أفكر أروح {_prov} للعائلة. وأنت؟"},{"role":"user","content":"أنا ناوي أرتاح بالبيت"},{"role":"assistant","content":"راحة البيت ما تعوضها شي"},{"role":"user","content":"إي، أحياناً البيت أحسن سفرة"},{"role":"assistant","content":"صح والله"}]
    elif tpl == 33:
        goals = random.randint(1, 4)
        opponent = pick(["السعودية","إيران","الكويت","البحرين","سوريا","الأردن"])
        score = f"{goals}-{random.randint(0,goals-1) if goals > 0 else 0}"
        msgs = [{"role":"user","content":f"شفت مباراة المنتخب ضد {opponent} أمس؟ {score}"},{"role":"assistant","content":f"إي شفتها! أحلى مباراة من زمان"},{"role":"user","content":f"الهدف بـ{_iplace} كان روعة"},{"role":"assistant","content":"والله، اللاعبين انبسطوا"},{"role":"user","content":"المنتخب هالمرة زين هواي"},{"role":"assistant","content":"إي ربي يوفقهم"}]
    elif tpl == 34:
        veg = pick(["طماطة","بطاطا","باذنجان","كوسة","خيار"])
        msgs = [{"role":"user","content":f"الأسعار هالأيام مو طبيعية بـ{_dplace}"},{"role":"assistant","content":"إي والله، كل شي صعد"},{"role":"user","content":f"كيلو {veg} وصل {random.randint(4,8)*1000:,}"},{"role":"assistant","content":f"مو معقول، قبل شهر كان نص هذا"},{"role":"user","content":"مو عارف شسوي"},{"role":"assistant","content":"الله يفرجها"}]
    elif tpl == 35:
        msgs = [{"role":"user","content":f"عندي مقابلة {_job} باچر، ادعيلي"},{"role":"assistant","content":"الله يوفقك! وين المقابلة؟"},{"role":"user","content":f"شركة بـ{_dplace}"},{"role":"assistant","content":"استعد زين واروح بثياب رسمية"},{"role":"user","content":"شكراً على النصيحة"},{"role":"assistant","content":"ربي يفتحها عليك"}]
    elif tpl == 36:
        msgs = [{"role":"user","content":f"الـ{_ww} هالأيام مرهق والله"},{"role":"assistant","content":"شنو يصير؟"},{"role":"user","content":f"المشاريع كثرت بـ{_dplace}"},{"role":"assistant","content":"حدد ثلاث أولويات كل يوم"},{"role":"user","content":"صح، أجرب هالطريقة"},{"role":"assistant","content":"تنفع والله، جربتها"}]
    elif tpl == 37:
        age = random.randint(10, 16)
        phone_budget = random.randint(2, 10) * 100000
        brand = pick(["سامسونج","أوبو","شاومي","ريلمي","تكنو"])
        msgs = [{"role":"user","content":f"ابني {_dname} عمره {age} يريد آيفون بـ{phone_budget:,}"},{"role":"assistant","content":"كيف ميزانيتك؟"},{"role":"user","content":f"ما أكدر أشتري آيفون، {brand} بنفس السعر؟"},{"role":"assistant","content":f"{brand} خيار ممتاز وبنفس السعر"},{"role":"user","content":"بس أصحابه كلهم عندهم آيفون"},{"role":"assistant","content":"فهمه إن القيمة مو بالماركة"}]
    elif tpl == 38:
        car_type = pick(["أوتوماتيك","يدوي","SUV","سيدان"])
        drive_weeks = random.randint(2, 8)
        msgs = [{"role":"user","content":f"أريد أتعلم قيادة سيارة {car_type} بـ{_prov}"},{"role":"assistant","content":"ابدأ بمدرسة سياقة معتمدة"},{"role":"user","content":"المدة شكد؟"},{"role":"assistant","content":f"حوالي {drive_weeks} أسابيع للمبتدئين"},{"role":"user","content":"والرخصة بعدين؟"},{"role":"assistant","content":"تروح مديرية المرور بعد الاختبار"}]
    elif tpl == 39:
        eng_level = pick(["مبتدئ","متوسط","متقدم"])
        eng_months = random.randint(3, 12)
        msgs = [{"role":"user","content":f"أريد أتعلم إنجليزي مستوى {eng_level}، {_dname} تنصحني؟"},{"role":"assistant","content":"دوولينگو يومياً + أفلام إنجليزية"},{"role":"user","content":f"شكد وقت أحتاج لـ{eng_level}؟"},{"role":"assistant","content":f"تقريباً {eng_months} أشهر بالممارسة اليومية"},{"role":"user","content":"شكراً، أبدأ"},{"role":"assistant","content":"الله يوفقك"}]
    elif tpl == 40:
        msgs = [{"role":"user","content":f"شلونك {_dname}؟ ما شفناك من زمان"},{"role":"assistant","content":f"بخير الحمد لله، مشغول بالـ{_ww}"},{"role":"user","content":f"اللي يشتغل {_job} يبارك فيه"},{"role":"assistant","content":"هههه، صح. وأنت شنو أخبارك؟"},{"role":"user","content":"كلشي تمام"},{"role":"assistant","content":"الحمد لله، ربي يديم النعمة"}]
    elif tpl == 41:
        hrs = random.randint(2, 6)
        msgs = [{"role":"user","content":f"كيف السفر لـ{_prov} هالأيام؟"},{"role":"assistant","content":"بالسيارة أحسن، الباص طويل"},{"role":"user","content":"شكد الطريق؟"},{"role":"assistant","content":f"حوالي {hrs} ساعات من بغداد"},{"role":"user","content":"والأمن؟"},{"role":"assistant","content":"الله يسلمكم، الطريق مأمون هالأيام"}]
    elif tpl == 42:
        msgs = [{"role":"user","content":f"أريد أعزم العائلة على {_pfood}، وين أحسن مطعم؟"},{"role":"assistant","content":f"مطعم أبو نواس قرب {_iplace}، أحسن {_pfood} ببغداد"},{"role":"user","content":"شكد يكلف لـ5 أشخاص؟"},{"role":"assistant","content":f"حوالي {random.randint(100,300)*1000:,} دينار"},{"role":"user","content":"معقول، نروح هناك"},{"role":"assistant","content":"إن شاء الله تنبسطون"}]
    elif tpl == 43:
        msgs = [{"role":"user","content":f"أم {_dname} تعبانة من الـ{_hltw}، ما تقدر تطبخ"},{"role":"assistant","content":"الله يعافيها! شنو صاير؟"},{"role":"user","content":"تعب عام وضغط"},{"role":"assistant","content":"خذوا أكل من المطعم، لازم ترتاح"},{"role":"user","content":"الله يشفيها"},{"role":"assistant","content":"إن شاء الله تقوم بالسلامة"}]
    elif tpl == 44:
        msgs = [{"role":"user","content":f"{_dname} صاحبي يبي يفتح مشروع {_job} بـ{_prov}"},{"role":"assistant","content":"فكرة زينة! شنو المشروع بالضبط؟"},{"role":"user","content":f"مكتب {_job} مستقل"},{"role":"assistant","content":"يحتاج ترخيص وموقع زين"},{"role":"user","content":"من وين يبدأ؟"},{"role":"assistant","content":"الغرفة التجارية أول خطوة"}]
    elif tpl == 45:
        amt = random.randint(1, 10) * 500000
        msgs = [{"role":"user","content":f"أريد أبعث فلوس لـ{_dname} بـ{_prov}"},{"role":"assistant","content":"كيف تبعث؟"},{"role":"user","content":f"مبلغ {amt:,} دينار"},{"role":"assistant","content":"زين كاش أو آسيا حوالة، سريعين وأمينين"},{"role":"user","content":"الأجرة شكد؟"},{"role":"assistant","content":"1-2% من المبلغ"}]
    elif tpl == 46:
        shrine = pick(["النجف","كربلاء"])
        visit_day = pick(["ليلة الجمعة","يوم الخميس","الإجازة","نهاية الأسبوع"])
        stay_days = random.randint(1, 3)
        msgs = [{"role":"user","content":f"أم {_dname} تبي تزور {shrine} يوم {visit_day}، نقعد {stay_days} أيام"},{"role":"assistant","content":"زيارة مباركة! الله يوفقكم"},{"role":"user","content":"أدعيلنا"},{"role":"assistant","content":"إن شاء الله ترجعون بالسلامة والقبول"},{"role":"user","content":"آمين، شكراً"},{"role":"assistant","content":"الله يقبل زيارتكم"}]
    elif tpl == 47:
        job_salary = random.randint(4, 20) * 100000
        msgs = [{"role":"user","content":f"ولدي {_dname} نجح وراح يشتغل {_job} بـ{_prov}، راتب {job_salary:,}"},{"role":"assistant","content":"مبارك! الله يبارك فيه"},{"role":"user","content":"فرحان هواي والله"},{"role":"assistant","content":"يستاهل، تعب وحصل"},{"role":"user","content":"ربي يكمل عليه"},{"role":"assistant","content":"إن شاء الله دايماً يفرحكم"}]
    elif tpl == 48:
        away_city = pick(["بغداد","البصرة","الموصل","كركوك","أربيل"])
        away_months = random.randint(6, 18)
        msgs = [{"role":"user","content":f"أخوي {_dname} يشتغل بـ{away_city} ومن {away_months} شهر ما يجي يزورنا"},{"role":"assistant","content":"الشغل يشغل، بس لازم يجي يزور"},{"role":"user","content":"مشتاقين له هواي"},{"role":"assistant","content":"كلمه وذكره بأهمية العائلة"},{"role":"user","content":"أخاف يزعل"},{"role":"assistant","content":"كلمه بحب، هو يفهم"}]
    elif tpl == 49:
        msgs = [{"role":"user","content":f"عندي حفلة لبنتي بـ{_dplace}، شكد أعزم؟"},{"role":"assistant","content":"شكد شخص تفكر؟"},{"role":"user","content":"حوالي 50"},{"role":"assistant","content":"قاعة صغيرة أنيق وريح باله"},{"role":"user","content":f"وأكل {_pfood} يناسب؟"},{"role":"assistant","content":"ممتاز للحفلات"}]
    elif tpl == 50:
        yrs_work = random.randint(2, 8)
        msgs = [{"role":"user","content":f"زميلي {_dname} ترقى بعد {yrs_work} سنين وأنا ما ترقيت"},{"role":"assistant","content":"شنو شعورك؟"},{"role":"user","content":"زعلان بس ما أريد أظهر"},{"role":"assistant","content":"طبيعي. اسأل مديرك شنو ينقصك للترقية"},{"role":"user","content":"صح، لازم أتطور"},{"role":"assistant","content":"ربي يوفقك"}]
    elif tpl == 51:
        bride_type = pick(["معلمة","طالبة","موظفة","دكتورة","مهندسة"])
        msgs = [{"role":"user","content":f"أريد أتزوج {bride_type} من {_prov}، شنو رأيك {_dname}؟"},{"role":"assistant","content":"الناس بكل المحافظات محترمون. المهم الرجل كفؤ"},{"role":"user","content":"أخاف الفرق الجغرافي مشكلة"},{"role":"assistant","content":"مو مشكلة لو الاثنين راضيين"},{"role":"user","content":"صح، الموضوع بالتفاهم"},{"role":"assistant","content":"ربي يوفقك"}]
    elif tpl == 52:
        num = random.randint(20, 100)
        msgs = [{"role":"user","content":f"عندي عرس، شنو أطبخ لـ{num} شخص؟"},{"role":"assistant","content":f"{_pfood} خيار ممتاز للأعراس"},{"role":"user","content":"بقدر أطبخ بيتياً؟"},{"role":"assistant","content":"للأعداد الكبيرة أفضل طباخ أعراس"},{"role":"user","content":"شكد يكلف؟"},{"role":"assistant","content":f"تقريباً {random.randint(3,8)*1000:,} للشخص"}]
    elif tpl == 53:
        age2 = random.randint(15, 35)
        msgs = [{"role":"user","content":f"أريد هدية ليوم ميلاد {_dname}، عمرها {age2}"},{"role":"assistant","content":"شنو تحب؟"},{"role":"user","content":"تحب العطور والإكسسوار"},{"role":"assistant","content":"عطر فاخر هدية ممتازة، محلات المنصور تشوف"},{"role":"user","content":"شكد الميزانية المناسبة؟"},{"role":"assistant","content":f"بين {random.randint(50,200)*1000:,} دينار"}]
    elif tpl == 54:
        msgs = [{"role":"user","content":f"ابن {_dname} سُلب موبايله قرب {_iplace}"},{"role":"assistant","content":"الله يحفظه! شنو صار؟"},{"role":"user","content":"جاه شخص على موتور وسلبه"},{"role":"assistant","content":"روحوا تبلغوا الشرطة بأسرع وقت"},{"role":"user","content":"وفائدة التبليغ؟"},{"role":"assistant","content":"أحياناً يلقوهم، والأهم توثيق الحادثة"}]
    elif tpl == 55:
        neigh_gift = pick(["تمر","حلويات","فاكهة","كيك","چاي"])
        neigh_origin = pick(["من محافظة ثانية","عائلة شبابية","عائلة كبيرة","أقارب جدد","غرباء"])
        msgs = [{"role":"user","content":f"الجيران الجدد {neigh_origin} قدامنا بـ{_dplace}، كيف أتعرف عليهم؟"},{"role":"assistant","content":"روح قدمهم بنفسك مع هدية صغيرة"},{"role":"user","content":f"وش أحمل؟ {neigh_gift}؟"},{"role":"assistant","content":f"{neigh_gift} ممتاز، الكل يحبه"},{"role":"user","content":"صح، أروح بكره"},{"role":"assistant","content":"الجار قبل الدار"}]
    elif tpl == 56:
        myage = random.randint(30, 45)
        msgs = [{"role":"user","content":f"أريد أكمل {_sw} وعمري {myage}"},{"role":"assistant","content":"ما في عمر للتعليم"},{"role":"user","content":"أخاف ما أقدر أنافس الشباب"},{"role":"assistant","content":f"خبرتك تعوضك، والجامعات المسائية مناسبة بـ{_prov}"},{"role":"user","content":"فكرة زينة"},{"role":"assistant","content":"الله يوفقك"}]
    elif tpl == 57:
        inherit_type = pick(["بيت","أرض","دكان","سيارة","ذهب"])
        inherit_val = random.randint(10, 200) * 1000000
        msgs = [{"role":"user","content":f"عندي خلاف مع أختي على ميراث {inherit_type} بـ{_prov} قيمته {inherit_val:,}"},{"role":"assistant","content":"الميراث موضوع حساس. شنو الخلاف؟"},{"role":"user","content":"تريد أكثر من حقها الشرعي"},{"role":"assistant","content":"وساطة شخص مؤثر بالعائلة أحسن من المحكمة"},{"role":"user","content":"ما أريد نخسر بعض"},{"role":"assistant","content":"الكلام الطيب يحل أكثر من القضاء"}]
    elif tpl == 58:
        donate_t = pick(["كفالة يتيم","أرملة","طالب فقير","مريض","سلة غذائية"])
        donate_a = random.randint(50, 500) * 1000
        msgs = [{"role":"user","content":f"أريد أتبرع {donate_a:,} دينار لجمعية خيرية بـ{_prov}"},{"role":"assistant","content":"إن شاء الله تقبل. ابحث عن الجمعيات المعتمدة"},{"role":"user","content":"أحسن نوع تبرع؟"},{"role":"assistant","content":f"{donate_t}، دايم ومتواصل"},{"role":"user","content":"زين، أبحث"},{"role":"assistant","content":"الله يبارك فيك ويضاعف أجرك"}]
    elif tpl == 59:
        alone_yrs = random.randint(1, 5)
        msgs = [{"role":"user","content":f"أبو {_dname} يعاني وحدة من {alone_yrs} سنين بعد وفاة زوجته"},{"role":"assistant","content":"الله يرحمها. الوحدة صعبة بعد السنين"},{"role":"user","content":"شنو نسوي له؟"},{"role":"assistant","content":"خليه يشارك بمجالس اجتماعية، والزيارة المتكررة مهمة"},{"role":"user","content":"والتلفون؟"},{"role":"assistant","content":"علمه واتساب فيديو، يفرق هواي"}]
    elif tpl == 60:
        msgs = [{"role":"user","content":f"أهلنا بـ{_prov} ما زارونا من زمان {_dname}"},{"role":"assistant","content":"الناس مشغولين هالأيام"},{"role":"user","content":"بس مشتاقين لهم"},{"role":"assistant","content":"اتصل فيهم وعزمهم أو زورهم أنتم"},{"role":"user","content":"صح، نروح بالعطلة"},{"role":"assistant","content":"الله يجمعكم على خير"}]
    elif tpl == 61:
        house_budget = random.randint(50, 300) * 1000000
        house_rooms = random.randint(2, 5)
        msgs = [{"role":"user","content":f"أريد أشتري بيت {house_rooms} غرف بـ{_prov}، ميزانية {house_budget:,}"},{"role":"assistant","content":"يعتمد على المنطقة"},{"role":"user","content":"أريد منطقة هادية"},{"role":"assistant","content":f"أطراف {_prov} أرخص وهادية"},{"role":"user","content":"وإيجارات؟"},{"role":"assistant","content":"الشراء أحسن من الإيجار على المدى البعيد"}]
    elif tpl == 62:
        msgs = [{"role":"user","content":f"شنو تنصحني أشتري بـ{_dplace}؟ {_dfood} أو {_dfood2}؟"},{"role":"assistant","content":f"يعتمد على مزاجك، {_dfood} أحلى للغدا"},{"role":"user","content":f"بس {_dfood2} أسرع"},{"role":"assistant","content":"لو مستعجل خذ الأسرع"},{"role":"user","content":"صح، شكراً"},{"role":"assistant","content":"تفضل، بالعافية"}]
    elif tpl == 63:
        rel_type2 = pick(["الجيران","الأقارب","زملاء الشغل","الأصحاب"])
        rel_issue2 = pick(["ما يردون السلام","بعيدين عنا","مشغولين","ما يتواصلون"])
        msgs = [{"role":"user","content":f"كيف أحسن علاقتي مع {rel_type2} بـ{_dplace}؟ {rel_issue2}"},{"role":"assistant","content":"ابدأ بالسلام والتعارف"},{"role":"user","content":f"وإذا {rel_issue2}؟"},{"role":"assistant","content":"استمر، الناس أحياناً تحتاج وقت"},{"role":"user","content":"صح، أصبر"},{"role":"assistant","content":"الجار قبل الدار"}]
    elif tpl == 64:
        decor_color = pick(["بيج","رمادي","أزرق فاتح","أخضر فاتح","أبيض"])
        decor_budget2 = random.randint(1, 8) * 1000000
        msgs = [{"role":"user","content":f"أريد أعيد تزيين بيتي بـ{_dplace}، ميزانية {decor_budget2:,}"},{"role":"assistant","content":"فكرة حلوة! شنو تريد تغير؟"},{"role":"user","content":f"الـ{_hw} والألوان، أفضل {decor_color}؟"},{"role":"assistant","content":f"لون {decor_color} هادي وأنيق"},{"role":"user","content":f"والـ{_hw} أشتري جديد؟"},{"role":"assistant","content":"لو ميزانيتك تحتمل، يستاهل"}]
    elif tpl == 65:
        time2 = pick(["الصباح","العصر","المساء","الليل","الجمعة"])
        act2 = pick(["مشي","رياضة","صور","قهوة","قراءة"])
        msgs = [{"role":"user","content":f"شنو أسوي وقت {time2} بـ{_iplace}؟"},{"role":"assistant","content":f"{act2} هناك ممتاز وهواء منعش"},{"role":"user","content":"وبالليل؟"},{"role":"assistant","content":"الكافيهات قريبة وأجواء حلوة"},{"role":"user","content":f"تجي معي {_dname}؟"},{"role":"assistant","content":"إي ماشي، باچر"}]
    elif tpl == 66:
        msgs = [{"role":"user","content":f"سمعت أسعار {_pfood} غلت بـ{_dplace}"},{"role":"assistant","content":"إي، الأسعار مو طبيعية هالأيام"},{"role":"user","content":"سبب غلاء الأسعار؟"},{"role":"assistant","content":"الوقود والنقل والطلب المتزايد"},{"role":"user","content":"الله يفرجها"},{"role":"assistant","content":"ربي يخفف على الكل"}]
    elif tpl == 67:
        msgs = [{"role":"user","content":f"أريد أبدأ مشروع {_dfood} بيتي بـ{_prov}"},{"role":"assistant","content":"فكرة ممتازة! الطلب على الأكل البيتي كثير"},{"role":"user","content":"من وين أبدأ؟"},{"role":"assistant","content":"من واتساب وإنستقرام أول"},{"role":"user","content":"ورأسمال؟"},{"role":"assistant","content":f"ابدأ بـ{random.randint(100,500)*1000:,} دينار"}]
    elif tpl == 68:
        msgs = [{"role":"user","content":f"شنو أفضل تطبيق توصيل {_pfood} بـ{_prov}؟"},{"role":"assistant","content":"مزيود أو طاغ، الاثنين سريعين"},{"role":"user","content":"والأسعار؟"},{"role":"assistant","content":"أجرة توصيل 2-5 آلاف دينار"},{"role":"user","content":"ماشي، أجرب"},{"role":"assistant","content":"إن شاء الله تنبسط"}]
    elif tpl == 69:
        camp_age = random.randint(8, 17)
        camp_type = pick(["رياضي","علمي","فني","ديني","ثقافي"])
        msgs = [{"role":"user","content":f"ولدي {_dname} عمره {camp_age}، يبحث عن معسكر {camp_type} بـ{_prov}"},{"role":"assistant","content":f"فكرة ممتازة، يتعلم ويستمتع"},{"role":"user","content":"وين أسجله؟"},{"role":"assistant","content":"مديرية الشباب بالمحافظة عندهم برامج"},{"role":"user","content":"شكراً"},{"role":"assistant","content":"الله يوفقه"}]
    elif tpl == 70:
        visit_ppl = random.randint(2, 8)
        visit_transport = pick(["بالسيارة","بالتاكسي","بالباص","بالأوبر"])
        msgs = [{"role":"user","content":f"أريد أزور {_iplace} مع {visit_ppl} أشخاص، أحسن وقت؟"},{"role":"assistant","content":"الربيع والخريف أحسن، الجو معتدل"},{"role":"user","content":f"نروح {visit_transport}؟"},{"role":"assistant","content":f"{visit_transport} ممتاز لـ{visit_ppl} أشخاص"},{"role":"user","content":"تجي معنا؟"},{"role":"assistant","content":"إي ماشي، وين لقاءنا؟"}]
    elif tpl == 71:
        msgs = [{"role":"user","content":f"شنو رأيك بمحلات {_dplace2}؟ أحسن من {_dplace}؟"},{"role":"assistant","content":"يعتمد شنو تشتري"},{"role":"user","content":f"أشتري {_dfood} وحاجات البيت"},{"role":"assistant","content":f"{_dplace} للبيت أحسن، {_dplace2} للأكل"},{"role":"user","content":"ماشي، شكراً"},{"role":"assistant","content":"تفضل"}]
    elif tpl == 72:
        dest_abroad = pick(["ألمانيا","كندا","أمريكا","تركيا","هولندا","السويد"])
        msgs = [{"role":"user","content":f"صاحبي {_dname} يبي يسافر {dest_abroad} ويتركنا"},{"role":"assistant","content":"مو بده يتركك، بده يحسن حياته"},{"role":"user","content":"صح بس الصداقة تنقطع"},{"role":"assistant","content":"الصداقة الحقيقية تبقى حتى عن بعد"},{"role":"user","content":"صح والله"},{"role":"assistant","content":f"الله يوفقه بـ{dest_abroad} ويوفقكم"}]
    elif tpl == 73:
        fight_yrs = random.randint(1, 8)
        fight_cause2 = pick(["كلام جرح","ميراث","سوء فهم","مشكلة عائلية"])
        msgs = [{"role":"user","content":f"أريد أتصالح مع {_dname} بعد {fight_yrs} سنين خلاف بسبب {fight_cause2}"},{"role":"assistant","content":"قرار زين! صلة الرحم واجبة"},{"role":"user","content":"بس من يبدأ؟"},{"role":"assistant","content":"أنت ابدأ، صاحب المبادرة له الأجر"},{"role":"user","content":"يمكن يرفض"},{"role":"assistant","content":"مسؤوليتك تمد يدك"}]
    elif tpl == 74:
        absent_months = random.randint(2, 12)
        msgs = [{"role":"user","content":f"شلونكم بـ{_prov}؟ ما شفناكم من {absent_months} شهر"},{"role":"assistant","content":"الحمد لله كلنا بخير. وأنتم؟"},{"role":"user","content":"كلنا تمام الحمد لله"},{"role":"assistant","content":"الله يديم النعمة"},{"role":"user","content":"متى تجون تزورونا؟"},{"role":"assistant","content":"قريب إن شاء الله"}]
    elif tpl == 75:
        msgs = [{"role":"user","content":f"أريد أشتري سيارة مستعملة بـ{_dplace}"},{"role":"assistant","content":"شنو ميزانيتك؟"},{"role":"user","content":f"حوالي {random.randint(5,20)*1000000:,} دينار"},{"role":"assistant","content":"كمبدأ، فحص السيارة بالكراج قبل الشراء"},{"role":"user","content":"وين الفحص؟"},{"role":"assistant","content":f"كراج موثوق قرب {_iplace}"}]
    elif tpl == 76:
        internet_speed = pick(["1 ميغا","5 ميغا","10 ميغا","50 ميغا"])
        internet_price = random.randint(20, 100) * 1000
        msgs = [{"role":"user","content":f"الإنترنت عندنا بطيء كلش بـ{_prov}، باقة {internet_speed} بـ{internet_price:,}"},{"role":"assistant","content":"اتصل بشركة الإنترنت وبلّغ"},{"role":"user","content":"بلغت بس ما صلحوا"},{"role":"assistant","content":"غير الشركة أو جرب باقة أسرع"},{"role":"user","content":"إيه شركة تنصحني؟"},{"role":"assistant","content":"زين أو آسياسيل أحسن تغطية"}]
    elif tpl == 77:
        msgs = [{"role":"user","content":f"أريد أتعلم طبخ {_pfood} من صفر"},{"role":"assistant","content":"فكرة حلوة! ابدأ من يوتيوب"},{"role":"user","content":"في كورس متخصص؟"},{"role":"assistant","content":f"في أكاديميات طبخ بـ{_prov}"},{"role":"user","content":"شكراً، أسجل"},{"role":"assistant","content":"بالتوفيق، إن شاء الله تنجح"}]
    elif tpl == 78:
        msgs = [{"role":"user","content":f"شنو رأيك بمطعم {_pfood} الجديد قرب {_iplace}؟"},{"role":"assistant","content":"شفت تقييماته زينة"},{"role":"user","content":"جربته؟"},{"role":"assistant","content":f"لا بعد، بس ناوي أروح مع {_dname}"},{"role":"user","content":"روح وحچيلي"},{"role":"assistant","content":"إي، إن شاء الله باچر"}]
    elif tpl == 79:
        msgs = [{"role":"user","content":f"الدراسة والـ{_ww} مع بعض صعب كلش"},{"role":"assistant","content":"إي، يحتاج تنظيم وقت"},{"role":"user","content":"شنو تنصحني؟"},{"role":"assistant","content":f"جدول أسبوعي ثابت، {_sw} الصبح و{_ww} المسا"},{"role":"user","content":"أجرب هالطريقة"},{"role":"assistant","content":"الله يوفقك، أنت قادر"}]
    else:
        msgs = [{"role":"user","content":f"{_gr} {_dname}، شكو ماكو؟"},{"role":"assistant","content":f"{_rg}. وأنت {_dname2}؟"},{"role":"user","content":f"بخير، مشغول بالـ{_ww} هالأيام"},{"role":"assistant","content":f"الله يعينك. شلون أحوالكم بـ{_prov}؟"},{"role":"user","content":"كلشي تمام الحمد لله"},{"role":"assistant","content":"الحمد لله، ربي يديم النعمة"}]

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
    _city2 = pick(_IRAQI_CITIES)
    _mname = pick(_MALE_NAMES_S)
    _mname2= pick(_MALE_NAMES_S)
    _fname = pick(_FEMALE_NAMES_S)
    _fname2= pick(_FEMALE_NAMES_S)
    _job   = pick(_JOBS_S)
    _job2  = pick(_JOBS_S)
    _food  = pick(_FOODS_S)
    _food2 = pick(_FOODS_S)
    _prov  = pick(_cat("المحافظات العراقية") or ["بغداد","البصرة","النجف","كربلاء"])
    _pfood = pick(_cat("الأكلات الشعبية العراقية") or ["مسگوف","پاچة","دولمة"])
    _iplace= pick(_cat("المدن والأماكن العراقية") or ["شارع المتنبي","كورنيش أبو نواس"])
    _sp    = pick(_SYMPATHY_W) if _SYMPATHY_W else "الله يوفقك"
    _pr    = pick(PRAISE) if PRAISE else "كفو"
    _fw    = pick(_FAMILY_WORDS) if _FAMILY_WORDS else "أخوية"
    _pw    = pick(_PROBLEM_W) if _PROBLEM_W else "مشكلة"
    _rw    = pick(_RELIGION_W) if _RELIGION_W else "إن شاء الله"
    tpl = random.randint(1, 80)

    if tpl == 1:
        msgs = [{"role":"user","content":f"شنو رأيك بالزواج المبكر يا {_mname}؟"},{"role":"assistant","content":"الزواج المبكر مشكلة، الشاب لازم يكمل دراسته أول"},{"role":"user","content":f"بس أهل البنت بـ{_prov} يضغطون"},{"role":"assistant","content":"لازم تفهمهم إن الزواج يحتاج نضج وإمكانيات"},{"role":"user","content":"وإذا ما يفهمون؟"},{"role":"assistant","content":f"اطلب وساطة {_fw} يحترمونه يشرح لهم"}]
    elif tpl == 2:
        hosp = pick(["ابن البيطار","الصدر","اليرموك","مدينة الطب"])
        msgs = [{"role":"user","content":f"أمي مريضة ومحتاجة عملية قلب بـ{_prov}"},{"role":"assistant","content":f"الله يشفيها. خذها لمستشفى {hosp}، {_sp}"},{"role":"user","content":"غالية هالعمليات؟"},{"role":"assistant","content":"في حكومي مجاني بس انتظار، وخصوصي من 5 لـ10 مليون"},{"role":"user","content":"أي تنصح؟"},{"role":"assistant","content":"لو عندك إمكانية الخصوصي أسرع وأريح"}]
    elif tpl == 3:
        dest = pick(["ألمانيا","كندا","أمريكا","هولندا","السويد","أستراليا"])
        msgs = [{"role":"user","content":f"أخوي {_mname} يريد يسافر للشغل لبرا البلد"},{"role":"assistant","content":"وين يريد يروح؟"},{"role":"user","content":f"{dest}"},{"role":"assistant","content":f"كندا أسهل هجرة بس {dest} فيها فرص"},{"role":"user","content":f"بس بعيدة عن {_prov}"},{"role":"assistant","content":"الغربة صعبة، بس لو الفرصة زينة يستاهل"}]
    elif tpl == 4:
        num = random.randint(8, 20)
        msgs = [{"role":"user","content":f"عزيمة بكره لـ{num} شخص، شنو أطبخ؟"},{"role":"assistant","content":f"شكد نفر؟ {_pfood} أكلة عراقية أصيلة"},{"role":"user","content":f"{_pfood} صعبة؟"},{"role":"assistant","content":"تحتاج صبر بس ما تحتاج خبرة كبيرة"},{"role":"user","content":"ماشي، أحاول"},{"role":"assistant","content":"بالتوفيق، الله يوفقك"}]
    elif tpl == 5:
        msgs = [{"role":"user","content":f"بنتي {_fname} تبي تدرس برا البلد"},{"role":"assistant","content":"يا بلد تبي تروح؟"},{"role":"user","content":"تركيا أو ماليزيا"},{"role":"assistant","content":"ماليزيا أرخص وجامعاتها معترف فيها دولياً"},{"role":"user","content":f"أمانة على بناتنا من {_prov}؟"},{"role":"assistant","content":"البنت المسؤولة تكدر تدرس برا، الدراسة مهمة"}]
    elif tpl == 6:
        noise_type = pick(["يرفع الموسيقى","يحرك سيارته","يشغل المولدة","يجمع أصحابه بالليل","يصرخ"])
        noise_months = random.randint(1, 6)
        msgs = [{"role":"user","content":f"جاري بـ{_iplace} يزعجني من {noise_months} أشهر، {noise_type} بالليل"},{"role":"assistant","content":"كلمه بهدوء أول، لو ما أثر اشكه للبلدية"},{"role":"user","content":"جربت بس ما نفع"},{"role":"assistant","content":"اشكه للبلدية رسمياً، هم يحلوا"},{"role":"user","content":"صح، أروح البلدية"},{"role":"assistant","content":"الله يحل الموضوع"}]
    elif tpl == 7:
        prop_type = pick(["بيت","دكان","أرض","سيارة"])
        msgs = [{"role":"user","content":f"أريد أصالح أخوي {_mname} بعد خلاف إرث {prop_type} بـ{_prov}"},{"role":"assistant","content":"مشاكل الإرث صعبة. شنو الخلاف بالضبط؟"},{"role":"user","content":f"يريد يبيع الـ{prop_type} وأنا ما أريد"},{"role":"assistant","content":f"جيب {_fw} وسيط من الأهل يحل"},{"role":"user","content":"وإذا ما قبل الوساطة؟"},{"role":"assistant","content":"الصبر والدعاء والتواصل يجيب نتيجة"}]
    elif tpl == 8:
        age_mo = random.randint(6, 36)
        cry_reason = pick(["أسنان","مغص","جوع","حمى خفيفة","يريد انتباه"])
        msgs = [{"role":"user","content":f"ولدي يبكي هواي، عمره {age_mo} شهر"},{"role":"assistant","content":"شنو صاير فيه؟"},{"role":"user","content":"ما أدري، كل ليلة يبكي"},{"role":"assistant","content":f"ممكن {cry_reason}، شوف إذا حرارة"},{"role":"user","content":"ما عنده حرارة"},{"role":"assistant","content":"شيله ولعب معه، يحتاج انتباه"}]
    elif tpl == 9:
        issue = pick(["تتدخل بكل شي","تنتقد زوجتي دايماً","ما تعطيها خصوصية","تتصل كثير"])
        msgs = [{"role":"user","content":f"زوجتي {_fname} وأمي ما يتفاهمون بـ{_prov}"},{"role":"assistant","content":"هذي مشكلة شايعة، لازم تكون وسيط"},{"role":"user","content":f"أمي دايماً {issue}"},{"role":"assistant","content":"ما تحكي لواحدة عن الثانية، وكون عادل بالوقت"},{"role":"user","content":"يصعب"},{"role":"assistant","content":"فهمها بهدوء إن الزوجة تحتاج خصوصية"}]
    elif tpl == 10:
        ring_price = random.randint(3, 15) * 1000000
        msgs = [{"role":"user","content":f"خطيبتي {_fname} تريد خاتم بـ{ring_price:,} دينار"},{"role":"assistant","content":"كلمها بصراحة عن إمكانياتك"},{"role":"user","content":"أخاف ما تقبل"},{"role":"assistant","content":"اللي تحبك تفهمك، الخاتم البسيط أحلى من الدين"},{"role":"user","content":"صح، بكلمها"},{"role":"assistant","content":f"توفيق {_rw}"}]
    elif tpl == 11:
        gift = pick(["عطر","ساعة","حقيبة","فستان","مصروف"])
        msgs = [{"role":"user","content":f"عيد الأم جاي، أريد هدية لأمي بـ{_prov}"},{"role":"assistant","content":"أحسن هدية وقتك معها"},{"role":"user","content":f"وشي مادي؟ فكرت بـ{gift}"},{"role":"assistant","content":f"{gift} فكرة زينة، تختار ما يناسبها"},{"role":"user","content":"وهدية الأولاد الصغار؟"},{"role":"assistant","content":"رسمة باليد أغلى من أي هدية عند الأم"}]
    elif tpl == 12:
        wfh_prob = pick(["الأطفال يزعجون","ما أكدر أركز","الانترنت بطيء","الأهل يقاطعون"])
        msgs = [{"role":"user","content":f"شنو رأيك بالشغل من البيت {_mname}؟"},{"role":"assistant","content":"له مزايا وعيوب، راحة بس تحتاج انضباط"},{"role":"user","content":f"عندي مشكلة، {wfh_prob}"},{"role":"assistant","content":"حدد وقت ومكان للشغل وأطفئ الإشعارات"},{"role":"user","content":"وإذا ما نفع؟"},{"role":"assistant","content":"اشتغل بعد ما يناموا أو من مقهى هادي"}]
    elif tpl == 13:
        msgs = [{"role":"user","content":f"أريد أنزل وزن، شنو أسوي {_fname}؟"},{"role":"assistant","content":"قلل السكر والكربوهيدرات أول"},{"role":"user","content":"والرياضة؟"},{"role":"assistant","content":f"مشي 30 دقيقة يومياً قرب {_iplace} كافي للبداية"},{"role":"user","content":"وأكلي؟"},{"role":"assistant","content":"خضار وبروتين، قلل الأرز الأبيض"}]
    elif tpl == 14:
        msgs = [{"role":"user","content":f"أبي مريض والدكتور يريد يدخله مستشفى بـ{_prov}"},{"role":"assistant","content":"الله يشفيه. شنو عنده؟"},{"role":"user","content":"ضغط وسكر مرتفع"},{"role":"assistant","content":"التنويم ضروري للمتابعة المكثفة"},{"role":"user","content":"خايف عليه"},{"role":"assistant","content":f"الله يحفظه، {_sp}، توكل على الله"}]
    elif tpl == 15:
        subj = pick(["رياضيات","فيزياء","كيمياء","أحياء","إحصاء","محاسبة"])
        hrs_left = random.randint(3, 12)
        msgs = [{"role":"user","content":f"عندي امتحان {subj} باچر وما ذاكرت، {_mname2} ساعدني"},{"role":"assistant","content":f"{subj}؟ كم ساعة عندك؟"},{"role":"user","content":f"{hrs_left} ساعات"},{"role":"assistant","content":"ذاكر الأسئلة المتكررة وأهم المواضيع أول"},{"role":"user","content":"ما أكدر أخلص الكل"},{"role":"assistant","content":"ركز على 70% من المنهج اللي يطلع أكثر"}]
    elif tpl == 16:
        num_ppl = random.randint(6, 14)
        rooms = random.randint(1, 3)
        rent = random.randint(2, 8) * 100000
        msgs = [{"role":"user","content":f"بيتنا بـ{_city} صغير، {num_ppl} أشخاص بـ{rooms} غرف"},{"role":"assistant","content":"هذا صعب. تفكر تأجر أكبر؟"},{"role":"user","content":f"الإيجار غالي بـ{_city}، يوصل {rent:,}"},{"role":"assistant","content":"دور في أطراف المدينة، أرخص بكثير"},{"role":"user","content":"فكرة زينة"},{"role":"assistant","content":"الله يوفقك"}]
    elif tpl == 17:
        gift_type = pick(["ملابس","عطور","حلويات","إلكترونيات","ألعاب أطفال"])
        gift_budget = random.randint(50, 400) * 1000
        msgs = [{"role":"user","content":f"وين أشتري {gift_type} للعيد بـ{_iplace}؟ ميزانية {gift_budget:,}"},{"role":"assistant","content":"سوق العلاوي فيه كل شي وأسعاره معقولة"},{"role":"user","content":"ما أريد أروح سوق، تعبان"},{"role":"assistant","content":"اطلب أونلاين من تطبيق فاست ديليفري"},{"role":"user","content":"أمين هذي التطبيقات؟"},{"role":"assistant","content":"إي، فيه تقييمات وكثير ناس يستخدمونها"}]
    elif tpl == 18:
        hrs = random.randint(3, 10)
        game_age = random.randint(8, 16)
        sport = pick(["كرة قدم","سباحة","كاراتيه","دراجة","ركض"])
        msgs = [{"role":"user","content":f"ابني {_mname} عمره {game_age}، يلعب جيمز {hrs} ساعات يومياً"},{"role":"assistant","content":"هذا كثير هواي، يأثر على الدراسة"},{"role":"user","content":"شلون أوقفه؟"},{"role":"assistant","content":"حدد له ساعتين بعد الدراسة فقط"},{"role":"user","content":"وإذا ما قبل؟"},{"role":"assistant","content":f"انطه نشاط {sport}، الرياضة أحسن بديل"}]
    elif tpl == 19:
        num2 = random.randint(4, 8)
        msgs = [{"role":"user","content":f"أريد أعزم {num2} أصدقاء على عشاء، شنو أحضر؟"},{"role":"assistant","content":f"مسگوف أو {_pfood} أحلى عشاء"},{"role":"user","content":"صعب أسوي مسگوف بالبيت؟"},{"role":"assistant","content":f"تشتريه جاهز من {_iplace}، أو تطلب كاترينگ"},{"role":"user","content":"الكاترينگ كيفه؟"},{"role":"assistant","content":f"زين وبسعر معقول، {random.randint(15,30)*1000:,} دينار للشخص"}]
    elif tpl == 20:
        msgs = [{"role":"user","content":f"{_rw}! {_mname}"},{"role":"assistant","content":"الله يبارك فيك، كل عام وأنت بخير"},{"role":"user","content":f"شلون العيد وياكم بـ{_city}؟"},{"role":"assistant","content":"الحمد لله، اجتمعنا بالعائلة وانبسطنا"},{"role":"user","content":"هاي أحلى شي بالعيد"},{"role":"assistant","content":"إي والله، الاجتماع بالأهل لا يعوضه شي"}]
    elif tpl == 21:
        msgs = [{"role":"user","content":f"صاحبي {_mname} توفي البارحة"},{"role":"assistant","content":"إنا لله وإنا إليه راجعون. عظم الله أجرك"},{"role":"user","content":"والله صدمت، كان إنسان طيب"},{"role":"assistant","content":f"{_sp}، الله يرحمه ويغفر له"},{"role":"user","content":"آمين. ويصبر أهله"},{"role":"assistant","content":"الله يرحمه"}]
    elif tpl == 22:
        meals3 = pick(["دولمة","مرق دجاج","پاچة","تشريب","برياني"])
        msgs = [{"role":"user","content":f"يا {_fw}، تعال نتغدى سوا"},{"role":"assistant","content":"حاضر، وين؟"},{"role":"user","content":f"البيت، أمي طبخت {meals3}"},{"role":"assistant","content":f"والله؟ {meals3} أمك؟ جاي هسه هسه!"},{"role":"user","content":"هههه يلا استعجل"},{"role":"assistant","content":"بالطريق"}]
    elif tpl == 23:
        msgs = [{"role":"user","content":f"عندي {_pw} مع جاري بـ{_iplace}"},{"role":"assistant","content":"شنو صار بينكم؟"},{"role":"user","content":"يرفع الصوت بالليل"},{"role":"assistant","content":"كلمه بهدوء أول، لو ما سمع اشكه للبلدية"},{"role":"user","content":"خايف يزعل"},{"role":"assistant","content":"الكلام الطيب يحل"}]
    elif tpl == 24:
        msgs = [{"role":"user","content":f"ولدي {_mname} نجح بدرجة عالية اليوم"},{"role":"assistant","content":f"{_pr}! الله يبارك فيه"},{"role":"user","content":"فرحنا هواي والله"},{"role":"assistant","content":"يستاهل، هذا ثمرة تعبه"},{"role":"user","content":"ربي يكمل عليه"},{"role":"assistant","content":"إن شاء الله دايماً يفرحكم"}]
    elif tpl == 25:
        msgs = [{"role":"user","content":f"شلون حال {_fname} بعد رجوعها من {_prov}؟"},{"role":"assistant","content":"بخير الحمد لله. أهلاً برجوعها"},{"role":"user","content":"شكراً، كانت مسافرة"},{"role":"assistant","content":"الله يسلمها"},{"role":"user","content":"تعالوا تشربون چاي"},{"role":"assistant","content":"حاضر، بالطريق"}]
    elif tpl == 26:
        bad_habit = pick(["يشوف منجمة","يلعب ورق","يدخن","يشرب","ما يصلي"])
        msgs = [{"role":"user","content":f"أخوي {_mname2} {bad_habit}، تنصحني شسوي؟"},{"role":"assistant","content":"هذا موضوع حساس، كلمه بهدوء ومحبة"},{"role":"user","content":"بس ما يسمع"},{"role":"assistant","content":"المستقبل بيد الله والإنسان بجهده يصنعه"},{"role":"user","content":"صح، أصبر وأدعيله"},{"role":"assistant","content":f"ربي يهديه، {_rw}"}]
    elif tpl == 27:
        work_issue = pick(["أخذ كريدتي","يتأخر ويحمل علي","يشتكي مني للمدير","يكذب"])
        msgs = [{"role":"user","content":f"عندي {_pw} مع زميلي {_mname} بالشغل بـ{_city}"},{"role":"assistant","content":"شنو صار بينكم؟"},{"role":"user","content":f"{work_issue} قدام الكل"},{"role":"assistant","content":"لازم تكلمه أول بأول وبهدوء"},{"role":"user","content":"وإذا ما نفع؟"},{"role":"assistant","content":"راجع المدير بهدوء وبالأدلة"}]
    elif tpl == 28:
        inlaw_dist = random.randint(1, 15)
        msgs = [{"role":"user","content":f"أهلي بـ{_prov} يريدون أرجع أسكن وياهم بعد الزواج"},{"role":"assistant","content":"وأنت إيش تريد؟"},{"role":"user","content":f"أريد استقلالية، بيتنا على بعد {inlaw_dist} كيلو"},{"role":"assistant","content":"شرحلهم بلطف إنك تحتاج خصوصية بس ستبقى قريب"},{"role":"user","content":"صعب"},{"role":"assistant","content":f"الكلام الطيب والاحترام يحل، {_sp}"}]
    elif tpl == 29:
        mental_issue = pick(["قلق","اكتئاب","ضغط","توتر","إرهاق نفسي"])
        msgs = [{"role":"user","content":f"صديقتي {_fname} تعاني {mental_issue}، كيف أساعدها؟"},{"role":"assistant","content":"اسمعيها بدون ما تحكمين عليها"},{"role":"user","content":f"الـ{mental_issue} صعب عليها هواي"},{"role":"assistant","content":"حثيها تزور دكتور نفسي، الصحة النفسية مهمة"},{"role":"user","content":"خايفة تزعل"},{"role":"assistant","content":"قوليها إنك تحبيها وتريدين ليها الأفضل"}]
    elif tpl == 30:
        msgs = [{"role":"user","content":f"أريد أنتقل للشغل بـ{_city}، شنو رأيك؟"},{"role":"assistant","content":f"{_city} فيها فرص زينة خصوصاً بقطاع النفط"},{"role":"user","content":f"بس بعيدة عن أهلي بـ{_prov}"},{"role":"assistant","content":"الغربة صعبة بالأول، بس الإنسان يتأقلم"},{"role":"user","content":"وإيجارات البيوت؟"},{"role":"assistant","content":f"معقولة بـ{_city} أكثر من بغداد"}]
    elif tpl == 31:
        missed = pick(["ما يصلي","ما يصوم","ما يروح الجامع","يسهر كثير"])
        msgs = [{"role":"user","content":f"صديقي {_mname} {missed} وأنا خايف عليه"},{"role":"assistant","content":"أنصحه بالكلام اللطيف والقدوة الحسنة"},{"role":"user","content":f"جربت بس ما قبل موضوع {missed}"},{"role":"assistant","content":"ادعيله وخليك قدوة بعملك"},{"role":"user","content":"صح، الدعاء أقوى"},{"role":"assistant","content":f"الله يهدينا ويهديه، {_rw}"}]
    elif tpl == 32:
        meals4 = pick(["قوزي","مندي","كباب","مسگوف","دولمة"])
        msgs = [{"role":"user","content":f"أريد أعزم أهل زوجتي أول مرة للعشاء"},{"role":"assistant","content":"هذي مناسبة زينة!"},{"role":"user","content":f"شنو أطبخ؟ {meals4}؟"},{"role":"assistant","content":f"{meals4} ممتاز للضيوف"},{"role":"user","content":"وإذا ما تطلع زينة؟"},{"role":"assistant","content":f"اطلب من مطعم بـ{_iplace}، ما أحد يلاحظ"}]
    elif tpl == 33:
        debt = random.randint(1, 5) * 1000000
        msgs = [{"role":"user","content":f"عندي دين {debt:,} دينار على {_mname2} من سنة"},{"role":"assistant","content":"كلمه مباشرة وذكره"},{"role":"user","content":"خايف تنكسر العلاقة"},{"role":"assistant","content":"العلاقة الحقيقية تتحمل المطالبة بالحق"},{"role":"user","content":"صح، بكلمه"},{"role":"assistant","content":"استخدم وساطة لو ما نفع الكلام المباشر"}]
    elif tpl == 34:
        grade_drop = random.randint(10, 40)
        study_yr = pick(["الأول","الثاني","الثالث","الرابع","الخامس","السادس"])
        msgs = [{"role":"user","content":f"ولدي {_mname} بالصف {study_yr}، درجاته نزلت {grade_drop} درجة"},{"role":"assistant","content":"شنو صاير فيه؟"},{"role":"user","content":"ما يركز، ويتأخر بالدراسة"},{"role":"assistant","content":"ابحث عن السبب: مشكلة مع الأصحاب؟ ضغط؟"},{"role":"user","content":"ما أدري"},{"role":"assistant","content":"كلمه بهدوء وبدون إدانة، واسمعه"}]
    elif tpl == 35:
        engage_dur = random.randint(1, 6)
        msgs = [{"role":"user","content":f"أختي {_fname} أخذت خطيب وأنا قلقانة"},{"role":"assistant","content":"ليش قلقانة؟"},{"role":"user","content":f"الشاب من {_city} وما نعرفه كثير، خطوبتهم {engage_dur} أشهر بس"},{"role":"assistant","content":"العائلة مسؤولة تسأل وتتحرى قبل العرس"},{"role":"user","content":"صح، أكلم أهلي"},{"role":"assistant","content":"الاطمئنان مهم قبل الخطوة الكبيرة"}]
    elif tpl == 36:
        msgs = [{"role":"user","content":f"أريد أبدأ مشروع {_food2} بيتي بـ{_prov}"},{"role":"assistant","content":"فكرة زينة! الطلب على الأكل البيتي كثير"},{"role":"user","content":"وين أبدأ؟"},{"role":"assistant","content":"من الواتساب والإنستغرام، صورة ووصفة يومياً"},{"role":"user","content":"ورأسمال؟"},{"role":"assistant","content":f"ابدأ بـ{random.randint(100,400)*1000:,} دينار"}]
    elif tpl == 37:
        gen_issue = pick(["الدراسة","الشغل","الزواج","الملابس","الأصحاب","الوقت"])
        gen_age = random.randint(18, 30)
        msgs = [{"role":"user","content":f"أحس إن أهلي بـ{_prov} ما يفهمون موضوع {gen_issue}، عمري {gen_age}"},{"role":"assistant","content":"الفجوة بين الأجيال طبيعية"},{"role":"user","content":f"بس يصعبون موضوع {gen_issue} كلش"},{"role":"assistant","content":"حاول تفهم منطقهم، هم خايفين عليك"},{"role":"user","content":"شنو أسوي؟"},{"role":"assistant","content":"تكلمهم بهدوء واشرح وجهة نظرك بالدليل"}]
    elif tpl == 38:
        msgs = [{"role":"user","content":f"صاحبي {_mname} يبي يسافر الخارج ويتركنا"},{"role":"assistant","content":"مو بده يتركك، بده يحسن حياته"},{"role":"user","content":"صح بس الصداقة تنقطع"},{"role":"assistant","content":"الصداقة الحقيقية تبقى حتى عن بعد"},{"role":"user","content":"صح والله"},{"role":"assistant","content":f"الله يوفقه ويوفقكم بـ{_prov}"}]
    elif tpl == 39:
        yrs_fight = random.randint(1, 10)
        fight_cause = pick(["كلام","ميراث","سوء فهم","مشكلة عائلية"])
        msgs = [{"role":"user","content":f"أريد أتصالح مع قريبي {_mname2} بعد {yrs_fight} سنين خلاف بسبب {fight_cause}"},{"role":"assistant","content":"قرار زين! صلة الرحم واجبة"},{"role":"user","content":"بس من يبدأ؟"},{"role":"assistant","content":"أنت ابدأ، صاحب المبادرة له الأجر"},{"role":"user","content":"يمكن يرفض"},{"role":"assistant","content":f"مسؤوليتك تمد يدك، {_sp}"}]
    elif tpl == 40:
        absent_t = random.randint(2, 12)
        last_visit = pick(["العيد","رمضان","الصيف","الشتاء","المناسبة الأخيرة"])
        msgs = [{"role":"user","content":f"شلونكم بـ{_prov}؟ آخر مرة شفناكم {last_visit}، من {absent_t} أشهر"},{"role":"assistant","content":"الحمد لله كلنا بخير. وأنتم؟"},{"role":"user","content":"كلنا تمام الحمد لله، مشتاقين لكم"},{"role":"assistant","content":"الله يديم النعمة"},{"role":"user","content":"متى تجون تزورونا؟"},{"role":"assistant","content":"قريب إن شاء الله"}]
    elif tpl == 41:
        hrs2 = random.randint(2, 6)
        msgs = [{"role":"user","content":f"أبو {_mname} راح {_city}، كيف السفر من {_prov}؟"},{"role":"assistant","content":"بالسيارة أحسن، الباص طويل"},{"role":"user","content":"شكد الطريق؟"},{"role":"assistant","content":f"حوالي {hrs2} ساعات"},{"role":"user","content":"والأمن؟"},{"role":"assistant","content":"الله يسلمكم، الطريق مأمون هالأيام"}]
    elif tpl == 42:
        budget2 = random.randint(5, 25) * 100000
        msgs = [{"role":"user","content":f"أريد أعزم العائلة على {_pfood}، وين أحسن؟"},{"role":"assistant","content":f"{_pfood}! أكلة أصيلة. مطعم قرب {_iplace}"},{"role":"user","content":"شكد يكلف للعائلة؟"},{"role":"assistant","content":f"ميزانية {budget2:,} دينار تكفي"},{"role":"user","content":"ممتاز، نروح"},{"role":"assistant","content":"إن شاء الله تنبسطون"}]
    elif tpl == 43:
        msgs = [{"role":"user","content":f"أم {_fname} تعبانة من الحمل وما تطبخ"},{"role":"assistant","content":"الله يعافيها! لازم ترتاح"},{"role":"user","content":"شسوي؟"},{"role":"assistant","content":f"اطلب {_pfood} من مطعم، راحتها أهم"},{"role":"user","content":"الله يشفيها"},{"role":"assistant","content":"إن شاء الله تقوم بالسلامة"}]
    elif tpl == 44:
        msgs = [{"role":"user","content":f"{_mname} يبي يفتح مشروع {_job2} بـ{_city}"},{"role":"assistant","content":"فكرة زينة!"},{"role":"user","content":f"من وين يبدأ مشروع {_job2}؟"},{"role":"assistant","content":"الغرفة التجارية ثم ترخيص، وشبكة علاقات"},{"role":"user","content":"وميزانية؟"},{"role":"assistant","content":f"يعتمد على المشروع، من {random.randint(2,10)*1000000:,} دينار"}]
    elif tpl == 45:
        amt2 = random.randint(1, 10) * 500000
        msgs = [{"role":"user","content":f"أريد أبعث {amt2:,} دينار لـ{_mname2} بـ{_city}"},{"role":"assistant","content":"زين كاش أو آسيا حوالة أسرع"},{"role":"user","content":"الأجرة شكد؟"},{"role":"assistant","content":"1-2% من المبلغ"},{"role":"user","content":"وهل وصول فوري؟"},{"role":"assistant","content":"إي، نفس الدقيقة"}]
    elif tpl == 46:
        shrine2 = pick(["النجف","كربلاء"])
        msgs = [{"role":"user","content":f"أم {_fname} تبي تزور {shrine2} من {_prov}"},{"role":"assistant","content":"زيارة مباركة! متى تروحون؟"},{"role":"user","content":"ليلة الجمعة"},{"role":"assistant","content":"إن شاء الله ترجعون بالسلامة والقبول"},{"role":"user","content":"آمين، ادعيلنا"},{"role":"assistant","content":"الله يقبل زيارتكم"}]
    elif tpl == 47:
        msgs = [{"role":"user","content":f"ولدي {_mname} نجح وراح يشتغل {_job} بـ{_city}"},{"role":"assistant","content":"مبارك! الله يبارك فيه"},{"role":"user","content":"فرحان هواي والله"},{"role":"assistant","content":"يستاهل، تعب وحصل"},{"role":"user","content":"ربي يكمل عليه"},{"role":"assistant","content":"إن شاء الله دايماً يفرحكم"}]
    elif tpl == 48:
        msgs = [{"role":"user","content":f"أخوي {_mname2} يشتغل بـ{_city} وما يجي يزورنا من سنة"},{"role":"assistant","content":"الشغل يشغل، بس لازم يجي"},{"role":"user","content":"مشتاقين له"},{"role":"assistant","content":"كلمه وذكره بأهمية العائلة"},{"role":"user","content":"أخاف يزعل"},{"role":"assistant","content":"العائلة ما تزعل من بعض"}]
    elif tpl == 49:
        ppl3 = random.randint(30, 80)
        msgs = [{"role":"user","content":f"عندي حفلة سابع {_fname} لـ{ppl3} شخص"},{"role":"assistant","content":"مبارك! شكد تعزم؟"},{"role":"user","content":f"{ppl3} شخص"},{"role":"assistant","content":"قاعة صغيرة أنيق وريح باله"},{"role":"user","content":f"وأكل {_pfood} يناسب؟"},{"role":"assistant","content":"ممتاز، الكل يحبه"}]
    elif tpl == 50:
        promo_yrs = random.randint(1, 5)
        msgs = [{"role":"user","content":f"زميلي {_mname} ترقى بعد {promo_yrs} سنين وأنا ما ترقيت"},{"role":"assistant","content":"شنو شعورك؟"},{"role":"user","content":"زعلان بس ما أريد أظهر"},{"role":"assistant","content":f"طبيعي. اسأل مديرك شنو ينقصك للترقية"},{"role":"user","content":"صح، لازم أتطور"},{"role":"assistant","content":f"ربي يوفقك، {_pr}"}]
    elif tpl == 51:
        bride_job = pick(["طالبة","معلمة","دكتورة","مهندسة","موظفة"])
        msgs = [{"role":"user","content":f"أريد أتزوج من بنت {bride_job} من {_city}، شنو رأيك؟"},{"role":"assistant","content":f"ناس {_city} محترمون. المهم الكفاءة والأخلاق"},{"role":"user","content":f"أخاف الفرق الجغرافي بين {_city} و{_prov} مشكلة"},{"role":"assistant","content":"مو مشكلة لو الاثنين راضيين ومتفاهمين"},{"role":"user","content":"صح"},{"role":"assistant","content":"ربي يوفقك"}]
    elif tpl == 52:
        n3 = random.randint(20, 100)
        msgs = [{"role":"user","content":f"عندي عرس لـ{n3} شخص، شنو أطبخ؟"},{"role":"assistant","content":f"{_pfood} خيار ممتاز للأعراس"},{"role":"user","content":"بقدر أطبخ بيتياً؟"},{"role":"assistant","content":"للأعداد الكبيرة أفضل طباخ أعراس"},{"role":"user","content":"شكد يكلف؟"},{"role":"assistant","content":f"{random.randint(3,8)*1000:,} دينار للشخص"}]
    elif tpl == 53:
        age3 = random.randint(15, 40)
        msgs = [{"role":"user","content":f"أريد هدية ليوم ميلاد {_fname2}، عمرها {age3}"},{"role":"assistant","content":"شنو تحب؟"},{"role":"user","content":"تحب العطور والإكسسوار"},{"role":"assistant","content":"عطر فاخر هدية ممتازة"},{"role":"user","content":"الميزانية المناسبة؟"},{"role":"assistant","content":f"بين {random.randint(50,200)*1000:,} دينار"}]
    elif tpl == 54:
        msgs = [{"role":"user","content":f"ابن {_mname} سُلب موبايله بالشارع قرب {_iplace}"},{"role":"assistant","content":"الله يحفظه! شنو صار؟"},{"role":"user","content":"جاه شخص على موتور وسلبه"},{"role":"assistant","content":"روحوا تبلغوا الشرطة بأسرع وقت"},{"role":"user","content":"وفائدة التبليغ؟"},{"role":"assistant","content":"توثيق الحادثة مهم، وأحياناً يلقوهم"}]
    elif tpl == 55:
        neighbor_origin = pick(["من {_prov}","من محافظة ثانية","غرباء","عائلة شبابية","عائلة كبيرة"])
        gift = pick(["تمر","حلويات","فاكهة","خبز تنور","چاي"])
        msgs = [{"role":"user","content":f"الجيران الجدد {neighbor_origin} جنبنا بـ{_city}، كيف أتعرف عليهم؟"},{"role":"assistant","content":"روح قدمهم بنفسك مع هدية صغيرة"},{"role":"user","content":f"وش أحمل؟ {gift}؟"},{"role":"assistant","content":f"{gift} ممتاز، الكل يحبه"},{"role":"user","content":"صح، أروح بكره"},{"role":"assistant","content":"الجار قبل الدار"}]
    elif tpl == 56:
        myage2 = random.randint(30, 50)
        msgs = [{"role":"user","content":f"أريد أكمل دراستي وعمري {myage2} سنة"},{"role":"assistant","content":"ما في عمر للتعليم"},{"role":"user","content":"أخاف ما أنافس الشباب"},{"role":"assistant","content":f"خبرتك تعوضك، والجامعات المسائية بـ{_prov} مناسبة"},{"role":"user","content":"فكرة زينة"},{"role":"assistant","content":"الله يوفقك"}]
    elif tpl == 57:
        msgs = [{"role":"user","content":f"عندي خلاف مع أختي {_fname} على ميراث بـ{_prov}"},{"role":"assistant","content":"الميراث موضوع حساس. شنو الخلاف؟"},{"role":"user","content":"تريد أكثر من حقها الشرعي"},{"role":"assistant","content":"وساطة شخص مؤثر بالعائلة أحسن من المحكمة"},{"role":"user","content":"ما أريد نخسر بعض"},{"role":"assistant","content":"الكلام الطيب يحل أكثر من القضاء"}]
    elif tpl == 58:
        donate_amt = random.randint(50, 500) * 1000
        donate_type = pick(["كفالة يتيم","أرملة","طالب فقير","مريض","أسرة محتاجة"])
        msgs = [{"role":"user","content":f"أريد أتبرع {donate_amt:,} دينار لجمعية خيرية بـ{_city}"},{"role":"assistant","content":"إن شاء الله يتقبل. ابحث عن الجمعيات المعتمدة"},{"role":"user","content":"أحسن نوع تبرع؟"},{"role":"assistant","content":f"{donate_type}، دايم ومتواصل"},{"role":"user","content":"زين، أبحث"},{"role":"assistant","content":"الله يبارك فيك ويضاعف أجرك"}]
    elif tpl == 59:
        msgs = [{"role":"user","content":f"أبو {_mname2} يعاني وحدة بعد وفاة زوجته بـ{_prov}"},{"role":"assistant","content":"الله يرحمها. الوحدة صعبة"},{"role":"user","content":"شنو نسوي له؟"},{"role":"assistant","content":"خليه يشارك بمجالس اجتماعية، والزيارة المتكررة مهمة"},{"role":"user","content":"والتلفون؟"},{"role":"assistant","content":"علمه واتساب فيديو، يفرق هواي"}]
    elif tpl == 60:
        msgs = [{"role":"user","content":f"أهلنا بـ{_city} ما زارونا من زمان {_mname}"},{"role":"assistant","content":"الناس مشغولين هالأيام"},{"role":"user","content":"مشتاقين لهم"},{"role":"assistant","content":"اتصل فيهم وعزمهم"},{"role":"user","content":"صح، نروح بالعطلة"},{"role":"assistant","content":"الله يجمعكم على خير"}]
    elif tpl == 61:
        budget_house = random.randint(50, 300) * 1000000
        rooms_house = random.randint(2, 5)
        msgs = [{"role":"user","content":f"أريد أشتري بيت {rooms_house} غرف بـ{_city}، ميزانيتي {budget_house:,}"},{"role":"assistant","content":"يعتمد على الحي، أيش تفضل؟"},{"role":"user","content":"حي هادي وقريب من المدارس"},{"role":"assistant","content":f"أطراف {_city} أرخص وهادية"},{"role":"user","content":"والشراء أحسن من الإيجار؟"},{"role":"assistant","content":"على المدى البعيد نعم"}]
    elif tpl == 62:
        msgs = [{"role":"user","content":f"شنو أطبخ لضيوف جايين من {_prov}؟ {_food} أو {_food2}؟"},{"role":"assistant","content":f"{_pfood} للضيوف أفضل، أكلة أصيلة"},{"role":"user","content":f"بس {_food} أسهل"},{"role":"assistant","content":"لو مستعجل اختر الأسهل، المهم الاهتمام"},{"role":"user","content":"صح، شكراً"},{"role":"assistant","content":"بالتوفيق"}]
    elif tpl == 63:
        rel_type = pick(["أعمامي","أخوالي","أقاربي من جهة أمي","عشيرتي"])
        visit_freq = pick(["ما يردون","نادراً ما يجون","بعيدين عنا"])
        msgs = [{"role":"user","content":f"كيف أحسن علاقتي مع {rel_type} بـ{_city}؟ {visit_freq}"},{"role":"assistant","content":"زيارات منتظمة وتواصل دائم"},{"role":"user","content":"وإذا ما يردون على التواصل؟"},{"role":"assistant","content":"استمر أنت، الإنسان يتأقلم ويرد"},{"role":"user","content":"صح، أصبر"},{"role":"assistant","content":"صلة الرحم واجبة"}]
    elif tpl == 64:
        color = pick(["بيج","أزرق فاتح","رمادي","أخضر فاتح","أبيض مكسور"])
        decor_budget = random.randint(1, 10) * 1000000
        msgs = [{"role":"user","content":f"أريد أعيد تزيين بيتنا بـ{_city}، ميزانية {decor_budget:,}"},{"role":"assistant","content":"فكرة حلوة! شنو تريد تغير؟"},{"role":"user","content":f"الألوان، أفضل {color}؟"},{"role":"assistant","content":f"{color} لون هادي وأنيق، يريح العين"},{"role":"user","content":"وأثاث جديد؟"},{"role":"assistant","content":f"شوف معارض أثاث {_city}، أسعار تنافسية"}]
    elif tpl == 65:
        time_of_day = pick(["الصباح","العصر","المساء","الليل"])
        activity = pick(["مشي","رياضة","قراءة","صور","قهوة"])
        msgs = [{"role":"user","content":f"شنو أسوي بـ{_iplace} وقت {time_of_day}؟"},{"role":"assistant","content":f"{activity} هناك ممتاز وهواء منعش"},{"role":"user","content":"وبالليل؟"},{"role":"assistant","content":"الكافيهات قريبة وأجواء حلوة"},{"role":"user","content":"تجي معي؟"},{"role":"assistant","content":f"إي ماشي {_mname}، باچر نروح"}]
    elif tpl == 66:
        mig_reason = pick(["الشغل","الدراسة","الأمان","البحث عن مستقبل أفضل"])
        msgs = [{"role":"user","content":f"شنو رأيك بالشباب اللي يهاجرون من {_prov} بسبب {mig_reason}؟"},{"role":"assistant","content":"الهجرة قرار صعب، بس أحياناً الظروف تفرض"},{"role":"user","content":"تفتكر صح أو غلط؟"},{"role":"assistant","content":"لا صح ولا غلط، يعتمد على كل شخص وظرفه"},{"role":"user","content":"صح"},{"role":"assistant","content":"ربنا يوفق الجميع"}]
    elif tpl == 67:
        msgs = [{"role":"user","content":f"أريد أسافر مع عائلتي لـ{_city} للعطلة"},{"role":"assistant","content":"فكرة ممتازة! شنو تحب تشوف هناك؟"},{"role":"user","content":"أماكن سياحية وأكل شعبي"},{"role":"assistant","content":f"في {_iplace} وأكل {_pfood} أصيل"},{"role":"user","content":"ممتاز، نحجز"},{"role":"assistant","content":"إن شاء الله تنبسطون"}]
    elif tpl == 68:
        son_age = random.randint(20, 35)
        son_job = pick(["مهندس","دكتور","معلم","موظف","محاسب"])
        msgs = [{"role":"user","content":f"أريد أزوج ابني {_mname}، عمره {son_age} ويشتغل {son_job}"},{"role":"assistant","content":"الله يوفقه. شنو تبحث عن؟"},{"role":"user","content":f"بنت محترمة ومتعلمة من {_city}"},{"role":"assistant","content":"الأسرة الطيبة والتعليم أهم معيار"},{"role":"user","content":"وين أبحث؟"},{"role":"assistant","content":"أهل وأقارب ومعارف، خير وسيلة"}]
    elif tpl == 69:
        charity_type = pick(["مطبخ خيري","حملة ملابس","سلل رمضانية","توزيع كتب","دعم أيتام"])
        charity_budget = random.randint(1, 20) * 500000
        msgs = [{"role":"user","content":f"أريد أسوي {charity_type} بـ{_prov}، ميزانية {charity_budget:,}"},{"role":"assistant","content":f"فكرة عظيمة! {charity_type} مبادرة رائعة"},{"role":"user","content":"وين أبدأ؟"},{"role":"assistant","content":"ابدأ بالتواصل مع الجمعيات المحلية"},{"role":"user","content":"وتمويل إضافي؟"},{"role":"assistant","content":"حملة تبرعات على السوشيال ميديا تنجح هالأيام"}]
    elif tpl == 70:
        msgs = [{"role":"user","content":f"صاحبي {_mname2} طلب مني أقرضه فلوس"},{"role":"assistant","content":"شكد؟"},{"role":"user","content":f"{random.randint(1,5)*500000:,} دينار"},{"role":"assistant","content":"إذا أقرضته، كن جاهز إنه ما يرد بسرعة"},{"role":"user","content":"وإذا رفضت؟"},{"role":"assistant","content":"من حقك، لا تحرج نفسك لو ما تقدر"}]
    elif tpl == 71:
        video_type = pick(["فيديو سياحي","تجوال","أكل شعبي","تراث","حياة يومية"])
        followers = random.randint(500, 50000)
        msgs = [{"role":"user","content":f"أريد أسوي {video_type} عن {_iplace} للسوشيال ميديا، عندي {followers:,} متابع"},{"role":"assistant","content":"فكرة حلوة! الأماكن العراقية تجذب"},{"role":"user","content":"كيف أصور بشكل احترافي؟"},{"role":"assistant","content":"الموبايل كافي، المهم الإضاءة والزاوية"},{"role":"user","content":"وتيك توك أو يوتيوب؟"},{"role":"assistant","content":"ابدأ بتيك توك، أسرع انتشار"}]
    elif tpl == 72:
        msgs = [{"role":"user","content":f"أريد أسجل ولدي {_mname} بمدرسة زينة بـ{_prov}"},{"role":"assistant","content":"شنو تبحث عن بالمدرسة؟"},{"role":"user","content":"مستوى تعليمي وانضباط"},{"role":"assistant","content":"اسأل الجيران عن تجربتهم، أفضل معلومة"},{"role":"user","content":"صح، أسأل الأهل"},{"role":"assistant","content":"الله يوفق ولدك"}]
    elif tpl == 73:
        wife_job_field = pick(["تعليم","صحة","محاسبة","تصميم","إدارة"])
        marriage_yrs = random.randint(1, 5)
        msgs = [{"role":"user","content":f"زوجتي {_fname} تريد تشتغل بمجال {wife_job_field} بعد {marriage_yrs} سنين زواج"},{"role":"assistant","content":"شنو رأيك أنت؟"},{"role":"user","content":"أنا موافق بس أهلي مو موافقين"},{"role":"assistant","content":"الزوجة لها حق الشغل، الحوار مع الأهل بهدوء"},{"role":"user","content":"صح"},{"role":"assistant","content":f"التفاهم بينكم هو الأهم، {_sp}"}]
    elif tpl == 74:
        skill = pick(["تصوير","مونتاج","برمجة","تصميم جرافيك","كتابة محتوى","تسويق"])
        learn_time = random.randint(1, 6)
        msgs = [{"role":"user","content":f"أريد أتعلم {skill} خلال {learn_time} أشهر، شنو تنصح {_mname2}؟"},{"role":"assistant","content":f"سوق {skill} واسع هالأيام"},{"role":"user","content":f"صعب أتعلم {skill} لوحدي؟"},{"role":"assistant","content":f"يوتيوب مجاني وكافي للبداية بـ{skill}"},{"role":"user","content":"وكورس مدفوع؟"},{"role":"assistant","content":"بعد ما تأسس، الكورس يسرع التقدم"}]
    elif tpl == 75:
        msgs = [{"role":"user","content":f"أريد أعمل حفلة تخرج {_mname} بـ{_city}"},{"role":"assistant","content":"مبارك! شكد تفكر تعزم؟"},{"role":"user","content":f"حوالي {random.randint(30,80)} شخص"},{"role":"assistant","content":"قاعة أو مطعم مناسبين لهذا العدد"},{"role":"user","content":"وأكل؟"},{"role":"assistant","content":f"{_pfood} مناسب للحفلات"}]
    elif tpl == 76:
        absence_yrs = random.randint(1, 4)
        son_loc = pick(["الخارج","مدينة ثانية","السعودية","تركيا","أمريكا"])
        msgs = [{"role":"user","content":f"ابني {_mname} بـ{son_loc} من {absence_yrs} سنين، مشتاق هواي له"},{"role":"assistant","content":"الله يجمعكم على خير"},{"role":"user","content":"ما أشوفه إلا بالفيديو كول"},{"role":"assistant","content":"الفيديو كول يخفف الشوق، بس الزيارة أفضل"},{"role":"user","content":"ما يكفي والله"},{"role":"assistant","content":"متى تقدر تزوره هناك؟"}]
    elif tpl == 77:
        old_rent = random.randint(2, 8) * 100000
        new_rent = old_rent + random.randint(1, 5) * 100000
        msgs = [{"role":"user","content":f"صاحب بيتنا بـ{_city} يريد يرفع الإيجار من {old_rent:,} لـ{new_rent:,}"},{"role":"assistant","content":"تفاوض معه، وإذا ما نفع ابحث عن بديل"},{"role":"user","content":f"الإيجار غالي كلش هالأيام بـ{_city}"},{"role":"assistant","content":f"أطراف {_city} أرخص بكثير"},{"role":"user","content":"صح، أبحث"},{"role":"assistant","content":"الله يوفقك"}]
    elif tpl == 78:
        child_age = random.randint(5, 15)
        parenting_challenge = pick(["الموبايل","الأصحاب السيئين","الألعاب","الإنترنت","التلفزيون"])
        msgs = [{"role":"user","content":f"ولدي {_mname} عمره {child_age}، كيف أتعامل مع موضوع {parenting_challenge}؟"},{"role":"assistant","content":"التربية هالأيام أصعب من قبل"},{"role":"user","content":f"الـ{parenting_challenge} يؤثر عليه كثير"},{"role":"assistant","content":f"حدد وقت للـ{parenting_challenge} وكن قدوة"},{"role":"user","content":"شنو الحل؟"},{"role":"assistant","content":"حوار دائم مع الأطفال وقدوة حسنة"}]
    elif tpl == 79:
        msgs = [{"role":"user","content":f"أريد أشارك بمهرجان {_pfood} العراقي بـ{_prov}"},{"role":"assistant","content":"فكرة رائعة! شنو تقدم؟"},{"role":"user","content":f"وصفة {_pfood} عائلية قديمة"},{"role":"assistant","content":"الوصفات التراثية تجذب الجمهور أكثر"},{"role":"user","content":"كيف أتقدم؟"},{"role":"assistant","content":"تواصل مع منظمي المهرجان بالسوشيال ميديا"}]
    else:
        msgs = [{"role":"user","content":f"شلونكم بـ{_prov}؟ {_mname} بخير؟"},{"role":"assistant","content":"الحمد لله كلنا بخير. وأنتم؟"},{"role":"user","content":f"كلنا تمام. {_fname2} سألت عنكم"},{"role":"assistant","content":f"الله يخليها، سلمي عليها"},{"role":"user","content":"متى تجون تزورونا؟"},{"role":"assistant","content":"قريب إن شاء الله، الله يجمعنا"}]

    return {"id":f"social_{i:04d}","category":"social_family","dialect":"iraqi_arabic","messages":msgs}

# ============================================================
# FILE 10 - MIXED (Sales + General)
# ============================================================

def gen_mixed(i):
    choice = random.randint(1, 10)
    if choice == 1:
        return gen_elec(i)
    elif choice == 2:
        return gen_food(i)
    elif choice == 3:
        return gen_clothes(i)
    elif choice == 4:
        return gen_cars(i)
    elif choice == 5:
        return gen_realestate(i)
    elif choice == 6:
        return gen_furniture(i)
    elif choice == 7:
        return gen_services(i)
    elif choice == 8:
        return gen_daily(i)
    elif choice == 9:
        return gen_social(i)
    else:
        r = pick([gen_elec, gen_food, gen_clothes, gen_cars, gen_realestate,
                  gen_furniture, gen_services, gen_daily, gen_social])
        return r(i)

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

