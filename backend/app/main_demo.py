"""
Citizen Grievance & Welfare Intelligence System - Demo API
This is a simplified version without authentication for demo purposes.

For production use, see main.py with full authentication.
"""

from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from datetime import datetime
from . import models, schemas, database
from .database import engine
from .ml_engine import analyzer

models.Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="Citizen Grievance & Welfare Intelligence System",
    description="Demo-friendly platform for grievance management with explainable AI",
    version="2.0.0-demo"
)

# CORS middleware for frontend access
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # For demo - restrict in production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Dependency
def get_db():
    db = database.SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.get("/", response_model=dict)
def read_root():
    """Welcome endpoint with system information"""
    return {
        "system": "Citizen Grievance & Welfare Intelligence System",
        "version": "2.0.0-demo",
        "status": "operational",
        "mode": "demo",
        "message": "Government digital platform for citizen grievance management",
        "endpoints": {
            "register": "POST /auth/register",
            "login": "POST /auth/login",
            "submit_grievance": "POST /grievances/",
            "view_grievances": "GET /grievances/",
            "get_statistics": "GET /stats/",
            "update_status": "PATCH /grievances/{id}/status"
        }
    }

# ============ AUTHENTICATION ENDPOINTS (DEMO MODE) ============

@app.post("/auth/register")
def register(user_data: schemas.UserRegister, db: Session = Depends(get_db)):
    """
    Register a new citizen account (Demo mode - simplified).
    
    In demo mode, this creates a user without full JWT implementation.
    For production, use main.py with proper authentication.
    """
    try:
        # Check if user already exists
        existing_user = db.query(models.User).filter(models.User.email == user_data.email).first()
        if existing_user:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Email already registered"
            )
        
        # Create new user (demo mode - simplified password handling)
        db_user = models.User(
            email=user_data.email,
            name=user_data.name,
            phone=user_data.phone,
            password_hash="demo_hash_" + user_data.password,  # Demo only - not secure!
            is_verified=True  # Auto-verify in demo mode
        )
        
        db.add(db_user)
        db.commit()
        db.refresh(db_user)
        
        # Return demo response
        return {
            "access_token": f"demo_token_{db_user.id}",
            "token_type": "bearer",
            "user": {
                "id": db_user.id,
                "email": db_user.email,
                "name": db_user.name,
                "phone": db_user.phone,
                "is_verified": db_user.is_verified,
                "created_at": db_user.created_at.isoformat() if db_user.created_at else None
            },
            "message": "Registration successful! Your account has been created."
        }
    except HTTPException:
        raise
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=f"Registration error: {str(e)}")


@app.post("/auth/login")
def login(user_data: schemas.UserLogin, db: Session = Depends(get_db)):
    """
    Login to your citizen account (Demo mode - simplified).
    
    In demo mode, this provides basic login without full JWT validation.
    For production, use main.py with proper authentication.
    """
    try:
        db_user = db.query(models.User).filter(models.User.email == user_data.email).first()
        
        if not db_user:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid email or password"
            )
        
        # Demo mode - simple password check (not secure!)
        expected_hash = "demo_hash_" + user_data.password
        if db_user.password_hash != expected_hash:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid email or password"
            )
        
        # Return demo response
        return {
            "access_token": f"demo_token_{db_user.id}",
            "token_type": "bearer",
            "user": {
                "id": db_user.id,
                "email": db_user.email,
                "name": db_user.name,
                "phone": db_user.phone,
                "is_verified": db_user.is_verified,
                "created_at": db_user.created_at.isoformat() if db_user.created_at else None
            },
            "message": "Login successful!"
        }
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Login error: {str(e)}")

