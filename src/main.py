from fastapi import FastAPI, HTTPException, UploadFile, File
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List, Optional
import uuid
import os
import re
from pathlib import Path
from PIL import Image

from video_builder import VideoBuilder

# Create input, output, and temp directories if they don't exist
input_dir = Path("input")
input_dir.mkdir(exist_ok=True)
(input_dir / "pdfs").mkdir(exist_ok=True)
(input_dir / "scripts").mkdir(exist_ok=True)
(input_dir / "images").mkdir(exist_ok=True)

output_dir = Path("output")
output_dir.mkdir(exist_ok=True)

temp_dir = Path("temp")
temp_dir.mkdir(exist_ok=True)

app = FastAPI(
    title="Video Generator Service",
    description="Generate training videos from slides and narration scripts",
    version="1.0.0"
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Configure this properly for production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Mount static files for serving generated videos
app.mount("/output", StaticFiles(directory="output"), name="output")

# Pydantic models
class SlideScript(BaseModel):
    text: str
    duration: int
    slide: str  # URL or local file path

class VideoRequest(BaseModel):
    slides: List[str]
    script: List[SlideScript]
    voice: str = "female"
    include_subtitles: bool = False  # Changed default to False
    video_quality: str = "720p"  # 720p, 1080p
    image_config: Optional[dict] = None
    subtitle_config: Optional[dict] = {
        "position": "bottom",  # "top", "bottom", "center"
        "font_size": 36,
        "font_color": "white",
        "stroke_color": "black",
        "stroke_width": 2,
        "background_color": None,  # "black", "white", or None for transparent
        "background_opacity": 0.7,
        "max_width": 0.8  # Percentage of video width (0.0 to 1.0)
    }

class VideoResponse(BaseModel):
    video_url: str
    video_id: str
    duration: float
    status: str = "success"

class PDFUploadResponse(BaseModel):
    pdf_id: str
    slide_files: List[str]
    total_pages: int
    message: str

class ScriptParseResponse(BaseModel):
    script_id: str
    parsed_segments: List[SlideScript]
    total_segments: int
    total_duration: int
    message: str

@app.get("/")
async def root():
    """Health check endpoint"""
    return {
        "message": "Video Generator Service",
        "version": "1.0.0",
        "status": "healthy"
    }

@app.post("/generate-video", response_model=VideoResponse)
async def generate_video(req: VideoRequest):
    """
    Generate a video from slides and narration script.
    
    This endpoint accepts a list of slides and a script with timing information,
    then generates a professional training video with narration.
    """
    try:
        # Generate unique video ID
        video_id = str(uuid.uuid4())
        
        # Look for corresponding script file in input/scripts directory
        script_file_path = None
        scripts_dir = input_dir / "scripts"
        if scripts_dir.exists():
            # Look for any .txt script files (could be enhanced to match by name)
            script_files = list(scripts_dir.glob("*.txt"))
            if script_files:
                # For now, use the first script file found
                # In the future, this could be enhanced to match by project name
                script_file_path = str(script_files[0])
        
        # Initialize video builder
        builder = VideoBuilder(
            output_dir=output_dir,
            voice=req.voice,
            include_subtitles=req.include_subtitles,
            video_quality=req.video_quality,
            subtitle_config=req.subtitle_config,
            image_config=req.image_config
        )
        
        # Generate the video
        video_path, duration = await builder.generate_video(
            slides=req.slides,
            script=req.script,
            video_id=video_id,
            script_file_path=script_file_path
        )
        
        # Construct the public URL
        # In production, this would be your actual domain
        base_url = os.getenv("BASE_URL", "http://localhost:8000")
        video_url = f"{base_url}/output/{video_id}.mp4"
        
        return VideoResponse(
            video_url=video_url,
            video_id=video_id,
            duration=duration
        )
        
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Video generation failed: {str(e)}"
        )

@app.post("/upload-pdf", response_model=PDFUploadResponse)
async def upload_pdf(file: UploadFile = File(...)):
    """
    Upload a PDF file and convert each page to individual slide images.
    
    This endpoint accepts PDF files, converts each page to a high-quality image,
    and stores them for use in video generation.
    """
    try:
        # Validate file type
        if not file.content_type == "application/pdf":
            raise HTTPException(
                status_code=400,
                detail="File must be a PDF"
            )
        
        # Generate unique PDF ID
        pdf_id = str(uuid.uuid4())
        
        # Save uploaded PDF
        pdf_filename = f"{pdf_id}_{file.filename}"
        pdf_path = input_dir / "pdfs" / pdf_filename
        
        with open(pdf_path, "wb") as buffer:
            content = await file.read()
            buffer.write(content)
        
        # Convert PDF to images
        slide_files = await convert_pdf_to_images(pdf_path, pdf_id)
        
        return PDFUploadResponse(
            pdf_id=pdf_id,
            slide_files=slide_files,
            total_pages=len(slide_files),
            message=f"PDF processed successfully. {len(slide_files)} slides created."
        )
        
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"PDF processing failed: {str(e)}"
        )

