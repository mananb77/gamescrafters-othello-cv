# Othello Computer Vision

Computer vision system for automatic detection and analysis of Othello board game states. This project processes images and videos of Othello games to extract game positions, track moves, and generate game state strings compatible with GamesmanUni solver format.

## 🌐 Live Demo

**Try it now:** [https://mananb77.github.io/gamescrafters-othello-cv/](https://mananb77.github.io/gamescrafters-othello-cv/)

Interactive demo website featuring:
- 📸 **Mock Upload Demo** - Test with sample board positions
- 🎬 **Video Processing Demo** - Watch move detection in action (slowed 10x for clarity)
- ⚡ **Live Upload Demo** - Process your own images and videos in real-time
- 📊 **Test Results** - View performance metrics (14/14 tests passing)
- 📚 **Documentation** - Complete API reference and usage guides

**Sample Files for Testing:** Download files from the [`uploads/`](uploads/) folder to test the **Live Upload Demo**:
- [`input-othello-4x4-gamesmanuni.mov`](uploads/input-othello-4x4-gamesmanuni.mov) - 4x4 GamesmanUni video
- [`input-othello-8x8.mov`](uploads/input-othello-8x8.mov) - 8x8 standard Othello video
- [`random-board-gamesman-uni.png`](uploads/random-board-gamesman-uni.png) - Sample board image

**Note:** The Live Upload Demo requires the backend server to be running (see [Backend Setup](#backend-setup) below).

Built with UC Berkeley GamesCrafters branding and deployed on GitHub Pages.

## Overview

This project uses OpenCV and computer vision techniques to:
- Detect Othello boards from images and video footage
- Identify piece positions (black, white, or empty)
- Convert board states to string representations
- Track game progression through video analysis
- Apply perspective transformations for real-world boards
- Generate AutoGUI-compatible move sequences

## Features

- **Board Detection**: Automatic edge detection and board boundary identification
- **Piece Recognition**: Color-based masking to detect black and white pieces
- **Video Processing**: Frame-by-frame analysis with motion detection
- **Perspective Correction**: Transform skewed/angled boards to orthogonal view
- **State Extraction**: Convert visual boards to game state strings (e.g., `--B--BB--WWW----`)
- **Move Tracking**: Identify individual moves by comparing consecutive frames
- **Grid Support**: Works with both 4x4 and 8x8 board sizes

## Requirements

```
numpy
matplotlib
scipy
opencv-python
opencv-python-headless
Pillow
scikit-learn
```

## Installation

1. Clone this repository:
```bash
git clone https://github.com/gamescrafters/gamescrafters-othello-cv.git
cd gamescrafters-othello-cv
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

## Demo Software

**NEW!** Ready-to-use command-line demo for processing videos and images:

### Quick Start

```bash
# Process a video
python othello_demo.py --video uploads/input-othello-4x4-gamesmanuni.mov --board-size 4 --json

# Process an image
python othello_demo.py --image uploads/random-board-gamesman-uni.png --board-size 4 --annotate

# Run automated tests
./test_demo.sh
```

### Key Features
- **Standalone Python script** - No Jupyter notebooks required
- **Multiple output formats** - JSON, annotated videos, debug visualizations
- **Both board sizes** - Supports 4x4 (GamesmanUni) and 8x8 (standard Othello)
- **Easy integration** - Use as library or command-line tool

### Demo Files
- `othello_cv.py` - Core CV library (reusable module)
- `othello_demo.py` - Command-line interface
- `test_demo.sh` - Automated testing script
- `DEMO_INSTRUCTIONS.md` - **[Complete documentation →](DEMO_INSTRUCTIONS.md)**

### Example Output

**Video Processing:**
```bash
python othello_demo.py --video input.mov --board-size 4 --json
```
Produces:
- Game state strings for each move
- JSON with moves, timestamps, and metadata
- Text file with human-readable format

**Image Processing:**
```bash
python othello_demo.py --image board.png --board-size 8 --annotate --debug
```
Produces:
- Board state string
- Annotated image with grid overlay
- Debug masks (bilateral filter, color detection, etc.)

See **[DEMO_INSTRUCTIONS.md](DEMO_INSTRUCTIONS.md)** for complete usage guide, examples, and web integration instructions.

## Backend Setup

To enable the **Live Upload Demo** on the website, you need to run the Flask backend server:

### Local Development

```bash
cd backend
./start_server.sh
```

The backend will start at `http://localhost:5001` and automatically handle file uploads from the website.

**Features:**
- Real-time image and video processing
- RESTful API endpoints
- CORS enabled for web integration
- Automatic file cleanup after processing

See **[backend/README.md](backend/README.md)** for complete API documentation.

### Cloud Deployment (Optional)

For production use, deploy the backend to a cloud service:

**Option 1: Railway**
```bash
# Install Railway CLI: https://docs.railway.app/develop/cli
railway login
railway init
railway up
```

**Option 2: Heroku**
```bash
# Install Heroku CLI: https://devcenter.heroku.com/articles/heroku-cli
heroku login
heroku create othello-cv-api
git push heroku main
```

**Option 3: DigitalOcean App Platform**
- Connect your GitHub repository
- Set build command: `pip install -r backend/requirements.txt`
- Set run command: `python backend/app.py`

**Note:** GitHub Pages only serves static content, so the backend must be deployed separately for the Live Upload Demo to work online. The Mock Upload and Video demos work without a backend.

## Project Structure

```
gamescrafters-othello-cv/
├── othello_cv.py                           # ⭐ Core CV library (reusable)
├── othello_demo.py                         # ⭐ Command-line interface
├── test_demo.sh                            # ⭐ Automated testing script
├── requirements.txt                        # ⭐ Python dependencies
├── README.md                               # Project overview
├── DEMO_INSTRUCTIONS.md                    # ⭐ Complete usage guide
├── TEST_REPORT.md                          # ⭐ Test results & validation
│
├── backend/                                # ⭐ Flask API server
│   ├── app.py                              # Backend server
│   ├── requirements.txt                    # Backend dependencies
│   ├── start_server.sh                     # Quick start script
│   └── README.md                           # API documentation
│
├── docs/                                   # ⭐ Demo website
│   ├── index.html                          # Main website
│   ├── css/custom.css                      # Styles
│   ├── js/main.js                          # Interactive features
│   └── assets/                             # Images and videos
│
├── othello-cv-md.ipynb                     # Notebook: Basic CV pipeline
├── othello-gamesman-uni.ipynb              # Notebook: GamesmanUni integration
├── othello-online.ipynb                    # Notebook: Online game analysis
├── othello-real-world.ipynb                # Notebook: Real-world boards
├── othello-board-video-transform.ipynb     # Notebook: Perspective transform
│
├── uploads/                                # Input videos and images
│   ├── input-othello-4x4-gamesmanuni.mov   # Sample 4x4 video
│   ├── input-othello-8x8.mov               # Sample 8x8 video
│   └── random-board-gamesman-uni.png       # Sample image
├── outputs/                                # Processed output videos
├── masks/                                  # Debug masks and visualizations
└── test_results/                           # Generated test outputs
```

⭐ = Production-ready demo files

## Usage

### Processing a Single Image

```python
from process_frame import get_gamestate_from_board_image

# Extract game state from an image
game_state = get_gamestate_from_board_image('path/to/board_image.png')
print(game_state)  # Output: '--B--BB--WWW----'
```

### Processing Video for Game Moves

```python
from extract_frames import extract_frames

# Extract all game positions from video
game_states = extract_frames('path/to/game_video.mov', skip_frames=20)
for state in game_states:
    print(state)  # Output: 'p=1_-----WB--BW-----'
```

### Detecting Moves Between Frames

```python
from move_detection import get_move_from_two_frames

# Compare two frames to find the move made
move = get_move_from_two_frames('frame1.png', 'frame2.png')
print(move)  # Output: 'A_h_15_x'
```

## How It Works

### 1. Image Preprocessing
- Convert to grayscale
- Apply bilateral filtering to reduce noise
- Use Gaussian blur for edge detection

### 2. Board Detection
- Canny edge detection to find board boundaries
- Contour detection to identify the largest rectangular region
- Perspective transformation to correct viewing angle

### 3. Grid Division
- Divide board into NxN grid cells (4x4 or 8x8)
- Calculate cell dimensions based on detected board size

### 4. Piece Detection
- Create HSV color masks for black and white pieces
- Apply masks to filter out background colors (red, green, yellow)
- Analyze each cell to determine piece color based on dominant pixels
- Use threshold (>30% coverage) to classify pieces

### 5. State String Generation
- Map grid positions to characters: `B` (black), `W` (white), `-` (empty)
- Serialize 2D grid into 1D string format
- Output format: `p=N_BBWW--WW...` where N is player number

### 6. Video Analysis
- Process frames with configurable skip rate
- Detect motion between frames to identify stable board states
- Compare consecutive game states to identify moves
- Calculate move indices for AutoGUI format

## Notebooks

### othello-cv-md.ipynb
Basic computer vision pipeline demonstrating:
- Image loading and preprocessing
- Edge detection and board extraction
- Grid detection and piece recognition
- State string conversion

### othello-gamesman-uni.ipynb
Integration with GamesmanUni solver:
- Extract game states in GamesmanUni format
- Process pre-cropped gameplay videos
- Output compatible position strings

### othello-board-video-transform.ipynb
Perspective transformation techniques:
- Harris corner detection
- Perspective transform matrix computation
- Real-time video processing with transformation

### othello-online.ipynb
Online game analysis tools for processing digital board screenshots.

### othello-real-world.ipynb
Handles real-world Othello boards:
- Physical board detection under various lighting
- Robust piece detection with color calibration

## Game State Format

Game states are represented as strings where each character represents a board position:
- `B` = Black piece
- `W` = White piece
- `-` = Empty square

Example for 4x4 board (16 characters):
```
--B--BB--WWW----
```

With player information:
```
p=1_--B--BB--WWW----  # Player 1's turn
```

## AutoGUI Move Format

Moves are encoded as: `A_h_{position}_x`
- `A` = Action type
- `h` = Human move
- `{position}` = Index of the square (0-15 for 4x4, 0-63 for 8x8)
- `x` = End marker

Example: `A_h_15_x` means a piece was placed at position 15.

## Debug Visualization

The system generates debug images in the `masks/` directory:
- `bilateral_filtered_image.png` - Noise-reduced image
- `grid_image_with_cells.png` - Board with grid overlay
- `black_mask.png` / `white_mask.png` - Color detection masks
- `game_pieces_mask.png` - Combined piece detection
- `result_image.png` - Final processed result

## Contributing

This project is part of the GamesCrafters research group. Contributions are welcome for:
- Improved piece detection accuracy
- Support for different board materials/lighting
- Real-time processing optimization
- Additional board size support

## License

Part of the GamesCrafters project at UC Berkeley.

## Acknowledgments

Developed for the GamesCrafters research group to enable automatic game state extraction for computational game theory research.
