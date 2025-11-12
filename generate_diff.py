#!/usr/bin/env python3
"""
generate_diff.py
Reads requirements_old.txt and requirements.txt and writes an upgrade_report.md with a table of old and new versions.
"""
from packaging.version import parse as vparse
import re
import sys


def parse_req_line(line):
    line = line.strip()
    if not line or line.startswith('#'):
        return None
    m = re.match(r'([^=<>!~]+)(?:[=<>!~]+\s*([\d\.\w\-]+))?', line)
    if m:
        name = m.group(1).strip()
        ver = m.group(2) or ''
        return name.lower(), ver
    return None


def read_reqs(path):
    r = {}
    try:
        with open(path, 'r', encoding='utf-8') as fh:
            for line in fh:
                parsed = parse_req_line(line)
                if parsed:
                    r[parsed[0]] = parsed[1]
    except FileNotFoundError:
        print(f'Missing {path}', file=sys.stderr)
    return r


old = read_reqs('requirements_old.txt')
new = read_reqs('requirements.txt')

rows = []
for name in set(list(old.keys()) + list(new.keys())):
    o = old.get(name, '')
    n = new.get(name, '')
    changed = ''
    if o and n:
        try:
            if vparse(n) > vparse(o):
                changed = 'Upgraded'
            elif vparse(n) == vparse(o):
                changed = 'Unchanged'
            else:
                changed = 'Downgraded'
        except Exception:
            changed = 'Changed'
    elif o and not n:
        changed = 'Removed'
    elif not o and n:
        changed = 'Added'
    rows.append((name, o, n, changed))

rows.sort()

with open('upgrade_report.md', 'w', encoding='utf-8') as out:
    out.write('# Dependency Upgrade Report\n\n')
    out.write('| Package | Old Version | New Version | Status |\n')
    out.write('|---|---|---|---|\n')
    for name, o, n, changed in rows:
        out.write(f'| {name} | {o or "-"} | {n or "-"} | {changed} |\n')

print('Wrote upgrade_report.md')
