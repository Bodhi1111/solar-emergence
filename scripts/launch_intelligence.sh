#!/bin/bash

# SOLAR EMERGENCE - Launch Emergent Intelligence Discovery System
# Processes 1,500 videos sequentially with pattern emergence

set -e

echo "🌟 SOLAR EMERGENCE - Emergent Intelligence Discovery System"
echo "================================================"
echo "Mode: UNCONSTRAINED DISCOVERY"
echo "Constraint: LOCAL_ONLY, ZERO_COST"
echo "Videos: 1,500 sequential processing"
echo "================================================"

# Check environment
if [ ! -f ".env.discovery" ]; then
    echo "❌ Missing .env.discovery configuration file"
    exit 1
fi

# Load discovery configuration
source .env.discovery

# Create necessary directories
echo "📁 Creating discovery directories..."
mkdir -p intelligence_checkpoints
mkdir -p data/discoveries/unknown_correlations
mkdir -p data/discoveries/novel_sequences
mkdir -p data/discoveries/cross_modal_patterns
mkdir -p data/discoveries/threshold_discoveries
mkdir -p data/discoveries/meta_patterns
mkdir -p data/videos/queue
mkdir -p data/videos/processing
mkdir -p data/videos/processed
mkdir -p data/intelligence

echo "✅ Directories ready"

# Check Python environment
echo "🐍 Checking Python environment..."
if ! command -v python3 &> /dev/null; then
    echo "❌ Python 3 not found"
    exit 1
fi

# Check required Python packages
echo "📦 Checking required packages..."
python3 -c "import cv2, mediapipe, numpy, fastapi" 2>/dev/null || {
    echo "⚠️  Some packages missing. Installing..."
    pip3 install -r requirements-ml.txt || {
        echo "❌ Failed to install packages"
        exit 1
    }
}

# Start ML Bridge
echo "🌉 Starting ML Bridge..."
cd bridge
python3 -m uvicorn ml_connector:app --reload --port 8000 &
ML_BRIDGE_PID=$!
cd ..

# Wait for ML Bridge to be ready
echo "⏳ Waiting for ML Bridge to initialize..."
sleep 5

# Test ML Bridge
echo "🔍 Testing ML Bridge connection..."
curl -s http://localhost:8000/health > /dev/null || {
    echo "❌ ML Bridge not responding"
    kill $ML_BRIDGE_PID 2>/dev/null
    exit 1
}

echo "✅ ML Bridge active"

# Check Node environment
echo "📦 Checking Node environment..."
if ! command -v node &> /dev/null; then
    echo "❌ Node.js not found"
    kill $ML_BRIDGE_PID 2>/dev/null
    exit 1
fi

# Install Node dependencies if needed
if [ ! -d "node_modules" ]; then
    echo "📦 Installing Node dependencies..."
    npm install
fi

# Launch discovery pipeline
echo "🚀 Launching Emergent Intelligence Pipeline..."
echo "================================================"
echo "Processing mode: SEQUENTIAL"
echo "Starting from video: $CURRENT_VIDEO"
echo "Total videos: $TOTAL_VIDEOS"
echo "Checkpoint frequency: Every $CHECKPOINT_FREQUENCY videos"
echo "Unknown space allocation: $UNKNOWN_SPACE_ALLOCATION"
echo "================================================"

# Start the main pipeline
npm run process:sequential &
PIPELINE_PID=$!

# Start discovery monitor in another terminal if available
if command -v gnome-terminal &> /dev/null; then
    gnome-terminal -- bash -c "python3 scripts/monitor_emergence.py --realtime; exec bash"
elif command -v xterm &> /dev/null; then
    xterm -e "python3 scripts/monitor_emergence.py --realtime" &
else
    echo "ℹ️  Run 'python3 scripts/monitor_emergence.py --realtime' in another terminal to monitor discoveries"
fi

# Function to cleanup on exit
cleanup() {
    echo "🛑 Shutting down..."
    kill $ML_BRIDGE_PID 2>/dev/null
    kill $PIPELINE_PID 2>/dev/null
    echo "✅ Cleanup complete"
}

trap cleanup EXIT

# Monitor the pipeline
echo "📊 Pipeline running. Press Ctrl+C to stop."
echo "View discoveries: python3 scripts/view_discoveries.py"
echo "View intelligence: python3 scripts/generate_intelligence_report.py"

# Wait for pipeline to complete or user interrupt
wait $PIPELINE_PID

echo "✅ Processing complete!"
echo "📊 Generating final intelligence report..."
python3 scripts/generate_intelligence_report.py

echo "🎉 SOLAR EMERGENCE - Discovery session complete!"