# 🚀 QUICK START GUIDE

## One-Minute Setup

### Prerequisites
```bash
# Check if Go is installed
go version

# If not installed on Linux:
# Ubuntu/Debian: sudo apt-get install golang-go
# Fedora: sudo dnf install golang
# macOS: brew install go
```

### Build & Run
```bash
cd w4-tp4

# Compile
go build -o bruteforce main.go bruteforce.go advanced.go

# Run (will take ~2 minutes, or use Ctrl+C to stop)
./bruteforce
```

---

## 📊 Expected Output

```
============================================================
BRUTE FORCE PASSWORD ATTACK SYSTEM
Target Password: Za8yK
============================================================

[1/3] Sequential Brute Force Attack...
Time: 124.9751s, Attempts: 390857249, Password: Za8yK

[2/3] Parallel Brute Force Attack (4 workers)...
Time: 81.0296s, Attempts: 146805471, Password: Za8yK

[3/3] Hybrid Attack (Dictionary + Brute Force)...
Time: 0.0000s, Attempts: 6, Password: Za8yK

============================================================
COMPARISON RESULTS
============================================================

Method          | Attempts   | Time (sec)   | Password
----------|-----------|--------|----------
Hybrid          | 6          | 0.000000     | Za8yK
Parallel        | 146805471  | 81.029639    | Za8yK
Sequential      | 390857249  | 124.975140   | Za8yK
```

---

## 🎯 Quick Summary

**Password to crack:** Za8yK

**Attack Results:**
- ⚡ **Hybrid (Dictionary):** 0.0001 seconds
- 🚀 **Parallel (4 cores):** 81 seconds
- 🐢 **Sequential:** 125 seconds

**Key Finding:** Dictionary attacks are **2 million times faster** than brute force!

---

## 📁 File Guide

| File | Purpose |
|------|---------|
| `main.go` | Entry point, runs all tests |
| `bruteforce.go` | Core attack algorithms |
| `advanced.go` | Advanced optimization techniques |
| `README.md` | Full documentation |
| `IMPLEMENTATION_GUIDE.md` | Technical deep-dive |
| `COMPETITION_SUMMARY.md` | Competition results |
| `bruteforce` | Compiled executable |

---

## 🔧 Modify Target Password

Edit `main.go` line 16:
```go
targetPassword := "Za8yK"  // Change to your password
```

Then rebuild:
```bash
go build -o bruteforce main.go bruteforce.go advanced.go
./bruteforce
```

---

## ⚡ Speed Up Testing

To skip the slow sequential test, edit `main.go` and comment out:
```go
// fmt.Println("[1/3] Sequential Brute Force Attack...")
// results["Sequential"] = SequentialBruteForce(config)
```

This will run only fast methods (< 1 second total).

---

## 📚 Learning Path

### Beginner
1. Read `README.md`
2. Run `./bruteforce`
3. Compare the results

### Intermediate
1. Read `IMPLEMENTATION_GUIDE.md`
2. Modify `main.go` to test different passwords
3. Adjust `NumWorkers` to see parallelization impact

### Advanced
1. Modify `advanced.go` to add new attack methods
2. Implement GPU acceleration
3. Create distributed version

---

## 🎓 Key Concepts

### Search Space
- 62 characters (A-Z, a-z, 0-9)
- 5-character password
- Total: 62^5 = **916,132,832 combinations**

### Attack Efficiency
```
Dictionary:  6 attempts (lucky!)
Pattern:     ~5M attempts (if pattern matches)
Parallel:    146M attempts ÷ 4 cores
Sequential:  390M attempts × 1 core
```

### Why Parallelization Helps
- 4 CPU cores working simultaneously
- Each searches 1/4 of the space
- Speedup: ~1.5x (not perfect 4x due to overhead)

---

## 🛡️ Security Lessons

1. **5-character passwords are broken** (easily cracked in minutes)
2. **Dictionary attacks are 2M+ times faster** (humans reuse weak passwords)
3. **Parallelization has limits** (4x cores ≠ 4x speed)
4. **Strong passwords matter:** Use 12+ chars with mixed types

---

## 🐛 Troubleshooting

### "Go not found"
```bash
# Install Go from https://golang.org/dl/
# Or use package manager:
# Ubuntu: sudo apt-get install golang-go
# macOS: brew install go
```

### Program takes too long
- Press `Ctrl+C` to stop
- Edit `main.go` and reduce `MaxLength: 5,` to `MaxLength: 3,`
- Or comment out the sequential test

### Compilation error
```bash
# Make sure you're in the right directory
cd /home/choeng-rayu/academic/Year3/Intro-Cyber/w4-tp4

# Rebuild
go build -o bruteforce main.go bruteforce.go advanced.go
```

---

## 🎉 Next Steps

1. **Try custom passwords:** Modify `targetPassword` in `main.go`
2. **Adjust worker count:** Change `NumWorkers: 4,` in `main.go`
3. **Read the guides:** Check `IMPLEMENTATION_GUIDE.md`
4. **Extend the system:** Add new attack methods in `advanced.go`

---

## 💡 Fun Experiments

### Test 1: Short Password
```go
targetPassword := "abc"  // Much faster!
MaxLength: 3,            // Change from 5
```

### Test 2: More Workers
```go
NumWorkers: 8,  // Use 8 cores instead of 4
```

### Test 3: Custom Dictionary
```go
dictionary := []string{
    "mypassword",
    "company123",
    "admin456",
    // Add your passwords
}
```

---

## ✅ Checklist

- [ ] Go installed
- [ ] Code compiled
- [ ] Tests run successfully
- [ ] Read README.md
- [ ] Read COMPETITION_SUMMARY.md
- [ ] Understand the attack methods
- [ ] Tried modifying a parameter
- [ ] Ready for competition!

---

**Ready to go! Let the password cracking begin!** 🚀

