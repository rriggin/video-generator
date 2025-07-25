#!/usr/bin/env python3
"""
API test for Ohio State video generation using the running service.
Tests all fixes: Audio sync, Subtitles, Script backup, Duration matching
"""

import requests
import json
from pathlib import Path

def test_ohio_state_api():
    """Test Ohio State video generation via API."""
    
    print("🎬 Testing Ohio State Video Generation via API...")
    print("Service running on: http://localhost:8000")
    print("Testing fixes: Audio sync, Subtitles, Script backup, Duration matching")
    
    # API endpoint
    api_url = "http://localhost:8000/generate-video"
    
    # Get available slide files from existing project (as absolute paths for API)
    slide_base_path = "/Users/ryanriggin/Code/goskills/agents/video-generator-agent/output/roofmaxx_test_video/slides"
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
    
    # Create API request payload with actual Ohio State script content
    payload = {
        "slides": available_slides,
        "script": [
            {
                "text": "Welcome to 'Mastering the Roofmaxx Ohio State Study: Elevate Your Sales Expertise'. In this course, we will guide you through the key findings of the 2018 Ohio State study that validated Roofmaxx products against several roofing industry standards. This invaluable knowledge will enhance your sales expertise and help you effectively communicate the benefits of Roofmaxx to potential customers.",
                "duration": 20,
                "slide": "slide_001.png"
            },
            {
                "text": "Let's start with an overview of the Ohio State study. Conducted in 2018, this study aimed to evaluate the effectiveness of Roofmaxx products in restoring and extending the life of asphalt shingles. The study was rigorous and adhered to multiple industry standards to ensure the reliability of its findings.",
                "duration": 20,
                "slide": "slide_002.png"
            },
            {
                "text": "The primary focus of the study was to assess the impact of Roofmaxx on the flexibility, permeability, and granule adhesion of aged asphalt shingles. These are critical factors that determine the longevity and performance of roofing materials. The study included both laboratory and field tests to provide comprehensive results.",
                "duration": 20,
                "slide": "slide_003.png"
            },
            {
                "text": "One of the key findings of the study was the significant improvement in shingle flexibility after applying Roofmaxx. Flexibility is crucial because it allows shingles to withstand various weather conditions without cracking or breaking. The study showed that Roofmaxx-treated shingles exhibited a marked increase in flexibility, making them more durable and resilient.",
                "duration": 20,
                "slide": "slide_004.png"
            },
            {
                "text": "Another important aspect evaluated was permeability. Permeability measures the ability of shingles to resist water penetration, which is essential for preventing leaks and water damage. The Ohio State study demonstrated that Roofmaxx-treated shingles had reduced permeability, enhancing their ability to protect the underlying structure from moisture.",
                "duration": 20,
                "slide": "slide_005.png"
            },
            {
                "text": "Granule adhesion was also a critical factor examined in the study. Granules on shingles protect against UV rays and add an extra layer of durability. Over time, granules can become loose and fall off, diminishing the effectiveness of the shingles. The study found that Roofmaxx treatment significantly improved granule adhesion, ensuring that shingles maintained their protective properties longer.",
                "duration": 20,
                "slide": "slide_006.png"
            },
            {
                "text": "The study's results were validated against several industry standards, including ASTM D3462 and ASTM D7158. These standards are widely recognized in the roofing industry and set benchmarks for shingle performance. The Ohio State study confirmed that Roofmaxx-treated shingles met and, in many cases, exceeded these standards, providing strong evidence of the product's effectiveness.",
                "duration": 20,
                "slide": "slide_007.png"
            },
            {
                "text": "Understanding these findings allows you to confidently present Roofmaxx to potential customers. You can explain how Roofmaxx not only restores the flexibility and durability of their shingles but also enhances their resistance to water and UV damage. Highlighting the study's validation against industry standards adds credibility to your pitch and reassures customers of the product's reliability.",
                "duration": 20,
                "slide": "slide_008.png"
            },
            {
                "text": "Additionally, the environmental benefits of Roofmaxx can be a compelling selling point. By extending the life of existing shingles, Roofmaxx reduces the need for roof replacements, which in turn decreases the amount of waste sent to landfills. This eco-friendly aspect can appeal to environmentally conscious customers.",
                "duration": 20,
                "slide": "slide_009.png"
            },
            {
                "text": "In conclusion, the 2018 Ohio State study provides robust evidence of Roofmaxx's effectiveness in restoring and enhancing the performance of asphalt shingles. By leveraging this information, you can effectively communicate the benefits of Roofmaxx to potential customers, boosting your sales expertise and success.",
                "duration": 20,
                "slide": "slide_010.png"
            },
            {
                "text": "Thank you for completing this course. Let's now test your understanding with a few questions.",
                "duration": 20,
                "slide": "slide_011.png"
            }
        ],
        "voice": "female",
        "include_subtitles": True,  # Test our subtitle fixes
        "video_quality": "720p"
    }
    
    print(f"📝 Sending request with {len(payload['script'])} script segments")
    print(f"🎞️ Using {len(payload['slides'])} slide files")
    print(f"🔊 Subtitles enabled: {payload['include_subtitles']}")
    print(f"📡 API endpoint: {api_url}")
    
    try:
        # Send API request
        headers = {'Content-Type': 'application/json'}
        response = requests.post(api_url, json=payload, headers=headers, timeout=300)  # 5 min timeout
        
        if response.status_code == 200:
            result = response.json()
            print(f"\n✅ Video generation successful!")
            print(f"📹 Video URL: {result.get('video_url', 'N/A')}")
            print(f"🆔 Video ID: {result.get('video_id', 'N/A')}")
            print(f"⏱️ Duration: {result.get('duration', 'N/A')} seconds")
            
            # The service generates a UUID, but let's check if the files exist
            video_id = result.get('video_id')
            if video_id:
                project_path = Path(f"output/{video_id}")
                print(f"📁 Project folder: {project_path}")
                
                print(f"\n🔍 Verifying fixes applied:")
                print(f"  📂 Project structure: {'✅' if project_path.exists() else '❌'}")
                
                if project_path.exists():
                    print(f"  📝 Script backup: {'✅' if (project_path / 'roofmaxx-ohio-study-script.txt').exists() else '❌'}")
                    print(f"  🔊 Audio files: {'✅' if (project_path / 'audio').exists() else '❌'}")
                    print(f"  🎞️ Slide files: {'✅' if (project_path / 'slides').exists() else '❌'}")
                    print(f"  🎬 Final video: {'✅' if (project_path / 'video' / 'final_video.mp4').exists() else '❌'}")
                    
                    if (project_path / "audio").exists():
                        audio_files = list((project_path / "audio").glob("*.wav"))
                        print(f"  🎵 Audio segments: {len(audio_files)} files")
                        
                        # Check actual audio durations to verify timing fix
                        if audio_files:
                            print(f"\n🎵 Audio Duration Analysis (testing timing fixes):")
                            import subprocess
                            for audio_file in audio_files[:3]:  # Check first 3
                                try:
                                    duration = subprocess.check_output([
                                        'ffprobe', '-v', 'quiet', '-show_entries', 'format=duration',
                                        '-of', 'default=noprint_wrappers=1:nokey=1', str(audio_file)
                                    ]).decode().strip()
                                    print(f"    {audio_file.name}: {float(duration):.1f}s (should be ~9-12s, not 20s)")
                                except:
                                    print(f"    {audio_file.name}: Could not analyze")
            
            return result
            
        else:
            print(f"❌ API request failed: HTTP {response.status_code}")
            print(f"Response: {response.text}")
            return None
            
    except requests.exceptions.Timeout:
        print("❌ Request timed out - video generation may still be running")
        return None
    except Exception as e:
        print(f"❌ Request failed: {str(e)}")
        return None

if __name__ == "__main__":
    test_ohio_state_api() 