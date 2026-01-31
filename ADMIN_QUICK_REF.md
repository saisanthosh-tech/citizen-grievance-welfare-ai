# Admin Status Update - Quick Reference

## 🎯 Quick Start

### Endpoint
```
PATCH /grievances/{grievance_id}/status
```

### Allowed Status Values
- `Pending`
- `In Progress`
- `Resolved`

---

## 📝 Quick Examples

### cURL
```bash
curl -X PATCH http://127.0.0.1:8000/grievances/1/status \
  -H "Content-Type: application/json" \
  -d '{"status": "In Progress"}'
```

### Python
```python
import requests

requests.patch(
    "http://127.0.0.1:8000/grievances/1/status",
    json={"status": "In Progress"}
)
```

### JavaScript
```javascript
fetch('http://127.0.0.1:8000/grievances/1/status', {
  method: 'PATCH',
  headers: {'Content-Type': 'application/json'},
  body: JSON.stringify({status: 'In Progress'})
})
```

---

## 🧪 Test the Feature

```bash
cd backend
python test_admin_api.py
```

---

## 📚 Full Documentation

See [ADMIN_STATUS_UPDATE.md](ADMIN_STATUS_UPDATE.md) for complete details.

---

## 🔍 Interactive API Docs

Visit: http://127.0.0.1:8000/docs

Look for the "Admin Endpoints" section.
