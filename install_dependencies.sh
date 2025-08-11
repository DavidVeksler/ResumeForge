#!/bin/bash

# Resume Optimizer Dependency Installation Script

echo "🔧 Installing Resume Optimizer Dependencies"
echo "==========================================="

# Function to check if command exists
command_exists() {
    command -v "$1" >/dev/null 2>&1
}

# Check if we're in WSL or Ubuntu
if grep -q microsoft /proc/version; then
    echo "🐧 Detected WSL environment"
    WSL_ENV=true
else
    echo "🐧 Detected Linux environment"
    WSL_ENV=false
fi

# Check Python
if ! command_exists python3; then
    echo "❌ Python 3 not found. Please install Python 3.8+"
    exit 1
fi

echo "✓ Python found: $(python3 --version)"

# Install pip if not available
if ! command_exists pip3; then
    echo "📦 Installing pip..."
    if [ "$WSL_ENV" = true ]; then
        echo "Please run the following command in your terminal:"
        echo "  sudo apt update && sudo apt install python3-pip python3-venv -y"
        echo "Then re-run this script."
        exit 1
    else
        # Try to install pip
        python3 -m ensurepip --default-pip 2>/dev/null || {
            echo "❌ Could not install pip. Please install python3-pip manually."
            exit 1
        }
    fi
fi

echo "✓ pip found: $(pip3 --version)"

# Install Python dependencies
echo "📦 Installing Python dependencies..."
pip3 install --user Flask==3.0.0 Flask-CORS==4.0.0 Werkzeug==3.0.1 python-dotenv==1.0.0 pdfkit==1.0.0 openai==1.50.0

if [ $? -eq 0 ]; then
    echo "✅ Python dependencies installed successfully"
else
    echo "❌ Failed to install Python dependencies"
    exit 1
fi

# Install Node.js dependencies
if command_exists npm; then
    echo "📦 Installing Node.js dependencies..."
    npm install
    if [ $? -eq 0 ]; then
        echo "✅ Node.js dependencies installed successfully"
    else
        echo "❌ Failed to install Node.js dependencies"
        exit 1
    fi
else
    echo "⚠️  npm not found. Frontend dependencies not installed."
    echo "   Please install Node.js and npm, then run: npm install"
fi

echo ""
echo "🎉 Dependencies installed successfully!"
echo ""
echo "Next steps:"
echo "1. Run: ./start_backend.sh"
echo "2. In another terminal, run: ./start_frontend.sh"
echo "3. Open: http://localhost:3000"