#!/bin/bash
# Simple script to start the video generator service
# This eliminates venv confusion by handling the path correctly

# Get the directory where this script is located
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(dirname "$SCRIPT_DIR")"

echo "🎬 Starting Video Generator Service..."
echo "📁 Script directory: $SCRIPT_DIR"
echo "📁 Project root: $PROJECT_ROOT"

# Activate the virtual environment
echo "🔧 Activating virtual environment..."
source "$PROJECT_ROOT/venv/bin/activate"

# Check if activation worked
if [ $? -eq 0 ]; then
    echo "✅ Virtual environment activated successfully"
    echo "🐍 Python path: $(which python)"
    echo "🐍 Python version: $(python --version)"
else
    echo "❌ Failed to activate virtual environment"
    exit 1
fi

# Change to the project root directory
cd "$PROJECT_ROOT"

# Start the service
echo "🚀 Starting video generator service..."
python app.py 