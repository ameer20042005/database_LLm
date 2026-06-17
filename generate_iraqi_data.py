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
]


EXPENSIVE = [
    "هذا غالي هواي","غالي مو طبيعي","والله هذا ما ينفع",
    "هاي زيادة هواي","مو معقول هالسعر","كلش غالي",
    "هذا يطيح منه","ما عندي هالفلوس","صعب شوية على السعر",
    "هاي أكثر مما توقعت","ما تحط سعر أرخص؟",
]

DISC_REQ = [
    "تنزل شوية؟","ما تحط سعر أحسن؟","ما تعطيني تخفيض؟",
    "ما تحسن السعر شوية؟","ما تنزل علي؟","بعد شبي مجال",
    "ما أكو خصم؟","بعد شبي مجال صاحبي","گول سعر ثاني",
    "ما تعطيني بسعر زين؟","عندك خصم للزبون المعميل",
]

DISC_YES = [
    "ما اكدر بعد , أنزل عليك شوية بس هاي آخر سعر",
    "لأنك أنت، نزل بالسعر علي بس هاي آخر سعر والله",
    "زين، على خاطرك نزل شوي ",
    "ماشي بس ما أكدر أنزل أكثر من هيچي",
    "اروح فدوه الك ، بس هذا آخر سعر",
    "والله على خاطرك، هذا آخر سعر",
    "ماشي يا حجي، على خاطرك",
]

DISC_NO = [
    "والله أخوي هذا آخر سعر، ما أكدر أنزل",
    "هذا سعر نار، ما أكدر أنزل عليه",
    "والله ما أكدر، رأس مالي موجود",
    "هذا سعر التكلفة، صعب أنزل عليه",
    "هالسعر ما موجود في السوق، أرخص ما أكو",
    "صدق والله ما أكدر، هذا آخر سعر",
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
]

THINK = [
    "بفكر شوية وأرجع","لازم أستشير","راح أفكر وأرجع إن شاء الله",
    "خلني أشوف أول","محتاج وقت للتفكير","راح أتصل وأعوّد",
]

COME_BACK = [
    "ماشي، شوكت تقرر تعال نكمل","تفضل أخوي في أي وقت",
    "باب المحل مفتوح، تعال بأي وقت","حياك الله بأي وقت",
]

def pick(lst):
    return random.choice(lst)

def vp(price, lo=0.93, hi=1.07):
    return f"{int(price * random.uniform(lo, hi) / 1000) * 1000:,}"

def howmuch():
    """Returns a random Iraqi dialect phrase for 'how much'"""
    return random.choice(["بيش", "شكد السعر", "بيش سعره", "شكد"])

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
    tpl = random.randint(1, 10)

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
            {"role":"user","content":f"{pick(SHORT_GREET)}، أبي {p['n']} بس ما عندي ناقص فلوس"},
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
    else:
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
    tpl = random.randint(1, 10)

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
    else:
        msgs = [
            {"role":"user","content":f"مرحبا، عندكم {item['n']}؟"},
            {"role":"assistant","content":f"إي عندنا، بـ{vp(item['p'])} دينار الـ{item['unit']}"},
            {"role":"user","content":f"أريد {qty} {item['unit']}"},
            {"role":"assistant","content":f"الكل {vp(item['p']*qty)} دينار"},
            {"role":"user","content":"هاي"},
            {"role":"assistant","content":f"{pick(CLOSE)}"},
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
    tpl = random.randint(1, 10)

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
    else:
        _gc, _gs = greet_pair()
        msgs = [
            {"role":"user","content":_gc},
            {"role":"assistant","content":_gs},
            {"role":"user","content":f"شنو عندكم جديد؟"},
            {"role":"assistant","content":f"عندنا كولكشن جديد. {item['n']} بـ{vp(item['p'])} دينار، {item['f']}"},
            {"role":"user","content":f"يعجبني، أاخذه"},
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
]

def gen_cars(i):
    car = pick(CARS)
    car2 = pick(CARS)
    while car2["n"] == car["n"]:
        car2 = pick(CARS)
    tpl = random.randint(1, 10)

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
            {"role":"user","content":f"هلو، أبي {car['n']} لكن ميزانيتي محدودة"},
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
    else:
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
]

