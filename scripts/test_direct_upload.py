#!/usr/bin/env python3
"""
Test upload processing directly without FastAPI overhead
"""

import sys
import time
from pathlib import Path

# Add src to path
sys.path.append('src')

def test_direct_upload():
    """Test the upload processing functions directly."""
    
    print("🧪 Testing Direct Upload Processing")
    print("=" * 50)
    
    # Import the function directly
    from main import convert_pdf_to_images
    import uuid
    
    pdf_file = Path("input/pdfs/OSU Roof Maxx Report - Final 2018.pdf")
    
    if not pdf_file.exists():
        print(f"❌ PDF not found: {pdf_file}")
        return
    
    print(f"📄 Processing: {pdf_file}")
    
    # Test with different DPI levels
    for dpi in [75, 150]:
        print(f"\n🔄 Testing DPI: {dpi}")
        
        pdf_id = str(uuid.uuid4())
        start_time = time.time()
        
        try:
            # Call the async function in a sync way for testing
            import asyncio
            slide_files = asyncio.run(convert_pdf_to_images(pdf_file, pdf_id, dpi=dpi))
            
            end_time = time.time()
            processing_time = end_time - start_time
            
            print(f"✅ Processed {len(slide_files)} slides in {processing_time:.1f} seconds")
            print(f"   Files: {slide_files[:3]}...")
            
            # Check if files were actually created
            output_dir = Path("output")
            created_files = [f for f in slide_files if (output_dir / f).exists()]
            print(f"   Created: {len(created_files)}/{len(slide_files)} files")
            
            if processing_time > 10:
                print(f"⚠️  DPI {dpi} too slow: {processing_time:.1f}s")
                break
                
        except Exception as e:
            print(f"❌ Error with DPI {dpi}: {e}")
            import traceback
            traceback.print_exc()

if __name__ == "__main__":
    test_direct_upload() 