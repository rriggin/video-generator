#!/usr/bin/env python3
"""
Test script for subtitle enhancements in the video generator.
This script tests different subtitle configurations to validate the improvements.
"""

import asyncio
import json
import requests
import time
from pathlib import Path
from typing import List, Dict

# Test configurations for different subtitle styles
SUBTITLE_CONFIGS = {
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
    "large_text": {
        "position": "bottom",
        "font_size": 48,
        "font_color": "white",
        "stroke_color": "black",
        "stroke_width": 3,
        "background_color": "black",
        "background_opacity": 0.8,
        "max_width": 0.9
    },
    "no_subtitles": {
        "include_subtitles": False
    }
}

# Sample script segments for testing
TEST_SCRIPT = [
    {
        "text": "Welcome to our subtitle enhancement test!",
        "duration": 5,
        "slide": "827d7006-c527-4b12-8e8a-85648a988978_slide_001.png"
    },
    {
        "text": "This is a test of different subtitle configurations to validate our improvements.",
        "duration": 6,
        "slide": "827d7006-c527-4b12-8e8a-85648a988978_slide_002.png"
    },
    {
        "text": "We're testing positioning, font sizes, colors, and background options.",
        "duration": 5,
        "slide": "827d7006-c527-4b12-8e8a-85648a988978_slide_003.png"
    }
]

