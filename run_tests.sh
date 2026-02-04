#!/bin/bash
# run_tests.sh - Test execution and coverage report script

echo "========================================"
echo "Dependency Upgrade - Test Suite"
echo "========================================"
echo ""

# Record start time
START_TIME=$(date +"%Y-%m-%d %H:%M:%S")
START_EPOCH=$(date +%s)
echo "[$(date '+%Y-%m-%d %H:%M:%S')] Test execution starting..."
echo ""

# Check if virtual environment exists
if [ ! -d "venv" ]; then
    echo "ERROR: Virtual environment not found. Please run setup.sh first."
    exit 1
fi

# Activate virtual environment
source venv/bin/activate
echo "[$(date '+%Y-%m-%d %H:%M:%S')] Virtual environment activated."
echo ""

# Run pytest with coverage
echo "[$(date '+%Y-%m-%d %H:%M:%S')] Running pytest suite with coverage analysis..."
echo ""
pytest -v --cov=. --cov-report=term-missing --cov-report=html test_app.py
TEST_EXIT_CODE=$?
echo ""

# Display test results summary
if [ $TEST_EXIT_CODE -eq 0 ]; then
    echo "[$(date '+%Y-%m-%d %H:%M:%S')] ✓ All tests passed successfully!"
else
    echo "[$(date '+%Y-%m-%d %H:%M:%S')] ✗ Some tests failed. Exit code: $TEST_EXIT_CODE"
fi
echo ""

# Generate dependency report
echo "[$(date '+%Y-%m-%d %H:%M:%S')] Generating dependency report..."
echo ""
echo "Installed Packages:"
pip list
echo ""

# Record end time
END_TIME=$(date +"%Y-%m-%d %H:%M:%S")
END_EPOCH=$(date +%s)
DURATION=$((END_EPOCH - START_EPOCH))

echo "========================================"
echo "Test Execution Complete"
echo "Start Time: $START_TIME"
echo "End Time:   $END_TIME"
echo "Duration:   ${DURATION}s"
echo "========================================"
echo ""

# Coverage report location
echo "Coverage HTML report generated in: htmlcov/index.html"
echo ""

exit $TEST_EXIT_CODE
