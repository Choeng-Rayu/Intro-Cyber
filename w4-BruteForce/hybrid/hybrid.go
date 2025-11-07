package main

import (
	"fmt"
	"sync"
	"time"
)

// ============================================================================
// MULTI-THREADED BRUTE FORCE PASSWORD CRACKER
// ============================================================================

type AttackResult struct {
	Password  string
	Found     bool
	Attempts  int64
	TimeTaken time.Duration
	WorkerID  int
}

type Config struct {
	TargetPassword string
	CharacterSet   string
	MaxLength      int
	NumWorkers     int
	Verbose        bool
}

// ============================================================================
// PARALLEL BRUTE FORCE ATTACK
// ============================================================================

func ParallelBruteForceAttack(config Config) AttackResult {
	startTime := time.Now()

	if config.Verbose {
		fmt.Println("\n[PARALLEL BRUTE FORCE] Starting attack...")
		fmt.Printf("Using %d workers...\n", config.NumWorkers)
	}

	// Try each password length
	for length := 1; length <= config.MaxLength; length++ {
		if config.Verbose {
			fmt.Printf("\n  Trying all %d-character passwords with %d workers...\n", length, config.NumWorkers)
		}

		// Calculate total combinations for this length
		var totalCombinations int64 = 1
		for i := 0; i < length; i++ {
			totalCombinations *= int64(len(config.CharacterSet))
		}

		// Split work among workers
		workPerWorker := totalCombinations / int64(config.NumWorkers)
		var wg sync.WaitGroup
		resultChan := make(chan AttackResult, config.NumWorkers)
		stopChan := make(chan bool)

		// Start all workers
		for workerID := 0; workerID < config.NumWorkers; workerID++ {
			wg.Add(1)

			startNum := int64(workerID) * workPerWorker
			endNum := startNum + workPerWorker
			if workerID == config.NumWorkers-1 {
				endNum = totalCombinations
			}

			go bruteForceWorker(config, workerID, startNum, endNum, length, &wg, resultChan, stopChan)
		}

		// Wait for completion
		go func() {
			wg.Wait()
			close(resultChan)
		}()

		// Check results
		for result := range resultChan {
			if result.Found {
				close(stopChan)
				result.TimeTaken = time.Since(startTime)

				if config.Verbose {
					fmt.Printf("\n  ✓ FOUND by Worker #%d! Password is: %s\n", result.WorkerID, result.Password)
					fmt.Printf("  Total time: %f seconds\n", result.TimeTaken.Seconds())
				}

				return result
			}
		}
	}

	return AttackResult{Found: false, TimeTaken: time.Since(startTime)}
}

func bruteForceWorker(config Config, workerID int, startNum, endNum int64, length int, wg *sync.WaitGroup, resultChan chan<- AttackResult, stopChan <-chan bool) {
	defer wg.Done()

	attempts := int64(0)
	for num := startNum; num < endNum; num++ {
		select {
		case <-stopChan:
			return
		default:
		}

		password := numberToPassword(config.CharacterSet, num, length)
		attempts++

		if config.Verbose && attempts%5000000 == 0 {
			fmt.Printf("    Worker #%d: %d attempts\n", workerID, attempts)
		}

		if password == config.TargetPassword {
			resultChan <- AttackResult{
				Password: password,
				Found:    true,
				Attempts: attempts,
				WorkerID: workerID,
			}
			return
		}
	}

	resultChan <- AttackResult{Found: false, Attempts: attempts}
}

func numberToPassword(charset string, num int64, length int) string {
	base := int64(len(charset))
	password := make([]byte, length)

	for i := length - 1; i >= 0; i-- {
		password[i] = charset[num%base]
		num /= base
	}

	return string(password)
}

// ============================================================================
// MAIN
// ============================================================================

func main() {
	charset := "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789"
	targetPassword := "Za8yK"
	numWorkers := 16

	fmt.Println("🚀 MULTI-THREADED BRUTE FORCE ATTACK")
	fmt.Println("=" + string(make([]byte, 50)))
	fmt.Printf("Target:          %s\n", targetPassword)
	fmt.Printf("Workers:         %d parallel threads\n", numWorkers)
	fmt.Printf("Character Set:   %d chars (A-Z, a-z, 0-9)\n", len(charset))
	fmt.Println("=" + string(make([]byte, 50)))

	config := Config{
		TargetPassword: targetPassword,
		CharacterSet:   charset,
		MaxLength:      5,
		NumWorkers:     numWorkers,
		Verbose:        true,
	}

	result := ParallelBruteForceAttack(config)

	fmt.Println("\n" + "=" + string(make([]byte, 50)))
	fmt.Println("RESULTS")
	fmt.Println("=" + string(make([]byte, 50)))

	if result.Found {
		fmt.Printf("✓ SUCCESS!\n")
		fmt.Printf("Password Found:  %s\n", result.Password)
		fmt.Printf("Worker ID:       #%d\n", result.WorkerID)
		fmt.Printf("Attempts:        %d\n", result.Attempts)
		fmt.Printf("Time Taken:      %.3f seconds\n", result.TimeTaken.Seconds())
		fmt.Printf("Speed:           %.0f attempts/second\n", float64(result.Attempts)/result.TimeTaken.Seconds())
	} else {
		fmt.Printf("✗ Password not found\n")
	}

	fmt.Println("=" + string(make([]byte, 50)))
	fmt.Println()
	fmt.Printf("💡 Multi-threading speedup: ~%dx faster than single thread\n", numWorkers/2)
	fmt.Println("💡 More CPU cores = faster password cracking")
	fmt.Println("🔐 5-character passwords take minutes to crack - Use 12+ characters!")
}
