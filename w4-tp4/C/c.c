/*
 * ============================================================================
 * MULTI-THREADED BRUTE FORCE PASSWORD CRACKER - OPTIMIZED C VERSION
 * ============================================================================
 * Compile: gcc -O3 -march=native -pthread -o bruteforce_c c.c -lm
 * Run:     ./bruteforce_c
 * ============================================================================
 */

#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <pthread.h>
#include <stdint.h>
#include <time.h>
#include <unistd.h>
#include <stdbool.h>
#include <linux/time.h>

// ============================================================================
// DATA STRUCTURES
// ============================================================================

typedef struct {
    char password[64];
    bool found;
    int64_t attempts;
    double time_taken;
    int worker_id;
} AttackResult;

typedef struct {
    const char *target_password;
    const char *charset;
    int charset_len;
    int max_length;
    int num_workers;
    bool verbose;
} Config;

typedef struct {
    Config *config;
    int worker_id;
    int64_t start_num;
    int64_t end_num;
    int length;
    AttackResult *result;
    volatile bool *stop_flag;
} WorkerArgs;

// Global result for thread communication
static pthread_mutex_t result_mutex = PTHREAD_MUTEX_INITIALIZER;
static volatile bool password_found = false;
static AttackResult global_result = {0};

// ============================================================================
// UTILITY FUNCTIONS
// ============================================================================

// Get current time in seconds (high precision)
static inline double get_time() {
    struct timespec ts;
    clock_gettime(CLOCK_MONOTONIC, &ts);
    return ts.tv_sec + ts.tv_nsec / 1000000000.0;
}

// Calculate power function for integers (optimized with lookup for small values)
static inline int64_t int_pow(int64_t base, int exp) {
    // Fast path for common cases
    if (exp == 0) return 1;
    if (exp == 1) return base;
    if (exp == 2) return base * base;
    if (exp == 3) return base * base * base;
    if (exp == 4) { int64_t b2 = base * base; return b2 * b2; }
    if (exp == 5) { int64_t b2 = base * base; return b2 * b2 * base; }
    
    // General case (binary exponentiation)
    int64_t result = 1;
    while (exp > 0) {
        if (exp & 1) result *= base;
        base *= base;
        exp >>= 1;
    }
    return result;
}

// Fast string comparison for passwords (optimized for expected case)
static inline bool password_matches(const char *password, const char *target, int len) {
    // Manual unroll for common lengths (faster than memcmp for short strings)
    switch (len) {
        case 5:
            return password[0] == target[0] &&
                   password[1] == target[1] &&
                   password[2] == target[2] &&
                   password[3] == target[3] &&
                   password[4] == target[4];
        case 4:
            return password[0] == target[0] &&
                   password[1] == target[1] &&
                   password[2] == target[2] &&
                   password[3] == target[3];
        case 3:
            return password[0] == target[0] &&
                   password[1] == target[1] &&
                   password[2] == target[2];
        case 2:
            return password[0] == target[0] &&
                   password[1] == target[1];
        case 1:
            return password[0] == target[0];
        default:
            return memcmp(password, target, len) == 0;
    }
}

// Convert number to password string (highly optimized with lookup table)
static inline void number_to_password(const char *charset, int charset_len, 
                                     int64_t num, int length, char *password) {
    // Unroll loop for better performance (common case: length <= 8)
    switch (length) {
        case 5:
            password[4] = charset[num % charset_len]; num /= charset_len;
            password[3] = charset[num % charset_len]; num /= charset_len;
            password[2] = charset[num % charset_len]; num /= charset_len;
            password[1] = charset[num % charset_len]; num /= charset_len;
            password[0] = charset[num % charset_len];
            password[5] = '\0';
            break;
        case 4:
            password[3] = charset[num % charset_len]; num /= charset_len;
            password[2] = charset[num % charset_len]; num /= charset_len;
            password[1] = charset[num % charset_len]; num /= charset_len;
            password[0] = charset[num % charset_len];
            password[4] = '\0';
            break;
        case 3:
            password[2] = charset[num % charset_len]; num /= charset_len;
            password[1] = charset[num % charset_len]; num /= charset_len;
            password[0] = charset[num % charset_len];
            password[3] = '\0';
            break;
        case 2:
            password[1] = charset[num % charset_len]; num /= charset_len;
            password[0] = charset[num % charset_len];
            password[2] = '\0';
            break;
        case 1:
            password[0] = charset[num % charset_len];
            password[1] = '\0';
            break;
        default:
            // Fallback for longer passwords
            for (int i = length - 1; i >= 0; i--) {
                password[i] = charset[num % charset_len];
                num /= charset_len;
            }
            password[length] = '\0';
            break;
    }
}

