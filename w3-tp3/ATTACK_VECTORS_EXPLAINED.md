# Malware Auto-Execution Techniques on Windows
## Educational Guide - Understanding Attack Vectors

**⚠️ WARNING: For Educational Purposes Only**
This document explains malware techniques for cybersecurity education. Never use these techniques maliciously.

---

## Table of Contents
1. [How Malware Auto-Executes](#how-malware-auto-executes)
2. [Attack Workflow](#attack-workflow)
3. [Technical Implementation](#technical-implementation)
4. [Detection Methods](#detection-methods)
5. [Defense Strategies](#defense-strategies)

---

## How Malware Auto-Executes

### 1. **Delivery Mechanisms**

#### A. Social Engineering
- **Fake documents**: "Invoice.pdf.exe" (double extension trick)
- **Legitimate-looking icons**: Using PDF, Word, or image icons
- **Urgent messaging**: "Your package is delayed - click here"

#### B. File Sharing Platforms
- **Telegram/Discord**: Direct file sharing bypasses some security
- **Email attachments**: Traditional but still effective
- **Cloud storage**: Dropbox, Google Drive shared links

### 2. **Auto-Execution Techniques**

#### A. Windows Startup Registry (Persistence)
```
Location: HKEY_CURRENT_USER\Software\Microsoft\Windows\CurrentVersion\Run
Effect: Runs every time user logs in
Detection: Moderate (most AV software checks this)
```

**Code Example:**
```python
import winreg
key = winreg.OpenKey(winreg.HKEY_CURRENT_USER, 
                     r"Software\Microsoft\Windows\CurrentVersion\Run", 
                     0, winreg.KEY_SET_VALUE)
winreg.SetValueEx(key, "SystemUpdate", 0, winreg.REG_SZ, "C:\\path\\to\\malware.exe")
```

#### B. Startup Folder
```
Location: C:\Users\[Username]\AppData\Roaming\Microsoft\Windows\Start Menu\Programs\Startup
Effect: Executes on user login
Detection: Easy (visible in folder)
```

#### C. Scheduled Tasks
```powershell
schtasks /create /tn "SystemUpdate" /tr "C:\path\to\malware.exe" /sc onlogon
```

#### D. Browser Auto-Downloads
- Exploiting browser settings to auto-execute downloads
- Requires user to have disabled safety features

### 3. **Stealth Techniques**

#### A. No Console Window
```python
# Built with PyInstaller --noconsole flag
# Or programmatically:
import ctypes
ctypes.windll.user32.ShowWindow(ctypes.windll.kernel32.GetConsoleWindow(), 0)
```

#### B. Legitimate-Looking Names
- `system32.exe` (mimics system folder)
- `svchost.exe` (mimics Windows service)
- `update.exe` (looks like an update)

#### C. File Placement
- Placed in `%TEMP%` or `%APPDATA%` folders
- Hidden attributes: `attrib +h +s file.exe`

#### D. Code Obfuscation
- Encrypted strings
- Base64 encoding
- Dynamic imports

---

## Attack Workflow

### Phase 1: Creation
```
1. Write malicious Python script
2. Convert to .exe with PyInstaller (--noconsole --onefile)
3. Add legitimate-looking icon
4. Rename to something innocuous
```

### Phase 2: Delivery
```
1. Upload to file-sharing platform (Telegram, Discord)
2. Create convincing message:
   "Hey, check out this report I made!"
   "Your tax refund is ready - download here"
3. Send to victim
```

### Phase 3: Execution
```
1. Victim downloads file
2. Windows Defender/AV scans (may be bypassed if unknown signature)
3. User double-clicks (or auto-executes via browser setting)
4. Malware runs silently in background
```

### Phase 4: Persistence
```
1. Add to registry startup keys
2. Create scheduled tasks
3. Copy to multiple locations
4. Disable security software (if privileged)
```

### Phase 5: Payload
```
1. Keylogging
2. Screenshot capture
3. File exfiltration
4. Ransomware encryption
5. Botnet recruitment
6. Cryptocurrency mining
```

---

## Technical Implementation

### Building the Malware

**autoRun.py features:**
- ✅ Console hiding
- ✅ Registry persistence
- ✅ Silent execution
- ✅ System information logging

**Building to .exe:**
```batch
pyinstaller --onefile --noconsole --name "Document" autoRun.py
```

**Advanced options:**
```batch
pyinstaller --onefile ^
    --noconsole ^
    --icon=document.ico ^
    --name "TaxReport2024" ^
    --add-data "fake.pdf;." ^
    autoRun.py
```

### Why It Works

1. **User Trust**: Comes from "friend" via Telegram
2. **No Visible Signs**: No console window, no error messages
3. **Persistence**: Survives reboots
4. **Stealth**: Uses legitimate Windows APIs
5. **Low Signature**: Custom malware has no known signature

---

## Detection Methods

### 1. **Behavioral Analysis**
- Monitor new executables in Downloads/Temp
- Track registry modifications
- Watch for network connections

### 2. **Static Analysis**
- Hash-based detection (SHA256)
- String analysis in binary
- Import table examination

### 3. **Heuristic Analysis**
- Checks for suspicious behavior patterns
- Entropy analysis (packed/encrypted code)
- API call monitoring

### 4. **Endpoint Detection & Response (EDR)**
- Real-time monitoring
- Process tree analysis
- Memory scanning

---

## Defense Strategies

### For Users
1. **Don't trust unsolicited files** - Even from friends (their account may be compromised)
2. **Check file extensions** - Look for double extensions (.pdf.exe)
3. **Use antivirus** - Keep Windows Defender or other AV active
4. **Enable SmartScreen** - Windows SmartScreen Filter
5. **Verify before executing** - Right-click → Properties to check file details

### For System Administrators
1. **Application Whitelisting** - Only approved apps can run
2. **Disable AutoRun** - Prevent auto-execution of media
3. **Monitor Registry Keys** - Alert on modifications to Run keys
4. **Network Segmentation** - Limit lateral movement
5. **Regular Audits** - Review startup items and scheduled tasks

### For Organizations
1. **Email Filtering** - Block executable attachments
2. **Web Proxies** - Filter downloads
3. **EDR Solutions** - Deploy endpoint protection
4. **User Training** - Security awareness programs
5. **Incident Response Plan** - Prepare for breaches

---

## Testing Your Implementation

### Step 1: Prepare Test Environment
```
1. Use a virtual machine (VMware, VirtualBox)
2. Take a snapshot before testing
3. Disable network (if testing real malware)
4. Never test on production systems
```

### Step 2: Build the Executable
```batch
cd w3-tp3
build_malware.bat
```

### Step 3: Run Detector (on test machine)
```python
python enhanced_detector.py
```

### Step 4: Simulate Attack
```
1. Transfer autoRun.exe to test machine via USB or network share
2. Place in Downloads folder
3. Observe detector's response
4. Check security_log.txt for events
5. Verify quarantine folder
```

### Step 5: Verify Persistence
```
1. Check registry: regedit → HKCU\Software\Microsoft\Windows\CurrentVersion\Run
2. Look for "SystemUpdate" entry
3. Check %TEMP% folder for system_log.txt
```

### Step 6: Clean Up
```
1. Remove registry entry
2. Delete autoRun.exe and quarantine files
3. Delete system_log.txt from %TEMP%
4. Revert VM to clean snapshot
```

---

## Real-World Examples

### 1. **Emotet Banking Trojan**
- Spread via phishing emails
- Microsoft Word macros download payload
- Uses multiple persistence mechanisms
- Steals banking credentials

### 2. **WannaCry Ransomware**
- Exploited Windows SMB vulnerability
- Auto-spread through networks
- Encrypted files and demanded Bitcoin
- Affected 200,000+ computers worldwide

### 3. **Telegram Malware Campaigns**
- Attackers use Telegram bots to distribute malware
- Files shared in "cracked software" channels
- Auto-execution through fake installers
- Common in gaming and software piracy communities

---

## Legal and Ethical Considerations

### ⚠️ CRITICAL WARNING

**Creating and distributing malware is ILLEGAL in most jurisdictions:**

- **Computer Fraud and Abuse Act (USA)**: Up to 20 years in prison
- **UK Computer Misuse Act**: Up to 10 years in prison
- **EU Cybercrime Directive**: Varies by country

**Authorized Use Only:**
- ✅ Educational labs with permission
- ✅ Your own isolated systems
- ✅ Authorized penetration testing (with written consent)
- ✅ Security research in controlled environments

**NEVER:**
- ❌ Deploy on others' systems without permission
- ❌ Distribute to untrusted parties
- ❌ Use on corporate networks without authorization
- ❌ Share on public platforms

---

## Conclusion

This educational demonstration shows how attackers:
1. Create stealth executables
2. Deliver through social engineering
3. Achieve persistence on systems
4. Execute malicious payloads
5. Evade detection

**Key Takeaways:**
- Social engineering is the weakest link
- Persistence mechanisms are well-known but still effective
- Detection requires multi-layered approach
- User education is crucial defense

**Remember:** The goal is to understand these techniques to better defend against them, not to use them maliciously.

---

## Additional Resources

- [MITRE ATT&CK Framework](https://attack.mitre.org/)
- [VirusTotal](https://www.virustotal.com/) - Analyze suspicious files
- [Hybrid Analysis](https://www.hybrid-analysis.com/) - Malware sandbox
- [Windows Sysinternals](https://docs.microsoft.com/sysinternals/) - System analysis tools
- [OWASP Security Testing Guide](https://owasp.org/)

---

**Last Updated:** October 2024
**Author:** Cybersecurity Educational Project
**License:** Educational Use Only
