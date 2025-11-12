#!/usr/bin/env python3
"""
make_upgrade_diff.py - produce a simple markdown upgrade diff given old and new requirement files

Usage: python make_upgrade_diff.py requirements_old.txt requirements.txt > upgrade_diff.md
"""
import sys
import re
from typing import Dict


def parse_req(file_path):
    d = {}
    with open(file_path, 'r', encoding='utf-8') as fh:
        for line in fh:
            line = line.strip()
            if not line or line.startswith('#'):
                continue
            name, sep, version = re.split(r'==|>=|<=|~=|!=|>|<', line, 1)[0].partition('==') if '==' in line else (line, '', '')
            # simpler: handle 'name==version'
            if '==' in line:
                name, version = line.split('==', 1)
                d[name.strip()] = version.strip()
            else:
                d[line] = ''
    return d


def main():
    if len(sys.argv) < 3:
        print('Usage: make_upgrade_diff.py <old> <new>')
        sys.exit(2)
    old = parse_req(sys.argv[1])
    new = parse_req(sys.argv[2])

    headers = ['Package', 'Old', 'New']
    rows = []
    all_keys = sorted(set(old.keys()) | set(new.keys()), key=str.lower)
    for k in all_keys:
        rows.append([k, old.get(k, ''), new.get(k, '')])

    # print markdown table
    print('# Upgrade Diff')
    print()
    print('| ' + ' | '.join(headers) + ' |')
    print('|' + '|'.join(['---'] * len(headers)) + '|')
    for r in rows:
        print(f"| {r[0]} | {r[1] or 'unspecified'} | {r[2] or 'unspecified'} |")


if __name__ == '__main__':
    main()
