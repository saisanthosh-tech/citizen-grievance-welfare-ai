# 🏛️ Citizen Grievance & Welfare Intelligence System - Backend Guide

## Overview

This is a **government-grade backend** for managing citizen grievances with explainable AI analysis. The system is designed for:
- ✅ Government reliability and transparency
- ✅ Simple, explainable logic (no black-box AI)
- ✅ Secure data handling
- ✅ Scalable administration

---

## Architecture

### Technology Stack
- **Framework**: FastAPI (modern, fast, production-ready)
- **Database**: SQLite (portable, secure)
- **AI Engine**: Keyword-based rules (explainable)
- **Server**: Uvicorn (ASGI application server)

### Directory Structure
```
backend/
├── app/
│   ├── main.py           # FastAPI application & endpoints
│   ├── models.py         # SQLAlchemy database models
│   ├── schemas.py        # Pydantic request/response schemas
│   ├── database.py       # Database configuration
│   ├── ml_engine.py      # AI analysis engine (explainable)
│   └── __pycache__/      # Compiled Python files
├── requirements.txt      # Python dependencies
└── test_api.py          # API testing script
```

---

## Core Components

### 1. **Main Application** (`app/main.py`)

#### Endpoints

##### `GET /`
Welcome endpoint with system information.
```json
{
  "system": "Citizen Grievance & Welfare Intelligence System",
  "version": "1.0.0",
  "status": "operational",
  "endpoints": {
    "submit_grievance": "POST /grievances/",
    "view_grievances": "GET /grievances/",
    "get_statistics": "GET /stats/"
  }
}
```

##### `POST /grievances/`
**Submit a citizen grievance with AI analysis**

Request:
```json
{
  "title": "Water shortage in Sector 4",
  "description": "There has been no water supply for 3 days. This is urgent.",
  "location": "Ward No. 5, Sector 4"
}
```

Response:
```json
{
  "grievance": {
    "id": 1,
    "title": "Water shortage in Sector 4",
    "description": "There has been no water supply for 3 days...",
    "location": "Ward No. 5, Sector 4",
    "category": "Water Supply",
    "priority": "High",
    "status": "Pending",
    "suggested_schemes": ["Jal Jeevan Mission", "Atal Bhujal Yojana"],
    "confidence_score": 0.95,
    "analysis_metadata": {
      "category_detection": "Matched 3 keyword(s) in 'Water Supply' category",
      "confidence": "95%",
      "priority_reason": "High urgency keywords detected: urgent, shortage",
      "relevant_keywords": {
        "Water Supply": 3,
        "Healthcare": 0,
        "Education": 0
      }
    },
    "created_at": "2026-01-31T10:30:00"
  },
  "analysis": {
    "category": "Water Supply",
    "priority": "High",
    "confidence": 0.95,
    "explanation": {
      "category_detection": "Matched 3 keyword(s) in 'Water Supply' category",
      "confidence": "95%",
      "priority_reason": "High urgency keywords detected: urgent, shortage",
      "relevant_keywords": {
        "Water Supply": 3,
        "Healthcare": 0,
        "Education": 0
      }
    }
  },
  "message": "Your grievance has been received and will be processed fairly."
}
```

**Input Validation:**
- Title: minimum 5 characters
- Description: minimum 20 characters
- Location: optional but recommended

##### `GET /grievances/`
**Retrieve grievances with filtering and pagination**

Parameters:
- `skip`: Number of records to skip (default: 0)
- `limit`: Maximum records to return (default: 100, max: 100)
- `category`: Filter by category (e.g., "Water Supply", "Healthcare")
- `priority`: Filter by priority ("High", "Medium", "Low")

Example: `GET /grievances/?category=Water%20Supply&priority=High&limit=10`

Response:
```json
{
  "total": 45,
  "count": 10,
  "skip": 0,
  "limit": 10,
  "grievances": [...],
  "message": "Successfully retrieved 10 grievance(s) from 45 total"
}
```

##### `GET /stats/`
**Get aggregated statistics for analytics**

Response:
```json
{
  "total_grievances": 45,
  "by_category": {
    "Water Supply": 15,
    "Healthcare": 12,
    "Education": 10,
    "Roads & Transport": 5,
    "Electricity": 2,
    "Sanitation": 1
  },
  "by_priority": {
    "High": 12,
    "Medium": 28,
    "Low": 5
  },
  "average_confidence_score": 0.82,
  "message": "Statistics calculated successfully"
}
```

---

### 2. **ML Engine** (`app/ml_engine.py`)

The AI engine uses **explainable, keyword-based logic** for analyzing grievances.

#### How it Works

##### Step 1: Category Detection
- **Method**: Keyword matching across 6 categories
- **Categories**:
  - Healthcare: hospital, doctor, medicine, clinic, treatment
  - Education: school, teacher, student, books, exam
  - Water Supply: water, leak, pipe, shortage, dirty
  - Roads & Transport: road, pothole, bus, traffic, street
  - Electricity: power, outage, voltage, wire, pole
  - Sanitation: garbage, trash, waste, clean, drain

**Logic**: Counts keyword matches in grievance text. Category with most matches wins.

##### Step 2: Priority Detection
- **Method**: Keyword-based urgency detection
- **High**: urgent, immediate, emergency, severe, danger, accident
- **Low**: minor, suggestion, feedback, delay
- **Default**: Medium (if neither High nor Low keywords found)

