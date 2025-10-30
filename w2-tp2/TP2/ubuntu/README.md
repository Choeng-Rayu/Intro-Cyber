# 🧹 Smart Cleaner - Automatic Background File Cleanup Service

A powerful, easy-to-use Ubuntu/Linux service that automatically cleans up files and folders from any directory and moves them to a quarantine folder for safety.

---

## 📋 Table of Contents

- [Features](#features)
- [Installation](#installation)
- [Quick Start](#quick-start)
- [Configuration](#configuration)
- [Usage](#usage)
- [Management](#management)
- [Troubleshooting](#troubleshooting)
- [Uninstallation](#uninstallation)

---

## ✨ Features

✅ **One-Click Installation** - Just like a .exe file on Windows
✅ **Background Service** - Runs automatically in the background
✅ **Auto-Restart** - Automatically restarts on system boot
✅ **Safe Deletion** - Moves files to quarantine instead of permanent deletion
✅ **Configurable** - Easy to change folder path and cleanup interval
✅ **Logging** - Keeps detailed logs of all operations
✅ **Recursive Cleanup** - Cleans files in subdirectories too
✅ **Empty Folder Removal** - Automatically removes empty folders

---

## 📦 Installation

### Option 1: Double-Click Installation (Easiest) ⭐

1. Download the file: **`smart-cleaner-1.0.deb`**
2. Double-click it in your file manager
3. Click the **"Install"** button
4. Enter your password when prompted
5. Done! ✅

### Option 2: Command Line Installation

```bash
sudo apt install ./smart-cleaner-1.0.deb
```

### Option 3: Using GDebi Package Manager

```bash
sudo apt install gdebi
sudo gdebi smart-cleaner-1.0.deb
```

---

## 🚀 Quick Start

### After Installation

The service automatically starts and runs in the background. But first, **you MUST configure it**:

#### 1. Edit Configuration File
```bash
sudo nano /etc/smart-cleaner/smart-cleaner.conf
```

#### 2. Set Your Target Folder
Find this line and change it to your folder:
```ini
FOLDER_TO_CLEAN=/home/choeng-rayu/academic/Year3/Intro-Cyber/w3/testDelete
```

Example configurations:
```ini
# Clean Downloads folder
FOLDER_TO_CLEAN=/home/yourname/Downloads

# Clean Desktop
FOLDER_TO_CLEAN=/home/yourname/Desktop

# Clean a custom folder
FOLDER_TO_CLEAN=/home/yourname/MyFolder/ToClean
```

#### 3. Save and Exit
Press `Ctrl+X`, then `Y`, then `Enter`

#### 4. Restart the Service
```bash
sudo systemctl restart smart-cleaner
```

#### 5. Verify It's Running
```bash
sudo systemctl status smart-cleaner
```

You should see: **`● smart-cleaner.service - ... running`** ✅

---

## ⚙️ Configuration

### Configuration File Location
```
/etc/smart-cleaner/smart-cleaner.conf
```

### Configuration Options

```ini
# Target folder to clean (use full path)
FOLDER_TO_CLEAN=/path/to/your/folder

# Interval between cleanups in seconds
# Default: 30 (cleans every 30 seconds)
INTERVAL_SECONDS=30
```

### Examples

**Clean Downloads every minute:**
```ini
FOLDER_TO_CLEAN=/home/user/Downloads
INTERVAL_SECONDS=60
```

**Clean Desktop every 5 seconds:**
```ini
FOLDER_TO_CLEAN=/home/user/Desktop
INTERVAL_SECONDS=5
```

**Clean large folder every 2 minutes:**
```ini
FOLDER_TO_CLEAN=/media/external-drive/old-files
INTERVAL_SECONDS=120
```

---

## 📖 Usage

### Check Service Status

See if the service is running:
```bash
sudo systemctl status smart-cleaner
```

Output should show:
```
● smart-cleaner.service - Smart Cleaner Service - Background folder cleanup
   Loaded: loaded (/etc/systemd/system/smart-cleaner.service; enabled; vendor preset: enabled)
   Active: active (running) since ...
```

### View Live Logs

See what the service is doing in real-time:
```bash
sudo journalctl -u smart-cleaner -f
```

Press `Ctrl+C` to stop viewing logs.

### View Last 50 Log Entries

```bash
sudo journalctl -u smart-cleaner -n 50
```

### View Logs Since Last Boot

```bash
sudo journalctl -u smart-cleaner -b
```

---

## 🛠️ Management Commands

### Start the Service

```bash
sudo systemctl start smart-cleaner
```

### Stop the Service

```bash
sudo systemctl stop smart-cleaner
```

### Restart the Service

After changing the configuration file:
```bash
sudo systemctl restart smart-cleaner
```

### Enable Auto-Start on Boot

```bash
sudo systemctl enable smart-cleaner
```

### Disable Auto-Start on Boot

```bash
sudo systemctl disable smart-cleaner
```

### Check if Service Runs on Boot

```bash
sudo systemctl is-enabled smart-cleaner
```

---

## 📁 What Gets Installed

| File | Location |
|------|----------|
| Python Script | `/usr/local/bin/smart-cleaner` |
| Config File | `/etc/smart-cleaner/smart-cleaner.conf` |
| Service File | `/etc/systemd/system/smart-cleaner.service` |
| Logs | View with `journalctl` |
| Quarantine Folder | `~/quarantine_YYYYMMDD_HHMMSS` |

---

## 🔍 Troubleshooting

### Service Not Running

**Check status:**
```bash
sudo systemctl status smart-cleaner
```

**View recent errors:**
```bash
sudo journalctl -u smart-cleaner -n 20
```

**Restart the service:**
```bash
sudo systemctl restart smart-cleaner
```

### Config File Not Found

Create it:
```bash
sudo mkdir -p /etc/smart-cleaner
sudo nano /etc/smart-cleaner/smart-cleaner.conf
```

Add this content:
```ini
FOLDER_TO_CLEAN=/home/yourname/Downloads
INTERVAL_SECONDS=30
```

### Folder Path Not Valid

Error message: `❌ Invalid folder path.`

**Solution:**
1. Make sure the folder exists: `ls -la /your/folder/path`
2. Make sure you have read/write permissions
3. Use full absolute path (not relative paths like `~/Downloads`)

### Permission Denied

Error: `Permission denied`

**Solution:**
```bash
sudo chown -R $USER:$USER /path/to/your/folder
sudo chmod -R u+rwx /path/to/your/folder
```

### Service Crashes Frequently

**Check logs:**
```bash
sudo journalctl -u smart-cleaner -n 100 | grep ERROR
```

**Common causes:**
- Folder doesn't exist
- Folder path is wrong
- Permission issues
- Disk space full

---

## 🗑️ Uninstallation

### Remove Completely

```bash
# Stop the service
sudo systemctl stop smart-cleaner

# Disable auto-start
sudo systemctl disable smart-cleaner

# Uninstall the package
sudo apt remove smart-cleaner

# (Optional) Remove config files
sudo rm -rf /etc/smart-cleaner
```

---

## 📊 Example Workflow

### Step 1: Install
```bash
sudo apt install ./smart-cleaner-1.0.deb
```

### Step 2: Configure
```bash
sudo nano /etc/smart-cleaner/smart-cleaner.conf
# Edit FOLDER_TO_CLEAN to your desired path
# Save and exit
```

### Step 3: Restart Service
```bash
sudo systemctl restart smart-cleaner
```

### Step 4: Verify
```bash
sudo systemctl status smart-cleaner
```

### Step 5: View Live Logs
```bash
sudo journalctl -u smart-cleaner -f
```

---

## ⚠️ Important Notes

1. **Backup Important Files** - Make sure important files are not in the cleanup folder
2. **Quarantine Folder** - Files are moved to `~/quarantine_YYYYMMDD_HHMMSS`, not deleted permanently
3. **Permissions** - You need `sudo` to manage the service
4. **Absolute Paths** - Always use full paths in config (e.g., `/home/user/folder`, not `~/folder`)
5. **Test First** - Test with a non-critical folder before using on important data

---

## 📞 Support

If you encounter issues:

1. Check the logs: `sudo journalctl -u smart-cleaner -n 50`
2. Verify config file: `sudo cat /etc/smart-cleaner/smart-cleaner.conf`
3. Test folder access: `ls -la /your/folder/path`
4. Restart service: `sudo systemctl restart smart-cleaner`

---

## 📝 License

Created for educational purposes.

---

## 🎯 Version

**Smart Cleaner v1.0**

Release Date: October 30, 2025

---

## 🙏 Thank You

Enjoy automatic cleanup! 🚀
