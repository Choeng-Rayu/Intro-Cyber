# Malware Auto-Execution Demo - Educational Only

## 🎯 Goal
Understand how malware **auto-executes without user clicking** after download.

## 🔄 The Flow

### On Victim's Computer (runs detector.py as background service):
```
1. detector.py runs in background (auto-starts with Windows)
2. Monitors Downloads folder constantly
3. When ANY .exe appears → auto-executes it immediately
4. User never clicks anything - just downloads via Telegram
```

### Attack Scenario:
```
Attacker → Sends autoRun.exe via Telegram
         ↓
Victim → Clicks download button in Telegram
         ↓
File downloads to Downloads folder
         ↓
detector.py sees the new .exe file
         ↓
AUTO-EXECUTES in background (no window, no click needed!)
         ↓
autoRun.py runs silently:
  - Hides window
  - Adds to startup
  - Logs system info
         ↓
Victim has no idea anything happened!
```

## 🚀 How to Test

### Step 1: Setup Victim Computer (Test Machine)
```powershell
# Make detector.py run as background service
python detector.py
```

**Better: Make it auto-start with Windows**
```powershell
# Add to startup (victim's machine)
python setup_autorun_service.py
```

### Step 2: Build the Malware
```powershell
# On attacker's machine
build_malware.bat
```

### Step 3: Simulate Attack
```
1. Send dist\autoRun.exe via Telegram to victim
2. Victim clicks "Download" in Telegram
3. File goes to Downloads folder
4. detector.py auto-executes it immediately
5. autoRun.exe runs silently in background
6. Done! Malware is now persistent
```

### Step 4: Verify It Worked
```powershell
# Check if malware added itself to startup
reg query "HKCU\Software\Microsoft\Windows\CurrentVersion\Run"

# Check the hidden log file
notepad %TEMP%\log.txt

# Reboot and verify it auto-runs again
```

## 🔑 Key Points

**Why user doesn't notice:**
- ✅ No console window (--noconsole flag)
- ✅ Auto-executes via detector.py (no manual click)
- ✅ Runs in background (subprocess.Popen)
- ✅ Telegram just shows "Download complete"
- ✅ Victim thinks it's just a failed download

**How detector.py simulates vulnerability:**
- Represents misconfigured system
- Or malicious browser extension
- Or compromised auto-run service
- Real-world: Exploited software that monitors Downloads

**Real attack vectors:**
1. **Browser Exploit**: Auto-execute on download complete
2. **Malicious Extension**: Chrome/Firefox extension runs .exe
3. **Compromised Software**: Download manager auto-runs files
4. **Windows Vulnerability**: LNK file exploits, etc.

## 📁 Files

- `autoRun.py` - Simple malware (hides, persists, logs)
- `detector.py` - Auto-run service (simulates vulnerable system)
- `enhanced_detector.py` - Security tool (quarantines threats)
- `build_malware.bat` - Builds autoRun.exe

## ⚠️ Warning

**FOR EDUCATION ONLY!**
- Test only on isolated VM or test machine
- Never deploy on real systems
- Unauthorized use is illegal
- This demonstrates attack vectors for defense learning

## 🛡️ Defense

To protect against this:
1. **Don't run detector.py** (that's the vulnerability!)
2. **Run enhanced_detector.py** instead (it quarantines)
3. **Disable auto-run features**
4. **Use antivirus with behavior monitoring**
5. **Don't download .exe from untrusted sources**
