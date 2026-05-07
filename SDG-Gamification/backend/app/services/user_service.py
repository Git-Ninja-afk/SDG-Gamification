"""User service for handling user operations"""
from sqlalchemy.orm import Session
from datetime import datetime, timedelta
from app.models import User, UserRole
from app.core.security import get_password_hash, verify_password
from app.core.config import settings

class UserService:
    @staticmethod
    def create_user(db: Session, email: str, username: str, password: str, full_name: str, location: str) -> User:
        """Create a new user"""
        db_user = User(
            email=email,
            username=username,
            hashed_password=get_password_hash(password),
            full_name=full_name,
            location=location,  # Should be encrypted in production
            life_points=100,  # Starting life points
            total_points=0,
            level=1,
        )
        db.add(db_user)
        db.commit()
        db.refresh(db_user)
        return db_user

    @staticmethod
    def authenticate_user(db: Session, email: str, password: str) -> User:
        """Authenticate user with email and password"""
        user = db.query(User).filter(User.email == email).first()
        if not user or not verify_password(password, user.hashed_password):
            return None
        return user

    @staticmethod
    def get_user_by_id(db: Session, user_id: int) -> User:
        """Get user by ID"""
        return db.query(User).filter(User.id == user_id).first()

    @staticmethod
    def get_user_by_email(db: Session, email: str) -> User:
        """Get user by email"""
        return db.query(User).filter(User.email == email).first()

    @staticmethod
    def update_user(db: Session, user_id: int, **kwargs) -> User:
        """Update user fields"""
        user = db.query(User).filter(User.id == user_id).first()
        if user:
            for key, value in kwargs.items():
                if hasattr(user, key) and key != 'id':
                    setattr(user, key, value)
            user.updated_at = datetime.utcnow()
            db.commit()
            db.refresh(user)
        return user

    @staticmethod
    def add_life_points(db: Session, user_id: int, points: int) -> User:
        """Add life points to user"""
        user = db.query(User).filter(User.id == user_id).first()
        if user:
            user.life_points += points
            user.last_task_completion = datetime.utcnow()
            db.commit()
            db.refresh(user)
        return user

    @staticmethod
    def deduct_life_points(db: Session, user_id: int, points: int) -> User:
        """Deduct life points from user"""
        user = db.query(User).filter(User.id == user_id).first()
        if user:
            user.life_points = max(0, user.life_points - points)
            db.commit()
            db.refresh(user)
        return user

    @staticmethod
    def apply_credit_decay(db: Session, user_id: int) -> User:
        """Apply daily credit decay to inactive users"""
        user = db.query(User).filter(User.id == user_id).first()
        if user:
            # Check if user has been inactive for more than 1 day
            if user.last_active:
                days_inactive = (datetime.utcnow() - user.last_active).days
                if days_inactive > 1:
                    # Decay 5% per day of inactivity
                    decay_factor = 0.95 ** days_inactive
                    user.life_points = int(user.life_points * decay_factor)
            db.commit()
            db.refresh(user)
        return user

    @staticmethod
    def update_last_active(db: Session, user_id: int) -> User:
        """Update user's last active timestamp"""
        user = db.query(User).filter(User.id == user_id).first()
        if user:
            user.last_active = datetime.utcnow()
            db.commit()
            db.refresh(user)
        return user

    @staticmethod
    def get_user_stats(db: Session, user_id: int) -> dict:
        """Get comprehensive user statistics"""
        user = db.query(User).filter(User.id == user_id).first()
        if not user:
            return None
        
        return {
            "id": user.id,
            "username": user.username,
            "full_name": user.full_name,
            "life_points": user.life_points,
            "total_points": user.total_points,
            "level": user.level,
            "email": user.email,
            "location": user.location,
            "role": user.role.value,
            "is_active": user.is_active,
            "is_verified": user.is_verified,
            "created_at": user.created_at,
            "last_active": user.last_active,
            "profile_image": user.profile_image,
        }
