import json
import os
import re
import importlib
from packaging.version import parse as vparse
import importlib.metadata as im
from app import app


def load_requirements(path):
    reqs = {}
    with open(path, 'r', encoding='utf-8') as fh:
        for line in fh:
            line = line.strip()
            if not line or line.startswith('#'):
                continue
            m = re.match(r'([^=<>!~]+)(?:[=<>!~]+\s*([\d\.\w\-]+))?', line)
            if m:
                reqs[m.group(1).lower()] = m.group(2) or ''
    return reqs


def test_index_route():
    client = app.test_client()
    res = client.get('/')
    assert res.status_code == 200
    data = res.get_json()
    assert isinstance(data, dict)
    assert data.get('sum') == 6


def test_installed_versions_incremented_or_same():
    old_requirements = load_requirements('requirements_old.txt')
    # Check each old package has installed newer or equal version
    for pkg, old_ver in old_requirements.items():
        try:
            installed_ver = im.version(pkg)
        except im.PackageNotFoundError:
            # Try case-insensitive fallback
            installed_ver = None
            for d in im.distributions():
                if d.metadata['Name'].lower() == pkg.lower():
                    installed_ver = d.version
                    break
            if not installed_ver:
                assert False, f'Package {pkg} not installed'
        if old_ver:
            assert vparse(installed_ver) >= vparse(old_ver), f'{pkg} was not upgraded (installed {installed_ver} <= old {old_ver})'


def test_requirements_pinned_and_present():
    assert os.path.isfile('requirements.txt'), 'requirements.txt not found'
    reqs = load_requirements('requirements.txt')
    assert len(reqs) > 0, 'requirements.txt appears empty'
    # Ensure we have pinned entries for key packages
    for key in ['flask', 'requests', 'pandas', 'numpy']:
        assert key in reqs, f'{key} not in requirements.txt'
        assert re.match(r'\d', reqs[key] or ''), f'{key} in requirements.txt is not pinned to a version'
