# Frontend Implementation Guide

## Overview

The frontend has been **refactored from React/Vite to Streamlit**, following government-grade UI/UX principles.

### Why Streamlit?

✅ **Python-based**: Easier to maintain and extend with the backend  
✅ **No complex dependencies**: Simple, readable, and transparent code  
✅ **Government-appropriate**: Clean, serious, professional interface  
✅ **Rapid development**: Focus on functionality over styling  
✅ **Accessibility**: Built-in support for screen readers and keyboard navigation  

---

## Frontend Architecture

### File Structure
```
frontend_streamlit.py          # Main Streamlit application
requirements_frontend.txt      # Python dependencies for frontend
```

### Technology Stack
- **Framework**: Streamlit 1.31.1
- **HTTP Client**: Requests 2.31.0
- **Backend Communication**: REST API (HTTP)
- **Styling**: Custom CSS (inline, government-grade design)

---

## Setup Instructions

### 1. **Install Frontend Dependencies**

```bash
# From the project root directory
pip install -r requirements_frontend.txt
```

Or manually:
```bash
pip install streamlit==1.31.1 requests==2.31.0
```

### 2. **Ensure Backend is Running**

Before starting the frontend, the backend must be active:

```bash
cd backend
python -m uvicorn app.main:app --reload
# Backend will run on http://127.0.0.1:8000
```

### 3. **Start the Frontend**

```bash
# From the project root directory
streamlit run frontend_streamlit.py
```

The frontend will be available at: **http://localhost:8501**

---

## User Interface

### Landing Page

**Header Section:**
- Government logo and system title
- Clear value proposition
- Link to backend API status

**Information Box:**
- Step-by-step workflow explanation
- Trust and transparency messaging
- Data handling assurances

### Main Form Section

**Citizen Submission Panel:**
- **Grievance Title** (required)
  - Minimum 5 characters
  - Clear, descriptive title
  
- **Detailed Description** (required)
  - Text area with 150px height
  - Minimum 20 characters
  - Placeholder with guiding questions
  
- **Location/Address** (optional)
  - Helps with geographic analysis
  - Not required but recommended

**Submit Button:**
- Clear, prominent primary action
- Loading state with spinner
- Input validation before submission

### Results Display

After successful submission, users see:

1. **Success Confirmation**
   - Green success message
   - Visual feedback

2. **AI Analysis Results**
   - **Category**: Color-coded badge (Healthcare, Education, Water Supply, etc.)
   - **Priority Level**: Color-coded (High=Red, Medium=Yellow, Low=Green)
   - **Suggested Schemes**: List of relevant government welfare programs

3. **Submission Summary**
   - Title, description, location, timestamp
   - Reference for citizen records

### View All Grievances Section

- **Grievance Statistics**
  - Total count
  - Priority distribution (metrics cards)
  
- **Grievance Table**
  - Latest 10 grievances
  - Columns: Title, Category, Priority, Status, Created Date
  - Sortable and searchable (Streamlit native)

### Sidebar Information

- Citizen guidelines for better submissions
- System status indicator
- Backend connection status
- Last check timestamp

---

## API Integration

### Backend Endpoints Used

#### Submit Grievance
```
POST /grievances/
Content-Type: application/json

Request Body:
{
  "title": "string",
  "description": "string",
  "location": "string (optional)"
}

Response:
{
  "id": integer,
  "title": "string",
  "description": "string",
  "location": "string",
  "category": "string",
  "priority": "string",
  "status": "string",
  "suggested_schemes": ["string"],
  "created_at": "datetime"
}
```

#### Get All Grievances
```
GET /grievances/?skip=0&limit=100

Response:
[
  {
    "id": integer,
    "title": "string",
    "description": "string",
    "location": "string",
    "category": "string",
    "priority": "string",
    "status": "string",
    "suggested_schemes": ["string"],
    "created_at": "datetime"
  }
]
```

---

## Design Philosophy

### Government-Grade UI Principles

1. **Clarity Over Decoration**
   - No unnecessary animations
   - Clear typography hierarchy
   - Consistent color scheme (blue = official, red = urgent, green = positive)

2. **Accessibility**
   - Semantic HTML
   - High contrast text
   - Keyboard navigation support
   - Screen reader friendly

