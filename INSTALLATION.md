# 🚀 Installation & Setup Guide

**Citizen Grievance & Welfare Intelligence System**

This guide will help you set up and run the project on a new machine after cloning from GitHub.

---

## 📋 Prerequisites

Before you begin, ensure you have the following installed:

1. **Python 3.8 or higher**
   - Download from: https://www.python.org/downloads/
   - Verify installation: `python --version`

2. **pip** (Python package manager)
   - Usually comes with Python
   - Verify installation: `pip --version`

3. **Git** (to clone the repository)
   - Download from: https://git-scm.com/downloads
   - Verify installation: `git --version`

---

## 📥 Step 1: Clone the Repository

```bash
git clone <your-repository-url>
cd citizen-grievance-welfare-ai
```

---

## 🔧 Step 2: Install Backend Dependencies

### Option A: Using the provided batch file (Windows)

```bash
.\install_fix.bat
```

### Option B: Manual installation

```bash
# Navigate to backend directory
cd backend

# Install all backend dependencies
pip install -r requirements.txt

# Download spaCy language model (required for NLP)
python -m spacy download en_core_web_sm

# Go back to root directory
cd ..
```

**Backend Dependencies** (from `backend/requirements.txt`):
- `fastapi` - Web framework for the API
- `uvicorn` - ASGI server
- `sqlalchemy` - Database ORM
- `pydantic` - Data validation
- `spacy` - Natural Language Processing
- `sentence-transformers` - AI embeddings
- `scikit-learn` - Machine learning utilities
- `python-multipart` - File upload support
- `requests` - HTTP client
- `numpy` - Numerical computing
- `pandas` - Data manipulation
- `passlib[bcrypt]` - Password hashing
- `python-jose[cryptography]` - JWT authentication

---

## 🎨 Step 3: Install Frontend (Streamlit) Dependencies

```bash
# Install Streamlit frontend dependencies
pip install -r requirements_frontend.txt
```

**Frontend Dependencies** (from `requirements_frontend.txt`):
- `streamlit==1.31.1` - Web UI framework
- `requests==2.31.0` - HTTP client for API calls
- `plotly` - Interactive charts
- `folium` - Map visualization
- `streamlit-folium` - Streamlit-Folium integration
- `pandas` - Data manipulation

---

## ⚙️ Step 4: Download Required AI Models

The system uses spaCy for Natural Language Processing. Download the English language model:

```bash
python -m spacy download en_core_web_sm
```

This is a **one-time setup** and is required for the AI analysis to work.

---

## 🗄️ Step 5: Database Setup

The system uses SQLite by default (no additional setup needed). The database file will be created automatically when you first run the backend.

**Database file location**: `backend/grievances.db`

> **Note**: For production, you can configure PostgreSQL. See `DEPLOYMENT_GUIDE.md` for details.

---

## 🚀 Step 6: Run the Application

### Option A: Using the Demo Batch File (Windows - Recommended)

```bash
.\run_demo.bat
```

This will:
- Start the backend API on http://127.0.0.1:8000
- Start the Streamlit frontend on http://localhost:8501
- Both servers run in the same terminal window

### Option B: Manual Start (Run in separate terminals)

**Terminal 1 - Backend:**
```bash
cd backend
uvicorn app.main_demo:app --reload --host 127.0.0.1 --port 8000
```

**Terminal 2 - Streamlit Frontend:**
```bash
python -m streamlit run app_home.py
```

---

## 🌐 Step 7: Access the Application

Once both servers are running:

- **Streamlit Frontend**: http://localhost:8501
- **Backend API**: http://127.0.0.1:8000
- **API Documentation**: http://127.0.0.1:8000/docs

---

## 📦 Complete Installation Commands (Quick Reference)

For someone cloning the repo for the first time, here's the complete sequence:

```bash
# 1. Clone repository
git clone <your-repository-url>
cd citizen-grievance-welfare-ai

# 2. Install backend dependencies
pip install -r backend/requirements.txt

# 3. Install frontend dependencies
pip install -r requirements_frontend.txt

# 4. Download spaCy language model
python -m spacy download en_core_web_sm

# 5. Run the application
.\run_demo.bat
```

---

## 🔍 Verify Installation

After installation, verify everything is working:

1. **Check Python version**:
   ```bash
   python --version
   # Should show Python 3.8 or higher
   ```

2. **Check installed packages**:
   ```bash
   pip list
   # Should show all packages from requirements files
   ```

3. **Check spaCy model**:
   ```bash
   python -m spacy validate
   # Should show en_core_web_sm is installed
   ```

