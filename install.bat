@echo off
echo.
echo ========================================
echo Orion Sandbox - Windows 7 32-bit Installer
echo ========================================
echo.
echo This will install all required files...
echo.

REM Check if Python is installed
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo ERROR: Python is not installed or not in PATH
    echo.
    echo Please download Python 3.8 (32-bit) from:
    echo https://www.python.org/downloads/release/python-3810/
    echo.
    echo Then run this installer again.
    pause
    exit /b 1
)

echo Found Python installation.
echo.

REM Create lib directory if it doesn't exist
if not exist "lib" mkdir lib

echo Installing pygame...
pip install pygame==2.1.3 -t lib --no-cache-dir

if %errorlevel% neq 0 (
    echo Failed to install pygame
    echo Trying alternative method...
    pip install pygame==2.0.3 -t lib --no-cache-dir
)

echo.
echo Installation complete!
echo.
echo To play the game, double-click: play.bat
echo.
pause
