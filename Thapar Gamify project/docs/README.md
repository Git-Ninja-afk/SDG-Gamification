# Gamify SDG Platform - Comprehensive Documentation

## 🎯 Project Overview

**Gamify SDG** is a full-stack platform that gamifies the UN Sustainable Development Goals, making it engaging and rewarding for users to contribute positively to society. The platform combines game mechanics, AI/ML recommendations, real-time leaderboards, and payment integration to create an interactive experience.

### Key Features
- ✅ **Gamified Tasks** - Complete SDG-aligned tasks for points and life credits
- ✅ **Real-time Leaderboards** - Daily, weekly, and all-time rankings
- ✅ **AI-Powered Recommendations** - Personalized task and quiz suggestions
- ✅ **Interactive Quizzes** - SDG knowledge assessment with rewards
- ✅ **Multiplayer Games** - Competitive mini-games (collect plastic, plant trees, etc.)
- ✅ **Image Verification** - AI-based photo proof validation
- ✅ **Payment Integration** - Razorpay for reward redemption
- ✅ **Credit System** - Life points that decay with inactivity
- ✅ **Achievements & Badges** - Unlock badges and achievements
- ✅ **Multi-platform** - Web (React), Mobile (React Native), Admin CMS

---

## 📁 Project Structure

```
Thapar Gamify project/
├── backend/                    # Python FastAPI Backend
│   ├── app/
│   │   ├── core/              # Configuration, security, database
│   │   ├── models/            # SQLAlchemy ORM models
│   │   ├── routes/            # API endpoints
│   │   ├── services/          # Business logic
│   │   ├── ml/                # AI/ML modules
│   │   └── ws/                # WebSocket real-time features
│   ├── requirements.txt
│   ├── main.py
│   └── .env.example
│
├── web/                        # React Web Frontend
│   ├── src/
│   │   ├── pages/             # Page components
│   │   ├── components/        # Reusable components
│   │   ├── services/          # API calls
│   │   ├── store/             # Zustand state management
│   │   └── utils/             # Utilities
│   ├── package.json
│   └── App.jsx
│
├── mobile/                     # React Native Mobile App
│   ├── src/
│   │   ├── screens/           # Screen components
│   │   ├── components/        # Reusable components
│   │   ├── services/          # API integration
│   │   └── store/             # State management
│   └── package.json
│
├── admin-cms/                  # Admin Panel for CMS
│   ├── src/
│   │   └── App.jsx
│   └── package.json
│
├── infrastructure/             # AWS Configuration
│   ├── aws_config.py
│   └── cdk_stack.py
│
└── docs/                       # Documentation
```

---

## 🚀 Getting Started

### Prerequisites
- Python 3.9+
- Node.js 16+
- PostgreSQL 13+
- Redis 6.0+
- AWS Account (for deployment)
- Razorpay Account (for payments)

### Backend Setup

```bash
cd backend

# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Configure environment
cp .env.example .env
# Edit .env with your configuration

# Create database
python -m alembic upgrade head

# Start backend server
python -m uvicorn main:app --reload
```

Backend runs on: `http://localhost:8000`
API Docs: `http://localhost:8000/docs`

### Web Frontend Setup

```bash
cd web

# Install dependencies
npm install

# Create .env file
REACT_APP_API_URL=http://localhost:8000/api/v1
REACT_APP_WS_URL=ws://localhost:8000

# Start development server
npm start
```

Web app runs on: `http://localhost:3000`

### Mobile App Setup

```bash
cd mobile

# Install dependencies
npm install

# Start Expo
expo start

# For iOS
expo start --ios

# For Android
expo start --android
```

### Admin CMS Setup

```bash
cd admin-cms

# Install dependencies
npm install

# Start admin panel
npm start
```

Admin panel runs on: `http://localhost:3001`

---

## 🏗️ AWS Deployment

### Prerequisites
- AWS CLI configured
- CDK installed: `npm install -g aws-cdk`
- Docker installed (for containerization)

### Deployment Steps

```bash
cd infrastructure

# Bootstrap CDK (one-time)
cdk bootstrap aws://ACCOUNT-ID/ap-south-1

# Deploy infrastructure
cdk deploy

# Deploy backend to ECS/Lambda
aws ecs create-service ...
```

### AWS Services Used
- **RDS** - PostgreSQL database
- **ElastiCache** - Redis caching
- **S3** - File storage for user uploads
- **CloudFront** - CDN for static assets
- **ALB** - Load balancing
- **Lambda** - Serverless task verification
- **CloudWatch** - Logging and monitoring

---

## 🔐 Database Schema

