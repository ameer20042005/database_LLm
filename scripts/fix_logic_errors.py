#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
fix_logic_errors.py
-------------------
يصلح الأخطاء المنطقية في حوارات بيانات التدريب العراقية:
- وصف مكونات طبق خاطئة (مثل: شاي أخضر في مرق عدس)
- منتجات مكررة في نفس الجملة
- وصف علامات تجارية غير منطقية (LG لا تصنع صبغ جدران)
- خلط بين أوصاف الأطباق العراقية

الاستخدام:
    python scripts/fix_logic_errors.py
"""

import json
import os

FIXES = {
    "iraqi_train_01_electronics.json": [
        {
            "id": "electronics_sales_0002",
            "old": "لابتوب Dell Core i7 عنده رام 16 گيگا. كاميرا خلفية ممتازة للتصوير في الضوء الخافت",
            "new": "لابتوب Dell Core i7 عنده رام 16 گيگا. ويب كام مدمج HD ممتاز للاجتماعات وكاميرا واضحة",
            "reason": "اللابتوب ليس عنده كاميرا خلفية - عنده ويب كام"
        },
        {
            "id": "electronics_sales_0003",
            "old": "بهالحالة لابتوب Asus Core i7 أنسب لك وبسعر 979,000 دينار. رام 16 گيگا وما تحتاج أكثر",
            "new": "بهالحالة تلفزيون LG 43 إنش أنسب لك وبسعر 365,000 دينار. Full HD وما تحتاج أكثر",
            "reason": "الزبون يسأل عن تلفزيون - لا يعرض عليه لابتوب"
        },
    ],
    "iraqi_train_02_food.json": [
        {
            "id": "food_sales_0002",
            "old": "للـمرق عدس تريد: شاي أخضر ورز عنبر وبهارات. كلها موجودة عندنا",
            "new": "للـمرق عدس تريد: عدس مجروش وبصل وملح وبهارات. كلها موجودة عندنا",
            "reason": "مرق العدس لا يحتاج شاي أخضر أو رز"
        },
        {
            "id": "food_sales_0007",
            "old": "للـدولمة تريد رز بسمتي وكيك جاهز وبهارات. كلها موجودة عندنا",
            "new": "للـدولمة تريد رز وورق عنب ولحم مفروم وبهارات. كلها موجودة عندنا",
            "reason": "الدولمة لا تحتاج كيك جاهز"
        },
    ],
    "iraqi_train_07_services.json": [
        {
            "id": "svc_0007",
            "old": "صباح الخير، عندكم تصليح صبغ جدران ماركة LG؟",
            "new": "صباح الخير، عندكم تصليح مكيف ماركة LG؟",
            "reason": "LG لا تصنع صبغ جدران - تصنع مكيفات وأجهزة كهربائية"
        },
        {
            "id": "svc_0007",
            "old": "نعم، نصلح LG وكل ماركات المكيفات",
            "new": "صباح النور. نصلح LG وكل ماركات المكيفات",
            "reason": "إصلاح التحية لتكون عراقية"
        },
    ],
    "iraqi_train_14_restaurant.json": [
        {
            "id": "rest_0004",
            "old": "تشريب مشوي بالفحم، وكباب طبخ بيتي تقليدي",
            "new": "تشريب خبز عراقي مع مرق اللحم، والكباب مشوي على الجمر. كلهم طازجين",
            "reason": "الوصف معكوس: الكباب هو المشوي والتشريب هو الخبز مع المرق"
        },
    ],
}


def fix_file(base_dir, fname, fixes):
    path = os.path.join(base_dir, fname)
    if not os.path.exists(path):
        print(f'  SKIP: {fname} not found')
        return 0

    with open(path, 'r', encoding='utf-8') as f:
        data = json.load(f)

    changed = 0
    for fix in fixes:
        for conv in data:
            if conv['id'] != fix['id']:
                continue
            for msg in conv['messages']:
                if fix['old'] in msg.get('content', ''):
                    msg['content'] = msg['content'].replace(fix['old'], fix['new'])
                    print(f'  [{fname}] {fix["id"]}: {fix["reason"]}')
                    changed += 1

    if changed:
        with open(path, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=2)

    return changed


def main():
    base = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'iraqi_training_data')
    total = 0
    for fname, fixes in FIXES.items():
        n = fix_file(base, fname, fixes)
        total += n

    print(f'\nTotal logic fixes applied: {total}')


if __name__ == '__main__':
    main()
