"""Main FastAPI application"""
from fastapi import FastAPI, Depends, HTTPException, WebSocket, Query
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from datetime import datetime
import logging

from app.core import settings, get_db
from app.models import User
from app.services import UserService, LeaderboardService, PaymentService
from app.ml import RecommendationEngine
from app.ws import manager

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Create FastAPI app
app = FastAPI(
    title=settings.APP_NAME,
    version=settings.APP_VERSION,
    description="Gamified SDG Platform API"
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Health check endpoint
@app.get("/health")
async def health_check():
    return {"status": "healthy", "timestamp": datetime.utcnow()}

# WebSocket endpoint for real-time updates
@app.websocket("/ws/{user_id}")
async def websocket_endpoint(user_id: int, websocket: WebSocket):
    await manager.connect(user_id, websocket)
    try:
        while True:
            data = await websocket.receive_json()
            
            if data.get("type") == "ping":
                await websocket.send_json({"type": "pong"})
            elif data.get("type") == "location_update":
                await manager.broadcast_location_update(user_id, data.get("location"))
            elif data.get("type") == "get_online_count":
                online_count = manager.get_online_count()
                await websocket.send_json({
                    "type": "online_count",
                    "count": online_count
                })
    except Exception as e:
        logger.error(f"WebSocket error: {e}")
    finally:
        manager.disconnect(user_id)

# ============= USER ENDPOINTS =============

@app.post("/api/v1/auth/register")
async def register(
    email: str,
    username: str,
    password: str,
    full_name: str,
    location: str,
    db: Session = Depends(get_db)
):
    """Register new user"""
    # Check if user exists
    if UserService.get_user_by_email(db, email):
        raise HTTPException(status_code=400, detail="Email already registered")
    
    try:
        user = UserService.create_user(db, email, username, password, full_name, location)
        return {
            "success": True,
            "user_id": user.id,
            "message": "User registered successfully"
        }
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@app.post("/api/v1/auth/login")
async def login(email: str, password: str, db: Session = Depends(get_db)):
    """Authenticate user"""
    from app.core.security import create_access_token, create_refresh_token
    
    user = UserService.authenticate_user(db, email, password)
    if not user:
        raise HTTPException(status_code=401, detail="Invalid credentials")
    
    access_token = create_access_token({"sub": user.id, "email": user.email})
    refresh_token = create_refresh_token({"sub": user.id})
    
    UserService.update_last_active(db, user.id)
    
    return {
        "access_token": access_token,
        "refresh_token": refresh_token,
        "user_id": user.id,
        "username": user.username
    }

@app.get("/api/v1/users/{user_id}")
async def get_user(user_id: int, db: Session = Depends(get_db)):
    """Get user profile"""
    stats = UserService.get_user_stats(db, user_id)
    if not stats:
        raise HTTPException(status_code=404, detail="User not found")
    return stats

@app.put("/api/v1/users/{user_id}")
async def update_user(user_id: int, **kwargs):
    """Update user profile"""
    return {"message": "User profile updated"}

# ============= LEADERBOARD ENDPOINTS =============

@app.get("/api/v1/leaderboard/daily")
async def get_daily_leaderboard(
    limit: int = Query(100, le=500),
    user_id: int = None,
    db: Session = Depends(get_db)
):
    """Get daily leaderboard"""
    if user_id:
        return LeaderboardService.get_leaderboard_with_user(db, user_id, "daily", limit)
    
    leaderboard = LeaderboardService.get_daily_leaderboard(db, limit)
    result = []
    for idx, entry in enumerate(leaderboard, 1):
        result.append({
            "rank": idx,
            "user_id": entry.user_id,
            "username": entry.user.username,
            "points": entry.daily_score,
            "life_points": entry.life_points
        })
    return {"leaderboard": result}

@app.get("/api/v1/leaderboard/weekly")
async def get_weekly_leaderboard(
    limit: int = Query(100, le=500),
    user_id: int = None,
    db: Session = Depends(get_db)
):
    """Get weekly leaderboard"""
    if user_id:
        return LeaderboardService.get_leaderboard_with_user(db, user_id, "weekly", limit)
    
    leaderboard = LeaderboardService.get_weekly_leaderboard(db, limit)
    result = []
    for idx, entry in enumerate(leaderboard, 1):
        result.append({
            "rank": idx,
            "user_id": entry.user_id,
            "username": entry.user.username,
            "points": entry.weekly_score,
            "life_points": entry.life_points
        })
    return {"leaderboard": result}

@app.get("/api/v1/leaderboard/all-time")
async def get_all_time_leaderboard(
    limit: int = Query(100, le=500),
    user_id: int = None,
    db: Session = Depends(get_db)
):
    """Get all-time leaderboard"""
    if user_id:
        return LeaderboardService.get_leaderboard_with_user(db, user_id, "all_time", limit)
    
    leaderboard = LeaderboardService.get_all_time_leaderboard(db, limit)
    result = []
    for idx, entry in enumerate(leaderboard, 1):
        result.append({
            "rank": idx,
            "user_id": entry.user_id,
            "username": entry.user.username,
            "points": entry.all_time_score,
            "life_points": entry.life_points
        })
    return {"leaderboard": result}

@app.get("/api/v1/users/{user_id}/rank")
async def get_user_rank(user_id: int, period: str = "all_time", db: Session = Depends(get_db)):
    """Get user's rank in specific period"""
    rank_info = LeaderboardService.get_user_rank(db, user_id, period)
    if not rank_info:
        raise HTTPException(status_code=404, detail="User not found")
    return rank_info

# ============= RECOMMENDATIONS ENDPOINTS =============

@app.get("/api/v1/users/{user_id}/recommendations/tasks")
async def get_task_recommendations(
    user_id: int,
    limit: int = Query(5, le=20),
    db: Session = Depends(get_db)
):
    """Get personalized task recommendations"""
    tasks = RecommendationEngine.get_task_recommendations(db, user_id, limit)
    result = [{
        "id": task.id,
        "title": task.title,
        "description": task.description,
        "sdg_goal": task.sdg_goal.value,
        "points": task.base_points,
        "difficulty": task.difficulty.value
    } for task in tasks]
    return {"recommendations": result}

@app.get("/api/v1/users/{user_id}/recommendations/quizzes")
async def get_quiz_recommendations(
    user_id: int,
    limit: int = Query(3, le=10),
    db: Session = Depends(get_db)
):
    """Get personalized quiz recommendations"""
    quizzes = RecommendationEngine.get_quiz_recommendations(db, user_id, limit)
    result = [{
        "id": quiz.id,
        "title": quiz.title,
        "sdg_goal": quiz.sdg_goal.value,
        "difficulty": quiz.difficulty.value
    } for quiz in quizzes]
    return {"recommendations": result}

@app.get("/api/v1/users/{user_id}/engagement")
async def get_engagement_prediction(user_id: int, db: Session = Depends(get_db)):
    """Get user engagement prediction and suggestions"""
    prediction = RecommendationEngine.predict_user_engagement(db, user_id)
    if not prediction:
        raise HTTPException(status_code=404, detail="User not found")
    return prediction

@app.get("/api/v1/users/{user_id}/similar-users")
async def get_similar_users(
    user_id: int,
    limit: int = Query(5, le=20),
    db: Session = Depends(get_db)
):
    """Get similar users for multiplayer matching"""
    similar_users = RecommendationEngine.calculate_user_similarity(db, user_id, limit)
    result = [{
        "id": user.id,
        "username": user.username,
        "level": user.level,
        "life_points": user.life_points,
        "profile_image": user.profile_image
    } for user in similar_users]
    return {"similar_users": result}

# ============= ADMIN/CMS ENDPOINTS =============

@app.post("/api/v1/admin/leaderboard/update")
async def update_leaderboards(db: Session = Depends(get_db)):
    """Manually trigger leaderboard update"""
    try:
        LeaderboardService.update_daily_leaderboard(db)
        return {"success": True, "message": "Leaderboards updated"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/v1/admin/stats")
async def get_admin_stats(db: Session = Depends(get_db)):
    """Get platform statistics"""
    from sqlalchemy import func
    
    total_users = db.query(func.count(User.id)).scalar()
    active_users = db.query(func.count(User.id)).filter(User.is_active == True).scalar()
    online_users = manager.get_online_count()
    
    return {
        "total_users": total_users,
        "active_users": active_users,
        "online_users": online_users,
        "timestamp": datetime.utcnow()
    }

# ============= PAYMENT ENDPOINTS =============

@app.post("/api/v1/payments/create-order")
async def create_payment_order(user_id: int, reward_id: int, amount: float, db: Session = Depends(get_db)):
    """Create Razorpay payment order"""
    payment_service = PaymentService()
    order = payment_service.create_order(user_id, amount, reward_id)
    
    if "error" in order:
        raise HTTPException(status_code=400, detail=order["error"])
    
    return order

@app.post("/api/v1/payments/verify")
async def verify_payment(
    user_id: int,
    payment_id: str,
    order_id: str,
    signature: str,
    reward_id: int,
    db: Session = Depends(get_db)
):
    """Verify payment and complete reward redemption"""
    payment_service = PaymentService()
    
    if not payment_service.verify_payment(payment_id, order_id, signature):
        raise HTTPException(status_code=400, detail="Payment verification failed")
    
    # Process reward redemption
    result = payment_service.process_reward_redemption(db, user_id, reward_id, 100, 50)
    
    if not result["success"]:
        raise HTTPException(status_code=400, detail=result["error"])
    
    return result

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