@app.post("/parse-script", response_model=ScriptParseResponse)
async def parse_script(file: UploadFile = File(...)):
    """
    Upload and parse a timestamped script file into structured segments.
    
    This endpoint accepts text files with timestamp markers and converts them
    into structured script data for video generation.
    """
    try:
        # Validate file type
        if not file.content_type.startswith("text/"):
            raise HTTPException(
                status_code=400,
                detail="File must be a text file"
            )
        
        # Generate unique script ID
        script_id = str(uuid.uuid4())
        
        # Read script content
        content = await file.read()
        script_text = content.decode('utf-8')
        
        # Save script file
        script_filename = f"{script_id}_{file.filename}"
        script_path = input_dir / "scripts" / script_filename
        
        with open(script_path, "w") as f:
            f.write(script_text)
        
        # Parse script into segments
        parsed_segments = parse_timestamped_script(script_text)
        
        total_duration = max([seg.duration for seg in parsed_segments]) if parsed_segments else 0
        
        return ScriptParseResponse(
            script_id=script_id,
            parsed_segments=parsed_segments,
            total_segments=len(parsed_segments),
            total_duration=total_duration,
            message=f"Script parsed successfully. {len(parsed_segments)} segments created."
        )
        
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Script parsing failed: {str(e)}"
        )

@app.get("/subtitle-config-examples")
async def get_subtitle_config_examples():
    """Get example subtitle configurations for testing."""
    return {
        "examples": {
            "default": {
                "position": "bottom",
                "font_size": 36,
                "font_color": "white",
                "stroke_color": "black",
                "stroke_width": 2,
                "background_color": None,
                "background_opacity": 0.7,
                "max_width": 0.8
            },
            "top_position": {
                "position": "top",
                "font_size": 32,
                "font_color": "white",
                "stroke_color": "black",
                "stroke_width": 2,
                "background_color": "black",
                "background_opacity": 0.8,
                "max_width": 0.9
            },
            "center_position": {
                "position": "center",
                "font_size": 40,
                "font_color": "yellow",
                "stroke_color": "black",
                "stroke_width": 3,
                "background_color": "black",
                "background_opacity": 0.6,
                "max_width": 0.7
            },
            "no_subtitles": {
                "include_subtitles": False
            }
        },
        "usage": "Include any of these configurations in your VideoRequest.subtitle_config field"
    }

# Removed complex image config examples - using simple defaults only

@app.post("/upload-slide")
async def upload_slide(file: UploadFile = File(...)):
    """
    Upload a slide image for video generation.
    
    This endpoint accepts image files and stores them for use in video generation.
    """
    try:
        # Validate file type
        if not file.content_type.startswith("image/"):
            raise HTTPException(
                status_code=400,
                detail="File must be an image"
            )
        
        # Generate unique filename
        file_id = str(uuid.uuid4())
        file_extension = Path(file.filename).suffix
        filename = f"{file_id}{file_extension}"
        
        # Save file
        file_path = output_dir / filename
        with open(file_path, "wb") as buffer:
            content = await file.read()
            buffer.write(content)
        
        return {
            "filename": filename,
            "file_id": file_id,
            "message": "Slide uploaded successfully"
        }
        
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"File upload failed: {str(e)}"
        )

async def convert_pdf_to_images(pdf_path: Path, pdf_id: str, dpi: int = 75) -> List[str]:
    """Convert PDF pages to individual image files."""
    try:
        from pdf2image import convert_from_path
        
        # Convert PDF to images with fast processing DPI
        print(f"🔄 Converting PDF to images at {dpi} DPI...")
        images = convert_from_path(
            pdf_path,
            dpi=dpi,  # Fast DPI for quick processing
            fmt='PNG'
        )
        print(f"✅ Converted {len(images)} pages")
        
        slide_files = []
        for i, image in enumerate(images):
            # Generate filename for each slide
            slide_filename = f"{pdf_id}_slide_{i+1:03d}.png"
            slide_path = temp_dir / slide_filename  # Save to temp directory first
            
            print(f"📄 Saving slide {i+1}/{len(images)}: {image.width}x{image.height}")
            
            # Save with reduced quality for faster processing
            image.save(slide_path, 'PNG', optimize=True)
            
            slide_files.append(slide_filename)
        
        return slide_files
        
    except ImportError:
        raise Exception("PDF processing requires pdf2image. Install with: pip install pdf2image")
    except Exception as e:
        raise Exception(f"PDF conversion failed: {str(e)}")

def parse_timestamped_script(script_text: str) -> List[SlideScript]:
    """Parse timestamped script text into structured segments."""
    try:
        segments = []
        
        # Split by timestamp markers [MM:SS]
        timestamp_pattern = r'\[(\d{2}):(\d{2})\]'
        parts = re.split(timestamp_pattern, script_text)
        
        # Process each timestamped section
        for i in range(1, len(parts), 3):  # Skip first empty part, then take groups of 3
            if i + 2 < len(parts):
                minutes = int(parts[i])
                seconds = int(parts[i + 1])
                text = parts[i + 2].strip()
                
                if text:  # Skip empty segments
                    # Calculate duration (time until next segment or default)
                    current_time = minutes * 60 + seconds
                    
                    # Look ahead for next timestamp
                    if i + 5 < len(parts):
                        next_minutes = int(parts[i + 3])
                        next_seconds = int(parts[i + 4])
                        next_time = next_minutes * 60 + next_seconds
                        duration = max(next_time - current_time, 5)  # Minimum 5 seconds
                    else:
                        duration = 20  # Default duration for last segment
                    
                    # Estimate slide number based on timing
                    slide_number = len(segments) + 1
                    slide_name = f"slide_{slide_number:03d}.png"
                    
                    segments.append(SlideScript(
                        text=text,
                        duration=duration,
                        slide=slide_name
                    ))
        
        return segments
        
    except Exception as e:
        raise Exception(f"Script parsing failed: {str(e)}")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000) 