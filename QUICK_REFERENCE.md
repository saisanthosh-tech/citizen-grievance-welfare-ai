# Quick Reference Guide - Citizen Grievance & Welfare System

## 🚀 Getting Started (2 Minutes)

### Step 1: Install Frontend Dependencies
```bash
pip install -r requirements_frontend.txt
```

### Step 2: Start Backend (Terminal 1)
```bash
cd backend
python -m uvicorn app.main:app --reload
```
✅ Backend ready at: `http://127.0.0.1:8000`

### Step 3: Start Frontend (Terminal 2)
```bash
streamlit run frontend_streamlit.py
```
✅ Frontend ready at: `http://localhost:8501`

---

## 📱 User Interface Overview

```
┌─────────────────────────────────┐
│  Citizen Grievance & Welfare    │  ← Page Title
│  Intelligence System            │
└─────────────────────────────────┘

┌─────────────────────────────────┐
│  How it works (4 steps)         │  ← Info Box
└─────────────────────────────────┘

┌─────────────────────────────────┐
│  📝 Submit Your Grievance       │  ← Main Form
│  - Title (required)              │
│  - Description (required)        │
│  - Location (optional)           │
│  [Submit Button]                 │
└─────────────────────────────────┘

┌─────────────────────────────────┐
│  📊 AI Analysis Results         │  ← Results
│  - Category badge               │
│  - Priority level               │
│  - Suggested schemes            │
└─────────────────────────────────┘

┌─────────────────────────────────┐
│  📋 View All Grievances         │  ← Grievance List
│  - Statistics (metrics)         │
│  - Grievance table              │
└─────────────────────────────────┘
```

---

## 🎯 Key Features

| Feature | Description | Location |
|---------|-------------|----------|
| **Submit Grievance** | Citizen submits issue | Main Form |
| **AI Analysis** | Auto-categorize + prioritize | Results Panel |
| **View Schemes** | See relevant govt programs | Results Panel |
| **List Grievances** | View all submissions | Bottom Section |
| **Status Indicator** | Backend connectivity | Sidebar |

---

## ✅ Form Validation Rules

| Field | Type | Rules | Example |
|-------|------|-------|---------|
| Title | Text | Min 5 chars | "Water shortage in Sector 4" |
| Description | Text Area | Min 20 chars | "No water for 3 days..." |
| Location | Text | Optional | "Sector 4" or "Ward No. 5" |

---

## 🏷️ Grievance Categories

```
Category          Keywords Detected
─────────────────────────────────────────
Healthcare        hospital, doctor, health
Education         school, teacher, student
Water Supply      water, leak, shortage
Roads & Transport road, pothole, bus
Electricity       power, outage, voltage
Sanitation        garbage, waste, drain
```

---

## 🚨 Priority Levels

```
Priority  Color   Keywords
─────────────────────────────────────
HIGH      🔴 Red  urgent, emergency, danger
MEDIUM    🟡 Yellow (default)
LOW       🟢 Green minor, suggestion
```

---

## 🛠️ API Endpoints

### Submit Grievance
```bash
POST http://127.0.0.1:8000/grievances/

Request:
{
  "title": "Water shortage",
  "description": "No water for 3 days",
  "location": "Sector 4"
}

Response:
{
  "id": 1,
  "title": "Water shortage",
  "description": "No water for 3 days",
  "location": "Sector 4",
  "category": "Water Supply",
  "priority": "High",
  "status": "Pending",
  "suggested_schemes": [
    "Jal Jeevan Mission",
    "Atal Bhujal Yojana"
  ],
  "created_at": "2026-01-31T15:45:30"
}
```

### Get All Grievances
```bash
GET http://127.0.0.1:8000/grievances/?skip=0&limit=100
```

### API Documentation
```
http://127.0.0.1:8000/docs  (Interactive Swagger UI)
http://127.0.0.1:8000/redoc (ReDoc documentation)
```

---

## 🔍 Testing Commands

### Test Backend with Python
```bash
cd backend
python test_api.py
```

### Test with cURL
```bash
# Submit grievance
curl -X POST http://127.0.0.1:8000/grievances/ \
  -H "Content-Type: application/json" \
  -d '{"title":"Test","description":"Test grievance"}'

# Get all grievances
curl http://127.0.0.1:8000/grievances/
```

### Test Frontend
1. Open http://localhost:8501
2. Fill form with test data
3. Click "Submit for AI Analysis"
4. Verify results display

