#!/usr/bin/env python3
"""
Test just the upload endpoint to isolate the bottleneck
"""

import requests
import time

def test_upload_endpoint():
    """Test the upload endpoint in isolation."""
    
    print("🧪 Testing Upload Endpoint")
    print("=" * 50)
    
    # First check if service is running
    try:
        response = requests.get('http://localhost:8000/')
        print("✅ Service is running")
    except requests.exceptions.ConnectionError:
        print("❌ Service is not running. Start with:")
        print("   python -m uvicorn src.main:app --reload --host 0.0.0.0 --port 8000")
        return
    
    pdf_file = "input/pdfs/OSU Roof Maxx Report - Final 2018.pdf"
    
    print(f"📄 Uploading: {pdf_file}")
    print("⏱️  Starting upload...")
    
    start_time = time.time()
    
    with open(pdf_file, 'rb') as f:
        files = {'file': ('OSU Roof Maxx Report - Final 2018.pdf', f, 'application/pdf')}
        
        try:
            response = requests.post(
                'http://localhost:8000/upload-pdf',
                files=files,
                timeout=60  # 60 second timeout
            )
            
            end_time = time.time()
            upload_time = end_time - start_time
            
            print(f"⏱️  Upload completed in {upload_time:.1f} seconds")
            
            if response.status_code == 200:
                result = response.json()
                print("✅ Upload successful!")
                print(f"   PDF ID: {result['pdf_id']}")
                print(f"   Pages: {result['total_pages']}")
                print(f"   Files: {result['slide_files'][:3]}...")
            else:
                print(f"❌ Upload failed: {response.status_code}")
                print(f"   Error: {response.text}")
                
        except requests.exceptions.Timeout:
            print("❌ Upload timed out after 60 seconds")
        except Exception as e:
            print(f"❌ Upload error: {e}")

if __name__ == "__main__":
    test_upload_endpoint() 