class SubtitleEnhancementTester:
    def __init__(self, base_url: str = "http://localhost:8000"):
        self.base_url = base_url
        self.test_results = []
        
    async def test_service_health(self) -> bool:
        """Test if the video generator service is running."""
        try:
            response = requests.get(f"{self.base_url}/")
            if response.status_code == 200:
                print("✅ Service is running")
                return True
            else:
                print(f"❌ Service returned status {response.status_code}")
                return False
        except requests.exceptions.ConnectionError:
            print("❌ Cannot connect to service. Is it running?")
            return False
    
    async def test_subtitle_config_examples(self) -> bool:
        """Test the new subtitle configuration examples endpoint."""
        try:
            response = requests.get(f"{self.base_url}/subtitle-config-examples")
            if response.status_code == 200:
                configs = response.json()
                print("✅ Subtitle config examples endpoint working")
                print(f"   Available configs: {list(configs['examples'].keys())}")
                return True
            else:
                print(f"❌ Subtitle config examples failed: {response.status_code}")
                return False
        except Exception as e:
            print(f"❌ Error testing subtitle config examples: {e}")
            return False
    
    async def test_video_generation(self, config_name: str, subtitle_config: Dict) -> Dict:
        """Test video generation with a specific subtitle configuration."""
        print(f"\n🎬 Testing video generation with '{config_name}' configuration...")
        
        # Prepare the request
        request_data = {
            "slides": [
                "output/roofmaxx_test_video/slides/827d7006-c527-4b12-8e8a-85648a988978_slide_001.png",
                "output/roofmaxx_test_video/slides/827d7006-c527-4b12-8e8a-85648a988978_slide_002.png",
                "output/roofmaxx_test_video/slides/827d7006-c527-4b12-8e8a-85648a988978_slide_003.png"
            ],
            "script": TEST_SCRIPT,
            "voice": "female",
            "include_subtitles": subtitle_config.get("include_subtitles", True),
            "video_quality": "720p"
        }
        
        # Add subtitle config if subtitles are enabled
        if subtitle_config.get("include_subtitles", True):
            request_data["subtitle_config"] = subtitle_config
        
        try:
            start_time = time.time()
            response = requests.post(
                f"{self.base_url}/generate-video",
                json=request_data,
                timeout=300  # 5 minute timeout
            )
            end_time = time.time()
            
            if response.status_code == 200:
                result = response.json()
                print(f"✅ Video generated successfully!")
                print(f"   Video ID: {result['video_id']}")
                print(f"   Duration: {result['duration']:.1f}s")
                print(f"   URL: {result['video_url']}")
                print(f"   Generation time: {end_time - start_time:.1f}s")
                
                return {
                    "config_name": config_name,
                    "success": True,
                    "video_id": result['video_id'],
                    "duration": result['duration'],
                    "url": result['video_url'],
                    "generation_time": end_time - start_time
                }
            else:
                print(f"❌ Video generation failed: {response.status_code}")
                print(f"   Error: {response.text}")
                return {
                    "config_name": config_name,
                    "success": False,
                    "error": response.text,
                    "status_code": response.status_code
                }
                
        except requests.exceptions.Timeout:
            print("❌ Video generation timed out")
            return {
                "config_name": config_name,
                "success": False,
                "error": "Timeout"
            }
        except Exception as e:
            print(f"❌ Error during video generation: {e}")
            return {
                "config_name": config_name,
                "success": False,
                "error": str(e)
            }
    
    async def run_all_tests(self):
        """Run all subtitle enhancement tests."""
        print("🚀 Starting Subtitle Enhancement Tests")
        print("=" * 50)
        
        # Test 1: Service health
        if not await self.test_service_health():
            print("❌ Service health check failed. Please start the video generator service.")
            return
        
        # Test 2: Subtitle config examples endpoint
        if not await self.test_subtitle_config_examples():
            print("❌ Subtitle config examples test failed.")
            return
        
        # Test 3: Video generation with different subtitle configs
        print(f"\n🎬 Testing video generation with {len(SUBTITLE_CONFIGS)} different subtitle configurations...")
        
        for config_name, subtitle_config in SUBTITLE_CONFIGS.items():
            result = await self.test_video_generation(config_name, subtitle_config)
            self.test_results.append(result)
            
            # Add a small delay between tests
            await asyncio.sleep(2)
        
        # Generate test report
        self.generate_test_report()
    
    def generate_test_report(self):
        """Generate a comprehensive test report."""
        print("\n" + "=" * 50)
        print("📊 SUBTITLE ENHANCEMENT TEST REPORT")
        print("=" * 50)
        
        successful_tests = [r for r in self.test_results if r.get("success", False)]
        failed_tests = [r for r in self.test_results if not r.get("success", False)]
        
        print(f"✅ Successful tests: {len(successful_tests)}/{len(self.test_results)}")
        print(f"❌ Failed tests: {len(failed_tests)}/{len(self.test_results)}")
        
        if successful_tests:
            print("\n✅ SUCCESSFUL CONFIGURATIONS:")
            for result in successful_tests:
                print(f"   • {result['config_name']}: {result['duration']:.1f}s video")
                print(f"     URL: {result['url']}")
        
        if failed_tests:
            print("\n❌ FAILED CONFIGURATIONS:")
            for result in failed_tests:
                print(f"   • {result['config_name']}: {result.get('error', 'Unknown error')}")
        
        # Save detailed results to file
        report_file = Path("subtitle_test_report.json")
        with open(report_file, 'w') as f:
            json.dump({
                "test_timestamp": time.time(),
                "total_tests": len(self.test_results),
                "successful_tests": len(successful_tests),
                "failed_tests": len(failed_tests),
                "results": self.test_results
            }, f, indent=2)
        
        print(f"\n📄 Detailed report saved to: {report_file}")
        
        # Overall assessment
        if len(successful_tests) == len(self.test_results):
            print("\n🎉 ALL TESTS PASSED! Subtitle enhancements are working correctly.")
        elif len(successful_tests) > 0:
            print(f"\n⚠️  PARTIAL SUCCESS: {len(successful_tests)}/{len(self.test_results)} configurations working.")
        else:
            print("\n💥 ALL TESTS FAILED! Subtitle enhancements need debugging.")

async def main():
    """Main test function."""
    tester = SubtitleEnhancementTester()
    await tester.run_all_tests()

if __name__ == "__main__":
    asyncio.run(main()) 