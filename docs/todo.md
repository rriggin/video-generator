# 🎬 Video Generator Agent - Task List

## **Phase 1: Core Quality Improvements (High Priority)**

### **Task 1: Subtitle Display Enhancement** ✅ **COMPLETED**
- **Current Issue**: Subtitles may be hard to read or positioned poorly
- **Actions**:
  - [x] Review current subtitle positioning in `video_builder.py` (lines 400-450)
  - [x] Test different font sizes, colors, and positioning options
  - [x] Add subtitle toggle option in API (`include_subtitles: false`)
  - [x] Consider adding subtitle styling options (font, size, position, background)
  - [x] **Alternative**: Remove subtitles entirely if they're not adding value
- **Files to modify**: `video_builder.py`, `main.py`
- **Success criteria**: Clear, readable subtitles or clean removal
- **✅ Implementation**: Enhanced subtitle system with configurable positioning, styling, and background options

### **Task 2: Image Resolution & Quality Fix** ✅ **COMPLETED**
- **Current Issue**: Images appear blurry, possible cropping issues
- **Actions**:
  - [x] Review `resize_image()` method in `video_builder.py` (lines 350-380)
  - [x] Increase DPI settings in PDF conversion (increased from 300 to 600, configurable)
  - [x] Test different resampling methods (LANCZOS vs BICUBIC vs NEAREST) - now configurable
  - [x] Fix aspect ratio handling to prevent improper cropping - replaced with padding
  - [x] Add image quality validation before video generation
  - [x] Consider adding image preprocessing (sharpening, contrast adjustment) - implemented
- **Files to modify**: `video_builder.py`, `main.py`
- **Success criteria**: Sharp, clear images with proper aspect ratios
- **✅ Implementation**: 
  - **Enhanced PDF conversion**: Increased DPI from 300 to 600 (configurable up to 900)
  - **Improved resizing**: Added padding instead of aggressive cropping to preserve content
  - **Image preprocessing**: Added sharpness and contrast enhancement (configurable)
  - **Quality validation**: Added checks for resolution and blank images
  - **Configurable options**: Added `image_config` parameter with DPI, resampling, padding, enhancement settings
  - **New API endpoint**: `/image-config-examples` for testing different configurations

### **Task 3: Audio Quality & Voice Options**
- **Current Issue**: Choppy transitions, limited voice options
- **Actions**:
  - [ ] Research alternative TTS engines (ElevenLabs, Azure Speech, AWS Polly)
  - [ ] Test different gTTS parameters (speed, pitch, voice selection)
  - [ ] Add audio post-processing for smoother transitions
  - [ ] Implement voice selection in API (`voice: "male" | "female" | "custom"`)
  - [ ] Add audio fade-in/fade-out effects between segments
  - [ ] **Fallback**: If current solution can't be improved, document alternative TTS services for v2
- **Files to modify**: `video_builder.py`, `generate_audio.py`, `main.py`
- **Success criteria**: Smooth audio with multiple voice options

## **Phase 2: Content Enhancement (Medium Priority)**

### **Task 4: Script Enhancement with GoSkills Genie**
- **Current Issue**: Scripts are too dry/technical
- **Actions**:
  - [ ] Integrate with GoSkills Genie for more engaging script generation
  - [ ] Add script enhancement endpoint that calls Genie API
  - [ ] Implement script tone options (professional, conversational, enthusiastic)
  - [ ] Add script validation and improvement suggestions
  - [ ] Test with sample content to compare engagement levels
- **Files to modify**: `main.py` (new endpoint), integration with GoSkills Genie
- **Success criteria**: More engaging, varied script content

## **Phase 3: Architecture & Organization (Medium Priority)**

### **Task 5: Agent Directory Reorganization**
- **Current Issue**: Mixed agent types in directory structure
- **Actions**:
  - [ ] Review current agent structure vs. utilities
  - [ ] Create clear separation between true "agents" and utility components
  - [ ] Consider moving video-generator to `services/` if it's more of a utility
  - [ ] Update documentation to reflect new organization
  - [ ] Ensure consistent naming conventions across all agents
- **Files to modify**: Directory structure, documentation
- **Success criteria**: Cleaner, more logical project organization

### **Task 6: Standalone Codebase Preparation**
- **Current Issue**: Agent is embedded in larger project
- **Actions**:
  - [ ] Create new repository structure for standalone deployment
  - [ ] Extract video generator into its own package
  - [ ] Add proper dependency management (`requirements.txt`, `setup.py`)
  - [ ] Create deployment configuration (Docker, render.yaml, etc.)
  - [ ] Add simple web UI for non-technical users
  - [ ] Document API for external developers
- **Files to create**: New repository structure, deployment configs, UI components
- **Success criteria**: Deployable standalone service with web interface

## **Phase 4: Integration & Deployment (Lower Priority)**

### **Task 7: CustomGPT Integration Planning**
- **Current Issue**: Need programmatic access for CustomGPT
- **Actions**:
  - [ ] Design CustomGPT integration architecture
  - [ ] Create API wrapper for CustomGPT consumption
  - [ ] Add authentication/authorization for CustomGPT calls
  - [ ] Implement webhook support for async video generation
  - [ ] Test integration with sample CustomGPT implementation
  - [ ] Document integration patterns and best practices
- **Files to modify**: `main.py` (new endpoints), documentation
- **Success criteria**: Working CustomGPT integration prototype

---

## 🎯 **Recommended Execution Order**

1. **Start with Task 1 & 2** (subtitle and image quality) - these are visible issues that will have immediate impact
2. **Move to Task 3** (audio quality) - this affects the core user experience
3. **Tackle Task 4** (script enhancement) - this adds value but isn't blocking
4. **Complete Task 5 & 6** (reorganization and standalone prep) - these are architectural improvements
5. **Finish with Task 7** (CustomGPT integration) - this is future-facing

## 📋 **Progress Tracking**

- **Phase 1**: 2/3 tasks completed ✅
- **Phase 2**: 0/1 tasks completed  
- **Phase 3**: 0/2 tasks completed
- **Phase 4**: 0/1 tasks completed

**Total Progress**: 2/7 tasks completed (29%)

## 🚀 **Quick Start Commands**

```bash
# Start the video generator service
cd agents/video-generator-agent
uvicorn main:app --reload --host 0.0.0.0 --port 8000

# Test the service
curl http://localhost:8000/

# Generate a test video (example)
curl -X POST http://localhost:8000/generate-video \
  -H "Content-Type: application/json" \
  -d '{"slides": ["slide1.png"], "script": [{"text": "Test", "duration": 5, "slide": "slide1.png"}]}'
```

## 📝 **Notes**

- Each task should be completed and tested before moving to the next
- Keep track of any dependencies or blockers discovered during implementation
- Document any configuration changes or new environment variables needed
- Consider creating test videos for each improvement to validate changes 