@echo off
echo Starting Citizen Grievance Intelligence System...

echo Starting Backend...
start "Backend API" cmd /k "cd backend && venv\Scripts\activate && uvicorn app.main:app --reload"

echo Starting Frontend...
echo You may need to run 'npm install' in the frontend directory first if this fails.
start "Frontend Dashboard" cmd /k "cd frontend && echo Cleaning artifacts... && if exist node_modules rmdir /s /q node_modules && if exist package-lock.json del package-lock.json && npm cache clean --force && echo Installing dependencies (this may take a while)... && npm install --force && npm run dev"

echo Done!
echo Backend: http://127.0.0.1:8000
echo Frontend: http://localhost:5324
pause
