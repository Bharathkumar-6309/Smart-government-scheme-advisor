# Run Commands Guide

## 🚀 Quick Start

### Option 1: Docker Compose (Recommended)

```bash
# Clone the repository
git clone <repository-url>
cd Smart-Government-Scheme-Advisor

# Start development environment
docker-compose up -d

# View logs
docker-compose logs -f

# Stop services
docker-compose down
```

### Option 2: Local Development

```bash
# Clone the repository
git clone <repository-url>
cd Smart-Government-Scheme-Advisor

# Backend setup
cd app/backend
python -m venv venv
venv\Scripts\activate  # Windows
source venv/bin/activate  # macOS/Linux
pip install -r requirements.txt
python main.py

# Frontend setup (new terminal)
cd app/frontend
npm install
npm run dev
```

## 🐳 Docker Commands

### Development Environment

```bash
# Start all services
docker-compose up -d

# Start specific service
docker-compose up -d backend
docker-compose up -d frontend

# View logs
docker-compose logs -f
docker-compose logs -f backend
docker-compose logs -f frontend

# Stop services
docker-compose down

# Rebuild and start
docker-compose up --build -d

# Clean up
docker-compose down -v
docker system prune -f
```

### Production Environment

```bash
# Start production services
docker-compose -f docker-compose.prod.yml up -d

# Start with nginx reverse proxy
docker-compose -f docker-compose.prod.yml --profile nginx up -d

# View production logs
docker-compose -f docker-compose.prod.yml logs -f

# Stop production services
docker-compose -f docker-compose.prod.yml down
```

### Docker Management

```bash
# List running containers
docker ps

# List all containers
docker ps -a

# View container logs
docker logs <container_id>

# Execute command in container
docker exec -it <container_id> bash

# Remove all containers
docker container rm -f $(docker container ls -aq)

# Remove all images
docker image rm -f $(docker image ls -aq)
```

## 🖥️ Local Development Commands

### Backend Commands

```bash
# Navigate to backend
cd app/backend

# Create virtual environment
python -m venv venv

# Activate virtual environment
# Windows
venv\Scripts\activate
# macOS/Linux
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Run backend server
python main.py

# Run simplified backend (if main.py has issues)
python main_simple.py

# Initialize RAG system
python test_ingestion.py

# Run tests
pytest tests/ -v

# Run tests with coverage
pytest tests/ --cov=rag --cov-report=html
```

### Frontend Commands

```bash
# Navigate to frontend
cd app/frontend

# Install dependencies
npm install

# Start development server
npm run dev

# Build for production
npm run build

# Run tests
npm test

# Run tests with coverage
npm run test:coverage

# Preview production build
npm run preview

# Type checking
npm run type-check

# Linting
npm run lint
```

## 🔧 Environment Setup

### Backend Environment Variables

Create `.env` file in `app/backend/`:

```env
# OpenAI API Key (optional)
OPENAI_API_KEY=your_openai_api_key_here

# Server Configuration
PORT=8000
CORS_ORIGINS=http://localhost:5173,http://127.0.0.1:5173

# Logging
LOG_LEVEL=info
```

### Frontend Environment Variables

Create `.env` file in `app/frontend/`:

```env
# API Configuration
VITE_API_URL=http://localhost:8000

# App Configuration
VITE_APP_NAME=Smart Government Scheme Advisor
```

## 🧪 Testing Commands

### Backend Testing

```bash
cd app/backend

# Run all tests
pytest tests/ -v

# Run specific test file
pytest tests/test_api.py -v

# Run with coverage
pytest tests/ --cov=rag --cov-report=html

# Run tests with specific pattern
pytest tests/ -k "test_search" -v

# Run tests in parallel
pytest tests/ -n auto
```

### Frontend Testing

```bash
cd app/frontend

# Run tests
npm test

# Run tests in watch mode
npm test -- --watch

# Run tests with coverage
npm run test:coverage

# Run tests for specific file
npm test -- Advisor.test.tsx
```

