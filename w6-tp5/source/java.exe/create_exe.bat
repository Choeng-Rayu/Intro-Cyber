@echo off
REM Windows batch script to convert JAR to EXE using jpackage

echo =========================================
echo Java to EXE Converter (Windows)
echo =========================================

REM Check if test.jar exists
if not exist "test.jar" (
    echo [*] Compiling Java file...
    javac test.java
    jar cfe test.jar test test.class
)

echo [*] Creating native Windows executable...
echo.

REM Option 1: Using jpackage (Java 14+)
jpackage --input . --name test --main-jar test.jar --main-class test --type exe --win-console

if exist "test.exe" (
    echo [+] SUCCESS! Created test.exe
    dir test.exe
) else (
    echo [-] Failed. Trying alternative method...
    echo.
    echo Alternative: Download Launch4j from https://launch4j.sourceforge.net/
    echo Then use launch4j-config.xml to convert JAR to EXE
)

pause
