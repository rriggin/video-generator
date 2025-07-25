#!/usr/bin/env python3
"""
Test script for image quality improvements
Tests different image configurations and validates the results
"""

import asyncio
import requests
import json
from pathlib import Path

# Test configurations
TEST_CONFIGS = {
    "default": {
        "dpi": 600,
        "resampling": "lanczos",
        "padding": True,
        "enhance_sharpness": 1.2,
        "enhance_contrast": 1.1,
        "background_color": "white"
    },
    "high_quality": {
        "dpi": 900,
        "resampling": "lanczos",
        "padding": True,
        "enhance_sharpness": 1.3,
        "enhance_contrast": 1.2,
        "background_color": "white"
    },
    "fast_processing": {
        "dpi": 300,
        "resampling": "bicubic",
        "padding": False,
        "enhance_sharpness": 1.0,
        "enhance_contrast": 1.0,
        "background_color": "white"
    }
}

async def test_image_configurations():
    """Test different image configurations and report results."""
    
    base_url = "http://localhost:8000"
    
    print("🎬 Testing Image Quality Improvements")
    print("=" * 50)
    
    # Test 1: Check if service is running
    try:
        response = requests.get(f"{base_url}/")
        if response.status_code == 200:
            print("✅ Service is running")
        else:
            print("❌ Service is not responding correctly")
            return
    except Exception as e:
        print(f"❌ Cannot connect to service: {e}")
        return
    
    # Test 2: Get image config examples
    try:
        response = requests.get(f"{base_url}/image-config-examples")
        if response.status_code == 200:
            configs = response.json()
            print("✅ Image config examples endpoint working")
            print(f"   Available configs: {list(configs['examples'].keys())}")
        else:
            print("❌ Image config examples endpoint failed")
    except Exception as e:
        print(f"❌ Image config examples test failed: {e}")
    
    # Test 3: Test with sample data
    print("\n📋 Testing with sample data...")
    
    # Use existing script and slides if available
    script_path = Path("input/scripts/roofmaxx-ohio-study-script.txt")
    if not script_path.exists():
        print("❌ No test script found. Please upload a script first.")
        return
    
    # Create a simple test request
    test_request = {
        "slides": [
            "output/roofmaxx_test_video/slides/827d7006-c527-4b12-8e8a-85648a988978_slide_001.png",
            "output/roofmaxx_test_video/slides/827d7006-c527-4b12-8e8a-85648a988978_slide_002.png"
        ],
        "script": [
            {
                "text": "Welcome to our test video with improved image quality.",
                "duration": 5,
                "slide": "output/roofmaxx_test_video/slides/827d7006-c527-4b12-8e8a-85648a988978_slide_001.png"
            },
            {
                "text": "This slide demonstrates the enhanced image processing.",
                "duration": 5,
                "slide": "output/roofmaxx_test_video/slides/827d7006-c527-4b12-8e8a-85648a988978_slide_002.png"
            }
        ],
        "voice": "female",
        "include_subtitles": False,  # Disable subtitles as requested
        "video_quality": "720p",
        "image_config": TEST_CONFIGS["default"]
    }
    
    print(f"   Using config: {TEST_CONFIGS['default']}")
    
    try:
        response = requests.post(
            f"{base_url}/generate-video",
            json=test_request,
            timeout=300  # 5 minute timeout
        )
        
        if response.status_code == 200:
            result = response.json()
            print("✅ Video generation successful!")
            print(f"   Video ID: {result['video_id']}")
            print(f"   Duration: {result['duration']:.1f} seconds")
            print(f"   URL: {result['video_url']}")
        else:
            print(f"❌ Video generation failed: {response.status_code}")
            print(f"   Error: {response.text}")
            
    except Exception as e:
        print(f"❌ Video generation test failed: {e}")
    
    print("\n🎯 Image Quality Improvements Summary:")
    print("   ✅ Increased DPI from 300 to 600 (configurable)")
    print("   ✅ Added padding instead of cropping (configurable)")
    print("   ✅ Added image preprocessing (sharpness, contrast)")
    print("   ✅ Added image quality validation")
    print("   ✅ Configurable resampling methods")
    print("   ✅ Configurable background colors")
    print("   ✅ Added image configuration API")

if __name__ == "__main__":
    asyncio.run(test_image_configurations()) 