---

## 🎨 Color Reference

| Color | Hex Code | Usage |
|-------|----------|-------|
| Primary Blue | #0066cc | Headers, links |
| Success Green | #28a745 | Positive actions |
| Warning Yellow | #ffc107 | Medium priority |
| Danger Red | #dc3545 | High priority |
| Neutral Gray | #555 | Secondary text |
| White | #ffffff | Backgrounds |

---

## ⚙️ Configuration

### Change Backend URL
**File**: `frontend_streamlit.py`
**Line**: Find `API_BASE_URL = "http://127.0.0.1:8000"`
```python
API_BASE_URL = "http://your-backend-url:8000"
```

### Change Frontend Port
```bash
streamlit run frontend_streamlit.py --server.port 8502
```

### Change Backend Port
```bash
cd backend
python -m uvicorn app.main:app --reload --port 8001
# Update API_BASE_URL in frontend accordingly
```

---

## 🐛 Troubleshooting

| Issue | Solution |
|-------|----------|
| Backend won't start | Port 8000 in use? Kill process and retry |
| Frontend won't connect | Verify backend running on http://127.0.0.1:8000 |
| Dependencies missing | Run `pip install -r requirements_frontend.txt` |
| Database error | Delete `grievance.db` and restart backend |
| Streamlit not auto-reload | Save file again or restart server |

---

## 📁 Important Files

```
Project Root/
├── frontend_streamlit.py        ← Main frontend app
├── requirements_frontend.txt    ← Frontend dependencies
├── backend/
│   ├── app/main.py             ← Backend API
│   ├── app/ml_engine.py        ← AI analyzer
│   └── requirements.txt        ← Backend dependencies
├── FRONTEND_GUIDE.md           ← Detailed docs
├── UI_WALKTHROUGH.md           ← Interface guide
└── README.md                   ← Full documentation
```

---

## 📊 Demo Data

### Sample Grievance 1
```
Title: Water shortage in Sector 4
Description: No water supply for 3 days. Water tanks are empty.
             This is affecting daily life of 1000+ residents.
Location: Sector 4

Expected Result:
✓ Category: Water Supply
✓ Priority: High
✓ Schemes: Jal Jeevan Mission, Atal Bhujal Yojana
```

### Sample Grievance 2
```
Title: Potholes on Main Street
Description: Multiple potholes on Main Street are causing accidents.
             Bus passengers get injured. Needs immediate repair.
Location: Main Street, Ward 3

Expected Result:
✓ Category: Roads & Transport
✓ Priority: High
✓ Schemes: Pradhan Mantri Gram Sadak Yojana
```

### Sample Grievance 3
```
Title: School roof needs repair
Description: School roof has leak. During rain, water drips in classroom.
             Students can't attend classes properly.
Location: Government School, Area 5

Expected Result:
✓ Category: Education
✓ Priority: Medium
✓ Schemes: Sarva Shiksha Abhiyan
```

---

## 🚢 Deployment Checklist

- [ ] Backend running on production server
- [ ] Frontend deployed to Streamlit Cloud or similar
- [ ] SSL/HTTPS configured
- [ ] Database backed up
- [ ] API rate limiting configured
- [ ] Error logging enabled
- [ ] Monitoring set up
- [ ] Documentation updated
- [ ] User guide created
- [ ] Testing completed

---

## 📞 Support Resources

| Resource | Link | Purpose |
|----------|------|---------|
| Frontend Guide | `FRONTEND_GUIDE.md` | Detailed frontend docs |
| UI Walkthrough | `UI_WALKTHROUGH.md` | Interface screenshots |
| API Docs (Live) | `http://127.0.0.1:8000/docs` | Interactive API explorer |
| Backend Code | `backend/app/main.py` | Backend implementation |
| Frontend Code | `frontend_streamlit.py` | Frontend implementation |

---

## 🎓 Learning Path

1. **Start**: Read this quick reference
2. **Understand**: Read `README.md`
3. **Explore**: Open `http://127.0.0.1:8000/docs` (API docs)
4. **Try**: Submit sample grievances
5. **Examine**: Review `FRONTEND_GUIDE.md`
6. **Customize**: Edit `frontend_streamlit.py` or `backend/app/ml_engine.py`
7. **Deploy**: Follow deployment checklist

---

**Quick Reference Version 1.0**  
**Last Updated**: January 31, 2026  
**Status**: Ready for Production ✅
