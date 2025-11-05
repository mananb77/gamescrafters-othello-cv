# Quick Start Guide - Othello CV Demo

Get started with the Othello Computer Vision demo in under 2 minutes!

---

## Installation (30 seconds)

```bash
# 1. Navigate to project directory
cd gamescrafters-othello-cv

# 2. Install dependencies
pip install -r requirements.txt
```

---

## Run Your First Analysis (30 seconds)

### Option 1: Process an Image

```bash
python othello_demo.py \
    --image uploads/random-board-gamesman-uni.png \
    --board-size 4 \
    --json
```

**Output:**
```
Board state: -----BW-BWB-W---
Processing time: 0.03s
```

### Option 2: Process a Video

```bash
python othello_demo.py \
    --video uploads/input-othello-4x4-gamesmanuni.mov \
    --board-size 4 \
    --json
```

**Output:**
```
Total moves detected: 13
Total frames processed: 2646
Processing time: 12.5s
```

---

## View Results

Check the output files in the current directory:
- `{filename}_result.json` - Structured data with all moves
- `{filename}_moves.txt` - Human-readable move list

---

## Run Automated Tests (1 minute)

```bash
./test_demo.sh
```

This will test all features and generate comprehensive test results in `test_results/`.

---

## Use as Python Library

```python
from othello_cv import OthelloCV

# Initialize processor
processor = OthelloCV(board_size=4)

# Process video
result = processor.process_video('video.mov')
print(f"Detected {result['total_moves']} moves")

# Process image
img_result = processor.process_image('board.png')
print(f"Board state: {img_result['state']}")

# Get JSON output
json_data = processor.format_moves_as_json(result)
```

---

## Common Commands

### Generate Annotated Video
```bash
python othello_demo.py --video input.mov --board-size 4 --annotate
```

### Debug Mode (Show Masks)
```bash
python othello_demo.py --video input.mov --board-size 4 --debug
```

### All Outputs at Once
```bash
python othello_demo.py \
    --video input.mov \
    --board-size 4 \
    --json \
    --annotate \
    --debug \
    --output results/
```

---

## Need More Help?

- **Complete Documentation:** [DEMO_INSTRUCTIONS.md](DEMO_INSTRUCTIONS.md)
- **Test Results:** [TEST_REPORT.md](TEST_REPORT.md)
- **Project Overview:** [README.md](README.md)

---

## What's Included

✅ **Core Library** (`othello_cv.py`)
- Reusable OthelloCV class
- Process videos and images
- Multiple output formats

✅ **CLI Tool** (`othello_demo.py`)
- Command-line interface
- All features accessible via flags
- Comprehensive error handling

✅ **Automated Tests** (`test_demo.sh`)
- 14 comprehensive tests
- All tests passing ✅
- Validates all features

✅ **Documentation**
- Complete usage guide
- Test results report
- Web integration examples

---

## Quick Reference

### Board Sizes
- `--board-size 4` = 4x4 (GamesmanUni)
- `--board-size 8` = 8x8 (Standard Othello)

### Output Formats
- `--json` = JSON file with structured data
- `--annotate` = Video/image with grid overlay
- `--debug` = Debug masks for troubleshooting

### Configuration
- `--skip-frames N` = Process every Nth frame (default: 20)
- `--color-threshold X` = Piece detection sensitivity (default: 0.3)
- `--output DIR` = Save results to directory

---

**Ready to integrate into your website?** See [DEMO_INSTRUCTIONS.md](DEMO_INSTRUCTIONS.md#web-integration-guide) for REST API and web deployment examples!
