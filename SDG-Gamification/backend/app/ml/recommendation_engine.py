"""Recommendation engine using ML"""
import numpy as np
from sklearn.metrics.pairwise import cosine_similarity
from sqlalchemy.orm import Session
from app.models import User, Task, SDGGoal, UserTask

class RecommendationEngine:
    @staticmethod
    def get_task_recommendations(db: Session, user_id: int, limit: int = 5) -> list:
        """Get recommended tasks for user based on preferences and completion history"""
        user = db.query(User).filter(User.id == user_id).first()
        if not user:
            return []
        
        # Get user's completed tasks
        completed_tasks = db.query(UserTask).filter(UserTask.user_id == user_id).all()
        completed_goal_ids = [task.task.sdg_goal for task in completed_tasks]
        
        # Get all active tasks
        all_tasks = db.query(Task).filter(Task.is_active == True).all()
        
        # Score tasks based on:
        # 1. User's interest in SDG goals (based on history)
        # 2. Difficulty progression
        # 3. Points available
        scored_tasks = []
        
        for task in all_tasks:
            score = 0
            
            # Bonus for goals user has completed before
            if task.sdg_goal in completed_goal_ids:
                score += 2
            
            # Bonus for challenging tasks as user progresses
            if user.level >= 5 and task.difficulty == "hard":
                score += 1.5
            elif user.level >= 2 and task.difficulty == "medium":
                score += 1
            
            # Bonus for high-reward tasks
            if task.base_points > 500:
                score += 0.5
            
            # Penalty for tasks already done
            if any(t.task_id == task.id for t in completed_tasks):
                score = 0
                continue
            
            scored_tasks.append({"task": task, "score": score})
        
        # Sort by score and return top recommendations
        scored_tasks.sort(key=lambda x: x["score"], reverse=True)
        return [item["task"] for item in scored_tasks[:limit]]

    @staticmethod
    def get_quiz_recommendations(db: Session, user_id: int, limit: int = 3) -> list:
        """Get recommended quizzes for user"""
        from app.models import Quiz, QuizAttempt
        
        user = db.query(User).filter(User.id == user_id).first()
        if not user:
            return []
        
        # Get user's attempted quizzes
        attempted_quizzes = db.query(QuizAttempt).filter(QuizAttempt.user_id == user_id).all()
        attempted_quiz_ids = [attempt.quiz_id for attempt in attempted_quizzes]
        
        # Get all active quizzes
        all_quizzes = db.query(Quiz).filter(Quiz.is_active == True).all()
        
        scored_quizzes = []
        for quiz in all_quizzes:
            if quiz.id in attempted_quiz_ids:
                continue
            
            score = 1.0
            
            # Adjust difficulty based on user level
            if user.level >= 10 and quiz.difficulty == "hard":
                score += 0.5
            elif user.level < 5 and quiz.difficulty == "easy":
                score += 0.5
            
            # Calculate average score from similar difficulty quizzes
            similar_quizzes = db.query(QuizAttempt).join(Quiz).filter(
                QuizAttempt.user_id == user_id,
                Quiz.difficulty == quiz.difficulty
            ).all()
            
            if similar_quizzes:
                avg_score = sum([q.score for q in similar_quizzes]) / len(similar_quizzes)
                if avg_score > 80:
                    score += 0.3
            
            scored_quizzes.append({"quiz": quiz, "score": score})
        
        scored_quizzes.sort(key=lambda x: x["score"], reverse=True)
        return [item["quiz"] for item in scored_quizzes[:limit]]

    @staticmethod
    def predict_user_engagement(db: Session, user_id: int) -> dict:
        """Predict user engagement level and suggest interventions"""
        user = db.query(User).filter(User.id == user_id).first()
        if not user:
            return {}
        
        from datetime import datetime, timedelta
        
        # Calculate metrics
        days_since_last_active = (datetime.utcnow() - user.last_active).days if user.last_active else 100
        days_since_task_completion = (datetime.utcnow() - user.last_task_completion).days if user.last_task_completion else 100
        
        # Engagement score (0-100)
        engagement_score = 100
        
        if days_since_last_active > 7:
            engagement_score -= 30
        elif days_since_last_active > 3:
            engagement_score -= 15
        
        if days_since_task_completion > 7:
            engagement_score -= 20
        elif days_since_task_completion > 3:
            engagement_score -= 10
        
        engagement_score = max(0, engagement_score)
        
        # Determine engagement level
        if engagement_score >= 80:
            level = "highly_engaged"
            suggestion = "Great engagement! Keep it up!"
        elif engagement_score >= 50:
            level = "moderately_engaged"
            suggestion = "Try completing some new tasks to boost your score!"
        else:
            level = "at_risk"
            suggestion = "We miss you! Join a multiplayer game or complete an easy task to stay active."
        
        return {
            "engagement_score": engagement_score,
            "level": level,
            "suggestion": suggestion,
            "days_since_active": days_since_last_active,
            "days_since_task": days_since_task_completion
        }

    @staticmethod
    def calculate_user_similarity(db: Session, user_id: int, limit: int = 5) -> list:
        """Find similar users for multiplayer matching"""
        user = db.query(User).filter(User.id == user_id).first()
        if not user:
            return []
        
        # Get all active users
        all_users = db.query(User).filter(User.id != user_id, User.is_active == True).all()
        
        # Create feature vectors for users
        def get_user_vector(u):
            # Features: level, life_points, total_points, activity_days
            return np.array([
                u.level,
                min(u.life_points / 1000, 5),  # Normalize
                min(u.total_points / 10000, 5),
                min((datetime.utcnow() - u.last_active).days / 30, 5)  # Days active
            ])
        
        user_vector = get_user_vector(user)
        
        similarities = []
        for other_user in all_users:
            other_vector = get_user_vector(other_user)
            similarity = cosine_similarity([user_vector], [other_vector])[0][0]
            similarities.append((other_user, similarity))
        
        similarities.sort(key=lambda x: x[1], reverse=True)
        return [u[0] for u in similarities[:limit]]
