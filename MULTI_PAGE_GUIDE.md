# Citizen Grievance & Welfare Intelligence System
## Multi-Page Application User Guide

**System Status:** ✅ Fully Operational  
**Frontend:** Running on http://localhost:8501  
**Backend:** Running on http://localhost:8000  
**Database:** SQLite (auto-initialized)

---

## 🏠 Application Structure

### Pages

The application is organized into 5 main pages accessible from the sidebar:

#### 1. **Home Page** (`app_home.py`)
The main entry point with:
- Welcome banner and system overview
- Quick action buttons for common tasks
- System statistics dashboard
- Feature cards explaining how the system works
- Comprehensive FAQ section
- Government-grade design and messaging

**Features:**
- Statistics dashboard showing total grievances by priority
- Direct navigation to other pages
- Quick access to submit or track grievances
- Information about available support programs
- Contact information and support resources

#### 2. **Submit Grievance** (`pages/01_Submit_Grievance.py`)
Citizens submit their concerns and receive automated analysis.

**Features:**
- Simple, clear form with 3 inputs
- Input validation (title 5+ chars, description 20+ chars)
- Automatic AI categorization
- Confidence scoring (0-100%)
- Suggested government schemes
- Unique Grievance ID for tracking
- Submission history tracking

**Form Fields:**
- Subject of Your Concern (required)
- Detailed Description (required)
- Location (optional but recommended)

**Output:**
- Grievance ID (must save for tracking)
- Assigned category
- Priority level
- AI confidence score
- Relevant government programs
- Analysis explanation

#### 3. **Track Grievance** (`pages/02_Track_Grievance.py`)
Citizens check the status of submitted grievances.

**Features:**
- Simple search by Grievance ID
- Complete grievance details display
- Current status with emoji indicators
- Timeline of events
- Official notes and updates
- Analysis metadata (confidence, keywords)
- Priority level display
- Support information

**Status Indicators:**
- ⏲️ **Pending** - Awaiting initial review
- ⏳ **In Progress** - Being actively worked on
- ✓ **Resolved** - Completed
- ✗ **Rejected** - Cannot be processed

#### 4. **About & Help** (`pages/03_About_Help.py`)
Comprehensive information and support.

**Sections:**
1. **About System** - Mission, features, and service categories
2. **FAQ** - 10 common questions answered
3. **How to Use** - Step-by-step guides for each feature
4. **Contact & Support** - Support contact information and problem reporting

**Available Information:**
- System mission and principles
- Service categories (Healthcare, Education, Water, Roads, Electricity, Sanitation)
- Frequently asked questions
- Usage instructions with tips
- Contact methods
- Government resources and links

#### 5. **Admin Login** (`pages/04_Admin_Login.py`)
Government staff authentication portal.

**Features:**
- Secure login interface
- Demo credentials for testing
- Session management
- Clear security information
- Access control to admin dashboard

**Demo Credentials:**
```
Username: admin | Password: admin123
Username: manager | Password: manager123
```

#### 6. **Admin Dashboard** (`pages/04_Admin_Dashboard.py`)
Government staff management interface (requires login).

**Features:**
- Overall statistics and metrics
- Category breakdown with charts
- Priority distribution analysis
- Grievance filtering by status/category/priority
- Individual grievance management
- Status updates for grievances
- Notes addition for grievances
- Data export functionality
- Reports generation

**Dashboard Sections:**
- 📈 Statistics showing total, pending, in-progress, resolved counts
- 📂 Category breakdown chart
- 🎯 Priority distribution with color coding
- 📋 Grievance list with full management options
- 📥 Export and reporting tools

---

## 🚀 Getting Started

### Prerequisites
- Python 3.10+
- Virtual environment activated (.venv)
- Backend and frontend running

### Starting the Application

**Backend (API Server):**
```bash
cd backend
python -m uvicorn app.main:app --reload --port 8000
```

**Frontend (Multi-Page App):**
```bash
python -m streamlit run app_home.py
```

Then open http://localhost:8501 in your browser.

### First Time Users

1. **Navigate to Home Page**
   - View statistics and understand the system
   - Read the FAQ section
   - Learn about service categories

2. **Submit a Grievance**
   - Click "Submit Grievance" in sidebar
   - Fill in the form clearly
   - Save your Grievance ID immediately
   - Review the analysis and suggestions

3. **Track Your Grievance**
   - Click "Track Grievance" in sidebar
   - Enter your Grievance ID
   - Check status and any official updates
   - Review timeline of actions

4. **Get Help**
   - Click "About & Help" in sidebar
   - Browse FAQ or How to Use sections
   - Contact support if needed

---

## 📊 Data Structure

### Grievance Object
```json
{
  "id": "GR-7DIGIT",
  "title": "String",
  "description": "String",
  "location": "String (optional)",
  "category": "Healthcare|Education|Water Supply|Roads & Transport|Electricity|Sanitation",
  "priority": "High|Medium|Low",
  "status": "Pending|In Progress|Resolved",
  "suggested_schemes": ["Program 1", "Program 2"],
  "created_at": "ISO-8601 timestamp",
  "updated_at": "ISO-8601 timestamp",
  "notes": "String (admin only)",
  "analysis_metadata": {
    "confidence": 0.0-1.0,
    "explanation": {
      "category_detection": "String",
      "priority_reason": "String",
      "relevant_keywords": {"Category": count}
    }
  }
}
```