3. **Trust & Transparency**
   - Clear messaging about data handling
   - No hidden operations
   - Explicit success/error states
   - System status indicators

4. **Simplicity**
   - One primary action per section
   - Minimal form fields
   - Straightforward workflow
   - Clear instructions

### Color Scheme

- **Primary Blue (#0066cc)**: Headers, important elements, official information
- **Success Green (#28a745)**: Positive actions, low priority
- **Warning Yellow (#ffc107)**: Medium priority, caution
- **Danger Red (#dc3545)**: High priority, errors
- **Neutral Gray (#555)**: Secondary text
- **Background White (#ffffff)**: Content areas

---

## Error Handling

### Network Errors
- **Connection Error**: "Cannot connect to the backend service. Please ensure the backend is running."
- **Timeout Error**: "Backend service is not responding. Please try again."
- **HTTP Errors**: Specific error messages from backend

### Form Validation
- Minimum title length: 5 characters
- Minimum description length: 20 characters
- Required fields highlighted
- Errors shown before submission attempt

### User Feedback
- Green success alert on submission
- Red error alerts for failures
- Loading spinner during processing
- Clear timestamps for all actions

---

## Deployment Considerations

### For Production Government Use

1. **HTTPS/SSL Certificate**
   - Use Streamlit Cloud with SSL enabled
   - Or deploy with nginx/Apache reverse proxy

2. **Backend API Configuration**
   - Change `API_BASE_URL` to production URL
   - Implement proper CORS headers
   - Use environment variables for configuration

3. **Data Persistence**
   - Ensure SQLite database is on persistent storage
   - Or migrate to PostgreSQL for multi-server setup

4. **Rate Limiting**
   - Implement rate limiting on backend
   - Prevent spam submissions

5. **Audit Logging**
   - Log all submissions
   - Track user activities
   - Comply with government data retention policies

6. **Performance**
   - Cache grievance list (5-minute TTL)
   - Implement pagination properly
   - Optimize database queries

---

## Development Workflow

### Making Changes

1. **Backend Changes**
   ```bash
   cd backend
   # Make changes to models, schemas, or main.py
   # Backend auto-reloads with --reload flag
   ```

2. **Frontend Changes**
   ```bash
   # Edit frontend_streamlit.py
   # Streamlit auto-refreshes on save
   ```

3. **Testing Changes**
   - Use browser dev tools for debugging
   - Check terminal output for Streamlit logs
   - Verify backend responses in browser network tab

### Common Modifications

**Change API URL:**
```python
API_BASE_URL = "http://127.0.0.1:8000"  # Edit this line
```

**Add New Form Fields:**
```python
new_field = st.text_input("Label", help="Help text")
# Add to payload before submission
```

**Customize Colors:**
Edit the CSS in the markdown style block at the top of the file.

**Add Admin Dashboard:**
Create a separate `admin_dashboard.py` and use Streamlit multi-page apps.

---

## Performance Notes

- Initial load: ~2 seconds
- Form submission: ~1-2 seconds (depends on backend AI analysis)
- Grievance list refresh: ~1 second
- Frontend is stateless (all data from backend)

---

## Troubleshooting

### Issue: "Cannot connect to backend"
**Solution**: Ensure backend is running on http://127.0.0.1:8000
```bash
cd backend
python -m uvicorn app.main:app --reload
```

### Issue: Forms not submitting
**Solution**: Check browser console for error messages. Verify backend URL in code.

### Issue: Streamlit not auto-refreshing
**Solution**: Save the file again. If still not working, restart Streamlit server.

### Issue: Port already in use
**Solution**: Use different port:
```bash
streamlit run frontend_streamlit.py --server.port 8502
```

---

## Future Enhancements

### Phase 2
- User authentication (citizen login)
- Grievance tracking with unique ID
- Email notifications

### Phase 3
- Admin dashboard for monitoring
- Advanced filtering and analytics
- Integration with other government systems

### Phase 4
- Mobile app version
- Multilingual support
- Accessibility improvements
- Offline capability

---

## Support & Maintenance

For issues or questions:
1. Check backend logs: `backend/app/main.py`
2. Check frontend logs: Streamlit console output
3. Verify API endpoints: Open http://127.0.0.1:8000/docs (FastAPI Swagger UI)

---

**Last Updated**: January 31, 2026  
**Status**: Production Ready  
**Version**: 1.0
