"""Leaderboard service for managing rankings"""
from sqlalchemy.orm import Session
from sqlalchemy import func, desc
from datetime import datetime, timedelta
from app.models import LeaderboardEntry, User, UserTask, QuizAttempt

class LeaderboardService:
    @staticmethod
    def get_daily_leaderboard(db: Session, limit: int = 100) -> list:
        """Get top users for today"""
        today_start = datetime.utcnow().replace(hour=0, minute=0, second=0, microsecond=0)
        
        leaderboard = db.query(LeaderboardEntry).filter(
            LeaderboardEntry.period_type == "daily",
            LeaderboardEntry.period_start == today_start
        ).order_by(desc(LeaderboardEntry.daily_score)).limit(limit).all()
        
        return leaderboard

    @staticmethod
    def get_weekly_leaderboard(db: Session, limit: int = 100) -> list:
        """Get top users for this week"""
        today = datetime.utcnow()
        week_start = today - timedelta(days=today.weekday())
        week_start = week_start.replace(hour=0, minute=0, second=0, microsecond=0)
        
        leaderboard = db.query(LeaderboardEntry).filter(
            LeaderboardEntry.period_type == "weekly",
            LeaderboardEntry.period_start == week_start
        ).order_by(desc(LeaderboardEntry.weekly_score)).limit(limit).all()
        
        return leaderboard

    @staticmethod
    def get_all_time_leaderboard(db: Session, limit: int = 100) -> list:
        """Get all-time top users"""
        leaderboard = db.query(LeaderboardEntry).filter(
            LeaderboardEntry.period_type == "all_time"
        ).order_by(desc(LeaderboardEntry.all_time_score)).limit(limit).all()
        
        return leaderboard

    @staticmethod
    def update_daily_leaderboard(db: Session) -> None:
        """Update daily leaderboard entries"""
        today_start = datetime.utcnow().replace(hour=0, minute=0, second=0, microsecond=0)
        today_end = today_start + timedelta(days=1)
        
        # Get all users
        users = db.query(User).all()
        
        for user in users:
            # Calculate daily score
            daily_tasks = db.query(UserTask).filter(
                UserTask.user_id == user.id,
                UserTask.completion_date >= today_start,
                UserTask.completion_date < today_end,
                UserTask.status == "completed"
            ).all()
            
            daily_quiz_points = db.query(func.sum(QuizAttempt.points_earned)).filter(
                QuizAttempt.user_id == user.id,
                QuizAttempt.completed_at >= today_start,
                QuizAttempt.completed_at < today_end
            ).scalar() or 0
            
            daily_task_points = sum([t.points_earned for t in daily_tasks])
            daily_score = daily_task_points + daily_quiz_points
            
            # Update or create leaderboard entry
            entry = db.query(LeaderboardEntry).filter(
                LeaderboardEntry.user_id == user.id,
                LeaderboardEntry.period_type == "daily",
                LeaderboardEntry.period_start == today_start
            ).first()
            
            if entry:
                entry.daily_score = daily_score
                entry.total_points = user.total_points
                entry.life_points = user.life_points
            else:
                entry = LeaderboardEntry(
                    user_id=user.id,
                    daily_score=daily_score,
                    total_points=user.total_points,
                    life_points=user.life_points,
                    period_type="daily",
                    period_start=today_start,
                    period_end=today_end
                )
                db.add(entry)
        
        db.commit()

    @staticmethod
    def get_user_rank(db: Session, user_id: int, period: str = "all_time") -> dict:
        """Get user's rank in different periods"""
        user = db.query(User).filter(User.id == user_id).first()
        if not user:
            return None
        
        if period == "all_time":
            rank = db.query(func.count()).filter(
                LeaderboardEntry.all_time_score > db.query(LeaderboardEntry.all_time_score).filter(
                    LeaderboardEntry.user_id == user_id
                )
            ).scalar() + 1
            return {"rank": rank, "period": "all_time"}
        
        # Similar for daily and weekly
        return {"rank": 0, "period": period}

    @staticmethod
    def get_leaderboard_with_user(db: Session, user_id: int, period: str = "all_time", limit: int = 100) -> dict:
        """Get leaderboard with highlighted user position"""
        if period == "daily":
            leaderboard = LeaderboardService.get_daily_leaderboard(db, limit)
        elif period == "weekly":
            leaderboard = LeaderboardService.get_weekly_leaderboard(db, limit)
        else:
            leaderboard = LeaderboardService.get_all_time_leaderboard(db, limit)
        
        result = []
        user_entry = None
        
        for idx, entry in enumerate(leaderboard, 1):
            user_data = {
                "rank": idx,
                "user_id": entry.user_id,
                "username": entry.user.username,
                "points": entry.daily_score if period == "daily" else entry.weekly_score if period == "weekly" else entry.all_time_score,
                "life_points": entry.life_points,
                "profile_image": entry.user.profile_image
            }
            result.append(user_data)
            
            if entry.user_id == user_id:
                user_entry = user_data
        
        return {
            "leaderboard": result,
            "user_rank": user_entry,
            "period": period
        }
