"""Database models for gamification features"""
from sqlalchemy import Column, String, Integer, DateTime, Boolean, Float, Text, ForeignKey, Table
from sqlalchemy.orm import relationship
from datetime import datetime
from app.core.database import Base

# Association table for multiplayer games
game_players = Table(
    'game_players',
    Base.metadata,
    Column('game_id', Integer, ForeignKey('multiplayer_games.id')),
    Column('user_id', Integer, ForeignKey('users.id'))
)

class LeaderboardEntry(Base):
    __tablename__ = "leaderboard_entries"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    
    # Points
    total_points = Column(Integer, default=0)
    life_points = Column(Integer, default=0)
    
    # Rankings
    daily_rank = Column(Integer, nullable=True)
    weekly_rank = Column(Integer, nullable=True)
    all_time_rank = Column(Integer, nullable=True)
    
    # Scores for different periods
    daily_score = Column(Integer, default=0)
    weekly_score = Column(Integer, default=0)
    all_time_score = Column(Integer, default=0)
    
    period_type = Column(String(50))  # daily, weekly, all_time
    period_start = Column(DateTime)
    period_end = Column(DateTime)
    
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    user = relationship("User", back_populates="leaderboard_entries")

class Achievement(Base):
    __tablename__ = "achievements"
    
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(255))
    description = Column(Text)
    icon_url = Column(String(255))
    
    # Requirements
    requirement_type = Column(String(100))  # points_threshold, tasks_completed, quiz_streak, etc.
    requirement_value = Column(Integer)
    
    points_reward = Column(Integer, default=100)
    badge_category = Column(String(100))
    
    created_at = Column(DateTime, default=datetime.utcnow)
    
    # Relationships
    users = relationship("UserAchievement", back_populates="achievement")

class UserAchievement(Base):
    __tablename__ = "user_achievements"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    achievement_id = Column(Integer, ForeignKey("achievements.id"))
    
    earned_at = Column(DateTime, default=datetime.utcnow)
    
    # Relationships
    user = relationship("User", back_populates="achievements")
    achievement = relationship("Achievement", back_populates="users")

class MultiplayerGame(Base):
    __tablename__ = "multiplayer_games"
    
    id = Column(Integer, primary_key=True, index=True)
    game_type = Column(String(100))  # collect_plastic, clean_ocean, plant_trees, etc.
    sdg_goal = Column(String(100))
    
    title = Column(String(255))
    description = Column(Text)
    
    # Game State
    status = Column(String(50), default="active")  # active, completed, cancelled
    max_players = Column(Integer, default=2)
    current_players = Column(Integer, default=0)
    
    # Rewards
    winner_points = Column(Integer)
    loser_points = Column(Integer)
    life_points_reward = Column(Integer)
    
    # Temporal
    created_at = Column(DateTime, default=datetime.utcnow)
    started_at = Column(DateTime, nullable=True)
    completed_at = Column(DateTime, nullable=True)
    duration_minutes = Column(Integer, default=5)
    
    # Relationships
    players = relationship("User", secondary=game_players)
    scores = relationship("GameScore", back_populates="game", cascade="all, delete-orphan")

class GameScore(Base):
    __tablename__ = "game_scores"
    
    id = Column(Integer, primary_key=True, index=True)
    game_id = Column(Integer, ForeignKey("multiplayer_games.id"))
    user_id = Column(Integer, ForeignKey("users.id"))
    
    score = Column(Integer, default=0)
    position = Column(Integer)  # 1st, 2nd, etc.
    is_winner = Column(Boolean, default=False)
    
    actions = Column(Text)  # JSON array of game actions
    
    created_at = Column(DateTime, default=datetime.utcnow)
    
    # Relationships
    game = relationship("MultiplayerGame", back_populates="scores")

class Reward(Base):
    __tablename__ = "rewards"
    
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(255))
    description = Column(Text)
    reward_type = Column(String(100))  # voucher, coupon, discount, etc.
    
    # Reward Details
    points_cost = Column(Integer)
    life_points_cost = Column(Integer)
    
    value = Column(String(100))  # Actual value (e.g., "500 Rs", "50% discount")
    provider = Column(String(100))  # Brand/Provider
    
    quantity_available = Column(Integer)
    quantity_redeemed = Column(Integer, default=0)
    
    expiry_date = Column(DateTime, nullable=True)
    
    created_at = Column(DateTime, default=datetime.utcnow)
    is_active = Column(Boolean, default=True)

class Transaction(Base):
    __tablename__ = "transactions"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    
    transaction_type = Column(String(50))  # points_earned, points_spent, reward_redeemed, etc.
    amount = Column(Integer)
    
    description = Column(Text)
    related_id = Column(Integer, nullable=True)  # Task ID, Quiz ID, Reward ID, etc.
    related_type = Column(String(50))  # task, quiz, reward, etc.
    
    balance_before = Column(Integer)
    balance_after = Column(Integer)
    
    created_at = Column(DateTime, default=datetime.utcnow)
    
    # Relationships
    user = relationship("User", back_populates="transactions")
