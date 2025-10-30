@echo off
REM Setup Script to Convert Python to EXE and Create Service
REM Run this as Administrator

echo.
echo ================================================
echo  Smart Cleaner - Setup and Installation
echo ================================================
echo.

REM Check if running as Administrator
net session >nul 2>&1
if %errorLevel% neq 0 (
    echo ERROR: This script must be run as Administrator!
    echo Right-click and select "Run as Administrator"
    pause
    exit /b 1
)

echo [1/4] Installing PyInstaller...
pip install pyinstaller
if %errorLevel% neq 0 (
    echo ERROR: Failed to install PyInstaller
    pause
    exit /b 1
)

echo.
echo [2/4] Creating EXE file...
pyinstaller --onefile --console deleteFolderWindown_Dynamic.py
if %errorLevel% neq 0 (
    echo ERROR: Failed to create EXE
    pause
    exit /b 1
)

echo.
echo [3/4] EXE created successfully!
echo Location: %CD%\dist\deleteFolderWindown_Dynamic.exe

echo.
echo [4/4] To run as a Windows Service, you can:
echo.
echo Option A: Use Windows Task Scheduler
echo   - Press Win+R, type taskschd.msc
echo   - Create new task with the EXE
echo.
echo Option B: Use NSSM (Non-Sucking Service Manager)
echo   - Download from https://nssm.cc/download
echo   - Run: nssm install SmartCleaner "C:\path\to\deleteFolderWindown_Dynamic.exe" "D:\ 5"
echo.

echo.
echo ================================================
echo  Setup Complete!
echo ================================================
echo.
pause
