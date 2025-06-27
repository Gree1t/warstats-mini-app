#!/bin/bash

# War Thunder Stats Mini App Deployment Script
# Автоматическое развертывание на сервере

set -e

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Configuration
DOMAIN=${1:-"your-domain.com"}
EMAIL=${2:-"admin@your-domain.com"}
PROJECT_DIR="/var/www/wt-stats-mini-app"
SSL_DIR="/etc/letsencrypt/live/$DOMAIN"

echo -e "${BLUE}🚀 War Thunder Stats Mini App Deployment${NC}"
echo -e "${BLUE}==========================================${NC}"

# Function to print colored output
print_status() {
    echo -e "${GREEN}✅ $1${NC}"
}

print_warning() {
    echo -e "${YELLOW}⚠️  $1${NC}"
}

print_error() {
    echo -e "${RED}❌ $1${NC}"
}

print_info() {
    echo -e "${BLUE}ℹ️  $1${NC}"
}

# Check if running as root
if [[ $EUID -ne 0 ]]; then
   print_error "This script must be run as root"
   exit 1
fi

# Update system
print_info "Updating system packages..."
apt update && apt upgrade -y
print_status "System updated"

# Install required packages
print_info "Installing required packages..."
apt install -y nginx certbot python3-certbot-nginx docker.io docker-compose curl wget git
print_status "Packages installed"

# Create project directory
print_info "Creating project directory..."
mkdir -p $PROJECT_DIR
cd $PROJECT_DIR
print_status "Project directory created: $PROJECT_DIR"

# Clone or copy project files
if [ -d ".git" ]; then
    print_info "Updating existing repository..."
    git pull origin main
else
    print_info "Initializing git repository..."
    git init
    git remote add origin https://github.com/your-username/wt-stats-mini-app.git
    git pull origin main
fi

# Create SSL directory
mkdir -p /etc/nginx/ssl

# Generate self-signed certificate for initial setup
print_info "Generating self-signed SSL certificate..."
openssl req -x509 -nodes -days 365 -newkey rsa:2048 \
    -keyout /etc/nginx/ssl/key.pem \
    -out /etc/nginx/ssl/cert.pem \
    -subj "/C=US/ST=State/L=City/O=Organization/CN=$DOMAIN"
print_status "Self-signed certificate generated"

# Update nginx configuration
print_info "Configuring nginx..."
sed -i "s/your-domain.com/$DOMAIN/g" nginx.conf
cp nginx.conf /etc/nginx/nginx.conf
print_status "Nginx configured"

# Test nginx configuration
print_info "Testing nginx configuration..."
nginx -t
print_status "Nginx configuration is valid"

# Start nginx
print_info "Starting nginx..."
systemctl enable nginx
systemctl start nginx
print_status "Nginx started"

# Deploy with Docker Compose
print_info "Deploying with Docker Compose..."
docker-compose down || true
docker-compose up -d
print_status "Docker containers deployed"

# Wait for services to start
print_info "Waiting for services to start..."
sleep 10

# Check if services are running
print_info "Checking service status..."
if docker-compose ps | grep -q "Up"; then
    print_status "All services are running"
else
    print_error "Some services failed to start"
    docker-compose logs
    exit 1
fi

# Setup SSL certificate with Let's Encrypt
print_info "Setting up SSL certificate with Let's Encrypt..."
if certbot --nginx -d $DOMAIN --non-interactive --agree-tos --email $EMAIL; then
    print_status "SSL certificate installed successfully"
    
    # Update nginx configuration to use Let's Encrypt certificates
    sed -i "s|/etc/nginx/ssl/cert.pem|$SSL_DIR/fullchain.pem|g" /etc/nginx/nginx.conf
    sed -i "s|/etc/nginx/ssl/key.pem|$SSL_DIR/privkey.pem|g" /etc/nginx/nginx.conf
    
    # Reload nginx
    nginx -s reload
    print_status "Nginx reloaded with Let's Encrypt certificates"
else
    print_warning "Failed to install Let's Encrypt certificate, using self-signed"
fi

# Setup firewall
print_info "Configuring firewall..."
ufw allow 22/tcp
ufw allow 80/tcp
ufw allow 443/tcp
ufw --force enable
print_status "Firewall configured"

# Setup automatic SSL renewal
print_info "Setting up automatic SSL renewal..."
(crontab -l 2>/dev/null; echo "0 12 * * * /usr/bin/certbot renew --quiet") | crontab -
print_status "SSL renewal cron job added"

