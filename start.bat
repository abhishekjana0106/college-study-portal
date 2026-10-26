@echo off
title Centralized College Study Material & Question Paper Portal
cd /d "%~dp0"

echo ======================================================================
echo   CENTRALIZED COLLEGE STUDY MATERIAL & QUESTION PAPER PORTAL
echo ======================================================================
echo.

python --version >nul 2>&1
if errorlevel 1 (
    echo [ERROR] Python is not installed or not in system PATH!
    echo Please install Python 3.9+ from https://www.python.org/
    pause
    exit /b 1
)

if not exist portal.db (
    echo [INFO] First time initialization: Seeding database and sample materials...
    python seed_data.py
    echo [OK] Database seeded successfully!
)

echo.
echo [STARTING] Launching Academix Portal Web Server...
echo [INFO] Press CTRL+C at any time to stop the server.
echo.

python app.py

pause
