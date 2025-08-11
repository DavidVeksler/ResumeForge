# Ubuntu Server Deployment Guide

## 🚀 Quick Deployment

This application is **ready for Ubuntu server deployment** with the provided automated deployment script.

### Prerequisites
- Ubuntu 20.04+ server
- SSH access with sudo privileges
- Domain name (optional but recommended)

### One-Command Deployment
```bash
# Clone the repository
git clone https://github.com/DavidVeksler/ResumeForge /var/www/resumeforge.davidveksler.com/ResumeForge
cd /var/www/resumeforge.davidveksler.com/ResumeForge

# Run the deployment script (as johngalt user)
./deploy.sh
```

## 🔧 WordOps Deployment

### Current Configuration
- **Server Management**: WordOps-managed Ubuntu server
- **Application Directory**: `/var/www/resumeforge.davidveksler.com/ResumeForge`
- **Application User**: `johngalt` (not ubuntu)
- **Domain**: `resumeforge.davidveksler.com` 
- **Nginx Config**: `/etc/nginx/sites-available/resumeforge.davidveksler.com`
- **Service Files**: systemd services for backend API

### WordOps Commands
```bash
# Check site status
wo site info resumeforge.davidveksler.com

# Enable SSL
wo site update resumeforge.davidveksler.com --letsencrypt

# View site logs
wo log show resumeforge.davidveksler.com
```

## 🔧 What Gets Deployed

### System Services
- **Backend API**: Python Flask app running as systemd service on port 5000
- **Frontend**: Static React build served by Nginx on port 80
- **Reverse Proxy**: Nginx handles routing and static file serving
- **SSL Ready**: Configuration included for easy HTTPS setup

### Service Files Created
- `resumeforge-backend.service` - Backend API service
- `resumeforge-frontend.service` - Frontend service placeholder  
- `nginx.conf` - Nginx configuration with security headers
- `deploy.sh` - Automated deployment script

## 📋 Post-Deployment Configuration

### 1. Environment Variables
Edit `/var/www/resumeforge.davidveksler.com/ResumeForge/.env`:
```bash
# Required for AI features
OPENAI_API_KEY=your_openai_api_key_here

# Production settings  
FLASK_ENV=production
FLASK_DEBUG=False
REACT_APP_API_URL=https://resumeforge.davidveksler.com
```

### 2. Domain Configuration (WordOps)
The nginx configuration is managed by WordOps at:
- `/etc/nginx/sites-available/resumeforge.davidveksler.com`
- `/etc/nginx/sites-enabled/resumeforge.davidveksler.com`

Domain is already configured as:
```nginx
server_name resumeforge.davidveksler.com www.resumeforge.davidveksler.com;
```

### 3. SSL Certificate (WordOps)
SSL certificates are managed by WordOps. To enable SSL:
```bash
# Enable SSL for the site
wo site update resumeforge.davidveksler.com --letsencrypt

# Or enable SSL with other WordOps options
wo site update resumeforge.davidveksler.com --letsencrypt=subdomain
```

## 🔍 Service Management

### Backend Service
```bash
# Check status
sudo systemctl status resumeforge-backend

# View logs
sudo journalctl -u resumeforge-backend -f

# Restart service
sudo systemctl restart resumeforge-backend
```

### Nginx
```bash
# Check configuration
sudo nginx -t

# Reload configuration
sudo systemctl reload nginx

# View access logs
sudo tail -f /var/log/nginx/access.log
```

## 🛠 Troubleshooting

### Backend Not Starting
1. Check Python dependencies: `source venv/bin/activate && pip list`
2. Verify environment file: `cat .env`
3. Check service logs: `sudo journalctl -u resumeforge-backend -f`

### Frontend Not Loading
1. Verify build directory exists: `ls -la build/`
2. Check Nginx configuration: `sudo nginx -t`
3. Verify domain DNS settings

### API Requests Failing
1. Check firewall: `sudo ufw status`
2. Verify backend is running: `curl http://localhost:5000/api/health`
3. Check CORS configuration in `app.py`

## 📊 Monitoring

### Health Checks
- Backend API: `https://resumeforge.davidveksler.com/api/health`
- Frontend: `https://resumeforge.davidveksler.com`
- Service status: `systemctl status resumeforge-backend`

### Log Locations
- Backend logs: `sudo journalctl -u resumeforge-backend`
- Nginx access: `/var/log/nginx/access.log`
- Nginx errors: `/var/log/nginx/error.log`

## 🔒 Security Features

### Implemented
- ✅ Firewall configuration (UFW)
- ✅ Nginx security headers
- ✅ File access restrictions
- ✅ Process isolation (systemd user)
- ✅ CORS configuration

### Recommended Additions
- [ ] SSL/TLS certificate (Let's Encrypt)
- [ ] Rate limiting (Nginx)
- [ ] Log monitoring (fail2ban)
- [ ] Backup automation
- [ ] Update automation

## 📈 Performance Optimization

### Production Settings
- Static file caching (1 year for assets)
- Gzip compression enabled
- Process management via systemd
- Reverse proxy caching ready

### Scaling Considerations
- Add load balancer for multiple instances
- Database for session management
- Redis for caching
- CDN for static assets

## 🔄 Updates & Maintenance

### Application Updates
```bash
cd /var/www/resumeforge.davidveksler.com/ResumeForge
git pull origin main
npm run build
sudo systemctl restart resumeforge-backend
```

### System Updates
```bash
sudo apt update && sudo apt upgrade -y
sudo systemctl restart resumeforge-backend nginx
```

## ✅ Deployment Checklist

- [ ] Server provisioned with Ubuntu 20.04+
- [ ] SSH access configured
- [ ] Domain name pointed to server IP (managed by WordOps)
- [ ] Repository cloned to `/var/www/resumeforge.davidveksler.com/ResumeForge`
- [ ] `./deploy.sh` executed successfully as johngalt user
- [ ] `.env` file configured with API keys
- [ ] WordOps nginx configuration updated for API proxy
- [ ] SSL certificate installed via WordOps (recommended)
- [ ] Services running: `resumeforge-backend`, `nginx`
- [ ] Firewall configured and enabled
- [ ] Health checks passing

---

## 🎯 Production Ready

Your ResumeForge application is now deployed as a production service with:
- **High Availability**: Systemd service management with auto-restart
- **Security**: Firewall, security headers, and file restrictions
- **Performance**: Nginx reverse proxy with static file caching
- **Monitoring**: Centralized logging and health checks
- **Scalability**: Ready for SSL, load balancing, and horizontal scaling

The application will automatically start on server boot and recover from failures.