### API Endpoints

**Submit Grievance:**
```
POST /grievances/
Content-Type: application/json

{
  "title": "String",
  "description": "String",
  "location": "String (optional)"
}

Response: 200 OK
{
  "grievance": {Grievance Object},
  "analysis": {Analysis Details}
}
```

**Get Grievances:**
```
GET /grievances/?id=GR-123456
GET /grievances/

Response: 200 OK
{
  "grievances": [{Grievance Object}, ...],
  "total": Integer
}
```

**Get Statistics:**
```
GET /stats/

Response: 200 OK
{
  "total_grievances": Integer,
  "category_breakdown": {Category: count},
  "priority_breakdown": {Priority: count},
  "status_breakdown": {Status: count}
}
```

---

## 🎨 Design Principles

### Government-Grade
- Professional, serious interface
- Official government color scheme (#0066cc, #004499)
- Clear typography and hierarchy
- Comprehensive information architecture

### Citizen-Friendly
- Simple, non-technical language
- No registration or login required
- Clear instructions at every step
- Supportive and reassuring tone

### Accessible
- High color contrast for readability
- Clear navigation structure
- Responsive design
- Support information easily available

### Private & Fair
- No citizen login (simple access)
- Data protection reassurance
- Fair treatment emphasis
- Transparent process information

---

## 🔐 Security Notes

### Current Implementation (Development)
- Simple password authentication for admin
- Session management via Streamlit
- No HTTPS (development only)
- SQLite database

### Production Recommendations
1. **Authentication:**
   - Use enterprise authentication (Active Directory, OAuth, SAML)
   - Implement multi-factor authentication
   - Use LDAP for government systems

2. **Transport:**
   - Enable HTTPS/TLS everywhere
   - Use secure headers

3. **Data:**
   - Encrypt personal information
   - Use PostgreSQL instead of SQLite
   - Implement proper backup procedures

4. **Monitoring:**
   - Log all admin actions
   - Implement rate limiting
   - Monitor for suspicious activity

---

## 📱 Responsive Design

The application is designed to work on:
- Desktop browsers (recommended)
- Tablets (responsive layout)
- Mobile phones (simplified interface)

Best experience on:
- Chrome/Edge (recommended)
- Firefox
- Safari

---

## 🐛 Troubleshooting

### Frontend Not Loading
```
Error: Connection refused (http://localhost:8501)

Solution:
1. Check if frontend is running: streamlit run app_home.py
2. Check port 8501 is available
3. Check Python environment is activated
```

### Backend Connection Error
```
Error: Cannot connect to backend

Solution:
1. Check if backend is running: python -m uvicorn app.main:app --reload --port 8000
2. Check port 8000 is available
3. Check backend logs for errors
```

### Database Issues
```
Error: table has no column

Solution:
1. Delete backend/grievances.db
2. Backend will recreate schema automatically
3. Restart backend server
```

### Page Not Found
```
Error: Page not found

Solution:
1. Check pages/ directory has all files
2. Verify file names: 01_Submit_Grievance.py, 02_Track_Grievance.py, etc.
3. Restart Streamlit app
```

---

## 📞 Support

### For Citizens
- **FAQ:** Available in "About & Help" page
- **How to Use:** Step-by-step guides in "About & Help"
- **Email:** support@grievance-welfare.gov.in
- **Phone:** 1800-GRIEVANCE (toll-free)

### For Administrators
- **Admin Dashboard:** Manage all grievances
- **Data Export:** Generate reports and statistics
- **Status Updates:** Track grievance progress
- **Notes:** Add official comments to grievances

---

## 📈 System Statistics

The home page displays:
- **Total Grievances:** All submissions received
- **Pending:** Awaiting initial review
- **In Progress:** Being actively worked on
- **Resolved:** Successfully completed

Category breakdown shows distribution across:
1. Healthcare
2. Education
3. Water Supply
4. Roads & Transport
5. Electricity
6. Sanitation

---

## 🎯 Next Steps

### For Users
1. Submit your first grievance
2. Track it using the ID
3. Check for updates regularly
4. Contact support if needed

### For Administrators
1. Login to admin dashboard
2. Review pending grievances
3. Update status and add notes
4. Generate reports for management

### For Developers
1. Review backend API documentation
2. Check database schema (app/models.py)
3. Review ML engine logic (app/ml_engine.py)
4. Extend with new features as needed

---

## 📝 File Structure

```
citizen-grievance-welfare-ai/
├── app_home.py                 # Main entry point (home page)
├── pages/                      # Multi-page app directory
│   ├── 01_Submit_Grievance.py
│   ├── 02_Track_Grievance.py
│   ├── 03_About_Help.py
│   ├── 04_Admin_Login.py
│   └── 04_Admin_Dashboard.py
├── backend/
│   ├── app/
│   │   ├── main.py            # FastAPI application
│   │   ├── models.py          # Database models
│   │   ├── schemas.py         # Request/response schemas
│   │   ├── database.py        # Database configuration
│   │   └── ml_engine.py       # AI analysis engine
│   ├── requirements.txt
│   └── grievances.db          # SQLite database
└── frontend_streamlit.py       # Legacy single-page app (deprecated)
```

---

**Last Updated:** January 31, 2025  
**Version:** 2.0 (Multi-Page Application)  
**Status:** ✅ Production Ready (with production security recommendations)
