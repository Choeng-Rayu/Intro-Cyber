#!/usr/bin/env python3
import os, shutil, time, logging, configparser
from datetime import datetime
from pathlib import Path

class SmartCleaner:
    def __init__(self, folder=None, dry_run=False):
        # Default folder if not specified
        if folder is None:
            folder = "~/Downloads"
        self.folder = os.path.abspath(os.path.expanduser(folder))
        self.dry_run = dry_run
        self.quarantine = os.path.expanduser(
            f"~/quarantine_{datetime.now().strftime('%Y%m%d_%H%M%S')}")
        os.makedirs(self.quarantine, exist_ok=True)
        logging.basicConfig(
            filename=os.path.expanduser("~/smart_cleaner.log"),
            level=logging.INFO,
            format="%(asctime)s %(levelname)s: %(message)s"
        )

    def scan_files(self):
        # Recursively scan all files in the target directory and subdirectories
        try:
            for root, dirs, files in os.walk(self.folder):
                for f in files:
                    yield os.path.join(root, f)
        except Exception as e:
            logging.error(f"Error scanning {self.folder}: {e}")

    def remove_empty_folders(self):
        # Remove empty folders after files are moved
        try:
            for root, dirs, files in os.walk(self.folder, topdown=False):
                for d in dirs:
                    folder_path = os.path.join(root, d)
                    if not os.listdir(folder_path):  # Check if empty
                        if self.dry_run:
                            print(f"[DRY-RUN] Would delete empty folder: {folder_path}")
                        else:
                            os.rmdir(folder_path)
                            print(f"Deleted empty folder: {folder_path}")
                            logging.info(f"DELETED FOLDER {folder_path}")
        except Exception as e:
            logging.error(f"Error removing empty folders: {e}")

    def move_to_quarantine(self, path):
        dest = os.path.join(self.quarantine, os.path.basename(path))
        if self.dry_run:
            print(f"[DRY-RUN] Would move {path} -> {dest}")
            return
        shutil.move(path, dest)
        print(f"Moved: {path}")
        logging.info(f"MOVED {path} -> {dest}")

    def run(self):
        if not os.path.isdir(self.folder):
            print("❌ Invalid folder path.")
            return

        items = list(self.scan_files())
        if not items:
            print("✅ Folder is already clean.")
            return

        print(f"🧹 Found {len(items)} items to clean in {self.folder}")
        for item in items:
            try:
                self.move_to_quarantine(item)
            except Exception as e:
                logging.error(f"Error moving {item}: {e}")
                print(f"⚠️  Error moving {item}: {e}")

        # Remove empty folders after files are moved
        self.remove_empty_folders()
        print(f"✅ All items moved to {self.quarantine}")

def load_config():
    """Load configuration from smart-cleaner.conf file"""
    config_paths = [
        "/etc/smart-cleaner/smart-cleaner.conf",  # System-wide config
        "/usr/local/etc/smart-cleaner.conf",      # Local config
        os.path.expanduser("~/.config/smart-cleaner/smart-cleaner.conf"),  # User config
        "./smart-cleaner.conf"                    # Current directory
    ]
    
    config = configparser.ConfigParser()
    
    # Set default values
    defaults = {
        'FOLDER_TO_CLEAN': '~/Downloads',
        'INTERVAL_SECONDS': '30'
    }
    
    # Try to find and load config file
    for config_path in config_paths:
        if os.path.exists(config_path):
            print(f"📖 Loading config from: {config_path}")
            config.read(config_path)
            break
    
    # Get values from config or use defaults
    if config.has_section('DEFAULT'):
        folder = config.get('DEFAULT', 'FOLDER_TO_CLEAN', fallback=defaults['FOLDER_TO_CLEAN'])
        interval = config.getint('DEFAULT', 'INTERVAL_SECONDS', fallback=int(defaults['INTERVAL_SECONDS']))
    else:
        folder = defaults['FOLDER_TO_CLEAN']
        interval = int(defaults['INTERVAL_SECONDS'])
    
    return folder, interval

def main():
    # Load configuration from file
    FOLDER_TO_CLEAN, INTERVAL_SECONDS = load_config()
    
    cleaner = SmartCleaner(folder=FOLDER_TO_CLEAN, dry_run=False)
    
    print(f"🚀 Smart Cleaner Service Started")
    print(f"📁 Target folder: {cleaner.folder}")
    print(f"⏳ Running every {INTERVAL_SECONDS} seconds... Press Ctrl+C to stop.")
    
    try:
        while True:
            cleaner.run()
            time.sleep(INTERVAL_SECONDS)
    except KeyboardInterrupt:
        print("\n🛑 Stopped by user.")
    except Exception as e:
        logging.error(f"Service error: {e}")
        print(f"❌ Error: {e}")

if __name__ == "__main__":
    main()