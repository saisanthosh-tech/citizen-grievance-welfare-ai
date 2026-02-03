@echo off
REM Citizen Grievance & Welfare Intelligence System - Frontend Launcher
REM Streamlit-based government-grade UI

echo.
echo ==========================================
echo Citizen Grievance Welfare System - Frontend
echo ==========================================
echo.

REM Check if streamlit is installed
python -c "import streamlit" >nul 2>&1
if %errorlevel% neq 0 (
    echo [ERROR] Streamlit is not installed.
    echo.
    echo Please install dependencies first:
    echo   pip install -r requirements_frontend.txt
    echo.
    pause
    exit /b 1
)

echo [INFO] Starting Streamlit frontend...
echo [INFO] Frontend will be available at: http://localhost:8501
echo.
echo [IMPORTANT] Make sure the backend is running on http://127.0.0.1:8000
echo [IMPORTANT] If not started, open another terminal and run: run_backend.bat
echo.
echo Press Ctrl+C to stop the server
echo.

python -m streamlit run Home.py

pause