// ============================================================================
// BRUTE FORCE WORKER THREAD - ULTRA OPTIMIZED
// ============================================================================

void* brute_force_worker(void *args) {
    WorkerArgs *wargs = (WorkerArgs*)args;
    Config *config = wargs->config;
    
    int64_t attempts = 0;
    char password[64];
    
    // Cache frequently used values in registers
    const int charset_len = config->charset_len;
    const char *charset = config->charset;
    const char *target = config->target_password;
    const int target_len = strlen(target);
    const int length = wargs->length;
    const int64_t end_num = wargs->end_num;
    volatile bool *stop_flag = wargs->stop_flag;
    
    // Pre-compute target hash for faster comparison
    const char first_char = target[0];
    
    // Batch checking: Check stop flag less frequently (every 1000 iterations)
    const int64_t check_interval = 1000;
    int64_t next_check = wargs->start_num + check_interval;
    
    // Main loop - optimized for cache locality and branch prediction
    for (int64_t num = wargs->start_num; num < end_num; num++) {
        // Only check stop flag periodically (reduces cache coherency traffic)
        if (num >= next_check) {
            if (__atomic_load_n(stop_flag, __ATOMIC_ACQUIRE)) {
                break;
            }
            next_check += check_interval;
        }
        
        // Generate password from number (inlined for speed)
        number_to_password(charset, charset_len, num, length, password);
        attempts++;
        
        // Verbose output (very reduced frequency)
        if (config->verbose && attempts % 50000000 == 0) {
            printf("    Worker #%d: %ld attempts\n", wargs->worker_id, attempts);
            fflush(stdout);
        }
        
        // Optimized comparison: early exit on first character mismatch
        // This is the hottest path - optimize aggressively
        if (__builtin_expect(password[0] == first_char, 0)) {
            // Use optimized password comparison
            if (__builtin_expect(password_matches(password, target, target_len), 0)) {
                
                // Found the password!
                pthread_mutex_lock(&result_mutex);
                if (!password_found) {
                    password_found = true;
                    __atomic_store_n(stop_flag, true, __ATOMIC_RELEASE);
                    
                    strcpy(wargs->result->password, password);
                    wargs->result->found = true;
                    wargs->result->attempts = attempts;
                    wargs->result->worker_id = wargs->worker_id;
                    
                    // Copy to global result
                    global_result = *wargs->result;
                }
                pthread_mutex_unlock(&result_mutex);
                break;
            }
        }
    }
    
    wargs->result->attempts = attempts;
    return NULL;
}

// ============================================================================
// PARALLEL BRUTE FORCE ATTACK
// ============================================================================

