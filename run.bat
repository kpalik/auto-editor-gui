@echo off
echo Starting Auto-Editor GUI...
echo.

cd /d "%~dp0"

if not exist "src\main.py" (
    echo Error: main.py not found!
    echo Please run this script from the auto-editor-gui directory.
    pause
    exit /b 1
)

python src\main.py

if errorlevel 1 (
    echo.
    echo Error: Failed to start application.
    echo.
    echo Please ensure:
    echo 1. Python is installed and in PATH
    echo 2. Dependencies are installed: pip install -r requirements.txt
    echo 3. auto-editor is installed: pip install auto-editor
    echo.
    pause
)
