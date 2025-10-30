# 📱 TELEGRAM SENDING - VISUAL GUIDE

## 🎯 EXACTLY WHAT TO SEND (Simple Version)

```
You:     "Hey, check this out!"
         [SEND FILE #1: simple_payload.exe]
         
Them:    "Cool, I downloaded it"

You:     "Now run this:"
         [SEND FILE #2: observe_universal.py]
         
Them:    "Done! It says [ALERT] Executable detected!"
         "And now 'Hello World!' popped up!"
         
You:     "Perfect! That's the auto-execution attack!"
```

---

## 📋 FILE CHECKLIST - COPY PATHS

### ✅ MUST SEND (Minimum)

**File #1 - The Executable (MAIN)**
```
Name: simple_payload.exe
Size: 7.2 MB
Path: /home/choeng-rayu/academic/Year3/Intro-Cyber/w3-tp3/dist/simple_payload.exe
Purpose: This is the attack payload
```

**File #2 - The Monitor (Recommended)**
```
Name: observe_universal.py
Size: ~5 KB
Path: /home/choeng-rayu/academic/Year3/Intro-Cyber/w3-tp3/observe_universal.py
Purpose: Detects and auto-executes the .exe
```

### 📚 OPTIONAL BUT GOOD (Documentation)

**File #3 - Setup Guide**
```
Name: README_COMPLETE_SETUP.md
Path: /home/choeng-rayu/academic/Year3/Intro-Cyber/w3-tp3/README_COMPLETE_SETUP.md
Purpose: Explains everything
```

**File #4 - Source Code**
```
Name: simple_payload.py
Path: /home/choeng-rayu/academic/Year3/Intro-Cyber/w3-tp3/simple_payload.py
Purpose: Shows what the .exe does (harmless code)
```

---

## 🔢 SENDING ORDER SUMMARY

| Step | Send This | Size | Say This |
|------|-----------|------|----------|
| 1 | `simple_payload.exe` | 7.2 MB | "Check this out!" |
| 2 | `observe_universal.py` | 5 KB | "Run this on Windows" |
| 3 | `README_COMPLETE_SETUP.md` | 8 KB | "Here's how it works" |
| 4 | Your report | - | "Here's my analysis" |

---

## 🎬 What Happens Next

```
TIMELINE:

They download simple_payload.exe (7.2 MB)
         ↓ (1 minute later)
They run observe_universal.py
         ↓ (1 second later)
Monitor detects .exe automatically
         ↓ (instant)
"Hello World!" popup appears
         ↓ (2 seconds)
They send you screenshots
         ↓ (proof!)
You include in your assignment
         ↓
✅ ASSIGNMENT COMPLETE!
```

---

## 💬 MESSAGE EXAMPLES

### Message 1: Offer to Test
```
"Hi! I'm doing a cybersecurity assignment 
about malware auto-execution.
Can I test an educational demo on your Windows machine?
It's 100% safe - just prints 'Hello World'.
For my school project."
```

### Message 2: Send File 1
```
"Here's the executable:
[ATTACH: simple_payload.exe]

Just save it to your Downloads folder when you download it."
```

### Message 3: Send File 2
```
"Now run this Python script on your Windows machine:
[ATTACH: observe_universal.py]

Command: python observe_universal.py

It will watch for the .exe and auto-execute it."
```

### Message 4: Explain
```
"When you run that script, it will:
1. Watch your Downloads folder
2. See when you downloaded the .exe
3. Automatically run it
4. You'll see 'Hello World!' popup

This is how the vulnerability works!
Can you send me a screenshot of what happened?"
```

---

## ✅ SUCCESS INDICATORS

When they do it correctly, they should see:

```
[*] Universal Download Monitor Started
[*] Watching 7 locations
[*] Waiting for file downloads...
...
[ALERT] Executable detected: simple_payload.exe (7.2M)
[*] Auto-executing: C:\Users\...\Downloads\simple_payload.exe

==================================================
Hello World!
==================================================
[*] This executable was auto-executed!
[*] Educational demonstration for cybersecurity
[*] Timestamp: 2025-10-30 21:57:00
```

✅ If they see this → **ATTACK SUCCESSFUL!**

---

## 🚨 If Windows Defender Blocks It

That's NORMAL! It means security is working.

Tell them:
```
"Don't worry - Windows Defender blocked it.
That's the POINT of this demonstration!
The vulnerability exists, but defenses caught it.
For the assignment, I'll add an exception temporarily."
```

Then either:
- Run on a system without antivirus (lab only)
- Add temporary exception to Windows Defender
- Run in Windows Sandbox

---

## 📊 File Sizes for Reference

```
simple_payload.exe         7.2 MB  ← Main file (largest)
README_COMPLETE_SETUP.md   ~8 KB
ATTACK_ANALYSIS.md         ~5 KB
observe_universal.py       ~5 KB
simple_payload.py          ~600 B  ← Source code (smallest)
TELEGRAM_SENDING_GUIDE.md  ~9 KB
PAYLOAD_DELIVERY_GUIDE.md  ~10 KB
```

---

## 🎯 SUPER QUICK VERSION (TL;DR)

**Send 3 files:**
1. `simple_payload.exe` (7.2 MB) - "Check this out!"
2. `observe_universal.py` (5 KB) - "Run this"
3. `README_COMPLETE_SETUP.md` (8 KB) - "Here's how"

**They do:**
- Download .exe to Downloads
- Run python script
- See "Hello World!" popup
- Auto-execution = WORKS! ✅

**You document:**
- Screenshots
- Logs
- Add to assignment
- **DONE!** 🎉

---

## ⚖️ LEGAL CHECKLIST (MUST DO)

Before sending, verify:

- [ ] They agreed to participate
- [ ] They know it's for a school assignment
- [ ] They understand what will happen
- [ ] They own the test machine
- [ ] They're in an isolated environment
- [ ] They know it's EDUCATIONAL ONLY
- [ ] You have their consent documented

---

## 🔐 Safety Reminders

```
✓ GOOD: Testing with explicit permission
✓ GOOD: Using isolated machines
✓ GOOD: Documenting for educational purposes
✓ GOOD: Including defensive mechanisms

✗ BAD: Sending to random people
✗ BAD: Pretending it's something else
✗ BAD: Using without permission
✗ BAD: Ignoring security warnings
```

---

## 📞 Quick Command for Recipient

Tell them to run this on Windows:

```bash
python observe_universal.py
```

That's it! They'll see the monitor in action.

---

## 📸 SCREENSHOTS TO COLLECT

Ask recipient to send you:

1. Screenshot of monitor detecting .exe
2. Screenshot of "Hello World!" popup
3. Screenshot of log file (download_activity.log)
4. Any console output

These become EVIDENCE for your assignment!

---

## 🎓 FINAL CHECKLIST

Before you send:
- [ ] Have permission from recipient
- [ ] Files are ready (simple_payload.exe exists)
- [ ] Know recipient has Windows machine
- [ ] Have Python installed on their machine
- [ ] Understand attack flow
- [ ] Know how to document results

After they test:
- [ ] Get screenshots from them
- [ ] Collect log files
- [ ] Document timing
- [ ] Include in your assignment report

---

## 🎉 YOU'RE READY!

Your files are all set. Just send them in order:

1. **simple_payload.exe** (7.2 MB)
2. **observe_universal.py** (5 KB)
3. **Documentation** (optional)

Then collect the results and write your report!

Good luck! 🚀

---

**Created:** October 30, 2025  
**For:** Intro to Cybersecurity - W3-TP3  
**Status:** READY TO USE
