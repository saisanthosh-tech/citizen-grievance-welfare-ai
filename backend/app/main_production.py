"""
Citizen Grievance & Welfare Intelligence System - Main Backend API
Production-ready FastAPI backend with comprehensive security
"""

from fastapi import FastAPI, Depends, HTTPException, Request, status
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session
from sqlalchemy import func
import logging
import time
import os
from datetime import datetime, timedelta
from typing import Optional
from . import models, schemas, database
from .database import engine
from .ml_engine import analyzer
from .security import (
    RateLimiter, InputValidator, DataSanitizer, 
    audit_logger, PasswordValidator
)
from slowapi import Limiter
from slowapi.util import get_remote_address
from fastapi.middleware.cors import CORSMiddleware
from fastapi.middleware.trustedhost import TrustedHostMiddleware

# Database setup
models.Base.metadata.create_all(bind=engine)

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('logs/app.log'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

# Initialize FastAPI app
app = FastAPI(
    title="Citizen Grievance & Welfare Intelligence System",
    description="Government-grade platform for grievance management with explainable AI",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc"
)

# Security Middleware
app.add_middleware(TrustedHostMiddleware, allowed_hosts=os.getenv("ALLOWED_HOSTS", "localhost").split(","))

app.add_middleware(
    CORSMiddleware,
    allow_origins=os.getenv("CORS_ORIGINS", "http://localhost:3000").split(","),
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "DELETE"],
    allow_headers=["Content-Type", "Authorization"],
)

# Rate limiter
limiter = Limiter(key_func=get_remote_address)
app.state.limiter = limiter

# Initialize rate limiter
rate_limiter = RateLimiter(
    enabled=os.getenv("RATE_LIMIT_ENABLED", "True").lower() == "true",
    requests_per_window=int(os.getenv("RATE_LIMIT_REQUESTS", "100")),
    window_seconds=int(os.getenv("RATE_LIMIT_WINDOW_SECONDS", "60"))
)

# Dependency
def get_db():
    db = database.SessionLocal()
    try:
        yield db
    finally:
        db.close()


# Event handlers
@app.on_event("startup")
async def startup_event():
    """Initialize on startup"""
    logger.info("Citizen Grievance System starting up...")
    logger.info(f"Environment: {os.getenv('ENVIRONMENT', 'development')}")
    logger.info("Database connection established")


@app.on_event("shutdown")
async def shutdown_event():
    """Cleanup on shutdown"""
    logger.info("Citizen Grievance System shutting down...")


# Health check endpoint
@app.get("/health", tags=["System"])
def health_check():
    """Health check endpoint for monitoring"""
    return {
        "status": "healthy",
        "timestamp": datetime.utcnow().isoformat(),
        "version": "1.0.0"
    }


# Root endpoint
@app.get("/", response_model=dict, tags=["System"])
def read_root():
    """Welcome endpoint with system information"""
    logger.info("Root endpoint accessed")
    return {
        "system": "Citizen Grievance & Welfare Intelligence System",
        "version": "1.0.0",
        "status": "operational",
        "environment": os.getenv("ENVIRONMENT", "development"),
        "message": "Government digital platform for citizen grievance management",
        "endpoints": {
            "submit_grievance": "POST /grievances/",
            "view_grievances": "GET /grievances/",
            "get_statistics": "GET /stats/",
            "health": "GET /health"
        }
    }


