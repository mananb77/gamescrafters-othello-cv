#!/bin/bash

# Othello CV Backend - Start Server Script
# =========================================

echo "🎮 Othello CV Backend Server"
echo "============================="
echo ""

# Check if Python 3 is installed
if ! command -v python3 &> /dev/null; then
    echo "❌ Error: Python 3 is not installed"
    exit 1
fi

# Check if virtual environment exists
if [ ! -d "venv" ]; then
    echo "📦 Creating virtual environment..."
    python3 -m venv venv
fi

# Activate virtual environment
echo "🔧 Activating virtual environment..."
source venv/bin/activate

# Install/upgrade dependencies
echo "📥 Installing dependencies..."
pip install -q --upgrade pip
pip install -q -r requirements.txt

# Start the server
echo ""
echo "✅ Dependencies installed"
echo ""
echo "🚀 Starting Flask server..."
echo "📍 API will be available at: http://localhost:5000"
echo "💡 Press Ctrl+C to stop the server"
echo ""

python3 app.py
