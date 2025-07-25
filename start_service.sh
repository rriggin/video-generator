#!/bin/bash

# Bulletproof Video Generator Startup Script
# This ensures the virtual environment is properly activated and dependencies are installed

set -e  # Exit on any error

echo "🚀 Starting Video Generator Service..."

# Navigate to project directory
cd "$(dirname "$0")"

# Create virtual environment if it doesn't exist
if [ ! -d "venv" ]; then
    echo "📦 Creating virtual environment..."
    python3 -m venv venv
fi

# Always use venv's Python and pip directly (no activation needed)
PYTHON="./venv/bin/python3"
PIP="./venv/bin/pip"

# Check if requirements need to be installed/updated
echo "🔍 Checking dependencies..."
if [ ! -f "venv/.requirements_installed" ] || [ "requirements.txt" -nt "venv/.requirements_installed" ]; then
    echo "📥 Installing/updating dependencies..."
    $PIP install --upgrade pip
    $PIP install -r requirements.txt
    touch venv/.requirements_installed
    echo "✅ Dependencies up to date"
else
    echo "✅ Dependencies already current"
fi

# Start the service
echo "🎬 Starting video generator on http://localhost:8000"
echo "🛑 Press Ctrl+C to stop"
$PYTHON app.py 