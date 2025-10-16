# W1 - CPU and RAM Occupation Scripts

This directory contains Python scripts designed to demonstrate and test system resource consumption by occupying CPU and RAM resources.

## Files

### 1. `occupyCPU.py`
A script that occupies CPU resources based on user-specified percentage.

**What it does:**
- Displays the number of CPU cores available on your system
- Prompts user to enter a percentage (1-100) of CPU to occupy
- Calculates the number of cores to use: `max(1, round((percent / 100) * os.cpu_count()))`
- Spawns multiple processes, each running an infinite CPU-bound loop
- Each process continuously performs integer arithmetic operations to keep the CPU busy
- Runs until manually stopped with `Ctrl+C`

**How to run:**
```bash
python3 occupyCPU.py
```
Then enter your desired CPU percentage (e.g., `25` for 25% CPU usage).

### 2. `occupyRAM.py`
A script that allocates and holds memory to occupy a specified percentage of available RAM.

**What it does:**
- Uses the `psutil` library to display current memory statistics (total, used, free)
- Prompts user for percentage of available RAM to occupy (0-100)
- Calculates target memory in MB based on available memory
- Asks for confirmation before proceeding
- Allocates memory in 1 MB chunks (using `bytearray`)
- Shows progress every 100 MB allocated
- Keeps the memory occupied until stopped with `Ctrl+C`
- Gracefully handles memory allocation failures

**How to run:**
```bash
python3 occupyRAM.py
```
Enter percentage when prompted and confirm with `y`.

## Requirements

**For `occupyCPU.py`:**
- Python 3.x
- Standard library only (no external dependencies)

**For `occupyRAM.py`:**
- Python 3.x
- `psutil` library

Install psutil with:
```bash
pip install psutil
```

##  Important Safety Warnings

These scripts intentionally consume system resources and should be used carefully:

1. **System Responsiveness**: Occupying high percentages of CPU or RAM can make your system slow or unresponsive
2. **Start Small**: Begin with low percentages (e.g., 10-20%) to observe behavior
3. **Don't Use 100%**: Requesting 100% of resources can freeze your system
4. **Use in Safe Environments**: Run these scripts in:
   - Virtual machines
   - Test/lab environments
   - Systems where you can safely recover from unresponsiveness
5. **Know How to Stop**: Always use `Ctrl+C` to stop the scripts gracefully
6. **Close Other Applications**: Before running, save your work and close unnecessary applications

## How the Scripts Work

### CPU Occupation Strategy
The CPU scripts use multiprocessing to spawn separate processes (not threads). Each process:
- Runs an infinite loop performing integer arithmetic
- Uses modulo operations to keep numbers bounded (prevents overflow)
- Consumes approximately 100% of one CPU core per process
- Number of processes = `round(percentage/100 × total_cores)`

### RAM Occupation Strategy
The RAM script:
- Queries available memory using `psutil.virtual_memory().available`
- Allocates memory in 1 MB chunks by creating `bytearray` objects
- Stores references to all chunks in a list to prevent garbage collection
- Continues holding memory until the script exits
- Handles `MemoryError` exceptions if allocation fails

## Usage Examples

**Example 1: Occupy 25% of CPU**
```bash
$ python3 occupyCPU.py
Your System has 8 CPU cores
Enter the perecentage of CPU to be occupied(100): 25
occupying 2cpu cores
Started 2 CPU-occupying processes.
[Press Ctrl+C to stop]
```

**Example 2: Occupy 10% of available RAM**
```bash
$ python3 occupyRAM.py
Total Memory: 16.00
Used Memory: 8.50
Free Memory: 7.50
Enter the percentage of RAM to occupy (0-100): 10
Please presss "y" to confirm or press other to cancel: y
Occupying 768.00 MB offree  RAM (10%)

Starting to allocate 768.0 MB of RAM...
[Progress updates...]
Successfully allocated 768.0 MB of RAM.
RAM will remain the occpuied. Press Ctrl+C to exit...
```

## Educational Purpose

These scripts are designed for:
- Learning about system resource management
- Testing system performance under load
- Understanding memory allocation and CPU consumption
- Demonstrating resource occupation techniques
- Cybersecurity and system administration training

## Notes

- The CPU occupation is "all or nothing" per core - each spawned process uses 100% of one core
- To achieve precise percentage control (e.g., exactly 30% of one core), a duty-cycle approach (alternating busy/sleep periods) would be needed
- RAM allocation is based on *available* memory, not total system memory
- The scripts handle `KeyboardInterrupt` to cleanly release resources when stopped

## License

Educational use only. Use at your own risk.
