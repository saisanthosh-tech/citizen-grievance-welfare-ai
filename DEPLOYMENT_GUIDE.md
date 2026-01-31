# Production Deployment Guide
## Citizen Grievance & Welfare Intelligence System

---

## Phase 1: Pre-Deployment Preparation

### 1.1 Infrastructure Requirements

#### Server Specifications
```
Minimum (Small Deployment - 1,000 users):
- CPU: 2 vCPU (2.0 GHz+)
- RAM: 4 GB
- Storage: 50 GB SSD
- Network: 10 Mbps

Recommended (Medium Deployment - 10,000 users):
- CPU: 4 vCPU
- RAM: 8 GB
- Storage: 200 GB SSD
- Network: 100 Mbps

Production (Large Deployment - 100,000+ users):
- CPU: 8+ vCPU with auto-scaling
- RAM: 16-32 GB with caching layer
- Storage: 500+ GB SSD with distributed backups
- Network: 1 Gbps with CDN
- Load Balancer: Yes
- Database Replication: Yes
```

#### Operating System
```
Recommended: Ubuntu 22.04 LTS (Long-Term Support)
Alternatives:
- CentOS 8 Stream
- Debian 12
- Red Hat Enterprise Linux 8

NOT Recommended for production:
- Windows
- Development builds
```

### 1.2 Domain & SSL Certificate

#### Domain Setup
```
1. Register domain: grievance.gov.in
2. Configure DNS:
   A record: 192.0.2.x (your server IP)
   CNAME: www → grievance.gov.in (optional)
   MX records: For email notifications
   TXT record: SPF, DKIM, DMARC (for email)

3. Validate SSL:
   Get Let's Encrypt certificate (free, auto-renewing)
   OR use institutional certificate
```

#### SSL Certificate Installation
```bash
# Using Certbot (Let's Encrypt)
sudo apt-get install certbot python3-certbot-nginx -y
sudo certbot certonly --webroot -w /var/www/html -d grievance.gov.in -d www.grievance.gov.in

# Or using institutional cert
sudo cp /path/to/certificate.crt /etc/ssl/certs/
sudo cp /path/to/private.key /etc/ssl/private/
sudo chmod 600 /etc/ssl/private/private.key

# Auto-renewal
sudo systemctl enable certbot.timer
sudo systemctl start certbot.timer
```

---

## Phase 2: Server Setup

### 2.1 System Initialization

```bash
# Update system packages
sudo apt-get update
sudo apt-get upgrade -y

# Install required packages
sudo apt-get install -y \
    python3.11 \
    python3-pip \
    python3-venv \
    postgresql \
    postgresql-contrib \
    nginx \
    redis-server \
    git \
    curl \
    wget \
    nano \
    htop \
    fail2ban

# Create application directory
sudo mkdir -p /opt/grievance-system
sudo mkdir -p /var/log/grievance
sudo mkdir -p /opt/grievance-system/backups

# Set proper permissions
sudo chown -R grievance:grievance /opt/grievance-system
sudo chmod 750 /opt/grievance-system
```

### 2.2 Create Application User

```bash
# Create non-root user for application
sudo useradd -m -s /bin/bash -d /home/grievance grievance
sudo usermod -aG sudo grievance

# Set resource limits
sudo echo "grievance soft nofile 65536" >> /etc/security/limits.conf
sudo echo "grievance hard nofile 65536" >> /etc/security/limits.conf
```

### 2.3 Python Environment Setup

```bash
# Switch to grievance user
su - grievance

# Create virtual environment
python3.11 -m venv /opt/grievance-system/venv

# Activate virtual environment
source /opt/grievance-system/venv/bin/activate

# Upgrade pip and install dependencies
pip install --upgrade pip setuptools wheel
pip install -r requirements.txt
pip install gunicorn uvicorn[standard]
```

---

## Phase 3: Database Setup

### 3.1 PostgreSQL Configuration

```bash
# Switch to postgres user
sudo -u postgres psql

# Create database and user
CREATE DATABASE grievance_system OWNER postgres;
CREATE USER grievance_app WITH ENCRYPTED PASSWORD 'GenerateSecurePassword123!';

# Configure permissions
GRANT CONNECT ON DATABASE grievance_system TO grievance_app;
\c grievance_system
CREATE SCHEMA public;
GRANT USAGE ON SCHEMA public TO grievance_app;
GRANT CREATE ON SCHEMA public TO grievance_app;

# Create tables (run migration)
# Copy schema from backend/app/models.py
```

