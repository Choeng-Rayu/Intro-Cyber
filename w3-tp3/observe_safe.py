import time
from pathlib import Path
import subprocess
import logging
from datetime import datetime

# Setup logging for educational audit trail
logging.basicConfig(
    filename='activity_log.txt',
    level=logging.INFO,
    format='%(asctime)s - %(message)s'
)

# Set to Downloads folder
WATCH_DIR = Path.home() / "Downloads"

seen = set(p.name for p in WATCH_DIR.iterdir())
logging.info(f"Started monitoring: {WATCH_DIR}")

while True:
    try:
        current = set(p.name for p in WATCH_DIR.iterdir())
        new_files = current - seen
        
        for name in new_files:
            path = WATCH_DIR / name
            if path.suffix.lower() == ".exe":
                logging.warning(f"DETECTED .exe file: {name} at {path}")
                
                # EDUCATIONAL SAFETY: Log instead of execute
                logging.info(f"Would execute: {path}")
                print(f"[DEMO MODE] Detected executable: {name}")
                
                # UNCOMMENT ONLY IN ISOLATED TEST ENVIRONMENT:
                # time.sleep(1)
                # subprocess.run([str(path)])
                
            seen.add(name)
        
        seen &= current
        time.sleep(1)
        
    except Exception as e:
        logging.error(f"Error: {e}")
        time.sleep(5)
