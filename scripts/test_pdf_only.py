#!/usr/bin/env python3
"""
Minimal test to isolate PDF processing bottleneck
"""

import time
from pathlib import Path

def test_pdf_processing():
    """Test just the PDF→image conversion without any server overhead."""
    
    print("🧪 Testing PDF Processing in Isolation")
    print("=" * 50)
    
    pdf_file = "input/pdfs/OSU Roof Maxx Report - Final 2018.pdf"
    
    if not Path(pdf_file).exists():
        print(f"❌ PDF file not found: {pdf_file}")
        return
    
    print(f"📄 Testing: {pdf_file}")
    
    try:
        from pdf2image import convert_from_path
        
        # Test different DPI levels to find the sweet spot
        for dpi in [75, 150, 300]:
            print(f"\n🔄 Testing DPI: {dpi}")
            start_time = time.time()
            
            images = convert_from_path(pdf_file, dpi=dpi)
            
            end_time = time.time()
            processing_time = end_time - start_time
            
            print(f"✅ Processed {len(images)} pages in {processing_time:.1f} seconds")
            print(f"   Average: {processing_time/len(images):.2f}s per page")
            print(f"   First image size: {images[0].width}x{images[0].height}")
            
            # Clean up memory
            del images
            
            if processing_time > 30:
                print(f"⚠️  DPI {dpi} is too slow ({processing_time:.1f}s)")
                break
            else:
                print(f"✅ DPI {dpi} is acceptable")
    
    except ImportError:
        print("❌ pdf2image not installed")
    except Exception as e:
        print(f"❌ Error: {e}")

if __name__ == "__main__":
    test_pdf_processing() 