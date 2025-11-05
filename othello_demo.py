#!/usr/bin/env python3
"""
Othello Computer Vision Demo
============================
Command-line interface for processing Othello game videos and images.

Usage:
    python othello_demo.py --video input.mov --board-size 4 --json
    python othello_demo.py --image board.png --board-size 8 --annotate
"""

import argparse
import sys
import os
import time
from pathlib import Path
from othello_cv import OthelloCV


def main():
    parser = argparse.ArgumentParser(
        description='Othello Computer Vision Demo - Process videos and images of Othello games',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Process a 4x4 video and output JSON
  python othello_demo.py --video uploads/input-othello-4x4.mov --board-size 4 --json

  # Process an 8x8 video with annotated output
  python othello_demo.py --video uploads/input-othello-8x8.mov --board-size 8 --annotate

  # Process an image with debug visualizations
  python othello_demo.py --image uploads/board.png --board-size 4 --debug

  # Process video and save all outputs
  python othello_demo.py --video input.mov --board-size 8 --json --annotate --debug --output results/
        """
    )

    # Input options
    input_group = parser.add_mutually_exclusive_group(required=True)
    input_group.add_argument(
        '--video', '-v',
        type=str,
        help='Path to video file to process'
    )
    input_group.add_argument(
        '--image', '-i',
        type=str,
        help='Path to image file to process'
    )

    # Configuration options
    parser.add_argument(
        '--board-size', '-b',
        type=int,
        choices=[4, 8],
        default=4,
        help='Board size (4 for GamesmanUni, 8 for standard Othello) [default: 4]'
    )
    parser.add_argument(
        '--skip-frames',
        type=int,
        default=20,
        help='Number of frames to skip in video processing [default: 20]'
    )
    parser.add_argument(
        '--color-threshold',
        type=float,
        default=0.3,
        help='Threshold for piece color detection (0-1) [default: 0.3]'
    )

    # Output format options
    parser.add_argument(
        '--json', '-j',
        action='store_true',
        help='Output results as JSON'
    )
    parser.add_argument(
        '--annotate', '-a',
        action='store_true',
        help='Generate annotated video/image with detected pieces'
    )
    parser.add_argument(
        '--debug', '-d',
        action='store_true',
        help='Save debug visualizations (masks, grids, etc.)'
    )
    parser.add_argument(
        '--output', '-o',
        type=str,
        help='Output directory for results [default: current directory]'
    )

    # Parse arguments
    args = parser.parse_args()

    # Setup output directory
    if args.output:
        output_dir = Path(args.output)
        output_dir.mkdir(parents=True, exist_ok=True)
    else:
        output_dir = Path('.')

    # Create masks directory for debug output
    if args.debug:
        masks_dir = Path('masks')
        masks_dir.mkdir(exist_ok=True)

    # Initialize CV processor
    print(f"Initializing Othello CV with board size: {args.board_size}x{args.board_size}")
    processor = OthelloCV(
        board_size=args.board_size,
        skip_frames=args.skip_frames,
        color_threshold=args.color_threshold
    )

    # Process input
    start_time = time.time()

    try:
        if args.video:
            print(f"\nProcessing video: {args.video}")
            print(f"Skip frames: {args.skip_frames}")
            print(f"Color threshold: {args.color_threshold}")
            print("-" * 60)

            # Check if file exists
            if not os.path.exists(args.video):
                print(f"Error: Video file not found: {args.video}", file=sys.stderr)
                sys.exit(1)

            # Setup output video path if annotate requested
            output_video_path = None
            if args.annotate:
                video_name = Path(args.video).stem
                output_video_path = str(output_dir / f"{video_name}_annotated.mp4")
                print(f"Annotated video will be saved to: {output_video_path}")

            # Process video
            result = processor.process_video(
                args.video,
                save_debug=args.debug,
                output_video_path=output_video_path
            )

            # Output results
            processing_time = time.time() - start_time
            result['processing_time'] = round(processing_time, 2)

            print(f"\nProcessing complete!")
            print(f"Total moves detected: {result['total_moves']}")
            print(f"Total frames processed: {result['total_frames']}")
            print(f"Processing time: {processing_time:.2f}s")
            print("-" * 60)

            # Display moves
            if result['moves']:
                print("\nDetected moves:")
                for i, move in enumerate(result['moves'], 1):
                    print(f"  Move {i}: Player {move['player']} - {move['state']} (frame {move['frame']})")
            else:
                print("\nNo moves detected in video.")

            # Save JSON output
            if args.json:
                json_path = output_dir / f"{Path(args.video).stem}_result.json"
                with open(json_path, 'w') as f:
                    f.write(processor.format_moves_as_json(result, pretty=True))
                print(f"\nJSON output saved to: {json_path}")

            # Save text output
            text_path = output_dir / f"{Path(args.video).stem}_moves.txt"
            with open(text_path, 'w') as f:
                f.write(f"Othello CV Analysis\n")
                f.write(f"Video: {args.video}\n")
                f.write(f"Board size: {args.board_size}x{args.board_size}\n")
                f.write(f"Total moves: {result['total_moves']}\n")
                f.write(f"Processing time: {processing_time:.2f}s\n")
                f.write(f"\n{'-' * 60}\n\n")
                if result['moves']:
                    f.write(processor.format_moves_as_text(result['moves']))
                else:
                    f.write("No moves detected.")
            print(f"Text output saved to: {text_path}")

        elif args.image:
            print(f"\nProcessing image: {args.image}")
            print(f"Color threshold: {args.color_threshold}")
            print("-" * 60)

            # Check if file exists
            if not os.path.exists(args.image):
                print(f"Error: Image file not found: {args.image}", file=sys.stderr)
                sys.exit(1)

            # Process image
            result = processor.process_image(
                args.image,
                save_debug=args.debug
            )

            # Output results
            processing_time = time.time() - start_time
            result['processing_time'] = round(processing_time, 2)

            print(f"\nProcessing complete!")
            print(f"Board state: {result['state']}")
            print(f"Processing time: {processing_time:.2f}s")
            print("-" * 60)

            # Display grid
            print("\nDetected board:")
            grid = result['grid']
            for row in grid:
                row_str = ' '.join(['B' if cell == 1 else 'W' if cell == -1 else '-' for cell in row])
                print(f"  {row_str}")

            # Save JSON output
            if args.json:
                json_path = output_dir / f"{Path(args.image).stem}_result.json"
                with open(json_path, 'w') as f:
                    f.write(processor.format_moves_as_json(result, pretty=True))
                print(f"\nJSON output saved to: {json_path}")

            # Save annotated image
            if args.annotate:
                import cv2
                import numpy as np

                image = cv2.imread(args.image)
                grid_array = np.array(result['grid'])
                annotated_image = processor._annotate_frame(image, grid_array)

                output_image_path = output_dir / f"{Path(args.image).stem}_annotated.png"
                cv2.imwrite(str(output_image_path), annotated_image)
                print(f"Annotated image saved to: {output_image_path}")

            # Save text output
            text_path = output_dir / f"{Path(args.image).stem}_state.txt"
            with open(text_path, 'w') as f:
                f.write(f"Othello CV Analysis\n")
                f.write(f"Image: {args.image}\n")
                f.write(f"Board size: {args.board_size}x{args.board_size}\n")
                f.write(f"Board state: {result['state']}\n")
                f.write(f"Processing time: {processing_time:.2f}s\n")
            print(f"Text output saved to: {text_path}")

        # Debug output info
        if args.debug:
            print(f"\nDebug visualizations saved to: masks/")
            print("  - bilateral_filtered_image.png")
            print("  - grid_image_with_cells.png")
            print("  - black_mask.png / white_mask.png")
            print("  - game_pieces_mask.png")

        print("\nDone!")

    except Exception as e:
        print(f"\nError: {e}", file=sys.stderr)
        if args.debug:
            import traceback
            traceback.print_exc()
        sys.exit(1)


if __name__ == '__main__':
    main()
