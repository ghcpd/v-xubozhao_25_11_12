#!/usr/bin/env bash
# run_tests.sh - Run pytest with coverage
set -euo pipefail

START_TIME=$(date -u +"%Y-%m-%dT%H:%M:%SZ")
echo "Starting tests at ${START_TIME} UTC"

# Determine venv python
if [ -f "venv/Scripts/python.exe" ]; then
  VENV_PY="$(pwd)/venv/Scripts/python.exe"
else
  VENV_PY="$(pwd)/venv/bin/python"
fi

# Run pytest with coverage
"${VENV_PY}" -m pytest -v --maxfail=1 --disable-warnings --showlocals --cov=.

END_TIME=$(date -u +"%Y-%m-%dT%H:%M:%SZ")
echo "Tests completed at ${END_TIME} UTC"

echo "Start: ${START_TIME} - End: ${END_TIME}" > test_times.log

exit 0
