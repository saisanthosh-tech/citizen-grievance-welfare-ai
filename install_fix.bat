@echo off
echo ===================================================
echo     CITIZEN GRIEVANCE APP - INSTALL FIXER
echo ===================================================
echo.
echo 1. Cleaning old installation files...
cd frontend
if exist node_modules rmdir /s /q node_modules
if exist package-lock.json del package-lock.json
npm cache clean --force

echo.
echo 2. Installing dependencies (Verbose Mode)...
echo This may take a few minutes. Please wait...
echo.
npm install --loglevel verbose

echo.
echo ===================================================
echo IF THE INSTALLATION FAILED ABOVE:
echo Please take a screenshot of the error message or copy it.
echo.
echo IF IT SUCCEEDED:
echo You can now use run_app.bat to start the system.
echo ===================================================
pause
