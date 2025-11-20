# 📦 Smart Cleaner .deb Installation Guide

## For Your Ubuntu/Linux Friend

### Installation (Super Easy!)

#### **Method 1: Double-Click (Recommended) ⭐**
1. Download: `smart-cleaner-1.0.deb`
2. Double-click the file
3. Click "Install" button
4. Enter password when prompted
5. Done! ✅ Service starts automatically

#### **Method 2: Command Line**
```bash
sudo apt install ./smart-cleaner-1.0.deb
```

#### **Method 3: GDebi (GUI Package Manager)**
```bash
sudo apt install gdebi
sudo gdebi smart-cleaner-1.0.deb
```

---

## ⚙️ IMPORTANT: Configure Your Folder Path

After installation, you **MUST** set your folder path:

```bash
sudo nano /etc/smart-cleaner/smart-cleaner.conf
```

Edit the `FOLDER_TO_CLEAN` line to your folder:

```ini
FOLDER_TO_CLEAN=/path/to/your/folder
INTERVAL_SECONDS=30
```

Example:
```ini
FOLDER_TO_CLEAN=/home/yourname/Downloads
INTERVAL_SECONDS=30
```

Then restart the service:
```bash
sudo systemctl restart smart-cleaner
```

---

## After Installation

The service will:
✅ Start automatically immediately
✅ Run in background forever
✅ Auto-restart on computer boot
✅ Auto-restart if it crashes

---

## Management Commands

**Check if running:**
```bash
sudo systemctl status smart-cleaner
```

**View live logs:**
```bash
sudo journalctl -u smart-cleaner -f
```

**Stop service:**
```bash
sudo systemctl stop smart-cleaner
```

**Restart service:**
```bash
sudo systemctl restart smart-cleaner
```

**Uninstall completely:**
```bash
sudo apt remove smart-cleaner
```

---

## What Gets Installed

- Python script: `/usr/local/bin/smart-cleaner`
- Config file: `/etc/smart-cleaner/smart-cleaner.conf`
- Service file: `/etc/systemd/system/smart-cleaner.service`
- Logs: Check with `journalctl` command

---

## Troubleshooting

**Service not running?**
```bash
sudo systemctl status smart-cleaner
sudo journalctl -u smart-cleaner -n 50
```

**Config file not found?**
```bash
sudo nano /etc/smart-cleaner/smart-cleaner.conf
```

**Need to change folder path?**
1. Edit the config file: `sudo nano /etc/smart-cleaner/smart-cleaner.conf`
2. Change the `FOLDER_TO_CLEAN` path
3. Restart: `sudo systemctl restart smart-cleaner`

---

That's it! Easy installation! 🎉
