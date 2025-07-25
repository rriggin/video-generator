#!/usr/bin/env python3
"""
Quick test to demonstrate the restored tqdm progress bars
"""
import requests
import time

def test_progress_bars():
    # Test with a very short video to see full progress bar cycle
    test_request = {
        "slides": ["3b762f4d-63d7-4eb4-ba99-cb7b6ec46b0d_slide_001.png"],
        "script": [
            {
                "text": "Quick test", 
                "duration": 2,  # Very short duration
                "slide": "3b762f4d-63d7-4eb4-ba99-cb7b6ec46b0d_slide_001.png"
            }
        ],
        "include_subtitles": False  # Faster without subtitles
    }
    
    print("🧪 Testing restored tqdm progress bars...")
    print("📋 Request details:")
    print(f"   - Slides: 1")
    print(f"   - Duration: 2 seconds")
    print(f"   - Subtitles: Disabled for speed")
    print()
    
    try:
        print("🚀 Starting video generation...")
        response = requests.post(
            'http://localhost:8000/generate-video',
            json=test_request,
            timeout=60
        )
        
        if response.status_code == 200:
            result = response.json()
            print(f"✅ SUCCESS! Video generated:")
            print(f"   📹 Video URL: {result['video_url']}")
            print(f"   ⏱️  Duration: {result['duration']}s")
            print(f"   🆔 Video ID: {result['video_id']}")
        else:
            print(f"❌ FAILED: {response.status_code}")
            print(f"   Error: {response.text}")
            
    except requests.exceptions.Timeout:
        print("⏰ Test timed out - video generation taking too long")
    except Exception as e:
        print(f"❌ Error: {e}")

if __name__ == "__main__":
    test_progress_bars() 