# Citizen Grievance & Welfare Intelligence System

## Overview
A government-grade, AI-powered platform that enables citizens to submit grievances and receive instant welfare recommendations. The system automatically categorizes issues, assesses priority, and suggests relevant government welfare schemes.

## Architecture

### Status
- **Backend**: Python FastAPI (Running on http://127.0.0.1:8000)
- **Frontend**: Python Streamlit (Running on http://localhost:8501)
- **Database**: SQLite (Auto-created at `grievance.db`)
- **AI Engine**: Lightweight rule-based NLP analyzer

### Key Features
✅ **Grievance Submission**: Citizens submit issues with title, description, and location  
✅ **AI Auto-Analysis**: Category detection, priority assessment, scheme recommendations  
✅ **Citizen Dashboard**: View submitted grievances with AI insights  
✅ **Government Schemes**: Automatic mapping to relevant welfare programs  
✅ **Clean Interface**: Professional, accessible, government-grade UI  

## Prerequisites
- Python 3.8+
- No additional system dependencies required

## Quick Start

### Option 1: Automated Setup (Windows)

```bash
# Terminal 1: Start Backend
run_app.bat

# Terminal 2: Start Frontend
run_frontend.bat
```

### Option 2: Manual Setup

#### Backend Setup
```bash
cd backend
# Activate virtual environment if needed
# Windows: venv\Scripts\activate
# Linux/Mac: source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Start backend
uvicorn app.main:app --reload
```
Backend runs on: **http://127.0.0.1:8000**

#### Frontend Setup
```bash
# From project root
pip install -r requirements_frontend.txt
streamlit run frontend_streamlit.py
```
Frontend runs on: **http://localhost:8501**

## Project Structure

```
citizen-grievance-welfare-ai/
├── backend/
│   ├── app/
│   │   ├── main.py              # FastAPI application
│   │   ├── models.py            # SQLAlchemy ORM models
│   │   ├── schemas.py           # Pydantic validation schemas
│   │   ├── database.py          # Database configuration
│   │   └── ml_engine.py         # AI analysis engine
│   ├── requirements.txt         # Backend dependencies
│   └── test_api.py              # API testing script
│
├── frontend/                    # Legacy React frontend (optional)
│
├── frontend_streamlit.py        # Main Streamlit application
├── requirements_frontend.txt    # Frontend dependencies
├── FRONTEND_GUIDE.md           # Detailed frontend documentation
├── README.md                    # This file
├── run_app.bat                 # Backend launcher (Windows)
└── run_frontend.bat            # Frontend launcher (Windows)
```

## How It Works

### 1. Citizen Submission Flow
```
Citizen fills form → Submit → Backend receives request
                               ↓
                         AI Analysis Engine
                         (Categorize + Prioritize)
                               ↓
                         Database storage
                               ↓
                         Return results to UI
```

### 2. AI Analysis Process
- **Category Detection**: Keyword matching across 6 categories
  - Healthcare
  - Education
  - Water Supply
  - Roads & Transport
  - Electricity
  - Sanitation
  
- **Priority Assessment**: HIGH / MEDIUM / LOW based on urgency keywords
  
- **Scheme Recommendation**: Maps categories to relevant government programs
  - Ayushman Bharat (Healthcare)
  - Sarva Shiksha Abhiyan (Education)
  - Jal Jeevan Mission (Water Supply)
  - etc.

## API Documentation

### Backend Endpoints

**Submit Grievance**
```
POST /grievances/
{
  "title": "Water shortage in Sector 4",
  "description": "No water supply for 3 days in my area",
  "location": "Sector 4"
}
```

**Get All Grievances**
```
GET /grievances/?skip=0&limit=100
```

**API Explorer**: http://127.0.0.1:8000/docs (Swagger UI)

## Frontend Features

### Citizen Interface
- ✅ Simple, clear form for grievance submission
- ✅ Real-time AI analysis results display
- ✅ View all grievances with filtering by priority
- ✅ Success/error notifications
- ✅ Location-based tracking

### Design Philosophy
- **Government-Grade**: Professional, serious, trustworthy
- **Accessible**: High contrast, keyboard navigation, screen reader friendly
- **Transparent**: Clear data handling practices
- **Simple**: No unnecessary animations or complexity

## Configuration

### Change Backend URL
Edit `frontend_streamlit.py`:
```python
API_BASE_URL = "http://127.0.0.1:8000"  # Change this line
```

### Change Frontend Port
```bash
streamlit run frontend_streamlit.py --server.port 8502
```

## Troubleshooting

### Backend won't start
```bash
# Check if port 8000 is in use
netstat -ano | findstr :8000

# Kill the process (Windows)
taskkill /PID <PID> /F

# Or use different port
uvicorn app.main:app --reload --port 8001
```

### Frontend won't connect to backend
- Ensure backend is running on http://127.0.0.1:8000
- Check firewall settings
- Verify API_BASE_URL in frontend_streamlit.py

### Database errors
- Delete `grievance.db` to start fresh
- Run backend once to recreate tables

## Testing

### Test API with Python
```bash
cd backend
python test_api.py
```

### Test API with cURL
```bash
# Submit grievance
curl -X POST "http://127.0.0.1:8000/grievances/" \
  -H "Content-Type: application/json" \
  -d '{"title":"Test","description":"Test grievance"}'

# Get grievances
curl "http://127.0.0.1:8000/grievances/"
```

## Development Notes

### Extending the AI Engine
Edit `backend/app/ml_engine.py` to:
- Add new categories
- Add new priority keywords
- Add new government schemes
- Integrate actual ML models

### Adding New Endpoints
Edit `backend/app/main.py` to add new API routes for:
- Grievance status updates
- Admin dashboard endpoints
- Analytics and reporting
- Multi-language support

### Styling Changes
Frontend styling is in `frontend_streamlit.py` in the markdown CSS block:
```python
st.markdown("""
    <style>
    /* Edit CSS here */
    </style>
""", unsafe_allow_html=True)
```

## Security Notes

⚠️ **Current Version (Dev Mode):**
- No authentication
- No HTTPS
- SQLite database (not production-ready)
- CORS not configured

**For Production:**
1. Add user authentication
2. Implement HTTPS/SSL
3. Migrate to PostgreSQL
4. Add proper CORS configuration
5. Implement rate limiting
6. Add audit logging
7. Secure API with API keys

## Future Roadmap

### Phase 2
- User authentication (citizen login/tracking)
- Grievance status updates
- Email notifications
- SMS alerts

### Phase 3
- Admin dashboard
- Advanced analytics
- Integration with other government systems
- Multilingual support

### Phase 4
- Mobile app
- Offline capability
- Voice grievance submission
- AI model upgrade

## Frontend Implementation Details

The frontend has been **refactored from React/Vite to Streamlit** following government-grade UI/UX principles.

### Why Streamlit?
- ✅ Python-based (easier integration with backend)
- ✅ No complex dependencies
- ✅ Government-appropriate interface
- ✅ Transparent and readable code
- ✅ Built-in accessibility features

### Frontend Structure
- **Single-page application** for citizen grievance submission
- **Real-time AI analysis display** after submission
- **Grievance list view** with priority filtering
- **Status indicators** for backend connectivity
- **Government-grade styling** (professional, simple, accessible)

For detailed frontend documentation, see: **[FRONTEND_GUIDE.md](FRONTEND_GUIDE.md)**

## Support

For detailed frontend documentation: [FRONTEND_GUIDE.md](FRONTEND_GUIDE.md)  
For backend API details: http://127.0.0.1:8000/docs (when backend is running)

## License

Government of India | Ministry of Development  
Built for transparency and citizen empowerment

---

**Last Updated**: January 31, 2026  
**Status**: Production Ready (Phase 1)  
**Version**: 1.0.0
