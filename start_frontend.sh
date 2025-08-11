#!/bin/bash

# Resume Optimizer Frontend Startup Script

echo "🚀 Starting Resume Optimizer Frontend..."

# Check if Node.js is installed
if ! command -v node &> /dev/null; then
    echo "❌ Node.js is not installed. Please install Node.js and npm first."
    exit 1
fi

# Check if package.json exists
if [ ! -f "package.json" ]; then
    echo "❌ package.json not found. Make sure you're in the correct directory."
    exit 1
fi

# Install dependencies if node_modules doesn't exist
if [ ! -d "node_modules" ]; then
    echo "📦 Installing dependencies..."
    npm install
fi

# Set environment variables
export REACT_APP_API_URL=http://localhost:5000

# Start the development server
echo "🌐 Starting React development server..."
echo "Frontend will be available at: http://localhost:3000"
echo "Make sure the backend is running at: http://localhost:5000"
echo ""

npm start