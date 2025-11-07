import winreg
from packaging import version

def get_installed_apps():
    apps = {}
    
    paths = [
        (winreg.HKEY_LOCAL_MACHINE, r"SOFTWARE\Microsoft\Windows\CurrentVersion\Uninstall"),
        (winreg.HKEY_LOCAL_MACHINE, r"SOFTWARE\WOW6432Node\Microsoft\Windows\CurrentVersion\Uninstall"),
        (winreg.HKEY_CURRENT_USER, r"SOFTWARE\Microsoft\Windows\CurrentVersion\Uninstall")
    ]

    for root, path in paths:
        try:
            key = winreg.OpenKey(root, path)
            for i in range(winreg.QueryInfoKey(key)[0]):
                try:
                    subkey_name = winreg.EnumKey(key, i)
                    subkey = winreg.OpenKey(key, subkey_name)
                    
                    # Skip if no display name
                    try:
                        name = winreg.QueryValueEx(subkey, "DisplayName")[0]
                    except:
                        subkey.Close()
                        continue
                    
                    # Skip system components
                    try:
                        if winreg.QueryValueEx(subkey, "SystemComponent")[0] == 1:
                            subkey.Close()
                            continue
                    except:
                        pass
                    
                    # Skip Windows updates
                    try:
                        release_type = winreg.QueryValueEx(subkey, "ReleaseType")[0].lower()
                        if release_type in ["update", "hotfix", "security update"]:
                            subkey.Close()
                            continue
                    except:
                        pass
                    
                    # Get version
                    try:
                        app_version = winreg.QueryValueEx(subkey, "DisplayVersion")[0]
                    except:
                        app_version = "Unknown"
                    
                    apps[name] = app_version
                    subkey.Close()
                    
                except:
                    continue
            key.Close()
        except:
            continue
            
    return apps

def check_outdated_apps():
    # Common applications with their latest versions
    latest_versions = {
        "google chrome": "120.0.6099.109",
        "mozilla firefox": "121.0", 
        "microsoft edge": "120.0.2210.144",
        "vlc media player": "3.0.18",
        "7-zip": "23.01",
        "adobe reader": "2023.008.20421",
        "python": "3.12.1",
        "git": "2.43.0",
        "node.js": "20.11.0",
        "visual studio code": "1.85.1",
        "java": "21.0.1",
        "spotify": "1.2.15.828",
        "skype": "8.105.0.210",
        "zoom": "5.17.6",
        "discord": "1.0.9020"
    }
    
    installed_apps = get_installed_apps()
    outdated_apps = []
    uptodate_apps = []
    unknown_apps = []
    
    for app_name, installed_version in installed_apps.items():
        app_lower = app_name.lower()
        found = False
        
        for known_app, latest_version in latest_versions.items():
            if known_app in app_lower:
                found = True
                if installed_version == "Unknown":
                    unknown_apps.append((app_name, installed_version, latest_version))
                else:
                    try:
                        # Clean version strings for comparison
                        installed_clean = installed_version.split()[0]  # Take first part if space
                        latest_clean = latest_version.split()[0]
                        
                        if version.parse(installed_clean) < version.parse(latest_clean):
                            outdated_apps.append((app_name, installed_version, latest_version))
                        else:
                            uptodate_apps.append((app_name, installed_version, latest_version))
                    except:
                        unknown_apps.append((app_name, installed_version, latest_version))
                break
        
        if not found:
            unknown_apps.append((app_name, installed_version, "Unknown"))
    
    return outdated_apps, uptodate_apps, unknown_apps

# Check for outdated applications
print("Scanning for outdated applications...")
outdated, uptodate, unknown = check_outdated_apps()

print(f"\nFound {len(uptodate)} up-to-date applications, {len(outdated)} outdated applications, and {len(unknown)} with unknown status")

print("\n🟢 UP-TO-DATE APPLICATIONS:")
print("-" * 50)
for app, current, latest in uptodate:
    print(f"✓ {app}")
    print(f"  Version: {current} (Latest: {latest})")
    print()

print("\n🔴 OUTDATED APPLICATIONS:")
print("-" * 50)
for app, current, latest in outdated:
    print(f"✗ {app}")
    print(f"  Version: {current} → Latest: {latest}")
    print()
