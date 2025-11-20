# 🔧 Convert to EXE and Run as Background Service

## Features in Updated Code

✅ **Platform Detection** - Handles Windows and Linux paths automatically  
✅ **Safety Features** - Asks for confirmation before deleting  
✅ **Logging** - Saves all deletion records to a file  
✅ **Scheduling** - Can run at specific times (HH:MM format)  
✅ **Configuration** - Saves settings to JSON file  

---

## Part 1: Convert Python to .EXE

### Step 1: Install PyInstaller
Open Command Prompt as Administrator and run:

```bash
pip install pyinstaller
```

### Step 2: Create the EXE File
Navigate to the folder with `deleteFolderWindown_Dynamic.py` and run:

```bash
pyinstaller --onefile --windowed --icon=icon.ico deleteFolderWindown_Dynamic.py
```

**Options explained:**
- `--onefile` - Creates a single .exe file instead of multiple files
- `--windowed` - Runs without console window (optional)
- `--icon=icon.ico` - Adds an icon (optional, remove if no icon file)

### Step 3: Find Your EXE
The .exe file will be in the `dist` folder:
```
dist/deleteFolderWindown_Dynamic.exe
```

---

## Part 2: Run as Background Service

### Option A: Windows Task Scheduler (Easiest)

1. **Open Task Scheduler**
   - Press `Win + R`
   - Type `taskschd.msc` and press Enter

2. **Create New Task**
   - Click "Create Task" on the right panel
   - Name: `SmartCleaner`
   - Check: "Run with highest privileges"

3. **Set Trigger (When to Run)**
   - Go to "Triggers" tab
   - Click "New"
   - Choose "At startup" or "On a schedule"

4. **Set Action (What to Run)**
   - Go to "Actions" tab
   - Click "New"
   - Program: `C:\path\to\dist\deleteFolderWindown_Dynamic.exe`
   - Arguments: `D:\ 5` (folder and interval)

5. **Click OK and Save**

---

### Option B: Windows Service (Advanced)

Create a batch file `install_service.bat`:

```batch
@echo off
REM Run as Administrator to install
nssm install SmartCleaner "C:\path\to\dist\deleteFolderWindown_Dynamic.exe" "D:\ 5"
nssm start SmartCleaner
```

**Prerequisites:**
- Download NSSM (Non-Sucking Service Manager) from: https://nssm.cc/download
- Extract and add to System PATH

**Then run:**
```bash
install_service.bat
```

---

### Option C: Linux/Ubuntu Service

Create file: `/etc/systemd/system/smart-cleaner.service`

```ini
[Unit]
Description=Smart Cleaner - Auto Deletion Service
After=network.target

[Service]
Type=simple
User=root
ExecStart=/usr/bin/python3 /path/to/deleteFolderWindown_Dynamic.py /home/user/test 5
Restart=always
RestartSec=10

[Install]
WantedBy=multi-user.target
```

Then enable and start:
```bash
sudo systemctl daemon-reload
sudo systemctl enable smart-cleaner
sudo systemctl start smart-cleaner
sudo systemctl status smart-cleaner
```

---

## Part 3: Check Logs

### Windows
Log files are saved to:
```
C:\Users\YourUsername\AppData\Roaming\SmartCleaner\deletion_log.txt
```

### Linux
Log files are saved to:
```
~/.smart-cleaner/deletion_log.txt
```

View logs:
```bash
cat ~/.smart-cleaner/deletion_log.txt
```

---

## Usage Examples

### Interactive Mode (Prompts for Input)
```bash
deleteFolderWindown_Dynamic.exe
```

### Command Line Mode (Automatic)
```bash
# Delete from D: with 5-second interval
deleteFolderWindown_Dynamic.exe D:\ 5

# Delete from D: at specific time
deleteFolderWindown_Dynamic.exe D:\ 5 14:30
```

---

## Configuration File

After first run, settings are saved to:

**Windows:** `C:\Users\YourUsername\AppData\Roaming\SmartCleaner\config.json`

**Linux:** `~/.smart-cleaner/config.json`

Example:
```json
{
    "folder_path": "D:\\",
    "interval": 5,
    "schedule_time": "14:30",
    "created": "2025-10-30T15:45:32.123456",
    "system": "Windows"
}
```

---

## Troubleshooting

**Problem:** Permission Denied  
**Solution:** Run as Administrator (Windows) or with `sudo` (Linux)

**Problem:** Service not starting  
**Solution:** Check logs in the SmartCleaner folder

**Problem:** EXE file not working  
**Solution:** Make sure all dependencies are installed:
```bash
pip install pyinstaller
python deleteFolderWindown_Dynamic.py
```

---

## Security Notes ⚠️

⚠️ **WARNING:** This program will **PERMANENTLY DELETE** files!
- Always test on a non-critical folder first
- Keep backups before using in production
- This is for educational/security testing purposes only
- Unauthorized deletion of others' files is illegal

