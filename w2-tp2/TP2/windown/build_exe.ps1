# Smart Cleaner - EXE Builder (PowerShell)
# Run this in PowerShell as Administrator

Write-Host "========================================" -ForegroundColor Cyan
Write-Host "  Smart Cleaner - EXE Conversion" -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""

# Check if running as Administrator
$isAdmin = ([Security.Principal.WindowsPrincipal] [Security.Principal.WindowsIdentity]::GetCurrent()).IsInRole([Security.Principal.WindowsBuiltInRole] "Administrator")

if (-not $isAdmin) {
    Write-Host "ERROR: This script must be run as Administrator!" -ForegroundColor Red
    Write-Host ""
    Write-Host "How to run as Administrator:" -ForegroundColor Yellow
    Write-Host "1. Right-click PowerShell"
    Write-Host "2. Select 'Run as Administrator'"
    Write-Host "3. Navigate to this script folder"
    Write-Host "4. Run: .\build_exe.ps1"
    Write-Host ""
    Read-Host "Press Enter to exit"
    exit 1
}

# Step 1: Check Python
Write-Host "[Step 1] Checking Python installation..." -ForegroundColor Green
$pythonVersion = python --version 2>&1
if ($LASTEXITCODE -ne 0) {
    Write-Host "ERROR: Python is not installed or not in PATH!" -ForegroundColor Red
    Write-Host ""
    Write-Host "To fix this:" -ForegroundColor Yellow
    Write-Host "1. Download Python from https://www.python.org/downloads/"
    Write-Host "2. Run the installer"
    Write-Host "3. CHECK: 'Add Python to PATH'"
    Write-Host "4. Click 'Install Now'"
    Write-Host "5. Restart PowerShell"
    Write-Host ""
    Read-Host "Press Enter to exit"
    exit 1
}
Write-Host "Python found: $pythonVersion" -ForegroundColor Green
Write-Host ""

# Step 2: Install PyInstaller
Write-Host "[Step 2] Installing PyInstaller..." -ForegroundColor Green
pip install pyinstaller
if ($LASTEXITCODE -ne 0) {
    Write-Host "ERROR: Failed to install PyInstaller" -ForegroundColor Red
    Read-Host "Press Enter to exit"
    exit 1
}
Write-Host "PyInstaller installed successfully!" -ForegroundColor Green
Write-Host ""

# Step 3: Clean old builds
Write-Host "[Step 3] Cleaning old build files..." -ForegroundColor Green
if (Test-Path "build") { Remove-Item -Recurse -Force "build" }
if (Test-Path "dist") { Remove-Item -Recurse -Force "dist" }
if (Test-Path "*.spec") { Remove-Item -Force "*.spec" }
Write-Host "Old files cleaned" -ForegroundColor Green
Write-Host ""

# Step 4: Build EXE
Write-Host "[Step 4] Building executable..." -ForegroundColor Green
Write-Host "This may take a minute or two..." -ForegroundColor Yellow
Write-Host ""

pyinstaller --onefile --console --name=SmartCleaner deleteFolderWindown_Dynamic.py

if ($LASTEXITCODE -ne 0) {
    Write-Host "ERROR: EXE build failed!" -ForegroundColor Red
    Read-Host "Press Enter to exit"
    exit 1
}

# Success!
Write-Host ""
Write-Host "========================================" -ForegroundColor Green
Write-Host "  SUCCESS! EXE Created!" -ForegroundColor Green
Write-Host "========================================" -ForegroundColor Green
Write-Host ""
Write-Host "Location: $(Get-Location)\dist\SmartCleaner.exe" -ForegroundColor Cyan
Write-Host ""
Write-Host "Next steps:" -ForegroundColor Yellow
Write-Host "1. Copy SmartCleaner.exe to your desired location"
Write-Host "2. Create a shortcut for quick access"
Write-Host "3. Set up Windows Task Scheduler (optional)"
Write-Host ""
Write-Host "Usage:" -ForegroundColor Yellow
Write-Host "  SmartCleaner.exe                (interactive mode)"
Write-Host "  SmartCleaner.exe D:\ 5          (auto mode)"
Write-Host "  SmartCleaner.exe D:\ 5 14:30    (with schedule)"
Write-Host ""
Write-Host "Log files will be saved to:" -ForegroundColor Yellow
Write-Host "  $env:APPDATA\SmartCleaner\deletion_log.txt"
Write-Host ""

Read-Host "Press Enter to exit"
