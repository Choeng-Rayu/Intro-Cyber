# Java to EXE Conversion Guide

## Quick Start

### On Linux:
```bash
./create_exe.sh
```

### On Windows:
```cmd
create_exe.bat
```

---

## Method 1: jpackage (Recommended - Java 14+)

**Pros:** Bundles JRE, creates native installer  
**Cons:** Large file size, creates installer not single .exe

```bash
jpackage --input . \
         --name test \
         --main-jar test.jar \
         --main-class test \
         --type exe
```

---

## Method 2: Launch4j (Most Popular)

**Pros:** Small .exe wrapper, widely used  
**Cons:** Requires Java on target machine

### Steps:
1. Download Launch4j: https://launch4j.sourceforge.net/
2. Create JAR: `jar cfe test.jar test test.class`
3. Load `launch4j_config.xml` in Launch4j GUI
4. Click "Build wrapper"

---

## Method 3: GraalVM Native Image (Best)

**Pros:** True native .exe, no JRE needed, fast startup  
**Cons:** Complex setup

```bash
# Install GraalVM
sdk install java 21-graalvm

# Compile to native
native-image -jar test.jar test
```

---

## Method 4: jlink + jpackage (Custom JRE)

**Pros:** Smaller than full JRE bundle  
**Cons:** More complex

```bash
jlink --add-modules java.base --output custom-jre
jpackage --runtime-image custom-jre --input . --main-jar test.jar
```

---

## Simple Wrapper Scripts

### Windows BAT file:
```batch
@echo off
java -jar test.jar %*
```

### Linux/Mac Shell:
```bash
#!/bin/bash
java -jar test.jar "$@"
```

---

## File Requirements

- `test.java` - Source code
- `test.class` - Compiled bytecode
- `test.jar` - Executable JAR

## Platform Support

| Method | Windows | Linux | Mac |
|--------|---------|-------|-----|
| jpackage | ✓ | ✓ | ✓ |
| Launch4j | ✓ | ✗ | ✗ |
| GraalVM | ✓ | ✓ | ✓ |
| Wrapper | ✓ | ✓ | ✓ |
