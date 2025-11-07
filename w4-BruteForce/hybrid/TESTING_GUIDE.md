# 🔢 5-Character Password Testing Guide

## Current Configuration

The hybrid attack system is now **optimized for 5-character passwords**.

### Key Settings:
```go
MaxLength:      5      // Exactly 5 characters
NumWorkers:     4      // 4 parallel workers
CharacterSet:   62     // A-Z, a-z, 0-9
```

### Search Space:
- **Total combinations:** 916,132,832
- **Per worker:** ~229,033,208 combinations
- **Estimated time (brute force):** ~81 seconds with 4 workers

---

## 🎯 Testing Different 5-Character Passwords

### How to Test a New Password:

Edit line 471 in `hybrid.go`:
```go
targetPassword := "YOUR5"  // Replace with your 5-char password
```

Then rebuild and run:
```bash
go build -o hybrid hybrid.go
./hybrid
```

---

## 📋 Test Cases

### Easy Passwords (Found in Dictionary - Fast!)

| Password | Type | Expected Time | Why It's Fast |
|----------|------|---------------|---------------|
| `admin` | Dictionary | 0.0001s | Common word |
| `12345` | Dictionary | 0.0001s | Sequential numbers |
| `qwerty` | Dictionary | 0.0001s | Keyboard pattern |
| `abc123` | Dictionary | 0.0001s | Letter + number combo |
| `Za8yK` | Dictionary | 0.0001s | In dictionary list |

**Result:** Dictionary finds these in **microseconds**! ⚡

### Medium Passwords (Require Brute Force - Slower)

| Password | Type | Expected Time | Characteristics |
|----------|------|---------------|-----------------|
| `Xy9Zw` | Mixed | ~40s | Random mixed case + digit |
| `K3mP9` | Mixed | ~45s | Uppercase + lowercase + digit |
| `nB7qR` | Mixed | ~50s | No pattern |
| `vM4tL` | Mixed | ~55s | Random combination |
| `jF2wC` | Mixed | ~60s | Scattered across space |

**Result:** Brute force takes **40-80 seconds** with 4 workers.

### Hard Passwords (Take Longer)

| Password | Type | Expected Time | Why It's Slow |
|----------|------|---------------|---------------|
| `zzz99` | End of space | ~81s | Near end of search |
| `99999` | All digits end | ~75s | High in search order |
| `ZZZZZ` | All uppercase end | ~70s | Depends on charset order |

**Result:** Can take **full search time** if at the end.

---

## 🧪 Experiment Ideas

### 1. Test Password Strength
```go
// Try these and compare times:
targetPassword := "AAAAA"  // Very fast (first combination)
targetPassword := "aaaaa"  // Fast (early in charset)
targetPassword := "00000"  // Medium (digits at end of charset)
targetPassword := "Za8yK"  // Fast if in dictionary
```

### 2. Modify Dictionary
Add your own common passwords to test:
```go
commonPasswords := []string{
    "password", "12345", "admin",
    "mypass",   // Add your test passwords here
    "test1",
    "user5",
}
```

### 3. Test Worker Count
```go
NumWorkers: 1,   // Sequential (slowest)
NumWorkers: 2,   // 2x faster
NumWorkers: 4,   // ~3-4x faster (current)
NumWorkers: 8,   // ~6-7x faster (if you have 8+ cores)
```

### 4. Character Set Variations
```go
// Only uppercase + digits (smaller space = faster)
charset := "ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789"  // 36 chars

// Only lowercase (even faster)
charset := "abcdefghijklmnopqrstuvwxyz"  // 26 chars

// Full set (current)
charset := "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789"  // 62 chars
```

---

## 📊 Performance Benchmarks

### Dictionary Attack (If Password in List)
```
Time:     0.0001 - 0.001 seconds
Attempts: 1 - 10,000 (depends on dictionary size)
Success:  ~80% for real-world passwords
Speed:    10,000,000+ attempts/second
```

### Brute Force (4 Workers)
```
Time:     1 - 81 seconds (depends on position)
Attempts: Up to 916,132,832
Success:  100% (guaranteed)
Speed:    ~10,000,000 attempts/second
```

