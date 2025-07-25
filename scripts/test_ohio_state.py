#!/usr/bin/env python3
"""
Test script for Ohio State video generation with all fixes applied.
"""

import asyncio
import json
from pathlib import Path
from video_builder import VideoBuilder, SlideScript

async def test_ohio_state_video():
    """Test Ohio State video generation with real script and slides."""
    
    print("🎬 Starting Ohio State Test Video Generation...")
    print("Testing fixes: Audio sync, Subtitles, Script backup, Duration matching")
    
    # Create output directory
    output_dir = Path("output")
    output_dir.mkdir(exist_ok=True)
    
    # Use available slide files from the existing project
    slide_base_path = "output/roofmaxx_test_video/slides"
    available_slides = [
        f"{slide_base_path}/827d7006-c527-4b12-8e8a-85648a988978_slide_001.png",
        f"{slide_base_path}/827d7006-c527-4b12-8e8a-85648a988978_slide_002.png", 
        f"{slide_base_path}/827d7006-c527-4b12-8e8a-85648a988978_slide_003.png",
        f"{slide_base_path}/827d7006-c527-4b12-8e8a-85648a988978_slide_004.png",
        f"{slide_base_path}/827d7006-c527-4b12-8e8a-85648a988978_slide_005.png",
        f"{slide_base_path}/827d7006-c527-4b12-8e8a-85648a988978_slide_006.png",
        f"{slide_base_path}/827d7006-c527-4b12-8e8a-85648a988978_slide_007.png",
        f"{slide_base_path}/827d7006-c527-4b12-8e8a-85648a988978_slide_008.png",
        f"{slide_base_path}/827d7006-c527-4b12-8e8a-85648a988978_slide_009.png",
        f"{slide_base_path}/827d7006-c527-4b12-8e8a-85648a988978_slide_010.png",
        f"{slide_base_path}/827d7006-c527-4b12-8e8a-85648a988978_slide_011.png"
    ]
    
    # Create script segments based on the actual Ohio State script
    script_segments = [
        SlideScript(
            text="Welcome to 'Mastering the Roofmaxx Ohio State Study: Elevate Your Sales Expertise'. In this course, we will guide you through the key findings of the 2018 Ohio State study that validated Roofmaxx products against several roofing industry standards.",
            duration=20,
            slide="slide_001.png"
        ),
        SlideScript(
            text="Let's start with an overview of the Ohio State study. Conducted in 2018, this study aimed to evaluate the effectiveness of Roofmaxx products in restoring and extending the life of asphalt shingles.",
            duration=20,
            slide="slide_002.png"
        ),
        SlideScript(
            text="The primary focus of the study was to assess the impact of Roofmaxx on the flexibility, permeability, and granule adhesion of aged asphalt shingles. These are critical factors that determine the longevity and performance of roofing materials.",
            duration=20,
            slide="slide_003.png"
        ),
        SlideScript(
            text="One of the key findings of the study was the significant improvement in shingle flexibility after applying Roofmaxx. Flexibility is crucial because it allows shingles to withstand various weather conditions without cracking or breaking.",
            duration=20,
            slide="slide_004.png"
        ),
        SlideScript(
            text="Another important aspect evaluated was permeability. Permeability measures the ability of shingles to resist water penetration, which is essential for preventing leaks and water damage.",
            duration=20,
            slide="slide_005.png"
        ),
        SlideScript(
            text="Granule adhesion was also a critical factor examined in the study. Granules on shingles protect against UV rays and add an extra layer of durability. The study found that Roofmaxx treatment significantly improved granule adhesion.",
            duration=20,
            slide="slide_006.png"
        ),
        SlideScript(
            text="The study's results were validated against several industry standards, including ASTM D3462 and ASTM D7158. These standards are widely recognized in the roofing industry and set benchmarks for shingle performance.",
            duration=20,
            slide="slide_007.png"
        ),
        SlideScript(
            text="Understanding these findings allows you to confidently present Roofmaxx to potential customers. You can explain how Roofmaxx not only restores the flexibility and durability of their shingles but also enhances their resistance to water and UV damage.",
            duration=20,
            slide="slide_008.png"
        ),
        SlideScript(
            text="Additionally, the environmental benefits of Roofmaxx can be a compelling selling point. By extending the life of existing shingles, Roofmaxx reduces the need for roof replacements, which in turn decreases the amount of waste sent to landfills.",
            duration=20,
            slide="slide_009.png"
        ),
        SlideScript(
            text="In conclusion, the 2018 Ohio State study provides robust evidence of Roofmaxx's effectiveness in restoring and enhancing the performance of asphalt shingles. By leveraging this information, you can effectively communicate the benefits of Roofmaxx to potential customers.",
            duration=20,
            slide="slide_010.png"
        ),
        SlideScript(
            text="Thank you for completing this course. Let's now test your understanding with a few questions.",
            duration=20,
            slide="slide_011.png"
        )
    ]
    
    try:
        # Initialize video builder with subtitles enabled to test subtitle fixes
        builder = VideoBuilder(
            output_dir=output_dir,
            voice="female", 
            include_subtitles=True,  # Test subtitle implementation
            video_quality="720p"
        )
        
        # Path to the script file for backup functionality testing
        script_file_path = "input/scripts/roofmaxx-ohio-study-script.txt"
        
        print(f"📝 Using script: {script_file_path}")
        print(f"🎞️ Using {len(available_slides)} slide files")
        print(f"📄 Creating {len(script_segments)} script segments")
        print(f"🔊 Subtitles enabled: {builder.include_subtitles}")
        
        # Generate the video with our custom project name
        video_path, duration = await builder.generate_video(
            slides=available_slides,
            script=script_segments,
            video_id="ohio_state_test_1",  # Custom project name
            script_file_path=script_file_path  # Test script backup feature
        )
        
        print(f"\n✅ Video generation successful!")
        print(f"📹 Video saved to: {video_path}")
        print(f"⏱️ Total duration: {duration:.2f} seconds")
        print(f"📁 Project folder: output/ohio_state_test_1/")
        
        # Verify all the fixes
        project_path = Path("output/ohio_state_test_1")
        
        print(f"\n🔍 Verifying fixes applied:")
        print(f"  📂 Project structure: {'✅' if project_path.exists() else '❌'}")
        print(f"  📝 Script backup: {'✅' if (project_path / 'roofmaxx-ohio-study-script.txt').exists() else '❌'}")
        print(f"  🔊 Audio files: {'✅' if (project_path / 'audio').exists() else '❌'}")
        print(f"  🎞️ Slide files: {'✅' if (project_path / 'slides').exists() else '❌'}")
        print(f"  🎬 Final video: {'✅' if (project_path / 'video' / 'final_video.mp4').exists() else '❌'}")
        
        if (project_path / "audio").exists():
            audio_files = list((project_path / "audio").glob("*.wav"))
            print(f"  🎵 Audio segments generated: {len(audio_files)}")
        
        return video_path, duration
        
    except Exception as e:
        print(f"❌ Video generation failed: {str(e)}")
        import traceback
        traceback.print_exc()
        return None, 0

if __name__ == "__main__":
    # Run the test
    asyncio.run(test_ohio_state_video()) 