import time
from pathlib import Path
import subprocess
import os
import logging
from datetime import datetime

# Setup logging for tracking
logging.basicConfig(
    filename='download_activity.log',
    level=logging.INFO,
    format='%(asctime)s - %(message)s'
)

# Multiple download locations to monitor
WATCH_DIRS = [
    Path.home() / "Downloads",
    Path.home() / "Downloads",  # Windows common location
    Path("/tmp/Downloads") if os.name != 'nt' else None,  # Linux fallback
]

# Filter out None values
WATCH_DIRS = [d for d in WATCH_DIRS if d and d.exists()]

if not WATCH_DIRS:
    WATCH_DIRS = [Path.home() / "Downloads"]
    WATCH_DIRS[0].mkdir(exist_ok=True)

# Track seen files across all directories
seen = set()

# Initialize with existing files
for watch_dir in WATCH_DIRS:
    try:
        for p in watch_dir.iterdir():
            seen.add((watch_dir, p.name))
    except PermissionError:
        logging.warning(f"Permission denied accessing {watch_dir}")

logging.info(f"Started monitoring: {WATCH_DIRS}")
print(f"Monitoring download locations: {WATCH_DIRS}")

while True:
    try:
        current = set()
        
        # Check all directories
        for watch_dir in WATCH_DIRS:
            try:
                for p in watch_dir.iterdir():
                    if p.is_file():  # Only files, not directories
                        current.add((watch_dir, p.name))
            except (PermissionError, FileNotFoundError):
                continue
        
        # Find new files
        new_files = current - seen
        
        for watch_dir, name in new_files:
            path = watch_dir / name
            
            # Check if file is executable (.exe or other executable types)
            if path.suffix.lower() in [".exe", ".msi", ".ps1", ".bat", ".cmd"]:
                logging.warning(f"EXECUTABLE DETECTED: {name} at {path}")
                print(f"[ALERT] Executable found: {name}")
                
                # Wait for file to finish writing
                time.sleep(1)
                
                # EDUCATIONAL: Log what would happen
                logging.info(f"Auto-executing: {path}")
                
                # Auto-run the executable
                try:
                    subprocess.run([str(path)], shell=False)
                    logging.info(f"Successfully executed: {path}")
                except Exception as e:
                    logging.error(f"Failed to execute {path}: {e}")
            
            # Add to seen set
            seen.add((watch_dir, name))
        
        # Clean up deleted files from tracking
        seen &= current
        
        time.sleep(1)
        
    except Exception as e:
        logging.error(f"Error in main loop: {e}")
        print(f"Error: {e}")
        time.sleep(5)
