#!/usr/bin/env python3
"""
Video Generator Test Runner
Handles the complete workflow: start service, run test, cleanup
"""

import subprocess
import time
import requests
import sys
import os
from pathlib import Path

def wait_for_service(url="http://localhost:8000", timeout=30):
    """Wait for the service to be ready."""
    print("⏳ Waiting for service to start...")
    for i in range(timeout):
        try:
            response = requests.get(url)
            if response.status_code == 200:
                print("✅ Service is ready!")
                return True
        except requests.exceptions.ConnectionError:
            pass
        time.sleep(1)
        if i % 5 == 0:
            print(f"   Still waiting... ({i+1}/{timeout}s)")
    
    print("❌ Service failed to start within timeout")
    return False

def run_test():
    """Run the PDF upload test."""
    print("🧪 Running PDF upload test...")
    
    # Import and run the test
    sys.path.append(str(Path(__file__).parent / "tests"))
    from test_pdf_upload import test_pdf_upload
    
    try:
        test_pdf_upload()
        print("✅ Test completed successfully!")
        return True
    except Exception as e:
        print(f"❌ Test failed: {e}")
        return False

def main():
    """Main test workflow."""
    print("🎬 Video Generator Test Workflow")
    print("=" * 50)
    
    # Step 1: Start the service
    print("\n🚀 Step 1: Starting the service...")
    service_process = subprocess.Popen(
        ["python", "app.py"],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE
    )
    
    try:
        # Step 2: Wait for service to be ready
        if not wait_for_service():
            print("❌ Failed to start service")
            return False
        
        # Step 3: Run the test
        print("\n🧪 Step 2: Running test...")
        if not run_test():
            print("❌ Test failed")
            return False
        
        print("\n🎉 All tests passed!")
        return True
        
    finally:
        # Step 4: Cleanup
        print("\n🧹 Step 3: Cleaning up...")
        service_process.terminate()
        service_process.wait()
        print("✅ Service stopped")

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1) 