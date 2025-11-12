#!/bin/bash
# setup.sh - Environment setup script for dependency upgrade

echo "========================================"
echo "Dependency Upgrade - Environment Setup"
echo "========================================"
echo ""

# Record start time
START_TIME=$(date +"%Y-%m-%d %H:%M:%S")
echo "[$(date '+%Y-%m-%d %H:%M:%S')] Setup starting..."
echo ""

# Check Python installation
echo "[$(date '+%Y-%m-%d %H:%M:%S')] Checking Python installation..."
python --version
echo ""

# Create virtual environment if it doesn't exist
if [ ! -d "venv" ]; then
    echo "[$(date '+%Y-%m-%d %H:%M:%S')] Creating virtual environment..."
    python -m venv venv
    echo "[$(date '+%Y-%m-%d %H:%M:%S')] Virtual environment created."
else
    echo "[$(date '+%Y-%m-%d %H:%M:%S')] Virtual environment already exists."
fi
echo ""

# Activate virtual environment
echo "[$(date '+%Y-%m-%d %H:%M:%S')] Activating virtual environment..."
source venv/bin/activate
echo ""

# Upgrade pip
echo "[$(date '+%Y-%m-%d %H:%M:%S')] Upgrading pip..."
pip install --upgrade pip setuptools wheel
echo ""

# Install dependencies from requirements.txt
echo "[$(date '+%Y-%m-%d %H:%M:%S')] Installing dependencies from requirements.txt..."
pip install -r requirements.txt
echo ""

# Verify installation
echo "[$(date '+%Y-%m-%d %H:%M:%S')] Verifying installed packages..."
pip list
echo ""

# Record end time
END_TIME=$(date +"%Y-%m-%d %H:%M:%S")
echo "========================================"
echo "Setup Complete"
echo "Start Time: $START_TIME"
echo "End Time:   $END_TIME"
echo "========================================"
