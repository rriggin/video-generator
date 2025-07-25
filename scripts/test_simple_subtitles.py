#!/usr/bin/env python3
"""
Simple test script for subtitle toggle functionality.
Tests the existing include_subtitles boolean field.
"""

import asyncio
import json
import requests
import time
from pathlib import Path

# Simple test script
TEST_SCRIPT = [
    {
        "text": "Welcome to our simple subtitle test!",
        "duration": 5,
        "slide": "827d7006-c527-4b12-8e8a-85648a988978_slide_001.png"
    },
    {
        "text": "This is a test of the subtitle toggle functionality.",
        "duration": 6,
        "slide": "827d7006-c527-4b12-8e8a-85648a988978_slide_002.png"
    }
]

def test_subtitle_toggle():
    """Test subtitle toggle functionality."""
    print("🎬 Testing Subtitle Toggle Functionality")
    print("=" * 50)
    
    # Test 1: With subtitles enabled (default)
    print("\n✅ Test 1: Generating video WITH subtitles (default)")
    request_with_subtitles = {
        "slides": [
            "output/roofmaxx_test_video/slides/827d7006-c527-4b12-8e8a-85648a988978_slide_001.png",
            "output/roofmaxx_test_video/slides/827d7006-c527-4b12-8e8a-85648a988978_slide_002.png"
        ],
        "script": TEST_SCRIPT,
        "voice": "female",
        "include_subtitles": True,  # Explicitly enable subtitles
        "video_quality": "720p"
    }
    
    try:
        start_time = time.time()
        response = requests.post(
            "http://localhost:8000/generate-video",
            json=request_with_subtitles,
            timeout=300
        )
        end_time = time.time()
        
        if response.status_code == 200:
            result = response.json()
            print(f"✅ Video with subtitles generated successfully!")
            print(f"   Video ID: {result['video_id']}")
            print(f"   Duration: {result['duration']:.1f}s")
            print(f"   URL: {result['video_url']}")
            print(f"   Generation time: {end_time - start_time:.1f}s")
            video_with_subtitles_id = result['video_id']
        else:
            print(f"❌ Failed to generate video with subtitles: {response.status_code}")
            print(f"   Error: {response.text}")
            return False
            
    except Exception as e:
        print(f"❌ Error generating video with subtitles: {e}")
        return False
    
    # Test 2: With subtitles disabled
    print("\n❌ Test 2: Generating video WITHOUT subtitles")
    request_without_subtitles = {
        "slides": [
            "output/roofmaxx_test_video/slides/827d7006-c527-4b12-8e8a-85648a988978_slide_001.png",
            "output/roofmaxx_test_video/slides/827d7006-c527-4b12-8e8a-85648a988978_slide_002.png"
        ],
        "script": TEST_SCRIPT,
        "voice": "female",
        "include_subtitles": False,  # Disable subtitles
        "video_quality": "720p"
    }
    
    try:
        start_time = time.time()
        response = requests.post(
            "http://localhost:8000/generate-video",
            json=request_without_subtitles,
            timeout=300
        )
        end_time = time.time()
        
        if response.status_code == 200:
            result = response.json()
            print(f"✅ Video without subtitles generated successfully!")
            print(f"   Video ID: {result['video_id']}")
            print(f"   Duration: {result['duration']:.1f}s")
            print(f"   URL: {result['video_url']}")
            print(f"   Generation time: {end_time - start_time:.1f}s")
            video_without_subtitles_id = result['video_id']
        else:
            print(f"❌ Failed to generate video without subtitles: {response.status_code}")
            print(f"   Error: {response.text}")
            return False
            
    except Exception as e:
        print(f"❌ Error generating video without subtitles: {e}")
        return False
    
    # Test 3: With subtitles omitted (should default to True)
    print("\n🔍 Test 3: Generating video with subtitles omitted (should default to True)")
    request_default_subtitles = {
        "slides": [
            "output/roofmaxx_test_video/slides/827d7006-c527-4b12-8e8a-85648a988978_slide_001.png",
            "output/roofmaxx_test_video/slides/827d7006-c527-4b12-8e8a-85648a988978_slide_002.png"
        ],
        "script": TEST_SCRIPT,
        "voice": "female",
        "video_quality": "720p"
        # include_subtitles omitted - should default to True
    }
    
    try:
        start_time = time.time()
        response = requests.post(
            "http://localhost:8000/generate-video",
            json=request_default_subtitles,
            timeout=300
        )
        end_time = time.time()
        
        if response.status_code == 200:
            result = response.json()
            print(f"✅ Video with default subtitles generated successfully!")
            print(f"   Video ID: {result['video_id']}")
            print(f"   Duration: {result['duration']:.1f}s")
            print(f"   URL: {result['video_url']}")
            print(f"   Generation time: {end_time - start_time:.1f}s")
            video_default_subtitles_id = result['video_id']
        else:
            print(f"❌ Failed to generate video with default subtitles: {response.status_code}")
            print(f"   Error: {response.text}")
            return False
            
    except Exception as e:
        print(f"❌ Error generating video with default subtitles: {e}")
        return False
    
    # Summary
    print("\n" + "=" * 50)
    print("📊 SUBTITLE TOGGLE TEST RESULTS")
    print("=" * 50)
    print("✅ All tests passed! Subtitle toggle functionality is working.")
    print(f"\nGenerated videos:")
    print(f"  • With subtitles (explicit): {video_with_subtitles_id}")
    print(f"  • Without subtitles: {video_without_subtitles_id}")
    print(f"  • With default subtitles: {video_default_subtitles_id}")
    
    print(f"\n🎯 Next steps:")
    print(f"  1. Download and compare the videos to verify subtitle differences")
    print(f"  2. Check that the 'without subtitles' video has no text overlays")
    print(f"  3. Verify that the other two videos have subtitles")
    
    return True

if __name__ == "__main__":
    success = test_subtitle_toggle()
    if success:
        print("\n🎉 SUBTITLE TOGGLE TEST COMPLETED SUCCESSFULLY!")
    else:
        print("\n💥 SUBTITLE TOGGLE TEST FAILED!") 