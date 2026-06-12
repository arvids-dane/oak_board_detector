@echo off
REM Oak Board Detector - Windows Launcher
REM This script sets up and runs the application on Windows

setlocal enabledelayedexpansion

cls
echo ==================================================
echo Oak Board Detector - Windows Launcher
echo ==================================================
echo.

REM Check if Python is installed
python --version >nul 2>&1
if errorlevel 1 (
    echo ERROR: Python is not installed or not in PATH!
    echo.
    echo Please install Python 3.8 or higher from:
    echo   https://www.python.org/downloads/
    echo.
    echo Make sure to check "Add Python to PATH" during installation.
    echo.
    pause
    exit /b 1
)

for /f "tokens=2" %%i in ('python --version 2^>^&1') do set PYTHON_VERSION=%%i
echo [OK] Python %PYTHON_VERSION% detected
echo.

REM Check if pip is available
python -m pip --version >nul 2>&1
if errorlevel 1 (
    echo ERROR: pip is not available!
    echo Please ensure Python was installed with pip.
    pause
    exit /b 1
)

echo [OK] pip detected
echo.

REM Create virtual environment if it doesn't exist
if not exist "venv" (
    echo Creating virtual environment...
    python -m venv venv
    echo [OK] Virtual environment created
    echo.
)

REM Activate virtual environment
echo Activating virtual environment...
call venv\Scripts\activate.bat
echo [OK] Virtual environment activated
echo.

REM Install/upgrade requirements
echo Installing Python dependencies...
python -m pip install --upgrade pip setuptools wheel >nul 2>&1
pip install -r requirements.txt >nul 2>&1
echo [OK] Dependencies installed
echo.

echo ==================================================
echo Starting Oak Board Detector...
echo ==================================================
echo.
echo The application will open at: http://localhost:5000
echo Press Ctrl+C to stop the server
echo.

REM Run the application
cd app
python app.py

pause
