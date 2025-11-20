# Brute Force Password Attack System - Educational Project

## Overview
This is an educational project to understand how attackers crack passwords using brute force techniques. The system demonstrates **3 different programming language implementations** for cracking a 5-character password: **Za8yK**

Implementations include:
- **C** - Multi-threaded with Windows API (fastest)
- **C++** - Single-threaded for compatibility
- **Go** - Multi-threaded goroutines

## 🎯 Implementation Strategies

### 1. **C Implementation** (Multi-threaded - Windows) ⚡ **FASTEST**
- **Language:** C with Windows API threading
- **Threads:** 16 parallel workers
- **Target Password:** Za8yK
- **Attempts:** 32,288,867
- **Time:** 2.21 seconds
- **Speed:** 14,606,980 attempts/second
- **Key Optimizations:**
  - Windows `CreateThread()` for parallelization
  - Critical sections for thread synchronization
  - Number-to-password conversion with loop unrolling
  - Early exit on first character mismatch
  - Batch checking of stop flag (every 1000 iterations)

**How it works:**
```c
// Divide search space among 16 worker threads
for each worker thread:
  - Assign unique range of combinations
  - Convert numbers to password strings
  - Compare with target password
  - Signal other threads when found
  - Use critical section to avoid race conditions
```

**File:** `C/c.c`

---

### 2. **C++ Implementation** (Single-threaded)
- **Language:** C++ with STL
- **Threading:** Single-threaded (for broad compatibility)
- **Target Password:** Za8yK
- **Attempts:** 375,838,679
- **Time:** 2.77 seconds
- **Speed:** 135,697,460 attempts/second
- **Key Optimizations:**
  - Char arrays instead of std::string (faster)
  - `memcmp()` for fast password comparison
  - Index-based candidate generation
  - Base-N number increment algorithm

**How it works:**
```cpp
// Index-based approach: treat password as base-62 number
int indices[PASSWORD_LENGTH] = {0, 0, 0, 0, 0};

while not found:
  - Build candidate from ALPHABET[indices[i]]
  - Compare with target
  - Increment indices like base-62 counter
```

**File:** `C++/bruteForce.cpp`

---

### 3. **Go Implementation** (Multi-goroutine)
- **Language:** Go with concurrency primitives
- **Goroutines:** Multiple concurrent workers
- **Key Optimizations:**
  - Goroutine work distribution
  - Channel-based communication
  - Built-in race condition detection

**File:** `hybrid/hybrid.go` (and related files)

---

## 📊 Performance Comparison

| Language | Threads | Attempts | Time (sec) | Speed (attempts/sec) | Notes |
|----------|---------|----------|-----------|----------------------|-------|
| **C**    | 16      | 32.3M    | 2.21      | 14.6M                | **Windows API**, Fastest |
| **C++**  | 1       | 375.8M   | 2.77      | 135.7M               | Single-threaded, Standard library |
| **Go**   | Multiple| -        | -         | -                    | Goroutine-based |

---

## 🔍 How the C Implementation Works

### Data Structures
```c
// Configuration for attack
typedef struct {
    const char *target_password;    // Password to crack
    const char *charset;             // A-Z, a-z, 0-9
    int charset_len;                 // 62
    int max_length;                  // 5
    int num_workers;                 // 16
    bool verbose;
} Config;

// Arguments for each worker thread
typedef struct {
    Config *config;
    int worker_id;                   // Thread ID (0-15)
    int64_t start_num;              // Starting combination number
    int64_t end_num;                // Ending combination number
    int length;                      // Current password length (1-5)
    AttackResult *result;
    volatile bool *stop_flag;       // Signal all threads to stop
} WorkerArgs;
```

### Main Algorithm Flow

1. **Initialization Phase**
   ```
   1. Create CRITICAL_SECTION for thread synchronization
   2. Calculate total combinations: 62^5 = 916,132,832
   3. Allocate work per thread: 916,132,832 / 16 ≈ 57 million each
   ```

