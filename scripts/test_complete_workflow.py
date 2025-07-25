#!/usr/bin/env python3
"""
Integration test that validates the COMPLETE workflow.
This test will fail if any step is bypassed.
"""

import requests
import json

def test_complete_workflow():
    """Test that all three endpoints work together properly."""
    
    print("🧪 Testing COMPLETE Agent Workflow")
    print("=" * 50)
    
    # Step 1: Upload PDF (REQUIRED)
    print("📄 Step 1: Upload PDF...")
    with open("input/pdfs/OSU Roof Maxx Report - Final 2018.pdf", 'rb') as f:
        files = {'file': ('OSU Roof Maxx Report - Final 2018.pdf', f, 'application/pdf')}
        pdf_response = requests.post('http://localhost:8000/upload-pdf', files=files)
    
    assert pdf_response.status_code == 200, "PDF upload failed"
    pdf_result = pdf_response.json()
    print(f"✅ PDF uploaded: {pdf_result['total_pages']} slides")
    
    # Step 2: Parse Script (REQUIRED - don't skip!)
    print("📝 Step 2: Parse Script...")
    with open("input/scripts/roofmaxx-ohio-study-script.txt", 'rb') as f:
        files = {'file': ('roofmaxx-ohio-study-script.txt', f, 'text/plain')}
        script_response = requests.post('http://localhost:8000/parse-script', files=files)
    
    assert script_response.status_code == 200, "Script parsing failed"
    script_result = script_response.json()
    print(f"✅ Script parsed: {script_result['total_segments']} segments, {script_result['total_duration']}s")
    
    # Step 3: Generate Video (using results from Steps 1 & 2)
    print("🎥 Step 3: Generate Video...")
    video_request = {
        "slides": pdf_result['slide_files'],
        "script": script_result['parsed_segments'],
        "voice": "female",
        "include_subtitles": False,
        "video_quality": "720p"
    }
    
    video_response = requests.post('http://localhost:8000/generate-video', json=video_request)
    assert video_response.status_code == 200, "Video generation failed"
    video_result = video_response.json()
    
    print(f"✅ Video created: {video_result['duration']:.1f}s")
    print(f"🎯 Complete workflow validated!")
    
    # Validate that we used the real script timing
    expected_duration = script_result['total_duration']
    actual_duration = video_result['duration']
    assert abs(actual_duration - expected_duration) < 10, f"Duration mismatch: expected ~{expected_duration}s, got {actual_duration}s"
    
    return True

if __name__ == "__main__":
    try:
        test_complete_workflow()
        print("🎉 Complete workflow test PASSED")
    except Exception as e:
        print(f"❌ Complete workflow test FAILED: {e}")
        exit(1) 