##### Step 3: Confidence Scoring
- **Formula**: `confidence = min(1.0, matching_keywords / 3.0)`
- **Range**: 0.0 to 1.0
- **Meaning**: More keyword matches = higher confidence in categorization

##### Step 4: Scheme Recommendation
- **Logic**: Based on detected category, suggest relevant government schemes
- **Example**: Water Supply → ["Jal Jeevan Mission", "Atal Bhujal Yojana"]

#### Example Analysis

Input: "There's no electricity for 5 days, urgent"

1. **Keywords found**: "electricity" (1), "urgent" (1)
2. **Category**: Electricity (matches: 1)
3. **Priority**: High (urgent keyword found)
4. **Confidence**: 33% (1 keyword / 3)
5. **Schemes**: ["Saubhagya Scheme", "Deen Dayal Upadhyaya Gram Jyoti Yojana"]
6. **Explanation**: Clear reasoning for each decision

---

### 3. **Data Models** (`app/models.py`)

#### Grievance Table
```python
id              : Primary Key
title           : Grievance subject (indexed)
description     : Detailed description
location        : Optional citizen location
category        : Detected category (indexed)
priority        : High/Medium/Low
status          : Pending/In Progress/Resolved
created_at      : Timestamp
suggested_schemes : JSON array of relevant schemes
confidence_score : 0.0 to 1.0 (AI confidence)
analysis_metadata: JSON with analysis explanation
```

---

### 4. **Request/Response Schemas** (`app/schemas.py`)

All requests and responses are validated using Pydantic.

**GrievanceCreate**: Request schema
- `title` (str, required): 5+ characters
- `description` (str, required): 20+ characters  
- `location` (str, optional): Citizen location

**GrievanceResponse**: Includes analysis explanation
**GrievanceListResponse**: Paginated list with metadata
**StatisticsResponse**: Aggregated analytics

---

## Running the Backend

### Start the Server
```bash
cd backend
python -m uvicorn app.main:app --reload --port 8000
```

### Access API Documentation
- **Interactive API Docs**: http://localhost:8000/docs (Swagger UI)
- **Alternative Docs**: http://localhost:8000/redoc (ReDoc)

### Test an Endpoint
```bash
curl -X POST "http://localhost:8000/grievances/" \
  -H "Content-Type: application/json" \
  -d '{
    "title": "Pothole on Main Street",
    "description": "There is a large pothole causing accidents on Main Street near the market",
    "location": "Main Street, Market Area"
  }'
```

---

## Key Design Principles

### 1. **Government-Grade Reliability**
- ✅ Clear error messages
- ✅ Input validation
- ✅ Graceful error handling
- ✅ Pagination limits (max 100 records)

### 2. **Explainability**
- ✅ Every classification includes reasoning
- ✅ Confidence scores show AI certainty
- ✅ Keyword matches are transparent
- ✅ No black-box algorithms

### 3. **Fairness & Transparency**
- ✅ Rule-based logic (no hidden patterns)
- ✅ All grievances treated systematically
- ✅ Clear priority criteria
- ✅ Reproducible results

### 4. **Data Security**
- ✅ Secure database storage
- ✅ Input validation prevents SQL injection
- ✅ Error responses don't leak sensitive data

---

## Database Management

### Creating Database
The database is created automatically on first run.

```bash
# Database file location
backend/grievances.db
```

### Database Schema
```sql
CREATE TABLE grievances (
    id INTEGER PRIMARY KEY,
    title VARCHAR NOT NULL,
    description TEXT NOT NULL,
    location VARCHAR,
    category VARCHAR NOT NULL,
    priority VARCHAR NOT NULL,
    status VARCHAR DEFAULT 'Pending',
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    confidence_score FLOAT,
    analysis_metadata JSON
);
```

### Querying Data
```python
from app.database import SessionLocal
from app import models

db = SessionLocal()
grievances = db.query(models.Grievance).filter(
    models.Grievance.priority == "High"
).all()
```

---

## API Response Structure

### Success Response
```json
{
  "grievance": {...},
  "analysis": {...},
  "message": "Your grievance has been received..."
}
```

### Error Response
```json
{
  "detail": "Description must be at least 20 characters"
}
```

HTTP Status Codes:
- `200`: OK - Successful request
- `201`: Created - Grievance submitted
- `400`: Bad Request - Invalid input
- `500`: Server Error - Internal issue

---

## Deployment Checklist

- [ ] Install all dependencies: `pip install -r requirements.txt`
- [ ] Start backend server: `python -m uvicorn app.main:app --port 8000`
- [ ] Test API endpoints
- [ ] Ensure frontend can connect to backend
- [ ] Monitor database size
- [ ] Set up log rotation for production
- [ ] Enable HTTPS for production
- [ ] Set up regular backups of database

---

## Future Enhancements

1. **Authentication**: Add JWT tokens for secure access
2. **Advanced NLP**: Integrate more sophisticated text analysis
3. **Real-time Notifications**: WebSocket support for live updates
4. **Advanced Analytics**: Trends, patterns, predictive insights
5. **Multi-language Support**: Analyze grievances in multiple languages
6. **Admin Dashboard**: Management interface for staff

---

## Support & Documentation

- **API Docs**: http://localhost:8000/docs
- **GitHub**: [Repository URL]
- **Issues**: Report issues via GitHub Issues

---

**Built for transparency and citizen empowerment** 🇮🇳
