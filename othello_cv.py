"""
Othello Computer Vision Library
================================
Core CV processing for Othello board detection and game state extraction.

Supports both 4x4 (GamesmanUni) and 8x8 (standard) Othello boards.
"""

import cv2
import numpy as np
from typing import List, Tuple, Dict, Optional
import json


class OthelloCV:
    """
    Computer vision processor for Othello game boards.

    Attributes:
        board_size (int): Size of the board (4 or 8)
        resize_width (int): Width to resize frames for processing
        skip_frames (int): Number of frames to skip in video processing
        motion_threshold (int): Threshold for motion detection
        color_threshold (float): Threshold for piece color detection (0-1)
    """

    def __init__(
        self,
        board_size: int = 4,
        resize_width: int = 500,
        skip_frames: int = 20,
        motion_threshold: int = 10,
        color_threshold: float = 0.3
    ):
        """
        Initialize Othello CV processor.

        Args:
            board_size: Board dimensions (4 or 8)
            resize_width: Width to resize images for processing
            skip_frames: Frames to skip in video processing
            motion_threshold: Threshold for motion detection
            color_threshold: Threshold for piece detection (0-1)
        """
        if board_size not in [4, 8]:
            raise ValueError("Board size must be 4 or 8")

        self.board_size = board_size
        self.board_width = board_size
        self.board_height = board_size
        self.resize_width = resize_width
        self.skip_frames = skip_frames
        self.motion_threshold = motion_threshold
        self.color_threshold = color_threshold

        # HSV color ranges for piece detection (RGB values)
        self.BLACK_LOWER = np.array([0, 0, 0])
        self.BLACK_UPPER = np.array([110, 110, 110])
        self.WHITE_LOWER = np.array([150, 150, 150])
        self.WHITE_UPPER = np.array([255, 255, 255])

        # UI color ranges to mask out (for GamesmanUni interface)
        self.RED_LOWER = np.array([80, 0, 0])
        self.RED_UPPER = np.array([150, 50, 50])
        self.GREEN_LOWER = np.array([0, 110, 0])
        self.GREEN_UPPER = np.array([30, 150, 30])
        self.YELLOW_LOWER = np.array([216, 216, 39])
        self.YELLOW_UPPER = np.array([255, 255, 77])

    def process_image(self, image_path: str, save_debug: bool = False) -> Dict:
        """
        Process a single image and extract board state.

        Args:
            image_path: Path to the image file
            save_debug: Whether to save debug visualization images

        Returns:
            Dictionary with board state and metadata
        """
        image = cv2.imread(image_path)
        if image is None:
            raise ValueError(f"Could not load image: {image_path}")

        grid = self.process_frame(image, save_debug=save_debug)
        state_string = self.grid_to_position_string(grid)

        return {
            "board_size": self.board_size,
            "state": state_string,
            "grid": grid.tolist(),
            "image_path": image_path
        }

    def process_video(
        self,
        video_path: str,
        save_debug: bool = False,
        output_video_path: Optional[str] = None
    ) -> Dict:
        """
        Process a video and extract all game states.

        Args:
            video_path: Path to the video file
            save_debug: Whether to save debug images
            output_video_path: Optional path to save annotated video

        Returns:
            Dictionary with game moves and metadata
        """
        cap = cv2.VideoCapture(video_path)
        if not cap.isOpened():
            raise ValueError(f"Could not open video: {video_path}")

        # Setup video writer if output requested
        video_writer = None
        if output_video_path:
            fps = int(cap.get(cv2.CAP_PROP_FPS))
            width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
            height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
            fourcc = cv2.VideoWriter_fourcc(*'mp4v')
            video_writer = cv2.VideoWriter(output_video_path, fourcc, fps, (width, height))

        # Read first frame for motion detection
        ret, previous_frame = cap.read()
        if not ret:
            raise ValueError("Could not read first frame from video")

        previous_frame_gray = cv2.cvtColor(previous_frame, cv2.COLOR_BGR2GRAY)
        previous_frame_gray = cv2.GaussianBlur(previous_frame_gray, (21, 21), 0)

        # Initialize tracking variables
        previous_position_string = '-' * (self.board_size * self.board_size)
        moves = []
        frame_count = 0
        player = 1

        # Process video frames
        while cap.isOpened():
            ret, frame = cap.read()
            if not ret:
                break

            # Convert frame for motion detection
            gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            gray = cv2.GaussianBlur(gray, (21, 21), 0)

            # Process frame at intervals when no motion detected
            if frame_count % self.skip_frames == 0:
                if not self._is_motion(previous_frame_gray, gray):
                    # Process the stable frame
                    grid = self.process_frame(frame, save_debug=False)
                    current_position_string = self.grid_to_position_string(grid)

                    # Check if state changed
                    if current_position_string != previous_position_string:
                        moves.append({
                            "player": player,
                            "state": current_position_string,
                            "frame": frame_count
                        })
                        player = (player % 2) + 1  # Toggle between 1 and 2
                        previous_position_string = current_position_string

                    # Annotate frame if saving video
                    if video_writer:
                        annotated_frame = self._annotate_frame(frame.copy(), grid)
                        video_writer.write(annotated_frame)

                previous_frame_gray = gray

            frame_count += 1

        # Cleanup
        cap.release()
        if video_writer:
            video_writer.release()

        return {
            "board_size": self.board_size,
            "moves": moves,
            "total_moves": len(moves),
            "total_frames": frame_count,
            "video_path": video_path,
            "output_video": output_video_path
        }

    def process_frame(self, frame: np.ndarray, save_debug: bool = False) -> np.ndarray:
        """
        Process a single frame and return the board grid.

        Args:
            frame: Input frame as numpy array
            save_debug: Whether to save debug images

        Returns:
            2D numpy array representing the board
            (1 = black, -1 = white, 0 = empty)
        """
        # Resize frame
        img_h, img_w = frame.shape[:2]
        scale = self.resize_width / img_w
        img_w = int(img_w * scale)
        img_h = int(img_h * scale)
        img = cv2.resize(frame, (img_w, img_h), interpolation=cv2.INTER_AREA)

        # Apply bilateral filter to reduce noise
        bilateral_filtered = cv2.bilateralFilter(img, 15, 190, 190)

        if save_debug:
            cv2.imwrite('masks/bilateral_filtered_image.png', bilateral_filtered)

        # Calculate grid cell dimensions
        cell_width = img_w // self.board_width
        cell_height = img_h // self.board_height

        # Create debug visualization with grid
        if save_debug:
            grid_image = img.copy()
            for i in range(1, self.board_width):
                cv2.line(grid_image, (i * cell_width, 0),
                        (i * cell_width, img_h), (0, 255, 0), 1)
            for i in range(1, self.board_height):
                cv2.line(grid_image, (0, i * cell_height),
                        (img_w, i * cell_height), (0, 255, 0), 1)
            cv2.imwrite('masks/grid_image_with_cells.png', grid_image)

        # Initialize grid
        grid = np.zeros((self.board_height, self.board_width), dtype=int)

        # Create color masks
        white_mask = cv2.inRange(bilateral_filtered, self.WHITE_LOWER, self.WHITE_UPPER)
        black_mask = cv2.inRange(bilateral_filtered, self.BLACK_LOWER, self.BLACK_UPPER)

        if save_debug:
            cv2.imwrite('masks/white_mask.png', white_mask)
            cv2.imwrite('masks/black_mask.png', black_mask)
            game_pieces_mask = black_mask + white_mask
            cv2.imwrite('masks/game_pieces_mask.png', game_pieces_mask)

        # Analyze each cell
        for row in range(self.board_height):
            for col in range(self.board_width):
                x_start = col * cell_width
                y_start = row * cell_height

                grid[row, col] = self._process_cell(
                    bilateral_filtered,
                    x_start, y_start,
                    cell_width, cell_height,
                    save_debug=(save_debug and row == 0 and col == 0)
                )

        return grid

    def _process_cell(
        self,
        img: np.ndarray,
        x_start: int,
        y_start: int,
        width: int,
        height: int,
        save_debug: bool = False
    ) -> int:
        """
        Process a single cell and determine piece color.

        Returns:
            1 for black, -1 for white, 0 for empty
        """
        # Crop the cell
        cell_img = img[y_start:y_start + height, x_start:x_start + width]

        if save_debug:
            cv2.imwrite('masks/cell_img.png', cell_img)

        # Create masks for this cell
        white_mask_cell = cv2.inRange(cell_img, self.WHITE_LOWER, self.WHITE_UPPER)
        black_mask_cell = cv2.inRange(cell_img, self.BLACK_LOWER, self.BLACK_UPPER)

        if save_debug:
            cv2.imwrite('masks/white_mask_cell.png', white_mask_cell)
            cv2.imwrite('masks/black_mask_cell.png', black_mask_cell)

        # Determine piece color based on dominant color
        if self._is_color_dominant(white_mask_cell):
            return -1  # White piece
        elif self._is_color_dominant(black_mask_cell):
            return 1   # Black piece
        else:
            return 0   # Empty

    def _is_color_dominant(self, mask: np.ndarray) -> bool:
        """
        Check if a color is dominant in the mask.

        Args:
            mask: Binary mask to analyze

        Returns:
            True if color covers more than threshold percentage
        """
        white_pixels = cv2.countNonZero(mask)
        white_area_ratio = white_pixels / mask.size
        return white_area_ratio > self.color_threshold

    def _is_motion(self, previous_frame: np.ndarray, current_frame: np.ndarray) -> bool:
        """
        Detect motion between two frames.

        Args:
            previous_frame: Previous frame (grayscale)
            current_frame: Current frame (grayscale)

        Returns:
            True if motion detected
        """
        frame_delta = cv2.absdiff(previous_frame, current_frame)
        thresholded = cv2.threshold(frame_delta, 25, 255, cv2.THRESH_BINARY)[1]
        motion_level = np.sum(thresholded)
        return motion_level > self.motion_threshold

    def _annotate_frame(self, frame: np.ndarray, grid: np.ndarray) -> np.ndarray:
        """
        Annotate frame with detected pieces and grid.

        Args:
            frame: Input frame
            grid: Detected board state

        Returns:
            Annotated frame
        """
        img_h, img_w = frame.shape[:2]
        cell_width = img_w // self.board_width
        cell_height = img_h // self.board_height

        # Draw grid lines
        for i in range(1, self.board_width):
            cv2.line(frame, (i * cell_width, 0),
                    (i * cell_width, img_h), (0, 255, 0), 2)
        for i in range(1, self.board_height):
            cv2.line(frame, (0, i * cell_height),
                    (img_w, i * cell_height), (0, 255, 0), 2)

        # Draw piece labels
        for row in range(self.board_height):
            for col in range(self.board_width):
                if grid[row, col] != 0:
                    x_center = col * cell_width + cell_width // 2
                    y_center = row * cell_height + cell_height // 2

                    label = 'B' if grid[row, col] == 1 else 'W'
                    color = (255, 255, 255) if grid[row, col] == 1 else (0, 0, 0)

                    cv2.putText(frame, label, (x_center - 10, y_center + 10),
                               cv2.FONT_HERSHEY_SIMPLEX, 0.8, color, 2)

        return frame

    def grid_to_position_string(self, grid: np.ndarray) -> str:
        """
        Convert grid to position string.

        Args:
            grid: 2D numpy array representing the board

        Returns:
            String representation (e.g., '-----WB--BW-----')
        """
        rows, cols = grid.shape
        position_string = ''

        # Iterate column-first for Othello convention
        for col in range(cols):
            for row in range(rows):
                if grid[row, col] == 1:
                    position_string += 'B'
                elif grid[row, col] == -1:
                    position_string += 'W'
                else:
                    position_string += '-'

        return position_string

    def format_moves_as_text(self, moves: List[Dict]) -> str:
        """
        Format moves as text output.

        Args:
            moves: List of move dictionaries

        Returns:
            Formatted text string
        """
        lines = []
        for i, move in enumerate(moves, 1):
            lines.append(f"Move {i}: Player {move['player']} - {move['state']} (frame {move['frame']})")
        return '\n'.join(lines)

    def format_moves_as_json(self, result: Dict, pretty: bool = True) -> str:
        """
        Format result as JSON.

        Args:
            result: Result dictionary from process_video or process_image
            pretty: Whether to pretty-print JSON

        Returns:
            JSON string
        """
        indent = 2 if pretty else None
        return json.dumps(result, indent=indent)
