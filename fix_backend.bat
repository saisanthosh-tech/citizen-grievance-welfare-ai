@echo off
echo ========================================
echo FIXING BACKEND SERVER CONFLICTS
echo ========================================
echo.

echo Step 1: Killing all Python/Uvicorn processes...
taskkill /F /IM python.exe 2>nul
timeout /t 2 /nobreak >nul

echo Step 2: Verifying port 8000 is free...
netstat -ano | findstr :8000
if %ERRORLEVEL% EQU 0 (
    echo WARNING: Port 8000 still in use, waiting...
    timeout /t 3 /nobreak >nul
)

echo.
echo Step 3: Starting CORRECT backend (app.main) on port 8000...
cd backend
start "Backend Server" cmd /k "venv\Scripts\python -m uvicorn app.main:app --reload --port 8000"

echo.
echo Step 4: Waiting for backend to start...
timeout /t 5 /nobreak >nul

echo.
echo Step 5: Testing backend...
curl http://localhost:8000/docs >nul 2>&1
if %ERRORLEVEL% EQU 0 (
    echo [SUCCESS] Backend is running!
) else (
    echo [WARNING] Backend may still be starting...
)

echo.
echo ========================================
echo BACKEND FIXED!
echo ========================================
echo.
echo Backend running on: http://localhost:8000
echo API Docs: http://localhost:8000/docs
echo.
echo Now you can:
echo 1. Register new user on React app
echo 2. Login with registered credentials
echo.
echo Press any key to close...
pause >nul
