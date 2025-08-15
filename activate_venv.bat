@echo off
echo Activating Translation Engine Virtual Environment...
echo.
call venv\Scripts\activate.bat
echo.
echo Virtual environment activated! You can now run:
echo   python start.py
echo   python -m uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
echo   python test_app.py
echo   python demo.py
echo.
echo To deactivate, type: deactivate
echo.
cmd /k 