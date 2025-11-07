import winreg
import time

def get_installed_apps():
    
    apps = set()
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
                    
                    apps.add(name)
                    subkey.Close()
                    
                except:
                    continue
            key.Close()
        except:
            continue
            
    return apps

apps = get_installed_apps()
print(f"Found {len(apps)} user-installed applications:")
for app in sorted(apps):
    print(f" - {app}")
    