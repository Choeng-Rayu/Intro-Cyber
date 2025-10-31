import time
from pathlib import Path
import subprocess

# Windows Downloads folder: C:\Users\YourUsername\Downloads
# You can also use: AppData/Local/Temp, Desktop, Documents
WATCH_DIR = Path.home() / "Downloads"

seen = set(p.name for p in WATCH_DIR.iterdir())

while True:
    current = set(p.name for p in WATCH_DIR.iterdir())
    new_files = current - seen
    for name in new_files:
        path = WATCH_DIR / name
        if name.lower() == "autorun.exe": # for running specific script name
            # Wait briefly to allow file to finish writing
            time.sleep(1)
            subprocess.run([str(path)])
        seen.add(name)
    seen &= current
    time.sleep(1)
