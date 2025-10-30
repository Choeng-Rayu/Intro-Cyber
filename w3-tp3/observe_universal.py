import time
from pathlib import Path
import subprocess
import os
import logging
import shutil
from datetime import datetime

# Setup logging
logging.basicConfig(
    filename='universal_download_monitor.log',
    level=logging.INFO,
    format='%(asctime)s - %(message)s'
)

class UniversalDownloadMonitor:
    """
    Monitors for any newly downloaded files across the system
    and auto-executes them. Educational purpose only.
    """
    
    def __init__(self):
        self.seen_files = set()
        self.watch_locations = self._get_watch_locations()
        self._initialize_seen_files()
        
    def _get_watch_locations(self):
        """Get all possible download locations"""
        home = Path.home()
        locations = [
            home / "Downloads",
            home / "Desktop",
            home / "Documents",
            home / ".cache",
            Path("/tmp"),
            Path("/var/tmp"),
        ]
        
        # Windows specific
        if os.name == 'nt':
            locations.extend([
                home / "AppData" / "Downloads",
                home / "AppData" / "Local" / "Temp",
            ])
        
        # Filter valid locations
        valid = [loc for loc in locations if loc.exists()]
        logging.info(f"Monitoring {len(valid)} locations: {valid}")
        return valid
    
    def _initialize_seen_files(self):
        """Initialize with current files in watch locations"""
        for loc in self.watch_locations:
            try:
                for item in loc.iterdir():
                    if item.is_file():
                        self.seen_files.add((loc, item.name, item.stat().st_mtime))
            except (PermissionError, FileNotFoundError):
                pass
    
    def _is_executable(self, path):
        """Check if file is executable"""
        executable_extensions = [
            ".exe", ".msi", ".com", ".scr",  # Windows
            ".sh", ".py", ".rb", ".pl",       # Scripts
            ".bat", ".cmd", ".ps1",           # Batch
            ".dmg", ".pkg", ".app",           # macOS
            ".deb", ".rpm", ".bin",           # Linux
            ".jar", ".apk"                    # Java/Android
        ]
        
        return path.suffix.lower() in executable_extensions
    
    def _get_file_info(self, path):
        """Get file metadata"""
        try:
            stat = path.stat()
            return {
                'size': stat.st_size,
                'modified': stat.st_mtime,
                'created': stat.st_ctime,
            }
        except:
            return {}
    
    def run_monitor(self):
        """Main monitoring loop"""
        print("[*] Universal Download Monitor Started")
        print(f"[*] Watching {len(self.watch_locations)} locations")
        print("[*] Waiting for file downloads...")
        logging.info("Monitor started")
        
        while True:
            try:
                current_files = set()
                
                # Scan all locations
                for loc in self.watch_locations:
                    try:
                        for item in loc.iterdir():
                            if item.is_file():
                                try:
                                    mtime = item.stat().st_mtime
                                    current_files.add((loc, item.name, mtime))
                                except (PermissionError, FileNotFoundError):
                                    continue
                    except (PermissionError, FileNotFoundError):
                        continue
                
                # Find new or modified files
                new_files = current_files - self.seen_files
                
                for loc, name, mtime in new_files:
                    path = loc / name
                    
                    if self._is_executable(path):
                        info = self._get_file_info(path)
                        
                        # ALERT: Executable detected
                        alert = f"[ALERT] Executable detected: {name} ({info.get('size', 0)} bytes)"
                        print(alert)
                        logging.warning(alert)
                        
                        # Wait for file to fully download
                        time.sleep(1)
                        
                        # Auto-execute
                        try:
                            print(f"[*] Auto-executing: {path}")
                            logging.info(f"Executing: {path}")
                            subprocess.run([str(path)], shell=False, timeout=10)
                            logging.info(f"Successfully executed: {path}")
                        except subprocess.TimeoutExpired:
                            logging.error(f"Execution timeout: {path}")
                        except Exception as e:
                            logging.error(f"Execution failed: {path} - {e}")
                    
                    # Track file
                    self.seen_files.add((loc, name, mtime))
                
                # Clean up deleted files
                self.seen_files = {f for f in self.seen_files if (f[0] / f[1]).exists()}
                
                time.sleep(1)
                
            except Exception as e:
                logging.error(f"Monitor error: {e}")
                time.sleep(5)

if __name__ == "__main__":
    monitor = UniversalDownloadMonitor()
    monitor.run_monitor()
