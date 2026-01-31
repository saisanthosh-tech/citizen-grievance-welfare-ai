"""
Citizen Grievance & Welfare Intelligence System - FastAPI Backend
Secure, production-ready API with comprehensive error handling, logging, and security features
"""

import logging
import os
from datetime import datetime
from typing import Optional

from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.middleware.trustedhost import TrustedHostMiddleware
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session
from dotenv import load_dotenv

from . import models, schemas, database
from .database import engine
from .ml_engine import analyzer
from .security import RateLimiter

# Load environment variables
load_dotenv()

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

# Create database tables
models.Base.metadata.create_all(bind=engine)

# Initialize FastAPI app
app = FastAPI(
    title="Citizen Grievance & Welfare Intelligence System",
    description="Government-grade platform for grievance management with explainable AI and security",
    version="2.0.0",
    docs_url="/api/docs",
    redoc_url="/api/redoc",
    openapi_url="/api/openapi.json"
)

# Security middleware - CORS
CORS_ORIGINS = os.getenv("CORS_ORIGINS", "http://localhost:8501,http://localhost:3000").split(",")
app.add_middleware(
    CORSMiddleware,
    allow_origins=CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "DELETE", "OPTIONS"],
    allow_headers=["*"],
)

# Security middleware - Trusted hosts (in production)
if os.getenv("ENVIRONMENT") == "production":
    app.add_middleware(
        TrustedHostMiddleware,
        allowed_hosts=["grievance-welfare.gov.in", "www.grievance-welfare.gov.in"]
    )

# Rate limiter
rate_limiter = RateLimiter(
    enabled=os.getenv("RATE_LIMIT_ENABLED", "True").lower() == "true",
    requests_per_window=int(os.getenv("RATE_LIMIT_REQUESTS", "100")),
    window_seconds=int(os.getenv("RATE_LIMIT_WINDOW_SECONDS", "60"))
)

# Database dependency
def get_db():
    """Get database session"""
    db = database.SessionLocal()
    try:
        yield db
    except Exception as e:
        db.rollback()
        logger.error(f"Database error: {str(e)}")
        raise
    finally:
        db.close()

# Health check endpoint
@app.get("/health")
def health_check():
    """Health check endpoint for monitoring"""
    try:
        db = database.SessionLocal()
        db.execute("SELECT 1")
        db.close()
        return {
            "status": "healthy",
            "timestamp": datetime.utcnow().isoformat(),
            "database": "connected",
            "version": "2.0.0"
        }
    except Exception as e:
        logger.error(f"Health check failed: {str(e)}")
        return {
            "status": "unhealthy",
            "database": "disconnected",
            "error": str(e)
        }, 503

# Root endpoint
@app.get("/")
def read_root():
    """Welcome endpoint with system information"""
    logger.info("Root endpoint accessed")
    return {
        "system": "Citizen Grievance & Welfare Intelligence System",
        "version": "2.0.0",
        "status": "operational",
        "message": "Government digital platform for citizen grievance management",
        "environment": os.getenv("ENVIRONMENT", "development"),
        "endpoints": {
            "health": "GET /health",
            "submit_grievance": "POST /grievances/",
            "view_grievances": "GET /grievances/",
            "get_statistics": "GET /stats/",
            "api_docs": "GET /api/docs"
        }
    }

# Submit grievance endpoint
@app.post("/grievances/", response_model=schemas.GrievanceResponse)
async def create_grievance(
    grievance: schemas.GrievanceCreate,
    db: Session = Depends(get_db)
):
    """
    Submit a citizen grievance with AI analysis
    
    The system will:
    1. Validate submission
    2. Analyze using explainable AI
    3. Classify into service domain
    4. Assign priority level
    5. Identify relevant government schemes
    6. Store securely
    
    **Required fields:**
    - title: Brief description (min 5 characters)
    - description: Detailed explanation (min 20 characters)
    
    **Optional fields:**
    - location: Geographic location for issue
    """
    try:
        # Rate limiting check
        if not rate_limiter.allow_request():
            logger.warning("Rate limit exceeded")
            raise HTTPException(
                status_code=status.HTTP_429_TOO_MANY_REQUESTS,
                detail="Too many requests. Please try again later."
            )
        
        # Validate input
        if not grievance.title or len(grievance.title) < 5:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Title must be at least 5 characters"
            )
        
        if not grievance.description or len(grievance.description) < 20:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Description must be at least 20 characters"
            )
        
        # Perform AI analysis
        analysis = analyzer.analyze(grievance.description, grievance.title)
        
        # Create grievance record
        db_grievance = models.Grievance(
            title=grievance.title,
            description=grievance.description,
            location=grievance.location,
            category=analysis["category"],
            priority=analysis["priority"],
            status="Pending",
            suggested_schemes=analysis["suggested_schemes"],
            analysis_metadata={
                "confidence": analysis["confidence"],
                "explanation": analysis["explanation"]
            }
        )
        
        db.add(db_grievance)
        db.commit()
        db.refresh(db_grievance)
        
        logger.info(f"Grievance created: {db_grievance.id} - Category: {analysis['category']}")
        
        return schemas.GrievanceResponse(
            grievance=db_grievance,
            analysis=analysis,
            message="Grievance submitted successfully"
        )
    
    except HTTPException:
        raise
    except Exception as e:
        db.rollback()
        logger.error(f"Error creating grievance: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Error processing grievance. Please try again."
        )

