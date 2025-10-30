import os
import shutil
import platform
import time
import sys
import json
from datetime import datetime
from pathlib import Path

# Get platform-specific paths
SYSTEM = platform.system()
if SYSTEM == "Windows":
    LOG_DIR = os.path.join(os.getenv('APPDATA'), 'SmartCleaner')
else:
    LOG_DIR = os.path.expanduser("~/.smart-cleaner")

# Create log directory if it doesn't exist
os.makedirs(LOG_DIR, exist_ok=True)
LOG_FILE = os.path.join(LOG_DIR, "deletion_log.txt")
CONFIG_FILE = os.path.join(LOG_DIR, "config.json")


def log_action(message, action_type="INFO"):
    """
    Log actions to both file and console.
    
    Args:
        message (str): Message to log
        action_type (str): Type of action (INFO, DELETED, ERROR, WARNING)
    """
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    log_message = f"[{timestamp}] [{action_type}] {message}"
    
    # Print to console
    print(log_message)
    
    # Write to log file
    try:
        with open(LOG_FILE, 'a', encoding='utf-8') as f:
            f.write(log_message + "\n")
    except Exception as e:
        print(f"[ERROR] Could not write to log file: {e}")


def get_platform_path(user_path=""):
    """
    Convert user input path to platform-specific path.
    
    Args:
        user_path (str): User-provided path
        
    Returns:
        str: Platform-specific full path
    """
    if not user_path:
        if SYSTEM == "Windows":
            return "D:\\"
        else:
            return os.path.expanduser("~/Test")
    
    # Expand user home directory
    if user_path.startswith("~"):
        return os.path.expanduser(user_path)
    
    # Handle Windows drive letters
    if SYSTEM == "Windows" and len(user_path) == 2 and user_path[1] == ":":
        return user_path + "\\"
    
    return user_path


def ask_confirmation(folder_path):
    """
    Ask user for confirmation before starting deletion.
    
    Args:
        folder_path (str): The folder to delete from
        
    Returns:
        bool: True if user confirms
    """
    print("\n" + "="*60)
    print("⚠️  WARNING: DELETION SERVICE INITIALIZATION")
    print("="*60)
    print(f"Target Folder: {folder_path}")
    print(f"System: {SYSTEM}")
    print(f"Log File: {LOG_FILE}")
    print("="*60)
    print("\nThis will DELETE all files and folders in the target directory!")
    print("This action CANNOT be undone!\n")
    
    response = input("Do you want to continue? (yes/no): ").strip().lower()
    
    if response in ['yes', 'y']:
        return True
    else:
        print("[INFO] Operation cancelled by user")
        return False


def save_config(folder_path, interval, schedule_time=None):
    """
    Save configuration to JSON file for future use.
    
    Args:
        folder_path (str): Target folder path
        interval (int): Deletion interval in seconds
        schedule_time (str): Optional scheduled time (HH:MM format)
    """
    config = {
        "folder_path": folder_path,
        "interval": interval,
        "schedule_time": schedule_time,
        "created": datetime.now().isoformat(),
        "system": SYSTEM
    }
    
    try:
        with open(CONFIG_FILE, 'w') as f:
            json.dump(config, f, indent=4)
        log_action(f"Configuration saved to {CONFIG_FILE}", "INFO")
    except Exception as e:
        log_action(f"Could not save config: {e}", "ERROR")


def should_run_at_scheduled_time(schedule_time):
    """
    Check if current time matches scheduled time.
    
    Args:
        schedule_time (str): Time in HH:MM format
        
    Returns:
        bool: True if it's time to run
    """
    if not schedule_time:
        return True
    
    try:
        current_time = datetime.now().strftime("%H:%M")
        if current_time == schedule_time:
            return True
    except Exception as e:
        log_action(f"Error checking scheduled time: {e}", "ERROR")
    
    return False


