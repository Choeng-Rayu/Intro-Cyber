package main

import (
	"sync"
	"time"
)

// BruteForceConfig holds configuration for brute force attack
type BruteForceConfig struct {
	TargetPassword string
	CharacterSet   string
	MaxLength      int
	NumWorkers     int
}

// Result holds the found password and statistics
type Result struct {
	Password  string
	Found     bool
	Attempts  int64
	TimeTaken time.Duration
	WorkerID  int
}

// SequentialBruteForce performs a simple sequential brute force
func SequentialBruteForce(config BruteForceConfig) Result {
	start := time.Now()
	attempts := 0
	result := Result{Found: false}

	// Try all possible combinations
	for length := 1; length <= config.MaxLength; length++ {
		found, pwd, att := tryAllCombinations(config, length)
		if found {
			result.Password = pwd
			result.Found = found
			result.Attempts = int64(attempts + att)
			result.TimeTaken = time.Since(start)
			return result
		}
		attempts += att
	}

	result.Attempts = int64(attempts)
	result.TimeTaken = time.Since(start)
	return result
}

// tryAllCombinations tries all combinations of a specific length
func tryAllCombinations(config BruteForceConfig, length int) (bool, string, int) {
	attempts := 0
	indices := make([]int, length)

	for {
		// Generate current combination
		candidate := ""
		for _, idx := range indices {
			candidate += string(config.CharacterSet[idx])
		}

		attempts++

		if candidate == config.TargetPassword {
			return true, candidate, attempts
		}

		// Increment indices (like counting in a different base)
		carry := 1
		for i := length - 1; i >= 0 && carry > 0; i-- {
			indices[i] += carry
			if indices[i] >= len(config.CharacterSet) {
				indices[i] = 0
			} else {
				carry = 0
			}
		}

		// If carry is still 1, we've tried all combinations
		if carry > 0 {
			break
		}
	}

	return false, "", attempts
}

// ParallelBruteForce uses goroutines to speed up the search
func ParallelBruteForce(config BruteForceConfig) Result {
	start := time.Now()
	resultChan := make(chan Result, 1)
	var wg sync.WaitGroup

	for length := 1; length <= config.MaxLength; length++ {
		// For each length, distribute work among workers
		divisor := int64(1)
		for i := 0; i < length; i++ {
			divisor *= int64(len(config.CharacterSet))
		}

		chunkSize := (divisor + int64(config.NumWorkers) - 1) / int64(config.NumWorkers)

		for worker := 0; worker < config.NumWorkers; worker++ {
			wg.Add(1)
			go func(w int, length int, start, end int64) {
				defer wg.Done()
				res := bruteForceWorker(config, length, start, end, w)
				if res.Found {
					resultChan <- res
				}
			}(worker, length, int64(worker)*chunkSize, int64(worker+1)*chunkSize)
		}

		// Wait for all workers to finish this length
		wg.Wait()

		// Check if password was found
		select {
		case result := <-resultChan:
			result.TimeTaken = time.Since(start)
			return result
		default:
		}
	}

	return Result{Found: false, TimeTaken: time.Since(start)}
}

// bruteForceWorker processes a range of combinations
func bruteForceWorker(config BruteForceConfig, length int, start, end int64, workerID int) Result {
	attempts := int64(0)

	for n := start; n < end; n++ {
		// Convert number to string of given length
		candidate := numberToString(config.CharacterSet, n, length)
		attempts++

		if len(candidate) == length && candidate == config.TargetPassword {
			return Result{
				Password: candidate,
				Found:    true,
				Attempts: attempts,
				WorkerID: workerID,
			}
		}
	}

	return Result{Found: false, Attempts: attempts, WorkerID: workerID}
}

// numberToString converts a number to a string using the character set
func numberToString(charset string, num int64, length int) string {
	if num == 0 && length == 1 {
		return string(charset[0])
	}

	result := ""
	base := int64(len(charset))

	for i := 0; i < length; i++ {
		result = string(charset[num%base]) + result
		num /= base
	}

	// Pad with first character if needed
	for len(result) < length {
		result = string(charset[0]) + result
	}

	return result[:length]
}

// DictionaryAttack uses a predefined list of common passwords
func DictionaryAttack(config BruteForceConfig, dictionary []string) Result {
	start := time.Now()
	attempts := int64(0)

	for _, pwd := range dictionary {
		attempts++
		if pwd == config.TargetPassword {
			return Result{
				Password:  pwd,
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

// HybridBruteForce combines dictionary attack with brute force
func HybridBruteForce(config BruteForceConfig, dictionary []string) Result {
	// First try dictionary
	result := DictionaryAttack(config, dictionary)
	if result.Found {
		return result
	}

	// Then try brute force
	result2 := ParallelBruteForce(config)
	result2.Attempts += result.Attempts
	return result2
}

// PatternBruteForce uses patterns to reduce search space
// (e.g., common patterns like Capital+Lowercase+Number)
func PatternBruteForce(config BruteForceConfig) Result {
	start := time.Now()
	attempts := int64(0)

	// Define character subsets
	uppercase := "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
	lowercase := "abcdefghijklmnopqrstuvwxyz"
	numbers := "0123456789"
	special := "!@#$%^&*-_=+"

	patterns := []string{
		uppercase + lowercase + numbers + special,
		uppercase + lowercase + numbers,
		lowercase + numbers,
		uppercase + lowercase,
	}

	for _, charset := range patterns {
		config.CharacterSet = charset
		found, pwd, att := tryAllCombinations(config, config.MaxLength)
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
