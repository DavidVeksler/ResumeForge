#!/bin/bash

# Development Setup Script for Resume Optimizer

echo "🔧 Resume Optimizer Development Setup"
echo "======================================"

# Check Python
echo "Checking Python installation..."
if command -v python3 &> /dev/null; then
    PYTHON_VERSION=$(python3 --version)
    echo "✓ Python found: $PYTHON_VERSION"
else
    echo "❌ Python 3 not found. Please install Python 3.8+"
    exit 1
fi

# Check Node.js
echo "Checking Node.js installation..."
if command -v node &> /dev/null; then
    NODE_VERSION=$(node --version)
    echo "✓ Node.js found: $NODE_VERSION"
else
    echo "❌ Node.js not found. Please install Node.js 16+"
    exit 1
fi

# Check npm
if command -v npm &> /dev/null; then
    NPM_VERSION=$(npm --version)
    echo "✓ npm found: $NPM_VERSION"
else
    echo "❌ npm not found. Please install npm"
    exit 1
fi

# Test core functionality
echo ""
echo "Testing core functionality..."
python3 test_mock_api.py

if [ $? -eq 0 ]; then
    echo ""
    echo "🎉 Setup validation successful!"
    echo ""
    echo "To start the application:"
    echo "1. Backend:  ./start_backend.sh"
    echo "2. Frontend: ./start_frontend.sh"
    echo "3. Open:     http://localhost:3000"
    echo ""
    echo "Make sure to run both backend and frontend in separate terminals."
else
    echo ""
    echo "❌ Setup validation failed. Please check the errors above."
    exit 1
fi