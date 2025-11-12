#!/usr/bin/env bash
set -euo pipefail

echo "Starting setup at: $(date -u +"%Y-%m-%dT%H:%M:%SZ")"
START_TIME=$(date +%s)

# Create venv
python -m venv .venv

# Determine python executable in venv
if [ -f .venv/bin/python ]; then
    PY=.venv/bin/python
elif [ -f .venv/Scripts/python.exe ]; then
    PY=.venv/Scripts/python.exe
else
    PY=python
fi

# Upgrade pip and install
$PY -m pip install --upgrade pip
$PY -m pip install -r requirements.txt

# Record installed packages
$PY -m pip freeze | sort > installed_requirements.txt

# Generate upgrade diff report
$PY scripts/compare_requirements.py requirements_old.txt requirements.txt upgrade_report.md

END_TIME=$(date +%s)
DURATION=$((END_TIME-START_TIME))

echo "Setup completed at: $(date -u +"%Y-%m-%dT%H:%M:%SZ")"
echo "Duration: ${DURATION}s"

exit 0
