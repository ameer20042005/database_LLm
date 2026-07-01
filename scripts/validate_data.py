#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
validate_data.py
----------------
يفحص ملفات بيانات التدريب ويتحقق من:
1. عدم وجود placeholders غير ممتلئة ({_xxx})
2. صحة هيكل JSON
3. وجود حقول مطلوبة (id, category, dialect, messages)
4. أن كل محادثة تحتوي على رسائل user و assistant متناوبة

الاستخدام:
    python scripts/validate_data.py
    python scripts/validate_data.py --verbose
"""

import json
import re
import os
import argparse


def validate_file(path, verbose=False):
    fname = os.path.basename(path)
    errors = []
    warnings = []

    try:
        with open(path, 'r', encoding='utf-8') as f:
            data = json.load(f)
    except json.JSONDecodeError as e:
        return [f'JSON ERROR: {e}'], []

    for conv in data:
        cid = conv.get('id', '??')

        # Check required fields
        for field in ['id', 'category', 'dialect', 'messages']:
            if field not in conv:
                errors.append(f'{cid}: missing field "{field}"')

        msgs = conv.get('messages', [])
        if not msgs:
            errors.append(f'{cid}: empty messages')
            continue

        # Check for unfilled placeholders
        for i, msg in enumerate(msgs):
            content = msg.get('content', '')
            found = re.findall(r'\{_[a-zA-Z_]+\}', content)
            if found:
                errors.append(f'{cid}[{i}]: unfilled placeholders: {found} in: "{content[:60]}"')

        # Check alternating roles
        for i in range(len(msgs) - 1):
            if msgs[i].get('role') == msgs[i+1].get('role'):
                warnings.append(f'{cid}[{i}+{i+1}]: consecutive same-role messages ({msgs[i]["role"]})')

        # Check first message is user
        if msgs[0].get('role') != 'user':
            warnings.append(f'{cid}: first message is not from user')

    if verbose or errors:
        status = 'FAIL' if errors else 'OK'
        print(f'[{status}] {fname}: {len(data)} convs, {len(errors)} errors, {len(warnings)} warnings')
        for e in errors:
            print(f'  ERROR: {e}')
        if verbose:
            for w in warnings:
                print(f'  WARN:  {w}')

    return errors, warnings


def main():
    parser = argparse.ArgumentParser(description='Validate Iraqi training data files')
    parser.add_argument('--verbose', '-v', action='store_true')
    parser.add_argument('--dir', default='iraqi_training_data')
    args = parser.parse_args()

    base = os.path.join(os.path.dirname(os.path.dirname(__file__)), args.dir)
    # train.json has a different Q&A format - skip it
    files = sorted(f for f in os.listdir(base) if f.endswith('.json') and f != 'train.json')

    total_errors = 0
    total_warnings = 0

    for fname in files:
        errs, warns = validate_file(os.path.join(base, fname), verbose=args.verbose)
        total_errors += len(errs)
        total_warnings += len(warns)
        if not args.verbose and not errs:
            print(f'[OK] {fname}')

    print(f'\n{"="*50}')
    print(f'Total errors: {total_errors}')
    print(f'Total warnings: {total_warnings}')
    if total_errors == 0:
        print('All files passed validation!')


if __name__ == '__main__':
    main()
