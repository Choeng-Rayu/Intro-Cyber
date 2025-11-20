@echo off
REM =============================================================
REM  Smart Cleaner - EXE Builder
REM  This script converts the Python script to a standalone .exe
REM =============================================================

echo.
echo ========================================
echo  Smart Cleaner - EXE Conversion
echo ========================================
echo.

REM Check if running as Administrator
net session >nul 2>&1
if %errorLevel% neq 0 (
    echo ERROR: This script must be run as Administrator!
    echo.
    echo Steps to run as Administrator:
    echo 1. Right-click this batch file
    echo 2. Click "Run as Administrator"
    echo 3. Click "Yes" on the UAC prompt
    echo.
    pause
    exit /b 1
)

echo [Step 1] Checking Python installation...
python --version >nul 2>&1
if %errorLevel% neq 0 (
    echo ERROR: Python is not installed or not in PATH!
    echo.
    echo To fix this:
    echo 1. Install Python from https://www.python.org/downloads/
    echo 2. Make sure to check "Add Python to PATH" during installation
    echo.
    pause
    exit /b 1
)
echo Python found: 
python --version
echo.

echo [Step 2] Installing PyInstaller...
pip install pyinstaller
if %errorLevel% neq 0 (
    echo ERROR: Failed to install PyInstaller
    pause
    exit /b 1
)
echo PyInstaller installed successfully!
echo.

echo [Step 3] Building executable...
echo This may take a minute or two...
echo.

REM Remove old build artifacts
if exist build rmdir /s /q build
if exist dist rmdir /s /q dist
if exist *.spec del *.spec

REM Create the .exe file
pyinstaller --onefile --console --name=SmartCleaner deleteFolderWindown_Dynamic.py

if %errorLevel% neq 0 (
    echo ERROR: EXE build failed!
    pause
    exit /b 1
)

echo.
echo ========================================
echo  SUCCESS! EXE Created!
echo ========================================
echo.
echo Location: %CD%\dist\SmartCleaner.exe
echo.
echo Next steps:
echo 1. Copy SmartCleaner.exe to your desired location
echo 2. Create a shortcut for quick access
echo 3. Set up Windows Task Scheduler (optional)
echo.
echo Usage:
echo   SmartCleaner.exe                    (interactive mode)
echo   SmartCleaner.exe D:\ 5              (auto mode, D: drive, 5 second interval)
echo   SmartCleaner.exe D:\ 5 14:30        (with scheduled time)
echo.
echo Log files will be saved to:
echo   %APPDATA%\SmartCleaner\deletion_log.txt
echo.
pause
