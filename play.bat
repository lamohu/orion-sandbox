@echo off
echo.
echo ========================================
echo Orion Sandbox - Starting Game
echo ========================================
echo.

REM Check if Python exists
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo ERROR: Python not found!
    echo Please run install.bat first.
    pause
    exit /b 1
)

REM Check if pygame is installed
python -c "import pygame" >nul 2>&1
if %errorlevel% neq 0 (
    echo pygame not found. Installing...
    call install.bat
)

echo.
echo Starting Orion Sandbox...
echo.

REM Run the game
python game_simple.py

if %errorlevel% neq 0 (
    echo.
    echo Game crashed. Please check the error message above.
    echo If you continue to have issues, run install.bat again.
    pause
)
