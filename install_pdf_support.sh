#!/bin/bash

# PDF Support Installation Script for Resume Optimizer
# This script installs wkhtmltopdf for PDF export functionality

echo "🔧 Installing PDF Export Support"
echo "================================="

# Detect OS
if [[ "$OSTYPE" == "linux-gnu"* ]]; then
    echo "Detected Linux system"
    
    # Check if running on Ubuntu/Debian
    if command -v apt-get &> /dev/null; then
        echo "Installing wkhtmltopdf via apt-get..."
        sudo apt-get update
        sudo apt-get install -y wkhtmltopdf
    
    # Check if running on CentOS/RHEL/Fedora
    elif command -v yum &> /dev/null; then
        echo "Installing wkhtmltopdf via yum..."
        sudo yum install -y wkhtmltopdf
    
    elif command -v dnf &> /dev/null; then
        echo "Installing wkhtmltopdf via dnf..."
        sudo dnf install -y wkhtmltopdf
    
    else
        echo "❌ Unsupported Linux distribution. Please install wkhtmltopdf manually."
        echo "Visit: https://wkhtmltopdf.org/downloads.html"
        exit 1
    fi

elif [[ "$OSTYPE" == "darwin"* ]]; then
    echo "Detected macOS system"
    
    if command -v brew &> /dev/null; then
        echo "Installing wkhtmltopdf via Homebrew..."
        brew install wkhtmltopdf
    else
        echo "❌ Homebrew not found. Please install Homebrew first or install wkhtmltopdf manually."
        echo "Homebrew: https://brew.sh/"
        echo "wkhtmltopdf: https://wkhtmltopdf.org/downloads.html"
        exit 1
    fi

elif [[ "$OSTYPE" == "msys" || "$OSTYPE" == "cygwin" ]]; then
    echo "Detected Windows system"
    echo "Please download and install wkhtmltopdf manually from:"
    echo "https://wkhtmltopdf.org/downloads.html"
    echo ""
    echo "After installation, add the installation directory to your PATH."
    exit 1

else
    echo "❌ Unsupported operating system: $OSTYPE"
    echo "Please install wkhtmltopdf manually from:"
    echo "https://wkhtmltopdf.org/downloads.html"
    exit 1
fi

# Test installation
echo ""
echo "Testing wkhtmltopdf installation..."
if command -v wkhtmltopdf &> /dev/null; then
    VERSION=$(wkhtmltopdf --version | head -n1)
    echo "✓ wkhtmltopdf installed successfully: $VERSION"
    
    # Install Python package
    echo ""
    echo "Installing Python pdfkit package..."
    pip install pdfkit
    
    if [ $? -eq 0 ]; then
        echo "✓ pdfkit package installed successfully"
        echo ""
        echo "🎉 PDF export support is now ready!"
        echo "You can now export resumes as PDF files from the application."
    else
        echo "❌ Failed to install pdfkit package. Please run: pip install pdfkit"
        exit 1
    fi
else
    echo "❌ wkhtmltopdf installation failed. Please install manually."
    echo "Visit: https://wkhtmltopdf.org/downloads.html"
    exit 1
fi