def gen_realestate(i):
    prop = pick(PROPERTIES)
    tpl = random.randint(1, 10)

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
            {"role":"user","content":"أبي أكثر من هذا"},
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
            {"role":"user","content":f"{pick(SHORT_GREET)}، أبي {prop['n']} بس ما أعرف المنطقة زينة ولا لا"},
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
    else:
        _gc, _gs = greet_pair()
        msgs = [
            {"role":"user","content":_gc},
            {"role":"assistant","content":_gs},
            {"role":"user","content":f"أبي {prop['n']} بـ{prop['area']}"},
            {"role":"assistant","content":f"عندنا {prop['n']} بـ{prop['area']}، {prop['f']}. بـ{vp(prop['p'])} دينار"},
            {"role":"user","content":"أشوفه؟"},
            {"role":"assistant","content":"تفضل أي وقت"},
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
    tpl = random.randint(1, 10)

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
            {"role":"user","content":f"سلام، أريد {item['n']} بس أبي أشوف عينات القماش"},
            {"role":"assistant","content":"تفضل، عندنا عينات أكثر من 20 لون ونوع قماش"},
            {"role":"user","content":"يا لون يناسب غرفة بيضاء؟"},
            {"role":"assistant","content":"للغرفة البيضاء، الرمادي أو البيج يطلع حلو هواي"},
            {"role":"user","content":"أاخذ الرمادي"},
            {"role":"assistant","content":f"ممتاز! {vp(item['p'])} دينار. {pick(CLOSE)}"},
        ]
    else:
        msgs = [
            {"role":"user","content":f"{pick(SHORT_GREET)}، شنو عندكم من {item['n']}؟"},
            {"role":"assistant","content":f"عندنا {item['n']} ممتاز. {item['f']}. بـ{vp(item['p'])} دينار"},
            {"role":"user","content":f"{pick(DISC_REQ)}"},
            {"role":"assistant","content":f"{pick(DISC_YES)}"},
            {"role":"user","content":"ماشي"},
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
]

def gen_services(i):
    svc = pick(SERVICES)
    tpl = random.randint(1, 10)

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
    else:
        msgs = [
            {"role":"user","content":f"{pick(SHORT_GREET)}، أريد {svc['n']}"},
            {"role":"assistant","content":f"هلا، تفضل. شنو المشكلة؟"},
            {"role":"user","content":"مشكلة بسيطة بس محتاجة تصليح"},
            {"role":"assistant","content":f"ماشي، نشوف. تقريباً {vp(svc['p'])} دينار"},
            {"role":"user","content":"شوكت؟"},
            {"role":"assistant","content":"غداً إن شاء الله"},
        ]

    return {"id":f"svc_{i:04d}","category":"services","dialect":"iraqi_arabic","messages":msgs}

# ============================================================
# FILE 8 - DAILY LIFE CONVERSATIONS
# ============================================================

DAILY_TOPICS = [
    "الطقس","الأكل","العمل","المدرسة","الصحة","المواصلات","الكهرباء","الماء","الأخبار","الرياضة"
]

def gen_daily(i):
    tpl = random.randint(1, 20)

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
    else:
        msgs = [
            {"role":"user","content":"أبوك بخير؟"},
            {"role":"assistant","content":"الحمد لله بخير. وعائلتك؟"},
            {"role":"user","content":"كلهم بخير والحمد لله"},
            {"role":"assistant","content":"الله يحفظهم ويخليهم"},
            {"role":"user","content":"آمين، الله يسمع منك"},
            {"role":"assistant","content":"حياك الله، دايماً"},
        ]

    return {"id":f"daily_{i:04d}","category":"daily_life","dialect":"iraqi_arabic","messages":msgs}

# ============================================================
# FILE 9 - SOCIAL & FAMILY CONVERSATIONS
# ============================================================

def gen_social(i):
    tpl = random.randint(1, 20)

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
    else:
        msgs = [
            {"role":"user","content":"شلون حال أم محمد؟"},
            {"role":"assistant","content":"بخير الحمد لله، وين أنت؟ ما شفناك"},
            {"role":"user","content":"كنت مسافر"},
            {"role":"assistant","content":"أهلاً وسهلاً برجوعك، الله يسلمك"},
            {"role":"user","content":"الله يخليك"},
            {"role":"assistant","content":"تفضل اشرب چاي معنا"},
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
        for i in range(1000):
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
