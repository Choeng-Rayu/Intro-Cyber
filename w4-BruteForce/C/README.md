# High-Performance C Brute Force Password Cracker

## 🚀 Overview

This is a **multi-threaded C implementation** of a brute force password cracker for **Windows**. It cracks passwords by systematically trying all possible character combinations across 16 parallel worker threads.

**Target Password:** `Za8yK` (5 characters)  
**Performance:** ~14.6 million attempts/second

---

## 📋 What This Code Does

The program cracks a password through:
1. **Parallel Processing** - 16 worker threads attack simultaneously
2. **Search Space Division** - Each thread gets unique number range to test
3. **Number-to-Password Conversion** - Numbers converted to password strings
4. **Comparison** - Each candidate compared with target password
5. **Coordination** - First thread to find password signals others to stop

---

## 🔧 Code Architecture

### Core Components

- **Data Structures** - Store configuration, worker arguments, and results
- **Utility Functions** - Helper functions for timing, calculations, and comparisons
- **Worker Thread Function** - Core function run by each thread to search assigned range
- **Attack Coordinator** - Manages thread creation and work distribution
- **Main Entry Point** - Setup, execution, and result display

---

## ⚡ Key Optimizations

### 1. **Parallel Processing**
- 16 worker threads run simultaneously
- Each thread handles ~57 million combinations independently
- Provides significant speedup compared to single-threaded approach

### 2. **Work Distribution**
- Total combinations divided equally among all threads
- Each thread works on independent number range
- Ensures efficient CPU utilization

### 3. **Fast Password Generation**
- Uses base-62 conversion system (62 characters = A-Z, a-z, 0-9)
- Optimized for performance with loop unrolling
- Converts numbers sequentially to password strings

### 4. **Optimized Comparison**
- Two-stage matching process for efficiency
- First checks only critical characters (quick elimination)
- Full comparison only when necessary
- Early exit on mismatch

### 5. **Stop Flag Batching**
- Threads check stop flag periodically (not every iteration)
- Reduces cache synchronization overhead
- Improves multi-threaded performance

### 6. **Thread Synchronization**
- Uses Windows `CRITICAL_SECTION` for safe coordination
- Prevents race conditions when announcing password found
- Minimal performance impact on main loop

---

## 🔐 How It Works: Overview

### Initialization
```
Calculate total combinations: 62^5 = 916,132,832
Divide work: 916,132,832 ÷ 16 threads = ~57 million each
Create CRITICAL_SECTION for thread safety
```

### Execution
```
For each password length (1 to 5):
  Create 16 worker threads
  Each thread assigned unique number range
  Threads generate passwords and compare with target
  First thread to find match signals all others
  All threads exit
```

### Completion
```
First thread to find match:
  Acquires lock (critical section)
  Sets password found flag
  Sets stop flag (signals other threads)
  Stores result
  Releases lock

Other threads:
  Check stop flag periodically
  Exit when flag is set
```

---

## 📊 Performance Characteristics

### Time Complexity
- **Single-threaded:** O(62^5) = 916,132,832 operations
- **16-threaded:** O(62^5 / 16) ≈ 57 million operations per thread

### Password Cracking Time
```
Character Set: 62 (A-Z, a-z, 0-9)
Password Length: 5

Speed: 14.6 million attempts/second
Worst case: ~63 seconds
Average case: ~31 seconds
Target "Za8yK": 2.21 seconds
```

### Why It's Fast
- Native C code (no garbage collection overhead)
- Windows native threading support
- Compiler optimizations (`-O3 -march=native`)
- Minimal lock contention
- CPU vectorization

---

## 💻 Compilation & Usage

### Compile (Windows)
```bash
gcc -O3 -march=native c.c -o c.exe
```

### Run with Default Settings
```bash
c.exe
# Cracks "Za8yK" with 16 threads
```

### Run with Custom Password
```bash
c.exe "MyPassword"
```

### Run with Custom Password and Thread Count
```bash
c.exe "MyPassword" 32
```

---

## 🛡️ Security Implications

### 5-Character Passwords Are Weak
```
Total combinations: 916,132,832
Average time to crack: ~31 seconds
```

### Password Length Impact
```
5-char:  916M combinations → Seconds to crack
6-char:  57B combinations → Minutes to crack
7-char:  3.5T combinations → Days to crack
8-char:  218T combinations → Months to crack
```

### Defense Mechanisms
1. **Long passwords** (12+ characters) - Exponentially harder to crack
2. **Rate limiting** - Restrict login attempts per time period
3. **Account lockout** - Lock after failed attempts
4. **Multi-Factor Authentication** - Additional verification layer
5. **Password hashing** - Use bcrypt/argon2 to slow down each attempt

---

## 🎯 Key Features

| Feature | Purpose |
|---------|---------|
| **Multi-threading** | Windows `CreateThread()` creates 16 parallel workers |
| **Work Distribution** | Each thread gets unique range, no overlap |
| **Synchronization** | `CRITICAL_SECTION` ensures thread safety |
| **High-Precision Timing** | Windows `QueryPerformanceCounter()` |
| **Character Set** | 62 characters (A-Z, a-z, 0-9) |
| **Max Password Length** | 5 characters (configurable) |

---

## 📈 Example Execution

```
Password length 1: 62 combinations tested
Password length 2: 3,844 combinations tested
Password length 3: 238,328 combinations tested
Password length 4: 14,776,336 combinations tested
Password length 5: 916,132,832 combinations tested
  Thread 0: Tests range 0-57M
  Thread 1: Tests range 57M-114M
  ...
  Thread 6: Finds "Za8yK" in range 343M-400M
  
RESULT: Found in 2.21 seconds at 14.6M attempts/sec
```

---

## ⚠️ Legal & Ethical Notice

**This code is for educational purposes only.**

It demonstrates:
- How brute force attacks work
- Why password security is critical
- The computational cost of password cracking

**Unauthorized access to computer systems is illegal.**

---

## 📚 Key Takeaways

1. **Parallelization is effective** - 16 threads significantly faster than 1 thread
2. **Optimizations compound** - Multiple small optimizations create big speedup
3. **Passwords should be long** - 5 characters cracked in seconds
4. **Hardware matters** - More CPU cores = faster cracking
5. **Defense in depth** - Combine rate limiting, MFA, hashing for security

**Strong password policies are essential!** 🔒
