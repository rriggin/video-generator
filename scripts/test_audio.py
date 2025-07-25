#!/usr/bin/env python3
"""
Quick test script to debug audio generation issues
"""

import tempfile
from pathlib import Path
from gtts import gTTS
from moviepy.editor import AudioFileClip
import os

def test_audio_generation():
    """Test basic audio generation and loading"""
    try:
        print("Testing audio generation...")
        
        # Create temp directory
        with tempfile.TemporaryDirectory() as temp_dir:
            temp_path = Path(temp_dir)
            audio_path = temp_path / "test_audio.mp3"
            
            # Generate audio using gTTS
            print(f"Generating audio at: {audio_path}")
            tts = gTTS(text="Hello world, this is a test.", lang='en', slow=False)
            tts.save(str(audio_path))
            
            print(f"Audio file exists: {audio_path.exists()}")
            print(f"Audio file size: {audio_path.stat().st_size} bytes")
            
            # Try to load with MoviePy
            print("Loading audio with AudioFileClip...")
            audio_clip = AudioFileClip(str(audio_path))
            
            print(f"Audio duration: {audio_clip.duration} seconds")
            print(f"Audio FPS: {audio_clip.fps}")
            
            audio_clip.close()
            print("✅ Audio generation and loading successful!")
            
    except Exception as e:
        print(f"❌ Error: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    test_audio_generation() 