@app.post("/grievances/")
def create_grievance(
    grievance: schemas.GrievanceCreate, 
    db: Session = Depends(get_db)
):
    """
    Submit a citizen grievance (Demo version - no authentication required).
    
    The system will:
    1. Validate your submission
    2. Analyze using explainable AI
    3. Classify into a service domain
    4. Assign priority level
    5. Identify relevant government schemes
    6. Store securely for action
    
    All grievances are treated with fairness and confidentiality.
    """
    try:
        # Input validation
        if not grievance.title or len(grievance.title.strip()) < 5:
            raise HTTPException(status_code=400, detail="Title must be at least 5 characters")
        if not grievance.description or len(grievance.description.strip()) < 20:
            raise HTTPException(status_code=400, detail="Description must be at least 20 characters")
        
        # AI Analysis with explainability
        analysis = analyzer.analyze(grievance.description + " " + grievance.title)

        # Use raw SQL to insert without user_id (demo mode workaround)
        from sqlalchemy import text
        import json
        
        # Create initial timeline entry
        initial_history = [{
            "status": "Pending",
            "timestamp": datetime.utcnow().isoformat(),
            "changed_by": "citizen",
            "action": "Grievance submitted"
        }]
        
        sql = text("""
            INSERT INTO grievances 
            (title, description, location, category, priority, status, created_at, 
             suggested_schemes, confidence_score, analysis_metadata, status_history)
            VALUES 
            (:title, :description, :location, :category, :priority, :status, :created_at,
             :suggested_schemes, :confidence_score, :analysis_metadata, :status_history)
        """)
        
        result = db.execute(sql, {
            "title": grievance.title,
            "description": grievance.description,
            "location": grievance.location,
            "category": analysis["category"],
            "priority": analysis["priority"],
            "status": "Pending",
            "created_at": datetime.utcnow(),
            "suggested_schemes": json.dumps(analysis["suggested_schemes"]),
            "confidence_score": analysis.get("confidence_score", 0.0),
            "analysis_metadata": json.dumps(analysis.get("analysis_explanation", {})),
            "status_history": json.dumps(initial_history)
        })
        db.commit()
        
        # Get the inserted ID
        grievance_id = result.lastrowid
        
        # Fetch the created grievance
        db_grievance = db.query(models.Grievance).filter(models.Grievance.id == grievance_id).first()
        
        # Return simplified response for Streamlit
        return {
            "id": db_grievance.id,
            "title": db_grievance.title,
            "description": db_grievance.description,
            "location": db_grievance.location,
            "category": db_grievance.category,
            "priority": db_grievance.priority,
            "status": db_grievance.status,
            "suggested_schemes": db_grievance.suggested_schemes,
            "confidence_score": db_grievance.confidence_score,
            "created_at": db_grievance.created_at.isoformat() if db_grievance.created_at else None,
            "message": "Your grievance has been received and will be processed fairly."
        }
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error processing grievance: {str(e)}")

