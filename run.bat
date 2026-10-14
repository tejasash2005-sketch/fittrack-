@echo off
echo ======================================================
echo   ⚡ FITTRACK - PREPARING ENVIRONMENT
echo ======================================================

:: Check if Python is installed
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo [ERROR] Python is not installed or not in PATH.
    pause
    exit /b
)

:: Create Virtual Environment if it doesn't exist
if not exist "venv" (
    echo [1/5] Creating Virtual Environment...
    python -m venv venv
)

:: Activate Venv
call venv\Scripts\activate

:: Install Dependencies
echo [2/5] Installing Dependencies...
pip install -r requirements.txt

:: Run Migrations
echo [3/5] Applying Database Migrations...
python manage.py makemigrations accounts workouts diet metrics admin_panel
python manage.py migrate

:: Seed Data
echo [4/5] Seeding Initial Data...
python manage.py seed_data

:: Start Server
echo [5/5] Starting FitTrack Server...
echo ------------------------------------------------------
echo   ACCESS AT: http://127.0.0.1:8000
echo ------------------------------------------------------
start http://127.0.0.1:8000
python manage.py runserver
