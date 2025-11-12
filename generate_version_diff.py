"""
Utility script to generate a detailed version comparison report.
Compares requirements_old.txt with requirements.txt
"""
import re
from datetime import datetime


def parse_requirements(filepath):
    """Parse a requirements file and return a dict of package:version."""
    packages = {}
    try:
        with open(filepath, 'r') as f:
            for line in f:
                line = line.strip()
                if line and not line.startswith('#'):
                    # Match package==version format
                    match = re.match(r'([a-zA-Z0-9_-]+)==([0-9.]+)', line)
                    if match:
                        package, version = match.groups()
                        packages[package.lower()] = version
    except FileNotFoundError:
        print(f"Warning: {filepath} not found")
    return packages


def compare_versions(old_ver, new_ver):
    """Compare two version strings and return change type."""
    if old_ver == new_ver:
        return "unchanged"
    
    old_parts = [int(x) for x in old_ver.split('.')]
    new_parts = [int(x) for x in new_ver.split('.')]
    
    if new_parts[0] > old_parts[0]:
        return "major"
    elif len(new_parts) > 1 and len(old_parts) > 1 and new_parts[1] > old_parts[1]:
        return "minor"
    else:
        return "patch"


def main():
    """Generate version diff report."""
    print("Generating version comparison report...")
    print("=" * 60)
    
    old_reqs = parse_requirements('requirements_old.txt')
    new_reqs = parse_requirements('requirements.txt')
    
    all_packages = set(old_reqs.keys()) | set(new_reqs.keys())
    
    print(f"\nReport generated at: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
    print("Version Changes:")
    print("-" * 60)
    print(f"{'Package':<20} {'Old Version':<15} {'New Version':<15} {'Change':<10}")
    print("-" * 60)
    
    for package in sorted(all_packages):
        old_ver = old_reqs.get(package, "N/A")
        new_ver = new_reqs.get(package, "N/A")
        
        if old_ver == "N/A":
            change = "added"
            symbol = "➕"
        elif new_ver == "N/A":
            change = "removed"
            symbol = "➖"
        else:
            change = compare_versions(old_ver, new_ver)
            if change == "major":
                symbol = "🔴"
            elif change == "minor":
                symbol = "🟡"
            elif change == "patch":
                symbol = "🟢"
            else:
                symbol = "⚪"
        
        print(f"{package:<20} {old_ver:<15} {new_ver:<15} {symbol} {change}")
    
    print("-" * 60)
    print("\nLegend:")
    print("  🔴 Major version change")
    print("  🟡 Minor version change")
    print("  🟢 Patch version change")
    print("  ➕ New package added")
    print("  ➖ Package removed")
    print("  ⚪ Unchanged")


if __name__ == "__main__":
    main()

