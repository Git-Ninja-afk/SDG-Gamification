"""Database models for SDG content"""
from sqlalchemy import Column, String, Integer, DateTime, Boolean, Text, Enum as SQLEnum, Float, ForeignKey
from sqlalchemy.orm import relationship
from datetime import datetime
import enum
from app.core.database import Base

class SDGGoal(str, enum.Enum):
    GOAL_1 = "No Poverty"
    GOAL_2 = "Zero Hunger"
    GOAL_3 = "Good Health and Well-Being"
    GOAL_4 = "Quality Education"
    GOAL_5 = "Gender Equality"
    GOAL_6 = "Clean Water and Sanitation"
    GOAL_7 = "Affordable and Clean Energy"
    GOAL_8 = "Decent Work and Economic Growth"
    GOAL_9 = "Industry, Innovation and Infrastructure"
    GOAL_10 = "Reduced Inequalities"
    GOAL_11 = "Sustainable Cities and Communities"
    GOAL_12 = "Responsible Consumption and Production"
    GOAL_13 = "Climate Action"
    GOAL_14 = "Life Below Water"
    GOAL_15 = "Life on Land"
    GOAL_16 = "Peace, Justice and Strong Institutions"
    GOAL_17 = "Partnerships for the Goals"

class TaskDifficulty(str, enum.Enum):
    EASY = "easy"
    MEDIUM = "medium"
    HARD = "hard"

class Task(Base):
    __tablename__ = "tasks"
    
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(255))
    description = Column(Text)
    sdg_goal = Column(SQLEnum(SDGGoal))
    difficulty = Column(SQLEnum(TaskDifficulty), default=TaskDifficulty.EASY)
    
    # Points and Rewards
    base_points = Column(Integer)  # Base points for completing
    life_points = Column(Integer)  # Life points awarded
    xp_reward = Column(Integer, default=100)
    
    # Task Details
    instructions = Column(Text)
    proof_required = Column(Boolean, default=True)  # Requires photo/video proof
    duration_days = Column(Integer, default=1)
    category = Column(String(100))
    
    # Temporal
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    is_active = Column(Boolean, default=True)
    
    # Relationships
    completed_by = relationship("UserTask", back_populates="task")
    verification_required = relationship("TaskVerification", back_populates="task")

class UserTask(Base):
    __tablename__ = "user_tasks"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    task_id = Column(Integer, ForeignKey("tasks.id"))
    
    # Status
    status = Column(String(50), default="in_progress")  # in_progress, submitted, verified, completed, rejected
    completion_date = Column(DateTime, nullable=True)
    submission_date = Column(DateTime, nullable=True)
    verification_date = Column(DateTime, nullable=True)
    
    # Proof
    proof_image_url = Column(String(255), nullable=True)
    proof_video_url = Column(String(255), nullable=True)
    description = Column(Text, nullable=True)
    
    # Points
    points_earned = Column(Integer, default=0)
    life_points_earned = Column(Integer, default=0)
    
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    user = relationship("User", back_populates="tasks_completed")
    task = relationship("Task", back_populates="completed_by")
    verification = relationship("TaskVerification", uselist=False, back_populates="user_task")

class TaskVerification(Base):
    __tablename__ = "task_verifications"
    
    id = Column(Integer, primary_key=True, index=True)
    user_task_id = Column(Integer, ForeignKey("user_tasks.id"))
    verified_by = Column(Integer, ForeignKey("users.id"), nullable=True)  # Admin/Moderator
    
    status = Column(String(50), default="pending")  # pending, approved, rejected
    feedback = Column(Text, nullable=True)
    verification_method = Column(String(100))  # manual, ai, auto
    
    created_at = Column(DateTime, default=datetime.utcnow)
    verified_at = Column(DateTime, nullable=True)
    
    # Relationships
    user_task = relationship("UserTask", back_populates="verification")
    task = relationship("Task", back_populates="verification_required")

class Quiz(Base):
    __tablename__ = "quizzes"
    
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(255))
    description = Column(Text)
    sdg_goal = Column(SQLEnum(SDGGoal))
    
    # Rewards
    points_reward = Column(Integer, default=50)
    life_points_reward = Column(Integer, default=10)
    
    # Quiz Details
    difficulty = Column(SQLEnum(TaskDifficulty), default=TaskDifficulty.MEDIUM)
    time_limit = Column(Integer)  # seconds
    passing_score = Column(Integer, default=70)  # percentage
    
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    is_active = Column(Boolean, default=True)
    
    # Relationships
    questions = relationship("QuizQuestion", back_populates="quiz", cascade="all, delete-orphan")
    attempts = relationship("QuizAttempt", back_populates="quiz")

class QuizQuestion(Base):
    __tablename__ = "quiz_questions"
    
    id = Column(Integer, primary_key=True, index=True)
    quiz_id = Column(Integer, ForeignKey("quizzes.id"))
    
    question = Column(Text)
    question_type = Column(String(50))  # multiple_choice, true_false, short_answer
    options = Column(Text)  # JSON array
    correct_answer = Column(String(500))
    explanation = Column(Text, nullable=True)
    
    order = Column(Integer)
    
    # Relationships
    quiz = relationship("Quiz", back_populates="questions")

class QuizAttempt(Base):
    __tablename__ = "quiz_attempts"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    quiz_id = Column(Integer, ForeignKey("quizzes.id"))
    
    score = Column(Integer)  # percentage
    passed = Column(Boolean, default=False)
    answers = Column(Text)  # JSON object with question_id -> answer
    
    started_at = Column(DateTime, default=datetime.utcnow)
    completed_at = Column(DateTime, nullable=True)
    time_taken = Column(Integer, nullable=True)  # seconds
    
    points_earned = Column(Integer, default=0)
    life_points_earned = Column(Integer, default=0)
    
    # Relationships
    user = relationship("User", back_populates="quiz_attempts")
    quiz = relationship("Quiz", back_populates="attempts")