# Setup log rotation
print_info "Setting up log rotation..."
cat > /etc/logrotate.d/wt-stats-mini-app << EOF
$PROJECT_DIR/logs/*.log {
    daily
    missingok
    rotate 52
    compress
    delaycompress
    notifempty
    create 644 www-data www-data
    postrotate
        systemctl reload nginx
    endscript
}
EOF
print_status "Log rotation configured"

# Create monitoring script
print_info "Creating monitoring script..."
cat > /usr/local/bin/monitor-wt-stats.sh << 'EOF'
#!/bin/bash

# Check if services are running
if ! docker-compose -f /var/www/wt-stats-mini-app/docker-compose.yml ps | grep -q "Up"; then
    echo "$(date): Services are down, restarting..." >> /var/log/wt-stats-monitor.log
    docker-compose -f /var/www/wt-stats-mini-app/docker-compose.yml restart
fi

# Check disk space
DISK_USAGE=$(df / | awk 'NR==2 {print $5}' | sed 's/%//')
if [ $DISK_USAGE -gt 80 ]; then
    echo "$(date): Disk usage is high: ${DISK_USAGE}%" >> /var/log/wt-stats-monitor.log
fi

# Check memory usage
MEM_USAGE=$(free | awk 'NR==2{printf "%.0f", $3*100/$2}')
if [ $MEM_USAGE -gt 80 ]; then
    echo "$(date): Memory usage is high: ${MEM_USAGE}%" >> /var/log/wt-stats-monitor.log
fi
EOF

chmod +x /usr/local/bin/monitor-wt-stats.sh

# Add monitoring to crontab
(crontab -l 2>/dev/null; echo "*/5 * * * * /usr/local/bin/monitor-wt-stats.sh") | crontab -
print_status "Monitoring script created"

# Create backup script
print_info "Creating backup script..."
cat > /usr/local/bin/backup-wt-stats.sh << 'EOF'
#!/bin/bash

BACKUP_DIR="/var/backups/wt-stats-mini-app"
DATE=$(date +%Y%m%d_%H%M%S)

mkdir -p $BACKUP_DIR

# Backup project files
tar -czf $BACKUP_DIR/wt-stats-mini-app_$DATE.tar.gz -C /var/www wt-stats-mini-app

# Backup nginx configuration
cp /etc/nginx/nginx.conf $BACKUP_DIR/nginx.conf_$DATE

# Backup SSL certificates
if [ -d "/etc/letsencrypt/live" ]; then
    tar -czf $BACKUP_DIR/ssl_$DATE.tar.gz -C /etc letsencrypt
fi

# Keep only last 7 backups
find $BACKUP_DIR -name "*.tar.gz" -mtime +7 -delete
find $BACKUP_DIR -name "nginx.conf_*" -mtime +7 -delete

echo "Backup completed: $DATE" >> /var/log/wt-stats-backup.log
EOF

chmod +x /usr/local/bin/backup-wt-stats.sh

# Add backup to crontab (daily at 2 AM)
(crontab -l 2>/dev/null; echo "0 2 * * * /usr/local/bin/backup-wt-stats.sh") | crontab -
print_status "Backup script created"

# Final status check
print_info "Performing final status check..."

# Check nginx
if systemctl is-active --quiet nginx; then
    print_status "Nginx is running"
else
    print_error "Nginx is not running"
fi

# Check Docker containers
if docker-compose ps | grep -q "Up"; then
    print_status "Docker containers are running"
else
    print_error "Docker containers are not running"
fi

# Check SSL certificate
if [ -f "$SSL_DIR/fullchain.pem" ]; then
    print_status "SSL certificate is installed"
else
    print_warning "Using self-signed certificate"
fi

# Display final information
echo -e "${BLUE}🎉 Deployment completed successfully!${NC}"
echo -e "${BLUE}=====================================${NC}"
echo -e "${GREEN}🌐 Mini App URL: https://$DOMAIN/mini_app/${NC}"
echo -e "${GREEN}🔧 Health Check: https://$DOMAIN/health${NC}"
echo -e "${GREEN}📊 API Status: https://$DOMAIN/api/health${NC}"
echo -e "${YELLOW}📝 Logs: /var/log/nginx/access.log${NC}"
echo -e "${YELLOW}🔍 Error Logs: /var/log/nginx/error.log${NC}"
echo -e "${BLUE}📦 Project Directory: $PROJECT_DIR${NC}"
echo -e "${BLUE}🐳 Docker Compose: docker-compose -f $PROJECT_DIR/docker-compose.yml${NC}"

# Display useful commands
echo -e "${BLUE}📋 Useful Commands:${NC}"
echo -e "${YELLOW}  View logs: docker-compose logs -f${NC}"
echo -e "${YELLOW}  Restart services: docker-compose restart${NC}"
echo -e "${YELLOW}  Update app: git pull && docker-compose up -d --build${NC}"
echo -e "${YELLOW}  Monitor: tail -f /var/log/wt-stats-monitor.log${NC}"
echo -e "${YELLOW}  Backup: /usr/local/bin/backup-wt-stats.sh${NC}"

print_status "Deployment script completed!" 