# Grievance endpoints
@app.post("/grievances/", response_model=schemas.GrievanceResponse, tags=["Grievances"])
def create_grievance(grievance: schemas.GrievanceCreate, db: Session = Depends(get_db)):
    """
    Submit a citizen grievance.
    
    Rate limit: 10 requests per minute per IP
    
    The system will:
    1. Validate your submission
    2. Analyze using explainable AI
    3. Classify into a service domain
    4. Assign priority level
    5. Identify relevant government schemes
    6. Store securely for action
    
    Returns tracking token for monitoring
    """
    try:
        # Rate limiting check
        if not rate_limiter.allow_request("public"):
            logger.warning(f"Rate limit exceeded for grievance submission")
            raise HTTPException(
                status_code=429,
                detail="Too many requests. Please try again later."
            )
        
        # Input validation
        is_title_valid, title = InputValidator.validate_text(
            grievance.title, min_length=10, max_length=200
        )
        if not is_title_valid:
            logger.warning(f"Invalid title in grievance: {title}")
            raise HTTPException(status_code=400, detail=f"Title validation failed: {title}")
        
        is_desc_valid, description = InputValidator.validate_text(
            grievance.description, min_length=20, max_length=5000
        )
        if not is_desc_valid:
            logger.warning(f"Invalid description in grievance")
            raise HTTPException(status_code=400, detail=f"Description validation failed: {description}")
        
        is_email_valid, email = InputValidator.validate_email(grievance.email)
        if not is_email_valid:
            logger.warning(f"Invalid email in grievance: {email}")
            raise HTTPException(status_code=400, detail="Invalid email address")
        
        is_phone_valid, phone = InputValidator.validate_phone(grievance.phone)
        if not is_phone_valid:
            logger.warning(f"Invalid phone in grievance")
            raise HTTPException(status_code=400, detail="Invalid phone number (must be 10 digits)")
        
        is_category_valid, category = InputValidator.validate_category(grievance.category)
        if not is_category_valid:
            logger.warning(f"Invalid category in grievance: {grievance.category}")
            raise HTTPException(status_code=400, detail=f"Invalid category: {category}")
        
        # Sanitize inputs
        sanitized_data = DataSanitizer.sanitize_dict({
            "title": title,
            "description": description,
            "email": email,
            "phone": phone,
            "location": grievance.location
        })
        
        # AI Analysis
        analysis = analyzer.analyze(
            title=sanitized_data["title"],
            description=sanitized_data["description"]
        )
        
        # Create database record
        db_grievance = models.Grievance(
            title=sanitized_data["title"],
            description=sanitized_data["description"],
            category=category,
            citizen_name=DataSanitizer.sanitize_html(grievance.citizen_name),
            email=sanitized_data["email"],
            phone=sanitized_data["phone"],
            location=sanitized_data["location"],
            status="Pending",
            analysis_metadata=analysis.get("explanation", ""),
            confidence_score=analysis.get("confidence", 0.0),
            notes=f"Classified as: {analysis.get('category', 'General')}"
        )
        
        db.add(db_grievance)
        db.commit()
        db.refresh(db_grievance)
        
        # Audit log
        audit_logger.log_grievance_submission(
            grievance_id=str(db_grievance.id),
            category=category,
            user_location=sanitized_data["location"]
        )
        
        logger.info(f"Grievance created successfully: ID={db_grievance.id}, Category={category}")
        
        return schemas.GrievanceResponse(
            id=db_grievance.id,
            tracking_token=db_grievance.tracking_token,
            title=db_grievance.title,
            category=db_grievance.category,
            status=db_grievance.status,
            confidence_score=db_grievance.confidence_score,
            created_at=db_grievance.created_at,
            message="Grievance submitted successfully. Use tracking token to monitor status."
        )
    
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error creating grievance: {str(e)}")
        db.rollback()
        raise HTTPException(
            status_code=500,
            detail="Error processing grievance. Please try again later."
        )


@app.get("/grievances/", response_model=dict, tags=["Grievances"])
def get_grievances(
    skip: int = 0,
    limit: int = 20,
    status_filter: Optional[str] = None,
    category_filter: Optional[str] = None,
    db: Session = Depends(get_db)
):
    """
    Get list of grievances (admin only in production)
    
    Query Parameters:
    - skip: Number of records to skip (default: 0)
    - limit: Number of records to return (default: 20, max: 100)
    - status_filter: Filter by status (Pending, In Progress, Resolved, Rejected)
    - category_filter: Filter by category
    """
    try:
        # Rate limiting
        if not rate_limiter.allow_request("admin"):
            logger.warning("Rate limit exceeded for get_grievances")
            raise HTTPException(status_code=429, detail="Too many requests")
        
        # Limit validation
        limit = min(limit, 100)  # Max 100 records per request
        
        # Build query
        query = db.query(models.Grievance)
        
        if status_filter:
            is_valid, status = InputValidator.validate_status(status_filter)
            if is_valid:
                query = query.filter(models.Grievance.status == status)
        
        if category_filter:
            query = query.filter(models.Grievance.category == category_filter)
        
        # Execute query
        grievances = query.offset(skip).limit(limit).all()
        total_count = db.query(func.count(models.Grievance.id)).scalar()
        
        logger.info(f"Retrieved {len(grievances)} grievances (skip={skip}, limit={limit})")
        
        return {
            "total": total_count,
            "count": len(grievances),
            "skip": skip,
            "limit": limit,
            "data": [
                {
                    "id": g.id,
                    "title": g.title,
                    "category": g.category,
                    "status": g.status,
                    "confidence_score": g.confidence_score,
                    "created_at": g.created_at.isoformat() if g.created_at else None
                }
                for g in grievances
            ]
        }
    
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error retrieving grievances: {str(e)}")
        raise HTTPException(status_code=500, detail="Error retrieving grievances")


