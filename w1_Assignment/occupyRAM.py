import psutil
import time

def occupyRam(target_mb):
    """
    Occupies Ram by creating a list of filled with data args: 
    target_mb: Amount of Ram to occupy in megabytes
    """
    data = []
    chunk_size = 1024 * 1024 # 1 mb chunk (1024 * 1024 bytes)
    allocated_mb = 0

    try: 
        print(f"\nStarting to allocate {target_mb} MB of RAM...")
        while allocated_mb < target_mb:
            chunk = bytearray(chunk_size)
            data.append(chunk)
            allocated_mb += 1
            # show progress every 100 MB
            if allocated_mb % 100 == 0:
                current_used_memory = psutil.virtual_memory().used / (1024 ** 3)
                print(f"Allocated: {allocated_mb} MB | Current RAM usage: {current_used_memory:.2f} GB")
        print(f"\nSuccessfully allocated {target_mb} MB of RAM.")
        print(f"RAM will remain the occpuied. Press Ctrl+C to exit...")

        # keep the data in memory (infinite looop)
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        print("\n\n Releasing RAM and Existing...")
        data.clear()        
    except MemoryError:
        print("Memory allocation failed. Not enough available memory.")
        print(f"Only allocated {allocated_mb} MB before running out of memory.")
        data.clear()
    
def dislay_memory_info():
    """Display corrent memory statistices"""
    total_memory_gb = psutil.virtual_memory().total / (1024 ** 3)
    used_memory_gb = psutil.virtual_memory().used / (1024 ** 3)
    free_memory_gb = total_memory_gb - used_memory_gb
    print(f"Total Memory: {total_memory_gb:.2f}")
    print(f"Used Memory: {used_memory_gb:.2f}")
    print(f"Free Memory: {free_memory_gb:.2f}")

if __name__ == "__main__":
    dislay_memory_info()

    # let user input the percentage ot ram to occupies
    while True: 
        try:
            percent = float(input("Enter the percentage of RAM to occupy (0-100): "))
            if percent <= 0 or percent > 100:
                print("Percentage must be between greate then 0 to 100\n Please input again!")
                continue
            free_memory = psutil.virtual_memory().available
            target_bytes = free_memory * percent / 100
            target_mb = target_bytes / (1024 ** 2)
            confirmOccupy = input(f"Please presss ""y"" to confirm or press other to cancel: ")
            if confirmOccupy == "y":
                print(f"Occupying {target_mb:.2f} MB offree  RAM ({percent}%)")
                occupyRam(target_mb)
                break
            else:
                print("Occupying cancelled.")
                continue
        except ValueError:
            print("Invalid input. Please enter a valid number.")
        except KeyboardInterrupt:
            print("Occupying cancelled.")
            break


    
