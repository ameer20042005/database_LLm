#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Iraqi Sales Data Scraper — مُختبر ومُتحقق
يقشط بيانات البيع العراقية ويحوّلها لصيغة JSON للتدريب

المصادر المُتحققة:
  1. sooq.iq        — سيارات عراقية حقيقية (يعمل، 33 إعلان/صفحة)
  2. iq.opensooq.com — إلكترونيات وعقارات (يعمل بمسارات محددة)
  3. bazarak.com/iraq — سوق متنوع (تجريبي)

الاستخدام:
  venv\\Scripts\\python scrape_iraqi_sales.py
  venv\\Scripts\\python scrape_iraqi_sales.py --pages 10
  venv\\Scripts\\python scrape_iraqi_sales.py --source sooq --pages 20
  venv\\Scripts\\python scrape_iraqi_sales.py --merge iraqi_training_data/iraqi_train_04_cars.json
"""

import sys
import io
import json
import time
import random
import re
import argparse
import os
from datetime import datetime

import requests
from bs4 import BeautifulSoup
from fake_useragent import UserAgent

# ── إصلاح encoding على Windows ───────────────────────────
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8", errors="replace")
sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding="utf-8", errors="replace")

# ── إعدادات ───────────────────────────────────────────────
OUTPUT_DIR = "scraped_data"
os.makedirs(OUTPUT_DIR, exist_ok=True)

ua = UserAgent()
DELAY_MIN = 1.5
DELAY_MAX = 3.5

SESSION = requests.Session()
USD_TO_IQD = 1310


def _headers():
    return {
        "User-Agent": ua.random,
        "Accept-Language": "ar,en;q=0.9",
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
        # بدون br لأن requests لا يدعم brotli افتراضياً
        "Accept-Encoding": "gzip, deflate",
    }


def _get(url, retries=3):
    for attempt in range(retries):
        try:
            r = SESSION.get(url, headers=_headers(), timeout=15)
            if r.status_code == 200:
                return r
            if r.status_code in (410, 404, 403):
                print(f"  [!] HTTP {r.status_code} — تخطي: {url[:60]}")
                return None
            print(f"  [!] HTTP {r.status_code} — محاولة {attempt+1}/{retries}")
        except Exception as e:
            print(f"  [!] خطأ محاولة {attempt+1}/{retries}: {str(e)[:60]}")
        time.sleep(random.uniform(2, 4))
    return None


def _sleep():
    time.sleep(random.uniform(DELAY_MIN, DELAY_MAX))


def _clean(text):
    if not text:
        return ""
    text = re.sub(r"\s+", " ", text.strip())
    return text[:200]


# ── قوالب بناء المحادثة ───────────────────────────────────

GREET_PAIRS = [
    ("السلام عليكم", "وعليكم السلام، هلا وغلا! كيف أكدر أساعدك؟"),
    ("هلو", "هلا، أهلاً وسهلاً! تفضل شنو تريد؟"),
    ("مرحبا", "مرحبتين! شنو أكدر أساعدك؟"),
    ("صباح الخير", "صباح النور! هلا وغلا تفضل"),
    ("مساء الخير", "مساء النور! هلا وسهلاً تفضل"),
    ("هلا", "هلا بيك! تفضل شتريد؟"),
]

PRICE_Q    = ["بيش سعره؟", "شكد السعر؟", "بيش؟", "شكد؟", "شكد يكلف؟", "الثمن شكد؟", "شكد سعره؟"]
DISC_REQ   = ["ما تنزل شوية؟", "ما تعطيني خصم؟", "تحسن السعر؟", "ما أكو خصم؟", "سعر ثاني ما أكو؟", "نزل علي شوي", "تخفض الثمن شوي؟"]
DISC_YES   = ["زين، على خاطرك نزلت شوي", "ماشي بس هذا آخر سعر", "حاضر، على خاطرك", "فدوة الك، بس هذا آخر سعر", "تفضل، ماشي"]
DISC_NO    = ["والله هذا آخر سعر، ما أكدر أنزل", "هذا سعر نار ما أكدر", "صدك ما أكدر، رأس مالي موجود", "ما يصير أخوي", "مو بيدي أكثر من هيج"]
EXPENSIVE  = ["هذا غالي هواي", "مو معقول هالسعر", "كلش غالي", "هاي زيادة هواي", "مو طبيعي هالسعر"]
CLOSE      = ["الله يبارك فيك، مشكور", "مبارك عليك", "تسلم وتغنم", "شكراً على تعاملك", "بالعافية عليك", "دمت بخير"]
WARRANTY   = ["عنده ضمان؟", "الضمان شكد؟", "في ضمان؟", "ضمان موجود؟"]
WARRANTY_A = ["إي عنده ضمان سنة كاملة", "ضمان 6 أشهر من عندنا", "ضمان الشركة سنة", "إي ضمانة موجودة"]
CONDITION  = ["حالته شنو؟", "شلون حاله؟", "بيه عيب؟", "حاله زين؟"]
COND_GOOD  = ["حاله ممتاز، ما بيه أي عيب", "حالة أول بس مستعمل", "خاصية جداً، مثل الجديد", "حالة كويسة والله"]


def _pick(lst):
    return random.choice(lst)


def _make_car_conversation(car_data):
    """يبني محادثة بيع سيارة من بيانات حقيقية"""
    brand   = car_data.get("brand", "")
    model   = car_data.get("model", "")
    year    = car_data.get("year", "")
    mileage = car_data.get("mileage", "")
    price   = car_data.get("price_iqd", car_data.get("price_usd", "السعر بالتواصل"))
    city    = car_data.get("city", "")

    car_desc = f"{brand} {model} {year}".strip()
    if mileage:
        car_desc += f"، {mileage} على العداد"

    greet_c, greet_s = _pick(GREET_PAIRS)
    tpl = random.randint(1, 8)

    if tpl == 1:
        msgs = [
            {"role": "user",      "content": greet_c},
            {"role": "assistant", "content": greet_s},
            {"role": "user",      "content": f"الـ{brand} المعروضة للبيع، ما زالت موجودة؟"},
            {"role": "assistant", "content": f"إي موجودة. {car_desc}. السعر {price}"},
            {"role": "user",      "content": _pick(DISC_REQ)},
            {"role": "assistant", "content": _pick(DISC_YES)},
            {"role": "user",      "content": "ماشي، متفقين"},
            {"role": "assistant", "content": _pick(CLOSE)},
        ]
    elif tpl == 2:
        msgs = [
            {"role": "user",      "content": f"هلو، {_pick(PRICE_Q)} الـ{brand} {model}؟"},
            {"role": "assistant", "content": f"{car_desc}. السعر {price}"},
            {"role": "user",      "content": _pick(EXPENSIVE)},
            {"role": "assistant", "content": _pick(DISC_NO)},
            {"role": "user",      "content": "زين، بفكر وأرجعلك"},
            {"role": "assistant", "content": "حياك الله، التواصل مفتوح"},
        ]
    elif tpl == 3:
        msgs = [
            {"role": "user",      "content": greet_c},
            {"role": "assistant", "content": greet_s},
            {"role": "user",      "content": "شنو تفاصيل السيارة؟"},
            {"role": "assistant", "content": f"{car_desc}. {'في ' + city if city else ''}"},
            {"role": "user",      "content": _pick(CONDITION)},
            {"role": "assistant", "content": _pick(COND_GOOD)},
            {"role": "user",      "content": _pick(PRICE_Q)},
            {"role": "assistant", "content": price},
            {"role": "user",      "content": "ماشي، أجيك أشوفها"},
            {"role": "assistant", "content": _pick(CLOSE)},
        ]
    elif tpl == 4:
        msgs = [
            {"role": "user",      "content": f"مرحبا، الـ{brand} {model} موديل {year} باعت؟"},
            {"role": "assistant", "content": f"لا، ما زالت موجودة. {price}"},
            {"role": "user",      "content": _pick(DISC_REQ)},
            {"role": "assistant", "content": _pick(DISC_YES) if random.random() > 0.5 else _pick(DISC_NO)},
            {"role": "user",      "content": "وين موقعك؟"},
            {"role": "assistant", "content": f"{'في ' + city if city else 'بغداد، تواصل للموقع التفصيلي'}"},
            {"role": "user",      "content": "زين، أكلمك لاحقاً"},
            {"role": "assistant", "content": "حياك الله وتفضل"},
        ]
    elif tpl == 5:
        msgs = [
            {"role": "user",      "content": f"هلو، {_pick(CONDITION)} الـ{brand}؟"},
            {"role": "assistant", "content": _pick(COND_GOOD)},
            {"role": "user",      "content": _pick(PRICE_Q)},
            {"role": "assistant", "content": f"{price}. {car_desc}"},
            {"role": "user",      "content": "شكد المسافة؟"},
            {"role": "assistant", "content": f"{mileage if mileage else 'ما متذكر بالضبط، بس بالشكل كويس'}"},
            {"role": "user",      "content": _pick(DISC_REQ)},
            {"role": "assistant", "content": _pick(DISC_NO)},
            {"role": "user",      "content": "ماشي، متفقين"},
            {"role": "assistant", "content": _pick(CLOSE)},
        ]
    elif tpl == 6:
        msgs = [
            {"role": "user",      "content": f"السلام عليكم، أبي سيارة {brand} موديل {year}"},
            {"role": "assistant", "content": f"وعليكم السلام! عندي {car_desc}، بحالة ممتازة"},
            {"role": "user",      "content": _pick(PRICE_Q)},
            {"role": "assistant", "content": price},
            {"role": "user",      "content": "أكدر أقسطها؟"},
            {"role": "assistant", "content": "لا أخوي، نقداً بس. ما نسوي تقسيط"},
            {"role": "user",      "content": "زين، بفكر"},
            {"role": "assistant", "content": "تفضل ما في عجلة، الموضوع موجود"},
        ]
    elif tpl == 7:
        msgs = [
            {"role": "user",      "content": f"هلو، الـ{brand} {model} فيها حوادث؟"},
            {"role": "assistant", "content": "لا والله، نظيفة من أي حادثة"},
            {"role": "user",      "content": "كشف الميكانيكي؟"},
            {"role": "assistant", "content": "إي تكدر تاخذها للكشف على حسابك"},
            {"role": "user",      "content": _pick(PRICE_Q)},
            {"role": "assistant", "content": f"{price}. {car_desc}"},
            {"role": "user",      "content": _pick(DISC_REQ)},
            {"role": "assistant", "content": _pick(DISC_YES)},
            {"role": "user",      "content": "اتفقنا، متى أجيك؟"},
            {"role": "assistant", "content": "أي وقت تريد، موجود"},
        ]
    else:
        msgs = [
            {"role": "user",      "content": f"صباح الخير، شو تفاصيل إعلان الـ{brand}؟"},
            {"role": "assistant", "content": f"صباح النور! {car_desc}. {price}"},
            {"role": "user",      "content": _pick(WARRANTY)},
            {"role": "assistant", "content": _pick(WARRANTY_A)},
            {"role": "user",      "content": _pick(DISC_REQ)},
            {"role": "assistant", "content": _pick(DISC_YES)},
            {"role": "user",      "content": "ماشي، هاي الفلوس"},
            {"role": "assistant", "content": _pick(CLOSE)},
        ]

    return {
        "id":        f"sooqiq_{car_data.get('id', int(time.time()))}",
        "category":  "sales_cars",
        "dialect":   "iraqi_arabic",
        "source":    car_data.get("url", "https://sooq.iq"),
        "real_data": {
            "brand": brand, "model": model, "year": year,
            "mileage": mileage, "price": price, "city": city,
        },
        "messages": msgs,
    }


def _make_general_conversation(title, description, price, location, category, source_url):
    """يبني محادثة بيع عامة من بيانات إعلان"""
    price_text = price if price else "السعر بالتواصل"
    loc_text   = f" في {location}" if location else ""
    desc_short = _clean(description)
    greet_c, greet_s = _pick(GREET_PAIRS)
    tpl = random.randint(1, 6)

    if tpl == 1:
        msgs = [
            {"role": "user",      "content": greet_c},
            {"role": "assistant", "content": greet_s},
            {"role": "user",      "content": f"أريد {title}{loc_text}، متوفر؟"},
            {"role": "assistant", "content": f"إي متوفر. {desc_short}. السعر {price_text}"},
            {"role": "user",      "content": _pick(DISC_REQ)},
            {"role": "assistant", "content": _pick(DISC_YES)},
            {"role": "user",      "content": "ماشي، هاي الفلوس"},
            {"role": "assistant", "content": _pick(CLOSE)},
        ]
    elif tpl == 2:
        msgs = [
            {"role": "user",      "content": f"هلو، {_pick(PRICE_Q)} الـ{title}؟"},
            {"role": "assistant", "content": f"{title} بـ{price_text}. {desc_short}"},
            {"role": "user",      "content": _pick(EXPENSIVE)},
            {"role": "assistant", "content": _pick(DISC_NO)},
            {"role": "user",      "content": "زين، بفكر وأرجعلك"},
            {"role": "assistant", "content": "حياك الله، البضاعة موجودة"},
        ]
    elif tpl == 3:
        msgs = [
            {"role": "user",      "content": greet_c},
            {"role": "assistant", "content": greet_s},
            {"role": "user",      "content": f"شنو تفاصيل الـ{title}؟"},
            {"role": "assistant", "content": f"{desc_short}. السعر {price_text}{loc_text}"},
            {"role": "user",      "content": _pick(WARRANTY)},
            {"role": "assistant", "content": _pick(WARRANTY_A)},
            {"role": "user",      "content": "ماشي، أجيك"},
            {"role": "assistant", "content": _pick(CLOSE)},
        ]
    elif tpl == 4:
        msgs = [
            {"role": "user",      "content": f"مرحبا، {title} لا يزال متوفر؟"},
            {"role": "assistant", "content": f"إي موجود. {price_text}{loc_text}"},
            {"role": "user",      "content": _pick(DISC_REQ)},
            {"role": "assistant", "content": _pick(DISC_NO)},
            {"role": "user",      "content": "زين، متفقين"},
            {"role": "assistant", "content": _pick(CLOSE)},
        ]
    elif tpl == 5:
        msgs = [
            {"role": "user",      "content": f"هلو، {title} جديد ولا مستعمل؟"},
            {"role": "assistant", "content": f"{'جديد بالكرتون' if 'جديد' in str(title)+str(desc_short) else 'مستعمل بحالة ممتازة'}. {price_text}"},
            {"role": "user",      "content": "أشوفه وين؟"},
            {"role": "assistant", "content": f"{'في ' + location if location else 'تواصل معي للموعد'}"},
            {"role": "user",      "content": "ماشي، أتصل فيك"},
            {"role": "assistant", "content": "حياك الله"},
        ]
    else:
        msgs = [
            {"role": "user",      "content": f"هلو، عندكم {title}؟"},
            {"role": "assistant", "content": f"إي عندنا. {desc_short}"},
            {"role": "user",      "content": _pick(PRICE_Q)},
            {"role": "assistant", "content": price_text},
            {"role": "user",      "content": _pick(DISC_REQ)},
            {"role": "assistant", "content": _pick(DISC_YES)},
            {"role": "user",      "content": "زين، آخذه"},
            {"role": "assistant", "content": _pick(CLOSE)},
        ]

    return {
        "id":       f"scraped_{int(time.time())}_{random.randint(1000,9999)}",
        "category": category,
        "dialect":  "iraqi_arabic",
        "source":   source_url,
        "messages": msgs,
    }


# ── 1. sooq.iq — سيارات عراقية (مُتحقق) ─────────────────

def _parse_sooq_car(a_tag):
    """يُحلّل بيانات السيارة من رابط sooq.iq"""
    href = a_tag.get('href', '')
    if not href or '/ar/car/' not in href:
        return None

    text = a_tag.get_text(separator=' ', strip=True)

    price_m = re.search(r'\$\s*([\d,]+)', text)
    price_usd_val = int(price_m.group(1).replace(',', '')) if price_m else 0
    price_iqd = f"{price_usd_val * USD_TO_IQD:,} دينار" if price_usd_val else "السعر بالتواصل"

    year_m = re.search(r'\b(19|20)\d{2}\b', text)
    year   = year_m.group() if year_m else ''

    mile_m  = re.search(r'([\d,]+)\s*(ميل|كم)', text)
    mileage = f"{mile_m.group(1)} {mile_m.group(2)}" if mile_m else ''

    # URL: /ar/car/{city}/{brand}/{model}/{id}
    parts = href.strip('/').split('/')
    city       = parts[2] if len(parts) > 2 else ''
    brand      = parts[3].replace('-', ' ') if len(parts) > 3 else ''
    model      = parts[4].replace('--', '-').replace('-', ' ') if len(parts) > 4 else ''
    listing_id = parts[5] if len(parts) > 5 else str(int(time.time()))

    if not brand:
        return None

    return {
        'id':        listing_id,
        'title':     f'{brand} {model} {year}'.strip(),
        'brand':     brand,
        'model':     model,
        'year':      year,
        'mileage':   mileage,
        'price_usd': f'${price_usd_val:,}' if price_usd_val else '',
        'price_iqd': price_iqd,
        'city':      city,
        'seller':    'بائع خاص' if 'بائع خاص' in text else 'معرض',
        'url':       f'https://www.sooq.iq{href}',
    }


SOOQ_TYPES = [
    ('?condition=Used', 'مستعمل'),
    ('?condition=New',  'جديد'),
    ('?fuel=EV',        'كهربائي'),
]

SOOQ_BRANDS = [
    'تويوتا', 'كيا', 'هيونداي', 'نيسان', 'هوندا',
    'مرسيدس-بنز', 'بي-ام-دبليو', 'شيفروليه', 'ام-جي',
    'ميتسوبيشي', 'سوزوكي', 'رينو', 'جيب', 'فورد', 'مازدا',
]


def scrape_sooq_iq(pages=5):
    """يقشط إعلانات السيارات من sooq.iq"""
    print("\n[السيارات] sooq.iq")
    conversations = []
    seen_ids = set()
    base = "https://www.sooq.iq/ar/search"

    for search_type, label in SOOQ_TYPES:
        print(f"\n  [{label}]", end=" ", flush=True)
        for page in range(1, pages + 1):
            url = f"{base}{search_type}&page={page}"
            r = _get(url)
            if not r:
                continue

            soup = BeautifulSoup(r.text, "lxml")
            all_links = soup.find_all('a', href=True)
            car_links = [a for a in all_links if '/ar/car/' in a.get('href', '')]

            # إزالة التكرار (كل سيارة تظهر مرتين: mobile + desktop)
            unique = {}
            for a in car_links:
                if a['href'] not in unique:
                    unique[a['href']] = a

            count = 0
            for href, a_tag in unique.items():
                car = _parse_sooq_car(a_tag)
                if not car or car['id'] in seen_ids:
                    continue
                seen_ids.add(car['id'])
                conversations.append(_make_car_conversation(car))
                count += 1

            print(f"ص{page}:{count}", end=" ", flush=True)
            _sleep()

    # صفحات حسب الماركة لتنويع البيانات
    brand_pages = max(1, pages // 3)
    print(f"\n  [حسب الماركة، {brand_pages} صفحة]", end=" ", flush=True)
    for brand in SOOQ_BRANDS:
        for page in range(1, brand_pages + 1):
            url = f"https://www.sooq.iq/ar/search?brand={brand}&page={page}"
            r = _get(url)
            if not r:
                continue

            soup = BeautifulSoup(r.text, "lxml")
            all_links = soup.find_all('a', href=True)
            car_links = [a for a in all_links if '/ar/car/' in a.get('href', '')]

            unique = {}
            for a in car_links:
                if a['href'] not in unique:
                    unique[a['href']] = a

            count = 0
            for href, a_tag in unique.items():
                car = _parse_sooq_car(a_tag)
                if not car or car['id'] in seen_ids:
                    continue
                seen_ids.add(car['id'])
                conversations.append(_make_car_conversation(car))
                count += 1

            if count:
                print(f"{brand[:4]}:{count}", end=" ", flush=True)
            _sleep()

    print(f"\n  [مجموع] {len(conversations)}")
    return conversations


# ── 2. iq.opensooq.com — إعلانات عامة ────────────────────

IQ_PATHS = [
    ("/en/electronics",  "sales_electronics", "إلكترونيات"),
    ("/en/real-estate",  "sales_realestate",  "عقارات"),
    ("/en/furniture",    "sales_furniture",   "أثاث"),
    ("/en/clothes",      "sales_clothes",     "ملابس"),
    ("/en/services",     "services",          "خدمات"),
]


def scrape_opensooq(pages=3):
    """يقشط iq.opensooq.com بالمسارات الإنجليزية"""
    print("\n[عام] iq.opensooq.com")
    conversations = []
    base = "https://iq.opensooq.com"

    for path, category, label in IQ_PATHS:
        print(f"\n  [{label}]", end=" ", flush=True)

        for page in range(1, pages + 1):
            url = f"{base}{path}?page={page}"
            r = _get(url)
            if not r:
                continue

            soup = BeautifulSoup(r.text, "lxml")
            cards = (
                soup.select("li[class*=card]") or
                soup.select("li[class*=listing]") or
                soup.select("div[class*=listing-item]") or
                soup.select("article") or
                soup.select("[class*=ad-item]")
            )

            count = 0
            for card in cards:
                try:
                    title_el = card.select_one("h2,h3,[class*=title]")
                    price_el = card.select_one("[class*=price]")
                    loc_el   = card.select_one("[class*=location],[class*=city]")
                    desc_el  = card.select_one("[class*=desc],p")

                    title    = _clean(title_el.get_text() if title_el else "")
                    price    = _clean(price_el.get_text() if price_el else "")
                    location = _clean(loc_el.get_text() if loc_el else "")
                    desc     = _clean(desc_el.get_text() if desc_el else "")

                    if not title or len(title) < 3:
                        continue

                    conversations.append(_make_general_conversation(title, desc, price, location, category, url))
                    count += 1
                except Exception:
                    continue

            print(f"ص{page}:{count}", end=" ", flush=True)
            _sleep()

        print()

    return conversations


# ── 3. bazarak.com/iraq ────────────────────────────────────

BAZARAK_CATS = [
    ("/iraq/electronics",         "sales_electronics", "إلكترونيات"),
    ("/iraq/mobile-phones",       "sales_electronics", "موبايلات"),
    ("/iraq/real-estate",         "sales_realestate",  "عقارات"),
    ("/iraq/furniture",           "sales_furniture",   "أثاث"),
    ("/iraq/clothes-accessories", "sales_clothes",     "ملابس"),
]


def scrape_bazarak(pages=3):
    """يقشط bazarak.com/iraq"""
    print("\n[متنوع] bazarak.com")
    conversations = []
    base = "https://bazarak.com"

    for path, category, label in BAZARAK_CATS:
        print(f"\n  [{label}]", end=" ", flush=True)

        for page in range(1, pages + 1):
            url = f"{base}{path}?page={page}"
            r = _get(url)
            if not r:
                continue

            soup = BeautifulSoup(r.text, "lxml")
            cards = (
                soup.select("li[class*=item]") or
                soup.select("div[class*=item]") or
                soup.select("article") or
                soup.select("[class*=product]")
            )

            count = 0
            for card in cards:
                try:
                    title_el = card.select_one("h2,h3,h4,[class*=title]")
                    price_el = card.select_one("[class*=price]")
                    loc_el   = card.select_one("[class*=location],[class*=city]")
                    desc_el  = card.select_one("[class*=desc],p")

                    title    = _clean(title_el.get_text() if title_el else "")
                    price    = _clean(price_el.get_text() if price_el else "")
                    location = _clean(loc_el.get_text() if loc_el else "")
                    desc     = _clean(desc_el.get_text() if desc_el else "")

                    if not title or len(title) < 3:
                        continue

                    conversations.append(_make_general_conversation(title, desc, price, location, category, url))
                    count += 1
                except Exception:
                    continue

            print(f"ص{page}:{count}", end=" ", flush=True)
            _sleep()

        print()

    return conversations


# ── 4. قشط من رابط مخصص ────────────────────────────────────

def scrape_custom_url(url, category="sales_general", pages=1):
    """يقشط أي صفحة إعلانات عراقية"""
    print(f"\n[مخصص] {url}")
    conversations = []

    for page in range(1, pages + 1):
        paged = f"{url}?page={page}" if page > 1 else url
        r = _get(paged)
        if not r:
            continue

        soup = BeautifulSoup(r.text, "lxml")
        all_els = soup.find_all(['article', 'li', 'div'])
        count = 0
        seen = set()

        for el in all_els:
            text = el.get_text(strip=True)
            if len(text) < 20 or len(text) > 600:
                continue

            has_price  = any(w in text for w in ["دينار", "$", "دولار", "IQD", "ألف", "مليون"])
            has_arabic = len([c for c in text if "؀" <= c <= "ۿ"]) > 10

            if not (has_price and has_arabic):
                continue

            key = text[:80]
            if key in seen:
                continue
            seen.add(key)

            price_m = re.search(r'[\d,]+\s*(دينار|ألف|مليون)', text)
            price   = price_m.group(0) if price_m else ""

            lines = [l.strip() for l in text.split("\n") if l.strip()]
            title = lines[0][:80] if lines else text[:60]
            desc  = " ".join(lines[1:3])[:120] if len(lines) > 1 else ""

            if len(title) < 3:
                continue

            conversations.append(_make_general_conversation(title, desc, price, "", category, paged))
            count += 1

        print(f"  صفحة {page}: {count} إعلان")
        _sleep()

    return conversations


# ── حفظ ودمج ──────────────────────────────────────────────

def save(conversations, tag):
    if not conversations:
        print(f"[!] لا توجد بيانات ({tag})")
        return None

    ts    = datetime.now().strftime("%Y%m%d_%H%M%S")
    fname = os.path.join(OUTPUT_DIR, f"scraped_{tag}_{ts}.json")

    with open(fname, "w", encoding="utf-8") as f:
        json.dump(conversations, f, ensure_ascii=False, indent=2)

    print(f"\n[OK] حُفظ {len(conversations)} محادثة -> {fname}")

    cats = {}
    for c in conversations:
        cats[c["category"]] = cats.get(c["category"], 0) + 1
    for cat, n in sorted(cats.items(), key=lambda x: -x[1]):
        print(f"     {cat}: {n}")

    return fname


def merge_with_training(scraped_file, training_file):
    """يدمج بيانات القشط مع ملف تدريب موجود"""
    with open(scraped_file, encoding="utf-8") as f:
        scraped = json.load(f)
    with open(training_file, encoding="utf-8") as f:
        training = json.load(f)

    merged = training + scraped
    random.shuffle(merged)

    out = training_file.replace(".json", "_plus_scraped.json")
    with open(out, "w", encoding="utf-8") as f:
        json.dump(merged, f, ensure_ascii=False, indent=2)

    print(f"\n[OK] دُمج: {len(scraped)} مُقشطة + {len(training)} مولّدة = {len(merged)} إجمالي")
    print(f"     الملف: {out}")


# ── Main ───────────────────────────────────────────────────

def main():
    parser = argparse.ArgumentParser(
        description="Iraqi Sales Scraper"
    )
    parser.add_argument(
        "--source", choices=["sooq", "opensooq", "bazarak", "all"],
        default="all",
        help="المصدر (default: all)"
    )
    parser.add_argument(
        "--pages", type=int, default=5,
        help="عدد الصفحات (default: 5)"
    )
    parser.add_argument("--url",      type=str, default=None, help="رابط مخصص")
    parser.add_argument("--category", type=str, default="sales_general", help="تصنيف عند --url")
    parser.add_argument("--merge",    type=str, default=None, help="دمج مع ملف تدريب")
    args = parser.parse_args()

    print("=" * 55)
    print("  Iraqi Sales Data Scraper")
    print("=" * 55)

    all_convs = []

    if args.url:
        convs = scrape_custom_url(args.url, args.category, args.pages)
        f = save(convs, "custom")
        if f:
            all_convs.extend(convs)
    else:
        if args.source in ("sooq", "all"):
            convs = scrape_sooq_iq(pages=args.pages)
            f = save(convs, "sooq_cars")
            if f:
                all_convs.extend(convs)

        if args.source in ("opensooq", "all"):
            convs = scrape_opensooq(pages=args.pages)
            f = save(convs, "opensooq")
            if f:
                all_convs.extend(convs)

        if args.source in ("bazarak", "all"):
            convs = scrape_bazarak(pages=args.pages)
            f = save(convs, "bazarak")
            if f:
                all_convs.extend(convs)

        if args.source == "all" and len(all_convs) > 1:
            save(all_convs, "combined")

    if args.merge and all_convs:
        tmp = os.path.join(OUTPUT_DIR, "_tmp_scraped.json")
        with open(tmp, "w", encoding="utf-8") as f:
            json.dump(all_convs, f, ensure_ascii=False)
        merge_with_training(tmp, args.merge)
        os.remove(tmp)

    print("\n" + "=" * 55)
    print(f"  المجموع: {len(all_convs)} محادثة")
    print(f"  المجلد:  {OUTPUT_DIR}/")
    print("=" * 55)


if __name__ == "__main__":
    main()
