from sqlalchemy import Column, Integer, String, Text, DateTime, ForeignKey, Float, JSON
from sqlalchemy.orm import relationship
from datetime import datetime
from .database import Base

class Grievance(Base):
    __tablename__ = "grievances"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, index=True)
    description = Column(Text)
    location = Column(String, nullable=True)  # Citizen's location/address
    category = Column(String, index=True)  # Health, Education, etc.
    priority = Column(String)  # High, Medium, Low
    status = Column(String, default="Pending") # Pending, In Progress, Resolved
    created_at = Column(DateTime, default=datetime.utcnow)
    embedding = Column(Text) # JSON string or specific type for vector if PG
    suggested_schemes = Column(JSON, default=[])
    confidence_score = Column(Float, default=0.0)  # Analysis confidence (0.0 to 1.0)
    analysis_metadata = Column(JSON, default={})  # Stores reasoning and explanation

class Scheme(Base):
    __tablename__ = "schemes"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, index=True)
    description = Column(Text)
    domain = Column(String)
