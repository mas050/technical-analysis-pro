#!/bin/bash

# Technical Analysis Pro - Production Startup Script
# This script builds the frontend and runs the production server

echo "================================================"
echo "🚀 Starting Technical Analysis Pro (Production)"
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

# Build frontend
echo "🏗️  Building React frontend..."
cd frontend

# Install dependencies if needed
if [ ! -d "node_modules" ]; then
    echo "📦 Installing frontend dependencies..."
    npm install
fi

# Build production bundle
npm run build

cd ..

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
echo "✅ Build complete!"
echo "================================================"
echo ""
echo "🚀 Starting production server..."
echo ""

# Start Flask in production mode
python app.py

echo ""
echo "================================================"
echo "Server stopped"
echo "================================================"
