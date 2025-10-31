# Simple Malware Detector - FOR EDUCATION ONLY
import time
from pathlib import Path
from datetime import datetime

WATCH_DIR = Path.home() / "Downloads"
LOG_FILE = Path(__file__).parent / "security_log.txt"

def log(message):
    """Log events"""
    timestamp = datetime.now().strftime("%H:%M:%S")
    entry = f"[{timestamp}] {message}"
    print(entry)
    with open(LOG_FILE, 'a') as f:
        f.write(entry + "\n")

def quarantine(filepath):
    """Move suspicious file to quarantine folder"""
    try:
        quarantine_dir = Path(__file__).parent / "quarantine"
        quarantine_dir.mkdir(exist_ok=True)
        new_path = quarantine_dir / filepath.name
        filepath.rename(new_path)
        log(f"⚠️ QUARANTINED: {filepath.name}")
        return True
    except:
        return False

# Track seen files
seen = set(p.name for p in WATCH_DIR.iterdir() if p.is_file())

print("=" * 50)
print("Simple Malware Detector Running")
print(f"Watching: {WATCH_DIR}")
print("=" * 50)
log("Detector started")

while True:
    try:
        current = set(p.name for p in WATCH_DIR.iterdir() if p.is_file())
        new_files = current - seen
        
        for name in new_files:
            filepath = WATCH_DIR / name
            
            # Detect suspicious .exe files
            if name.lower().endswith('.exe'):
                log(f"🔍 NEW EXE DETECTED: {name}")
                time.sleep(1)  # Wait for file to finish writing
                
                # Check if it's suspicious
                if any(word in name.lower() for word in ['autorun', 'system', 'update']):
                    log(f"🚨 SUSPICIOUS FILE: {name}")
                    quarantine(filepath)
                else:
                    log(f"✓ File allowed: {name}")
            
            seen.add(name)
        
        seen = current
        time.sleep(2)
        
    except KeyboardInterrupt:
        log("Detector stopped by user")
        break
    except Exception as e:
        log(f"Error: {e}")
        time.sleep(2)