2. **Parallel Attack Loop**
   ```
   For each password length (1 to 5):
     - Create 16 worker threads
     - Each thread gets unique number range
     - Threads convert numbers to passwords
     - Compare passwords in parallel
     - First thread to find password signals stop
   ```

3. **Worker Thread Operation**
   ```c
   for (int64_t num = start_num; num < end_num; num++) {
       // Check stop flag every 1000 iterations (optimization)
       if (num % 1000 == 0 && stop_flag) break;
       
       // Convert number to password string
       number_to_password(charset, charset_len, num, length, password);
       attempts++;
       
       // Fast early exit: check first character
       if (password[0] != target[0]) continue;
       
       // Full comparison for match
       if (password_matches(password, target, length)) {
           // Found! Enter critical section and signal others
           EnterCriticalSection(&result_mutex);
           if (!password_found) {
               password_found = true;
               *stop_flag = true;
               strcpy(result->password, password);
           }
           LeaveCriticalSection(&result_mutex);
           break;
       }
   }
   ```

### Key Optimizations in C Code

1. **Number-to-Password Conversion** (Loop Unrolling)
   ```c
   // Instead of generic loop, use optimized switch for common lengths
   switch (length) {
       case 5:
           password[4] = charset[num % 62]; num /= 62;
           password[3] = charset[num % 62]; num /= 62;
           password[2] = charset[num % 62]; num /= 62;
           password[1] = charset[num % 62]; num /= 62;
           password[0] = charset[num % 62];
           break;
       // ... other cases ...
   }
   ```

2. **Fast Password Matching** (Char-by-char comparison)
   ```c
   case 5:
       return password[0] == target[0] &&
              password[1] == target[1] &&
              password[2] == target[2] &&
              password[3] == target[3] &&
              password[4] == target[4];
   ```

3. **Stop Flag Batching**
   ```c
   // Check stop flag every 1000 iterations, not every iteration
   // Reduces cache coherency overhead significantly
   const int64_t check_interval = 1000;
   if (num >= next_check) {
       if (*stop_flag) break;
       next_check += check_interval;
   }
   ```

---

## 🔐 Search Space Analysis

### Brute Force Complexity
```
Character Set: A-Z, a-z, 0-9 = 62 characters
Password Length: 5 characters
Total Possibilities: 62^5 = 916,132,832 combinations

Search time with C implementation (14.6M attempts/sec):
916,132,832 / 14,600,000 ≈ 62.7 seconds (worst case)
Average case: ~31 seconds
Found case (Za8yK): 2.21 seconds
```

### Password Strength Analysis
```
Password: Za8yK
- Length: 5 characters (❌ TOO SHORT - recommend 12-16)
- Uppercase: 1 (Z) ✓
- Lowercase: 3 (a, y, K) ✓  
- Numbers: 1 (8) ✓
- Special chars: 0 (❌ Should have !@#$%^&*)
- Entropy: log2(62^5) ≈ 29.6 bits (weak)
```

---

## 💻 Building & Running

### C Implementation (Windows)
```bash
cd C/
gcc -O3 -march=native c.c -o c.exe
.\c.exe
```

**Options:**
```bash
# With custom target password and worker count
.\c.exe "MyPassword" 8
```

---

### C++ Implementation
```bash
cd C++/
g++ -std=c++11 bruteForce.cpp -o bruteforce.exe
.\bruteforce.exe
```

---

### Performance Tips
1. **Use Release Build:** `-O3` optimization flag
2. **CPU Affinity:** Pin threads to specific CPU cores for better cache performance
3. **Larger Passwords:** The multi-threaded C version shows benefits with longer passwords

---

## 🛡️ Security Recommendations

### To Prevent Brute Force Attacks:

1. **Strong Passwords (12+ characters)**
   - UPPERCASE + lowercase + numbers + !@#$%^&*
   - Avoid dictionary words or patterns

2. **Rate Limiting**
   - Max 5 login attempts per 5 minutes
   - Progressive delays: 1s, 5s, 30s, 1h
   - Account lockout after max attempts

