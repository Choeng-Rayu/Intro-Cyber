@echo off
REM Create a simple wrapper for test.exe
REM This batch file will be converted to .exe using Bat2Exe

title Test Application
echo Starting Test Application...
java -jar test.jar
pause