## 📊 Monitoring Commands

### Health Checks

```bash
# Backend health check
curl http://localhost:8000/api/health

# Frontend health check
curl http://localhost:5173

# Docker health check
docker-compose ps
```

### Log Monitoring

```bash
# Docker logs
docker-compose logs -f

# Backend logs
docker-compose logs -f backend

# Frontend logs
docker-compose logs -f frontend

# Real-time logs with filtering
docker-compose logs -f backend | grep "ERROR"
```

### Performance Monitoring

```bash
# Check resource usage
docker stats

# Check container resource usage
docker stats <container_id>

# Check disk usage
docker system df

# Check network connections
netstat -an | grep :8000
netstat -an | grep :5173
```

## 🔄 Development Workflow

### Daily Development

```bash
# 1. Start services
docker-compose up -d

# 2. Check status
docker-compose ps

# 3. View logs if needed
docker-compose logs -f

# 4. Make changes to code

# 5. Rebuild if needed
docker-compose up --build -d

# 6. Run tests
docker-compose exec backend pytest tests/ -v
docker-compose exec frontend npm test

# 7. Stop when done
docker-compose down
```

### Code Changes

```bash
# After backend changes
docker-compose up --build backend -d

# After frontend changes
docker-compose up --build frontend -d

# After dependency changes
docker-compose up --build -d
```

### Debugging

```bash
# Enter backend container
docker exec -it scheme-advisor-backend-1 bash

# Enter frontend container
docker exec -it scheme-advisor-frontend-1 sh

# Check container processes
docker exec -it <container_id> ps aux

# Check environment variables
docker exec -it <container_id> env
```

## 🚀 Production Deployment

### Production Build

```bash
# Build production images
docker-compose -f docker-compose.prod.yml build

# Start production services
docker-compose -f docker-compose.prod.yml up -d

# Check production status
docker-compose -f docker-compose.prod.yml ps

# View production logs
docker-compose -f docker-compose.prod.yml logs -f
```

### Production Monitoring

```bash
# Check service health
curl http://localhost:3000/health
curl http://localhost:8000/api/health

# Monitor resource usage
docker stats

# Check logs for errors
docker-compose -f docker-compose.prod.yml logs -f | grep "ERROR"
```

## 🛠️ Troubleshooting Commands

### Common Issues

```bash
# Port conflicts
netstat -an | grep :8000
netstat -an | grep :5173

# Docker issues
docker system prune -f
docker volume prune -f

# Permission issues
sudo chown -R $USER:$USER ./

# Clean restart
docker-compose down -v
docker-compose up --build -d
```

### Debug Mode

```bash
# Run backend in debug mode
docker-compose -f docker-compose.yml run --rm backend python main.py --debug

# Run frontend in debug mode
docker-compose -f docker-compose.yml run --rm frontend npm run dev --debug
```

### Reset Environment

```bash
# Complete reset
docker-compose down -v
docker system prune -f
docker volume prune -f
docker-compose up --build -d
```

## 📱 Access URLs

### Development Environment
- **Frontend**: http://localhost:5173
- **Backend API**: http://localhost:8000
- **API Health**: http://localhost:8000/api/health

### Production Environment
- **Frontend**: http://localhost:3000
- **Backend API**: http://localhost:8000
- **API Health**: http://localhost:8000/api/health

## 🎯 Quick Verification

After starting services, verify everything works:

```bash
# Check services are running
docker-compose ps

# Test API health
curl http://localhost:8000/api/health

# Test frontend
curl http://localhost:5173

# Open browser
# http://localhost:5173
```

## 📝 Notes

- Use `docker-compose up -d` for detached mode
- Use `docker-compose logs -f` to follow logs
- Use `Ctrl+C` to stop following logs
- Use `docker-compose down` to stop all services
- Use `--build` flag to rebuild images
- Use `--force-recreate` to recreate containers

For production deployment, use `docker-compose.prod.yml` instead of `docker-compose.yml`.
