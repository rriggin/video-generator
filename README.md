# 🎬 Video Generator Agent

A FastAPI-based service that generates training videos from slides and narration scripts.

## ⚠️ IMPORTANT: Complete Workflow

**Use ALL 3 endpoints in sequence:**

1. **Upload PDF** → `/upload-pdf` → Get slides
2. **Parse Script** → `/parse-script` → Get timed segments  
3. **Generate Video** → `/generate-video` → Combine slides + script

**DON'T skip step 2!** See `docs/API_WORKFLOW.md` for examples.

## 🚀 Quick Start

### Option 1: One-Command Setup (Recommended)
```bash
cd agents/video-generator-agent
./setup_and_run.sh
```

This script will:
- Create/activate the virtual environment
- Install all dependencies from `requirements.txt`
- Start the service on http://localhost:8000

### Option 2: Manual Setup
```bash
# Navigate to the project root
cd /path/to/goskills

# Create and activate virtual environment
python3 -m venv venv
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Navigate to video generator
cd agents/video-generator-agent

# Start the service
python -m uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

## 📋 Dependencies

All dependencies are managed through the project's `requirements.txt` file:

- **FastAPI** - Web framework
- **Uvicorn** - ASGI server
- **MoviePy** - Video processing
- **gTTS** - Text-to-speech
- **Pillow** - Image processing
- **PDF2Image** - PDF conversion
- **Pydantic** - Data validation

## 🔧 Configuration

### Subtitle Settings
- **Default**: Subtitles are **OFF** by default for faster generation
- **Enable**: Set `"include_subtitles": true` in your request
- **Disable**: Set `"include_subtitles": false` or omit the field (default behavior)

### Video Quality
- **720p** (default): 1280x720
- **1080p**: 1920x1080

## 📡 API Endpoints

- **Health Check**: `GET /`
- **Generate Video**: `POST /generate-video`
- **Upload PDF**: `POST /upload-pdf`
- **Parse Script**: `POST /parse-script`
- **Upload Slide**: `POST /upload-slide`
- **API Docs**: `GET /docs`

## 🎯 Example Usage

```bash
# Generate a video with subtitles disabled (default)
curl -X POST http://localhost:8000/generate-video \
  -H "Content-Type: application/json" \
  -d '{
    "slides": ["slide1.png", "slide2.png"],
    "script": [
      {"text": "Welcome to our course", "duration": 5, "slide": "slide1.png"},
      {"text": "This is the second slide", "duration": 6, "slide": "slide2.png"}
    ],
    "voice": "female",
    "video_quality": "720p"
  }'

# Generate a video with subtitles enabled
curl -X POST http://localhost:8000/generate-video \
  -H "Content-Type: application/json" \
  -d '{
    "slides": ["slide1.png"],
    "script": [{"text": "Welcome", "duration": 5, "slide": "slide1.png"}],
    "include_subtitles": true,
    "voice": "female"
  }'
```

## 🧪 Testing

Run tests with the virtual environment:
```bash
./test_with_venv.sh
```

## 📁 Project Structure

```
video-generator-agent/
├── main.py                 # FastAPI application
├── video_builder.py        # Core video generation logic
├── generate_audio.py       # Text-to-speech functionality
├── setup_and_run.sh       # One-command setup script
├── test_with_venv.sh      # Test runner script
├── input/                 # Input files (PDFs, scripts, images)
├── output/                # Generated videos and assets
└── README.md             # This file
```

## 🔄 Development

The service uses `--reload` flag, so changes to Python files will automatically restart the server.

## 🐛 Troubleshooting

### Virtual Environment Issues
- Use the `setup_and_run.sh` script to avoid venv path issues
- Ensure you're in the correct directory when running commands

### Port Already in Use
- The script will detect if the service is already running
- Kill existing processes: `pkill -f uvicorn`

### Missing Dependencies
- Run `./setup_and_run.sh` to reinstall all dependencies
- Check that `requirements.txt` is up to date 