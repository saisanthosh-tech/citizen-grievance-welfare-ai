# Backend API - Security Implementation Guide

## Overview

This is a production-ready FastAPI backend for the Citizen Grievance & Welfare Intelligence System. Built with government-grade security for handling citizen grievances at the national level.

## Security Features Implemented

✅ **Rate Limiting** - Prevents abuse with configurable limits
✅ **Input Validation** - Comprehensive validation for all inputs
✅ **Data Sanitization** - HTML/SQL injection prevention
✅ **Audit Logging** - Complete operation tracking
✅ **CORS Security** - Restricted cross-origin requests
✅ **Error Handling** - Comprehensive exception handling
✅ **Environment Configuration** - Secure .env system
✅ **Database Encryption** - Support for encrypted databases
✅ **HTTPS Support** - Ready for production TLS/SSL
✅ **Health Monitoring** - Built-in health check endpoints

## Quick Start

### Development Setup

```bash
# Clone repository
cd backend

# Create virtual environment
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Create .env file
cp .env.example .env

# Run application
python -m uvicorn app.main:app --reload
```

### Production Setup

```bash
# Install security dependencies
pip install -r requirements-security.txt

# Configure environment variables
cp .env.example .env
# Edit .env with production values

# Run with Gunicorn
gunicorn -w 4 -k uvicorn.workers.UvicornWorker \
  --bind 0.0.0.0:8000 \
  app.main_production:app
```

## Environment Configuration

### Required Variables

```env
# Application
ENVIRONMENT=production
DEBUG=False
SECRET_KEY=<generate with: openssl rand -hex 32>

# Database
DATABASE_URL=postgresql://user:password@localhost/grievance_system

# Security
ALLOWED_HOSTS=grievance.gov.in,www.grievance.gov.in
CORS_ORIGINS=https://grievance.gov.in
ENABLE_HTTPS_REDIRECT=True

# Rate Limiting
RATE_LIMIT_ENABLED=True
RATE_LIMIT_REQUESTS=100
RATE_LIMIT_WINDOW_SECONDS=60

# Logging
LOG_LEVEL=WARNING
LOG_FILE=/var/log/grievance/app.log
```

See `.env.example` for complete list of configuration options.

## API Endpoints

### Public Endpoints

#### 1. Submit Grievance
```
POST /grievances/
Rate Limit: 10 requests/minute

Request:
{
  "title": "Water supply issue in sector 5",
  "description": "No water supply for 3 days, affecting 500 families",
  "category": "Water Supply",
  "citizen_name": "John Doe",
  "email": "john@example.com",
  "phone": "9876543210",
  "location": "Sector 5, New Delhi"
}

Response:
{
  "id": 1,
  "tracking_token": "GRV-2024-001-ABC123",
  "status": "Pending",
  "confidence_score": 0.95,
  "message": "Grievance submitted successfully"
}
```

#### 2. Health Check
```
GET /health

Response:
{
  "status": "healthy",
  "timestamp": "2024-01-15T10:30:45.123456",
  "version": "1.0.0"
}
```

### Admin Endpoints (Require Authentication)

#### 3. Get Grievances
```
GET /grievances/?skip=0&limit=20&status_filter=Pending

Response:
{
  "total": 150,
  "count": 20,
  "data": [...]
}
```

#### 4. Update Grievance
```
PUT /grievances/{id}

Request:
{
  "status": "In Progress",
  "notes": "Assigned to field team"
}
```

#### 5. Get Statistics
```
GET /stats/

Response:
{
  "total_grievances": 150,
  "status_distribution": {
    "Pending": 50,
    "In Progress": 40,
    "Resolved": 50,
    "Rejected": 10
  },
  "category_distribution": {...}
}
```

## Security Modules

### security.py

Contains security utilities:

- **RateLimiter** - Request rate limiting with configurable windows
- **InputValidator** - Comprehensive input validation for all data types
- **DataSanitizer** - HTML and SQL injection prevention
- **AuditLogger** - Security event logging
- **PasswordValidator** - Strong password enforcement

Usage:
```python
from app.security import InputValidator, DataSanitizer, audit_logger

# Validate input
is_valid, text = InputValidator.validate_text(user_input)

# Sanitize data
safe_data = DataSanitizer.sanitize_dict(user_data)

# Log audit event
audit_logger.log_grievance_submission(grievance_id="GRV-123", category="Healthcare")
```

## Logging

### Log Locations

- **Application Logs**: `/var/log/grievance/app.log`
- **Access Logs**: `/var/log/grievance/access.log`
- **Audit Logs**: `/var/log/grievance/audit.log`
- **Error Logs**: `/var/log/grievance/error.log`

