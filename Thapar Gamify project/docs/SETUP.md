# Installation & Setup Guide

## System Requirements
- macOS/Linux/Windows
- Python 3.9+
- Node.js 16+
- PostgreSQL 13+
- Redis 6.0+

## Step-by-Step Setup

### 1. PostgreSQL Setup (macOS with Homebrew)
```bash
brew install postgresql
brew services start postgresql
createdb gamify_sdg
```

### 2. Redis Setup
```bash
brew install redis
brew services start redis
```

### 3. Backend Setup
```bash
cd backend
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt

# Configure environment
cp .env.example .env
# Edit .env with your settings

# Create tables
python -c "from app.core.database import Base, engine; Base.metadata.create_all(bind=engine)"

# Run backend
python main.py
```

### 4. Web Frontend Setup
```bash
cd web
npm install

# Create .env file
echo "REACT_APP_API_URL=http://localhost:8000/api/v1" > .env
echo "REACT_APP_WS_URL=ws://localhost:8000" >> .env

npm start
```

### 5. Mobile App Setup
```bash
cd mobile
npm install
expo start
```

### 6. Admin CMS Setup
```bash
cd admin-cms
npm install
npm start
```

---

## Environment Configuration

### Backend .env
```
DATABASE_URL=postgresql://user:password@localhost:5432/gamify_sdg
REDIS_URL=redis://localhost:6379
SECRET_KEY=your-secret-key-min-32-chars
RAZORPAY_KEY_ID=your-key-id
RAZORPAY_KEY_SECRET=your-secret
AWS_ACCESS_KEY_ID=your-access-key
AWS_SECRET_ACCESS_KEY=your-secret-key
AWS_REGION=ap-south-1
AWS_S3_BUCKET=gamify-sdg-bucket
```

### Web Frontend .env
```
REACT_APP_API_URL=http://localhost:8000/api/v1
REACT_APP_WS_URL=ws://localhost:8000
```

---

## Troubleshooting

### Backend Issues
**Port 8000 already in use:**
```bash
# Find and kill process
lsof -i :8000
kill -9 <PID>
```

**Database connection error:**
```bash
# Check PostgreSQL is running
brew services list

# Restart if needed
brew services restart postgresql
```

### Frontend Issues
**npm dependencies error:**
```bash
rm -rf node_modules package-lock.json
npm install
```

---

## Quick Test

### Test Backend
```bash
curl http://localhost:8000/health
```

### Test API
```bash
curl -X POST http://localhost:8000/api/v1/auth/register \
  -H "Content-Type: application/json" \
  -d '{
    "email":"test@example.com",
    "username":"testuser",
    "password":"testpass123",
    "full_name":"Test User",
    "location":"Mumbai"
  }'
```

---

**Need help? Check the main README.md for more details.**
