# Gamify SDG Platform - API Implementation Guide

## REST API Endpoints

### Authentication Endpoints

#### Register User
```
POST /api/v1/auth/register
Content-Type: application/json

{
  "email": "user@example.com",
  "username": "username",
  "password": "password123",
  "full_name": "User Name",
  "location": "Mumbai"
}

Response: 200
{
  "success": true,
  "user_id": 1,
  "message": "User registered successfully"
}
```

#### Login
```
POST /api/v1/auth/login
Content-Type: application/json

{
  "email": "user@example.com",
  "password": "password123"
}

Response: 200
{
  "access_token": "eyJ0eXAiOiJKV1QiLC...",
  "refresh_token": "eyJ0eXAiOiJKV1QiLC...",
  "user_id": 1,
  "username": "username"
}
```

### User Endpoints

#### Get User Profile
```
GET /api/v1/users/{user_id}
Authorization: Bearer {access_token}

Response: 200
{
  "id": 1,
  "username": "username",
  "full_name": "User Name",
  "life_points": 150,
  "total_points": 5000,
  "level": 5,
  "email": "user@example.com",
  "location": "Mumbai",
  "role": "user",
  "is_active": true,
  "is_verified": true,
  "created_at": "2026-01-18T10:30:00",
  "last_active": "2026-01-18T15:45:00",
  "profile_image": "https://s3.amazonaws.com/..."
}
```

### Leaderboard Endpoints

#### Get Daily Leaderboard
```
GET /api/v1/leaderboard/daily?limit=100&user_id=1
Authorization: Bearer {access_token}

Response: 200
{
  "leaderboard": [
    {
      "rank": 1,
      "user_id": 2,
      "username": "player1",
      "points": 2500,
      "life_points": 200,
      "profile_image": "https://..."
    },
    ...
  ]
}
```

#### Get Weekly Leaderboard
```
GET /api/v1/leaderboard/weekly?limit=100
Authorization: Bearer {access_token}

Response: 200
{
  "leaderboard": [...]
}
```

#### Get All-Time Leaderboard
```
GET /api/v1/leaderboard/all-time?limit=100
Authorization: Bearer {access_token}

Response: 200
{
  "leaderboard": [...]
}
```

### Recommendation Endpoints

#### Get Task Recommendations
```
GET /api/v1/users/{user_id}/recommendations/tasks?limit=5
Authorization: Bearer {access_token}

Response: 200
{
  "recommendations": [
    {
      "id": 1,
      "title": "Plant a Tree",
      "description": "Plant a tree in your area",
      "sdg_goal": "Life on Land",
      "points": 100,
      "difficulty": "easy"
    },
    ...
  ]
}
```

#### Get Quiz Recommendations
```
GET /api/v1/users/{user_id}/recommendations/quizzes?limit=3
Authorization: Bearer {access_token}

Response: 200
{
  "recommendations": [
    {
      "id": 1,
      "title": "Climate Change Basics",
      "sdg_goal": "Climate Action",
      "difficulty": "medium"
    },
    ...
  ]
}
```

#### Get Engagement Prediction
```
GET /api/v1/users/{user_id}/engagement
Authorization: Bearer {access_token}

Response: 200
{
  "engagement_score": 75,
  "level": "moderately_engaged",
  "suggestion": "Try completing some new tasks to boost your score!",
  "days_since_active": 2,
  "days_since_task": 3
}
```

### Payment Endpoints

#### Create Payment Order
```
POST /api/v1/payments/create-order
Authorization: Bearer {access_token}
Content-Type: application/json

{
  "user_id": 1,
  "reward_id": 5,
  "amount": 500.0
}

Response: 200
{
  "id": "order_1234567890",
  "entity": "order",
  "amount": 50000,
  "amount_paid": 0,
  "amount_due": 50000,
  "currency": "INR",
  "receipt": "reward_5_1",
  "offer_id": null,
  "status": "created",
  "attempts": 0,
  "notes": {
    "user_id": 1,
    "reward_id": 5
  },
  "created_at": 1674074400
}
```

#### Verify Payment
```
POST /api/v1/payments/verify
Authorization: Bearer {access_token}
Content-Type: application/json

{
  "user_id": 1,
  "payment_id": "pay_1234567890",
  "order_id": "order_1234567890",
  "signature": "signature_string",
  "reward_id": 5
}

Response: 200
{
  "success": true,
  "message": "Reward redeemed successfully"
}
```

### WebSocket Connection

#### Connect to Real-time Updates
```
WS ws://localhost:8000/ws/{user_id}

Authentication: Include user_id in URL

Message Types:
1. Ping
   {"type": "ping"}
   
   Response:
   {"type": "pong"}

2. Location Update
   {"type": "location_update", "location": "Mumbai"}
   
3. Get Online Count
   {"type": "get_online_count"}
   
   Response:
   {"type": "online_count", "count": 150}

Server Broadcasts:
- {"type": "leaderboard_update", "data": {...}}
- {"type": "notification", "data": {...}}
- {"type": "achievement_unlocked", "achievement": {...}}
- {"type": "game_update", "game_id": 1, "data": {...}}
```

---

## Error Responses

### 400 Bad Request
```json
{
  "detail": "Email already registered"
}
```

### 401 Unauthorized
```json
{
  "detail": "Invalid credentials"
}
```

### 404 Not Found
```json
{
  "detail": "User not found"
}
```

### 500 Internal Server Error
```json
{
  "detail": "Internal server error"
}
```

---

## Rate Limiting

Currently no rate limiting implemented. Add in production:
```
- 100 requests per minute per user
- 1000 requests per minute per IP
```

---

## Authentication

All protected endpoints require JWT token in header:
```
Authorization: Bearer {access_token}
```

Token expiry: 30 minutes
Refresh token expiry: 7 days
