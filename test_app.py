import importlib
import os
from packaging.version import parse
import pytest

from app import app

OLD_REQ_FILE = os.path.join(os.path.dirname(__file__), 'requirements_old.txt')


def read_old_reqs():
    data = {}
    with open(OLD_REQ_FILE, 'r', encoding='utf-8') as f:
        for line in f:
            line=line.strip()
            if not line or line.startswith('#'):
                continue
            if '==' in line:
                pkg, ver = line.split('==', 1)
                data[pkg.lower()] = ver
    return data


def test_index_route():
    client = app.test_client()
    res = client.get('/')
    assert res.status_code == 200
    assert res.json['sum'] == 6


@pytest.mark.parametrize('pkg,module', [
    ('flask', 'flask'),
    ('requests', 'requests'),
    ('pandas', 'pandas'),
    ('numpy', 'numpy'),
])
def test_dependency_upgraded(pkg, module):
    old = read_old_reqs()[pkg]
    mod = importlib.import_module(module)
    ver = getattr(mod, '__version__', None)
    assert ver is not None, f"{module} has no __version__"
    assert parse(ver) >= parse(old), f"{module} version {ver} is older than original {old}"


def test_requirements_file_exists():
    assert os.path.exists('requirements.txt')
    with open('requirements.txt', 'r', encoding='utf-8') as f:
        assert 'flask' in f.read().lower()
