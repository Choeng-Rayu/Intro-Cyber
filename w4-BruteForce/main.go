package main

import (
	"fmt"
	"sort"
	"time"
)

func main() {
	fmt.Println("============================================================")
	fmt.Println("BRUTE FORCE PASSWORD ATTACK SYSTEM")
	fmt.Println("Target Password: Za8yK")
	fmt.Println("============================================================")
	fmt.Println()

	targetPassword := "Za8yK"

	// Character set: uppercase, lowercase, digits
	charSet := "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789"

	config := BruteForceConfig{
		TargetPassword: targetPassword,
		CharacterSet:   charSet,
		MaxLength:      5,
		NumWorkers:     4,
	}

	// Test different attack methods
	results := make(map[string]Result)

	// Method 1: Sequential Brute Force
	fmt.Println("[1/3] Sequential Brute Force Attack...")
	start := time.Now()
	results["Sequential"] = SequentialBruteForce(config)
	fmt.Printf("Time: %.4fs, Attempts: %d, Password: %s\n\n", time.Since(start).Seconds(), results["Sequential"].Attempts, results["Sequential"].Password)

	// Method 2: Parallel Brute Force
	fmt.Println("[2/3] Parallel Brute Force Attack (4 workers)...")
	start = time.Now()
	results["Parallel"] = ParallelBruteForce(config)
	fmt.Printf("Time: %.4fs, Attempts: %d, Password: %s\n\n", time.Since(start).Seconds(), results["Parallel"].Attempts, results["Parallel"].Password)

	// Method 3: Hybrid Attack (Dictionary + Brute Force)
	fmt.Println("[3/3] Hybrid Attack (Dictionary + Brute Force)...")
	dictionary := []string{
		"password", "123456", "admin", "letmein", "welcome",
		"Za8yK", "test123", "qwerty", "abc123", "Password1",
	}
	start = time.Now()
	results["Hybrid"] = HybridBruteForce(config, dictionary)
	fmt.Printf("Time: %.4fs, Attempts: %d, Password: %s\n\n", time.Since(start).Seconds(), results["Hybrid"].Attempts, results["Hybrid"].Password)

	// Summary and Comparison
	fmt.Println("============================================================")
	fmt.Println("COMPARISON RESULTS")
	fmt.Println("============================================================")
	fmt.Println()

	type methodResult struct {
		name     string
		result   Result
		attempts int64
		time     float64
	}

	var sortedResults []methodResult
	for name, res := range results {
		if res.Found {
			sortedResults = append(sortedResults, methodResult{
				name:     name,
				result:   res,
				attempts: res.Attempts,
				time:     res.TimeTaken.Seconds(),
			})
		}
	}

	// Sort by attempts (ascending)
	sort.Slice(sortedResults, func(i, j int) bool {
		return sortedResults[i].attempts < sortedResults[j].attempts
	})

	fmt.Printf("%-15s | %-10s | %-12s | %s\n", "Method", "Attempts", "Time (sec)", "Password")
	fmt.Println("----------|-----------|--------|----------")

	for _, mr := range sortedResults {
		fmt.Printf("%-15s | %-10d | %-12.6f | %s\n",
			mr.name, mr.attempts, mr.time, mr.result.Password)
	}

	fmt.Println()
	fmt.Println("============================================================")
	fmt.Println("SECURITY INSIGHTS")
	fmt.Println("============================================================")
	fmt.Println()
	fmt.Println("1. PASSWORD STRENGTH ANALYSIS:")
	fmt.Printf("   - Password: %s\n", targetPassword)
	fmt.Printf("   - Length: %d characters\n", len(targetPassword))
	fmt.Println("   - Character types: Uppercase (1), Lowercase (3), Digits (1)")
	fmt.Println()

	// Calculate search space
	searchSpace := 1
	for i := 0; i < 5; i++ {
		searchSpace *= len(charSet)
	}
	fmt.Printf("2. SEARCH SPACE: ~%d possible combinations\n", searchSpace)
	fmt.Println()

	fmt.Println("3. ATTACK EFFICIENCY:")
	if len(sortedResults) > 0 {
		fastest := sortedResults[0]
		fmt.Printf("   - Fastest Method: %s\n", fastest.name)
		fmt.Printf("   - Attempts Needed: %d\n", fastest.attempts)
		fmt.Printf("   - Time Taken: %.6f seconds\n", fastest.time)
		fmt.Printf("   - Average per attempt: %.9f ms\n", (fastest.time*1000)/float64(fastest.attempts))
	}
	fmt.Println()

	fmt.Println("4. RECOMMENDATIONS FOR STRONGER PASSWORDS:")
	fmt.Println("   - Use minimum 12-16 characters")
	fmt.Println("   - Mix uppercase, lowercase, numbers, and special characters")
	fmt.Println("   - Avoid dictionary words and common patterns")
	fmt.Println("   - Implement rate limiting on login attempts")
	fmt.Println("   - Use bcrypt/argon2 for password hashing (add computational cost)")
	fmt.Println()

	fmt.Println("============================================================")
}
