# W3-TP3: Auto-Execution Attack Vector - Educational Analysis

## Objective
Understand how malware can be delivered and automatically executed on a victim's system.

## Attack Flow Diagram
```
┌─────────────────────────────────────────────────┐
│ 1. ATTACKER creates malicious Python script     │
│    └─> payload.py (contains malware logic)      │
└────────────────┬────────────────────────────────┘
                 │
┌────────────────▼────────────────────────────────┐
│ 2. CONVERSION to .exe using PyInstaller         │
│    └─> payload.exe (portable Windows binary)    │
└────────────────┬────────────────────────────────┘
                 │
┌────────────────▼────────────────────────────────┐
│ 3. SOCIAL ENGINEERING to get victim to download │
│    └─> email attachment, malicious link, etc.   │
└────────────────┬────────────────────────────────┘
                 │
┌────────────────▼────────────────────────────────┐
│ 4. VICTIM DOWNLOADS file to Downloads/          │
│    └─> observe.py running in background         │
└────────────────┬────────────────────────────────┘
                 │
┌────────────────▼────────────────────────────────┐
│ 5. observe.py DETECTS .exe file                 │
│    └─> Monitors Downloads folder constantly     │
└────────────────┬────────────────────────────────┘
                 │
┌────────────────▼────────────────────────────────┐
│ 6. AUTO-EXECUTION via subprocess.run()          │
│    └─> Malicious .exe runs with user privileges │
└────────────────┬────────────────────────────────┘
                 │
┌────────────────▼────────────────────────────────┐
│ 7. PAYLOAD EXECUTES (prints "Hello World")      │
│    └─> In real attack: steals data, installs    │
│        backdoor, encrypts files, etc.           │
└─────────────────────────────────────────────────┘
```

## Code Analysis: observe.py

### What It Does:
1. **Line 6**: Sets watch directory to Downloads folder
2. **Line 8**: Takes initial snapshot of files
3. **Line 10-19**: Infinite loop that:
   - Gets current files
   - Finds NEW files (new_files = current - seen)
   - If file ends with `.exe`, runs it with subprocess
   - Updates seen set
4. **Line 20**: Removes deleted files from tracking
5. **Line 21**: Wait 1 second before next check

### Why It's Dangerous:
- ✗ No validation of executable origin
- ✗ No user confirmation before execution
- ✗ Runs with current user's privileges
- ✗ Could compromise entire system

## Defense Mechanisms

### OS-Level:
- Windows SmartScreen (warns about unknown publishers)
- Code signing certificates (expensive, deters legitimate use)
- UAC prompts (User Account Control)

### User-Level:
- Never execute files from unknown sources
- Verify file signatures
- Use antivirus scanning

### Code-Level:
- Whitelist trusted applications only
- Require user confirmation
- Log all execution attempts
- Use sandboxing

## Example: Safe Implementation
```python
# Instead of auto-executing:
if path.suffix.lower() == ".exe":
    logging.warning(f"Suspicious .exe detected: {name}")
    # Require user confirmation
    # Scan with antivirus
    # Log for audit trail
    # DO NOT auto-execute
```

## Learning Outcomes
After this exercise, you should understand:
1. ✓ How attackers deliver malware
2. ✓ Why file monitoring is useful (and dangerous)
3. ✓ The importance of code signing and verification
4. ✓ Defense-in-depth principles
5. ✓ User awareness in security

## References
- [OWASP - Execution After Download](https://owasp.org/www-community/attacks/Execution_After_Download)
- [CWE-427: Uncontrolled Search Path Element](https://cwe.mitre.org/data/definitions/427.html)
- [PyInstaller Documentation](https://pyinstaller.org/)

---
⚠️ **DISCLAIMER**: This is for educational purposes only. Creating and distributing malware is illegal.
