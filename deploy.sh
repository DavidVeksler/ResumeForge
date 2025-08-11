#!/bin/bash

# ResumeForge Ubuntu Server Deployment Script
set -e

echo "🚀 ResumeForge Ubuntu Server Deployment"
echo "======================================"

# Configuration
APP_NAME="resumeforge"
APP_USER="ubuntu"
APP_DIR="/home/$APP_USER/ResumeForge"
PYTHON_VERSION="python3"

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

print_status() {
    echo -e "${GREEN}✓${NC} $1"
}

print_warning() {
    echo -e "${YELLOW}⚠${NC} $1"
}

print_error() {
    echo -e "${RED}❌${NC} $1"
}

# Check if running as ubuntu user
if [ "$USER" != "$APP_USER" ]; then
    print_error "This script should be run as the ubuntu user"
    exit 1
fi

# Update system packages
print_status "Updating system packages..."
sudo apt update && sudo apt upgrade -y

# Install required system packages
print_status "Installing system dependencies..."
sudo apt install -y \
    python3 \
    python3-pip \
    python3-venv \
    nodejs \
    npm \
    nginx \
    wkhtmltopdf \
    curl \
    git \
    ufw

# Create Python virtual environment
print_status "Setting up Python virtual environment..."
if [ ! -d "$APP_DIR/venv" ]; then
    cd $APP_DIR
    python3 -m venv venv
    print_status "Virtual environment created"
else
    print_warning "Virtual environment already exists"
fi

# Install Python dependencies
print_status "Installing Python dependencies..."
cd $APP_DIR
source venv/bin/activate
pip install --upgrade pip
pip install -r requirements.txt

# Install Node.js dependencies and build React app
print_status "Installing Node.js dependencies..."
npm install

print_status "Building React application..."
npm run build

# Set up environment file
print_status "Setting up environment configuration..."
if [ ! -f "$APP_DIR/.env" ]; then
    cp $APP_DIR/.env.example $APP_DIR/.env
    print_warning "Please edit $APP_DIR/.env with your configuration"
else
    print_status "Environment file already exists"
fi

# Set correct permissions
print_status "Setting file permissions..."
sudo chown -R $APP_USER:$APP_USER $APP_DIR
chmod +x $APP_DIR/*.sh

# Install systemd service files
print_status "Installing systemd services..."
sudo cp $APP_DIR/resumeforge-backend.service /etc/systemd/system/
sudo systemctl daemon-reload

# Configure Nginx
print_status "Configuring Nginx..."
sudo cp $APP_DIR/nginx.conf /etc/nginx/sites-available/resumeforge
sudo ln -sf /etc/nginx/sites-available/resumeforge /etc/nginx/sites-enabled/
sudo rm -f /etc/nginx/sites-enabled/default

# Test Nginx configuration
print_status "Testing Nginx configuration..."
sudo nginx -t

# Configure firewall
print_status "Configuring firewall..."
sudo ufw allow 22/tcp
sudo ufw allow 80/tcp
sudo ufw allow 443/tcp
sudo ufw --force enable

# Start and enable services
print_status "Starting services..."
sudo systemctl enable resumeforge-backend
sudo systemctl start resumeforge-backend
sudo systemctl enable nginx
sudo systemctl restart nginx

# Check service status
print_status "Checking service status..."
if sudo systemctl is-active --quiet resumeforge-backend; then
    print_status "Backend service is running"
else
    print_error "Backend service failed to start"
    sudo systemctl status resumeforge-backend
fi

if sudo systemctl is-active --quiet nginx; then
    print_status "Nginx is running"
else
    print_error "Nginx failed to start"
    sudo systemctl status nginx
fi

# Run basic health check
print_status "Running health check..."
sleep 5
if curl -f http://localhost:5000/api/health > /dev/null 2>&1; then
    print_status "Backend API is responding"
else
    print_warning "Backend API health check failed"
fi

echo ""
echo "🎉 Deployment completed!"
echo ""
echo "Next steps:"
echo "1. Edit $APP_DIR/.env with your OpenAI API key and other settings"
echo "2. Update nginx.conf with your domain name"
echo "3. Restart services: sudo systemctl restart resumeforge-backend nginx"
echo "4. Set up SSL certificate (recommended): sudo apt install certbot python3-certbot-nginx"
echo ""
echo "Service management:"
echo "- View logs: sudo journalctl -u resumeforge-backend -f"
echo "- Restart backend: sudo systemctl restart resumeforge-backend"
echo "- Restart nginx: sudo systemctl restart nginx"
echo ""
echo "Your application should be accessible at: http://$(curl -s ifconfig.me)"