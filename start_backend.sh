#!/bin/bash

# ResumeForge Backend Startup Script

set -e  # Exit on error

echo "🚀 Starting ResumeForge Backend..."
echo ""

# Color codes
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m'

# Check if Python is installed
if ! command -v python3 &> /dev/null; then
    echo -e "${RED}❌ Python 3 is not installed${NC}"
    echo "Please install Python 3.8+ and try again"
    exit 1
fi

echo -e "${GREEN}✓ Python found: $(python3 --version)${NC}"

# Check if requirements.txt exists
if [ ! -f "requirements.txt" ]; then
    echo -e "${RED}❌ requirements.txt not found${NC}"
    echo "Make sure you're in the correct directory"
    exit 1
fi

# Check if .env exists
if [ ! -f ".env" ]; then
    echo -e "${YELLOW}⚠️  .env file not found${NC}"
    if [ -f ".env.example" ]; then
        echo "Creating .env from template..."
        cp .env.example .env
        echo -e "${YELLOW}⚠️  Please edit .env and add your OPENAI_API_KEY${NC}"
        echo ""
    fi
else
    echo -e "${GREEN}✓ .env configuration found${NC}"
fi

# Check if pip is available
if command -v pip3 &> /dev/null; then
    echo -e "${GREEN}✓ pip3 found${NC}"

    # Check if dependencies are installed
    echo -e "${BLUE}Checking Python dependencies...${NC}"
    if ! python3 -c "import flask, flask_cors, dotenv, openai" 2>/dev/null; then
        echo -e "${YELLOW}Installing Python dependencies...${NC}"
        pip3 install -r requirements.txt --user
        echo -e "${GREEN}✓ Dependencies installed${NC}"
    else
        echo -e "${GREEN}✓ All dependencies installed${NC}"
    fi
else
    echo -e "${YELLOW}⚠️  pip3 not found${NC}"
    echo "Will attempt to start server (may fail if dependencies missing)"
fi

# Check if port 5000 is already in use
if lsof -Pi :5000 -sTCP:LISTEN -t >/dev/null 2>&1; then
    echo -e "${RED}❌ Port 5000 is already in use${NC}"
    echo "To kill the existing process:"
    echo "  lsof -ti:5000 | xargs kill -9"
    exit 1
fi

# Set environment variables
export FLASK_ENV=development
export FLASK_DEBUG=True

echo ""
echo -e "${GREEN}═══════════════════════════════════════${NC}"
echo -e "${GREEN}   Backend server starting...${NC}"
echo -e "${GREEN}═══════════════════════════════════════${NC}"
echo ""
echo -e "  ${BLUE}API URL:${NC}      http://localhost:5000"
echo -e "  ${BLUE}Health:${NC}       http://localhost:5000/api/health"
echo -e "  ${BLUE}Environment:${NC}  Development"
echo ""
echo -e "${YELLOW}Press Ctrl+C to stop${NC}"
echo ""

# Start the consolidated backend server
if python3 -c "import flask, flask_cors, dotenv" 2>/dev/null; then
    echo -e "${GREEN}Starting ResumeForge Backend v2.0 (consolidated architecture)...${NC}"
    echo ""
    python3 -m backend.main
else
    echo -e "${RED}❌ Flask dependencies not available${NC}"
    echo "Please install dependencies: pip3 install -r requirements.txt --user"
    exit 1
fi