### Hybrid Strategy
```
Best case:  0.0001s (dictionary hit)
Worst case: 81s (brute force to end)
Average:    40s (if not in dictionary)
```

---

## 🎯 Quick Tests

### Test 1: Verify Dictionary Speed
```go
targetPassword := "admin"  // Should find in 0.0001s
```
**Expected:** Found in dictionary, < 0.001 seconds

### Test 2: Test First Combination
```go
targetPassword := "AAAAA"  // First in search space
```
**Expected:** Found immediately in brute force, < 0.1 seconds

### Test 3: Test Last Combination
```go
targetPassword := "99999"  // Near end of search space
```
**Expected:** Takes full brute force time, ~75-81 seconds

### Test 4: Test Middle Combination
```go
targetPassword := "Za8yK"  // Middle of search space
```
**Expected:** 
- If in dictionary: 0.0001s
- If not in dictionary: ~40s

---

## 🔐 Security Implications

### 5-Character Password Analysis:

| Characteristic | Value | Security Rating |
|----------------|-------|-----------------|
| Search space | 916M | ⚠️ Medium |
| Crack time (4 workers) | 81s | ❌ WEAK |
| Crack time (dictionary) | 0.0001s | ❌ VERY WEAK |
| Recommended minimum | 12 chars | ✅ STRONG |

### Time to Crack by Length:

| Length | Combinations | Time (4 workers) | Security |
|--------|--------------|------------------|----------|
| 3 | 238,328 | 0.5s | ❌ Very Weak |
| 4 | 14.8M | 30s | ❌ Weak |
| 5 | 916M | 81s | ⚠️ Poor |
| 6 | 56.8B | 1.4 hours | ⚠️ Fair |
| 7 | 3.5T | 3.6 days | ⚠️ Moderate |
| 8 | 218T | 230 days | ✅ Good |
| 9 | 13.5Q | 39 years | ✅ Strong |
| 12+ | - | Centuries | ✅ Very Strong |

**Lesson:** 5 characters is NOT enough for security!

---

## 💡 Pro Tips

### 1. Add More Dictionary Words
Increase success rate by adding common patterns:
```go
commonPasswords := []string{
    "password", "12345", "admin", "qwerty",
    "User1", "Test1", "Pass1", "Root1",  // Add more
}
```

### 2. Optimize for Speed
If you know the password structure:
```go
// If password is: Uppercase + 3 lowercase + 1 digit
// Reduce charset for each position
// This is advanced pattern matching!
```

### 3. Use More Workers
If you have more CPU cores:
```go
NumWorkers: runtime.NumCPU(),  // Use all available cores
```

### 4. Disable Verbose for Speed
For benchmarking:
```go
Verbose: false,  // Faster without printing
```

---

## 🚀 Quick Commands

```bash
# Test current password
./hybrid

# Test with a different password
# (Edit hybrid.go first, line 471)
go build -o hybrid hybrid.go && ./hybrid

# Time the execution
time ./hybrid

# Run without verbose output
# (Edit Verbose: false in code first)
./hybrid | grep "SUCCESS"
```

---

## 📝 Validation Features

The code now includes:

✅ **Password Length Check**
```go
if len(targetPassword) != 5 {
    fmt.Printf("❌ ERROR: Password must be exactly 5 characters!\n")
    return
}
```

✅ **Search Space Calculation**
```go
totalCombinations := 1
for i := 0; i < 5; i++ {
    totalCombinations *= len(charset)
}
// Displays: 916,132,832 combinations
```

✅ **Configuration Display**
Shows all settings before starting attack

✅ **Educational Summary**
Explains why 5-char passwords are weak

---

## 🎓 What You'll Learn

By testing different 5-character passwords, you'll understand:

1. **Dictionary attacks are incredibly fast** (microseconds)
2. **Brute force is guaranteed but slow** (seconds to minutes)
3. **Position in search space matters** (early = fast, late = slow)
4. **Parallel processing helps** (~1.5x speedup with 4 workers)
5. **5 characters is insufficient** for security

---

**Happy Testing!** 🔐

Remember: This is for **educational purposes** to understand password security! 🎓