### 3.2 Database Optimization

```sql
-- Enable extensions
CREATE EXTENSION pg_stat_statements;
CREATE EXTENSION pgcrypto;

-- Create indexes
CREATE INDEX idx_grievance_status ON grievances(status);
CREATE INDEX idx_grievance_category ON grievances(category);
CREATE INDEX idx_grievance_created_at ON grievances(created_at);
CREATE INDEX idx_grievance_tracking_token ON grievances(tracking_token);

-- Enable connection pooling (PgBouncer)
# Install: sudo apt-get install pgbouncer
# Configure: /etc/pgbouncer/pgbouncer.ini
```

### 3.3 Backup Configuration

```bash
# Create backup script
sudo tee /opt/grievance-system/backup.sh > /dev/null <<EOF
#!/bin/bash
BACKUP_DIR="/opt/grievance-system/backups"
TIMESTAMP=$(date +"%Y%m%d_%H%M%S")
BACKUP_FILE="$BACKUP_DIR/grievance_system_$TIMESTAMP.sql.gz"

# Create backup
sudo -u postgres pg_dump grievance_system | gzip > $BACKUP_FILE

# Keep only last 30 days
find $BACKUP_DIR -name "*.sql.gz" -mtime +30 -delete

# Encrypt backup
openssl enc -aes-256-cbc -in $BACKUP_FILE -out ${BACKUP_FILE}.enc -k $ENCRYPTION_KEY
rm $BACKUP_FILE
EOF

# Make executable
sudo chmod +x /opt/grievance-system/backup.sh

# Add to crontab (daily at 2 AM)
sudo crontab -e
# Add: 0 2 * * * /opt/grievance-system/backup.sh >> /var/log/grievance/backup.log 2>&1
```

---

## Phase 4: Application Deployment

### 4.1 Clone and Configure Application

```bash
# Clone repository
cd /opt/grievance-system
git clone <repository-url> app
cd app

# Create environment file
cp .env.example .env
nano .env  # Edit with production values

# Install dependencies
pip install -r backend/requirements.txt
```

### 4.2 Environment Configuration

```bash
# Edit .env with production values
nano /opt/grievance-system/.env

# Required values:
ENVIRONMENT=production
DEBUG=False
SECRET_KEY=<Generate using: openssl rand -hex 32>
ALGORITHM=HS256
DATABASE_URL=postgresql://grievance_app:password@localhost/grievance_system
ALLOWED_HOSTS=grievance.gov.in,www.grievance.gov.in
CORS_ORIGINS=https://grievance.gov.in
ENABLE_HTTPS_REDIRECT=True
LOG_LEVEL=INFO
```

### 4.3 Application Server Setup (Gunicorn)

```bash
# Create systemd service file
sudo tee /etc/systemd/system/grievance-api.service > /dev/null <<EOF
[Unit]
Description=Grievance System API
After=network.target postgresql.service

[Service]
Type=notify
User=grievance
Group=grievance
WorkingDirectory=/opt/grievance-system/app
Environment="PATH=/opt/grievance-system/venv/bin"
EnvironmentFile=/opt/grievance-system/.env
ExecStart=/opt/grievance-system/venv/bin/gunicorn \
    --workers 4 \
    --worker-class uvicorn.workers.UvicornWorker \
    --bind 127.0.0.1:8000 \
    --timeout 60 \
    --access-logfile /var/log/grievance/access.log \
    --error-logfile /var/log/grievance/error.log \
    --log-level info \
    backend.app.main:app

Restart=on-failure
RestartSec=10s

[Install]
WantedBy=multi-user.target
EOF

# Enable and start service
sudo systemctl enable grievance-api.service
sudo systemctl start grievance-api.service
sudo systemctl status grievance-api.service
```

---

## Phase 5: Web Server Configuration (Nginx)

### 5.1 Nginx Setup

