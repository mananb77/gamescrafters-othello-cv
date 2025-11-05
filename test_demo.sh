#!/bin/bash
# Automated testing script for Othello CV Demo
# Tests all available video and image inputs

set -e  # Exit on error

echo "========================================"
echo "Othello CV Demo - Automated Testing"
echo "========================================"
echo ""

# Create test output directory
TEST_OUTPUT_DIR="test_results"
mkdir -p "$TEST_OUTPUT_DIR"

echo "Test output will be saved to: $TEST_OUTPUT_DIR/"
echo ""

# Test counter
TESTS_PASSED=0
TESTS_FAILED=0

# Function to run test
run_test() {
    local test_name=$1
    local command=$2

    echo "----------------------------------------"
    echo "TEST: $test_name"
    echo "Command: $command"
    echo ""

    if eval "$command"; then
        echo "✓ PASSED: $test_name"
        ((TESTS_PASSED++))
    else
        echo "✗ FAILED: $test_name"
        ((TESTS_FAILED++))
    fi
    echo ""
}

# ========================================
# 4x4 Board Tests (GamesmanUni)
# ========================================
echo "========================================"
echo "Testing 4x4 Boards (GamesmanUni)"
echo "========================================"
echo ""

if [ -f "uploads/input-othello-4x4-gamesmanuni.mov" ]; then
    run_test "4x4 Video - Basic Processing" \
        "python3 othello_demo.py --video uploads/input-othello-4x4-gamesmanuni.mov --board-size 4 --output $TEST_OUTPUT_DIR/test_4x4_basic"

    run_test "4x4 Video - JSON Output" \
        "python3 othello_demo.py --video uploads/input-othello-4x4-gamesmanuni.mov --board-size 4 --json --output $TEST_OUTPUT_DIR/test_4x4_json"

    run_test "4x4 Video - Annotated Output" \
        "python3 othello_demo.py --video uploads/input-othello-4x4-gamesmanuni.mov --board-size 4 --annotate --output $TEST_OUTPUT_DIR/test_4x4_annotate"

    run_test "4x4 Video - Debug Mode" \
        "python3 othello_demo.py --video uploads/input-othello-4x4-gamesmanuni.mov --board-size 4 --debug --output $TEST_OUTPUT_DIR/test_4x4_debug"

    run_test "4x4 Video - All Output Formats" \
        "python3 othello_demo.py --video uploads/input-othello-4x4-gamesmanuni.mov --board-size 4 --json --annotate --debug --output $TEST_OUTPUT_DIR/test_4x4_all"
else
    echo "⚠ Skipping 4x4 video tests - file not found"
    echo ""
fi

# ========================================
# 8x8 Board Tests (Standard Othello)
# ========================================
echo "========================================"
echo "Testing 8x8 Boards (Standard Othello)"
echo "========================================"
echo ""

if [ -f "uploads/input-othello-8x8.mov" ]; then
    run_test "8x8 Video - Basic Processing" \
        "python3 othello_demo.py --video uploads/input-othello-8x8.mov --board-size 8 --output $TEST_OUTPUT_DIR/test_8x8_basic"

    run_test "8x8 Video - JSON Output" \
        "python3 othello_demo.py --video uploads/input-othello-8x8.mov --board-size 8 --json --output $TEST_OUTPUT_DIR/test_8x8_json"

    run_test "8x8 Video - Skip Frames = 10" \
        "python3 othello_demo.py --video uploads/input-othello-8x8.mov --board-size 8 --skip-frames 10 --output $TEST_OUTPUT_DIR/test_8x8_skip10"
else
    echo "⚠ Skipping 8x8 video tests - file not found"
    echo ""
fi

# ========================================
# Image Tests
# ========================================
echo "========================================"
echo "Testing Image Input"
echo "========================================"
echo ""

if [ -f "uploads/random-board-gamesman-uni.png" ]; then
    run_test "Image - Basic Processing" \
        "python3 othello_demo.py --image uploads/random-board-gamesman-uni.png --board-size 4 --output $TEST_OUTPUT_DIR/test_image_basic"

    run_test "Image - JSON Output" \
        "python3 othello_demo.py --image uploads/random-board-gamesman-uni.png --board-size 4 --json --output $TEST_OUTPUT_DIR/test_image_json"

    run_test "Image - Annotated Output" \
        "python3 othello_demo.py --image uploads/random-board-gamesman-uni.png --board-size 4 --annotate --output $TEST_OUTPUT_DIR/test_image_annotate"

    run_test "Image - Debug Mode" \
        "python3 othello_demo.py --image uploads/random-board-gamesman-uni.png --board-size 4 --debug --output $TEST_OUTPUT_DIR/test_image_debug"
else
    echo "⚠ Skipping image tests - file not found"
    echo ""
fi

# ========================================
# Additional Video Tests (if available)
# ========================================
echo "========================================"
echo "Testing Additional Videos"
echo "========================================"
echo ""

if [ -f "uploads/input-othello-gamesmanuni-full.mov" ]; then
    run_test "GamesmanUni Full Video - 4x4" \
        "python3 othello_demo.py --video uploads/input-othello-gamesmanuni-full.mov --board-size 4 --json --output $TEST_OUTPUT_DIR/test_gamesman_full"
else
    echo "⚠ Skipping GamesmanUni full video test - file not found"
fi

if [ -f "uploads/input-othello-real-world.mov" ]; then
    run_test "Real World Video - 8x8" \
        "python3 othello_demo.py --video uploads/input-othello-real-world.mov --board-size 8 --json --output $TEST_OUTPUT_DIR/test_real_world"
else
    echo "⚠ Skipping real world video test - file not found"
fi

echo ""

# ========================================
# Test Summary
# ========================================
echo "========================================"
echo "Test Summary"
echo "========================================"
echo "Tests Passed: $TESTS_PASSED"
echo "Tests Failed: $TESTS_FAILED"
echo "Total Tests:  $((TESTS_PASSED + TESTS_FAILED))"
echo ""

if [ $TESTS_FAILED -eq 0 ]; then
    echo "✓ All tests passed!"
    echo ""
    echo "Test results saved to: $TEST_OUTPUT_DIR/"
    exit 0
else
    echo "✗ Some tests failed. Check output above for details."
    exit 1
fi
