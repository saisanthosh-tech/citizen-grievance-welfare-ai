# Citizen Grievance & Welfare Intelligence System

## Status
- **Backend**: Python FastAPI (Running on http://127.0.0.1:8000)
- **Frontend**: React + Vite (Code ready, needs dependency installation)
- **Database**: SQLite (Auto-created)

## Prerequisites
- Python 3.8+
- Node.js 16+

## Setup Instructions

### 1. Backend
The backend is already configured. To restart it:
```bash
cd backend
# Activate virtual env if not active
# Windows: venv\Scripts\activate
# Linux/Mac: source venv/bin/activate
pip install -r requirements.txt
uvicorn app.main:app --reload
```

### 2. Frontend
The frontend requires dependencies to be installed.
```bash
cd frontend
npm install
npm install axios lucide-react recharts
npm run dev
```

**Note**: If `npm install` fails, try:
```bash
npm cache clean --force
rm -rf node_modules package-lock.json
npm install
```

## Features Implemented
- **Grievance Submission API**: POST /grievances/
- **Grievance List API**: GET /grievances/
- **Admin Dashboard**: React UI to view and submit grievances.
- **Auto-Categorization**: (Placeholder in ML engine)