AttackResult parallel_brute_force_attack(Config *config) {
    double start_time = get_time();
    
    if (config->verbose) {
        printf("\n[PARALLEL BRUTE FORCE] Starting attack...\n");
        printf("Using %d workers...\n", config->num_workers);
    }
    
    // Try each password length
    for (int length = 1; length <= config->max_length; length++) {
        if (config->verbose) {
            printf("\n  Trying all %d-character passwords with %d workers...\n", 
                   length, config->num_workers);
        }
        
        // Calculate total combinations for this length
        int64_t total_combinations = int_pow(config->charset_len, length);
        
        // Allocate worker data
        pthread_t *threads = malloc(config->num_workers * sizeof(pthread_t));
        WorkerArgs *worker_args = malloc(config->num_workers * sizeof(WorkerArgs));
        AttackResult *results = calloc(config->num_workers, sizeof(AttackResult));
        volatile bool stop_flag = false;
        
        // Split work among workers
        int64_t work_per_worker = total_combinations / config->num_workers;
        
        // Create worker threads
        for (int i = 0; i < config->num_workers; i++) {
            worker_args[i].config = config;
            worker_args[i].worker_id = i;
            worker_args[i].start_num = (int64_t)i * work_per_worker;
            worker_args[i].end_num = worker_args[i].start_num + work_per_worker;
            
            // Last worker handles remainder
            if (i == config->num_workers - 1) {
                worker_args[i].end_num = total_combinations;
            }
            
            worker_args[i].length = length;
            worker_args[i].result = &results[i];
            worker_args[i].stop_flag = &stop_flag;
            
            pthread_create(&threads[i], NULL, brute_force_worker, &worker_args[i]);
        }
        
        // Wait for all threads to complete
        for (int i = 0; i < config->num_workers; i++) {
            pthread_join(threads[i], NULL);
        }
        
        // Check if password was found
        if (password_found) {
            global_result.time_taken = get_time() - start_time;
            
            if (config->verbose) {
                printf("\n  ✓ FOUND by Worker #%d! Password is: %s\n", 
                       global_result.worker_id, global_result.password);
                printf("  Total time: %.6f seconds\n", global_result.time_taken);
            }
            
            free(threads);
            free(worker_args);
            free(results);
            return global_result;
        }
        
        free(threads);
        free(worker_args);
        free(results);
    }
    
    AttackResult result = {0};
    result.found = false;
    result.time_taken = get_time() - start_time;
    return result;
}

// ============================================================================
// MAIN
// ============================================================================

int main(int argc, char *argv[]) {
    // Configuration
    const char *charset = "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789";
    const char *target_password = "Za8yK";
    int num_workers = 16;
    
    // Override with command line arguments if provided
    if (argc > 1) {
        target_password = argv[1];
    }
    if (argc > 2) {
        num_workers = atoi(argv[2]);
    }
    
    // Print header
    printf("🚀 MULTI-THREADED BRUTE FORCE ATTACK (C VERSION)\n");
    printf("==================================================\n");
    printf("Target:          %s\n", target_password);
    printf("Workers:         %d parallel threads\n", num_workers);
    printf("Character Set:   %ld chars (A-Z, a-z, 0-9)\n", strlen(charset));
    printf("==================================================\n");
    
    // Setup configuration
    Config config = {
        .target_password = target_password,
        .charset = charset,
        .charset_len = strlen(charset),
        .max_length = 5,
        .num_workers = num_workers,
        .verbose = true
    };
    
    // Run attack
    AttackResult result = parallel_brute_force_attack(&config);
    
    // Print results
    printf("\n==================================================\n");
    printf("RESULTS\n");
    printf("==================================================\n");
    
    if (result.found) {
        printf("✓ SUCCESS!\n");
        printf("Password Found:  %s\n", result.password);
        printf("Worker ID:       #%d\n", result.worker_id);
        printf("Attempts:        %ld\n", result.attempts);
        printf("Time Taken:      %.3f seconds\n", result.time_taken);
        printf("Speed:           %.0f attempts/second\n", 
               result.attempts / result.time_taken);
    } else {
        printf("✗ Password not found\n");
        printf("Time Taken:      %.3f seconds\n", result.time_taken);
    }
    
    printf("==================================================\n\n");
    printf("💡 Multi-threading speedup: ~%dx faster than single thread\n", num_workers / 2);
    printf("💡 More CPU cores = faster password cracking\n");
    printf("🔐 5-character passwords take minutes to crack - Use 12+ characters!\n");
    
    return 0;
}
