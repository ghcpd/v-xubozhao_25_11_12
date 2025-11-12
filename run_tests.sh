#!/usr/bin/env bash
set -euo pipefail

START_TIME=$(date -u +"%Y-%m-%dT%H:%M:%SZ")
echo "Start time: $START_TIME"

# Activate virtualenv
if [ -f ".venv/bin/activate" ]; then
  source .venv/bin/activate
elif [ -f ".venv/Scripts/Activate" ]; then
  source .venv/Scripts/Activate
fi

# Run pytest with coverage using module to avoid CLI entrypoint issues
python -m pytest -v --maxfail=1 --disable-warnings --cov=.

END_TIME=$(date -u +"%Y-%m-%dT%H:%M:%SZ")
echo "End time: $END_TIME"

# Generate simple coverage summary (text)
python - <<'PY'
from coverage import coverage
print('Run `coverage html` for an HTML report if desired (requires coverage package).')
PY