4. **Test backend API**:
   - Open http://127.0.0.1:8000/docs
   - You should see the FastAPI documentation

5. **Test Streamlit frontend**:
   - Open http://localhost:8501
   - You should see the home page with language selector

---

## 🌍 Language Support

The system supports **4 languages**:
- 🇬🇧 English
- 🇮🇳 Hindi (हिंदी)
- 🇮🇳 Telugu (తెలుగు)
- 🇮🇳 Tamil (தமிழ்)

Language switching is available in the sidebar of the Streamlit app.

---

## 🛠️ Troubleshooting

### Issue: "Module not found" errors

**Solution**: Reinstall dependencies
```bash
pip install -r backend/requirements.txt
pip install -r requirements_frontend.txt
```

### Issue: "spaCy model not found"

**Solution**: Download the language model
```bash
python -m spacy download en_core_web_sm
```

### Issue: "Port already in use"

**Solution**: Kill the process using the port or use a different port
```bash
# For backend (port 8000)
uvicorn app.main_demo:app --reload --host 127.0.0.1 --port 8001

# For frontend (port 8501)
streamlit run app_home.py --server.port 8502
```

### Issue: "Cannot connect to backend"

**Solution**: Ensure backend is running
1. Check if backend is running on http://127.0.0.1:8000
2. Open http://127.0.0.1:8000/docs to verify
3. Check the terminal for error messages

### Issue: Statistics not loading

**Solution**: Ensure both backend and frontend are running
1. Backend must be running on port 8000
2. Frontend must be running on port 8501
3. Refresh the browser page

---

## 📁 Project Structure

```
citizen-grievance-welfare-ai/
├── backend/                    # FastAPI backend
│   ├── app/
│   │   ├── main_demo.py       # Demo API (no auth)
│   │   ├── main.py            # Production API (with auth)
│   │   ├── models.py          # Database models
│   │   ├── schemas.py         # Pydantic schemas
│   │   ├── ml_engine.py       # AI analysis engine
│   │   └── database.py        # Database configuration
│   ├── requirements.txt       # Backend dependencies
│   └── grievances.db          # SQLite database (auto-created)
│
├── pages/                      # Streamlit pages
│   ├── 01_Submit_Grievance.py
│   ├── 02_Track_Grievance.py
│   ├── 03_About_Help.py
│   ├── 04_Admin_Dashboard.py
│   ├── 05_Analytics_Dashboard.py
│   └── 06_Grievance_Map.py
│
├── components/                 # Reusable components
│   └── map_view.py
│
├── app_home.py                # Main Streamlit app
├── translations.py            # Multi-language support
├── language_selector.py       # Language switcher
├── requirements_frontend.txt  # Frontend dependencies
├── run_demo.bat              # Quick start script
└── README.md                 # Project documentation
```

---

## 🔐 Production Deployment

For production deployment with authentication and security:

1. Use `backend/app/main.py` instead of `main_demo.py`
2. Configure environment variables
3. Set up PostgreSQL database
4. Enable HTTPS
5. Configure proper CORS settings

See `DEPLOYMENT_GUIDE.md` for detailed production setup instructions.

---

## 📝 Additional Notes

### Virtual Environment (Recommended)

It's recommended to use a virtual environment:

```bash
# Create virtual environment
python -m venv venv

# Activate (Windows)
venv\Scripts\activate

# Activate (Linux/Mac)
source venv/bin/activate

# Install dependencies
pip install -r backend/requirements.txt
pip install -r requirements_frontend.txt
```

### Updating Dependencies

To update all packages to their latest versions:

```bash
pip install --upgrade -r backend/requirements.txt
pip install --upgrade -r requirements_frontend.txt
```

---

## 🎯 Quick Start Summary

**For a new user cloning the repository:**

1. Install Python 3.8+
2. Clone the repository
3. Run: `pip install -r backend/requirements.txt`
4. Run: `pip install -r requirements_frontend.txt`
5. Run: `python -m spacy download en_core_web_sm`
6. Run: `.\run_demo.bat` (Windows) or start backend and frontend separately
7. Open http://localhost:8501 in your browser

**That's it! You're ready to use the system.** 🎉

---

## 📞 Support

If you encounter any issues:

1. Check the troubleshooting section above
2. Review the error messages in the terminal
3. Ensure all dependencies are installed correctly
4. Verify Python version is 3.8 or higher

---

**Last Updated**: February 2, 2026  
**Version**: 2.0.0
