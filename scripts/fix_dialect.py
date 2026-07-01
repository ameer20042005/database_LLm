#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
fix_dialect.py
--------------
يصلح المفردات غير العراقية في ملفات بيانات التدريب ويستبدلها بمفردات عراقية أصيلة.

المشاكل المكتشفة:
- استخدام "هلو" بدلاً من "هلا"
- استخدام "أيش" (خليجية) بدلاً من "شنو"
- استخدام "كيف" بدلاً من "شلون"
- غياب: اسولف، احچي، اكدر، شويه
- لغة رسمية في ملفات العمل والحكومة

الاستخدام:
    python scripts/fix_dialect.py
    python scripts/fix_dialect.py --dry-run
"""

import json
import os
import re
import argparse

# استبدالات مباشرة — ترتيب مهم: الأطول أولاً لتجنب التعارض
WORD_REPLACEMENTS = [
    # تحيات
    ("هلو،",          "هلا،"),
    ("هلو ",          "هلا "),
    ("مرحبا،",        "هلا،"),
    ("مرحبا ",        "هلا "),
    ("مرحباً،",       "هلا،"),
    ("مرحباً ",       "هلا "),
    ("صباح الخير،",   "صباح النور،"),
    ("مساء الخير،",   "مساء النور،"),
    ("مساء الخير ",   "مساء النور "),

    # كلمات خليجية → عراقية
    ("أيش ",          "شنو "),
    ("أيش؟",          "شنو؟"),
    ("إيش ",          "شنو "),
    ("إيش؟",          "شنو؟"),
    ("وش ",           "شنو "),
    ("وش؟",           "شنو؟"),
    ("كيف ذلك",       "شلون هيچي"),
    ("كيف هذا",       "شلون هذا"),
    ("لماذا ",        "ليش "),
    ("لماذا؟",        "ليش؟"),

    # أفعال — استبدال حذر (مع سياق)
    ("لا أستطيع",     "ما اكدر"),
    ("لا أعرف",       "ما أدري"),
    ("لا أعلم",       "ما أدري"),
    ("أتحدث",         "احچي"),
    ("أتكلم",         "احچي"),
    ("يتحدث",         "يحچي"),
    ("يتكلم",         "يحچي"),

    # كلمات يومية
    ("قليلاً",        "شويه"),
    ("قليلا",         "شويه"),
    ("ببطء",          "شويه شويه"),
    ("الآن",          "هسه"),
    ("الان",          "هسه"),
    ("كثيراً",        "هواي"),
    ("كثيرا",         "هواي"),
    ("جداً",          "كلش"),
    ("جدا",           "كلش"),
    ("غداً",          "باچر"),
    # "غدا" بدون تنوين خطرة — تظهر داخل "بغداد" وكلمات أخرى، نتجنبها
    ("لا يوجد",       "ماكو"),
    ("يوجد هناك",     "أكو"),

    # ردود
    ("حسناً،",        "زين،"),
    ("حسنا،",         "زين،"),
    ("حسناً ",        "زين "),
    ("حسنا ",         "زين "),
    ("طيب،",          "زين،"),
    ("طيب ",          "زين "),
    ("ممتاز!",        "خوش كلش!"),
    ("رائع!",         "خوش كلش!"),

    # كلمات خليجية شائعة في الملفات
    ("يبي ",          "يريد "),
    ("يبي.",          "يريد."),
    ("يبي،",          "يريد،"),
    ("تبين ",         "تريدين "),
    ("أبي ",          "أريد "),
    ("أبغى ",         "أريد "),
    ("وايد",          "هواي"),

    # ولدك → ابنك (طلب المستخدم)
    ("ولدك",          "ابنك"),
    ("ولدي",          "ابني"),
    ("ولدها",         "ابنها"),
    ("ولده",          "ابنه"),
    ("ولدهم",         "أبناءهم"),

    # أسئلة عراقية
    ("من متى ",       "من شوكت "),
    ("من متى؟",       "من شوكت؟"),
    ("منذ متى ",      "من شوكت "),
    ("منذ متى؟",      "من شوكت؟"),
    ("متى ",          "شوكت "),
    ("متى؟",          "شوكت؟"),
]

# إضافة "اسولف" في سياق الكلام عن التحدث/الشرح
PHRASE_INSERTIONS = [
    # لا نضيف تلقائياً — قد يكسر المعنى
]


def fix_content(text: str) -> str:
    for old, new in WORD_REPLACEMENTS:
        text = text.replace(old, new)
    return text


def process_file(path: str, dry_run: bool = False) -> int:
    with open(path, encoding='utf-8') as f:
        data = json.load(f)

    changed = 0
    for conv in data:
        for msg in conv.get('messages', []):
            orig = msg.get('content', '')
            fixed = fix_content(orig)
            if fixed != orig:
                if not dry_run:
                    msg['content'] = fixed
                changed += 1

    if not dry_run and changed:
        with open(path, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=2)

    return changed


def main():
    parser = argparse.ArgumentParser(description='Fix non-Iraqi dialect words in training data')
    parser.add_argument('--dry-run', action='store_true', help='Show counts without saving')
    parser.add_argument('--dir', default='iraqi_training_data')
    parser.add_argument('--file', help='Process a single file only')
    args = parser.parse_args()

    base = os.path.join(os.path.dirname(os.path.dirname(__file__)), args.dir)

    if args.file:
        files = [args.file]
    else:
        files = sorted(f for f in os.listdir(base) if f.endswith('.json') and f != 'train.json')

    total = 0
    for fname in files:
        path = os.path.join(base, fname)
        n = process_file(path, dry_run=args.dry_run)
        if n:
            action = 'سيُصلح' if args.dry_run else 'صُلح'
            print(f'[{action}] {fname}: {n} رسالة')
        else:
            print(f'[OK] {fname}')
        total += n

    print(f'\nالمجموع: {total} رسالة {"(dry-run)" if args.dry_run else "صُلحت"}')


if __name__ == '__main__':
    main()
