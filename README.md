# 🎬 Video Generator Service

A FastAPI-based service that generates training videos from slides and narration scripts. **Designed for programmatic access by CustomGPT and other AI systems.**

## ⚠️ IMPORTANT: Complete Workflow

**Use ALL 3 endpoints in sequence:**

1. **Upload PDF** → `/upload-pdf` → Get slides
2. **Parse Script** → `/parse-script` → Get timed segments  
3. **Generate Video** → `/generate-video` → Combine slides + script

**DON'T skip step 2!** See `docs/API_WORKFLOW.md` for examples.

## 🚀 **Starting the Service**

### **✅ CORRECT Method (Always Use This)**
```bash
# Use the automated startup script
./start_service.sh
```

This script automatically:
- ✅ Creates virtual environment (if needed)
- ✅ Installs/updates dependencies from `requirements.txt`
- ✅ Starts the service on http://localhost:8000
- ✅ Handles all path and configuration issues

### **❌ DON'T Do This**
```bash
# Don't manually start these - use ./start_service.sh instead
python app.py
python3 app.py
uvicorn main:app --reload
source venv/bin/activate && python app.py
```

## 🧪 **Verifying the Service**

### **Health Check**
```bash
curl http://localhost:8000/
```
**Expected Response:**
```json
{
  "message": "Video Generator Service",
  "version": "1.0.0", 
  "status": "healthy"
}
```

### **API Documentation**
- **Interactive Docs**: http://localhost:8000/docs
- **OpenAPI Schema**: http://localhost:8000/openapi.json

## 📋 Dependencies

All dependencies are managed through `requirements.txt`:

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
- **Upload PDF**: `POST /upload-pdf`
- **Parse Script**: `POST /parse-script`
- **Generate Video**: `POST /generate-video`
- **Upload Slide**: `POST /upload-slide`
- **API Docs**: `GET /docs`

## 🎯 **CustomGPT Integration Example**

### **Complete Workflow**
```python
import requests

# Step 1: Upload PDF
with open('presentation.pdf', 'rb') as f:
    pdf_response = requests.post(
        'http://localhost:8000/upload-pdf',
        files={'file': f}
    )
slides_data = pdf_response.json()

# Step 2: Parse Script
with open('script.txt', 'rb') as f:
    script_response = requests.post(
        'http://localhost:8000/parse-script',
        files={'file': f}
    )
script_data = script_response.json()

# Step 3: Generate Video
video_response = requests.post(
    'http://localhost:8000/generate-video',
    json={
        "slides": slides_data["slide_files"],
        "script": script_data["parsed_segments"],
        "voice": "female",
        "include_subtitles": False,
        "video_quality": "720p"
    }
)
video_data = video_response.json()
print(f"Video ready: {video_data['video_url']}")
```

### **Simple cURL Examples**
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

### **Run Test Scripts**
```bash
# Test complete workflow
./scripts/test_complete_workflow.py

# Test PDF upload only
./scripts/test_pdf_upload.py

# Test with Ohio State data
./scripts/test_ohio_api.py
```

## 📁 Project Structure

```
video-generator/
├── start_service.sh          # 🚀 MAIN STARTUP SCRIPT
├── app.py                    # Entry point (used by startup script)
├── src/
│   ├── main.py              # FastAPI application
│   ├── video_builder.py     # Core video generation logic
│   └── generate_audio.py    # Text-to-speech functionality
├── input/                   # Input files (PDFs, scripts, images)
├── output/                  # Generated videos (gitignored)
├── temp/                    # Temporary files (gitignored)
├── logs/                    # Service logs (gitignored)
├── scripts/                 # Test and utility scripts
├── docs/                    # Documentation
├── requirements.txt         # Python dependencies
└── README.md               # This file
```

## 🔄 Development Workflow

### **Setup (First Time)**
```bash
git clone https://github.com/rriggin/video-generator.git
cd video-generator
./start_service.sh  # Handles everything automatically
```

### **Daily Development**
```bash
# Start service
./start_service.sh

# Make code changes...
# Service auto-reloads with --reload flag

# Stop service
Ctrl+C
```

## 🛠️ Troubleshooting

### **Service Won't Start**
```bash
# Check if port 8000 is busy
lsof -i :8000

# Kill existing processes
pkill -f uvicorn
./start_service.sh
```

### **Dependencies Issues**
```bash
# Force reinstall dependencies
rm venv/.requirements_installed
./start_service.sh
```

### **Import Errors**
- **Problem**: Usually path issues
- **Solution**: Always use `./start_service.sh` (handles paths correctly)

### **Permission Errors**
```bash
chmod +x start_service.sh
chmod +x scripts/*.sh
```

### **Virtual Environment Issues**
- Use `./start_service.sh` to avoid venv path issues
- The script handles virtual environment creation/activation automatically

## 🔒 **Security & Git**

### **Protected Files (in .gitignore)**
- `venv/` - Virtual environment
- `output/` - Generated videos  
- `temp/` - Temporary files
- `logs/` - Log files
- `input/pdfs/*.pdf` - Sensitive input files
- `input/scripts/*.txt` - Script files
- `.env*` - Environment files

### **Tracked Files**
- Source code (`src/`, `app.py`)
- Documentation (`docs/`, `README.md`)
- Configuration (`requirements.txt`)
- Scripts (`scripts/`)

## 📝 **Development Rules**

1. **Always use `./start_service.sh`** - Never manually start services
2. **Test before committing** - Run test scripts
3. **Keep sensitive files out of git** - Check .gitignore
4. **Document API changes** - Update docs/ folder
5. **Follow 3-step workflow** - Don't skip script parsing

## 🎯 **Ready for CustomGPT Integration!**

This service is designed specifically for **programmatic access** with:
- ✅ RESTful API endpoints
- ✅ JSON request/response format  
- ✅ File upload support
- ✅ Comprehensive error handling
- ✅ Automated testing suite
- ✅ Complete documentation

**Service URL**: http://localhost:8000  
**API Docs**: http://localhost:8000/docs

**GitHub Repository**: https://github.com/rriggin/video-generator 