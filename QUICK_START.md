# 🚀 Quick Start Guide - Multi-Page Application

## Start Here

Your Citizen Grievance & Welfare Intelligence System is now a professional multi-page web application!

---

## ⚡ Quick Start (2 Minutes)

### Step 1: Open Two Terminals

**Terminal 1 - Backend:**
```bash
cd citizen-grievance-welfare-ai\backend
python -m uvicorn app.main:app --reload --port 8000
```

**Terminal 2 - Frontend:**
```bash
cd citizen-grievance-welfare-ai
python -m streamlit run app_home.py
```

### Step 2: Open Browser
Visit: **http://localhost:8501**

### Step 3: Explore!
- 🏠 See the Home page with stats
- 📝 Submit a test grievance
- 🔍 Track using the ID
- ❓ Browse the Help page
- 🔐 Try admin login (admin/admin123)

---

## 📖 Navigation

### Main Menu (Left Sidebar)
- 🏛️ **Home** - Main page with stats
- 📝 **Submit Grievance** - Create new
- 🔍 **Track Grievance** - Check status
- ❓ **About & Help** - FAQ & guides
- 🔐 **Admin Login** - Staff access

### Quick Demo

**As a Citizen:**
1. Click **Submit Grievance**
2. Fill form: "Pothole on Main Street"
3. Get your **Grievance ID**
4. Click **Track Grievance**
5. Enter the ID to see status

**As Admin:**
1. Click **Admin Login**
2. Username: `admin` | Password: `admin123`
3. View dashboard with all grievances
4. Update status and add notes

---

## 📁 File Structure

```
Root Directory:
├── app_home.py ..................... HOME PAGE (entry point)
├── pages/ .......................... PAGE FILES
│   ├── 01_Submit_Grievance.py ...... Submit page
│   ├── 02_Track_Grievance.py ....... Track page
│   ├── 03_About_Help.py ............ Help page
│   ├── 04_Admin_Login.py ........... Login page
│   └── 04_Admin_Dashboard.py ....... Dashboard
├── backend/ ........................ API SERVER
│   ├── app/
│   │   ├── main.py ................ FastAPI app
│   │   ├── ml_engine.py ........... AI analysis
│   │   ├── models.py .............. Database
│   │   └── schemas.py ............. Data types
│   └── requirements.txt
├── MULTI_PAGE_GUIDE.md ............ FULL DOCUMENTATION
└── IMPLEMENTATION_SUMMARY.md ...... WHAT WAS CREATED
```

---

## 🎯 5 Main Pages

### 1. 🏠 Home (`app_home.py`)
- Statistics dashboard
- System overview
- Quick actions
- FAQ

### 2. 📝 Submit (`01_Submit_Grievance.py`)
- Grievance form
- AI analysis
- ID generation
- Program suggestions

### 3. 🔍 Track (`02_Track_Grievance.py`)
- Search by ID
- Status display
- Timeline view
- Official notes

### 4. ❓ Help (`03_About_Help.py`)
- FAQ (10 questions)
- How-to guides
- Contact info
- Problem reporting

### 5. 🔐 Admin (`04_Admin_Login.py` + `04_Admin_Dashboard.py`)
- Staff login
- Grievance management
- Statistics
- Status updates

---

## ✨ Key Features

✅ **No Login Required** - Citizens submit anonymously  
✅ **AI Categorization** - Automatic analysis of grievances  
✅ **Unique IDs** - Track grievances easily  
✅ **Admin Dashboard** - Manage all submissions  
✅ **Government-Grade** - Professional design  
✅ **Mobile Friendly** - Works on phones/tablets  
✅ **Help Section** - Comprehensive support  

---

## 🔗 URLs

- **Frontend:** http://localhost:8501
- **Backend API:** http://localhost:8000
- **API Docs:** http://localhost:8000/docs

---

## 🧪 Quick Test

### Submit a Test Grievance
1. Go to Home page
2. Click "📝 Submit Grievance" button
3. Fill form:
   - **Title:** "Water leak on Street 5"
   - **Description:** "There has been a water leak for 3 days affecting 50 homes"
   - **Location:** "Ward 5"
4. Click "Submit Grievance"
5. **SAVE YOUR ID** (looks like: GR-123456)

### Track Your Grievance
1. Click "🔍 Track Grievance"
2. Paste your ID
3. Click "Search"
4. See status and details

### Try Admin Dashboard
1. Click "🔐 Admin Login"
2. Username: **admin**
3. Password: **admin123**
4. Click "Login"
5. View dashboard with stats and all grievances

---

## ⚙️ Configuration

### Backend Port
```python
# Currently: http://localhost:8000
# To change: python -m uvicorn app.main:app --port 9000
```

### Frontend Port
```python
# Currently: http://localhost:8501
# To change: streamlit run app_home.py --server.port 9501
```

---

## 🆘 Troubleshooting

### "Cannot connect to backend"
```
✓ Check backend is running (look for "Uvicorn running" message)
✓ Check port 8000 is free
✓ Restart both services
```

### "No data showing"
```
✓ Submit a test grievance first
✓ Check backend is running
✓ Refresh page (F5)
```

### "Can't find my grievance"
```
✓ Check you entered correct ID
✓ Check ID format: GR-XXXXXX
✓ Check ID exists in system
```

### "Admin login failed"
```
✓ Use demo credentials:
  - Username: admin
  - Password: admin123
```

---

## 📊 System Stats

- **Pages:** 5 main pages
- **Lines of Code:** 2000+ lines
- **Database:** SQLite (auto-created)
- **API:** FastAPI with 3 endpoints
- **Design:** Government-grade UI/UX

---

## 🎓 Documentation

Full documentation in:
1. **MULTI_PAGE_GUIDE.md** - Complete guide (200+ lines)
2. **IMPLEMENTATION_SUMMARY.md** - What was created
3. **BACKEND_GUIDE.md** - API reference
4. **In-app Help** - "About & Help" page

---

## 🚀 What Happens Next?

After exploring:
1. ✅ Review MULTI_PAGE_GUIDE.md for full details
2. ✅ Test all features thoroughly
3. ✅ Check backend API at http://localhost:8000/docs
4. ✅ Review code and understand structure
5. ✅ Plan production deployment

---

## 🎉 You're All Set!

The application is:
- ✅ Fully functional
- ✅ Production-ready (with security updates recommended)
- ✅ Multi-page and professional
- ✅ Government-grade design
- ✅ Citizen-friendly
- ✅ Well-documented

**Enjoy exploring! 🎊**

---

## 📞 Getting Help

### Inside the App
- Go to "❓ About & Help" page
- Browse FAQ section
- Read How-to guides
- Contact support info

### In Code
- Check comment blocks
- Review MULTI_PAGE_GUIDE.md
- Review BACKEND_GUIDE.md
- Check function docstrings

---

**Remember:** Always keep both terminals running (backend + frontend)!

Last Updated: January 31, 2025  
Status: ✅ Ready to Use
