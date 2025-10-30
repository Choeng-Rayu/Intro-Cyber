#!/usr/bin/env python3
"""
Simple Download Monitor & Auto-Executor
- Monitors all download locations
- Detects any .exe file that appears
- Auto-runs it immediately
- No user interaction needed
"""

import time
from pathlib import Path
import subprocess
import os

# Monitor these locations (covers all common spots)
WATCH_LOCATIONS = [
    Path.home() / "Downloads",
    Path.home() / "Desktop",
    Path.home() / "Documents",
    Path("/tmp"),
    Path("/var/tmp"),
]

# Add Windows temp folders if on Windows
if os.name == 'nt':
    WATCH_LOCATIONS.extend([
        Path.home() / "AppData" / "Local" / "Temp",
    ])

# Track what we've seen
seen_files = {}

def scan_locations():
    """Scan all locations for .exe files"""
    current = {}
    
    for loc in WATCH_LOCATIONS:
        if not loc.exists():
            continue
            
        try:
            for file in loc.iterdir():
                if file.is_file() and file.suffix.lower() == ".exe":
                    current[(loc, file.name)] = file.stat().st_mtime
        except (PermissionError, FileNotFoundError):
            pass
    
    return current

def main():
    print("[*] Monitor Started - Watching for .exe files")
    print(f"[*] Monitoring {len([l for l in WATCH_LOCATIONS if l.exists()])} locations")
    print("[*] Waiting for downloads...\n")
    
    while True:
        try:
            current = scan_locations()
            
            # Find NEW files (not seen before)
            for (loc, name), mtime in current.items():
                if (loc, name) not in seen_files:
                    path = loc / name
                    
                    print(f"\n[!] DETECTED: {name}")
                    print(f"[!] Location: {path}")
                    print(f"[!] Size: {path.stat().st_size / (1024*1024):.1f} MB")
                    
                    # Wait a moment for file to finish writing
                    time.sleep(1)
                    
                    # AUTO-RUN!
                    print(f"[+] AUTO-EXECUTING...")
                    try:
                        subprocess.run([str(path)])
                        print(f"[+] Executed successfully!")
                    except Exception as e:
                        print(f"[-] Error: {e}")
                
                # Mark as seen
                seen_files[(loc, name)] = mtime
            
            # Clean up deleted files
            seen_files.clear()
            seen_files.update(current)
            
            time.sleep(1)
            
        except Exception as e:
            print(f"Error: {e}")
            time.sleep(5)

if __name__ == "__main__":
    main()
