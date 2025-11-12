#!/usr/bin/env python3
"""
upgrade_requirements.py

This script reads an old requirements file and outputs a new `requirements.txt` with the latest
available versions for each listed package. It also writes an upgrade report markdown file summarizing
old and new versions.

Usage: python upgrade_requirements.py requirements_old.txt requirements.txt upgrade_report.md

This script uses `pip index versions` to look up the latest version for each package. If that fails,
it will try `pip install` to resolve to a compatible version and read the installed version using
`pip show`.
"""

import sys
import re
import subprocess
from typing import List, Tuple


def parse_requirement_line(line: str) -> Tuple[str, str]:
    # Extract package name and version (if present)
    line = line.strip()
    if not line or line.startswith("#"):
        return "", ""
    # handle forms like package==1.2.3 or package>=1.2.0 or package
    parts = re.split(r"([<>=!~]+)", line, maxsplit=1)
    if len(parts) >= 3:
        name = parts[0].strip()
        op = parts[1]
        rest = parts[2].strip()
        # We just treat it as name plus rest
        return name, (op + rest)
    else:
        return line, ""


def get_latest_version(package: str, python_exec: str = sys.executable) -> str:
    # Try pip index versions (pip >= 20.3)
    try:
        cmd = [python_exec, "-m", "pip", "index", "versions", package]
        p = subprocess.run(cmd, capture_output=True, text=True, check=False)
        out = p.stdout.strip() or p.stderr.strip()
        # Search lines like 'Available versions: 2.0.3, 1.8.2, 1.8.0'
        m = re.search(r"Available versions: (.*)$", out, re.MULTILINE)
        if m:
            versions = m.group(1).split(",")
            if versions:
                latest = versions[0].strip()
                return latest
    except Exception:
        pass

    # Fallback: try to install to a temporary venv (this will modify env) - prefer not to
    # Alternative fallback: use pip install {package} and check installed version
    try:
        cmd = [python_exec, "-m", "pip", "install", "--upgrade", package]
        p = subprocess.run(cmd, capture_output=True, text=True)
        # read version with pip show
        cmd = [python_exec, "-m", "pip", "show", package]
        p = subprocess.run(cmd, capture_output=True, text=True, check=False)
        out = p.stdout.strip()
        for line in out.splitlines():
            if line.startswith("Version: "):
                return line.split("Version: ", 1)[1].strip()
    except Exception:
        pass
    return ""


def main():
    if len(sys.argv) < 4:
        print("Usage: upgrade_requirements.py <old_req> <new_req> <report.md>")
        sys.exit(2)
    input_file = sys.argv[1]
    output_file = sys.argv[2]
    report_file = sys.argv[3]

    packages = []  # (name, old_spec)
    with open(input_file, "r", encoding="utf-8") as fh:
        for line in fh:
            name, spec = parse_requirement_line(line)
            if name:
                packages.append((name, spec))

    # Find latest versions
    resolved = []  # (name, old_spec, latest_version)
    for name, old_spec in packages:
        print(f"Querying latest for {name}...", file=sys.stderr)
        latest = get_latest_version(name)
        resolved.append((name, old_spec, latest))

    # Write new requirements file with pinned versions
    with open(output_file, "w", encoding="utf-8") as outfh:
        outfh.write("# Auto-generated requirements.txt\n")
        for name, old_spec, latest in resolved:
            if latest:
                outfh.write(f"{name}=={latest}\n")
            else:
                # If couldn't resolve, keep old spec
                if old_spec:
                    outfh.write(f"{name}{old_spec}\n")
                else:
                    outfh.write(f"{name}\n")

    # Write upgrade report
    lines = ["# Upgrade Report", "", "| Package | Old Spec | New Version |", "|---|---|---|"]
    for name, old_spec, latest in resolved:
        lines.append(f"| {name} | {old_spec or 'unspecified'} | {latest or 'unknown'} |")
    with open(report_file, "w", encoding="utf-8") as rf:
        rf.write("\n".join(lines))

    print(f"Wrote: {output_file} and {report_file}")


if __name__ == '__main__':
    main()