### Log Level Configuration

```env
LOG_LEVEL=INFO  # Options: DEBUG, INFO, WARNING, ERROR, CRITICAL
```

## Error Handling

### Standard Error Responses

All errors follow this format:

```json
{
  "detail": "Error message",
  "status_code": 400,
  "timestamp": "2024-01-15T10:30:45.123456"
}
```

### Common Error Scenarios

| Scenario | Status | Detail |
|----------|--------|--------|
| Missing required field | 400 | Validation error message |
| Invalid email format | 400 | "Invalid email address" |
| Rate limit exceeded | 429 | "Too many requests..." |
| Grievance not found | 404 | "Grievance not found" |
| Server error | 500 | "Internal server error" |

## Database

### Supported Databases

**Development:**
- SQLite (default, not recommended for production)

**Production:**
- PostgreSQL (recommended)

### Database URL Examples

```env
# SQLite (development)
DATABASE_URL=sqlite:///./grievance_system.db

# PostgreSQL (production)
DATABASE_URL=postgresql://grievance_app:password@prod-db.internal:5432/grievance_system

# PostgreSQL with connection pooling
DATABASE_URL=postgresql+psycopg2://grievance_app:password@pgbouncer.internal:6432/grievance_system
```

## Testing

### Run Tests
```bash
# Unit tests
pytest tests/

# With coverage
pytest --cov=app tests/

# Specific test file
pytest tests/test_security.py -v
```

### Manual API Testing

```bash
# Test health endpoint
curl https://grievance.gov.in/health

# Submit grievance
curl -X POST https://grievance.gov.in/grievances/ \
  -H "Content-Type: application/json" \
  -d '{
    "title": "Test Grievance",
    "description": "This is a test grievance for validation",
    "category": "Healthcare",
    "citizen_name": "Test User",
    "email": "test@example.com",
    "phone": "9876543210",
    "location": "Test Location"
  }'
```

## Performance Optimization

### Database Indexes

Key indexes created automatically:
- `idx_grievance_status` - For filtering by status
- `idx_grievance_category` - For filtering by category
- `idx_grievance_created_at` - For date range queries
- `idx_grievance_tracking_token` - For tracking lookups

### Caching Recommendations

For production, consider:
- Redis for session management
- Elasticsearch for grievance search
- CDN for static assets
- Database query caching

## Deployment

### Using Docker

```dockerfile
FROM python:3.11-slim

WORKDIR /app

COPY requirements-security.txt .
RUN pip install -r requirements-security.txt

COPY . .

CMD ["gunicorn", "--workers", "4", "--worker-class", "uvicorn.workers.UvicornWorker", "--bind", "0.0.0.0:8000", "app.main_production:app"]
```

### Using Systemd

See [DEPLOYMENT_GUIDE.md](../DEPLOYMENT_GUIDE.md) for complete systemd service configuration.

## Monitoring

### Health Check
```bash
# Regular health monitoring
curl -s https://grievance.gov.in/health | jq .
```

### Metrics to Monitor

- API response time (p50, p95, p99)
- Error rate (< 1% target)
- Request rate
- Database connection pool usage
- Disk usage
- Memory usage

## Security Checklist

Before deployment:

- [ ] Change all default credentials
- [ ] Set strong SECRET_KEY (minimum 32 characters)
- [ ] Enable HTTPS/TLS
- [ ] Configure .env with production values
- [ ] Set DEBUG=False
- [ ] Enable rate limiting
- [ ] Configure logging
- [ ] Set up automated backups
- [ ] Enable audit logging
- [ ] Test all endpoints
- [ ] Run security scan
- [ ] Document incident procedures

## Troubleshooting

### API Returns 502 Bad Gateway

```bash
# Check service status
sudo systemctl status grievance-api

# Check application logs
tail -f /var/log/grievance/error.log

# Restart service
sudo systemctl restart grievance-api
```

### Database Connection Failed

```bash
# Test connection
sudo -u postgres psql -d grievance_system -c "SELECT 1"

# Check database logs
sudo tail -f /var/log/postgresql/postgresql.log
```

### Rate Limiting Too Strict

Adjust in `.env`:
```env
RATE_LIMIT_REQUESTS=100    # Increase this
RATE_LIMIT_WINDOW_SECONDS=60
```

## Support

- **Technical Issues**: tech@grievance.gov.in
- **Security Concerns**: security@grievance.gov.in
- **Emergency**: +91-XXX-XXXX-XXXX

## License

Government of India - Citizen Grievance & Welfare System

---

**Version:** 1.0  
**Last Updated:** 2024-01-15  
**Maintainer:** System Administration Team
