#!/bin/bash

# Development script for Health Fact Checker

echo "🚀 Starting Health Fact Checker Development Servers..."

# Check if .env file exists
if [ ! -f .env ]; then
    echo "⚠️  Warning: .env file not found. Please create one using .env.example as template."
    exit 1
fi

# Check if node_modules exists
if [ ! -d "node_modules" ]; then
    echo "📦 Installing Node.js dependencies..."
    npm install
fi

# Check if Python dependencies are installed
if ! python -c "import fastapi" 2>/dev/null; then
    echo "🐍 Installing Python dependencies..."
    pip install -r requirements.txt
fi

# Start both servers in the background
echo "🌐 Starting Frontend (NextJS) on http://localhost:3000..."
npm run dev &
FRONTEND_PID=$!

echo "🔧 Starting Backend (FastAPI) on http://localhost:8000..."
cd api && python main.py &
BACKEND_PID=$!

# Wait for servers to start
sleep 3

echo "✅ Development servers started!"
echo "   Frontend: http://localhost:3000"
echo "   Backend:  http://localhost:8000"
echo "   Press Ctrl+C to stop both servers"

# Handle Ctrl+C
trap 'kill $FRONTEND_PID $BACKEND_PID; exit' INT

# Wait for both processes
wait $FRONTEND_PID $BACKEND_PID 