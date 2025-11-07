// EXAMPLES: Different Ways to Use the Brute Force System

// This file contains example code snippets showing how to use
// the different attack methods

package main

/*

// EXAMPLE 1: Basic Sequential Attack
func example1BasicSequential() {
    config := BruteForceConfig{
        TargetPassword: "abc123",
        CharacterSet:   "abcdefghijklmnopqrstuvwxyz0123456789",
        MaxLength:      6,
        NumWorkers:     1,
    }

    result := SequentialBruteForce(config)

    fmt.Printf("Found: %v\n", result.Found)
    fmt.Printf("Password: %s\n", result.Password)
    fmt.Printf("Attempts: %d\n", result.Attempts)
    fmt.Printf("Time: %.2fs\n", result.TimeTaken.Seconds())
}

// EXAMPLE 2: Parallel Attack
func example2Parallel() {
    config := BruteForceConfig{
        TargetPassword: "abc123",
        CharacterSet:   "abcdefghijklmnopqrstuvwxyz0123456789",
        MaxLength:      6,
        NumWorkers:     8,  // Use 8 CPU cores
    }

    result := ParallelBruteForce(config)

    fmt.Printf("Password: %s\n", result.Password)
    fmt.Printf("Time: %.2fs\n", result.TimeTaken.Seconds())
}

// EXAMPLE 3: Dictionary Attack
func example3Dictionary() {
    config := BruteForceConfig{
        TargetPassword: "password123",
        CharacterSet:   "abcdefghijklmnopqrstuvwxyz0123456789",
        MaxLength:      20,
        NumWorkers:     1,
    }

    dictionary := []string{
        "password",
        "password123",
        "admin",
        "letmein",
        "qwerty",
    }

    result := DictionaryAttack(config, dictionary)

    fmt.Printf("Found in dictionary: %v\n", result.Found)
    fmt.Printf("Attempts: %d\n", result.Attempts)
}

// EXAMPLE 4: Hybrid Attack (Fast & Reliable)
func example4Hybrid() {
    config := BruteForceConfig{
        TargetPassword: "Za8yK",
        CharacterSet:   "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789",
        MaxLength:      5,
        NumWorkers:     4,
    }

    dictionary := []string{
        "password", "123456", "admin", "Za8yK", "welcome",
    }

    // Best approach: Try dictionary first, then brute force
    result := HybridBruteForce(config, dictionary)

    fmt.Printf("Password: %s\n", result.Password)
    fmt.Printf("Time: %.6fs\n", result.TimeTaken.Seconds())
    fmt.Printf("Attempts: %d\n", result.Attempts)
}

// EXAMPLE 5: Pattern-Based Attack
func example5PatternBased() {
    config := BruteForceConfig{
        TargetPassword: "Za8yK",
        CharacterSet:   "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789",
        MaxLength:      5,
        NumWorkers:     1,
    }

    // Assume pattern: Uppercase + 3 Lowercase + Digit
    masks := []string{
        "ABCDEFGHIJKLMNOPQRSTUVWXYZ",
        "abcdefghijklmnopqrstuvwxyz",
        "abcdefghijklmnopqrstuvwxyz",
        "abcdefghijklmnopqrstuvwxyz",
        "0123456789",
    }

    found, password, attempts := tryMaskedCombinations(masks, config.TargetPassword)

    fmt.Printf("Found: %v\n", found)
    fmt.Printf("Password: %s\n", password)
    fmt.Printf("Attempts: %d\n", attempts)
}

// EXAMPLE 6: Custom Character Set
func example6CustomCharset() {
    // For passwords known to contain only lowercase + digits
    customCharset := "abcdefghijklmnopqrstuvwxyz0123456789"

    config := BruteForceConfig{
        TargetPassword: "abc123",
        CharacterSet:   customCharset,
        MaxLength:      6,
        NumWorkers:     4,
    }

    result := ParallelBruteForce(config)
    fmt.Printf("Password: %s\n", result.Password)
}

// EXAMPLE 7: Performance Comparison
func example7Comparison() {
    config := BruteForceConfig{
        TargetPassword: "abc",
        CharacterSet:   "abcdefghijklmnopqrstuvwxyz",
        MaxLength:      3,
        NumWorkers:     4,
    }

    // Test 1: Sequential
    start := time.Now()
    seq := SequentialBruteForce(config)
    seqTime := time.Since(start)

    // Test 2: Parallel
    start = time.Now()
    par := ParallelBruteForce(config)
    parTime := time.Since(start)

    // Compare
    fmt.Printf("Sequential: %.4fs, %d attempts\n", seqTime.Seconds(), seq.Attempts)
    fmt.Printf("Parallel:   %.4fs, %d attempts\n", parTime.Seconds(), par.Attempts)
    fmt.Printf("Speedup:    %.2fx\n", seqTime.Seconds()/parTime.Seconds())
}

// EXAMPLE 8: Benchmark Different Lengths
func example8BenchmarkLengths() {
    for length := 1; length <= 5; length++ {
        config := BruteForceConfig{
            TargetPassword: "a" + strings.Repeat("a", length-1),
            CharacterSet:   "abcdefghijklmnopqrstuvwxyz",
            MaxLength:      length,
            NumWorkers:     4,
        }

        start := time.Now()
        result := ParallelBruteForce(config)
        elapsed := time.Since(start)

        fmt.Printf("Length %d: %d attempts, %.4fs\n",
            length, result.Attempts, elapsed.Seconds())
    }
}

// EXAMPLE 9: Optimize Character Order
func example9OptimizedCharset() {
    // Standard charset (random order)
    standard := "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789"

    // Optimized (frequency-based)
    optimized := "aeioustnrlydcmghbfpvkwxjzAEIOUSTNRLYDCMGHBFPVKWXJZ0123456789"

    config1 := BruteForceConfig{
        TargetPassword: "ease",
        CharacterSet:   standard,
        MaxLength:      4,
        NumWorkers:     1,
    }

    config2 := BruteForceConfig{
        TargetPassword: "ease",
        CharacterSet:   optimized,
        MaxLength:      4,
        NumWorkers:     1,
    }

    // With standard charset
    start := time.Now()
    seq1 := SequentialBruteForce(config1)
    time1 := time.Since(start)

    // With optimized charset
    start = time.Now()
    seq2 := SequentialBruteForce(config2)
    time2 := time.Since(start)

    fmt.Printf("Standard:  %d attempts, %.4fs\n", seq1.Attempts, time1.Seconds())
    fmt.Printf("Optimized: %d attempts, %.4fs\n", seq2.Attempts, time2.Seconds())
    fmt.Printf("Improvement: %.2fx\n", float64(seq1.Attempts)/float64(seq2.Attempts))
}

// EXAMPLE 10: Real-world Attack Scenario
func example10RealWorldScenario() {
    // Scenario: Cracking a user's password with partial knowledge
    // Known: Uses common patterns, previously seen "admin" in other sites

    config := BruteForceConfig{
        TargetPassword: "Admin2024",
        CharacterSet:   "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789",
        MaxLength:      10,
        NumWorkers:     8,
    }

    // Known patterns to try first
    dictionary := []string{
        "admin",
        "admin123",
        "admin2024",
        "password",
        "Admin",
        "Admin123",
        "Admin2024",
        "welcome",
        "welcome123",
    }

    // Use hybrid approach
    result := HybridBruteForce(config, dictionary)

    fmt.Printf("SUCCESS!\n")
    fmt.Printf("Password: %s\n", result.Password)
    fmt.Printf("Attempts: %d\n", result.Attempts)
    fmt.Printf("Time: %.4fs\n", result.TimeTaken.Seconds())
}

*/

// To use these examples:
// 1. Uncomment the code
// 2. Add necessary imports (time, strings, fmt)
// 3. Call the function you want to test
// 4. Rebuild: go build -o bruteforce main.go bruteforce.go advanced.go