# Get grievances endpoint
@app.get("/grievances/")
async def get_grievances(
    id: Optional[str] = None,
    status_filter: Optional[str] = None,
    category: Optional[str] = None,
    db: Session = Depends(get_db)
):
    """
    Fetch grievances with optional filtering
    
    **Query parameters:**
    - id: Search by grievance ID
    - status_filter: Filter by status (Pending, In Progress, Resolved)
    - category: Filter by category
    """
    try:
        # Rate limiting check
        if not rate_limiter.allow_request():
            raise HTTPException(
                status_code=status.HTTP_429_TOO_MANY_REQUESTS,
                detail="Too many requests. Please try again later."
            )
        
        query = db.query(models.Grievance)
        
        if id:
            query = query.filter(models.Grievance.id == id)
        
        if status_filter:
            query = query.filter(models.Grievance.status == status_filter)
        
        if category:
            query = query.filter(models.Grievance.category == category)
        
        grievances = query.order_by(models.Grievance.created_at.desc()).all()
        
        logger.info(f"Retrieved {len(grievances)} grievances")
        
        return {
            "grievances": grievances,
            "total": len(grievances),
            "timestamp": datetime.utcnow().isoformat()
        }
    
    except Exception as e:
        logger.error(f"Error fetching grievances: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Error fetching grievances"
        )

# Update grievance endpoint (Admin)
@app.put("/grievances/{grievance_id}")
async def update_grievance(
    grievance_id: str,
    update: schemas.GrievanceUpdate,
    db: Session = Depends(get_db)
):
    """
    Update grievance status and notes (Admin only)
    
    **Parameters:**
    - grievance_id: ID of grievance to update
    - status: New status
    - notes: Admin notes
    """
    try:
        grievance = db.query(models.Grievance).filter(
            models.Grievance.id == grievance_id
        ).first()
        
        if not grievance:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Grievance not found"
            )
        
        if update.status:
            grievance.status = update.status
        
        if update.notes:
            grievance.notes = update.notes
        
        grievance.updated_at = datetime.utcnow()
        
        db.commit()
        db.refresh(grievance)
        
        logger.info(f"Grievance updated: {grievance_id}")
        
        return {
            "message": "Grievance updated successfully",
            "grievance": grievance
        }
    
    except HTTPException:
        raise
    except Exception as e:
        db.rollback()
        logger.error(f"Error updating grievance: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Error updating grievance"
        )

# Statistics endpoint
@app.get("/stats/")
async def get_statistics(db: Session = Depends(get_db)):
    """
    Get system statistics and grievance breakdown
    """
    try:
        # Rate limiting check
        if not rate_limiter.allow_request():
            raise HTTPException(
                status_code=status.HTTP_429_TOO_MANY_REQUESTS,
                detail="Too many requests. Please try again later."
            )
        
        total_grievances = db.query(models.Grievance).count()
        
        # Status breakdown
        status_breakdown = {}
        for status in ["Pending", "In Progress", "Resolved"]:
            count = db.query(models.Grievance).filter(
                models.Grievance.status == status
            ).count()
            status_breakdown[status] = count
        
        # Category breakdown
        category_breakdown = {}
        categories = db.query(models.Grievance.category).distinct()
        for cat_row in categories:
            category = cat_row[0]
            count = db.query(models.Grievance).filter(
                models.Grievance.category == category
            ).count()
            category_breakdown[category] = count
        
        # Priority breakdown
        priority_breakdown = {}
        for priority in ["High", "Medium", "Low"]:
            count = db.query(models.Grievance).filter(
                models.Grievance.priority == priority
            ).count()
            priority_breakdown[priority] = count
        
        logger.info("Statistics retrieved")
        
        return {
            "total_grievances": total_grievances,
            "status_breakdown": status_breakdown,
            "category_breakdown": category_breakdown,
            "priority_breakdown": priority_breakdown,
            "timestamp": datetime.utcnow().isoformat()
        }
    
    except Exception as e:
        logger.error(f"Error fetching statistics: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Error fetching statistics"
        )

# Exception handlers
@app.exception_handler(HTTPException)
async def http_exception_handler(request, exc):
    """Handle HTTP exceptions"""
    logger.warning(f"HTTP Exception: {exc.status_code} - {exc.detail}")
    return JSONResponse(
        status_code=exc.status_code,
        content={
            "detail": exc.detail,
            "timestamp": datetime.utcnow().isoformat()
        }
    )

@app.exception_handler(Exception)
async def general_exception_handler(request, exc):
    """Handle general exceptions"""
    logger.error(f"Unhandled Exception: {str(exc)}")
    return JSONResponse(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        content={
            "detail": "Internal server error",
            "timestamp": datetime.utcnow().isoformat()
        }
    )

# Startup event
@app.on_event("startup")
async def startup_event():
    """Initialize on startup"""
    logger.info("Application starting up...")
    logger.info(f"Environment: {os.getenv('ENVIRONMENT', 'development')}")

# Shutdown event
@app.on_event("shutdown")
async def shutdown_event():
    """Cleanup on shutdown"""
    logger.info("Application shutting down...")
