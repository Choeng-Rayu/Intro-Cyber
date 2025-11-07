import os
from pathlib import Path

def count_mac_apps():
    # Common macOS application directories
    system_apps = Path("/Applications")
    user_apps = Path.home() / "Applications"

    app_paths = [system_apps, user_apps]
    total_apps = 0
    app_list = []

    for path in app_paths:
        if path.exists():
            # List all items that end with .app
            apps = [item.name for item in path.iterdir() if item.suffix == ".app"]
            total_apps += len(apps)
            app_list.extend(apps)

    print(f"Total applications found: {total_apps}")
    print("\nAll installed apps:")
    print("=" * 50)
    for app in app_list:  # Show all apps
        print(f" - {app}")

if __name__ == "__main__":
    count_mac_apps()