# Dependency Upgrade Project

This project demonstrates the process of upgrading outdated Python dependencies to their latest compatible versions, with comprehensive testing and validation.

## Project Structure

```
.
├── requirements_old.txt    # Original outdated dependencies
├── requirements.txt        # Updated dependencies (generated)
├── app.py                  # Flask application using the dependencies
├── test_app.py             # Pytest test suite
├── setup.sh                # Setup script (Unix/Linux/Mac)
├── setup.bat               # Setup script (Windows)
├── run_tests.sh            # Test runner script (Unix/Linux/Mac)
├── run_tests.bat           # Test runner script (Windows)
├── upgrade_and_test.py     # Main Python script with timing
├── upgrade_report.md       # Version diff report
└── README.md              # This file
```

## Quick Start

### Option 1: Using Shell Scripts (Unix/Linux/Mac)

1. **Setup environment:**
   ```bash
   chmod +x setup.sh run_tests.sh
   ./setup.sh
   ```

2. **Run tests:**
   ```bash
   ./run_tests.sh
   ```

### Option 2: Using Batch Files (Windows)

1. **Setup environment:**
   ```cmd
   setup.bat
   ```

2. **Run tests:**
   ```cmd
   run_tests.bat
   ```

### Option 3: Using Python Script (Cross-platform)

```bash
python upgrade_and_test.py
```

This script will:
- Run the setup process
- Execute all tests
- Display start and end times
- Show total duration

## Manual Setup

1. **Create virtual environment:**
   ```bash
   python -m venv venv
   ```

2. **Activate virtual environment:**
   - Windows: `venv\Scripts\activate`
   - Unix/Linux/Mac: `source venv/bin/activate`

3. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

4. **Run tests:**
   ```bash
   pytest -v
   ```

## Dependency Upgrades

| Package | Old Version | New Version |
|---------|-------------|-------------|
| flask | 1.0.2 | 3.0.0 |
| requests | 2.19.1 | 2.31.0 |
| pandas | 0.24.2 | 2.2.0 |
| numpy | 1.16.0 | 1.26.4 |

See `upgrade_report.md` for detailed information about the upgrades.

## Testing

The test suite (`test_app.py`) includes:

1. **Functional Tests:**
   - Route existence and response codes
   - JSON response validation
   - Application logic correctness

2. **Environment Tests:**
   - Dependency version verification
   - Import functionality checks
   - Package compatibility validation

3. **Integration Tests:**
   - Combined dependency and application logic tests

Run tests with:
```bash
pytest -v
```

Run tests with coverage:
```bash
pytest -v --cov=app --cov-report=html
```

## Expected Output

When running the complete process, you should see:

1. Setup process start time
2. Virtual environment creation
3. Dependency installation
4. Setup process end time
5. Test execution start time
6. Test results with coverage
7. Test execution end time
8. Total duration

## Requirements

- Python 3.7 or higher
- pip (Python package installer)
- Virtual environment support (venv)

## Notes

- The application code (`app.py`) required no changes - all upgrades maintain backward compatibility for this use case
- All tests pass successfully with the upgraded dependencies
- Coverage reports are generated in the `htmlcov/` directory

