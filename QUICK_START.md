# Quick Setup Commands

For someone cloning this repository, run these commands in order:

```bash
# 1. Clone the repository
git clone <your-repository-url>
cd citizen-grievance-welfare-ai

# 2. Install backend dependencies
pip install -r backend/requirements.txt

# 3. Install frontend dependencies  
pip install -r requirements_frontend.txt

# 4. Download spaCy language model (required for AI)
python -m spacy download en_core_web_sm

# 5. Run the application
.\run_demo.bat
```

Then open http://localhost:8501 in your browser.

---

## What Gets Installed

### Backend (API Server)
- FastAPI, uvicorn, SQLAlchemy, pydantic
- spaCy, sentence-transformers, scikit-learn
- Authentication: passlib, python-jose
- Total: ~15 packages

### Frontend (Streamlit UI)
- Streamlit, requests, plotly
- folium, streamlit-folium, pandas
- Total: ~6 packages

### AI Model
- spaCy English model (en_core_web_sm)
- One-time download, ~12 MB

---

## Servers

After running `.\run_demo.bat`:
- **Backend API**: http://127.0.0.1:8000
- **Frontend UI**: http://localhost:8501
- **API Docs**: http://127.0.0.1:8000/docs

---

See `INSTALLATION.md` for detailed setup instructions and troubleshooting.
