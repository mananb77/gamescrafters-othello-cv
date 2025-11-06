# Othello CV Backend API

Flask-based REST API for live Othello board image and video processing.

## Features

- **Image Processing**: Upload images, get board state detection
- **Video Processing**: Upload videos, get move-by-move analysis
- **Real-time Results**: JSON responses with piece counts, states, and timing
- **CORS Enabled**: Works seamlessly with frontend demo
- **Error Handling**: Comprehensive validation and error messages

## Quick Start

### 1. Start the Server

```bash
cd backend
./start_server.sh
```

The server will start at `http://localhost:5000`

### 2. Test the API

**Health Check:**
```bash
curl http://localhost:5000/api/health
```

**Process an Image:**
```bash
curl -X POST -F "file=@test.png" -F "board_size=4" \
  http://localhost:5000/api/process
```

**Get Examples:**
```bash
curl http://localhost:5000/api/examples
```

## API Endpoints

### `GET /api/health`

Health check endpoint.

**Response:**
```json
{
  "status": "healthy",
  "service": "Othello CV API",
  "version": "1.0.0"
}
```

### `POST /api/process`

Process uploaded image or video file.

**Parameters (form-data):**
- `file` (required): Image (png, jpg, jpeg) or video (mp4, mov, avi)
- `board_size` (optional): `4` or `8` (default: 4)
- `annotate` (optional): `true` or `false` (default: false)
- `debug` (optional): `true` or `false` (default: false)

**Response (Image):**
```json
{
  "type": "image",
  "board_size": 4,
  "state": "-----BW-BWB-W---",
  "piece_count": {
    "black": 3,
    "white": 3,
    "empty": 10
  },
  "processing_time": 0.03
}
```

**Response (Video):**
```json
{
  "type": "video",
  "board_size": 4,
  "moves": [
    {
      "player": 1,
      "state": "-----BW-BWB-W---",
      "frame": 0
    },
    ...
  ],
  "total_moves": 13,
  "processing_time": 12.5
}
```

**Error Response:**
```json
{
  "error": "Invalid file type. Allowed: png, jpg, jpeg, mp4, mov, avi"
}
```

### `GET /api/examples`

Get list of example board states.

**Response:**
```json
[
  {
    "id": "4x4-early",
    "name": "4x4 Early Game",
    "board_size": 4,
    "state": "-----BW-BWB-W---",
    "description": "GamesmanUni - 3B 3W - 6 moves"
  },
  ...
]
```

## Manual Setup

If you prefer manual setup:

```bash
# Create virtual environment
python3 -m venv venv

# Activate it
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Run the server
python3 app.py
```

## Configuration

Edit `app.py` to modify:

- **Port**: Change `port=5000` in `app.run()`
- **Max File Size**: Modify `MAX_FILE_SIZE` (default: 50MB)
- **Allowed Extensions**: Update `ALLOWED_EXTENSIONS` set
- **Debug Mode**: Set `debug=False` for production

## Integration with Frontend

The frontend automatically connects to `http://localhost:5000` when running locally.

To use with the demo website:

1. Start the backend: `./start_server.sh`
2. Open the website in your browser
3. Go to "Live Demo" tab
4. Upload an image or video

## Deployment

### Local Development

- Backend: `http://localhost:5000`
- Frontend: `http://localhost:8000`

### Production Deployment

**Option 1: Heroku**
```bash
# Install Heroku CLI
# https://devcenter.heroku.com/articles/heroku-cli

# Login and create app
heroku login
heroku create othello-cv-api

# Deploy
git push heroku main
```

**Option 2: Railway**
```bash
# Install Railway CLI
# https://docs.railway.app/develop/cli

# Login and deploy
railway login
railway init
railway up
```

**Option 3: DigitalOcean App Platform**
- Connect your GitHub repository
- Set build command: `pip install -r backend/requirements.txt`
- Set run command: `python backend/app.py`

### Environment Variables

For production, set:
```bash
FLASK_ENV=production
PORT=5000
```

## Testing

Test all endpoints:

```bash
# Health check
curl http://localhost:5000/api/health

# Upload 4x4 image
curl -X POST -F "file=@uploads/random-board-gamesman-uni.png" \
  -F "board_size=4" \
  http://localhost:5000/api/process

# Upload 8x8 video
curl -X POST -F "file=@uploads/input-othello-8x8-vid.mp4" \
  -F "board_size=8" \
  http://localhost:5000/api/process

# Get examples
curl http://localhost:5000/api/examples
```

## Troubleshooting

**Port already in use:**
```bash
# Kill process on port 5000
lsof -ti:5000 | xargs kill -9
```

**Module not found:**
```bash
# Reinstall dependencies
pip install -r requirements.txt
```

**CORS errors:**
- Ensure Flask-CORS is installed
- Check browser console for specific errors
- Verify API URL in frontend code

**Processing errors:**
- Check file format (png, jpg, mp4 supported)
- Verify board size (4 or 8)
- Check server logs for detailed errors

## Architecture

```
backend/
├── app.py              # Flask API server
├── requirements.txt    # Python dependencies
├── start_server.sh     # Startup script
└── README.md          # This file

Main Components:
- Flask: Web framework
- Flask-CORS: Cross-origin resource sharing
- OthelloCV: Core CV processing (from parent dir)
- Werkzeug: File upload handling
```

## Security Notes

- **File Validation**: Only allowed extensions accepted
- **File Size Limit**: 50MB maximum
- **Temporary Storage**: Files deleted after processing
- **Secure Filenames**: Werkzeug sanitization applied
- **Error Handling**: No sensitive info in error messages

## Performance

- **Image Processing**: ~0.03-0.05s per image
- **Video Processing**: ~0.8-1.2s per second of video
- **Memory Usage**: ~100-200MB typical
- **Concurrent Requests**: Supports multiple simultaneous uploads

## License

Part of the Othello CV project.
Built in GamesCrafters at UC Berkeley under Professor Dan Garcia.

## Support

For issues or questions:
- Check the main project README
- Review test results in `test_results/`
- Check Flask logs for debugging
