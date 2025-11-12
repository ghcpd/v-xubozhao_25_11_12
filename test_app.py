import json
import re
import subprocess
from importlib import metadata
import sys
import os

import pytest

# Import the app from the workspace
from app import app


def test_index_sum():
    client = app.test_client()
    resp = client.get('/')
    assert resp.status_code == 200
    data = resp.get_json()
    assert data['sum'] == 6


def parse_requirements(req_file: str):
    with open(req_file, 'r', encoding='utf-8') as fh:
        for line in fh:
            line = line.strip()
            if not line or line.startswith('#'):
                continue
            m = re.match(r"([^=<>!~]+)==([0-9a-zA-Z.\-]+)", line)
            if m:
                yield m.group(1).strip(), m.group(2).strip()


def get_installed_version(name: str):
    # importlib.metadata.version can fail with 'flask' vs 'Flask' etc; normalize
    try:
        return metadata.version(name)
    except metadata.PackageNotFoundError:
        # try a case-insensitive search
        for dist in metadata.distributions():
            if dist.metadata['Name'] and dist.metadata['Name'].lower() == name.lower():
                return dist.version
        raise


def test_dependency_versions_are_installed():
    req_file = os.path.join(os.path.dirname(__file__), 'requirements.txt')
    missing = []
    for name, expected_version in parse_requirements(req_file):
        try:
            installed = get_installed_version(name)
        except metadata.PackageNotFoundError:
            pytest.fail(f"Dependency not installed: {name}")
        # compare normalized versions (strip leading v)
        if installed.lstrip('v') != expected_version.lstrip('v'):
            pytest.fail(f"Version mismatch for {name}: expected {expected_version}, installed {installed}")


if __name__ == '__main__':
    pytest.main(['-v'])
