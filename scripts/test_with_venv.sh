#!/bin/bash
# Script to run tests with proper venv activation

# Get the directory where this script is located
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(dirname "$SCRIPT_DIR")"

echo "🧪 Running tests with virtual environment..."

# Activate the virtual environment
source "$PROJECT_ROOT/venv/bin/activate"

# Change to the video generator directory
cd "$SCRIPT_DIR"

# Run the test
python3 test_default_subtitles.py 