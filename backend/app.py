#!/usr/bin/env python3
"""
Othello CV Backend API
Flask server for live image/video processing
"""

import os
import sys
import json
import tempfile
from flask import Flask, request, jsonify, send_file
from flask_cors import CORS
from werkzeug.utils import secure_filename
import cv2

# Add parent directory to path to import othello_cv
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from othello_cv import OthelloCV

app = Flask(__name__)
CORS(app)  # Enable CORS for all routes

# Configuration
UPLOAD_FOLDER = tempfile.gettempdir()
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'mp4', 'mov', 'avi'}
MAX_FILE_SIZE = 50 * 1024 * 1024  # 50MB

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['MAX_CONTENT_LENGTH'] = MAX_FILE_SIZE


def allowed_file(filename):
    """Check if file extension is allowed"""
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


def is_video(filename):
    """Check if file is a video"""
    ext = filename.rsplit('.', 1)[1].lower()
    return ext in {'mp4', 'mov', 'avi'}


@app.route('/api/health', methods=['GET'])
def health_check():
    """Health check endpoint"""
    return jsonify({
        'status': 'healthy',
        'service': 'Othello CV API',
        'version': '1.0.0'
    })


@app.route('/api/process', methods=['POST'])
def process_upload():
    """
    Process uploaded image or video

    Form data:
        - file: Image or video file
        - board_size: 4 or 8 (default: 4)
        - annotate: true/false (default: false)
        - debug: true/false (default: false)

    Returns:
        JSON with processing results
    """
    # Check if file was uploaded
    if 'file' not in request.files:
        return jsonify({'error': 'No file provided'}), 400

    file = request.files['file']

    if file.filename == '':
        return jsonify({'error': 'No file selected'}), 400

    if not allowed_file(file.filename):
        return jsonify({'error': 'Invalid file type. Allowed: png, jpg, jpeg, mp4, mov, avi'}), 400

    # Get parameters
    board_size = int(request.form.get('board_size', 4))
    annotate = request.form.get('annotate', 'false').lower() == 'true'
    debug = request.form.get('debug', 'false').lower() == 'true'

    if board_size not in [4, 8]:
        return jsonify({'error': 'board_size must be 4 or 8'}), 400

    try:
        # Save uploaded file
        filename = secure_filename(file.filename)
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(filepath)

        # Initialize Othello CV
        cv_processor = OthelloCV(board_size=board_size)

        # Process based on file type
        is_vid = is_video(filename)

        if is_vid:
            # Process video
            output_path = None
            if annotate:
                output_path = os.path.join(app.config['UPLOAD_FOLDER'], f'annotated_{filename}')

            result = cv_processor.process_video(
                filepath,
                save_debug=debug,
                output_video_path=output_path
            )

            # Clean up uploaded file
            os.remove(filepath)

            if result is None:
                return jsonify({'error': 'Video processing failed'}), 500

            # Extract moves from result dict
            moves = result.get('moves', [])

            # Format response
            response = {
                'type': 'video',
                'board_size': board_size,
                'moves': moves,
                'total_moves': result.get('total_moves', len(moves)),
                'total_frames': result.get('total_frames', 0),
                'processing_time': 0  # Video processing doesn't track time per move
            }

        else:
            # Process image
            result = cv_processor.process_image(
                filepath,
                save_debug=debug
            )

            # Clean up uploaded file
            os.remove(filepath)

            if result is None or 'state' not in result:
                return jsonify({'error': 'Image processing failed'}), 500

            state = result['state']
            processing_time = result.get('processing_time', 0)

            # Count pieces
            piece_count = {
                'black': state.count(1),
                'white': state.count(-1),
                'empty': state.count(0)
            }

            # Convert state to string format
            state_str = ''.join(['B' if x == 1 else 'W' if x == -1 else '-' for x in state])

            # Format response
            response = {
                'type': 'image',
                'board_size': board_size,
                'state': state_str,
                'piece_count': piece_count,
                'processing_time': processing_time
            }

        return jsonify(response)

    except Exception as e:
        # Clean up on error
        if os.path.exists(filepath):
            os.remove(filepath)

        return jsonify({'error': f'Processing failed: {str(e)}'}), 500


@app.route('/api/examples', methods=['GET'])
def get_examples():
    """Get list of example boards"""
    examples = [
        {
            'id': '4x4-early',
            'name': '4x4 Early Game',
            'board_size': 4,
            'state': '-----BW-BWB-W---',
            'description': 'GamesmanUni - 3B 3W - 6 moves'
        },
        {
            'id': '8x8-opening',
            'name': '8x8 Opening',
            'board_size': 8,
            'state': '---------------------------WB------BW---------------------------',
            'description': 'Standard - 2B 2W - Classic start'
        },
        {
            'id': '4x4-complex',
            'name': '4x4 Late Game',
            'board_size': 4,
            'state': 'W-WBWWB-WWBBWBW-',
            'description': 'GamesmanUni - 5B 9W - Near end'
        }
    ]
    return jsonify(examples)


@app.errorhandler(413)
def request_entity_too_large(error):
    """Handle file too large error"""
    return jsonify({'error': 'File too large. Maximum size is 50MB'}), 413


@app.errorhandler(500)
def internal_error(error):
    """Handle internal server error"""
    return jsonify({'error': 'Internal server error'}), 500


if __name__ == '__main__':
    print("🚀 Starting Othello CV Backend API...")
    print("📍 Server: http://localhost:5001")
    print("🔗 API Endpoint: http://localhost:5001/api/process")
    print("💚 Health Check: http://localhost:5001/api/health")
    print()

    app.run(debug=True, host='0.0.0.0', port=5001)
