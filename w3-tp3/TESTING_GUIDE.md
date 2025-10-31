# Testing Guide: Malware Auto-Execution Simulation

## ⚠️ IMPORTANT SAFETY NOTICE
**Test ONLY in isolated, controlled environments!**
- Use virtual machines (VMware, VirtualBox)
- Never test on production systems
- Disable network connections during testing
- Take VM snapshots before testing

---

## Setup Instructions

### 1. Prepare Test Environment

#### Option A: Windows Virtual Machine (Recommended)
```
1. Install VirtualBox or VMware
2. Create Windows 10/11 VM
3. Take a clean snapshot
4. Install Python 3.8+ on VM
5. Disable Windows Defender (for testing only):
   Settings → Windows Security → Virus & threat protection → Manage settings → Turn OFF
```

#### Option B: Separate Physical Test Machine
```
1. Use an old/spare computer
2. Fresh Windows installation
3. Not connected to important networks
4. No sensitive data on the system
```

### 2. Install Dependencies

**On your development machine:**
```powershell
cd d:\Y3-Term1\Cyber-Security\TP3\Intro-Cyber\w3-tp3
pip install pyinstaller
```

---

## Test Scenarios

### Scenario 1: Basic Auto-Execution via Downloads Folder

**Purpose:** Test if detector catches executable in Downloads folder

**Steps:**
1. **On Test Machine:**
   ```powershell
   # Start the detector
   python detector.py
   ```

2. **On Development Machine:**
   ```powershell
   # Build the executable
   build_malware.bat
   ```

3. **Transfer to Test Machine:**
   - Copy `dist\autoRun.exe` to USB drive
   - Or use network share
   - Place in Downloads folder

