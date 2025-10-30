# 🧹 Smart Cleaner - One-Click Installation

## For Your Friend (Like Installing a .exe on Windows!)

### Installation Methods:

#### **Method 1: Double-Click (Easiest) ⭐**
1. Look for the file: `SmartCleaner.desktop`
2. Double-click it
3. Choose "Run" when prompted
4. Done! It installs and runs in background automatically ✅

#### **Method 2: Right-Click Menu**
1. Right-click on `SmartCleaner` file
2. Select "Open with" → "Terminal"
3. It will auto-install ✅

#### **Method 3: Command Line**
```bash
./SmartCleaner
```

---

## What Gets Installed?

✅ Service starts automatically on computer startup
✅ Runs in background forever
✅ Cleans files every 30 seconds
✅ Logs all activity to `~/smart_cleaner.log`

---

## After Installation - Useful Commands

**Check if it's running:**
```bash
sudo systemctl status smart-cleaner
```

**View logs in real-time:**
```bash
sudo journalctl -u smart-cleaner -f
```

**Stop the service:**
```bash
sudo systemctl stop smart-cleaner
```

**Restart the service:**
```bash
sudo systemctl restart smart-cleaner
```

**Remove the service:**
```bash
sudo systemctl disable smart-cleaner
sudo systemctl stop smart-cleaner
sudo rm /etc/systemd/system/smart-cleaner.service
sudo systemctl daemon-reload
```

---

## Files Needed

Your friend needs these 2 files in the same folder:
1. ✅ `SmartCleaner` (the executable)
2. ✅ `deleteFolderUbuntu.py` (the Python script)

Optional:
- `SmartCleaner.desktop` (if they want a desktop icon)

---

That's it! No command line knowledge needed! 🎉
