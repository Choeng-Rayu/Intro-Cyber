import time
import os
import multiprocessing

def occupyCPU():
    """Infinite loop to occupy CPU resources"""
    x = 0 
    while True:
        x = (x + 1) % 1000000  # Keep x bounded to prevent overflow
        x = x ** 2 % 1000000   # Modulo keeps number manageable
    
if __name__ == "__main__":
    print(f"Your System has {os.cpu_count()} CPU cores")
    # ask user to input the percentage of CPU to be occupied
    
    while (True): 

        percent = float(input("Enter the perecentage of CPU to be occupied(100): "))
        if(percent > 0 and percent <= 100):
            num_cores = max(1, round((percent / 100) * os.cpu_count()))
            print(f"occupying {num_cores}cpu cores")
            processes = []
            for i in range(num_cores):
                p = multiprocessing.Process(target=occupyCPU)
                p.start()
                processes.append(p)
            print(f"Started {num_cores} CPU-occupying processes.")
            try: 
                while True:
                    time.sleep(1)
            except KeyboardInterrupt:
                print("\nStopping all CPU processes...")
                for p in processes:
                    p.terminate()
                    p.join()
                print("All CPU processes stopped.")
            break
        else:
            print ("Invalid input, please enter a number between 1 to 100")
