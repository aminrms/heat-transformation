#!/bin/bash

# Exit script if any command fails
set -e

# Project's main script name
MAIN_SCRIPT="main.py"

# Check if Python is installed
if ! command -v python &>/dev/null; then
    echo "Python is not installed. Please install Python before running this script."
    exit 1
fi

# Step 1: Create a virtual environment
echo "Creating virtual environment..."
python -m venv venv

# Activate the virtual environment
echo "Activating virtual environment..."
source venv/Scripts/activate

# Step 2: Install required packages
if [ ! -f requirements.txt ]; then
    echo "Error: requirements.txt not found. Please add your dependencies to a requirements.txt file."
    deactivate
    exit 1
fi

echo "Installing required packages..."
# pip install --upgrade pip
pip install -r requirements.txt

# Step 3: Check if PyInstaller is installed, if not, install it
if ! pip show pyinstaller &>/dev/null; then
    echo "PyInstaller not found. Installing PyInstaller..."
    pip install pyinstaller
fi

# Step 4: Build the executable
if [ ! -f "$MAIN_SCRIPT" ]; then
    echo "Error: $MAIN_SCRIPT not found in the current directory."
    deactivate
    exit 1
fi

BASE_NAME=$(basename "$MAIN_SCRIPT" .py)

echo "Building .exe file for $MAIN_SCRIPT..."
pyinstaller --onefile --clean "$MAIN_SCRIPT"

# Step 5: Output the result
if [ -f "dist/$BASE_NAME.exe" ]; then
    echo "Build successful! The executable file is located at:"
    echo "dist/$BASE_NAME.exe"
else
    echo "Error: .exe file not generated. Check PyInstaller output for details."
fi

# Step 6: Deactivate virtual environment
deactivate
echo "Virtual environment deactivated."

# Done
echo "Setup and build process completed!"