def delete_folder_contents(folder_path, interval=5, verbose=True, schedule_time=None):
    """
    Enhanced deletion monitor with all features.
    
    Args:
        folder_path (str): The folder path to monitor and delete from
        interval (int): Time in seconds between deletion attempts
        verbose (bool): Whether to print what's being deleted
        schedule_time (str): Optional scheduled time (HH:MM format)
    """
    
    if not os.path.exists(folder_path):
        log_action(f"Folder does not exist: {folder_path}", "ERROR")
        return False
    
    if not os.path.isdir(folder_path):
        log_action(f"Path is not a directory: {folder_path}", "ERROR")
        return False
    
    log_action(f"Starting deletion monitor on: {folder_path}", "INFO")
    log_action(f"Files will be deleted every {interval} seconds", "WARNING")
    if schedule_time:
        log_action(f"Scheduled to run at: {schedule_time}", "INFO")
    log_action("Press Ctrl+C to stop", "INFO")
    
    # Save configuration
    save_config(folder_path, interval, schedule_time)
    
    try:
        while True:
            # Check if we should run at scheduled time
            if not should_run_at_scheduled_time(schedule_time):
                time.sleep(1)
                continue
            
            if os.path.exists(folder_path):
                items = os.listdir(folder_path)
                
                if items:
                    if verbose:
                        log_action(f"Found {len(items)} items to delete", "INFO")
                    
                    for item in items:
                        item_path = os.path.join(folder_path, item)
                        try:
                            if os.path.isfile(item_path):
                                os.remove(item_path)
                                log_action(f"File deleted: {item}", "DELETED")
                            elif os.path.isdir(item_path):
                                shutil.rmtree(item_path)
                                log_action(f"Folder deleted: {item}/", "DELETED")
                        except PermissionError:
                            log_action(f"Permission denied: {item}", "ERROR")
                        except Exception as e:
                            log_action(f"Could not delete {item}: {e}", "ERROR")
                else:
                    if verbose:
                        log_action("Folder is empty, waiting...", "INFO")
            
            time.sleep(interval)
    
    except KeyboardInterrupt:
        log_action("Deletion monitor stopped by user", "INFO")
        return True


def main():
    """Main entry point with enhanced features"""
    
    print("╔" + "="*58 + "╗")
    print("║" + " "*10 + "🔧 SMART CLEANER - FOLDER DELETION SERVICE" + " "*5 + "║")
    print("║" + " "*16 + f"Platform: {SYSTEM}" + " "*36 + "║")
    print("╚" + "="*58 + "╝\n")
    
    # Get target folder
    if len(sys.argv) > 1:
        target_folder = sys.argv[1]
    else:
        print("Enter the folder path to monitor:")
        print("  Examples:")
        print("    Windows: D:\\  or  C:\\Users\\YourName\\Temp")
        print("    Linux:   ~/Test  or  /tmp/test\n")
        user_input = input("Folder path: ").strip()
        target_folder = get_platform_path(user_input) if user_input else get_platform_path()
    
    target_folder = get_platform_path(target_folder)
    
    if not target_folder:
        log_action("No folder path provided", "ERROR")
        return
    
    # Get deletion interval
    interval = 5
    if len(sys.argv) > 2:
        try:
            interval = int(sys.argv[2])
        except ValueError:
            log_action(f"Invalid interval, using default: {interval} seconds", "WARNING")
    else:
        try:
            user_interval = input("\nDeletion interval in seconds (default 5): ").strip()
            if user_interval:
                interval = int(user_interval)
        except ValueError:
            log_action(f"Invalid input, using default interval: {interval} seconds", "WARNING")
    
    # Get optional scheduled time
    schedule_time = None
    if len(sys.argv) > 3:
        schedule_time = sys.argv[3]
    else:
        schedule_opt = input("Set scheduled time? (HH:MM format, or press Enter to skip): ").strip()
        if schedule_opt:
            schedule_time = schedule_opt
    
    # Ask for confirmation
    if not ask_confirmation(target_folder):
        return
    
    # Run the deletion monitor
    try:
        delete_folder_contents(target_folder, interval=interval, verbose=True, schedule_time=schedule_time)
    except Exception as e:
        log_action(f"Unexpected error: {e}", "ERROR")


if __name__ == "__main__":
    main()