```bash
# Create nginx configuration
sudo tee /etc/nginx/sites-available/grievance > /dev/null <<'EOF'
upstream grievance_api {
    server 127.0.0.1:8000;
}

# Redirect HTTP to HTTPS
server {
    listen 80;
    listen [::]:80;
    server_name grievance.gov.in www.grievance.gov.in;
    
    return 301 https://$server_name$request_uri;
}

# Main HTTPS server
server {
    listen 443 ssl http2;
    listen [::]:443 ssl http2;
    server_name grievance.gov.in www.grievance.gov.in;

    # SSL Configuration
    ssl_certificate /etc/letsencrypt/live/grievance.gov.in/fullchain.pem;
    ssl_certificate_key /etc/letsencrypt/live/grievance.gov.in/privkey.pem;
    ssl_protocols TLSv1.2 TLSv1.3;
    ssl_ciphers HIGH:!aNULL:!MD5;
    ssl_prefer_server_ciphers on;
    ssl_session_cache shared:SSL:10m;
    ssl_session_timeout 10m;

    # Security Headers
    add_header Strict-Transport-Security "max-age=31536000; includeSubDomains" always;
    add_header X-Frame-Options "DENY" always;
    add_header X-Content-Type-Options "nosniff" always;
    add_header X-XSS-Protection "1; mode=block" always;
    add_header Content-Security-Policy "default-src 'self'; script-src 'self' 'unsafe-inline'; style-src 'self' 'unsafe-inline';" always;
    add_header Referrer-Policy "strict-origin-when-cross-origin" always;

    # Logging
    access_log /var/log/nginx/grievance_access.log;
    error_log /var/log/nginx/grievance_error.log;

    # Client size limit
    client_max_body_size 10M;

    # API endpoints
    location / {
        proxy_pass http://grievance_api;
        proxy_http_version 1.1;
        proxy_set_header Upgrade $http_upgrade;
        proxy_set_header Connection "upgrade";
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
        proxy_read_timeout 60s;
        proxy_connect_timeout 10s;
    }

    # Static files (if any)
    location /static/ {
        alias /opt/grievance-system/app/static/;
        expires 30d;
    }
}
EOF

# Enable site
sudo ln -s /etc/nginx/sites-available/grievance /etc/nginx/sites-enabled/
sudo rm -f /etc/nginx/sites-enabled/default

# Test configuration
sudo nginx -t

# Restart nginx
sudo systemctl enable nginx
sudo systemctl restart nginx
```

---

## Phase 6: Security Hardening

### 6.1 Firewall Configuration (UFW)

```bash
# Enable UFW
sudo ufw enable

# Allow SSH
sudo ufw allow ssh

# Allow HTTP/HTTPS
sudo ufw allow http
sudo ufw allow https

# Database (internal only)
sudo ufw allow from 127.0.0.1 to 127.0.0.1 port 5432

# Verify rules
sudo ufw status numbered
```

### 6.2 Fail2Ban Configuration

```bash
# Create local jail configuration
sudo tee /etc/fail2ban/jail.local > /dev/null <<EOF
[DEFAULT]
ignoreip = 127.0.0.1/8
bantime = 3600
findtime = 600
maxretry = 5

[sshd]
enabled = true
port = ssh
filter = sshd
logpath = /var/log/auth.log

[nginx-http-auth]
enabled = true
port = http,https
filter = nginx-http-auth
logpath = /var/log/nginx/error.log

[nginx-limit-req]
enabled = true
port = http,https
filter = nginx-limit-req
logpath = /var/log/nginx/error.log
EOF

# Restart Fail2Ban
sudo systemctl restart fail2ban
```

### 6.3 SSH Hardening

```bash
# Edit SSH configuration
sudo nano /etc/ssh/sshd_config

# Set these values:
Port 22
PermitRootLogin no
PasswordAuthentication no
PubkeyAuthentication yes
X11Forwarding no
PrintMotd no
MaxAuthTries 3
MaxSessions 10
ClientAliveInterval 300
ClientAliveCountMax 2

# Restart SSH
sudo systemctl restart ssh
```

---

## Phase 7: Monitoring & Logging

### 7.1 Log Rotation

```bash
# Create logrotate configuration
sudo tee /etc/logrotate.d/grievance > /dev/null <<EOF
/var/log/grievance/*.log {
    daily
    rotate 30
    compress
    delaycompress
    missingok
    notifempty
    create 0640 grievance grievance
    sharedscripts
    postrotate
        systemctl reload grievance-api > /dev/null 2>&1 || true
    endscript
}
EOF
```

### 7.2 Health Monitoring