4. **Observe:**
   - Detector should detect and execute it
   - Check if console appears (it shouldn't)
   - Check `%TEMP%\system_log.txt` for payload output

**Expected Result:**
- ✅ autoRun.exe executes silently
- ✅ No visible window
- ✅ system_log.txt is created
- ✅ Registry entry added

---

### Scenario 2: Simulated Telegram Download

**Purpose:** Mimic real-world Telegram file delivery

**Steps:**
1. **On Development Machine:**
   - Rename `autoRun.exe` to something deceptive:
     ```powershell
     copy dist\autoRun.exe dist\Assignment_Report.exe
     ```
   - Or even better: `Important_Document.pdf.exe` (double extension trick)

2. **Simulate Telegram Download:**
   - On test machine, ensure detector is running
   - Manually copy file to Downloads folder (simulating Telegram download)
   - In real scenario, user would download via Telegram

3. **Observe Execution:**
   - File should auto-execute via detector
   - No visible signs to user
   - Malware persists in startup

**Expected Result:**
- ✅ Executes without user noticing
- ✅ Adds to startup registry
- ✅ Survives reboot

---

### Scenario 3: Enhanced Detection with Security Monitor

**Purpose:** Test enhanced detector's ability to catch and quarantine

**Steps:**
1. **Stop basic detector**

2. **Start enhanced detector:**
   ```powershell
   python enhanced_detector.py
   ```

3. **Drop malware in Downloads:**
   - Copy autoRun.exe to Downloads
   - Enhanced detector should:
     - Detect immediately
     - Calculate hash
     - Analyze threat level
     - Quarantine automatically

4. **Check Results:**
   - Review `security_log.txt`
   - Check `quarantine\` folder
   - Verify file was moved

**Expected Result:**
- ✅ Immediate detection
- ✅ Threat analysis logged
- ✅ File quarantined
- ✅ No execution occurred

---

### Scenario 4: Persistence Testing

**Purpose:** Verify malware survives system reboot

**Steps:**
1. **Allow autoRun.exe to execute once**
   - It adds itself to registry

2. **Check Registry:**
   ```powershell
   reg query "HKCU\Software\Microsoft\Windows\CurrentVersion\Run"
   ```
   - Look for "SystemUpdate" entry

3. **Reboot test machine**

4. **After Reboot:**
   - Check Task Manager for running process
   - Check if new entries in system_log.txt
   - Verify it auto-started

**Expected Result:**
- ✅ Registry entry created
- ✅ Auto-starts after reboot
- ✅ Runs silently again

---

### Scenario 5: Full Attack Simulation

**Purpose:** Complete end-to-end attack simulation

**Steps:**

#### Phase 1: Attacker (Your Development Machine)
```powershell
# 1. Build malware with deceptive name
pyinstaller --onefile --noconsole --name "Homework_Assignment" autoRun.py

# 2. Add fake icon (optional)
# Find a document icon and use: --icon=document.ico

# 3. Prepare for "sending"
# In real scenario, attacker would upload to Telegram
```

#### Phase 2: Delivery (Simulation)
```
1. Transfer to USB drive
2. Label as "School_Project.exe" or similar
3. Bring to test machine
```

#### Phase 3: Victim (Test Machine)
```powershell
# Victim receives file via Telegram
# Victim downloads to Downloads folder
# Detector is NOT running (realistic scenario)
# Victim double-clicks the file
```

#### Phase 4: Observation
```
1. File executes silently
2. No window appears
3. Victim thinks nothing happened
4. Malware is now persistent
5. Check %TEMP%\system_log.txt
6. Check startup registry
```

#### Phase 5: Detection (Deploy Security)
```powershell
# Now deploy your detector
python enhanced_detector.py

# It should detect:
# - Suspicious registry entries
# - Existing malware files
# - Log the threat
```

**Expected Result:**
- ✅ Realistic attack flow demonstrated
- ✅ Malware executes undetected initially
- ✅ Enhanced detector finds it later
- ✅ Quarantine successful

---

## Verification Checklist

After each test, verify:

- [ ] Check if `system_log.txt` exists in `%TEMP%`
- [ ] Check registry: `HKCU\Software\Microsoft\Windows\CurrentVersion\Run`
- [ ] Check if detector logged events
- [ ] Check quarantine folder for captured files
- [ ] Verify no visible windows appeared
- [ ] Test persistence (reboot)

---

## Cleanup Procedures

### Manual Cleanup
```powershell
# 1. Remove from registry
reg delete "HKCU\Software\Microsoft\Windows\CurrentVersion\Run" /v "SystemUpdate" /f

# 2. Delete payload log
del "%TEMP%\system_log.txt"

# 3. Kill process if running
tasklist | findstr autoRun
taskkill /F /IM autoRun.exe

# 4. Delete executable
del "%USERPROFILE%\Downloads\autoRun.exe"

# 5. Clear quarantine
rmdir /S /Q "quarantine"
```

### Automated Cleanup Script
Create `cleanup.bat`:
```batch
@echo off
echo Cleaning up malware simulation...
reg delete "HKCU\Software\Microsoft\Windows\CurrentVersion\Run" /v "SystemUpdate" /f 2>nul
del "%TEMP%\system_log.txt" 2>nul
taskkill /F /IM autoRun.exe 2>nul
del "%USERPROFILE%\Downloads\autoRun.exe" 2>nul
del "%USERPROFILE%\Downloads\*.exe" 2>nul
rmdir /S /Q "quarantine" 2>nul
echo Cleanup complete!
pause
```

---

## Troubleshooting

### Issue: Detector doesn't execute the file
**Solution:**
- Ensure detector.py is running before file appears
- Check WATCH_DIR path is correct
- Verify file name is exactly "autorun.exe" (case-insensitive)

### Issue: Windows Defender blocks the file
**Solution:**
- Temporarily disable Windows Defender
- Add exclusion for test folder
- Or test in VM without antivirus

### Issue: Console window appears
**Solution:**
- Rebuild with `--noconsole` flag
- Ensure you're running the .exe, not .py file
- Check PyInstaller build output for errors

### Issue: Registry entry not created
**Solution:**
- Check if running with proper permissions
- Verify Windows user has registry write access
- Check for error in system_log.txt

### Issue: File doesn't persist after reboot
**Solution:**
- Verify registry entry exists before reboot
- Check if antivirus removed it
- Ensure full path to executable is correct in registry

---

## Learning Objectives

After completing these tests, you should understand:

1. ✅ **How malware achieves auto-execution**
   - Windows startup mechanisms
   - Registry manipulation
   - Silent execution techniques

2. ✅ **Why it's effective**
   - No visible indicators
   - Survives reboots
   - Bypasses basic user awareness

3. ✅ **How to detect it**
   - File system monitoring
   - Registry monitoring
   - Behavioral analysis
   - Threat scoring

4. ✅ **How to defend against it**
   - Endpoint detection
   - Quarantine procedures
   - User education
   - System hardening

---

## Advanced Exercises

### Exercise 1: Improve Evasion
Try to modify autoRun.py to:
- Change registry key location
- Use Task Scheduler instead
- Encrypt the payload log
- Add anti-detection techniques

### Exercise 2: Improve Detection
Enhance enhanced_detector.py to:
- Monitor Task Scheduler
- Check for process hollowing
- Implement YARA rules
- Add network traffic monitoring

### Exercise 3: Create Countermeasures
Build a tool that:
- Automatically removes persistence
- Repairs system after infection
- Creates restore points
- Blocks known attack vectors

---

## Report Template

Document your findings:

```markdown
## Test Report: Malware Auto-Execution Simulation

**Date:** [Date]
**Tester:** [Your Name]
**Environment:** [VM/Physical, OS Version]

### Test Results

#### Scenario 1: Basic Auto-Execution
- Result: [Pass/Fail]
- Observations: [What happened]
- Evidence: [Screenshots, logs]

#### Scenario 2: Telegram Simulation
- Result: [Pass/Fail]
- Observations: [What happened]
- Evidence: [Screenshots, logs]

[Continue for each scenario]

### Key Findings
1. [Finding 1]
2. [Finding 2]
3. [Finding 3]

### Recommendations
1. [Recommendation 1]
2. [Recommendation 2]
3. [Recommendation 3]

### Conclusion
[Your analysis of the exercise]
```

---

## Next Steps

After mastering these basics:
1. Study real malware samples (in isolated environment)
2. Learn about advanced persistence techniques
3. Explore memory forensics
4. Study reverse engineering
5. Practice incident response

**Resources:**
- MITRE ATT&CK Framework
- Malware Analysis courses
- Practical Malware Analysis book
- Security certifications (CEH, OSCP)

---

**Remember:** This knowledge is for defense, not offense. Always follow ethical guidelines and legal requirements.
