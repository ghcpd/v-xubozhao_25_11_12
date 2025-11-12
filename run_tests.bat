@echo off
REM Script to execute all tests and generate a coverage report for Windows

setlocal enabledelayedexpansion

echo ==========================================
set START_TIME=%date% %time%
echo Test execution started at: %START_TIME%
echo ==========================================

REM Activate virtual environment if it exists
if exist "venv\Scripts\activate.bat" (
    echo Activating virtual environment...
    call venv\Scripts\activate.bat
) else (
    echo Warning: Virtual environment not found. Running tests in current environment.
)

REM Check if pytest is installed
python -m pytest --version >nul 2>&1
if errorlevel 1 (
    echo Error: pytest is not installed. Please run setup.bat first.
    exit /b 1
)

REM Run tests with verbose output and coverage
echo Running tests with pytest...
echo.

python -m pytest -v --cov=app --cov-report=term-missing --cov-report=html test_app.py

echo.
echo ==========================================
set END_TIME=%date% %time%
echo Test execution completed at: %END_TIME%
echo ==========================================
echo.
echo Coverage report generated in htmlcov\index.html

