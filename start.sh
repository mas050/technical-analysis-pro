#!/bin/bash

# Technical Analysis Pro - Startup Script
# This script starts both the Flask backend and React frontend

echo "================================================"
echo "🚀 Starting Technical Analysis Pro"
echo "================================================"
echo ""

# Check if Python is installed
if ! command -v python3 &> /dev/null; then
    echo "❌ Python 3 is not installed. Please install Python 3.9 or higher."
    exit 1
fi

# Check if Node.js is installed
if ! command -v node &> /dev/null; then
    echo "❌ Node.js is not installed. Please install Node.js 16 or higher."
    exit 1
fi

# Check if virtual environment exists
if [ ! -d "venv" ]; then
    echo "📦 Creating virtual environment..."
    python3 -m venv venv
fi

# Activate virtual environment
echo "🔧 Activating virtual environment..."
source venv/bin/activate

# Install Python dependencies
echo "📦 Installing Python dependencies..."
pip install -q -r requirements.txt

# Check if frontend dependencies are installed
if [ ! -d "frontend/node_modules" ]; then
    echo "📦 Installing frontend dependencies..."
    cd frontend
    npm install
    cd ..
fi

# Create necessary directories
mkdir -p charts
mkdir -p reports

# Check for GEMINI_API_KEY
if [ -z "$GEMINI_API_KEY" ]; then
    echo ""
    echo "⚠️  Warning: GEMINI_API_KEY environment variable is not set."
    echo "   AI insights will not be available without an API key."
    echo "   Get your free key at: https://makersuite.google.com/app/apikey"
    echo ""
fi

echo ""
echo "================================================"
echo "✅ Setup complete!"
echo "================================================"
echo ""
echo "Starting services..."
echo ""

# Start Flask backend in background
echo "🔧 Starting Flask backend on port 5000..."
python app.py &
BACKEND_PID=$!

# Wait a bit for backend to start
sleep 3

# Start React frontend
echo "🎨 Starting React frontend on port 3000..."
cd frontend
npm start &
FRONTEND_PID=$!

echo ""
echo "================================================"
echo "🎉 Application is starting!"
echo "================================================"
echo ""
echo "📊 Backend API: http://localhost:5000"
echo "🌐 Frontend UI: http://localhost:3000"
echo ""
echo "Press Ctrl+C to stop all services"
echo "================================================"
echo ""

# Wait for Ctrl+C
trap "echo ''; echo 'Stopping services...'; kill $BACKEND_PID $FRONTEND_PID 2>/dev/null; exit" INT

# Keep script running
wait
