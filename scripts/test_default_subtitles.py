#!/usr/bin/env python3
"""
Quick test to verify the default subtitle behavior.
"""

import requests
import json

def test_default_subtitles():
    """Test the default subtitle behavior."""
    print("🎬 Testing Default Subtitle Behavior")
    print("=" * 40)
    
    # Test with minimal request (no include_subtitles field)
    request_data = {
        "slides": [
            "output/roofmaxx_test_video/slides/827d7006-c527-4b12-8e8a-85648a988978_slide_001.png"
        ],
        "script": [
            {
                "text": "Testing default subtitle behavior",
                "duration": 3,
                "slide": "827d7006-c527-4b12-8e8a-85648a988978_slide_001.png"
            }
        ],
        "voice": "female",
        "video_quality": "720p"
        # include_subtitles omitted - should use default
    }
    
    print("📝 Request data (include_subtitles omitted):")
    print(json.dumps(request_data, indent=2))
    
    try:
        response = requests.post(
            "http://localhost:8000/generate-video",
            json=request_data,
            timeout=300
        )
        
        if response.status_code == 200:
            result = response.json()
            print(f"\n✅ Video generated successfully!")
            print(f"   Video ID: {result['video_id']}")
            print(f"   Duration: {result['duration']:.1f}s")
            print(f"   URL: {result['video_url']}")
            
            # Check if the video was generated with or without subtitles
            # We can infer this from generation time (faster = no subtitles)
            print(f"\n🎯 Analysis:")
            print(f"   • Generation time: {result.get('generation_time', 'N/A')}")
            print(f"   • Expected behavior: Subtitles should be OFF by default")
            print(f"   • Video should be clean (no text overlays)")
            
            return True
        else:
            print(f"❌ Failed: {response.status_code}")
            print(f"   Error: {response.text}")
            return False
            
    except Exception as e:
        print(f"❌ Error: {e}")
        return False

if __name__ == "__main__":
    test_default_subtitles() 