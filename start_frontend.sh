#!/bin/bash

# ResumeForge Frontend Startup Script

set -e  # Exit on error

echo "🚀 Starting ResumeForge Frontend..."
echo ""

# Color codes
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m'

# Check if Node.js is installed
if ! command -v node &> /dev/null; then
    echo -e "${RED}❌ Node.js is not installed${NC}"
    echo "Please install Node.js 16+ and npm"
    exit 1
fi

echo -e "${GREEN}✓ Node.js found: $(node --version)${NC}"

# Check if npm is installed
if ! command -v npm &> /dev/null; then
    echo -e "${RED}❌ npm is not installed${NC}"
    echo "Please install npm"
    exit 1
fi

echo -e "${GREEN}✓ npm found: v$(npm --version)${NC}"

# Check if package.json exists
if [ ! -f "package.json" ]; then
    echo -e "${RED}❌ package.json not found${NC}"
    echo "Make sure you're in the correct directory"
    exit 1
fi

# Install dependencies if node_modules doesn't exist
if [ ! -d "node_modules" ]; then
    echo -e "${YELLOW}⚠️  node_modules not found${NC}"
    echo -e "${BLUE}Installing dependencies (this may take a few minutes)...${NC}"
    npm install
    echo -e "${GREEN}✓ Dependencies installed${NC}"
else
    echo -e "${GREEN}✓ Dependencies found${NC}"
fi

# Check if backend is running
echo -e "${BLUE}Checking backend connection...${NC}"
if curl -s http://localhost:5000/api/health > /dev/null 2>&1; then
    echo -e "${GREEN}✓ Backend is running at http://localhost:5000${NC}"
else
    echo -e "${YELLOW}⚠️  Backend not detected at http://localhost:5000${NC}"
    echo "Make sure to start the backend first:"
    echo "  ./start_backend.sh"
    echo ""
    echo "Continuing anyway (frontend will start but API calls will fail)..."
fi

# Check if port 3000 is already in use
if lsof -Pi :3000 -sTCP:LISTEN -t >/dev/null 2>&1; then
    echo -e "${RED}❌ Port 3000 is already in use${NC}"
    echo "To kill the existing process:"
    echo "  lsof -ti:3000 | xargs kill -9"
    exit 1
fi

# Set environment variables
export REACT_APP_API_URL=http://localhost:5000

echo ""
echo -e "${GREEN}═══════════════════════════════════════${NC}"
echo -e "${GREEN}   Frontend server starting...${NC}"
echo -e "${GREEN}═══════════════════════════════════════${NC}"
echo ""
echo -e "  ${BLUE}Frontend:${NC}     http://localhost:3000"
echo -e "  ${BLUE}Backend API:${NC}  http://localhost:5000"
echo -e "  ${BLUE}Environment:${NC}  Development"
echo ""
echo -e "${YELLOW}Press Ctrl+C to stop${NC}"
echo -e "${BLUE}The browser will open automatically...${NC}"
echo ""

# Start the development server
npm start
