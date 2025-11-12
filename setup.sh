#!/usr/bin/env bash
# setup.sh - create venv, install requirements, and write a freeze file
set -euo pipefail

START_TIME=$(date -u +"%Y-%m-%dT%H:%M:%SZ")
echo "Starting environment setup at ${START_TIME} UTC"
PYTHON=$(python -c "import sys;print(sys.executable)")

echo "Using Python: ${PYTHON}"
# Create virtual environment
${PYTHON} -m venv venv

# Determine venv Python executable path
if [ -f "venv/Scripts/python.exe" ]; then
  VENV_PY="$(pwd)/venv/Scripts/python.exe"
else
  VENV_PY="$(pwd)/venv/bin/python"
fi

echo "Venv Python: ${VENV_PY}"
# Upgrade pip and install requirements
"${VENV_PY}" -m pip install --upgrade pip setuptools wheel
"${VENV_PY}" -m pip install -r requirements.txt

# Freeze precise versions to requirements_freeze.txt
"${VENV_PY}" -m pip freeze > requirements_freeze.txt

END_TIME=$(date -u +"%Y-%m-%dT%H:%M:%SZ")
echo "Environment setup completed at ${END_TIME} UTC"

echo "Start: ${START_TIME} - End: ${END_TIME}" > env_times.log

exit 0
