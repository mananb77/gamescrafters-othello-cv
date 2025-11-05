# Othello CV Demo - Instructions

Complete guide for running and testing the Othello Computer Vision demo software.

## Table of Contents
- [Quick Start](#quick-start)
- [Installation](#installation)
- [Usage](#usage)
- [Examples](#examples)
- [Output Formats](#output-formats)
- [Testing](#testing)
- [Web Integration Guide](#web-integration-guide)
- [Troubleshooting](#troubleshooting)

---

## Quick Start

```bash
# 1. Install dependencies
pip install -r requirements.txt

# 2. Process a video
python othello_demo.py --video uploads/input-othello-4x4-gamesmanuni.mov --board-size 4 --json

# 3. Run automated tests
./test_demo.sh
```

---

## Installation

### Prerequisites
- Python 3.7 or higher
- pip package manager
- (Optional) Virtual environment tool (venv, conda, etc.)

### Step-by-Step Installation

1. **Clone or navigate to the repository:**
```bash
cd gamescrafters-othello-cv
```

2. **(Recommended) Create a virtual environment:**
```bash
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. **Install dependencies:**
```bash
pip install -r requirements.txt
```

4. **Verify installation:**
```bash
python3 othello_demo.py --help
```

You should see the help message with all available options.

---

## Usage

### Basic Command Structure

```bash
python othello_demo.py [INPUT] [OPTIONS]
```

### Input Options

**Video Processing:**
```bash
python othello_demo.py --video <path_to_video> --board-size <4|8>
```

**Image Processing:**
```bash
python othello_demo.py --image <path_to_image> --board-size <4|8>
```

### Configuration Options

| Option | Description | Default |
|--------|-------------|---------|
| `--board-size`, `-b` | Board dimensions (4 or 8) | 4 |
| `--skip-frames` | Frames to skip in video processing | 20 |
| `--color-threshold` | Piece detection threshold (0-1) | 0.3 |

### Output Options

| Option | Description |
|--------|-------------|
| `--json`, `-j` | Output results as JSON |
| `--annotate`, `-a` | Generate annotated video/image with grid overlay |
| `--debug`, `-d` | Save debug visualizations (masks) |
| `--output`, `-o` | Output directory for results |

---

## Examples

### Example 1: Basic Video Processing (4x4)

Process a 4x4 GamesmanUni video and extract game states:

```bash
python othello_demo.py \
    --video uploads/input-othello-4x4-gamesmanuni.mov \
    --board-size 4
```

**Output:**
- Console output with detected moves
- Text file: `input-othello-4x4-gamesmanuni_moves.txt`

### Example 2: JSON Output

Get structured JSON output for API integration:

```bash
python othello_demo.py \
    --video uploads/input-othello-8x8.mov \
    --board-size 8 \
    --json \
    --output results/
```

**Output:**
- `results/input-othello-8x8_result.json` - Full JSON with moves, timestamps, metadata
- `results/input-othello-8x8_moves.txt` - Human-readable text

### Example 3: Annotated Video

Create a video with grid overlay and detected pieces:

```bash
python othello_demo.py \
    --video uploads/input-othello-4x4-gamesmanuni.mov \
    --board-size 4 \
    --annotate \
    --output results/
```

**Output:**
- `results/input-othello-4x4-gamesmanuni_annotated.mp4` - Video with visual overlay
- Text file with moves

### Example 4: Debug Mode

Generate all debug visualizations for troubleshooting:

```bash
python othello_demo.py \
    --video uploads/input-othello-8x8.mov \
    --board-size 8 \
    --debug \
    --output results/
```

**Output:**
- `masks/bilateral_filtered_image.png` - Noise-reduced image
- `masks/grid_image_with_cells.png` - Grid overlay
- `masks/black_mask.png` - Black piece detection mask
- `masks/white_mask.png` - White piece detection mask
- `masks/game_pieces_mask.png` - Combined piece mask
- Regular output files

### Example 5: Image Processing

Process a single board state image:

```bash
python othello_demo.py \
    --image uploads/random-board-gamesman-uni.png \
    --board-size 4 \
    --json \
    --annotate
```

**Output:**
- JSON file with board state
- Annotated image with grid and pieces
- Console output with ASCII board visualization

### Example 6: All Output Formats

Generate every possible output type:

```bash
python othello_demo.py \
    --video uploads/input-othello-4x4-gamesmanuni.mov \
    --board-size 4 \
    --json \
    --annotate \
    --debug \
    --output results/demo_all/
```

**Output:**
- JSON file
- Text file
- Annotated video
- All debug masks
- Complete processing metadata

### Example 7: Fine-Tuning Detection

Adjust detection parameters for better accuracy:

```bash
python othello_demo.py \
    --video uploads/input-othello-real-world.mov \
    --board-size 8 \
    --skip-frames 10 \
    --color-threshold 0.4 \
    --json
```

---

## Output Formats

### 1. Console Output

Real-time progress and summary displayed in terminal:

```
Initializing Othello CV with board size: 4x4

Processing video: uploads/input-othello-4x4-gamesmanuni.mov
Skip frames: 20
Color threshold: 0.3
------------------------------------------------------------

Processing complete!
Total moves detected: 5
Total frames processed: 420
Processing time: 3.45s
------------------------------------------------------------

Detected moves:
  Move 1: Player 1 - -----WB--BW----- (frame 60)
  Move 2: Player 2 - -----WB--BWB---W (frame 140)
  Move 3: Player 1 - -B---BBW-BBW--BW (frame 220)
  Move 4: Player 2 - WB--WBBWWWWW--BW (frame 300)
  Move 5: Player 1 - WWWBWWBWWBWWWWWW (frame 380)
```

### 2. JSON Output Format

Structured data for API integration:

```json
{
  "board_size": 4,
  "moves": [
    {
      "player": 1,
      "state": "-----WB--BW-----",
      "frame": 60
    },
    {
      "player": 2,
      "state": "-----WB--BWB---W",
      "frame": 140
    }
  ],
  "total_moves": 5,
  "total_frames": 420,
  "video_path": "uploads/input-othello-4x4-gamesmanuni.mov",
  "output_video": null,
  "processing_time": 3.45
}
```

### 3. Text Output Format

Human-readable move list:

```
Othello CV Analysis
Video: uploads/input-othello-4x4-gamesmanuni.mov
Board size: 4x4
Total moves: 5
Processing time: 3.45s

------------------------------------------------------------

Move 1: Player 1 - -----WB--BW----- (frame 60)
Move 2: Player 2 - -----WB--BWB---W (frame 140)
Move 3: Player 1 - -B---BBW-BBW--BW (frame 220)
Move 4: Player 2 - WB--WBBWWWWW--BW (frame 300)
Move 5: Player 1 - WWWBWWBWWBWWWWWW (frame 380)
```

### 4. Game State String Format

Board states are encoded as strings where:
- `B` = Black piece
- `W` = White piece
- `-` = Empty square

**4x4 board (16 characters):**
```
-----WB--BW-----
```

**8x8 board (64 characters):**
```
----------------------------OWWOWO---OOOOO-----------------------------
```

**Board layout** (column-first ordering):
```
4x4 Example:
  0  4  8 12
  1  5  9 13
  2  6 10 14
  3  7 11 15
```

---

## Testing

### Automated Test Suite

Run the complete test suite:

```bash
./test_demo.sh
```

This will:
1. Test 4x4 video processing (if available)
2. Test 8x8 video processing (if available)
3. Test image processing (if available)
4. Test all output formats (JSON, annotated, debug)
5. Generate a test report

**Output location:** `test_results/`

### Manual Testing

Test specific functionality:

```bash
# Test 4x4 processing
python othello_demo.py --video uploads/input-othello-4x4-gamesmanuni.mov --board-size 4 --json --output test/

# Test 8x8 processing
python othello_demo.py --video uploads/input-othello-8x8.mov --board-size 8 --json --output test/

# Test image processing
python othello_demo.py --image uploads/random-board-gamesman-uni.png --board-size 4 --annotate --output test/
```

### Available Test Files

Located in `uploads/`:

**4x4 Videos:**
- `input-othello-4x4-gamesmanuni.mov` (12.4 MB)
- `input-othello-gamesmanuni-full.mov` (9.5 MB)

**8x8 Videos:**
- `input-othello-8x8.mov` (11.8 MB)
- `input-othello-real-world.mov` (29.2 MB)

**Images:**
- `random-board-gamesman-uni.png` (56 KB)

---

## Web Integration Guide

### Using as a Python Library

Import and use the `OthelloCV` class directly:

```python
from othello_cv import OthelloCV

# Initialize processor
processor = OthelloCV(board_size=4, skip_frames=20)

# Process video
result = processor.process_video('video.mov')

# Get JSON output
json_output = processor.format_moves_as_json(result)

# Process image
image_result = processor.process_image('board.png')
state = image_result['state']
```

### REST API Integration

Example Flask integration:

```python
from flask import Flask, request, jsonify
from othello_cv import OthelloCV
import tempfile
import os

app = Flask(__name__)

@app.route('/analyze_video', methods=['POST'])
def analyze_video():
    # Get uploaded file
    video_file = request.files['video']
    board_size = int(request.form.get('board_size', 4))

    # Save temporarily
    with tempfile.NamedTemporaryFile(delete=False, suffix='.mov') as tmp:
        video_file.save(tmp.name)
        tmp_path = tmp.name

    try:
        # Process video
        processor = OthelloCV(board_size=board_size)
        result = processor.process_video(tmp_path)

        return jsonify(result)
    finally:
        os.unlink(tmp_path)

@app.route('/analyze_image', methods=['POST'])
def analyze_image():
    # Similar implementation for images
    pass

if __name__ == '__main__':
    app.run(debug=True)
```

### Streamlit Web UI

Example Streamlit app:

```python
import streamlit as st
from othello_cv import OthelloCV
import tempfile

st.title("Othello Board Analyzer")

board_size = st.selectbox("Board Size", [4, 8])
uploaded_file = st.file_uploader("Upload Video or Image", type=['mov', 'mp4', 'png', 'jpg'])

if uploaded_file:
    with tempfile.NamedTemporaryFile(delete=False) as tmp:
        tmp.write(uploaded_file.read())
        tmp_path = tmp.name

    processor = OthelloCV(board_size=board_size)

    if uploaded_file.type.startswith('video'):
        result = processor.process_video(tmp_path)
        st.json(result)
    else:
        result = processor.process_image(tmp_path)
        st.text(f"Board State: {result['state']}")
```

---

## Troubleshooting

### Issue: Video file not found

**Error:** `Error: Video file not found: <path>`

**Solution:**
- Verify the file path is correct
- Use absolute paths or paths relative to current directory
- Check file permissions

### Issue: Poor piece detection accuracy

**Symptoms:** Missing pieces or incorrect colors detected

**Solutions:**
1. Adjust color threshold:
   ```bash
   python othello_demo.py --video input.mov --board-size 4 --color-threshold 0.4
   ```

2. Use debug mode to inspect masks:
   ```bash
   python othello_demo.py --video input.mov --board-size 4 --debug
   ```
   Check `masks/` directory for visualization

3. Ensure good lighting conditions in source video
4. Verify correct board size is specified (4 or 8)

### Issue: Too many/few moves detected

**Symptoms:** Extra moves or missing moves in output

**Solutions:**
1. Adjust frame skip rate (lower = more sensitive):
   ```bash
   python othello_demo.py --video input.mov --board-size 4 --skip-frames 10
   ```

2. Check video quality and stability
3. Ensure camera is stable (not moving during recording)

### Issue: Module import errors

**Error:** `ModuleNotFoundError: No module named 'cv2'`

**Solution:**
```bash
pip install -r requirements.txt
```

If still failing, install OpenCV manually:
```bash
pip install opencv-python opencv-python-headless
```

### Issue: Permission denied on test script

**Error:** `Permission denied: ./test_demo.sh`

**Solution:**
```bash
chmod +x test_demo.sh
./test_demo.sh
```

Or run with bash:
```bash
bash test_demo.sh
```

### Issue: Annotated video not playing

**Symptoms:** Generated `.mp4` file won't play

**Solutions:**
1. Try different video player (VLC, QuickTime, etc.)
2. Check if video was fully written (not interrupted)
3. Verify sufficient disk space
4. Install additional codecs:
   ```bash
   pip install --upgrade opencv-python
   ```

---

## Performance Tips

### For Faster Processing

1. **Increase frame skip rate:**
   ```bash
   --skip-frames 30  # Skip more frames (default: 20)
   ```

2. **Disable debug output:**
   ```bash
   # Don't use --debug flag for production
   ```

3. **Process videos in batches:**
   ```bash
   # Use the test script for batch processing
   ./test_demo.sh
   ```

### For Better Accuracy

1. **Lower frame skip rate:**
   ```bash
   --skip-frames 10  # More sensitive to changes
   ```

2. **Adjust color threshold:**
   ```bash
   --color-threshold 0.25  # Lower = more sensitive
   ```

3. **Use debug mode to fine-tune:**
   ```bash
   --debug  # Inspect masks and adjust parameters
   ```

---

## Next Steps

1. **For Development:** Integrate `othello_cv.py` into your web application
2. **For Testing:** Run `./test_demo.sh` to verify all functionality
3. **For Production:** Deploy as REST API or embed in existing system
4. **For Customization:** Modify color thresholds in `OthelloCV` class

---

## Support

For issues or questions:
- Check the [main README](README.md) for project overview
- Review debug visualizations in `masks/` directory
- Examine JSON output for detailed metadata
- Report issues to the GamesCrafters team

---

**Happy analyzing!**
