#!/bin/bash

# ============================================================================
# Benchmark Script: C vs Go Brute Force Performance
# ============================================================================

echo "🔬 PERFORMANCE BENCHMARK: C vs Go"
echo "===================================================="
echo ""

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Test configuration
TARGET_PASSWORD="Za8yK"
WORKERS=16

# Check if Go version exists
if [ ! -f "../bruteforce" ]; then
    echo -e "${YELLOW}Go version not found. Building...${NC}"
    cd .. && go build -o bruteforce bruteforce.go
    cd C
fi

# Check if C version exists
if [ ! -f "./c" ]; then
    echo -e "${YELLOW}C version not found. Building...${NC}"
    make clean && make
fi

echo -e "${BLUE}Configuration:${NC}"
echo "  Target Password: $TARGET_PASSWORD"
echo "  Workers: $WORKERS"
echo ""

# Run Go version
echo -e "${YELLOW}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
echo -e "${YELLOW}Testing Go Implementation${NC}"
echo -e "${YELLOW}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"

GO_START=$(date +%s.%N)
GO_OUTPUT=$(../bruteforce 2>&1 | grep -E "Time Taken:|Speed:")
GO_END=$(date +%s.%N)
GO_TIME=$(echo "$GO_END - $GO_START" | bc)

echo "$GO_OUTPUT"
echo ""

# Run C version
echo -e "${YELLOW}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
echo -e "${YELLOW}Testing C Implementation${NC}"
echo -e "${YELLOW}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"

C_START=$(date +%s.%N)
C_OUTPUT=$(./c "$TARGET_PASSWORD" $WORKERS 2>&1 | grep -E "Time Taken:|Speed:")
C_END=$(date +%s.%N)
C_TIME=$(echo "$C_END - $C_START" | bc)

echo "$C_OUTPUT"
echo ""

# Calculate speedup
SPEEDUP=$(echo "scale=2; $GO_TIME / $C_TIME" | bc)

# Results
echo -e "${GREEN}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
echo -e "${GREEN}BENCHMARK RESULTS${NC}"
echo -e "${GREEN}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
echo ""
printf "%-20s %10s\n" "Implementation" "Time (s)"
echo "────────────────────────────────────────"
printf "%-20s %10.3f\n" "Go" "$GO_TIME"
printf "%-20s %10.3f\n" "C" "$C_TIME"
echo ""
echo -e "${GREEN}✨ C is ${SPEEDUP}x faster than Go!${NC}"
echo ""

# Performance metrics
echo "📊 Performance Metrics:"
echo "────────────────────────────────────────"

# Extract speeds from outputs
GO_SPEED=$(echo "$GO_OUTPUT" | grep "Speed:" | grep -oP '\d+' | tail -1)
C_SPEED=$(echo "$C_OUTPUT" | grep "Speed:" | grep -oP '\d+' | tail -1)

if [ ! -z "$GO_SPEED" ] && [ ! -z "$C_SPEED" ]; then
    SPEED_IMPROVEMENT=$(echo "scale=1; ($C_SPEED - $GO_SPEED) * 100 / $GO_SPEED" | bc)
    echo "  Go Speed:  ${GO_SPEED} attempts/sec"
    echo "  C Speed:   ${C_SPEED} attempts/sec"
    echo "  Improvement: ${SPEED_IMPROVEMENT}% faster"
fi

echo ""
echo "💡 Tips for even better performance:"
echo "  • Use more workers: ./c \"$TARGET_PASSWORD\" 32"
echo "  • Build ultra-fast: make fast"
echo "  • Enable CPU performance mode: sudo cpupower frequency-set -g performance"
echo ""
