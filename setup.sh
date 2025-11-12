#!/usr/bin/env bash
set -euo pipefail

# Setup script: creates virtualenv, upgrades pip, installs dependencies, freezes them into requirements.txt
# Logs start and end times to console.

START_TIME=$(date -u +"%Y-%m-%dT%H:%M:%SZ")
echo "Start time: $START_TIME"

# Create venv (idempotent)
python -m venv .venv || python3 -m venv .venv

# Activate venv: works for POSIX environments
if [ -f ".venv/bin/activate" ]; then
  # POSIX-like shells
  source .venv/bin/activate
elif [ -f ".venv/Scripts/Activate" ]; then
  # PowerShell activation script (for Git Bash)
  source .venv/Scripts/Activate
else
  echo "Could not find virtualenv activation script; activating manually may be required."
fi

# Upgrade pip & tools
python -m pip install --upgrade pip setuptools wheel

# Install/upgrade packages using the newest compatible versions
if [ -f "requirements.txt" ]; then
  echo "Installing pinned requirements from requirements.txt"
  python -m pip install --upgrade -r requirements.txt
elif [ -f "requirements_old.txt" ]; then
  echo "Upgrading packages from requirements_old.txt to their latest compatible versions"
  # Install by package name (strip pins) so pip fetches latest released versions
  PKGS=$(awk -F '==' '{print $1}' requirements_old.txt | grep -v '^#' | xargs)
  python -m pip install --upgrade $PKGS
else
  echo "No requirements_old.txt found; aborting."
  exit 1
fi

# No explicit upgrade for test tooling: rely on requirements.txt pins for reproducibility

# Freeze pinned requirements
python -m pip freeze | sort > requirements.txt

END_TIME=$(date -u +"%Y-%m-%dT%H:%M:%SZ")
echo "End time: $END_TIME"

echo "Requirements have been written to requirements.txt."

echo "To run tests: source .venv/bin/activate && ./run_tests.sh"
