#!/usr/bin/env python3
"""
Video Generation Service
Creates training videos from slides and narration scripts.
"""

import os
import subprocess
import asyncio
import tempfile
import uuid
from pathlib import Path
from typing import List, Tuple, Dict, Optional
import requests
from PIL import Image, ImageDraw, ImageFont
import numpy as np

from moviepy.editor import ImageClip, TextClip, VideoFileClip, AudioFileClip, CompositeVideoClip, concatenate_videoclips
from gtts import gTTS
from pydantic import BaseModel
from tqdm import tqdm

class SlideScript(BaseModel):
    text: str
    duration: int
    slide: str

class VideoBuilder:
    """
    Core video generation engine that combines slides and narration into training videos.
    """
    
    def __init__(
        self,
        output_dir: Path,
        voice: str = "female",
        include_subtitles: bool = False,  # Default to False - no subtitles
        video_quality: str = "720p",
        subtitle_config: dict = None,
        image_config: dict = None
    ):
        self.output_dir = output_dir
        self.voice = voice
        self.include_subtitles = include_subtitles
        self.video_quality = video_quality
        
        # Set video dimensions based on quality - VERTICAL for PDF content
        if video_quality == "1080p":
            self.width, self.height = 1080, 1920  # Vertical 1080p
        else:  # 720p default
            self.width, self.height = 720, 1280   # Vertical 720p
        
        # Simple image config - no processing overhead
        self.image_config = image_config or {}
        
        # Set subtitle configuration with defaults
        self.subtitle_config = subtitle_config or {
            "position": "bottom",
            "font_size": 36,
            "font_color": "white",
            "stroke_color": "black",
            "stroke_width": 2,
            "background_color": None,
            "background_opacity": 0.7,
            "max_width": 0.8
        }
    
    async def generate_video(
        self,
        slides: List[str],
        script: List[SlideScript],
        video_id: str,
        script_file_path: str = None
    ) -> Tuple[str, float]:
        """
        Generate a complete video from slides and script.
        
        Args:
            slides: List of slide image URLs or file paths
            script: List of SlideScript objects with text and timing
            video_id: Unique identifier for the video
            script_file_path: Optional path to the original script file to copy for reference
            
        Returns:
            Tuple of (video_path, duration)
        """
        try:
            # Create temporary directory for processing
            with tempfile.TemporaryDirectory() as temp_dir:
                temp_path = Path(temp_dir)
                
                # Create organized project structure for this video course
                project_dir = self.output_dir / video_id
                slides_dir = project_dir / "slides"
                audio_dir = project_dir / "audio"
                video_dir = project_dir / "video"
                
                # Create all directories
                slides_dir.mkdir(parents=True, exist_ok=True)
                audio_dir.mkdir(parents=True, exist_ok=True)
                video_dir.mkdir(parents=True, exist_ok=True)
                
                # Copy script file to project folder for reference
                if script_file_path and Path(script_file_path).exists():
                    import shutil
                    script_filename = Path(script_file_path).name
                    shutil.copy2(script_file_path, project_dir / script_filename)
                
                # Process each slide and script segment
                video_clips = []
                total_duration = 0
                total_scaled_duration = 0
                
                # Create progress bar for overall video generation
                print(f"🎬 Starting video generation: {len(script)} segments")
                progress_bar = tqdm(
                    total=len(script),
                    desc="🎥 Generating video",
                    unit="segment",
                    bar_format="{l_bar}{bar}| {n_fmt}/{total_fmt} [{elapsed}<{remaining}, {rate_fmt}]"
                )
                
                for i, script_segment in enumerate(script):
                    progress_bar.set_description(f"🎥 Processing: {script_segment.slide}")
                    
                    # Find the corresponding slide
                    slide_path = self._get_slide_path(slides, script_segment.slide)
                    
                    # Copy slide to project's slides folder
                    project_slide_path = await self._copy_slide_to_project(slide_path, slides_dir)
                    
                    # Extract slide number from slide name for proper audio naming
                    slide_number = self._extract_slide_number(script_segment.slide)
                    
                    # Generate audio for this segment with proper naming
                    audio_filename = f"audio_{slide_number:03d}.wav"
                    audio_path = await self.generate_audio(
                        text=script_segment.text,
                        output_path=audio_dir / audio_filename
                    )
                    
                    # Create video clip for this segment
                    video_clip = await self.create_video_segment(
                        slide_path=project_slide_path,
                        audio_path=audio_path,
                        duration=script_segment.duration,
                        text=script_segment.text if self.include_subtitles else None,
                        temp_path=temp_path
                    )
                    
                    video_clips.append(video_clip)
                    total_duration += script_segment.duration
                    total_scaled_duration += (script_segment.duration / self.playback_speed)
                    progress_bar.update(1)
                
                progress_bar.close()
                
                # Concatenate all video clips
                print("\n🔗 Concatenating video clips...")
                concatenation_progress = tqdm(
                    total=1,
                    desc="🔗 Final assembly",
                    unit="video",
                    bar_format="{l_bar}{bar}| {desc} [{elapsed}]"
                )
                final_video = concatenate_videoclips(video_clips)
                concatenation_progress.update(1)
                concatenation_progress.close()
                
                # Save the final video in organized structure
                output_path = video_dir / "final_video.mp4"
                print(f"\n💾 Saving video to: {output_path}")
                save_progress = tqdm(
                    total=1,
                    desc="💾 Encoding video",
                    unit="file",
                    bar_format="{l_bar}{bar}| {desc} [{elapsed}]"
                )
                final_video.write_videofile(
                    str(output_path),
                    fps=24,
                    codec='libx264',
                    audio_codec='aac',
                    verbose=False,  # Suppress MoviePy's own progress output
                    logger=None     # Disable MoviePy logging to avoid conflicts
                )
                save_progress.update(1)
                save_progress.close()
                
                # Clean up
                final_video.close()
                for clip in video_clips:
                    clip.close()
                
                return str(output_path), total_scaled_duration
                
        except Exception as e:
            raise Exception(f"Video generation failed: {str(e)}")
    
    def _get_slide_path(self, slides: List[str], slide_name: str) -> str:
        """Get the full path to a slide image."""
        # First check if it's a local file
        if os.path.exists(slide_name):
            return slide_name
        
        # Check if it's in the temp directory (processed files) - PRIORITY
        temp_slide_path = Path("temp") / slide_name
        if temp_slide_path.exists():
            return str(temp_slide_path)
        
        # Handle generic slide names by mapping to actual files in TEMP directory first
        if slide_name.startswith('slide_') and slide_name.endswith('.png'):
            # Extract slide number from generic name (e.g., "slide_001.png" -> 1)
            try:
                slide_num = int(slide_name.split('_')[1].split('.')[0])
                if 1 <= slide_num <= len(slides):
                    actual_slide_name = slides[slide_num - 1]  # Use corresponding actual slide
                    # Check temp directory FIRST for the actual slide file
                    temp_actual_path = Path("temp") / actual_slide_name
                    if temp_actual_path.exists():
                        return str(temp_actual_path)
                    # Fallback to output directory
                    output_slide_path = self.output_dir / actual_slide_name
                    if output_slide_path.exists():
                        return str(output_slide_path)
            except (ValueError, IndexError):
                pass
        
        # Check if it's in the output directory (uploaded files) - FALLBACK
        output_slide_path = self.output_dir / slide_name
        if output_slide_path.exists():
            return str(output_slide_path)
        
        # Check if it's a URL
        if slide_name.startswith(('http://', 'https://')):
            return slide_name
        
        # Try to find it in the slides list
        for slide in slides:
            if slide.endswith(slide_name) or slide == slide_name:
                # Check if this slide exists in temp directory
                temp_slide_path = Path("temp") / slide
                if temp_slide_path.exists():
                    return str(temp_slide_path)
                return slide
        
        raise ValueError(f"Slide not found: {slide_name}")
    
    def _extract_slide_number(self, slide_name: str) -> int:
        """Extract slide number from slide filename."""
        try:
            # Handle full paths - get just the filename
            filename = os.path.basename(slide_name)
            
            # Extract number from patterns like:
            # - "slide_001.png" 
            # - "cf75241c-5fac-4df2-81b1-634c6f6fff15_slide_001.png"
            # - "001.png"
            import re
            
            # Try to find slide_XXX pattern first
            slide_match = re.search(r'slide_(\d+)', filename)
            if slide_match:
                return int(slide_match.group(1))
            
            # Try to find any 3-digit number pattern
            number_match = re.search(r'(\d{3})', filename)
            if number_match:
                return int(number_match.group(1))
            
            # If no pattern found, just use the position in script (fallback)
            return 1
            
        except Exception:
            # Fallback to 1 if extraction fails
            return 1
    
    async def generate_audio(self, text: str, output_path: Path) -> str:
        """Generate audio narration using gTTS."""
        try:
            # Run gTTS in a thread to avoid blocking
            loop = asyncio.get_event_loop()
            await loop.run_in_executor(
                None,
                self._generate_audio_sync,
                text,
                output_path
            )
            return str(output_path)
        except Exception as e:
            raise Exception(f"Audio generation failed: {str(e)}")
    
    def _generate_audio_sync(self, text: str, output_path: Path):
        """Synchronous audio generation using gTTS."""
        try:
            # Ensure output directory exists
            output_path.parent.mkdir(parents=True, exist_ok=True)
            
            # Generate MP3 first with gTTS in the SAME directory as final output
            # This prevents temp directory conflicts with MoviePy
            mp3_path = output_path.with_suffix('.mp3')
            tts = gTTS(text=text, lang='en', slow=False)
            tts.save(str(mp3_path))
            
            # Ensure MP3 file is fully written and accessible
            import time
            time.sleep(0.3)  # Increased delay for file system sync
            
            # Verify MP3 was created successfully before conversion
            if not mp3_path.exists() or mp3_path.stat().st_size == 0:
                raise Exception(f"MP3 file was not created properly: {mp3_path}")
            
            # Convert MP3 to WAV using FFMPEG for better MoviePy compatibility
            import subprocess
            result = subprocess.run([
                'ffmpeg', '-y', '-i', str(mp3_path), 
                '-acodec', 'pcm_s16le', '-ar', '22050', 
                str(output_path)
            ], check=True, capture_output=True, text=True)
            
            # Verify WAV file was created successfully
            if not output_path.exists() or output_path.stat().st_size == 0:
                raise Exception(f"WAV file was not created properly: {output_path}")
            
            # Clean up temporary MP3 - use more robust cleanup
            try:
                if mp3_path.exists():
                    mp3_path.unlink()
            except Exception as cleanup_error:
                # Log cleanup error but don't fail the whole process
                print(f"Warning: Could not clean up MP3 file {mp3_path}: {cleanup_error}")
                
            # Final verification
            wav_size = output_path.stat().st_size
            print(f"✅ Audio generated: {output_path.name} ({wav_size:,} bytes)")
                
        except subprocess.CalledProcessError as e:
            raise Exception(f"FFMPEG conversion failed: {e.stderr}")
        except Exception as e:
            # Clean up any partial files on error
            for cleanup_path in [mp3_path, output_path]:
                try:
                    if 'cleanup_path' in locals() and cleanup_path.exists():
                        cleanup_path.unlink()
                except:
                    pass
            raise Exception(f"Audio generation failed: {str(e)}")
    
    async def create_video_segment(
        self,
        slide_path: str,
        audio_path: str,
        duration: int,
        text: str = None,
        temp_path: Path = None
    ) -> ImageClip:
        """Create a video segment from a slide and audio."""
        try:
            # Convert audio_path to absolute path to avoid MoviePy temp issues
            audio_path = str(Path(audio_path).resolve())
            
            # Load the slide image
            if slide_path.startswith(('http://', 'https://')):
                # Download remote image
                slide_image = await self.download_image(slide_path, temp_path)
            else:
                slide_image = Image.open(slide_path)
            
            # Validate image quality before processing
            slide_name = Path(slide_path).name
            if not self._validate_image_quality(slide_image, slide_name):
                print(f"Warning: Image quality issues detected for {slide_name}, but continuing...")
            
            # Resize image to video dimensions
            slide_image = self.resize_image(slide_image)
            
            # Initialize audio duration variables
            actual_audio_duration = duration  # Default to script duration
            audio_clip = None
            
            # Load audio if provided and get actual duration
            if os.path.exists(audio_path):
                try:
                    # Ensure audio file is readable before loading
                    import time
                    time.sleep(0.1)  # Small delay to ensure file is ready
                    
                    # Verify file format and size before loading into MoviePy
                    audio_file_path = Path(audio_path)
                    if not audio_file_path.suffix.lower() == '.wav':
                        raise Exception(f"Expected WAV file, got: {audio_file_path.suffix}")
                    
                    file_size = audio_file_path.stat().st_size
                    if file_size == 0:
                        raise Exception(f"Audio file is empty: {audio_path}")
                    
                    print(f"🎵 Loading audio: {audio_file_path.name} ({file_size:,} bytes)")
                    
                    # Load audio with MoviePy using absolute path
                    audio_clip = AudioFileClip(audio_path)
                    if audio_clip.duration > 0:
                        actual_audio_duration = audio_clip.duration
                        print(f"   Duration: {actual_audio_duration:.1f}s")
                    else:
                        print(f"Warning: Audio file has zero duration: {audio_path}")
                        audio_clip.close()
                        audio_clip = None
                        
                except Exception as e:
                    print(f"Warning: Could not load audio file {audio_path}: {e}")
                    if audio_clip:
                        try:
                            audio_clip.close()
                        except:
                            pass
                        audio_clip = None
                    # Continue without audio rather than failing completely
            else:
                print(f"Warning: Audio file does not exist: {audio_path}")
            
            # Create video clip from image using ACTUAL audio duration instead of script duration
            # This prevents audio overlap issues when concatenating
            video_clip = ImageClip(np.array(slide_image), duration=actual_audio_duration)
            
            # Add audio if loaded successfully
            if audio_clip and audio_clip.duration > 0:
                video_clip = video_clip.set_audio(audio_clip)
            
            # Add subtitles if requested (also use actual duration)
            if text and self.include_subtitles:
                subtitle_clip = self.create_subtitle_clip(text, actual_audio_duration)
                if subtitle_clip is not None:  # Handle potential subtitle creation failure
                    video_clip = CompositeVideoClip([video_clip, subtitle_clip])
                else:
                    print("Warning: Subtitle creation failed, continuing without subtitles")
            
            return video_clip
            
        except Exception as e:
            # Clean up any resources on error
            if 'audio_clip' in locals() and audio_clip:
                try:
                    audio_clip.close()
                except:
                    pass
            raise Exception(f"Video segment creation failed: {str(e)}")
    
    async def download_image(self, url: str, temp_path: Path) -> Image.Image:
        """Download an image from URL."""
        try:
            response = requests.get(url, timeout=30)
            response.raise_for_status()
            
            # Save to temporary file
            temp_file = temp_path / f"temp_image_{hash(url)}.jpg"
            with open(temp_file, 'wb') as f:
                f.write(response.content)
            
            return Image.open(temp_file)
            
        except Exception as e:
            raise Exception(f"Image download failed: {str(e)}")
    
    def resize_image(self, image: Image.Image) -> Image.Image:
        """Resize image to video dimensions - simplified for vertical videos."""
        # Convert to RGB if needed
        if image.mode != 'RGB':
            image = image.convert('RGB')
        
        # For vertical videos and portrait PDFs, just resize to fit exactly
        # No complex padding/cropping needed since orientations match
        resampling = Image.Resampling.LANCZOS
        
        # Simply resize to exact video dimensions
        # The aspect ratios should be very close for PDF pages
        final_image = image.resize((self.width, self.height), resampling)
        
        print(f"✅ Resized image: {image.width}x{image.height} → {self.width}x{self.height}")
        return final_image
    
    def _preprocess_image(self, image: Image.Image) -> Image.Image:
        """Apply minimal image preprocessing - simplified for performance."""
        try:
            # Convert to RGB if needed
            if image.mode != 'RGB':
                image = image.convert('RGB')
            
            # Skip enhancement processing for better performance
            # since vertical orientation should give good quality by default
            return image
            
        except Exception as e:
            # If preprocessing fails, return original image
            print(f"Warning: Image preprocessing failed: {e}")
            return image
    
    def _validate_image_quality(self, image: Image.Image, slide_name: str) -> bool:
        """Validate that an image meets quality standards."""
        try:
            # Check image dimensions
            if image.width < 800 or image.height < 600:
                print(f"Warning: {slide_name} has low resolution: {image.width}x{image.height}")
                return False
            
            # Check for completely blank/white images
            if image.mode == 'RGB':
                # Convert to grayscale for analysis
                gray = image.convert('L')
                # Check if image is mostly white (value > 240)
                white_pixels = sum(1 for pixel in gray.getdata() if pixel > 240)
                total_pixels = gray.width * gray.height
                white_ratio = white_pixels / total_pixels
                
                if white_ratio > 0.95:  # 95% white
                    print(f"Warning: {slide_name} appears to be mostly blank")
                    return False
            
            # Check file size (if available)
            # This would require saving to a temporary file, so we'll skip for now
            
            print(f"✅ Image quality validated: {slide_name} ({image.width}x{image.height})")
            return True
            
        except Exception as e:
            print(f"Warning: Image quality validation failed for {slide_name}: {e}")
            return True  # Continue processing even if validation fails
    
    def create_subtitle_clip(self, text: str, duration: float) -> TextClip:
        """Create a subtitle overlay for the video with enhanced styling and positioning."""
        try:
            # Wrap long text for better readability
            max_chars = int(60 * self.subtitle_config.get("max_width", 0.8))
            wrapped_text = self._wrap_subtitle_text(text, max_chars_per_line=max_chars)
            
            # Calculate subtitle width based on configuration
            subtitle_width = int(self.width * self.subtitle_config.get("max_width", 0.8))
            
            # Get configuration values with defaults
            font_size = self.subtitle_config.get("font_size", 36)
            font_color = self.subtitle_config.get("font_color", "white")
            stroke_color = self.subtitle_config.get("stroke_color", "black")
            stroke_width = self.subtitle_config.get("stroke_width", 2)
            background_color = self.subtitle_config.get("background_color")
            background_opacity = self.subtitle_config.get("background_opacity", 0.7)
            
            # Try to create subtitle with enhanced styling
            try:
                # Build TextClip parameters
                clip_params = {
                    "text": wrapped_text,
                    "font_size": font_size,
                    "color": font_color,
                    "stroke_color": stroke_color,
                    "stroke_width": stroke_width,
                    "method": 'caption',
                    "size": (subtitle_width, None)
                }
                
                # Add background if specified
                if background_color:
                    clip_params["bg_color"] = background_color
                    clip_params["opacity"] = background_opacity
                
                # Try with system font first
                try:
                    clip_params["font"] = 'Arial'
                    subtitle_clip = TextClip(**clip_params)
                except Exception as font_error:
                    print(f"Font error with Arial, trying without font specification: {font_error}")
                    # Remove font parameter and try again
                    if "font" in clip_params:
                        del clip_params["font"]
                    subtitle_clip = TextClip(**clip_params)
                
                # Position the subtitle based on configuration
                position = self.subtitle_config.get("position", "bottom")
                positioned_clip = self._position_subtitle(subtitle_clip, position)
                
                return positioned_clip.with_duration(float(duration))
                
            except Exception as method_error:
                print(f"Enhanced subtitle creation failed, using basic fallback: {method_error}")
                
                # Fallback: Basic text without advanced styling
                subtitle_clip = TextClip(
                    text=wrapped_text,
                    font_size=font_size,
                    color=font_color
                )
                
                # Position the fallback subtitle
                positioned_clip = self._position_subtitle(subtitle_clip, position)
                return positioned_clip.with_duration(float(duration))
                    
        except Exception as e:
            print(f"Subtitle creation failed, using minimal fallback: {e}")
            
            # Final fallback: Minimal text clip
            try:
                subtitle_clip = TextClip(
                    text="[Subtitle Error]",
                    font_size=24,
                    color='white'
                )
                positioned_clip = self._position_subtitle(subtitle_clip, "bottom")
                return positioned_clip.with_duration(float(duration))
            except:
                # If even the fallback fails, return None (handled in create_video_segment)
                return None
    
    def _position_subtitle(self, subtitle_clip: TextClip, position: str) -> TextClip:
        """Position subtitle clip based on configuration."""
        position = position.lower()
        
        if position == "top":
            # Position at top with margin
            return subtitle_clip.with_position(('center', 50))
        elif position == "center":
            # Position in center of video
            return subtitle_clip.with_position(('center', 'center'))
        elif position == "bottom":
            # Position at bottom with margin
            return subtitle_clip.with_position(('center', 'bottom'))
        else:
            # Default to bottom
            return subtitle_clip.with_position(('center', 'bottom'))
    
    def _wrap_subtitle_text(self, text: str, max_chars_per_line: int = 60) -> str:
        """Wrap text for subtitles to improve readability."""
        import textwrap
        
        # Remove extra spaces and line breaks
        text = ' '.join(text.split())
        
        # If text is short enough, return as-is
        if len(text) <= max_chars_per_line:
            return text
        
        # Wrap text preserving word boundaries
        wrapped = textwrap.fill(text, width=max_chars_per_line, break_long_words=False)
        
        # Limit to maximum 3 lines for subtitles
        lines = wrapped.split('\n')
        if len(lines) > 3:
            lines = lines[:3]
            lines[-1] = lines[-1][:max_chars_per_line-3] + "..."
        
        return '\n'.join(lines)

    async def _copy_slide_to_project(self, slide_path: str, slides_dir: Path) -> str:
        """Copy a slide file to the project's slides directory."""
        try:
            import shutil
            from pathlib import Path
            
            # Get the slide filename
            slide_filename = Path(slide_path).name
            
            # Create the destination path in the project's slides folder
            project_slide_path = slides_dir / slide_filename
            
            # Copy the slide file to the project folder
            if not project_slide_path.exists():
                shutil.copy2(slide_path, project_slide_path)
            
            return str(project_slide_path)
            
        except Exception as e:
            # If copying fails, return the original path as fallback
            print(f"Warning: Could not copy slide to project folder: {e}")
            return slide_path 