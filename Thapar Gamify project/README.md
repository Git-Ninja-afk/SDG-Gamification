![Python](https://img.shields.io/badge/Python-3.11-3776AB?logo=python&logoColor=white)
![FastAPI](https://img.shields.io/badge/FastAPI-0.100-009688?logo=fastapi&logoColor=white)
![React](https://img.shields.io/badge/React-18-61DAFB?logo=react&logoColor=black)
![React Native](https://img.shields.io/badge/React_Native-Expo-000020?logo=expo&logoColor=white)
![PostgreSQL](https://img.shields.io/badge/PostgreSQL-15-336791?logo=postgresql&logoColor=white)
![Redis](https://img.shields.io/badge/Redis-7-DC382D?logo=redis&logoColor=white)
![AWS](https://img.shields.io/badge/AWS-Deployed-FF9900?logo=amazonaws&logoColor=white)
![TypeScript](https://img.shields.io/badge/TypeScript-5-3178C6?logo=typescript&logoColor=white)
# Root Level Project Configuration

This is the Gamify SDG Platform - a comprehensive hackathon project that gamifies UN Sustainable Development Goals.

## 📦 Project Structure

- **backend/** - Python FastAPI server with AI/ML
- **web/** - React web application
- **mobile/** - React Native mobile app (iOS/Android)
- **admin-cms/** - Admin panel for content management
- **infrastructure/** - AWS deployment configuration
- **docs/** - Complete documentation

## 🎯 Quick Start

### Start All Services (One Command)
```bash
# Terminal 1: Backend
cd backend && source venv/bin/activate && python main.py

# Terminal 2: Web
cd web && npm start

# Terminal 3: Mobile
cd mobile && npm start

# Terminal 4: Admin CMS
cd admin-cms && npm start
```

### Individual Service Setup
See `docs/SETUP.md` for detailed instructions.

## 🌟 Key Features

1. **Gamified SDG Tasks** - Complete tasks aligned with 17 UN goals
2. **Real-time Leaderboards** - Daily, weekly, all-time rankings
3. **AI Recommendations** - Personalized task/quiz suggestions
4. **Image Verification** - CV-based photo proof validation
5. **Multiplayer Games** - Competitive mini-games
6. **Payment Integration** - Razorpay reward redemption
7. **Credit System** - Life points with inactivity decay
8. **Achievements** - Badges and milestone unlocks
9. **WebSocket** - Real-time notifications and updates
10. **Responsive Design** - Web + Mobile compatible

## 🔧 Technology Stack

### Backend
- FastAPI (Python)
- PostgreSQL
- Redis
- SQLAlchemy ORM
- JWT Authentication
- WebSockets
- Razorpay API
- OpenCV (Image Processing)
- scikit-learn (ML)

### Frontend
- React 18
- React Native (Expo)
- Tailwind CSS
- Zustand (State Management)
- Socket.IO (Real-time)
- Framer Motion (Animations)

### Infrastructure
- AWS RDS (PostgreSQL)
- AWS S3 (File Storage)
- AWS ElastiCache (Redis)
- AWS ECS/Lambda
- AWS CloudFront (CDN)
- AWS ALB (Load Balancer)

## 📊 Architecture

```
User Devices (Web/Mobile)
        ↓
    React Apps
        ↓
    REST API + WebSocket
        ↓
    FastAPI Backend
        ↓
    ┌─────────────┬───────────────┬──────────────┐
    ↓             ↓               ↓              ↓
PostgreSQL      Redis          S3              ML Engine
Database      Caching       File Storage    Recommendations
```

## 🚀 Deployment

### Development
All services run locally on different ports:
- Backend: `http://localhost:8000`
- Web: `http://localhost:3000`
- Mobile: Expo dev server
- Admin: `http://localhost:3001`

### Production
Deploy to AWS using:
```bash
cd infrastructure
cdk deploy
```

## 📋 API Documentation

Visit `http://localhost:8000/docs` (Swagger UI) after starting backend.

## 🔐 Security

- Password hashing: bcrypt
- Authentication: JWT tokens
- Database: SSL connections
- Encryption: Location data encrypted
- HTTPS: Required in production

## 📞 Support

For questions or issues, refer to individual component READMEs:
- Backend: `backend/README.md`
- Web: `web/README.md`
- Mobile: `mobile/README.md`
- Admin: `admin-cms/README.md`

---

