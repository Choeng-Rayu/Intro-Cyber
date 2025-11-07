"""
Setup detector.py as Windows auto-start service
This makes the auto-run service start with Windows (simulating compromised system)
FOR EDUCATION ONLY!
"""

import sys
import os
import winreg
from pathlib import Path

def add_to_startup():
    """Add detector.py to Windows startup"""
    try:
        # Get path to detector.py
        detector_path = Path(__file__).parent / "detector.py"
        python_path = sys.executable
        
        # Command to run detector.py at startup
        command = f'"{python_path}" "{detector_path}"'
        
        # Add to registry
        key = winreg.OpenKey(
            winreg.HKEY_CURRENT_USER,
            r"Software\Microsoft\Windows\CurrentVersion\Run",
            0,
            winreg.KEY_SET_VALUE
        )
        winreg.SetValueEx(key, "SecurityMonitor", 0, winreg.REG_SZ, command)
        winreg.CloseKey(key)
        
        print("=" * 60)
        print("✓ Auto-run service installed!")
        print("=" * 60)
        print(f"detector.py will now start automatically at login")
        print(f"Location: {detector_path}")
        print()
        print("To test: Reboot and check if detector.py is running")
        print()
        print("To remove:")
        print('  reg delete "HKCU\\Software\\Microsoft\\Windows\\CurrentVersion\\Run" /v "SecurityMonitor" /f')
        print("=" * 60)
        
        return True
        
    except Exception as e:
        print(f"Error: {e}")
        return False

def remove_from_startup():
    """Remove detector.py from Windows startup"""
    try:
        key = winreg.OpenKey(
            winreg.HKEY_CURRENT_USER,
            r"Software\Microsoft\Windows\CurrentVersion\Run",
            0,
            winreg.KEY_SET_VALUE
        )
        winreg.DeleteValue(key, "SecurityMonitor")
        winreg.CloseKey(key)
        print("✓ Auto-run service removed from startup")
        return True
    except:
        print("Not found in startup")
        return False

if __name__ == "__main__":
    print("=" * 60)
    print("Auto-Run Service Setup (Simulates Vulnerable System)")
    print("=" * 60)
    print()
    print("This will make detector.py auto-start with Windows")
    print("detector.py will then auto-execute any .exe in Downloads")
    print()
    print("Options:")
    print("  1. Install auto-run service")
    print("  2. Remove auto-run service")
    print()
    
    choice = input("Enter choice (1 or 2): ").strip()
    
    if choice == "1":
        add_to_startup()
    elif choice == "2":
        remove_from_startup()
    else:
        print("Invalid choice")
