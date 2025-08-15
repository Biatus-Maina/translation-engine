@echo off
echo Starting Translation Engine...
echo.
echo Activating virtual environment...
call venv\Scripts\activate.bat
echo.
echo Starting FastAPI server...
echo.
echo Web Interface: http://localhost:8000
echo API Documentation: http://localhost:8000/docs
echo.
echo Press Ctrl+C to stop the server
echo.
python -m uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
pause 