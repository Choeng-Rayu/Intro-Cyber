# Brute Force Password Attack System - Educational Project

## Overview
This is an educational project to understand how hackers attempt to crack passwords using various brute force attack techniques. The system demonstrates **3 different attack strategies** implemented in Go for cracking a 5-character password: **Za8yK**

## 🎯 Attack Strategies

### 1. **Sequential Brute Force** (Naive Approach)
- **Attempts:** 390,857,249
- **Time:** 124.98 seconds
- **How it works:** Systematically tries every possible combination one by one
- **Pros:** Simple to understand
- **Cons:** Very slow, single-threaded

**Code Logic:**
```
For each password length (1 to 5):
  For each possible combination:
    Check if it matches target password
```

### 2. **Parallel Brute Force** (Multi-threaded Approach)
- **Attempts:** 146,805,471
- **Time:** 81.03 seconds
- **Workers:** 4 concurrent goroutines
- **Speed Improvement:** ~54% faster than sequential
- **How it works:** Distributes the search space across multiple CPU cores

**Key Optimization:**
- Divides search space into chunks
- Each worker processes its chunk independently
- Synchronizes when password is found

### 3. **Hybrid Attack** (Dictionary + Brute Force) ⚡
- **Attempts:** 6
- **Time:** 0.0001 seconds
- **Speed Improvement:** **2 million times faster!**
- **How it works:** 
  1. First tries common passwords from a dictionary
  2. If not found, falls back to brute force
  3. Password was in dictionary, so it found instantly

**Why it's so effective:**
```
Most passwords are either:
1. Dictionary words
2. Common patterns (Password1, admin123, etc.)
3. Previously leaked passwords
```

## 📊 Performance Comparison

| Method     | Attempts      | Time (sec) | Why it works |
|-----------|---------------|-----------|------------|
| Hybrid    | 6             | 0.0001    | Found in dictionary |
| Parallel  | 146,805,471   | 81.03     | Multi-threaded search |
| Sequential| 390,857,249   | 124.98    | Single-threaded search |

## 🔐 Key Findings

### Search Space Analysis
- **Character Set:** A-Z, a-z, 0-9 = 62 characters
- **Password Length:** 5 characters
- **Total Possibilities:** 62^5 = **916,132,832 combinations**

### Password Strength
- **Given Password:** Za8yK
  - Length: 5 characters (❌ Too short)
  - Uppercase: 1 character ✓
  - Lowercase: 3 characters ✓
  - Digits: 1 character ✓
  - Special chars: 0 ❌

## 🛡️ Security Recommendations

### To Prevent Brute Force Attacks:

1. **Strong Password Requirements**
   - Minimum 12-16 characters (not 5!)
   - Mix: UPPERCASE + lowercase + numbers + !@#$%^&*

2. **Rate Limiting**
   - Limit login attempts (e.g., 5 attempts per 5 minutes)
   - Progressive delays or account lockout

3. **Password Hashing**
   - Use **bcrypt** or **argon2** (adds computational cost)
   - Never store plain passwords
   - One failed attempt = expensive hash computation

4. **Multi-Factor Authentication (MFA)**
   - Even if password is cracked, still need 2FA code
   - SMS, authenticator apps, hardware keys

5. **Dictionary Protection**
   - Avoid common words in passwords
   - Use password managers (LastPass, 1Password, Bitwarden)

## 💻 Building & Running

### Prerequisites
- Go 1.13+ installed

### Build
```bash
cd w4-tp4
go build -o bruteforce main.go bruteforce.go
```

### Run
```bash
./bruteforce
```

### Expected Output
```
BRUTE FORCE PASSWORD ATTACK SYSTEM
Target Password: Za8yK

[1/3] Sequential Brute Force Attack...
[2/3] Parallel Brute Force Attack (4 workers)...
[3/3] Hybrid Attack (Dictionary + Brute Force)...

COMPARISON RESULTS
...
```

## 📁 File Structure

```
w4-tp4/
├── main.go          # Entry point with test scenarios
├── bruteforce.go    # Core attack algorithms
└── README.md        # This file
```

## 🔬 Attack Algorithm Details

### Sequential Attack
```go
func SequentialBruteForce(config) Result {
    for length := 1 to maxLength {
        for each combination of length {
            if candidate == target {
                return found
            }
        }
    }
}
```

### Parallel Attack
```go
func ParallelBruteForce(config) Result {
    for length := 1 to maxLength {
        // Divide work into chunks
        chunkSize := totalCombinations / numWorkers
        
        // Launch multiple goroutines
        for worker := 0 to numWorkers {
            go worker.search(chunk)
        }
        
        // Wait for any worker to find password
    }
}
```

### Hybrid Attack
```go
func HybridBruteForce(dictionary) Result {
    // Fast path: check dictionary
    for pwd in dictionary {
        if pwd == target {
            return found (very fast!)
        }
    }
    
    // Slow path: brute force if not found
    return BruteForce()
}
```

## 📈 Performance Analysis

### Time Complexity
- **Sequential:** O(base^n) where base=62, n=5
- **Parallel:** O(base^n / k) where k=number of workers
- **Hybrid (if in dictionary):** O(dictionary_size)

### Space Complexity
- **Sequential:** O(n) for storing current combination
- **Parallel:** O(n × k) for k worker contexts
- **Hybrid:** O(dictionary_size)

## 🎓 Educational Value

This project teaches:

1. **Algorithm Design**
   - Sequential vs parallel approaches
   - Optimization techniques

2. **Go Concurrency**
   - Goroutines for parallel processing
   - WaitGroups for synchronization
   - Channels for communication

3. **Cybersecurity Concepts**
   - Password strength analysis
   - Attack vectors
   - Defense mechanisms

4. **Performance Engineering**
   - Benchmarking different approaches
   - CPU utilization optimization
   - Time/space tradeoffs

## ⚠️ Ethical Notice

This code is **for educational purposes only**. It demonstrates:
- How hackers attempt unauthorized access
- Why strong passwords matter
- How to protect systems

**Unauthorized access to computer systems is illegal.**

## 🚀 Next Steps / Enhancements

1. **GPU Acceleration** - Use CUDA for massive parallelism
2. **Rainbow Tables** - Pre-computed hash values
3. **Rule-based Cracking** - Add patterns like "Capital + 4 lowercase"
4. **Distributed Attack** - Use multiple machines
5. **Custom Character Sets** - Optimize for known password patterns

## 📚 References

- Go Concurrency: https://golang.org/doc/effective_go#concurrency
- Password Security: https://owasp.org/www-community/attacks/Password_Cracking
- Bcrypt: https://en.wikipedia.org/wiki/Bcrypt

---

**Competition Purpose:** Understanding attack mechanisms helps build better defenses! 🔒
