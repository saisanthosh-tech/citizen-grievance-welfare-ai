# Security Best Practices Quick Reference

## For Developers

### 1. Input Validation
```python
from backend.app.security import InputValidator

# Validate text
is_valid, text = InputValidator.validate_text(user_input, min_length=1, max_length=5000)
if not is_valid:
    raise HTTPException(status_code=400, detail=text)

# Validate email
is_valid, email = InputValidator.validate_email(user_email)

# Validate category
is_valid, category = InputValidator.validate_category(category_input)
```

### 2. Data Sanitization
```python
from backend.app.security import DataSanitizer

# Sanitize text
safe_text = DataSanitizer.sanitize_html(user_text)

# Sanitize dictionary
safe_data = DataSanitizer.sanitize_dict(user_dict)

# Sanitize for SQL
safe_sql = DataSanitizer.sanitize_sql_string(user_input)
```

### 3. Audit Logging
```python
from backend.app.security import audit_logger

# Log grievance submission
audit_logger.log_grievance_submission(grievance_id="GRV-123", category="Healthcare")

# Log status update
audit_logger.log_grievance_update(grievance_id="GRV-123", status="Resolved", admin_id="admin_001")

# Log suspicious activity
audit_logger.log_suspicious_activity(activity="SQL_Injection_Attempt", details="Suspicious pattern detected")
```

---

## For System Administrators

### 1. Environment Configuration (.env)

**CRITICAL - Never share this file!**

```bash
# Generate secure keys
openssl rand -hex 32  # For SECRET_KEY
openssl rand -hex 16  # For ENCRYPTION_KEY

# Example .env
ENVIRONMENT=production
DEBUG=False
SECRET_KEY=<Generated64CharacterKey>
DATABASE_URL=postgresql://grievance_app:SecurePassword@prod-db.internal/grievance_system
ALLOWED_HOSTS=grievance.gov.in,www.grievance.gov.in
CORS_ORIGINS=https://grievance.gov.in
ENABLE_HTTPS_REDIRECT=True
RATE_LIMIT_ENABLED=True
LOG_LEVEL=WARNING
```

### 2. Database Security

**PostgreSQL Connection String Format:**
```
postgresql://username:password@host:5432/database_name
```

**Restrictions:**
```sql
-- Revoke unnecessary permissions
REVOKE DELETE ON ALL TABLES IN SCHEMA public FROM grievance_app;
REVOKE DROP ON SCHEMA public FROM grievance_app;
REVOKE CREATE ON DATABASE grievance_system FROM grievance_app;
```

### 3. SSL/TLS Certificate

**Let's Encrypt (Free):**
```bash
sudo certbot certonly --webroot -w /var/www/html -d grievance.gov.in
```

**Certificate Validation:**
```bash
# Check expiration
openssl x509 -in /path/to/cert.pem -noout -dates

# Check validity
curl -I https://grievance.gov.in
```

### 4. Firewall Rules

**UFW (Ubuntu):**
```bash
sudo ufw allow ssh
sudo ufw allow http
sudo ufw allow https
sudo ufw deny from any to any port 5432  # Block external DB access
```

### 5. Backup & Recovery

**Encrypted Backup:**
```bash
# Create backup
sudo -u postgres pg_dump grievance_system | gzip | \
  openssl enc -aes-256-cbc -salt -out backup.sql.gz.enc -k $ENCRYPTION_KEY

# Restore from backup
openssl enc -d -aes-256-cbc -in backup.sql.gz.enc -k $ENCRYPTION_KEY | \
  gunzip | sudo -u postgres psql grievance_system
```

---

## For Operations Team

### 1. Daily Checks

```bash
# Check API health
curl https://grievance.gov.in/health

# Check database connection
sudo systemctl status postgresql

# Check application service
sudo systemctl status grievance-api

# Check disk space
df -h

# Check memory usage
free -h
```

### 2. Weekly Tasks

- [ ] Review security logs: `grep ERROR /var/log/grievance/app.log | tail -100`
- [ ] Verify backups: `ls -lh /opt/grievance-system/backups/`
- [ ] Check for failed logins: `grep "Failed" /var/log/auth.log`
- [ ] Monitor disk usage: `du -sh /var/lib/postgresql/`

### 3. Monthly Tasks

