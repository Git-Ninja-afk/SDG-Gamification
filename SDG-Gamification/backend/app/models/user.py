"""Database models for users"""
from sqlalchemy import Column, String, Integer, DateTime, Boolean, Float, Enum as SQLEnum, Text
from sqlalchemy.orm import relationship
from datetime import datetime
import enum
from app.core.database import Base

class UserRole(str, enum.Enum):
    USER = "user"
    ADMIN = "admin"
    MODERATOR = "moderator"

class User(Base):
    __tablename__ = "users"
    
    id = Column(Integer, primary_key=True, index=True)
    email = Column(String(255), unique=True, index=True)
    username = Column(String(255), unique=True, index=True)
    full_name = Column(String(255))
    hashed_password = Column(String(255))
    phone = Column(String(20), nullable=True)
    location = Column(String(255))  # Encrypted before storage
    bio = Column(Text, nullable=True)
    profile_image = Column(String(255), nullable=True)
    
    # Points and Levels
    life_points = Column(Integer, default=0)
    total_points = Column(Integer, default=0)
    level = Column(Integer, default=1)
    
    # Status
    is_active = Column(Boolean, default=True)
    is_verified = Column(Boolean, default=False)
    role = Column(SQLEnum(UserRole), default=UserRole.USER)
    
    # Temporal
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    last_active = Column(DateTime, default=datetime.utcnow)
    
    # Last activity for credit degradation
    last_task_completion = Column(DateTime, nullable=True)
    credit_decay_rate = Column(Float, default=1.0)  # Daily decay percentage
    
    # Relationships
    tasks_completed = relationship("UserTask", back_populates="user")
    quiz_attempts = relationship("QuizAttempt", back_populates="user")
    leaderboard_entries = relationship("LeaderboardEntry", back_populates="user")
    transactions = relationship("Transaction", back_populates="user")
    achievements = relationship("UserAchievement", back_populates="user")
