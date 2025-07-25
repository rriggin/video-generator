#!/bin/bash
# Simple setup and run script for the video generator
# Uses the existing requirements.txt file

set -e  # Exit on any error

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

echo -e "${GREEN}🎬 Video Generator Setup & Run Script${NC}"
echo "=========================================="

# Get the directory where this script is located
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(dirname "$SCRIPT_DIR")"
VENV_PATH="$PROJECT_ROOT/venv"

echo -e "${YELLOW}📁 Script directory: $SCRIPT_DIR${NC}"
echo -e "${YELLOW}📁 Project root: $PROJECT_ROOT${NC}"
echo -e "${YELLOW}🐍 Virtual environment: $VENV_PATH${NC}"

# Check if virtual environment exists
if [ ! -d "$VENV_PATH" ]; then
    echo -e "${YELLOW}🔧 Creating virtual environment...${NC}"
    python3 -m venv "$VENV_PATH"
fi

# Activate virtual environment
echo -e "${YELLOW}🔧 Activating virtual environment...${NC}"
source "$VENV_PATH/bin/activate"

# Verify activation
if [ $? -eq 0 ]; then
    echo -e "${GREEN}✅ Virtual environment activated${NC}"
    echo -e "${YELLOW}🐍 Python: $(which python)${NC}"
    echo -e "${YELLOW}🐍 Version: $(python --version)${NC}"
else
    echo -e "${RED}❌ Failed to activate virtual environment${NC}"
    exit 1
fi

# Install dependencies from requirements.txt
echo -e "${YELLOW}📦 Installing dependencies from requirements.txt...${NC}"
pip install -r "$PROJECT_ROOT/requirements.txt"

if [ $? -eq 0 ]; then
    echo -e "${GREEN}✅ Dependencies installed successfully${NC}"
else
    echo -e "${RED}❌ Failed to install dependencies${NC}"
    exit 1
fi

# Change to the video generator directory
cd "$SCRIPT_DIR"

# Check if the service is already running
if curl -s http://localhost:8000/ > /dev/null 2>&1; then
    echo -e "${YELLOW}⚠️  Service is already running on port 8000${NC}"
    echo -e "${YELLOW}   You can access it at: http://localhost:8000${NC}"
    echo -e "${YELLOW}   API docs at: http://localhost:8000/docs${NC}"
    echo ""
    echo -e "${GREEN}🎉 Setup complete! Service is ready to use.${NC}"
    exit 0
fi

# Start the service
echo -e "${YELLOW}🚀 Starting video generator service...${NC}"
echo -e "${GREEN}   Service will be available at: http://localhost:8000${NC}"
echo -e "${GREEN}   API docs at: http://localhost:8000/docs${NC}"
echo -e "${YELLOW}   Press Ctrl+C to stop the service${NC}"
echo ""

python -m uvicorn main:app --reload --host 0.0.0.0 --port 8000 