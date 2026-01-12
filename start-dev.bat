@echo off
REM Development startup script for MooAgent (Windows)
REM This script starts both backend and frontend servers

echo Starting MooAgent Development Servers...
echo.

REM Check if .env files exist
if not exist "backend\.env" (
    echo Backend .env file not found!
    echo Run: copy backend\.env.example backend\.env
    echo Then configure your environment variables.
    exit /b 1
)

if not exist "frontend\.env" (
    echo Frontend .env file not found. Creating from example...
    copy frontend\.env.example frontend\.env
)

REM Start backend
echo Starting Backend (FastAPI)...
cd backend

REM Activate virtual environment if it exists
if exist "venv\Scripts\activate.bat" (
    call venv\Scripts\activate.bat
) else (
    echo Virtual environment not found. Creating...
    python -m venv venv
    call venv\Scripts\activate.bat
    pip install -r requirements.txt
)

start "MooAgent Backend" cmd /k "python main.py"
cd ..

REM Wait for backend to start
echo Waiting for backend to start...
timeout /t 5 /nobreak >nul

REM Start frontend
echo.
echo Starting Frontend (React + Vite)...
cd frontend

REM Install dependencies if node_modules doesn't exist
if not exist "node_modules" (
    echo Node modules not found. Installing...
    call npm install
)

start "MooAgent Frontend" cmd /k "npm run dev"
cd ..

echo.
echo ==========================================
echo MooAgent is starting!
echo ==========================================
echo.
echo API Documentation: http://localhost:8000/docs
echo Chat Interface:    http://localhost:3000
echo.
echo Press any key to continue...
pause >nul
