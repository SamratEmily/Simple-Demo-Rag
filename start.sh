#!/bin/bash

# Simple RAG Chat - Startup Script
echo "🚀 Starting Simple RAG Chat..."

# Check if .env exists
if [ ! -f .env ]; then
    echo "❌ .env file not found. Please create one with your GEMINI_API_KEY"
    echo "Example: echo 'GEMINI_API_KEY=your_key_here' > .env"
    exit 1
fi

# Check if virtual environment exists
if [ ! -d .venv ]; then
    echo "❌ Virtual environment not found. Please run setup first:"
    echo "python3 -m venv .venv"
    echo "source .venv/bin/activate"
    echo "pip install -r requirements.txt"
    exit 1
fi

echo "✅ Environment looks good!"

# Start FastAPI server in background
echo "🔧 Starting FastAPI server on http://127.0.0.1:8000"
source .venv/bin/activate
uvicorn api:app --host 127.0.0.1 --port 8000 &
API_PID=$!

# Wait a moment for API to start
sleep 3

# Start React dev server in background
echo "🎨 Starting React dev server on http://127.0.0.1:5173"
cd ui
npm run dev -- --host 127.0.0.1 --port 5173 &
REACT_PID=$!

echo ""
echo "🎉 Both servers are starting up!"
echo "📱 React UI: http://127.0.0.1:5173"
echo "🔌 API: http://127.0.0.1:8000"
echo "📖 API Docs: http://127.0.0.1:8000/docs"
echo ""
echo "Press Ctrl+C to stop both servers"

# Function to cleanup on exit
cleanup() {
    echo ""
    echo "🛑 Stopping servers..."
    kill $API_PID 2>/dev/null
    kill $REACT_PID 2>/dev/null
    echo "✅ Servers stopped"
    exit 0
}

# Set trap to cleanup on script exit
trap cleanup SIGINT SIGTERM

# Wait for both processes
wait
