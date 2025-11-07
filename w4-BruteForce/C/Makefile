# Makefile for High-Performance Brute Force Password Cracker
# ============================================================================

# Compiler and flags
CC = gcc
CFLAGS = -O3 -march=native -pthread -Wall -Wextra
LDFLAGS = -lm -pthread

# Target executable
TARGET = c
FAST_TARGET = c_fast
DEBUG_TARGET = c_debug

# Source file
SRC = c.c

# Default target
all: $(TARGET)

# Standard optimized build
$(TARGET): $(SRC)
	@echo "🔨 Building optimized version..."
	$(CC) $(CFLAGS) -o $(TARGET) $(SRC) $(LDFLAGS)
	@echo "✅ Build complete: ./$(TARGET)"

# Ultra-fast build (aggressive optimizations)
fast: $(SRC)
	@echo "🚀 Building ULTRA-FAST version..."
	$(CC) -O3 -march=native -mtune=native -flto -funroll-loops \
	      -pthread -Wall -o $(FAST_TARGET) $(SRC) $(LDFLAGS)
	@echo "✅ Ultra-fast build complete: ./$(FAST_TARGET)"

# Debug build
debug: $(SRC)
	@echo "🐛 Building debug version..."
	$(CC) -g -O0 -pthread -Wall -Wextra -o $(DEBUG_TARGET) $(SRC) $(LDFLAGS)
	@echo "✅ Debug build complete: ./$(DEBUG_TARGET)"

# Profile-guided optimization (two-step build)
pgo: $(SRC)
	@echo "📊 Building with Profile-Guided Optimization..."
	@echo "  Step 1: Generating profile..."
	$(CC) -O3 -march=native -pthread -fprofile-generate -o $(TARGET)_pgo $(SRC) $(LDFLAGS)
	./$(TARGET)_pgo "test" 16
	@echo "  Step 2: Building with profile..."
	$(CC) -O3 -march=native -pthread -fprofile-use -o $(TARGET)_pgo_final $(SRC) $(LDFLAGS)
	@rm -f $(TARGET)_pgo *.gcda
	@mv $(TARGET)_pgo_final $(TARGET)
	@echo "✅ PGO build complete: ./$(TARGET)"

# Run with default password
run: $(TARGET)
	@echo "🏃 Running with default settings..."
	./$(TARGET)

# Run with custom password
run-custom: $(TARGET)
	@read -p "Enter password to crack: " pwd; \
	read -p "Enter number of workers [16]: " workers; \
	workers=$${workers:-16}; \
	./$(TARGET) "$$pwd" "$$workers"

# Benchmark different worker counts
bench: $(TARGET)
	@echo "📊 Benchmarking different worker counts..."
	@for workers in 1 2 4 8 16 32; do \
		echo ""; \
		echo "=== Testing with $$workers workers ==="; \
		./$(TARGET) "Za8yK" $$workers; \
	done

# Compare with Go version
compare: $(TARGET)
	@echo "⚖️  Comparing C vs Go performance..."
	@if [ -f ../bruteforce ]; then \
		echo ""; \
		echo "=== Go Version ==="; \
		time ../bruteforce; \
		echo ""; \
		echo "=== C Version ==="; \
		time ./$(TARGET); \
	else \
		echo "Go version not found at ../bruteforce"; \
		echo "Building Go version first..."; \
		cd .. && go build -o bruteforce bruteforce.go; \
		echo ""; \
		echo "=== Go Version ==="; \
		time ../bruteforce; \
		echo ""; \
		echo "=== C Version ==="; \
		time ./$(TARGET); \
	fi

# Clean build artifacts
clean:
	@echo "🧹 Cleaning build artifacts..."
	rm -f $(TARGET) $(FAST_TARGET) $(DEBUG_TARGET) $(TARGET)_pgo*
	rm -f *.o *.gcda *.gcno gmon.out
	@echo "✅ Clean complete"

# Profile with gprof
profile: $(SRC)
	@echo "📈 Building with profiling enabled..."
	$(CC) -O3 -march=native -pthread -pg -o $(TARGET)_prof $(SRC) $(LDFLAGS)
	./$(TARGET)_prof "Za8yK" 16
	gprof $(TARGET)_prof gmon.out > profile_report.txt
	@echo "✅ Profile report saved to profile_report.txt"
	@rm -f $(TARGET)_prof gmon.out

# Profile with perf (Linux)
perf: $(TARGET)
	@echo "🔍 Profiling with perf..."
	@if command -v perf > /dev/null; then \
		sudo perf record -g ./$(TARGET) "Za8yK" 16; \
		sudo perf report; \
	else \
		echo "perf not found. Install with: sudo apt-get install linux-tools-generic"; \
	fi

# Show assembly output
asm: $(SRC)
	@echo "🔧 Generating assembly output..."
	$(CC) -O3 -march=native -pthread -S -fverbose-asm -o c.asm $(SRC)
	@echo "✅ Assembly saved to c.asm"

# Static analysis
analyze: $(SRC)
	@echo "🔍 Running static analysis..."
	@if command -v cppcheck > /dev/null; then \
		cppcheck --enable=all --suppress=missingIncludeSystem $(SRC); \
	else \
		echo "cppcheck not found. Install with: sudo apt-get install cppcheck"; \
	fi

# Help
help:
	@echo "Available targets:"
	@echo "  make          - Build optimized version"
	@echo "  make fast     - Build ultra-fast version (aggressive opts)"
	@echo "  make debug    - Build debug version"
	@echo "  make pgo      - Build with Profile-Guided Optimization"
	@echo "  make run      - Run with default settings"
	@echo "  make run-custom - Run with custom password/workers"
	@echo "  make bench    - Benchmark different worker counts"
	@echo "  make compare  - Compare C vs Go performance"
	@echo "  make profile  - Profile with gprof"
	@echo "  make perf     - Profile with perf (requires sudo)"
	@echo "  make asm      - Generate assembly output"
	@echo "  make analyze  - Run static analysis"
	@echo "  make clean    - Remove build artifacts"
	@echo "  make help     - Show this help"

.PHONY: all fast debug pgo run run-custom bench compare clean profile perf asm analyze help
