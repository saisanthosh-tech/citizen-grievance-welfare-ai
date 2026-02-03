# 🚀 Setup Instructions for Your Teammate

After cloning the repository, follow these steps:

---

## Step 1: Clone the Repository (Already Done)

```bash
git clone https://github.com/saisanthosh-tech/citizen-grievance-welfare-ai.git
cd citizen-grievance-welfare-ai
```

---

## Step 2: Install Dependencies

Run these commands in order:

```bash
# Install backend dependencies
pip install -r backend/requirements.txt

# Install frontend dependencies
pip install -r requirements_frontend.txt

# Download AI model (REQUIRED - one-time setup)
python -m spacy download en_core_web_sm
```

**Wait for all installations to complete** (~2-5 minutes depending on internet speed)

---

## Step 3: Run the Project

### Option A: Quick Start (Windows - Recommended)

```bash
.\run_demo.bat
```

This will start both servers automatically!

### Option B: Manual Start (Any OS)

**Open 2 terminals:**

**Terminal 1 - Backend:**
```bash
cd backend
uvicorn app.main_demo:app --reload --host 127.0.0.1 --port 8000
```

**Terminal 2 - Frontend:**
```bash
python -m streamlit run app_home.py
```

---

## Step 4: Access the Application

Once the servers are running, open these URLs in your browser:

### 🌐 Main Application URLs

1. **Frontend (Streamlit UI)**  
   👉 http://localhost:8501
   - This is the main user interface
   - Use this to interact with the system

2. **Backend API**  
   👉 http://127.0.0.1:8000
   - This is the REST API server
   - Shows basic system info

3. **API Documentation (Interactive)**  
   👉 http://127.0.0.1:8000/docs
   - Full API documentation
   - Test API endpoints directly

---

## ✅ Verify Everything is Working

### Check 1: Backend is Running
- Open: http://127.0.0.1:8000
- You should see: System information JSON

### Check 2: API Docs are Accessible
- Open: http://127.0.0.1:8000/docs
- You should see: FastAPI documentation page

### Check 3: Frontend is Running
- Open: http://localhost:8501
- You should see: Home page with language selector

### Check 4: Test Language Switching
- Look at the sidebar
- You should see 4 language buttons:
  - 🇬🇧 English
  - 🇮🇳 हिंदी
  - 🇮🇳 తెలుగు
  - 🇮🇳 தமிழ்
- Click each button to test

---

## 🎯 Quick Test

1. **Submit a Grievance:**
   - Click "Submit Grievance"
   - Fill in the form
   - Submit and see AI analysis

2. **Track Grievance:**
   - Note the Grievance ID
   - Click "Track Grievance"
   - Enter the ID to see details

3. **View Analytics:**
   - Click "Analytics Dashboard"
   - See statistics and charts

---

## 🔧 Troubleshooting

### Problem: "Module not found" error

**Solution:**
```bash
pip install -r backend/requirements.txt
pip install -r requirements_frontend.txt
```

### Problem: "spaCy model not found"

**Solution:**
```bash
python -m spacy download en_core_web_sm
```

### Problem: "Port already in use"

**Solution:** Kill the process or use different ports:
```bash
# Backend on different port
uvicorn app.main_demo:app --reload --host 127.0.0.1 --port 8001

# Frontend on different port
streamlit run app_home.py --server.port 8502
```

### Problem: "Cannot connect to backend"

**Solution:**
1. Make sure backend is running on port 8000
2. Check: http://127.0.0.1:8000
3. Look for errors in the backend terminal

---

## 📋 Complete Command Summary

Copy and paste these commands in order:

```bash
# 1. Navigate to project
cd citizen-grievance-welfare-ai

# 2. Install backend dependencies
pip install -r backend/requirements.txt

# 3. Install frontend dependencies
pip install -r requirements_frontend.txt

# 4. Download AI model
python -m spacy download en_core_web_sm

# 5. Run the project
.\run_demo.bat
```

Then open: **http://localhost:8501**

---

## 🌐 URLs Quick Reference

| Service | URL | Purpose |
|---------|-----|---------|
| **Frontend** | http://localhost:8501 | Main UI - Use this! |
| **Backend** | http://127.0.0.1:8000 | API Server |
| **API Docs** | http://127.0.0.1:8000/docs | Test APIs |

---

## ⏱️ Expected Setup Time

- **Installation**: 2-5 minutes
- **First Run**: 30 seconds
- **Total**: ~5-10 minutes

---

## ✨ Features to Test

1. ✅ Multi-language support (4 languages)
2. ✅ Submit grievances
3. ✅ AI auto-categorization
4. ✅ Track grievances
5. ✅ Admin dashboard
6. ✅ Analytics dashboard
7. ✅ GPS map view

---

**That's it! Your teammate is ready to run the project!** 🎉
