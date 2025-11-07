# 🔐 HYBRID ATTACK METHOD - Easy Guide

## What is the Hybrid Attack?

The **Hybrid Attack** combines TWO powerful strategies:
1. **Dictionary Attack** (Fast - tries common passwords)
2. **Brute Force Attack** (Slow but thorough - tries every combination)

Think of it like this:
- **Dictionary Attack** = Trying the most common keys first (quick!)
- **Brute Force Attack** = Trying every possible key (guaranteed but slow)

---

## 🎯 How It Works (Step by Step)

### Step 1: Dictionary Attack (0.0001 seconds)
```
Try these first:
├─ "password"     ❌ No match
├─ "123456"       ❌ No match
├─ "admin"        ❌ No match
├─ ...
├─ "Za8yK"        ✅ FOUND IT!
└─ Time: 0.0001 seconds
```

**Why this works:**
- 80% of people use weak, common passwords
- We check thousands of common passwords instantly
- If the password is common, we find it IMMEDIATELY!

### Step 2: Brute Force (if dictionary fails)
```
Dictionary failed? Try EVERYTHING:
├─ Length 1: A, B, C, ... Z, a, b, ... 9
├─ Length 2: AA, AB, AC, ... 99
├─ Length 3: AAA, AAB, ... 999
├─ Length 4: AAAA, AAAB, ... 9999
└─ Length 5: AAAAA, ... Za8yK ✅ FOUND!
```

**Why this works:**
- Tries EVERY possible combination
- WILL find any password (guaranteed!)
- But can be VERY slow for long passwords

---

## 📊 Real Results

### Testing Password: "Za8yK"

| Phase | Method | Result | Time | Attempts |
|-------|--------|--------|------|----------|
| 1 | Dictionary | ✅ Found! | 0.0001s | 21 |
| 2 | Brute Force | (skipped) | - | - |

**Total Time:** 0.0001 seconds (instant!)

---

## 💡 Why Hybrid is the BEST Strategy

### Scenario 1: Common Password
```
Password: "password123"
├─ Dictionary tries: 5 attempts
├─ Time: 0.0001 seconds
└─ Result: ✅ FOUND (super fast!)
```

### Scenario 2: Random Password
```
Password: "xK9mP"
├─ Dictionary tries: 10,000 attempts (not found)
├─ Brute Force tries: 500,000 attempts
├─ Time: 2.5 seconds
└─ Result: ✅ FOUND (slower but still works!)
```

### Scenario 3: Strong Password
```
Password: "aB3$dE7&iJ"
├─ Dictionary tries: 10,000 attempts (not found)
├─ Brute Force tries: Would take YEARS!
├─ Time: Too long!
└─ Result: ❌ This is a GOOD password!
```

---

## 🚀 Performance Comparison

```
Single-threaded Brute Force:    125 seconds
Parallel Brute Force (4 cores):  81 seconds  (1.5× faster)
Dictionary Attack:               0.0001s     (1,250,000× faster!)
Hybrid Attack:                   Best of both! ✨
```

---

## 📖 Code Structure (Easy to Understand)

### 1. Dictionary Attack Function
```go
func DictionaryAttack(config) {
    // Try each common password
    for password in dictionary {
        if password == target {
            return FOUND! // Success!
        }
    }
    return NOT_FOUND // Continue to brute force
}
```

### 2. Brute Force Function
```go
func BruteForceAttack(config) {
    // Try all combinations
    for length = 1 to MaxLength {
        for combination in allPossibleCombinations(length) {
            if combination == target {
                return FOUND!
            }
        }
    }
}
```

### 3. Hybrid Function (Combines Both)
```go
func HybridAttack(config) {
    // Phase 1: Try dictionary first
    result = DictionaryAttack(config)
    if result.Found {
        return result  // Fast win!
    }
    
    // Phase 2: Dictionary failed, use brute force
    result = BruteForceAttack(config)
    return result  // Guaranteed to find it
}
```

---

## 🎮 How to Use

### Build the Program
```bash
cd w4-tp4/hybrid
go build -o hybrid hybrid.go
```

### Run It
```bash
./hybrid
```

### Modify the Target Password
Edit `hybrid.go` line 523:
```go
targetPassword := "Za8yK"  // Change this!
```

### Modify the Dictionary
Edit `hybrid.go` line 526-534:
```go
commonPasswords := []string{
    "password",
    "123456",
    "YourPassword",  // Add your passwords here
}
```

---

## 🔬 Understanding the Code

### Main Components:

