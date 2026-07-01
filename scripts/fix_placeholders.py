#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
fix_placeholders.py
-------------------
يصلح الـ placeholders غير الممتلئة ({_xxx}) في ملفات بيانات التدريب العراقية.
يُستخدم بعد أي عملية توليد بيانات للتحقق وإصلاح أي قيم فارغة تسربت.

الاستخدام:
    python scripts/fix_placeholders.py
    python scripts/fix_placeholders.py --dry-run   # فقط يعرض المشاكل بدون إصلاح
"""

import json
import re
import os
import random
import argparse

random.seed(42)

REPLACEMENTS = {
    "{_wait_min}":    ["15 دقيقة", "20 دقيقة", "ربع ساعة", "10 دقايق", "25 دقيقة"],
    "{_city}":        ["بغداد", "البصرة", "الموصل", "النجف", "كربلاء", "أربيل", "كركوك", "السماوة"],
    "{_overtime_h}":  ["ساعتين إضافيتين", "3 ساعات إضافية", "ساعة إضافية", "4 ساعات إضافية"],
    "{_expire_yrs}":  ["سنتين", "3 سنين", "5 سنين", "سنة واحدة"],
    "{_dog_time}":    ["الصبح الباكر", "المساء بعد المغرب", "الفجر", "بعد الظهر"],
    "{_prop_type}":   ["بيت", "شقة", "دكان", "أرض سكنية", "بستان"],
    "{_stadium}":     ["ملعب الشعب", "ملعب الكرادة", "ملعب اليرموك", "ملعب الصداقة"],
    "{_hours_new}":   ["8 ساعات", "6 ساعات", "9 ساعات", "7 ساعات"],
    "{_course_goal}": ["المحاسبة", "إدارة المشاريع", "البرمجة", "التسويق الرقمي", "اللغة الإنكليزية"],
    "{_water_prob}":  ["الضغط واطي", "الماء ما يجي بالكافي", "المواسير تسرب شوي"],
    "{_pax}":         ["شخصين", "3 أشخاص", "4 أشخاص", "شخص واحد"],
    "{_abroad}":      ["ألمانيا", "تركيا", "ماليزيا", "هولندا", "كندا", "بريطانيا", "فرنسا"],
    "{_grade}":       ["امتياز", "جيد جداً", "جيد", "95%", "88%", "72%"],
    "{_garden_plant}":["نبات الزينة", "شجرة الليمون", "نبات الياسمين", "شجرة التين", "الورد"],
    "{_prov}":        ["الناصرية", "الحلة", "الديوانية", "الكوت", "العمارة", "الرمادي", "تكريت"],
    "{_hw}":          ["الغسالة", "الثلاجة", "المكيف", "التلفزيون", "الأثاث"],
}


def replace_placeholders(text):
    def _sub(match):
        ph = match.group(0)
        return random.choice(REPLACEMENTS[ph]) if ph in REPLACEMENTS else ph
    return re.sub(r'\{_[a-zA-Z_]+\}', _sub, text)


def process_file(path, dry_run=False):
    with open(path, 'r', encoding='utf-8') as f:
        data = json.load(f)

    changed = 0
    for conv in data:
        for msg in conv.get('messages', []):
            orig = msg.get('content', '')
            fixed = replace_placeholders(orig)
            if fixed != orig:
                if not dry_run:
                    msg['content'] = fixed
                changed += 1

    if not dry_run and changed:
        with open(path, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=2)

    return changed


def main():
    parser = argparse.ArgumentParser(description='Fix placeholders in Iraqi training data')
    parser.add_argument('--dry-run', action='store_true', help='Show issues without fixing')
    parser.add_argument('--dir', default='iraqi_training_data', help='Data directory')
    args = parser.parse_args()

    base = os.path.join(os.path.dirname(os.path.dirname(__file__)), args.dir)
    files = sorted(f for f in os.listdir(base) if f.endswith('.json'))

    total = 0
    for fname in files:
        path = os.path.join(base, fname)
        n = process_file(path, dry_run=args.dry_run)
        if n:
            action = "Found" if args.dry_run else "Fixed"
            print(f'{action} {n} messages in {fname}')
            total += n

    if total == 0:
        print('No placeholders found.')
    else:
        action = "found" if args.dry_run else "fixed"
        print(f'\nTotal {action}: {total} messages')


if __name__ == '__main__':
    main()