@app.get("/grievances/")
def read_grievances(
    skip: int = 0, 
    limit: int = 100, 
    category: str = None, 
    priority: str = None,
    db: Session = Depends(get_db)
):
    """
    Retrieve grievances with optional filtering (Demo version - no authentication).
    
    Parameters:
    - skip: Number of records to skip (pagination)
    - limit: Maximum records to return (default 100, max 100)
    - category: Filter by category (e.g., Healthcare, Education)
    - priority: Filter by priority (High, Medium, Low)
    """
    try:
        # Validate pagination
        limit = min(limit, 100)  # Max 100 records per request
        
        # Build query - show all grievances in demo mode
        query = db.query(models.Grievance)
        
        # Apply filters
        if category:
            query = query.filter(models.Grievance.category == category)
        if priority:
            query = query.filter(models.Grievance.priority == priority)
        
        # Get total count before pagination
        total_count = query.count()
        
        # Get paginated results (latest first)
        grievances = query.order_by(models.Grievance.created_at.desc()).offset(skip).limit(limit).all()
        
        # Convert to dict for Streamlit compatibility
        grievances_list = []
        for g in grievances:
            grievances_list.append({
                "id": g.id,
                "title": g.title,
                "description": g.description,
                "location": g.location,
                "category": g.category,
                "priority": g.priority,
                "status": g.status,
                "suggested_schemes": g.suggested_schemes or [],
                "confidence_score": g.confidence_score,
                "created_at": g.created_at.isoformat() if g.created_at else None
            })
        
        return {
            "total": total_count,
            "count": len(grievances_list),
            "skip": skip,
            "limit": limit,
            "grievances": grievances_list,
            "message": f"Successfully retrieved {len(grievances_list)} grievance(s) from {total_count} total"
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error retrieving grievances: {str(e)}")

@app.get("/grievances/{grievance_id}")
def get_grievance_by_id(
    grievance_id: int,
    db: Session = Depends(get_db)
):
    """
    Get a specific grievance by ID (Demo version - no authentication).
    """
    try:
        grievance = db.query(models.Grievance).filter(models.Grievance.id == grievance_id).first()
        
        if not grievance:
            raise HTTPException(
                status_code=404,
                detail=f"Grievance with ID {grievance_id} not found"
            )
        
        return {
            "id": grievance.id,
            "title": grievance.title,
            "description": grievance.description,
            "location": grievance.location,
            "category": grievance.category,
            "priority": grievance.priority,
            "status": grievance.status,
            "suggested_schemes": grievance.suggested_schemes or [],
            "confidence_score": grievance.confidence_score,
            "created_at": grievance.created_at.isoformat() if grievance.created_at else None
        }
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error retrieving grievance: {str(e)}")

@app.get("/stats/")
def get_statistics(db: Session = Depends(get_db)):
    """
    Get aggregated statistics for grievance analytics.
    
    Returns:
    - Total grievances received
    - Distribution by category
    - Distribution by priority level
    - Average AI confidence score
    
    Useful for administrative dashboards and performance monitoring.
    """
    try:
        grievances = db.query(models.Grievance).all()
        total = len(grievances)
        
        if total == 0:
            return {
                "total_grievances": 0,
                "by_category": {},
                "by_priority": {},
                "by_status": {},
                "average_confidence_score": 0.0,
                "message": "No grievances yet. System is ready to receive citizen grievances."
            }
        
        # Calculate distributions
        by_category = {}
        by_priority = {}
        by_status = {}
        
        for g in grievances:
            by_category[g.category] = by_category.get(g.category, 0) + 1
            by_priority[g.priority] = by_priority.get(g.priority, 0) + 1
            by_status[g.status] = by_status.get(g.status, 0) + 1
        
        # Calculate average confidence
        avg_confidence = sum(g.confidence_score or 0 for g in grievances) / total if total > 0 else 0
        
        return {
            "total_grievances": total,
            "by_category": by_category,
            "by_priority": by_priority,
            "by_status": by_status,
            "average_confidence_score": round(avg_confidence, 2),
            "message": "Statistics calculated successfully"
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error calculating statistics: {str(e)}")

# ============ ADMIN ENDPOINTS ============

@app.patch("/grievances/{grievance_id}/status")
def update_grievance_status(
    grievance_id: int,
    status_update: schemas.GrievanceStatusUpdate,
    db: Session = Depends(get_db)
):
    """
    Update the status of a grievance (Admin feature).
    
    Simple admin endpoint for demo purposes - no authentication required.
    
    Parameters:
    - grievance_id: ID of the grievance to update
    - status: New status value (Pending, In Progress, or Resolved)
    
    Returns:
    - Updated grievance object
    
    Note: This is a demo feature. Production systems should implement
    proper authentication and authorization.
    """
    try:
        # Validate status value
        allowed_statuses = ["Pending", "In Progress", "Resolved"]
        if status_update.status not in allowed_statuses:
            raise HTTPException(
                status_code=400,
                detail=f"Invalid status. Allowed values: {', '.join(allowed_statuses)}"
            )
        
        # Find the grievance
        grievance = db.query(models.Grievance).filter(models.Grievance.id == grievance_id).first()
        
        if not grievance:
            raise HTTPException(
                status_code=404,
                detail=f"Grievance with ID {grievance_id} not found"
            )
        
        # Update status and add to timeline
        import json
        
        # Get current history or initialize empty list
        current_history = grievance.status_history or []
        if isinstance(current_history, str):
            current_history = json.loads(current_history)
        
        # Add new timeline entry
        new_entry = {
            "status": status_update.status,
            "timestamp": datetime.utcnow().isoformat(),
            "changed_by": "admin",
            "action": f"Status changed to {status_update.status}"
        }
        current_history.append(new_entry)
        
        # Update grievance
        grievance.status = status_update.status
        grievance.status_history = current_history
        db.commit()
        db.refresh(grievance)
        
        return {
            "id": grievance.id,
            "title": grievance.title,
            "description": grievance.description,
            "location": grievance.location,
            "category": grievance.category,
            "priority": grievance.priority,
            "status": grievance.status,
            "suggested_schemes": grievance.suggested_schemes or [],
            "confidence_score": grievance.confidence_score,
            "created_at": grievance.created_at.isoformat() if grievance.created_at else None,
            "message": f"Status updated to: {status_update.status}"
        }
        
    except HTTPException:
        raise
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=f"Error updating grievance status: {str(e)}")
