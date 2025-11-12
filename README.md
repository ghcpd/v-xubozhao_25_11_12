# Dependency Upgrade & Validation

This workspace demonstrates upgrading and verifying a Python project's dependencies.

Files created:
- `requirements.txt` — Updated dependency list (latest versions found by `upgrade_requirements.py`).
- `requirements_freeze.txt` — Exact versions installed after environment setup.
- `upgrade_report.md` — High-level report showing old vs new versions.
- `upgrade_diff.md` — Markdown table showing differences between old & new dep versions.
- `upgrade_requirements.py` — Script to automatically query and pin latest package versions.
- `make_upgrade_diff.py` — Script to generate a markdown diff between requirements files.
- `setup.sh` — Creates venv and installs `requirements.txt` (cross-platform caveats noted).
- `run_tests.sh` — Runs `pytest` within the venv and records start/end times.
- `test_app.py` — pytest test suite verifying app behavior and dependency versions.

How to reproduce (Windows PowerShell recommended):
1. Create a new virtual environment: `python -m venv venv`
2. Install dependencies from `requirements.txt` into the venv:
   - On Windows: `venv\Scripts\python.exe -m pip install -r requirements.txt`
   - On Linux/WSL: `venv/bin/python -m pip install -r requirements.txt`
3. Run tests:
   - On Windows: `venv\Scripts\python.exe -m pytest -v`
   - On Linux/WSL: `venv/bin/python -m pytest -v`
4. To re-generate the `requirements.txt` using the latest versions: `python upgrade_requirements.py requirements_old.txt requirements.txt upgrade_report.md` (requires network access to PyPI)

Notes:
- The scripts `setup.sh` and `run_tests.sh` are POSIX `bash` scripts; if you use PowerShell, use the corresponding commands from the steps above to run the Python in the created virtual environment.
- The upgrade script may install or upgrade packages when needed (e.g., fallback `pip install` usage).
- For a perfect CI-friendly run, call `setup.sh` in a bash environment and `run_tests.sh` in a bash environment (or create PowerShell equivalents using the steps above).

