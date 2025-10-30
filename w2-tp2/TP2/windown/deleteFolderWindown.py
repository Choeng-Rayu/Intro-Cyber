import os
import shutil
import platform
import time

# Base path
if platform.system() == "Windows":
    base_path = "D:\\"
else:
    base_path = os.path.expanduser("~")

folder_path = os.path.join(base_path, "Test")

while True:
    if os.path.exists(folder_path):
        for item in os.listdir(folder_path):
            item_path = os.path.join(folder_path, item)
            try:
                if os.path.isfile(item_path):
                    os.remove(item_path)
                else:
                    shutil.rmtree(item_path)
            except:
                pass
    time.sleep(5)  # wait 5 seconds before checking again


