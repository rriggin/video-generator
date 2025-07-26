#!/bin/bash
# Enhanced script to start the video generator service with automated health checks
# This eliminates venv confusion by handling the path correctly

# Parse command line arguments
SKIP_TESTS=false
if [[ "$1" == "--skip-tests" || "$1" == "-s" ]]; then
    SKIP_TESTS=true
fi

# Get the directory where this script is located
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(dirname "$SCRIPT_DIR")"

# If this script is in the project root, use current directory
if [ "$(basename "$SCRIPT_DIR")" = "video-generator" ]; then
    PROJECT_ROOT="$SCRIPT_DIR"
fi

echo "🎬 Starting Video Generator Service..."
echo "📁 Script directory: $SCRIPT_DIR"
echo "📁 Project root: $PROJECT_ROOT"

# Activate the virtual environment
echo "🔧 Activating virtual environment..."
source "$PROJECT_ROOT/venv/bin/activate"

# Check if activation worked
if [ $? -eq 0 ]; then
    echo "✅ Virtual environment activated successfully"
    echo "🐍 Python path: $(which python)"
    echo "🐍 Python version: $(python --version)"
else
    echo "❌ Failed to activate virtual environment"
    exit 1
fi

# Change to the project root directory
cd "$PROJECT_ROOT"

# Function to wait for service to be ready
wait_for_service() {
    local url="http://localhost:8000"
    local timeout=30
    echo "⏳ Waiting for service to be ready..."
    
    for ((i=1; i<=timeout; i++)); do
        if curl -s "$url" > /dev/null 2>&1; then
            echo "✅ Service is ready!"
            return 0
        fi
        sleep 1
        if [ $((i % 5)) -eq 0 ]; then
            echo "   Still waiting... ($i/${timeout}s)"
        fi
    done
    
    echo "❌ Service failed to start within ${timeout}s timeout"
    return 1
}

# Function to run basic health checks
run_health_checks() {
    echo "🧪 Running automated health checks..."
    echo "=" * 50
    
    # Test 1: Health check endpoint
    echo "📋 Test 1: Health check endpoint..."
    response=$(curl -s http://localhost:8000/)
    if echo "$response" | grep -q "Video Generator Service"; then
        echo "✅ Health check passed"
    else
        echo "❌ Health check failed"
        return 1
    fi
    
    # Test 2: Subtitle config examples endpoint
    echo "📋 Test 2: Subtitle config examples..."
    response=$(curl -s http://localhost:8000/subtitle-config-examples)
    if echo "$response" | grep -q "examples"; then
        echo "✅ Subtitle config endpoint working"
    else
        echo "❌ Subtitle config endpoint failed"
        return 1
    fi
    
    # Test 3: API documentation available
    echo "📋 Test 3: API documentation..."
    response=$(curl -s http://localhost:8000/docs)
    if echo "$response" | grep -q "swagger-ui"; then
        echo "✅ API documentation available"
    else
        echo "❌ API documentation unavailable"
        return 1
    fi
    
    echo "🎉 All health checks passed!"
    echo ""
    echo "🌐 Service URLs:"
    echo "   • API: http://localhost:8000"
    echo "   • Docs: http://localhost:8000/docs"
    echo "   • Health: http://localhost:8000/"
    echo ""
    return 0
}

# Function to test complete workflow automatically
test_complete_workflow() {
    echo "🎬 Running automated complete workflow test..."
    echo "=" * 60
    
    # Check if test files exist
    if [ ! -f "input/pdfs/OSU Roof Maxx Report - Final 2018.pdf" ]; then
        echo "⚠️  Test PDF not found, skipping workflow test"
        return 0
    fi
    
    if [ ! -f "input/scripts/roofmaxx-ohio-study-script.txt" ]; then
        echo "⚠️  Test script not found, skipping workflow test"
        return 0
    fi
    
    echo "📋 Testing streamlined /generate-video endpoint..."
    echo "📁 PDF: OSU Roof Maxx Report - Final 2018.pdf"
    echo "📝 Script: roofmaxx-ohio-study-script.txt"
    echo ""
    
    # Run the complete workflow test
    response=$(curl -X POST \
        -F "pdf_file=@input/pdfs/OSU Roof Maxx Report - Final 2018.pdf" \
        -F "script_file=@input/scripts/roofmaxx-ohio-study-script.txt" \
        -F "voice=female" \
        -F "include_subtitles=false" \
        -F "video_quality=720p" \
        http://localhost:8000/generate-video \
        2>/dev/null)
    
    if echo "$response" | grep -q "video_url"; then
        echo "🎉 COMPLETE WORKFLOW SUCCESS!"
        echo "$response" | python3 -c "
import sys, json
try:
    data = json.load(sys.stdin)
    print(f'✅ Video generated successfully!')
    print(f'🎬 Video ID: {data[\"video_id\"]}')
    print(f'🎬 Video URL: {data[\"video_url\"]}')
    print(f'⏱️  Duration: {data[\"duration\"]}s ({int(data[\"duration\"]//60)}:{int(data[\"duration\"]%60):02d})')
    print(f'📊 Status: {data[\"status\"]}')
except:
    print('✅ Workflow completed (JSON parsing issue)')
"
        echo ""
        echo "🎯 CustomGPT Integration Ready!"
        echo "📍 Use endpoint: POST /generate-video"
        echo "📍 Upload: PDF file + script file"
        echo "📍 Returns: Video URL immediately"
    else
        echo "❌ Complete workflow test failed"
        echo "Response: $response"
        return 1
    fi
    
    return 0
}

# Start the service in background
echo "🚀 Starting video generator service in background..."
cd "$PROJECT_ROOT"
python app.py &
SERVICE_PID=$!

# Give the service a moment to start
sleep 2

# Check if process is still running
if ! kill -0 $SERVICE_PID 2>/dev/null; then
    echo "❌ Service failed to start"
    exit 1
fi

echo "✅ Service started (PID: $SERVICE_PID)"

# Wait for service to be ready and run health checks
if wait_for_service; then
    if [ "$SKIP_TESTS" = false ]; then
        if run_health_checks; then
            echo "🎯 Service ready and all health checks passed!"
            # Run complete workflow test automatically
            if test_complete_workflow; then
                echo ""
                echo "🚀 ALL SYSTEMS GO! Service is fully operational."
            else
                echo "⚠️  Service running but workflow test failed"
                echo "💡 Individual endpoints work, check logs for workflow issues"
            fi
        else
            echo "⚠️  Service started but some health checks failed"
            echo "💡 You can still use the service, but check the logs for issues"
        fi
    else
        echo "⏭️  Health checks skipped (use without --skip-tests to run them)"
        echo "🌐 Service available at: http://localhost:8000"
    fi
else
    echo "❌ Service startup verification failed"
    kill $SERVICE_PID 2>/dev/null
    exit 1
fi

# Keep the service running
echo ""
echo "🔄 Service is running. Press Ctrl+C to stop."
echo "💡 Usage: ./start_service.sh [--skip-tests|-s] to skip health checks"
echo ""

# Wait for the service process or handle Ctrl+C
trap 'echo ""; echo "🛑 Stopping service..."; kill $SERVICE_PID 2>/dev/null; wait $SERVICE_PID 2>/dev/null; echo "✅ Service stopped"; exit 0' INT

wait $SERVICE_PID 