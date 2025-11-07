/*
 * brute_force_optimized.cpp
 * ULTRA-OPTIMIZED version - fixes performance issues
 * 
 * Key optimizations:
 * 1. Uses char arrays instead of std::string (faster)
 * 2. Better work distribution (only 12 threads, not 62)
 * 3. Removed progress monitor overhead
 * 4. Inline functions for speed
 */

#include <iostream>
#include <vector>
#include <thread>
#include <atomic>
#include <chrono>
#include <cstring>
using namespace std;

// ===== CONFIGURATION =====
const char TARGET[] = "Za8yK";
const char ALPHABET[] = "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789";
const int PASSWORD_LENGTH = 5;
const int NUM_THREADS = 12;  // Exactly your CPU core count
// =========================

atomic<bool> found(false);
std::atomic<uint64_t> total_attempts(0);
char found_password[PASSWORD_LENGTH + 1] = {0};

// Ultra-fast worker using char arrays (no string overhead)
inline void worker_range(int start_idx, int end_idx, int alphabet_size) {
    char candidate[PASSWORD_LENGTH + 1];
    candidate[PASSWORD_LENGTH] = '\0';
    uint64_t local_attempts = 0;
    
    // Process range of first characters
    for (int first = start_idx; first < end_idx && !found.load(std::memory_order_relaxed); first++) {
        candidate[0] = ALPHABET[first];
        
        // Generate all combinations with this first character
        int indices[PASSWORD_LENGTH];
        for (int i = 0; i < PASSWORD_LENGTH; i++) indices[i] = 0;
        indices[0] = first;
        
        while (!found.load(std::memory_order_relaxed)) {
            // Build candidate
            for (int i = 0; i < PASSWORD_LENGTH; i++) {
                candidate[i] = ALPHABET[indices[i]];
            }
            
            local_attempts++;
            
            // Fast comparison using memcmp
            if (memcmp(candidate, TARGET, PASSWORD_LENGTH) == 0) {
                if (!found.exchange(true, std::memory_order_relaxed)) {
                    memcpy(found_password, candidate, PASSWORD_LENGTH);
                }
                goto done;
            }
            
            // Increment indices
            int pos = PASSWORD_LENGTH - 1;
            while (pos > 0) {  // Don't change first character
                indices[pos]++;
                if (indices[pos] < alphabet_size) break;
                indices[pos] = 0;
                pos--;
            }
            if (pos == 0) break;  // Done with this first character
        }
    }
    
done:
    total_attempts.fetch_add(local_attempts, std::memory_order_relaxed);
}

int main() {
    const int alphabet_size = strlen(ALPHABET);
    
    std::cout << "🚀 C++ ULTRA-OPTIMIZED BRUTE-FORCE" << std::endl;
    std::cout << "========================================" << std::endl;
    std::cout << "Target: " << TARGET << std::endl;
    std::cout << "Alphabet size: " << alphabet_size << std::endl;
    std::cout << "Password length: " << PASSWORD_LENGTH << std::endl;
    std::cout << "Threads: " << NUM_THREADS << " (optimized distribution)" << std::endl;
    
    uint64_t total_combinations = 1;
    for (int i = 0; i < PASSWORD_LENGTH; i++) {
        total_combinations *= alphabet_size;
    }
    std::cout << "Total combinations: " << total_combinations << std::endl;
    std::cout << "========================================" << std::endl;
    std::cout << "Starting attack...\n" << std::endl;
    
    auto start_time = std::chrono::high_resolution_clock::now();
    
    // Create exactly NUM_THREADS threads with balanced work
    std::vector<std::thread> threads;
    int chars_per_thread = (alphabet_size + NUM_THREADS - 1) / NUM_THREADS;
    
    for (int t = 0; t < NUM_THREADS; t++) {
        int start_idx = t * chars_per_thread;
        int end_idx = std::min(start_idx + chars_per_thread, alphabet_size);
        
        if (start_idx < alphabet_size) {
            threads.emplace_back(worker_range, start_idx, end_idx, alphabet_size);
        }
    }
    
    // Wait for completion
    for (auto& thread : threads) {
        thread.join();
    }
    
    auto end_time = std::chrono::high_resolution_clock::now();
    std::chrono::duration<double> elapsed = end_time - start_time;
    
    std::cout << "\n========================================" << std::endl;
    
    if (found.load()) {
        std::cout << "✅ SUCCESS! Password found: '" << found_password << "'" << std::endl;
        std::cout << "   Attempts: " << total_attempts.load() << std::endl;
        std::cout << "   Time: " << elapsed.count() << " seconds" << std::endl;
        std::cout << "   Speed: " << (uint64_t)(total_attempts.load() / elapsed.count()) 
                  << " attempts/second" << std::endl;
    } else {
        std::cout << "❌ Password not found" << std::endl;
        std::cout << "   Attempts: " << total_attempts.load() << std::endl;
        std::cout << "   Time: " << elapsed.count() << " seconds" << std::endl;
    }
    std::cout << "========================================" << std::endl;
    
    return 0;
}