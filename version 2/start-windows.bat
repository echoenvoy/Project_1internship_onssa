@echo off
chcp 65001 >nul
title Stock Manager Professional

echo ========================================
echo    Stock Manager Professional
echo ========================================
echo.

:: Check if Python is installed
python --version >nul 2>&1
if errorlevel 1 (
    echo ❌ Python is not installed or not in PATH
    echo Please install Python 3.8+ from python.org
    pause
    exit /b 1
)

:: Check if virtual environment exists
if not exist "venv" (
    echo Creating virtual environment...
    python -m venv venv
)

:: Activate virtual environment
echo Activating virtual environment...
call venv\Scripts\activate.bat

:: Install requirements
echo Installing dependencies...
pip install -r requirements.txt

:: Initialize database
echo Initializing database...
python backend/database.py

:: Start the application
echo.
echo Starting Stock Manager Professional...
echo Access the application at: http://localhost:5000
echo Press Ctrl+C to stop the server
echo.
python backend/app.py

pause