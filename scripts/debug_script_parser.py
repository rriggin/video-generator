#!/usr/bin/env python3
"""
Debug script to test script parsing functionality
"""

import requests
import json

def debug_script_parsing():
    # First get slides
    with open("input/pdfs/OSU Roof Maxx Report - Final 2018.pdf", 'rb') as f:
        files = {'file': ('OSU Roof Maxx Report - Final 2018.pdf', f, 'application/pdf')}
        pdf_response = requests.post('http://localhost:8000/upload-pdf', files=files)
    
    pdf_result = pdf_response.json()
    print(f"📄 PDF uploaded: {len(pdf_result['slide_files'])} slides")
    print(f"First 3 slide files: {pdf_result['slide_files'][:3]}")
    
    # Parse script with slide files
    with open("input/scripts/roofmaxx-ohio-study-script.txt", 'rb') as f:
        files = {'file': ('roofmaxx-ohio-study-script.txt', f, 'text/plain')}
        data = {'slide_files': json.dumps(pdf_result['slide_files'])}
        script_response = requests.post('http://localhost:8000/parse-script', files=files, data=data)
    
    script_result = script_response.json()
    print(f"\n📝 Script parsed: {script_result['total_segments']} segments")
    print(f"First 3 parsed segments:")
    for i, segment in enumerate(script_result['parsed_segments'][:3]):
        print(f"  {i+1}. Slide: {segment['slide']}")
        print(f"     Text: {segment['text'][:50]}...")
        print(f"     Duration: {segment['duration']}s")

if __name__ == "__main__":
    debug_script_parsing() 