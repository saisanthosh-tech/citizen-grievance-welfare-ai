# 🚀 Installation & Setup

## Prerequisites
- Python 3.8 or higher
- pip (Python package manager)
- Git

## Quick Setup

```bash
# 1. Clone the repository
git clone https://github.com/your-username/citizen-grievance-welfare-ai.git
cd citizen-grievance-welfare-ai

# 2. Install backend dependencies
pip install -r backend/requirements.txt

# 3. Install frontend dependencies
pip install -r requirements_frontend.txt

# 4. Download AI model (required for NLP)
python -m spacy download en_core_web_sm

# 5. Run the application
.\run_demo.bat
```

## Access the Application

- **Frontend (Streamlit UI)**: http://localhost:8501
- **Backend API**: http://127.0.0.1:8000
- **API Documentation**: http://127.0.0.1:8000/docs

## Manual Start (Alternative)

If you prefer to run servers separately:

**Terminal 1 - Backend:**
```bash
cd backend
uvicorn app.main_demo:app --reload --host 127.0.0.1 --port 8000
```

**Terminal 2 - Frontend:**
```bash
python -m streamlit run app_home.py
```

## Features

- 🌍 **Multi-language Support**: English, Hindi, Telugu, Tamil
- 🤖 **AI-Powered Analysis**: Automatic grievance categorization
- 📊 **Analytics Dashboard**: Real-time statistics and insights
- 🗺️ **GPS Mapping**: Location-based grievance visualization
- 🔐 **Secure**: Government-grade security features

## Troubleshooting

**Issue: Module not found**
```bash
pip install -r backend/requirements.txt
pip install -r requirements_frontend.txt
```

**Issue: spaCy model not found**
```bash
python -m spacy download en_core_web_sm
```

**Issue: Port already in use**
- Backend: Change port in command (e.g., `--port 8001`)
- Frontend: Use `streamlit run app_home.py --server.port 8502`

For detailed setup instructions, see [INSTALLATION.md](INSTALLATION.md)
