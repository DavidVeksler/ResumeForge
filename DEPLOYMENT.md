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
git clone <your-repo-url> /home/ubuntu/ResumeForge
cd /home/ubuntu/ResumeForge

# Run the deployment script
./deploy.sh
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
Edit `/home/ubuntu/ResumeForge/.env`:
```bash
# Required for AI features
OPENAI_API_KEY=your_openai_api_key_here

# Production settings  
FLASK_ENV=production
FLASK_DEBUG=False
REACT_APP_API_URL=https://yourdomain.com
```

### 2. Domain Configuration
Update `nginx.conf`:
```nginx
server_name your_domain.com www.your_domain.com;
```

### 3. SSL Certificate (Recommended)
```bash
# Install Certbot
sudo apt install certbot python3-certbot-nginx

# Get SSL certificate
sudo certbot --nginx -d your_domain.com -d www.your_domain.com
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
- Backend API: `http://your-domain.com/api/health`
- Frontend: `http://your-domain.com`
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
cd /home/ubuntu/ResumeForge
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
- [ ] Domain name pointed to server IP
- [ ] Repository cloned to `/home/ubuntu/ResumeForge`
- [ ] `./deploy.sh` executed successfully
- [ ] `.env` file configured with API keys
- [ ] Domain name updated in `nginx.conf`
- [ ] SSL certificate installed (recommended)
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