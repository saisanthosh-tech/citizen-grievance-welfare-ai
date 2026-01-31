# Security Guidelines for Citizen Grievance & Welfare System

## 📋 Table of Contents
1. [Authentication & Authorization](#authentication--authorization)
2. [Data Protection](#data-protection)
3. [API Security](#api-security)
4. [Infrastructure Security](#infrastructure-security)
5. [Monitoring & Compliance](#monitoring--compliance)
6. [Incident Response](#incident-response)

---

## Authentication & Authorization

### Current State
- Demo credentials for testing only (NOT for production)
- Admin credentials: admin/admin_password_123 (CHANGE IMMEDIATELY IN PRODUCTION)

### Production Requirements

#### 1. Multi-Factor Authentication (MFA)
```
REQUIRED for all admin accounts
- Email OTP (2-factor)
- Time-based One-Time Password (TOTP)
- SMS verification
```

#### 2. Session Management
- Session timeout: 30 minutes of inactivity
- Secure session cookies with HttpOnly flag
- Secure flag for HTTPS connections
- SameSite=Strict cookie policy

#### 3. Password Policy
- Minimum 12 characters
- Must contain: uppercase, lowercase, digits, special characters
- Password expiration: Every 90 days
- Password history: Last 5 passwords cannot be reused
- Lockout: 5 failed attempts = 30 minute lockout

#### 4. API Authentication
- Bearer token with JWT
- Token expiration: 1 hour
- Refresh tokens: 7 days
- All API calls require authentication (except health check)

```python
# Example
POST /token
{
  "username": "admin",
  "password": "SecurePassword123!",
  "mfa_code": "123456"
}

# Response
{
  "access_token": "eyJ0eXAiOiJKV1QiLCJhbGc...",
  "token_type": "bearer",
  "expires_in": 3600
}
```

---

## Data Protection

### 1. Encryption in Transit
```
REQUIRED: TLS 1.2+ for all connections
- HTTP to HTTPS redirect
- HSTS header: max-age=31536000
- Certificate pinning for critical endpoints
```

### 2. Encryption at Rest
```
SQLite (Development):
- Not recommended for production
- Database file permissions: 600 (owner only)

PostgreSQL (Production):
- pgcrypto extension for encryption
- Transparent Data Encryption (TDE)
- Encrypted backups
```

### 3. Field-Level Encryption
Encrypt sensitive fields before storing:
```python
ENCRYPTED FIELDS:
- Citizen name
- Phone number
- Email address
- Address/Location
- Grievance description
- Admin notes
```

### 4. Data Retention Policy
```
Grievances:
- Active: Keep for 1 year
- Archived: Keep for 5 years (encrypted)
- Deleted: Permanent deletion after 7 years

Audit Logs:
- Keep for 7 years minimum
- Immutable storage
```

### 5. PII Protection
```
Privacy Controls:
- Mask phone numbers: XXX-XXX-1234
- Mask email: a***@example.com
- Mask address: Partially visible to non-admin users
- Full data only to grievance owner and assigned admin
```

---

## API Security

### 1. Rate Limiting
```
Configured limits:
- Anonymous users: 10 requests/minute
- Authenticated users: 100 requests/minute
- Admin users: 500 requests/minute
- Emergency override: Available for government officials

Penalties:
- 1st violation: Warning
- 2nd-5th violation: 10 minute block
- 6+ violations: 1 hour block + admin review
```

### 2. Input Validation
```
All inputs validated:
✓ Text length limits
✓ Email format validation
✓ Phone number validation
✓ Category whitelist
✓ Status whitelist
✓ File type validation
✓ File size limits (max 10MB per file)
```

### 3. SQL Injection Prevention
```
Implementation:
- SQLAlchemy ORM (parameterized queries)
- No string concatenation in queries
- Input validation before database operations
- Prepared statements for all queries
```

### 4. XSS Protection
```
Implementation:
- HTML sanitization on all inputs
- Content-Security-Policy headers
- X-Frame-Options: DENY
- X-Content-Type-Options: nosniff
- X-XSS-Protection: 1; mode=block
```

### 5. CSRF Protection
```
CSRF Token Strategy:
- Token in session
- Token in request header
- Token rotation on sensitive operations
- SameSite cookies (Strict)
```

### 6. API Endpoints Security

#### POST /grievances/
```
Authentication: Public (rate limited)
Rate Limit: 10 requests/minute per IP
Validation:
  - Category required + validated
  - Title: 10-200 characters
  - Description: 20-5000 characters
  - Email: Valid format
  - Phone: 10 digits
Response: Grievance ID (token) for tracking
```

#### GET /grievances/
```
Authentication: Admin only (JWT)
Rate Limit: 100 requests/minute
Filters: Status, Category, Date range
Returns: Paginated results (default 20 per page, max 100)
```

#### PUT /grievances/{id}
```
Authentication: Admin only (JWT)
Rate Limit: 100 requests/minute
Authorization: Admin users only
Validation:
  - Status must be valid
  - Notes: Optional, 0-2000 characters
Audit: Log all updates with timestamp and admin ID
```

#### GET /stats/
```
Authentication: Admin only (JWT)
Rate Limit: 50 requests/minute
Returns: Aggregated statistics only
Privacy: No individual grievance data
```

---

## Infrastructure Security

### 1. Server Configuration

#### Firewall Rules
```
Ingress:
  - HTTPS (443): World
  - SSH (22): Admin networks only
  - HTTP (80): World (redirect to HTTPS)
  
Egress:
  - SMTP (587): Configured email servers only
  - DNS (53): System DNS only
```

#### Server Hardening
```
✓ Disable unused services
✓ SSH key-based authentication (no passwords)
✓ Fail2Ban for brute-force protection
✓ SELinux or AppArmor enabled
✓ Automatic security updates enabled
✓ Unnecessary ports closed
✓ All services running as non-root
```

### 2. Database Security

#### PostgreSQL Production Setup
```sql
-- Create encrypted database
CREATE DATABASE grievance_system
  WITH OWNER postgres
  TEMPLATE template0
  ENCODING 'UTF8';

-- Enable pgcrypto extension
CREATE EXTENSION pgcrypto;

-- Create app user (not superuser)
CREATE USER grievance_app WITH ENCRYPTED PASSWORD 'GeneratedSecurePassword123!';

-- Restrict permissions
GRANT CONNECT ON DATABASE grievance_system TO grievance_app;
GRANT USAGE ON SCHEMA public TO grievance_app;
GRANT SELECT, INSERT, UPDATE ON ALL TABLES IN SCHEMA public TO grievance_app;
REVOKE DELETE ON ALL TABLES IN SCHEMA public FROM grievance_app;

-- Connection pooling
-- Use PgBouncer with 20 max connections
```

#### Backup Strategy
```
Automated Daily Backups:
- Full backup: Daily at 2 AM UTC
- Incremental backups: Every 6 hours
- Backup retention: 30 days (encrypted storage)
- Backup testing: Weekly restore test
- Geographically distributed: 2 locations minimum
- Encryption: AES-256 for backup files
```

### 3. Application Server

#### Environment Variables
```
Required for production (.env file):

# Security
SECRET_KEY=<GenerateSecureKey_MinimumLength64>
ALGORITHM=HS256
JWT_EXPIRATION_HOURS=1

# Database
DATABASE_URL=postgresql://grievance_app:password@prod-db.internal/grievance_system

# Server
ENVIRONMENT=production
DEBUG=False
ALLOWED_HOSTS=grievance.gov.in,www.grievance.gov.in,admin.grievance.gov.in

# Security Headers
ENABLE_HTTPS_REDIRECT=True
ENABLE_SECURITY_HEADERS=True
CORS_ORIGINS=https://grievance.gov.in

# Rate Limiting
RATE_LIMIT_ENABLED=True
RATE_LIMIT_REQUESTS=100
RATE_LIMIT_WINDOW_SECONDS=60

# Logging
LOG_LEVEL=WARNING
LOG_FILE=/var/log/grievance/app.log

# Email (for notifications)
SMTP_ENABLED=True
SMTP_HOST=mail.example.com
SMTP_PORT=587
SMTP_USER=noreply@grievance.gov.in
SMTP_PASSWORD=<Encrypted>

# Encryption
ENCRYPTION_ENABLED=True
ENCRYPTION_KEY=<GenerateSecureKey_MinimumLength32>
```

---

## Monitoring & Compliance

### 1. Security Logging

#### Log All Events
```
✓ Authentication attempts (success/failure)
✓ Authorization failures
✓ API errors and exceptions
✓ Rate limit violations
✓ Admin actions (create, read, update, delete)
✓ Data access requests
✓ Suspicious patterns (detected malicious requests)
✓ System errors and warnings
```

#### Audit Log Format
```json
{
  "timestamp": "2024-01-15T10:30:45Z",
  "event_type": "grievance_created",
  "event_id": "EVT-2024-001234",
  "user_id": "anonymous",
  "ip_address": "192.168.1.100",
  "endpoint": "/grievances/",
  "method": "POST",
  "status_code": 201,
  "duration_ms": 245,
  "grievance_id": "GRV-2024-005678",
  "category": "Healthcare",
  "risk_level": "low"
}
```

### 2. Compliance Requirements

#### Government Standards
```
REQUIRED COMPLIANCE:
- National Information Board (NIB) guidelines
- Data Protection Act compliance
- Right to Information (RTI) requirements
- Official Secrets Act considerations
- ISO 27001 Information Security Management

OPTIONAL BUT RECOMMENDED:
- ISO 27035 Incident Response
- SOC 2 Type II certification
- Regular penetration testing
- Annual security audit
```

### 3. Monitoring & Alerts

#### Dashboard Metrics
```
Real-time Monitoring:
- Total grievances: Daily count
- Response time: P50, P95, P99
- Error rate: % of failed requests
- Active users: Concurrent sessions
- Rate limit violations: Daily count
- Failed logins: Daily attempts
- Unauthorized access attempts: Daily count
```

#### Alert Thresholds
```
CRITICAL (Immediate Notification):
- Error rate > 5% for 5 minutes
- Failed login attempts: > 10 per hour
- Rate limit violations: > 100 per hour
- Database connection failures
- API response time > 5 seconds

WARNING (Daily Report):
- Error rate > 1%
- Disk usage > 80%
- Failed backups
- Expired certificates (7 days warning)
```

### 4. Vulnerability Management

#### Regular Security Activities
```
✓ Weekly: Log review and analysis
✓ Monthly: Security scan execution
✓ Quarterly: Penetration testing
✓ Semi-annually: Full security audit
✓ Annually: Disaster recovery drill

Vulnerability Tracking:
- Track all identified vulnerabilities
- Risk scoring (CVSS)
- Remediation timeline
- Root cause analysis
```

---

## Incident Response

### 1. Incident Classification

#### Severity Levels
```
CRITICAL: 
- Data breach confirmed
- System down (> 1 hour)
- Authentication system compromised
- Response: 15 minutes

HIGH:
- Unauthorized access attempt
- Performance degradation (> 50%)
- Security alert triggered
- Response: 1 hour

MEDIUM:
- Failed authentication multiple times
- Warning logs exceed threshold
- Response: 4 hours

LOW:
- Informational logs
- Normal operational alerts
- Response: Next business day
```

### 2. Response Procedure

#### Step 1: Detect & Alert
```
- Automated alert triggered
- On-call team notified
- Incident ticket created
- Response clock starts
```

#### Step 2: Contain
```
- Isolate affected systems
- Preserve evidence/logs
- Stop ongoing compromise
- Notify management
```

#### Step 3: Investigate
```
- Root cause analysis
- Scope of compromise
- Data affected (if any)
- Timeline reconstruction
```

#### Step 4: Remediate
```
- Apply security patches
- Remove malicious access
- Restore from backups if needed
- Validate system integrity
```

#### Step 5: Recovery
```
- Restore normal operations
- Monitor for recurrence
- User notifications if required
- Legal notification (if required by law)
```

#### Step 6: Post-Incident
```
- Full incident report
- Root cause documentation
- Process improvements
- Team training/updates
- Regulatory notification (if required)
```

### 3. Contact Information
```
Security Team: security@grievance.gov.in
Emergency: +91-XXX-XXXX-XXXX
Legal: legal@grievance.gov.in
Public Relations: pr@grievance.gov.in
```

---

## Security Checklist for Deployment

### Before Going Live
- [ ] Change all default credentials
- [ ] Enable HTTPS with valid certificate
- [ ] Configure .env with production values
- [ ] Enable database encryption
- [ ] Configure automated backups
- [ ] Set up monitoring and alerts
- [ ] Configure rate limiting
- [ ] Enable audit logging
- [ ] Configure firewall rules
- [ ] Run security scan
- [ ] Complete penetration test
- [ ] Train admin team on security policies
- [ ] Establish incident response procedures
- [ ] Document disaster recovery plan
- [ ] Notify relevant government bodies

### Ongoing Security
- [ ] Weekly: Review security logs
- [ ] Monthly: Update dependencies
- [ ] Quarterly: Run penetration tests
- [ ] Annually: Full security audit
- [ ] Daily: Monitor alerts and metrics
- [ ] Immediate: Respond to security incidents

---

## Additional Resources

### Security Best Practices
- OWASP Top 10: https://owasp.org/www-project-top-ten/
- NIST Cybersecurity Framework: https://www.nist.gov/cyberframework
- CIS Critical Security Controls: https://www.cisecurity.org/controls

### Tools
- OWASP ZAP: Web application security testing
- SQLMap: SQL injection testing
- Burp Suite: Security testing platform
- Bandit: Python security linter

---

**Document Version:** 1.0  
**Last Updated:** 2024-01-15  
**Approval:** System Administrator  
**Review Frequency:** Quarterly
