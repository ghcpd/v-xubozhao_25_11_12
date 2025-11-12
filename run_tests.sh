#!/bin/bash
# Script to execute all tests and generate a coverage report

set -e  # Exit on any error

START_TIME=$(date)
echo "=========================================="
echo "Test execution started at: $START_TIME"
echo "=========================================="

# Activate virtual environment if it exists
if [ -d "venv" ]; then
    echo "Activating virtual environment..."
    if [[ "$OSTYPE" == "msys" || "$OSTYPE" == "win32" || -n "$WINDIR" ]]; then
        source venv/Scripts/activate
    else
        source venv/bin/activate
    fi
else
    echo "Warning: Virtual environment not found. Running tests in current environment."
fi

# Check if pytest is installed
if ! python -m pytest --version &> /dev/null; then
    echo "Error: pytest is not installed. Please run setup.sh first."
    exit 1
fi

# Run tests with verbose output and coverage
echo "Running tests with pytest..."
echo ""

python -m pytest -v --cov=app --cov-report=term-missing --cov-report=html test_app.py

echo ""
echo "=========================================="
END_TIME=$(date)
echo "Test execution completed at: $END_TIME"
echo "=========================================="
echo ""
echo "Coverage report generated in htmlcov/index.html"