- [ ] Update system packages: `sudo apt-get update && apt-get upgrade`
- [ ] Review admin activity: `grep "admin" /var/log/grievance/audit.log`
- [ ] Test backup restoration
- [ ] Review API error rates
- [ ] Check certificate expiration: `sudo certbot renew --dry-run`

### 4. Quarterly Tasks

- [ ] Security audit
- [ ] Penetration testing
- [ ] Disaster recovery drill
- [ ] Performance review
- [ ] Dependency updates

---

## Security Incident Response

### If You Notice Something Suspicious:

**1. DO NOT PANIC** - Follow the procedure

**2. ISOLATE**
```bash
# Check active connections
netstat -tulpn | grep ESTABLISHED

# If attacked, temporarily block IP
sudo ufw deny from 192.168.1.100

# Stop service if necessary
sudo systemctl stop grievance-api
```

**3. DOCUMENT**
```bash
# Capture current state
ps aux > /tmp/processes_snapshot.txt
netstat -tulpn > /tmp/network_snapshot.txt
sudo tail -1000 /var/log/grievance/app.log > /tmp/app_logs.txt
sudo tail -1000 /var/log/auth.log > /tmp/auth_logs.txt
```

**4. INVESTIGATE**
```bash
# Check for recent file changes
find /opt/grievance-system -mtime -1 -type f

# Check for suspicious processes
ps aux | grep -v "grep"

# Review recent logins
last -20
```

**5. REPORT**
- Email: security@grievance.gov.in
- Phone: +91-XXX-XXXX-XXXX
- Include: Time detected, symptoms, evidence collected

---

## Password Management

### For Admins

**Password Policy:**
- Minimum 12 characters
- Must include: UPPERCASE, lowercase, numbers, special characters
- Change every 90 days
- Never reuse last 5 passwords
- Never share via email or chat

**Strong Password Examples:**
```
Correct-Horse-Battery-Staple!2024
G0v3rnment-C1t1zen$ervice#Secure
MyDept@Grievance2024!NewPassword
```

**Weak Password Examples (DON'T USE):**
```
password123 (too simple)
admin1234 (predictable)
grievance (common word)
12345678 (sequential numbers)
```

---

## API Rate Limits

### Current Limits

| User Type | Requests/Min | Requests/Hour |
|-----------|--------------|---------------|
| Anonymous | 10 | 600 |
| Authenticated | 100 | 6000 |
| Admin | 500 | 30000 |

### Handling Rate Limits

**Response when limit exceeded:**
```json
{
  "status_code": 429,
  "detail": "Too many requests. Please try again later."
}
```

**Retry Strategy:**
- Wait 1 minute before retrying
- Use exponential backoff for multiple failures
- Contact support if legitimate needs exceed limits

---

## Common Error Codes

| Code | Meaning | Action |
|------|---------|--------|
| 400 | Bad Request | Check input validation |
| 401 | Unauthorized | Verify credentials/token |
| 403 | Forbidden | Check permissions |
| 404 | Not Found | Verify resource ID |
| 429 | Rate Limited | Wait and retry later |
| 500 | Server Error | Contact support |
| 503 | Service Unavailable | Check service status |

---

## Monitoring Dashboards

**Recommended Tools:**
- Prometheus: Metrics collection
- Grafana: Dashboard visualization
- ELK Stack: Log aggregation
- Sentry: Error tracking

**Key Metrics to Monitor:**
- API response time (target: <500ms)
- Error rate (target: <1%)
- Active users
- Grievance submission rate
- Database connection pool usage
- Disk space usage
- Memory utilization

---

## Support Contacts

| Issue | Contact | Method |
|-------|---------|--------|
| Technical Problem | tech@grievance.gov.in | Email |
| Security Incident | security@grievance.gov.in | Email + Phone |
| Urgent Issues | +91-XXX-XXXX-XXXX | Phone |
| Feature Request | support@grievance.gov.in | Email/Portal |
| Government Relations | legal@grievance.gov.in | Email |

---

## Document Information

- **Version:** 1.0
- **Last Updated:** 2024-01-15
- **Next Review:** 2024-04-15
- **Classification:** Internal - Sensitive
- **Distribution:** Development, Operations, Security Teams Only

**DO NOT share with unauthorized personnel**