3. **Password Hashing**
   - Use `bcrypt` or `argon2` (adds computational cost)
   - Salting prevents rainbow table attacks
   - Makes each hash attempt expensive

4. **Multi-Factor Authentication (MFA)**
   - Even if password cracked, need 2FA
   - SMS, TOTP, hardware keys
   - Backup codes for recovery

5. **Detection Systems**
   - Monitor failed login attempts
   - Alert on suspicious patterns
   - IP-based blocking for repeated failures

---

## 📁 File Structure

```
w4-BruteForce/
├── C/
│   ├── c.c                  # Multi-threaded C implementation
│   ├── c.exe                # Compiled executable
│   └── README.md            # C implementation notes
├── C++/
│   ├── bruteForce.cpp       # Single-threaded C++ implementation
│   ├── bruteforce.exe       # Compiled executable
│   └── [spec files]         # PyInstaller specs (if needed)
├── hybrid/
│   ├── hybrid.go            # Go implementation
│   └── [supporting files]
└── README.md                # This file
```

---

## 🔬 Technical Details

### Thread Synchronization in C
```c
// Critical section prevents race conditions
CRITICAL_SECTION result_mutex;

EnterCriticalSection(&result_mutex);
{
    if (!password_found) {
        password_found = true;      // Only first thread succeeds
        strcpy(result->password, password);
    }
}
LeaveCriticalSection(&result_mutex);
```

### High-Resolution Timing
```c
// Windows API for accurate measurement
LARGE_INTEGER frequency, counter;
QueryPerformanceFrequency(&frequency);
QueryPerformanceCounter(&counter);
double time_seconds = (double)counter.QuadPart / frequency.QuadPart;
```

---

## 📈 Performance Analysis

### Time Complexity
- **Sequential:** O(n × base^n) where base=62, n≤5
- **Parallel (k threads):** O((n × base^n) / k)
- **C Implementation (16 threads):** ~O((5 × 62^5) / 16)

### Space Complexity
- **Per thread:** O(n) for password buffer + O(log n) for recursion
- **Total:** O(k × n) where k=number of threads

### Cache Efficiency
- Loop unrolling reduces instruction cache misses
- Batch stop-flag checking reduces cache coherency traffic
- First-character mismatch eliminates unnecessary comparisons

---

## 🎓 Educational Value

This project teaches:

1. **Low-Level Optimization**
   - Loop unrolling and inlining
   - Cache locality and CPU efficiency
   - Binary exponentiation for fast power calculation

2. **Parallel Programming**
   - Windows threading API
   - Critical sections and synchronization
   - Work distribution across threads

3. **Cybersecurity**
   - Brute force attack mechanics
   - Password strength analysis
   - Computational cost of cracking

4. **Performance Engineering**
   - Profiling and benchmarking
   - Identifying bottlenecks
   - Hardware-aware optimization

---

## ⚠️ Ethical & Legal Notice

**This code is for educational purposes only.**

It demonstrates:
- How brute force attacks work
- Why password security matters
- How to defend against attacks

**Unauthorized access to computer systems is illegal** under laws like:
- Computer Fraud and Abuse Act (USA)
- Computer Misuse Act (UK)
- Similar laws in your jurisdiction

---

## 🚀 Future Enhancements

1. **GPU Acceleration** - CUDA/OpenCL for massive parallelism
2. **Dictionary Attack** - Pre-computed common passwords
3. **Hybrid Approach** - Dictionary → Brute Force fallback
4. **Custom Character Sets** - Optimize for known patterns
5. **Distributed Attack** - Network-based multi-machine cracking
6. **Rule-based Mutations** - Common transformations (leet speak, etc.)

---

## 📚 References

- Password Hashing: https://en.wikipedia.org/wiki/Bcrypt
- OWASP Password Cracking: https://owasp.org/www-community/attacks/Password_Cracking
- Windows Threading: https://docs.microsoft.com/en-us/windows/win32/procthread/about-processes-and-threads
- Go Concurrency: https://golang.org/doc/effective_go#concurrency

---

**Remember:** Building secure systems requires understanding attack mechanisms! 🔒
