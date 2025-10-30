import os
import sys
import time

if sys.platform == 'win32':
    import winreg
    _registry = winreg.ConnectRegistry(None, winreg.HKEY_CURRENT_USER)

    def get_runonce():
        return winreg.OpenKey(
            _registry,
            r"SOFTWARE\Microsoft\Windows\CurrentVersion\Run",
            0,
            winreg.KEY_ALL_ACCESS
        )

    def add(name, application):
        """Add a new autostart entry"""
        key = get_runonce()
        try:
            winreg.SetValueEx(key, name, 0, winreg.REG_SZ, application)
            print(f"[+] Added startup entry: {name}")
        except WindowsError as e:
            print(e)
        winreg.CloseKey(key)

    def exists(name):
        """Check if an autostart entry exists"""
        key = get_runonce()
        exists = True
        try:
            winreg.QueryValueEx(key, name)
        except WindowsError:
            exists = False
        winreg.CloseKey(key)
        return exists

    def remove(name):
        """Delete an autostart entry"""
        if exists(name):
            key = get_runonce()
            winreg.DeleteValue(key, name)
            winreg.CloseKey(key)
            print(f"[-] Removed startup entry: {name}")

else:
    _xdg_config_home = os.environ.get("XDG_CONFIG_HOME", "~/.config")
    _xdg_user_autostart = os.path.join(os.path.expanduser(_xdg_config_home), "autostart")
    if not os.path.exists(_xdg_user_autostart):
        os.makedirs(_xdg_user_autostart)

    def getfilename(name):
        return os.path.join(_xdg_user_autostart, name + ".desktop")

    def add(name, application):
        desktop_entry = f"[Desktop Entry]\nName={name}\nExec={application}\nType=Application\nTerminal=false\n"
        with open(getfilename(name), "w") as f:
            f.write(desktop_entry)
        print(f"[+] Added autostart file: {getfilename(name)}")

    def exists(name):
        return os.path.exists(getfilename(name))

    def remove(name):
        if exists(name):
            os.unlink(getfilename(name))
            print(f"[-] Removed autostart file: {getfilename(name)}")


def main():
    app_name = "HelloWorldAutoRun"
    app_path = os.path.abspath(sys.argv[0])

    if not exists(app_name):
        add(app_name, app_path)
    
    
    while True:
        print("Hello Heng")
        time.sleep(30)


if __name__ == "__main__":
    main()
