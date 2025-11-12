#!/usr/bin/env bash
set -euo pipefail

echo "Tests start: $(date -u +"%Y-%m-%dT%H:%M:%SZ")"
START_TIME=$(date +%s)

# Ensure venv exists
if [ -f .venv/bin/python ]; then
    PY=.venv/bin/python
elif [ -f .venv/Scripts/python.exe ]; then
    PY=.venv/Scripts/python.exe
else
    echo "Virtualenv not found. Run setup.sh first."; exit 1
fi

# Run pytest with coverage
$PY -m pytest -v --cov=.

END_TIME=$(date +%s)
DURATION=$((END_TIME-START_TIME))

echo "Tests end: $(date -u +"%Y-%m-%dT%H:%M:%SZ")"
echo "Duration: ${DURATION}s"

exit 0
