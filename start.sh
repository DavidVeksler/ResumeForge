#!/bin/bash

# ResumeForge Quick Start Script
# Starts both backend and frontend in a single terminal

set -e  # Exit on error

echo "🚀 ResumeForge Quick Start"
echo "=========================="
echo ""

# Color codes for better output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Function to cleanup background processes on exit
cleanup() {
    echo ""
    echo -e "${YELLOW}Shutting down ResumeForge...${NC}"
    if [ ! -z "$BACKEND_PID" ]; then
        echo "Stopping backend (PID: $BACKEND_PID)..."
        kill $BACKEND_PID 2>/dev/null || true
    fi
    if [ ! -z "$FRONTEND_PID" ]; then
        echo "Stopping frontend (PID: $FRONTEND_PID)..."
        kill $FRONTEND_PID 2>/dev/null || true
    fi
    echo "Goodbye!"
    exit 0
}

# Register cleanup function for Ctrl+C
trap cleanup SIGINT SIGTERM

# Check prerequisites
echo -e "${BLUE}Checking prerequisites...${NC}"

if ! command -v python3 &> /dev/null; then
    echo -e "${RED}❌ Python 3 not found. Please install Python 3.8+${NC}"
    exit 1
fi
echo -e "${GREEN}✓ Python 3 found: $(python3 --version)${NC}"

if ! command -v node &> /dev/null; then
    echo -e "${RED}❌ Node.js not found. Please install Node.js 16+${NC}"
    exit 1
fi
echo -e "${GREEN}✓ Node.js found: $(node --version)${NC}"

# Check if .env exists
if [ ! -f ".env" ]; then
    echo -e "${YELLOW}⚠️  .env file not found. Creating from template...${NC}"
    if [ -f ".env.example" ]; then
        cp .env.example .env
        echo -e "${YELLOW}⚠️  Please edit .env and add your OPENAI_API_KEY${NC}"
    else
        echo -e "${RED}❌ .env.example not found${NC}"
        exit 1
    fi
fi

# Install dependencies if needed
if [ ! -d "node_modules" ]; then
    echo -e "${BLUE}📦 Installing frontend dependencies...${NC}"
    npm install
fi

# Check Python dependencies
if ! python3 -c "import flask, flask_cors, dotenv, openai" 2>/dev/null; then
    echo -e "${YELLOW}⚠️  Python dependencies missing. Installing...${NC}"
    if command -v pip3 &> /dev/null; then
        pip3 install -r requirements.txt --user
    else
        echo -e "${RED}❌ pip3 not found. Please run: ./install_dependencies.sh${NC}"
        exit 1
    fi
fi

echo ""
echo -e "${GREEN}All prerequisites met!${NC}"
echo ""

# Start backend in background
echo -e "${BLUE}🔧 Starting backend server...${NC}"
python3 run_app.py > /tmp/resumeforge-backend.log 2>&1 &
BACKEND_PID=$!

# Wait for backend to start
echo "Waiting for backend to start..."
for i in {1..10}; do
    if curl -s http://localhost:5000/api/health > /dev/null 2>&1; then
        echo -e "${GREEN}✓ Backend started successfully (PID: $BACKEND_PID)${NC}"
        break
    fi
    if [ $i -eq 10 ]; then
        echo -e "${RED}❌ Backend failed to start. Check logs: tail /tmp/resumeforge-backend.log${NC}"
        cleanup
        exit 1
    fi
    sleep 1
done

# Start frontend in background
echo -e "${BLUE}⚛️  Starting frontend server...${NC}"
export BROWSER=none  # Prevent auto-opening browser
npm start > /tmp/resumeforge-frontend.log 2>&1 &
FRONTEND_PID=$!

# Wait for frontend to start
echo "Waiting for frontend to start..."
for i in {1..20}; do
    if curl -s http://localhost:3000 > /dev/null 2>&1; then
        echo -e "${GREEN}✓ Frontend started successfully (PID: $FRONTEND_PID)${NC}"
        break
    fi
    if [ $i -eq 20 ]; then
        echo -e "${RED}❌ Frontend failed to start. Check logs: tail /tmp/resumeforge-frontend.log${NC}"
        cleanup
        exit 1
    fi
    sleep 1
done

echo ""
echo -e "${GREEN}═══════════════════════════════════════${NC}"
echo -e "${GREEN}   ResumeForge is now running! 🎉${NC}"
echo -e "${GREEN}═══════════════════════════════════════${NC}"
echo ""
echo -e "  ${BLUE}Frontend:${NC}  http://localhost:3000"
echo -e "  ${BLUE}Backend:${NC}   http://localhost:5000"
echo -e "  ${BLUE}API Docs:${NC}  http://localhost:5000/api/health"
echo ""
echo -e "${YELLOW}Press Ctrl+C to stop both servers${NC}"
echo ""
echo -e "${BLUE}Logs:${NC}"
echo -e "  Backend:  tail -f /tmp/resumeforge-backend.log"
echo -e "  Frontend: tail -f /tmp/resumeforge-frontend.log"
echo ""

# Wait for user interrupt
wait
