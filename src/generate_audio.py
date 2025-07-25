#!/usr/bin/env python3
"""
Production audio generation script for video content
This script contains the working audio pipeline used in video generation
"""

import subprocess
from pathlib import Path
from gtts import gTTS

def generate_audio():
    # Create proper project directory structure
    project_name = "roofmaxx_ohio_state_study"
    project_dir = Path("output") / project_name
    audio_dir = project_dir / "audio"
    audio_dir.mkdir(parents=True, exist_ok=True)
    
    # Video content segments with proper slide numbering
    video_segments = [
        (1, "Welcome to Mastering the Roofmaxx Ohio State Study. This course will guide you through the key findings of the 2018 Ohio State study."),
        (2, "Let's start with an overview of the Ohio State study. Conducted in 2018, this study aimed to evaluate the effectiveness of Roofmaxx products."),
        (3, "One of the key findings was the significant improvement in shingle flexibility after applying Roofmaxx. Flexibility is crucial for durability."),
        (4, "In conclusion, the 2018 Ohio State study provides robust evidence of Roofmaxx's effectiveness in restoring asphalt shingles.")
    ]
    
    for slide_num, text in video_segments:
        audio_filename = f"audio_{slide_num:03d}.wav"
        print(f"Generating {audio_filename}...")
        
        # Generate MP3 with gTTS
        mp3_path = audio_dir / f"audio_{slide_num:03d}.mp3"
        tts = gTTS(text=text, lang='en', slow=False)
        tts.save(str(mp3_path))
        
        # Convert to WAV using FFMPEG (same as video generator)
        wav_path = audio_dir / audio_filename
        subprocess.run([
            'ffmpeg', '-y', '-i', str(mp3_path), 
            '-acodec', 'pcm_s16le', '-ar', '22050', 
            str(wav_path)
        ], check=True, capture_output=True)
        
        # Clean up MP3
        mp3_path.unlink()
        
        print(f"✅ Created: {wav_path}")
        print(f"   Size: {wav_path.stat().st_size:,} bytes")

def generate_custom_audio(text, filename, project_name="custom_project"):
    """Generate audio for custom text - useful for video development"""
    project_dir = Path("output") / project_name
    audio_dir = project_dir / "audio"
    audio_dir.mkdir(parents=True, exist_ok=True)
    
    # Ensure filename has .wav extension
    if not filename.endswith('.wav'):
        filename = f"{filename}.wav"
    
    print(f"Generating audio: {filename}")
    
    # Generate MP3 with gTTS
    mp3_filename = filename.replace('.wav', '.mp3')
    mp3_path = output_dir / mp3_filename
    tts = gTTS(text=text, lang='en', slow=False)
    tts.save(str(mp3_path))
    
    # Convert to WAV using FFMPEG
    wav_path = output_dir / filename
    subprocess.run([
        'ffmpeg', '-y', '-i', str(mp3_path), 
        '-acodec', 'pcm_s16le', '-ar', '22050', 
        str(wav_path)
    ], check=True, capture_output=True)
    
    # Clean up MP3
    mp3_path.unlink()
    
    print(f"✅ Created: {wav_path}")
    return str(wav_path)

if __name__ == "__main__":
    generate_audio() 