### Key Tables
- **users** - User profiles with encrypted location
- **tasks** - SDG-aligned tasks to complete
- **user_tasks** - Task completion tracking with proof
- **quizzes** - Knowledge assessment quizzes
- **quiz_attempts** - User quiz attempts
- **leaderboard_entries** - Rankings (daily/weekly/all-time)
- **achievements** - Achievement definitions
- **user_achievements** - User earned achievements
- **multiplayer_games** - Mini-game sessions
- **rewards** - Redeemable rewards/vouchers
- **transactions** - Point/credit transactions

---

## 🔗 API Endpoints

### Authentication
- `POST /api/v1/auth/register` - Register new user
- `POST /api/v1/auth/login` - Login user

### Users
- `GET /api/v1/users/{user_id}` - Get user profile
- `PUT /api/v1/users/{user_id}` - Update user profile

### Leaderboards
- `GET /api/v1/leaderboard/daily` - Daily rankings
- `GET /api/v1/leaderboard/weekly` - Weekly rankings
- `GET /api/v1/leaderboard/all-time` - All-time rankings
- `GET /api/v1/users/{user_id}/rank` - User's rank

### Recommendations
- `GET /api/v1/users/{user_id}/recommendations/tasks` - Task recommendations
- `GET /api/v1/users/{user_id}/recommendations/quizzes` - Quiz recommendations
- `GET /api/v1/users/{user_id}/engagement` - Engagement prediction
- `GET /api/v1/users/{user_id}/similar-users` - Similar users for multiplayer

### Payments
- `POST /api/v1/payments/create-order` - Create payment order
- `POST /api/v1/payments/verify` - Verify payment

### WebSocket
- `WS /ws/{user_id}` - Real-time updates connection

---

## 🤖 AI/ML Features

### Recommendation Engine
Analyzes user behavior and suggests:
- Tasks aligned with user preferences
- Quizzes based on difficulty progression
- Engagement predictions and interventions
- Similar users for multiplayer matching

### Image Verification
Computer vision-based task proof validation:
- **Tree Detection** - Identifies vegetation in photos
- **Plastic Detection** - Detects waste in images
- **Environment Cleanliness** - Assesses photo clarity and lighting
- Confidence scoring for verification

### Engagement Prediction
Predicts user engagement level and provides:
- Engagement score (0-100)
- Suggestions for improving engagement
- Days since last active tracking
- Credit decay calculation

---

## 💳 Payment Integration

### Razorpay Setup
1. Create Razorpay account
2. Get Key ID and Key Secret
3. Add to `.env` file

### Payment Flow
1. User selects reward
2. System calculates cost
3. Payment order created
4. Payment processed
5. Signature verified
6. Points deducted & reward issued

---

## 📱 Real-time Features

### WebSocket Events
- **leaderboard_update** - Live leaderboard changes
- **notification** - User notifications
- **achievement_unlocked** - New achievements
- **game_update** - Multiplayer game events
- **location_update** - User location broadcasts
- **online_count** - Online user count

### Broadcasting
- Server broadcasts updates to all connected users
- Location-aware filtering for nearby tasks
- Game-specific notifications for players

---

## 🔒 Security

### Encryption
- Passwords: bcrypt hashing
- JWT tokens for authentication
- User location encrypted before storage
- HTTPS for all communications

### API Security
- CORS configuration
- Rate limiting (implement with middleware)
- Input validation with Pydantic
- JWT token expiration

### Database
- SQL injection prevention via SQLAlchemy ORM
- Connection pooling
- Automated backups (30-day retention)
- Multi-AZ deployment for high availability

---

## 📊 Key Metrics

### User Engagement
- Life points decay: 5% daily (inactivity)
- Starting points: 100
- Points restore on task completion
- Engagement score calculation

### Gamification
- 17 SDG goals to target
- Multiple difficulty levels (easy, medium, hard)
- Achievement system with badges
- Leaderboard competitions
- Multiplayer games with scoring

### Rewards
- Configurable point costs
- Life point requirements
- Vouchers, coupons, discounts
- Quantity-based inventory

---

## 🧪 Testing

### Backend Testing
```bash
cd backend
pytest tests/
```

### Frontend Testing
```bash
cd web
npm test
```

---

## 🚢 Deployment Checklist

- [ ] Configure environment variables
- [ ] Set up AWS infrastructure
- [ ] Configure Razorpay keys
- [ ] Set up PostgreSQL database
- [ ] Configure Redis cache
- [ ] Set up S3 bucket
- [ ] Configure CloudFront CDN
- [ ] Set up SSL certificates
- [ ] Configure domain name
- [ ] Set up monitoring and alerts
- [ ] Run database migrations
- [ ] Deploy backend service
- [ ] Deploy web frontend
- [ ] Deploy mobile apps to stores
- [ ] Deploy admin panel
- [ ] Run smoke tests
- [ ] Monitor for errors

---

## 📞 Support & Contribution

For issues, questions, or contributions, please refer to the main repository.

---

## 📄 License

This project is proprietary and confidential.

---

**Happy Gaming! 🎮🌍**
