from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from . import models, schemas, database
from .database import engine
from .ml_engine import analyzer

models.Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="Citizen Grievance & Welfare Intelligence System",
    description="Government-grade platform for grievance management with explainable AI",
    version="1.0.0"
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
        "version": "1.0.0",
        "status": "operational",
        "message": "Government digital platform for citizen grievance management",
        "endpoints": {
            "submit_grievance": "POST /grievances/",
            "view_grievances": "GET /grievances/",
            "get_statistics": "GET /stats/"
        }
    }

@app.post("/grievances/", response_model=schemas.GrievanceResponse)
def create_grievance(grievance: schemas.GrievanceCreate, db: Session = Depends(get_db)):
    """
    Submit a citizen grievance.
    
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

        db_grievance = models.Grievance(
            title=grievance.title,
            description=grievance.description,
            location=grievance.location,
            category=analysis["category"],
            priority=analysis["priority"],
            suggested_schemes=analysis["suggested_schemes"],
            confidence_score=analysis.get("confidence_score", 0.0),
            analysis_metadata=analysis.get("analysis_explanation", {})
        )
        db.add(db_grievance)
        db.commit()
        db.refresh(db_grievance)
        
        return schemas.GrievanceResponse(
            grievance=db_grievance,
            analysis=schemas.AnalysisResult(
                category=analysis["category"],
                priority=analysis["priority"],
                confidence=analysis.get("confidence_score", 0.0),
                explanation=analysis.get("analysis_explanation", {})
            ),
            message="Your grievance has been received and will be processed fairly."
        )
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error processing grievance: {str(e)}")

@app.get("/grievances/", response_model=schemas.GrievanceListResponse)
def read_grievances(skip: int = 0, limit: int = 100, category: str = None, priority: str = None, db: Session = Depends(get_db)):
    """
    Retrieve grievances with optional filtering.
    
    Parameters:
    - skip: Number of records to skip (pagination)
    - limit: Maximum records to return (default 100, max 100)
    - category: Filter by category (e.g., Healthcare, Education)
    - priority: Filter by priority (High, Medium, Low)
    """
    try:
        # Validate pagination
        limit = min(limit, 100)  # Max 100 records per request
        
        # Build query
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
        
        return schemas.GrievanceListResponse(
            total=total_count,
            count=len(grievances),
            skip=skip,
            limit=limit,
            grievances=grievances,
            message=f"Successfully retrieved {len(grievances)} grievance(s) from {total_count} total"
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error retrieving grievances: {str(e)}")

@app.get("/stats/", response_model=schemas.StatisticsResponse)
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
            return schemas.StatisticsResponse(
                total_grievances=0,
                by_category={},
                by_priority={},
                average_confidence_score=0.0,
                message="No grievances yet. System is ready to receive citizen grievances."
            )
        
        # Calculate distributions
        by_category = {}
        by_priority = {}
        
        for g in grievances:
            by_category[g.category] = by_category.get(g.category, 0) + 1
            by_priority[g.priority] = by_priority.get(g.priority, 0) + 1
        
        # Calculate average confidence
        avg_confidence = sum(g.confidence_score or 0 for g in grievances) / total if total > 0 else 0
        
        return schemas.StatisticsResponse(
            total_grievances=total,
            by_category=by_category,
            by_priority=by_priority,
            average_confidence_score=round(avg_confidence, 2),
            message="Statistics calculated successfully"
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error calculating statistics: {str(e)}")
