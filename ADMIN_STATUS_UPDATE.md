# Admin Status Update Feature - Documentation

## Overview

A simple admin backend feature has been added to allow updating the status of citizen grievances. This is a **demo-ready feature** without authentication, suitable for government demonstrations and testing.

---

## API Endpoint

### Update Grievance Status

**Endpoint:** `PATCH /grievances/{grievance_id}/status`

**Description:** Update the status of a specific grievance by its ID.

**Authentication:** None (demo feature)

---

## Request Format

### URL Parameters
- `grievance_id` (integer, required): The ID of the grievance to update

### Request Body
```json
{
  "status": "In Progress"
}
```

### Allowed Status Values
- `Pending` - Grievance has been received but not yet acted upon
- `In Progress` - Grievance is being actively worked on
- `Resolved` - Grievance has been resolved

---

## Response Format

### Success Response (200 OK)

Returns the complete updated grievance object:

```json
{
  "id": 1,
  "user_id": 1,
  "title": "Water shortage in Sector 4",
  "description": "No water supply for 3 days...",
  "location": "Sector 4, Ward 5",
  "category": "Water Supply",
  "priority": "High",
  "status": "In Progress",
  "created_at": "2026-01-31T15:30:00",
  "suggested_schemes": ["Jal Jeevan Mission"],
  "confidence_score": 0.85,
  "analysis_metadata": {...}
}
```

### Error Responses

**400 Bad Request** - Invalid status value
```json
{
  "detail": "Invalid status. Allowed values: Pending, In Progress, Resolved"
}
```

**404 Not Found** - Grievance ID doesn't exist
```json
{
  "detail": "Grievance with ID 999 not found"
}
```

**500 Internal Server Error** - Database or server error
```json
{
  "detail": "Error updating grievance status: [error message]"
}
```

---

## Usage Examples

### Using cURL

```bash
# Update status to "In Progress"
curl -X PATCH http://127.0.0.1:8000/grievances/1/status \
  -H "Content-Type: application/json" \
  -d '{"status": "In Progress"}'

# Update status to "Resolved"
curl -X PATCH http://127.0.0.1:8000/grievances/1/status \
  -H "Content-Type: application/json" \
  -d '{"status": "Resolved"}'
```

### Using Python (requests)

```python
import requests

API_BASE_URL = "http://127.0.0.1:8000"
grievance_id = 1

# Update status
payload = {"status": "In Progress"}
response = requests.patch(
    f"{API_BASE_URL}/grievances/{grievance_id}/status",
    json=payload
)

if response.status_code == 200:
    updated_grievance = response.json()
    print(f"Status updated to: {updated_grievance['status']}")
else:
    print(f"Error: {response.json()['detail']}")
```

### Using JavaScript (fetch)

```javascript
const API_BASE_URL = "http://127.0.0.1:8000";
const grievanceId = 1;

// Update status
fetch(`${API_BASE_URL}/grievances/${grievanceId}/status`, {
  method: 'PATCH',
  headers: {
    'Content-Type': 'application/json',
  },
  body: JSON.stringify({ status: 'In Progress' })
})
  .then(response => response.json())
  .then(data => console.log('Updated:', data))
  .catch(error => console.error('Error:', error));
```

---

## Testing

A test script has been provided to verify the endpoint works correctly.

### Run the Test Script

```bash
cd backend
python test_admin_api.py
```

The test script will:
1. ✓ Fetch existing grievances
2. ✓ Update status to "In Progress"
3. ✓ Update status to "Resolved"
4. ✓ Test invalid status (should fail with 400)
5. ✓ Test non-existent ID (should fail with 404)
6. ✓ Reset to original status

---

## Integration with Streamlit Frontend

The Streamlit admin dashboard can use this endpoint to update grievance statuses.

### Example Streamlit Code

