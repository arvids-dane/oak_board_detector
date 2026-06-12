#!/bin/bash

# Oak Board Detector - Linux Launcher
# This script sets up and runs the application on Linux

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$SCRIPT_DIR"

echo "=================================================="
echo "Oak Board Detector - Linux Launcher"
echo "=================================================="
echo ""

# Check if Python 3 is installed
if ! command -v python3 &> /dev/null; then
    echo "ERROR: Python 3 is not installed!"
    echo "Please install Python 3.8 or higher:"
    echo "  Ubuntu/Debian: sudo apt-get install python3 python3-pip"
    echo "  Fedora: sudo dnf install python3 python3-pip"
    echo "  Arch: sudo pacman -S python python-pip"
    exit 1
fi

PYTHON_VERSION=$(python3 --version 2>&1 | awk '{print $2}')
echo "✓ Python $PYTHON_VERSION detected"
echo ""

# Check if pip is installed
if ! command -v pip3 &> /dev/null; then
    echo "ERROR: pip3 is not installed!"
    echo "Please install pip: sudo apt-get install python3-pip"
    exit 1
fi

echo "✓ pip3 detected"
echo ""

# Create virtual environment if it doesn't exist
if [ ! -d "venv" ]; then
    echo "Creating virtual environment..."
    python3 -m venv venv
    echo "✓ Virtual environment created"
    echo ""
fi

# Activate virtual environment
echo "Activating virtual environment..."
source venv/bin/activate
echo "✓ Virtual environment activated"
echo ""

# Install/upgrade requirements
echo "Installing Python dependencies..."
pip install --upgrade pip setuptools wheel > /dev/null 2>&1
pip install -r requirements.txt > /dev/null 2>&1
echo "✓ Dependencies installed"
echo ""

# Check for required system packages
echo "Checking for required system libraries..."

if ! pkg-config --exists opencv4 2>/dev/null && ! pkg-config --exists opencv 2>/dev/null; then
    echo ""
    echo "NOTE: OpenCV system libraries not found."
    echo "If you experience video capture issues, install:"
    echo "  Ubuntu/Debian: sudo apt-get install libopencv-dev"
    echo "  Fedora: sudo dnf install opencv-devel"
    echo ""
fi

echo ""
echo "=================================================="
echo "Starting Oak Board Detector..."
echo "=================================================="
echo ""
echo "The application will open at: http://localhost:5000"
echo "Press Ctrl+C to stop the server"
echo ""

# Run the application
cd app
python3 app.py
