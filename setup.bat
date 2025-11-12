@echo off
REM Setup script for Windows to install dependencies and prepare the environment

setlocal enabledelayedexpansion

echo ==========================================
set START_TIME=%date% %time%
echo Setup process started at: %START_TIME%
echo ==========================================

REM Check if Python is available
python --version >nul 2>&1
if errorlevel 1 (
    echo Error: Python is not installed or not in PATH
    exit /b 1
)

echo Using Python:
python --version

REM Create virtual environment if it doesn't exist
if not exist "venv" (
    echo Creating virtual environment...
    python -m venv venv
) else (
    echo Virtual environment already exists
)

REM Activate virtual environment
echo Activating virtual environment...
call venv\Scripts\activate.bat

REM Upgrade pip
echo Upgrading pip...
python -m pip install --upgrade pip --quiet

REM Install dependencies
echo Installing dependencies from requirements.txt...
pip install -r requirements.txt

echo.
echo ==========================================
set END_TIME=%date% %time%
echo Setup process completed at: %END_TIME%
echo ==========================================
echo.
echo Virtual environment is ready!
echo To activate it manually, run: venv\Scripts\activate.bat

