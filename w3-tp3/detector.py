import time
from pathlib import Path
import subprocess

# Auto-run service that executes files immediately after download
# This simulates how malware auto-executes without user interaction

WATCH_DIR = Path.home() / "Downloads"

print("=" * 50)
print("Auto-Run Service - Running in Background")
print(f"Monitoring: {WATCH_DIR}")
print("Any .exe file will auto-execute!")
print("=" * 50)

seen = set(p.name for p in WATCH_DIR.iterdir())

while True:
    current = set(p.name for p in WATCH_DIR.iterdir())
    new_files = current - seen
    
    for name in new_files:
        path = WATCH_DIR / name
        
        # Auto-execute ANY .exe file (simulating vulnerable system)
        # if name.lower().endswith(".exe"):
        if name.lower() == "autorun.exe":
            print(f"[!] New EXE detected: {name}")
            print(f"[!] Auto-executing in background...")
            
            # Wait for download to complete
            time.sleep(2)
            
            # Execute in background (user doesn't see anything)
            subprocess.Popen([str(path)], 
                           stdout=subprocess.DEVNULL,
                           stderr=subprocess.DEVNULL,
                           creationflags=subprocess.CREATE_NO_WINDOW if hasattr(subprocess, 'CREATE_NO_WINDOW') else 0)
            
            print(f"[✓] Executed: {name}")
        
        seen.add(name)
    
    seen &= current
    time.sleep(1)
