/*
 * brute_force_optimized.cpp
 * OPTIMIZED version - single-threaded for compatibility
 * 
 * Key optimizations:
 * 1. Uses char arrays instead of std::string (faster)
 * 2. Removed threading overhead and compatibility issues
 * 3. Removed progress monitor overhead
 * 4. Inline functions for speed
 */

#include <iostream>
#include <cstring>
#include <chrono>
using namespace std;

// ===== CONFIGURATION =====
const char TARGET[] = "Za8yK";
const char ALPHABET[] = "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789";
const int PASSWORD_LENGTH = 5;
// =========================

bool found_flag = false;
uint64_t total_attempts = 0;
char found_password[PASSWORD_LENGTH + 1] = {0};

// Fast brute-force function
void brute_force_single_threaded(const int alphabet_size) {
    char candidate[PASSWORD_LENGTH + 1];
    candidate[PASSWORD_LENGTH] = '\0';
    
    // Initialize indices array
    int indices[PASSWORD_LENGTH];
    for (int i = 0; i < PASSWORD_LENGTH; i++) {
        indices[i] = 0;
    }
    
    while (!found_flag) {
        // Build candidate from indices
        for (int i = 0; i < PASSWORD_LENGTH; i++) {
            candidate[i] = ALPHABET[indices[i]];
        }
        
        total_attempts++;
        
        // Fast comparison using memcmp
        if (memcmp(candidate, TARGET, PASSWORD_LENGTH) == 0) {
            found_flag = true;
            strcpy(found_password, candidate);
            return;
        }
        
        // Increment indices (like incrementing a base-N number)
        int pos = PASSWORD_LENGTH - 1;
        while (pos >= 0) {
            indices[pos]++;
            if (indices[pos] < alphabet_size) {
                break;
            }
            indices[pos] = 0;
            pos--;
        }
        
        // If we've wrapped around completely, we're done
        if (pos < 0) {
            break;
        }
    }
}

int main() {
    const int alphabet_size = strlen(ALPHABET);
    
    std::cout << "C++ BRUTE-FORCE PASSWORD CRACKER" << std::endl;
    std::cout << "========================================" << std::endl;
    std::cout << "Target: " << TARGET << std::endl;
    std::cout << "Alphabet size: " << alphabet_size << std::endl;
    std::cout << "Password length: " << PASSWORD_LENGTH << std::endl;
    
    uint64_t total_combinations = 1;
    for (int i = 0; i < PASSWORD_LENGTH; i++) {
        total_combinations *= alphabet_size;
    }
    std::cout << "Total combinations: " << total_combinations << std::endl;
    std::cout << "========================================" << std::endl;
    std::cout << "Starting attack...\n" << std::endl;
    
    auto start_time = std::chrono::high_resolution_clock::now();
    
    // Single-threaded brute force
    brute_force_single_threaded(alphabet_size);
    
    auto end_time = std::chrono::high_resolution_clock::now();
    std::chrono::duration<double> elapsed = end_time - start_time;
    
    std::cout << "\n========================================" << std::endl;
    
    if (found_flag) {
        std::cout << "SUCCESS! Password found: '" << found_password << "'" << std::endl;
        std::cout << "   Attempts: " << total_attempts << std::endl;
        std::cout << "   Time: " << elapsed.count() << " seconds" << std::endl;
        if (elapsed.count() > 0) {
            std::cout << "   Speed: " << (uint64_t)(total_attempts / elapsed.count()) 
                      << " attempts/second" << std::endl;
        }
    } else {
        std::cout << "Password not found" << std::endl;
        std::cout << "   Attempts: " << total_attempts << std::endl;
        std::cout << "   Time: " << elapsed.count() << " seconds" << std::endl;
    }
    std::cout << "========================================" << std::endl;
    
    return 0;
}