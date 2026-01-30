@echo off
echo Starting Flood Forecasting System (Next.js Edition)...

echo Checking Backend...
cd backend
if not exist "venv" (
    echo Creating virtual environment...
    python -m venv venv
)
call venv\Scripts\activate
pip install -r requirements.txt > nul 2>&1

echo Building Next.js Frontend...
cd ../frontend-next
call cmd /c npm install
call cmd /c npm run build
cd ../backend

echo Starting Unified Server...
echo Access the app at: http://localhost:8000
uvicorn main:app --reload --port 8000

pause
