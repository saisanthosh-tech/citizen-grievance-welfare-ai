from sqlalchemy import Column, Integer, String, Text, DateTime, ForeignKey, Float, JSON, Boolean
from sqlalchemy.orm import relationship
from datetime import datetime
from .database import Base

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True)
    name = Column(String, index=True)
    phone = Column(String, nullable=True)
    password_hash = Column(String)  # Hashed password (never store plain text)
    is_verified = Column(Boolean, default=False)  # Email verification status
    verification_token = Column(String, nullable=True)  # For email verification
    created_at = Column(DateTime, default=datetime.utcnow)
    last_login = Column(DateTime, nullable=True)
    grievances = relationship("Grievance", back_populates="citizen")

class Grievance(Base):
    __tablename__ = "grievances"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), index=True, nullable=True)  # Optional for demo mode
    title = Column(String, index=True)
    description = Column(Text)
    location = Column(String, nullable=True)  # Citizen's location/address
    latitude = Column(Float, nullable=True)  # GPS latitude
    longitude = Column(Float, nullable=True)  # GPS longitude
    category = Column(String, index=True)  # Health, Education, etc.
    priority = Column(String)  # High, Medium, Low
    status = Column(String, default="Pending") # Pending, In Progress, Resolved
    created_at = Column(DateTime, default=datetime.utcnow)
    embedding = Column(Text) # JSON string or specific type for vector if PG
    suggested_schemes = Column(JSON, default=[])
    confidence_score = Column(Float, default=0.0)  # Analysis confidence (0.0 to 1.0)
    analysis_metadata = Column(JSON, default={})  # Stores reasoning and explanation
    status_history = Column(JSON, default=[])  # Timeline of status changes
    citizen = relationship("User", back_populates="grievances")

class Scheme(Base):
    __tablename__ = "schemes"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, index=True)
    description = Column(Text)
    domain = Column(String)