```bash
# Create monitoring script
sudo tee /opt/grievance-system/monitor.sh > /dev/null <<'EOF'
#!/bin/bash

# Check API health
API_STATUS=$(curl -s -o /dev/null -w "%{http_code}" http://127.0.0.1:8000/health)
if [ "$API_STATUS" != "200" ]; then
    echo "ALERT: API health check failed with status $API_STATUS"
    systemctl restart grievance-api
fi

# Check database connection
DB_STATUS=$(sudo -u postgres psql -d grievance_system -c "SELECT 1" 2>&1)
if [[ ! $DB_STATUS =~ "1" ]]; then
    echo "ALERT: Database connection failed"
fi

# Check disk space
DISK_USAGE=$(df /opt | awk 'NR==2 {print $5}' | cut -d% -f1)
if [ $DISK_USAGE -gt 80 ]; then
    echo "ALERT: Disk usage at ${DISK_USAGE}%"
fi

# Check memory
MEM_USAGE=$(free | awk 'NR==2{printf("%.0f", $3/$2 * 100.0)}')
if [ $MEM_USAGE -gt 85 ]; then
    echo "ALERT: Memory usage at ${MEM_USAGE}%"
fi
EOF

sudo chmod +x /opt/grievance-system/monitor.sh

# Add to crontab (every 5 minutes)
sudo crontab -e
# Add: */5 * * * * /opt/grievance-system/monitor.sh >> /var/log/grievance/monitor.log 2>&1
```

---

## Phase 8: Verification Checklist

### Pre-Launch Verification

- [ ] SSL certificate installed and valid (no warnings)
- [ ] API accessible at https://grievance.gov.in/health
- [ ] Database connection working
- [ ] Logging to `/var/log/grievance/` files
- [ ] Backups running and encrypted
- [ ] Firewall rules in place
- [ ] Fail2Ban protecting SSH
- [ ] Rate limiting working
- [ ] Admin credentials changed from default
- [ ] All environment variables set correctly
- [ ] CORS configured for correct domains only
- [ ] Security headers present in responses
- [ ] HTTPS redirect working
- [ ] Health monitoring script running
- [ ] Disk space sufficient
- [ ] Memory available
- [ ] CPU not maxed out

### Post-Launch Validation

- [ ] Submit test grievance through API
- [ ] Verify grievance saved in database
- [ ] Track grievance with token
- [ ] Admin login functional
- [ ] Admin can view and update grievances
- [ ] Statistics endpoint returns correct data
- [ ] Error handling works (test with invalid data)
- [ ] Rate limiting active (test > limit)
- [ ] Logs contain all operations
- [ ] Audit trail present for all admin actions

---

## Phase 9: Post-Deployment

### 9.1 Monitoring Dashboard Setup

```bash
# Install Prometheus and Grafana (optional but recommended)
sudo apt-get install prometheus grafana-server

# Configure Prometheus to scrape application metrics
# Edit /etc/prometheus/prometheus.yml

# Configure Grafana dashboards for:
- API response times
- Error rates
- Grievance counts
- Admin activity
- System health
```

### 9.2 Backup Verification

```bash
# Test restoration weekly
sudo -u postgres psql -d grievance_system < backup.sql

# Verify data integrity
SELECT COUNT(*) FROM grievances;
SELECT COUNT(*) FROM audit_logs;
```

### 9.3 Security Scanning

```bash
# Run security checks
sudo apt-get install openssh-known-hosts
sudo sshpass -p 'password' ssh-keyscan -t rsa host >> ~/.ssh/known_hosts

# SSL certificate validation
curl -I https://grievance.gov.in

# Security headers check
curl -I -H "Host: grievance.gov.in" https://grievance.gov.in
```

---

## Troubleshooting

### Common Issues

#### 502 Bad Gateway
```bash
# Check API service
sudo systemctl status grievance-api
sudo systemctl restart grievance-api

# Check logs
tail -f /var/log/grievance/error.log
```

#### Database Connection Error
```bash
# Test connection
sudo -u postgres psql -d grievance_system -c "SELECT 1"

# Check PgBouncer
sudo systemctl status pgbouncer
```

#### High Memory Usage
```bash
# Restart API service
sudo systemctl restart grievance-api

# Monitor processes
htop

# Check for memory leaks
ps aux | grep gunicorn
```

#### SSL Certificate Issues
```bash
# Renew certificate manually
sudo certbot renew --force-renewal

# Check expiration
sudo openssl x509 -in /etc/letsencrypt/live/grievance.gov.in/fullchain.pem -noout -dates
```

---

## Support & Escalation

- **Technical Issues**: security@grievance.gov.in
- **Emergency**: +91-XXX-XXXX-XXXX
- **24/7 Monitoring**: ops-team@grievance.gov.in

---

**Document Version:** 1.0  
**Last Updated:** 2024-01-15  
**Next Review:** 2024-04-15
