import sys
from packaging.version import parse

def parse_reqs(path):
    d = {}
    with open(path, 'r', encoding='utf-8') as f:
        for line in f:
            line=line.strip()
            if not line or line.startswith('#'):
                continue
            if '==' in line:
                pkg, ver = line.split('==', 1)
            elif '>=' in line:
                pkg, ver = line.split('>=', 1)
            else:
                pkg, ver = line.split('=', 1) if '=' in line else (line, '')
            d[pkg.lower().strip()] = ver.strip()
    return d


def main(old_path, new_path, out_path=None):
    old=parse_reqs(old_path)
    new=parse_reqs(new_path)
    lines=["# Dependency Upgrade Report\n"]
    lines.append('| Package | Old version | New version | Upgraded? |')
    lines.append('|--------:|:------------:|:-----------:|:---------:|')
    for pk in sorted(set(old) | set(new)):
        o=old.get(pk, '')
        n=new.get(pk, '')
        up='N/A'
        if o and n:
            try:
                up = 'Yes' if parse(n) > parse(o) else ('No' if parse(n) == parse(o) else 'Downgraded')
            except Exception:
                up='Unknown'
        elif not o and n:
            up='New'
        elif o and not n:
            up='Removed'
        lines.append(f'| {pk} | {o or "-"} | {n or "-"} | {up} |')

    report='\n'.join(lines)
    if out_path:
        with open(out_path, 'w', encoding='utf-8') as f:
            f.write(report)
    else:
        print(report)

if __name__=='__main__':
    argv=sys.argv[1:]
    if len(argv)<2:
        print('Usage: compare_requirements.py <requirements_old.txt> <requirements_new.txt> [output.md]')
        sys.exit(2)
    main(*argv)
