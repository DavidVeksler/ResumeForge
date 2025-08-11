#!/bin/bash

# Resume Optimizer Backend Startup Script

echo "🚀 Starting Resume Optimizer Backend..."

# Check if Python is installed
if ! command -v python3 &> /dev/null; then
    echo "❌ Python 3 is not installed. Please install Python 3 first."
    exit 1
fi

# Check if requirements.txt exists
if [ ! -f "requirements.txt" ]; then
    echo "❌ requirements.txt not found. Make sure you're in the correct directory."
    exit 1
fi

# Check if pip is available, continue without it if not found
if command -v pip3 &> /dev/null; then
    # Check if dependencies are installed
    echo "🔍 Checking Python dependencies..."
    python3 -c "import flask, flask_cors, dotenv" 2>/dev/null || {
        echo "📦 Installing Python dependencies..."
        pip3 install -r requirements.txt --user
    }
else
    echo "⚠️  pip3 not found. Will use simple server without Flask dependencies."
fi

# Set environment variables
export FLASK_ENV=development
export FLASK_DEBUG=True

# Try to start the Flask server, fallback to simple server
echo "🌐 Starting backend server..."
echo "Backend API will be available at: http://localhost:5000"
echo "API endpoints:"
echo "  - GET  /api/health"
echo "  - POST /api/optimize"
echo ""

# Try Flask first, fallback to simple server
if python3 -c "import flask, flask_cors, dotenv" 2>/dev/null; then
    echo "🌶️  Starting Flask server..."
    python3 run_app.py
else
    echo "⚠️  Flask dependencies not available, starting simple server..."
    echo "💡 For full functionality, run: ./install_dependencies.sh"
    echo ""
    python3 simple_server.py
fi