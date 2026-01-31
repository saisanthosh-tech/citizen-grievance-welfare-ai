@echo off
echo ========================================
echo Citizen Grievance System - DEMO MODE
echo ========================================
echo.
echo Starting backend in DEMO mode (no authentication required)...
echo.

cd backend
start "Backend API (Demo Mode)" cmd /k "venv\Scripts\activate && uvicorn app.main_demo:app --reload"

timeout /t 3 /nobreak > nul

echo.
echo Starting Streamlit frontend...
echo.

cd ..
start "Streamlit Frontend" cmd /k "streamlit run frontend_streamlit.py"

echo.
echo ========================================
echo System Started!
echo ========================================
echo.
echo Backend API: http://127.0.0.1:8000
echo API Docs: http://127.0.0.1:8000/docs
echo Streamlit UI: http://localhost:8501
echo.
echo Mode: DEMO (No authentication required)
echo.
echo Press any key to exit this window...
pause > nul