1. **AttackResult** - Stores the result
   ```go
   type AttackResult struct {
       Password  string  // The password we found
       Found     bool    // Did we find it?
       Attempts  int64   // How many tries?
       TimeTaken time.Duration  // How long?
       Method    string  // Which method worked?
   }
   ```

2. **HybridConfig** - Settings for the attack
   ```go
   type HybridConfig struct {
       TargetPassword string   // Password to crack
       Dictionary     []string // Common passwords
       CharacterSet   string   // All possible chars
       MaxLength      int      // Max password length
       NumWorkers     int      // Parallel workers
       Verbose        bool     // Show progress?
   }
   ```

3. **Flow Diagram**
   ```
   START
     ↓
   Dictionary Attack
     ↓
   Found? ──YES──→ DONE! (Fast)
     ↓
    NO
     ↓
   Brute Force Attack (Parallel)
     ↓
   Found? ──YES──→ DONE! (Slow)
     ↓
    NO
     ↓
   NOT FOUND (password too long)
   ```

---

## 🎓 Key Concepts

### 1. Search Space
```
Characters: 62 (A-Z, a-z, 0-9)
Length: 5
Total combinations: 62^5 = 916,132,832

That's why brute force is slow!
```

### 2. Dictionary Size vs Speed
```
Small dictionary (100 passwords):   Very fast, low success
Medium dictionary (10,000):         Fast, good success
Large dictionary (1,000,000):       Slower, high success

Our example: 26 passwords (for demo)
```

### 3. Parallel Processing
```
1 worker:  100% of work
2 workers: 50% each  = ~2× faster
4 workers: 25% each  = ~3.5× faster (overhead exists)
8 workers: 12.5% each = ~6× faster
```

---

## 🛡️ Security Lessons

### Weak Password (Easy to Crack)
```
Password: "password123"
✗ In dictionary
✗ Only 11 characters
✗ Common pattern
Result: Cracked in 0.0001 seconds
```

### Medium Password (Harder)
```
Password: "Za8yK"
✗ Only 5 characters
✓ Mixed case
✓ Has numbers
Result: Cracked in 0.0001s (in dictionary)
          or 81s (brute force)
```

### Strong Password (Very Hard)
```
Password: "mK9#pL2$vN8@qR4!"
✓ 17 characters
✓ Mixed case
✓ Numbers
✓ Special characters
✓ Not in dictionary
Result: Would take YEARS to crack!
```

---

## 📝 Quick Summary

### What Makes Hybrid Attack Powerful?

✅ **Fast for common passwords** (dictionary)
✅ **Guaranteed to find any password** (brute force)
✅ **Uses parallel processing** (faster)
✅ **Practical for real-world use** (combines strengths)

### When to Use Each Method?

| Method | Best For | Speed | Success Rate |
|--------|----------|-------|--------------|
| Dictionary | Common passwords | ⚡⚡⚡ | ~80% |
| Brute Force | Any password | 🐢 | 100% |
| Hybrid | **Everything!** | ⚡⚡⚡ or 🐢 | 100% |

---

## 🎯 Test Yourself

Try modifying the code to crack these passwords:

### Easy (will use dictionary)
```go
targetPassword := "admin123"
```

### Medium (will use brute force)
```go
targetPassword := "aB3cD"
```

### Hard (will take a while)
```go
targetPassword := "xY9zW"
MaxLength := 6  // Increase this
```

---

## 🚀 Next Steps

1. **Run the program** and see how fast it is
2. **Change the target password** to test different scenarios
3. **Add more passwords** to the dictionary
4. **Increase NumWorkers** to use more CPU cores
5. **Read the code comments** to understand each part

---

## 💻 Expected Output

```
=======================================================================
HYBRID ATTACK - COMBINATION OF DICTIONARY + BRUTE FORCE
=======================================================================

Target Password: Za8yK
Dictionary Size: 26 passwords
Max Length: 5 characters
Workers: 4

[STEP 1] Starting Dictionary Attack...
Checking 26 common passwords...
  ✓ FOUND! Password is: Za8yK
  Attempts: 21
  Time: 0.000053 seconds

=======================================================================
SUCCESS! Password found using Dictionary Attack!
=======================================================================
Password: Za8yK
Attempts: 21
Time: 0.000160 seconds

📚 WHAT YOU LEARNED:
1. Dictionary attacks are VERY fast for common passwords
2. Brute force attacks are slow but WILL find any password
3. Hybrid attacks combine the best of both methods
4. Parallel processing makes brute force much faster
5. Strong passwords (12+ chars, mixed types) are MUCH harder to crack!
```

---

**You're now ready to understand and use the Hybrid Attack method!** 🎉