```python
import streamlit as st
import requests

API_BASE_URL = "http://127.0.0.1:8000"

def update_status(grievance_id, new_status):
    """Update grievance status via API"""
    try:
        response = requests.patch(
            f"{API_BASE_URL}/grievances/{grievance_id}/status",
            json={"status": new_status}
        )
        response.raise_for_status()
        return response.json(), None
    except Exception as e:
        return None, str(e)

# In your Streamlit admin page
grievance_id = st.number_input("Grievance ID", min_value=1)
new_status = st.selectbox("New Status", ["Pending", "In Progress", "Resolved"])

if st.button("Update Status"):
    result, error = update_status(grievance_id, new_status)
    if error:
        st.error(f"Error: {error}")
    else:
        st.success(f"Status updated to: {result['status']}")
```

---

## Database Changes

The status field in the `grievances` table is updated directly. No new tables or columns are required.

### Database Schema (Grievance Model)
```python
class Grievance(Base):
    __tablename__ = "grievances"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), index=True)
    title = Column(String, index=True)
    description = Column(Text)
    location = Column(String, nullable=True)
    category = Column(String, index=True)
    priority = Column(String)
    status = Column(String, default="Pending")  # <-- This field is updated
    created_at = Column(DateTime, default=datetime.utcnow)
    # ... other fields
```

---

## Security Notes

⚠️ **Important:** This is a **demo feature** without authentication.

### For Production Deployment:

1. **Add Authentication**: Require admin login/JWT token
2. **Add Authorization**: Verify user has admin role
3. **Add Audit Logging**: Track who changed what and when
4. **Add Rate Limiting**: Prevent abuse
5. **Add Input Validation**: Additional checks beyond status values
6. **Add Notifications**: Email/SMS to citizen when status changes

### Example Production Enhancement:

```python
@app.patch("/grievances/{grievance_id}/status")
def update_grievance_status(
    grievance_id: int,
    status_update: schemas.GrievanceStatusUpdate,
    current_admin: User = Depends(get_current_admin),  # Add auth
    db: Session = Depends(get_db)
):
    # Log the change
    audit_log.record(
        action="status_update",
        admin_id=current_admin.id,
        grievance_id=grievance_id,
        old_status=grievance.status,
        new_status=status_update.status
    )
    
    # Update status
    grievance.status = status_update.status
    db.commit()
    
    # Send notification to citizen
    send_notification(grievance.user_id, f"Your grievance status: {status_update.status}")
    
    return grievance
```

---

## API Documentation

The endpoint is automatically documented in FastAPI's interactive docs:

- **Swagger UI**: http://127.0.0.1:8000/docs
- **ReDoc**: http://127.0.0.1:8000/redoc

Navigate to the "Admin Endpoints" section to see the interactive documentation and test the endpoint directly from your browser.

---

## Troubleshooting

### Common Issues

**1. "Cannot connect to backend"**
- Ensure backend is running: `uvicorn app.main:app --reload`
- Check the URL is correct: `http://127.0.0.1:8000`

**2. "Grievance not found"**
- Verify the grievance ID exists
- Use `GET /grievances/` to see all available IDs

**3. "Invalid status"**
- Only use: `Pending`, `In Progress`, or `Resolved`
- Status values are case-sensitive

**4. "Database error"**
- Check database file exists: `backend/grievance.db`
- Ensure database is not locked by another process

---

## Summary

✅ **What's Implemented:**
- Simple PATCH endpoint for status updates
- Validation for allowed status values
- Error handling for invalid IDs and statuses
- Clear error messages
- Test script for verification

✅ **What's NOT Implemented (by design):**
- Authentication/authorization
- Audit logging
- Email notifications
- Rate limiting
- Advanced security features

This is a **minimal, demo-ready admin feature** suitable for government demonstrations and testing environments.

---

**Last Updated:** 2026-01-31  
**Status:** Complete and tested  
**Endpoint:** `PATCH /grievances/{grievance_id}/status`