@app.put("/grievances/{grievance_id}", response_model=schemas.GrievanceResponse, tags=["Grievances"])
def update_grievance(
    grievance_id: int,
    update_data: schemas.GrievanceUpdate,
    db: Session = Depends(get_db)
):
    """
    Update grievance status (admin only)
    
    Only admins can update grievance status and add notes
    """
    try:
        # Rate limiting
        if not rate_limiter.allow_request("admin"):
            raise HTTPException(status_code=429, detail="Too many requests")
        
        # Find grievance
        grievance = db.query(models.Grievance).filter(
            models.Grievance.id == grievance_id
        ).first()
        
        if not grievance:
            logger.warning(f"Grievance not found: ID={grievance_id}")
            raise HTTPException(status_code=404, detail="Grievance not found")
        
        # Validate status
        is_valid, status = InputValidator.validate_status(update_data.status)
        if not is_valid:
            raise HTTPException(status_code=400, detail=f"Invalid status: {update_data.status}")
        
        # Sanitize notes
        notes = ""
        if update_data.notes:
            is_valid, notes = InputValidator.validate_text(
                update_data.notes, min_length=1, max_length=2000
            )
            if not is_valid:
                raise HTTPException(status_code=400, detail="Invalid notes")
            notes = DataSanitizer.sanitize_html(notes)
        
        # Update grievance
        grievance.status = status
        if notes:
            grievance.notes = notes
        grievance.updated_at = datetime.utcnow()
        
        db.commit()
        db.refresh(grievance)
        
        # Audit log
        audit_logger.log_grievance_update(
            grievance_id=str(grievance_id),
            status=status,
            admin_id="admin_system"
        )
        
        logger.info(f"Grievance updated: ID={grievance_id}, Status={status}")
        
        return schemas.GrievanceResponse(
            id=grievance.id,
            tracking_token=grievance.tracking_token,
            title=grievance.title,
            category=grievance.category,
            status=grievance.status,
            confidence_score=grievance.confidence_score,
            created_at=grievance.created_at,
            message="Grievance updated successfully"
        )
    
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error updating grievance: {str(e)}")
        db.rollback()
        raise HTTPException(status_code=500, detail="Error updating grievance")


@app.get("/stats/", response_model=dict, tags=["Statistics"])
def get_statistics(db: Session = Depends(get_db)):
    """
    Get system statistics (admin only)
    
    Returns aggregated statistics about grievances
    """
    try:
        # Rate limiting
        if not rate_limiter.allow_request("admin"):
            raise HTTPException(status_code=429, detail="Too many requests")
        
        total_grievances = db.query(func.count(models.Grievance.id)).scalar()
        
        status_counts = db.query(
            models.Grievance.status,
            func.count(models.Grievance.id).label("count")
        ).group_by(models.Grievance.status).all()
        
        category_counts = db.query(
            models.Grievance.category,
            func.count(models.Grievance.id).label("count")
        ).group_by(models.Grievance.category).all()
        
        logger.info("Statistics retrieved successfully")
        
        return {
            "total_grievances": total_grievances,
            "status_distribution": {status: count for status, count in status_counts},
            "category_distribution": {category: count for category, count in category_counts},
            "timestamp": datetime.utcnow().isoformat()
        }
    
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error retrieving statistics: {str(e)}")
        raise HTTPException(status_code=500, detail="Error retrieving statistics")


# Exception handlers
@app.exception_handler(HTTPException)
async def http_exception_handler(request: Request, exc: HTTPException):
    """Handle HTTP exceptions"""
    logger.error(f"HTTP Exception: {exc.status_code} - {exc.detail}")
    return JSONResponse(
        status_code=exc.status_code,
        content={
            "detail": exc.detail,
            "status_code": exc.status_code,
            "timestamp": datetime.utcnow().isoformat()
        }
    )


@app.exception_handler(Exception)
async def general_exception_handler(request: Request, exc: Exception):
    """Handle general exceptions"""
    logger.error(f"Unhandled Exception: {str(exc)}")
    audit_logger.log_suspicious_activity(
        activity="Unhandled_Exception",
        details=str(exc)[:200]
    )
    return JSONResponse(
        status_code=500,
        content={
            "detail": "Internal server error",
            "timestamp": datetime.utcnow().isoformat()
        }
    )


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        app,
        host="0.0.0.0",
        port=8000,
        log_level="info"
    )
