#!/bin/bash

# Gamify SDG Platform - Complete Startup Script
# This script starts all services for development

set -e

echo "🚀 Starting Gamify SDG Platform..."
echo ""

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Function to print section headers
print_section() {
    echo ""
    echo -e "${YELLOW}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
    echo -e "${GREEN}$1${NC}"
    echo -e "${YELLOW}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
    echo ""
}

# Check prerequisites
print_section "Checking Prerequisites"

# Check Python
if ! command -v python3 &> /dev/null; then
    echo -e "${RED}❌ Python 3 not found. Please install Python 3.9+${NC}"
    exit 1
else
    PYTHON_VERSION=$(python3 --version)
    echo -e "${GREEN}✅ $PYTHON_VERSION found${NC}"
fi

# Check Node.js
if ! command -v node &> /dev/null; then
    echo -e "${RED}❌ Node.js not found. Please install Node.js 16+${NC}"
    exit 1
else
    NODE_VERSION=$(node --version)
    echo -e "${GREEN}✅ Node.js $NODE_VERSION found${NC}"
fi

# Check npm
if ! command -v npm &> /dev/null; then
    echo -e "${RED}❌ npm not found${NC}"
    exit 1
else
    NPM_VERSION=$(npm --version)
    echo -e "${GREEN}✅ npm $NPM_VERSION found${NC}"
fi

# Option to use Docker or local
print_section "Startup Options"

echo "Choose how to start the services:"
echo "1) Docker (Recommended - requires Docker & Docker Compose)"
echo "2) Local Development (requires PostgreSQL, Redis, Node.js, Python)"
echo ""
read -p "Enter choice (1 or 2): " choice

case $choice in
    1)
        print_section "Starting with Docker Compose"
        
        if ! command -v docker-compose &> /dev/null; then
            echo -e "${RED}❌ Docker Compose not found${NC}"
            exit 1
        fi
        
        docker-compose up -d
        
        echo -e "${GREEN}✅ Services started with Docker Compose${NC}"
        echo ""
        echo "Access services at:"
        echo "  Backend API: http://localhost:8000"
        echo "  API Docs: http://localhost:8000/docs"
        echo "  Web: http://localhost:3000 (after running npm start in web/)"
        echo ""
        echo "To view logs:"
        echo "  docker-compose logs -f backend"
        
        ;;
    2)
        print_section "Starting Local Development Services"
        
        # Check if PostgreSQL is running
        echo "Checking PostgreSQL..."
        if ! pg_isready -h localhost -p 5432 &> /dev/null; then
            echo -e "${RED}❌ PostgreSQL not running on localhost:5432${NC}"
            echo "Start PostgreSQL with: brew services start postgresql"
            exit 1
        fi
        echo -e "${GREEN}✅ PostgreSQL is running${NC}"
        
        # Check if Redis is running
        echo "Checking Redis..."
        if ! redis-cli ping &> /dev/null; then
            echo -e "${RED}❌ Redis not running on localhost:6379${NC}"
            echo "Start Redis with: brew services start redis"
            exit 1
        fi
        echo -e "${GREEN}✅ Redis is running${NC}"
        
        # Start Backend
        print_section "Starting Backend Server"
        cd backend
        
        if [ ! -d "venv" ]; then
            echo "Creating virtual environment..."
            python3 -m venv venv
        fi
        
        source venv/bin/activate
        
        if [ ! -f ".env" ]; then
            echo "Creating .env file..."
            cp .env.example .env
            echo -e "${YELLOW}⚠️  Edit .env with your configuration${NC}"
        fi
        
        pip install -r requirements.txt
        
        echo -e "${GREEN}✅ Starting backend on http://localhost:8000${NC}"
        python main.py &
        BACKEND_PID=$!
        
        cd ..
        
        sleep 3
        
        # Start Web Frontend
        print_section "Starting Web Frontend"
        cd web
        
        npm install --silent
        
        echo -e "${GREEN}✅ Starting web on http://localhost:3000${NC}"
        npm start &
        WEB_PID=$!
        
        cd ..
        
        sleep 5
        
        # Start Mobile
        print_section "Starting Mobile App"
        cd mobile
        
        npm install --silent
        
        echo -e "${GREEN}✅ Starting mobile (Expo)${NC}"
        echo "Choose platform when prompted:"
        echo "  - Press 'a' for Android"
        echo "  - Press 'i' for iOS"
        echo "  - Press 'w' for web"
        
        expo start &
        MOBILE_PID=$!
        
        cd ..
        
        # Cleanup on exit
        trap "kill $BACKEND_PID $WEB_PID $MOBILE_PID 2>/dev/null" EXIT
        
        echo ""
        echo -e "${GREEN}════════════════════════════════════════════════${NC}"
        echo -e "${GREEN}✅ All services started!${NC}"
        echo -e "${GREEN}════════════════════════════════════════════════${NC}"
        echo ""
        echo "Access services at:"
        echo "  Backend API: http://localhost:8000"
        echo "  API Docs: http://localhost:8000/docs"
        echo "  Web: http://localhost:3000"
        echo "  Mobile: Check Expo terminal"
        echo ""
        echo "Press Ctrl+C to stop all services"
        echo ""
        
        wait
        ;;
    *)
        echo -e "${RED}Invalid choice${NC}"
        exit 1
        ;;
esac
