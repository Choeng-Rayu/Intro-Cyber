package main

import (
	"fmt"
	"sync"
	"time"
)

// OptimizedBruteForce uses smarter character ordering for faster cracking
func OptimizedBruteForce(config BruteForceConfig) Result {
	start := time.Now()

	// Reorder character set by frequency in passwords
	// Numbers and common letters first
	optimizedCharset := "0123456789aeioustnrlydcmghbfpvkwxjzAEIOUSTNRLYDCMGHBFPVKWXJZ"
	config.CharacterSet = optimizedCharset

	result := SequentialBruteForce(config)
	result.TimeTaken = time.Since(start)
	return result
}

// MaskBruteForce attempts attacks with known patterns
// E.g., if we know password is: Uppercase + lowercase + digit + lowercase + digit
func MaskBruteForce(config BruteForceConfig) Result {
	start := time.Now()
	attempts := int64(0)

	uppercase := "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
	lowercase := "abcdefghijklmnopqrstuvwxyz"
	digits := "0123456789"

	// Pattern analysis: Try common password structures
	patterns := []struct {
		name  string
		masks []string
	}{
		{
			name:  "Digit + Uppercase + 3 Lowercase",
			masks: []string{digits, uppercase, lowercase, lowercase, lowercase},
		},
		{
			name:  "Uppercase + 3 Lowercase + Digit",
			masks: []string{uppercase, lowercase, lowercase, lowercase, digits},
		},
		{
			name:  "2 Uppercase + 3 Lowercase",
			masks: []string{uppercase, uppercase, lowercase, lowercase, lowercase},
		},
	}

	for _, pattern := range patterns {
		found, pwd, att := tryMaskedCombinations(pattern.masks, config.TargetPassword)
		attempts += int64(att)

		if found {
			return Result{
				Password:  pwd,
				Found:     true,
				Attempts:  attempts,
				TimeTaken: time.Since(start),
			}
		}
	}

	return Result{Found: false, Attempts: attempts, TimeTaken: time.Since(start)}
}

// tryMaskedCombinations tries combinations following a mask pattern
func tryMaskedCombinations(masks []string, target string) (bool, string, int64) {
	attempts := int64(0)
	length := len(masks)
	indices := make([]int, length)

	for {
		candidate := ""
		valid := true
		for i, idx := range indices {
			if idx >= len(masks[i]) {
				valid = false
				break
			}
			candidate += string(masks[i][idx])
		}

		if !valid {
			break
		}

		attempts++
		if candidate == target {
			return true, candidate, attempts
		}

		// Increment indices
		carry := 1
		for i := length - 1; i >= 0 && carry > 0; i-- {
			indices[i] += carry
			if indices[i] >= len(masks[i]) {
				indices[i] = 0
			} else {
				carry = 0
			}
		}

		if carry > 0 {
			break
		}
	}

	return false, "", attempts
}

// RainbowTableAttack simulates using pre-computed hash tables
func RainbowTableAttack(config BruteForceConfig, rainbowTable map[string]bool) Result {
	start := time.Now()
	attempts := int64(0)

	for hash := range rainbowTable {
		attempts++
		if hash == config.TargetPassword {
			return Result{
				Password:  hash,
				Found:     true,
				Attempts:  attempts,
				TimeTaken: time.Since(start),
			}
		}
	}

	return Result{
		Found:     false,
		Attempts:  attempts,
		TimeTaken: time.Since(start),
	}
}

// AdaptiveParallelBruteForce dynamically adjusts worker count
func AdaptiveParallelBruteForce(config BruteForceConfig) Result {
	start := time.Now()
	resultChan := make(chan Result, 1)
	var wg sync.WaitGroup
	totalAttempts := int64(0)
	var mu sync.Mutex

	for length := 1; length <= config.MaxLength; length++ {
		// Calculate search space for this length
		divisor := int64(1)
		for i := 0; i < length; i++ {
			divisor *= int64(len(config.CharacterSet))
		}

		// Dynamic worker count based on search space
		workers := config.NumWorkers
		if divisor < 100000 {
			workers = 1 // Single thread for small space
		} else if divisor < 1000000 {
			workers = 2
		}

		chunkSize := (divisor + int64(workers) - 1) / int64(workers)

		for worker := 0; worker < workers; worker++ {
			wg.Add(1)
			go func(w int, length int, start, end int64) {
				defer wg.Done()
				res := bruteForceWorker(config, length, start, end, w)
				mu.Lock()
				totalAttempts += res.Attempts
				mu.Unlock()

				if res.Found {
					resultChan <- res
				}
			}(worker, length, int64(worker)*chunkSize, int64(worker+1)*chunkSize)
		}

		wg.Wait()

		// Check if password was found
		select {
		case result := <-resultChan:
			result.Attempts = totalAttempts
			result.TimeTaken = time.Since(start)
			return result
		default:
		}
	}

	return Result{Found: false, Attempts: totalAttempts, TimeTaken: time.Since(start)}
}

// PrintAttackComparison runs multiple attack methods and prints comparison
func PrintAttackComparison(config BruteForceConfig, dictionary []string) {
	separator := "======================================================================"
	dash := "----------------------------------------------------------------------"

	fmt.Println("\n" + separator)
	fmt.Println("ADVANCED BRUTE FORCE COMPARISON")
	fmt.Println(separator + "\n")

	results := make(map[string]Result)

	// Test 1: Optimized Brute Force
	fmt.Print("[1/4] Optimized Brute Force (frequency-based character ordering)... ")
	start := time.Now()
	results["Optimized"] = OptimizedBruteForce(config)
	fmt.Printf("DONE (%.4fs, %d attempts)\n", time.Since(start).Seconds(), results["Optimized"].Attempts)

	// Test 2: Mask-based Attack
	fmt.Print("[2/4] Mask-based Brute Force (pattern matching)... ")
	start = time.Now()
	results["Mask-based"] = MaskBruteForce(config)
	fmt.Printf("DONE (%.4fs, %d attempts)\n", time.Since(start).Seconds(), results["Mask-based"].Attempts)

	// Test 3: Adaptive Parallel
	fmt.Print("[3/4] Adaptive Parallel Brute Force... ")
	start = time.Now()
	results["Adaptive"] = AdaptiveParallelBruteForce(config)
	fmt.Printf("DONE (%.4fs, %d attempts)\n", time.Since(start).Seconds(), results["Adaptive"].Attempts)

	// Test 4: Dictionary
	fmt.Print("[4/4] Dictionary Attack... ")
	start = time.Now()
	results["Dictionary"] = DictionaryAttack(config, dictionary)
	fmt.Printf("DONE (%.4fs, %d attempts)\n", time.Since(start).Seconds(), results["Dictionary"].Attempts)

	// Print comparison
	fmt.Println("\n" + dash)
	fmt.Printf("%-20s | %-15s | %-15s\n", "Method", "Attempts", "Time (sec)")
	fmt.Println(dash)

	for method, result := range results {
		if result.Found {
			fmt.Printf("%-20s | %-15d | %-15.6f\n",
				method, result.Attempts, result.TimeTaken.Seconds())
		}
	}
	fmt.Println(separator + "\n")
}
