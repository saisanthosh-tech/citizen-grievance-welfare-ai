from pydantic import BaseModel
from datetime import datetime
from typing import Optional, Dict, List

class GrievanceBase(BaseModel):
    title: str
    description: str
    location: Optional[str] = None

class GrievanceCreate(GrievanceBase):
    pass

class Grievance(GrievanceBase):
    id: int
    category: str
    priority: str
    status: str
    suggested_schemes: list[str] = []
    created_at: datetime
    location: Optional[str] = None
    confidence_score: Optional[float] = None
    analysis_metadata: Optional[Dict] = None

    class Config:
        from_attributes = True

class AnalysisResult(BaseModel):
    """Analysis result with explainability"""
    category: str
    priority: str
    confidence: float
    explanation: Dict

class GrievanceResponse(BaseModel):
    """Enhanced response with analysis explanation"""
    grievance: Grievance
    analysis: AnalysisResult
    message: str

class GrievanceListResponse(BaseModel):
    """Paginated list response with metadata"""
    total: int
    count: int
    skip: int
    limit: int
    grievances: List[Grievance]
    message: str

class StatisticsResponse(BaseModel):
    """Statistics and analytics response"""
    total_grievances: int
    by_category: Dict[str, int]
    by_priority: Dict[str, int]
    average_confidence_score: float
    message: str

class SchemeBase(BaseModel):
    name: str
    description: str
    domain: str

class Scheme(SchemeBase):
    id: int

    class Config:
        from_attributes = True
