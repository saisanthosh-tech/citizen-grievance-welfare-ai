from pydantic import BaseModel, EmailStr
from datetime import datetime
from typing import Optional, Dict, List

# ============ USER SCHEMAS ============

class UserRegister(BaseModel):
    """User registration request"""
    email: EmailStr
    name: str
    phone: Optional[str] = None
    password: str

class UserLogin(BaseModel):
    """User login request"""
    email: EmailStr
    password: str

class UserResponse(BaseModel):
    """User response (no password)"""
    id: int
    email: str
    name: str
    phone: Optional[str] = None
    is_verified: bool
    created_at: datetime

    class Config:
        from_attributes = True

class TokenResponse(BaseModel):
    """JWT token response"""
    access_token: str
    token_type: str
    user: UserResponse
    message: str

class VerifyEmailRequest(BaseModel):
    """Email verification request"""
    token: str

# ============ GRIEVANCE SCHEMAS ============

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

class GrievanceStatusUpdate(BaseModel):
    """Schema for updating grievance status (admin feature)"""
    status: str
    
    class Config:
        schema_extra = {
            "example": {
                "status": "In Progress"
            }
        }

class SchemeBase(BaseModel):
    name: str
    description: str
    domain: str

class Scheme(SchemeBase):
    id: int

    class Config:
        from_attributes = True
