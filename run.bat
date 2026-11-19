@echo off
title TrafficSense Delhi AI Dashboard Launcher
echo ===============================================================
echo        TrafficSense Delhi - AI Traffic Management System
echo ===============================================================
echo.
echo [1/3] Checking ML Service (Port 5001)...
start "TrafficSense ML Service" /min cmd /k "cd /d "%~dp0ml-service" && python app.py"

echo [2/3] Starting Frontend Dev Server (Port 5173)...
start "TrafficSense Frontend" cmd /k "cd /d "%~dp0frontend" && npm run dev"

echo [3/3] Launching Web Browser...
timeout /t 3 /nobreak >nul
start http://localhost:5173

echo.
echo TrafficSense is live!
echo Dashboard URL : http://localhost:5173
echo ML Service    : http://127.0.0.1:5001/health
echo ===============================================================
pause
