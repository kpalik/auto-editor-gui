@echo off
echo Installing Auto-Editor GUI Dependencies...
echo.

cd /d "%~dp0"

echo Step 1: Installing Python packages...
pip install -r requirements.txt

if errorlevel 1 (
    echo.
    echo Error: Failed to install dependencies.
    echo Please ensure Python and pip are installed correctly.
    pause
    exit /b 1
)

echo.
echo Step 2: Testing installation...
python test_installation.py

echo.
echo Installation complete!
echo.
echo To run the application, use: run.bat
echo Or: python src\main.py
echo.
pause
