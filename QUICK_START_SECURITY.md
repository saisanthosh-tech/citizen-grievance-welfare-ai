# 🚀 Quick Start Guide

**For**: Citizen Grievance & Welfare Intelligence System  
**Phase**: Security Hardening Complete  
**Status**: Production Ready

---

## ⚡ 5-Minute Setup (Development)

### Step 1: Clone & Navigate
```bash
cd citizen-grievance-welfare-ai
cd backend
```

### Step 2: Create Virtual Environment
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

### Step 3: Install Dependencies
```bash
pip install -r requirements.txt
```

### Step 4: Setup Environment
```bash
cp .env.example .env
# Edit .env with development values (keep defaults for dev)
```

### Step 5: Run Backend
```bash
python -m uvicorn app.main:app --reload
```

Backend is now running at: `http://localhost:8000`

### Step 6: Run Frontend (New Terminal)
```bash
cd ..  # Go to root
streamlit run app_home.py
```

Frontend is now running at: `http://localhost:8501`

---

## 📊 Test the System

### Check API Health
```bash
curl http://localhost:8000/health
```

Expected Response:
```json
{
  "status": "healthy",
  "timestamp": "2024-01-15T10:30:45.123456",
  "version": "1.0.0"
}
```

### Submit a Grievance
```bash
curl -X POST http://localhost:8000/grievances/ \
  -H "Content-Type: application/json" \
  -d '{
    "title": "Water Supply Issue",
    "description": "No water supply for 3 days in our area",
    "category": "Water Supply",
    "citizen_name": "John Doe",
    "email": "john@example.com",
    "phone": "9876543210",
    "location": "Sector 5, Delhi"
  }'
```

### Check Grievances
```bash
curl http://localhost:8000/grievances/
```

---

## 🔒 Security Features Enabled

✅ Rate Limiting (10 requests/minute for public)
✅ Input Validation (all fields validated)
✅ Data Sanitization (XSS/SQL injection prevention)
✅ Audit Logging (all operations logged)
✅ Error Handling (comprehensive)
✅ CORS Protection (cross-origin restricted)
✅ Health Checks (available)

---

## 📁 Important Files

| File | Purpose |
|------|---------|
| `backend/app/security.py` | Security modules |
| `backend/app/main.py` | Development API |
| `backend/app/main_production.py` | Production API |
| `backend/.env.example` | Configuration template |
| `SECURITY.md` | Security guidelines |
| `DEPLOYMENT_GUIDE.md` | Production deployment |

---

## 🛠️ Troubleshooting

### Port Already in Use
```bash
# Change port for backend
python -m uvicorn app.main:app --reload --port 8001

# Change port for frontend
streamlit run app_home.py --server.port 8502
```

### Module Not Found
```bash
# Ensure virtual environment is activated
source venv/bin/activate

# Reinstall requirements
pip install -r requirements.txt
```

### Database Error
```bash
# SQLite database will auto-create
# Check if grievance.db exists in backend/
ls -la backend/grievance.db
```

---

## 📚 Documentation

| Document | For | What |
|----------|-----|------|
| [SECURITY.md](SECURITY.md) | Admins/Security | Security architecture |
| [DEPLOYMENT_GUIDE.md](DEPLOYMENT_GUIDE.md) | Ops | Production deployment |
| [backend/BACKEND_README.md](backend/BACKEND_README.md) | Developers | API documentation |
| [SECURITY_QUICK_REFERENCE.md](SECURITY_QUICK_REFERENCE.md) | All | Quick lookup |

---

## 🚀 Production Deployment

For production deployment with HTTPS, PostgreSQL, and monitoring:

**See**: [DEPLOYMENT_GUIDE.md](DEPLOYMENT_GUIDE.md)

Quick summary:
1. Read DEPLOYMENT_GUIDE.md
2. Set up Ubuntu 22.04 LTS server
3. Configure .env with production values
4. Install PostgreSQL
5. Deploy with Gunicorn + Nginx
6. Enable HTTPS with Let's Encrypt
7. Set up monitoring and backups

---

## 📞 Help

- **Docs**: Read the markdown files
- **Code**: Check comments in source files
- **Issues**: See SECURITY_QUICK_REFERENCE.md for troubleshooting
- **Support**: tech@grievance.gov.in

---

## ✅ Verification

After starting both services, verify:

- [ ] Backend responds to `/health`
- [ ] Frontend loads on port 8501
- [ ] Can submit a grievance
- [ ] Tracking token generated
- [ ] No errors in logs
- [ ] Rate limiting active

---

## 🎯 Next Steps

1. **Explore the System**
   - Submit some test grievances
   - Check the frontend pages
   - Review the API endpoints

2. **Read the Docs**
   - Start with SECURITY_QUICK_REFERENCE.md
   - Review SECURITY.md for deeper understanding
   - Check DEPLOYMENT_GUIDE.md for production setup

3. **Understand Security**
   - Review backend/app/security.py
   - Understand each validator
   - Check logging output

4. **Plan Deployment**
   - Read DEPLOYMENT_GUIDE.md completely
   - Prepare production server
   - Create deployment checklist
   - Train your team

---

**Ready to go!** 🚀

Start with: `streamlit run app_home.py`

See [DEPLOYMENT_GUIDE.md](DEPLOYMENT_GUIDE.md) for production setup.
