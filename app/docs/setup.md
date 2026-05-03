# Setup Documentation

## Prerequisites

### System Requirements

- **Python**: 3.14 (recommended)
- **Node.js**: 18.0.0 or higher
- **npm**: 8.0.0 or higher
- **Git**: For version control

### Optional Requirements

- **Docker**: 20.0.0 or higher (for containerized deployment)
- **OpenAI API Key**: For LLM functionality (optional, has fallback)

## Installation

### 1. Clone the Repository

```bash
git clone <repository-url>
cd Smart-Government-Scheme-Advisor
```

### 2. Backend Setup

#### Navigate to Backend Directory
```bash
cd app/backend
```

#### Create Virtual Environment
```bash
python -m venv venv

# Windows
venv\Scripts\activate

# macOS/Linux
source venv/bin/activate
```

#### Install Dependencies
```bash
pip install -r requirements.txt
```

#### Backend Dependencies
```
faiss-cpu==1.13.2          # Vector similarity search
sentence-transformers==2.2.2 # Text embeddings
numpy==2.0.2                # Numerical operations
torch==2.11.0               # Deep learning framework
openai==1.30.1              # OpenAI API client
```

#### Environment Variables (Optional)
Create a `.env` file in the backend directory:
```env
OPENAI_API_KEY=your_openai_api_key_here
```

### 3. Frontend Setup

#### Navigate to Frontend Directory
```bash
cd app/frontend
```

#### Install Dependencies
```bash
npm install
```

#### Frontend Dependencies
```json
{
  "react": "^18.2.0",
  "react-dom": "^18.2.0",
  "react-router-dom": "^6.8.1",
  "typescript": "^5.0.2",
  "vite": "^4.3.9",
  "tailwindcss": "^3.3.0"
}
```

## Data Setup

### 1. Scheme Data

The system uses JSON files for scheme data:

```bash
app/data/
├── schemes.json          # Main scheme data
├── vector_store.faiss    # FAISS index (auto-generated)
└── vector_store.pkl      # Metadata (auto-generated)
```

### 2. Initialize RAG System

Run the initialization script to create vector embeddings:

```bash
cd app/backend
python test_ingestion.py
```

This will:
- Load scheme data from `schemes.json`
- Process text and create chunks
- Generate embeddings
- Build FAISS index
- Save vector store files

## Development Setup

### 1. Start Backend Server

```bash
cd app/backend
python main.py
```

The backend will start on `http://localhost:8000`

### 2. Start Frontend Development Server

```bash
cd app/frontend
npm run dev
```

The frontend will start on `http://localhost:5173`

### 3. Verify Setup

#### Backend Health Check
```bash
curl http://localhost:8000/api/health
```

Expected response:
```json
{
  "status": "healthy",
  "timestamp": "2026-05-02T23:30:00.000Z",
  "app": "Smart Government Scheme Advisor",
  "version": "1.0.0"
}
```

#### Frontend Access
Open `http://localhost:5173` in your browser

## Testing Setup

### Backend Testing

#### Install Test Dependencies
```bash
cd app/backend
pip install pytest pytest-asyncio
```

#### Run Tests
```bash
cd app/backend
pytest tests/ -v
```

#### Test Coverage
```bash
pytest tests/ --cov=rag --cov-report=html
```

### Frontend Testing

#### Run Frontend Tests
```bash
cd app/frontend
npm test
```

#### Test Coverage
```bash
npm run test:coverage
```

## Docker Setup

### 1. Build Docker Images

```bash
# Backend Docker Image
cd app/backend
docker build -t scheme-advisor-backend .

# Frontend Docker Image
cd app/frontend
docker build -t scheme-advisor-frontend .
```

### 2. Run with Docker Compose

```bash
cd app
docker-compose up -d
```

This will start:
- Backend on `http://localhost:8000`
- Frontend on `http://localhost:3000`

### 3. Docker Compose Configuration

The `docker-compose.yml` includes:
- **Backend Service**: Python HTTP server with RAG system
- **Frontend Service**: Nginx serving React build
- **Volume Mounts**: For data persistence
- **Environment Variables**: For configuration

## Production Setup

### 1. Environment Configuration

#### Backend Environment Variables
```env
# Production
NODE_ENV=production
PORT=8000
CORS_ORIGINS=https://yourdomain.com

# Optional
OPENAI_API_KEY=your_production_api_key
LOG_LEVEL=info
```

#### Frontend Environment Variables
```env
# Production
VITE_API_URL=https://api.yourdomain.com
VITE_APP_NAME=Smart Government Scheme Advisor
```

### 2. Build for Production

#### Backend
```bash
cd app/backend
python -m py_compile *.py
```

#### Frontend
```bash
cd app/frontend
npm run build
```

### 3. Production Deployment

#### Option 1: Docker
```bash
docker-compose -f docker-compose.prod.yml up -d
```

#### Option 2: Manual Deployment
```bash
# Backend
cd app/backend
gunicorn main:app --host 0.0.0.0 --port 8000

# Frontend (Nginx configuration required)
cd app/frontend
npm run build
# Serve build/ directory with Nginx
```

## Troubleshooting

### Common Issues

#### 1. Backend Import Errors
**Problem**: `ImportError: cannot import name 'cached_download'`

**Solution**: The system includes mock fallbacks for compatibility issues. The mock embedding service will work without sentence-transformers.

#### 2. Frontend Build Errors
**Problem**: TypeScript compilation errors

**Solution**: Check `tsconfig.json` and ensure all dependencies are installed:
```bash
npm install
npm run build
```

#### 3. CORS Issues
**Problem**: Frontend cannot connect to backend

**Solution**: Ensure backend CORS headers include your frontend URL:
```python
CORS_ORIGINS = ["http://localhost:5173", "http://127.0.0.1:5173"]
```

#### 4. Vector Store Issues
**Problem**: FAISS index not found

**Solution**: Run the initialization script:
```bash
cd app/backend
python test_ingestion.py
```

#### 5. OpenAI API Issues
**Problem**: LLM service not working

**Solution**: Set up OpenAI API key or use mock mode:
```env
OPENAI_API_KEY=your_key_here
```

### Debug Mode

#### Backend Debugging
```bash
cd app/backend
python main.py --debug
```

#### Frontend Debugging
```bash
cd app/frontend
npm run dev
```

Open browser developer tools for debugging.

### Log Files

#### Backend Logs
```bash
# Real-time logs
tail -f app/backend/logs/app.log

# Error logs
tail -f app/backend/logs/error.log
```

#### Frontend Logs
Check browser console for frontend logs.

## Performance Optimization

### Backend Optimization

1. **Vector Store**: Use appropriate FAISS index type
2. **Caching**: Implement Redis for frequent queries
3. **Batch Processing**: Process embeddings in batches

### Frontend Optimization

1. **Code Splitting**: Implement lazy loading
2. **Bundle Size**: Use Webpack bundle analyzer
3. **Caching**: Implement service worker caching

## Security Considerations

### Backend Security

1. **API Keys**: Store in environment variables
2. **Input Validation**: Validate all user inputs
3. **Rate Limiting**: Implement request rate limiting
4. **HTTPS**: Use SSL/TLS in production

### Frontend Security

1. **CSP**: Implement Content Security Policy
2. **XSS Protection**: Sanitize user inputs
3. **Authentication**: Implement user authentication

## Monitoring

### Health Checks

```bash
# Backend health
curl http://localhost:8000/api/health

# Frontend health
curl http://localhost:5173
```

### Performance Monitoring

1. **Response Times**: Monitor API response times
2. **Error Rates**: Track error percentages
3. **Resource Usage**: Monitor CPU and memory usage

### Logging

Configure structured logging for production:
```python
import logging

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('app.log'),
        logging.StreamHandler()
    ]
)
```

## Backup and Recovery

### Data Backup

1. **Scheme Data**: Backup `schemes.json`
2. **Vector Store**: Backup `.faiss` and `.pkl` files
3. **Configuration**: Backup environment files

### Recovery Process

1. Restore data files
2. Rebuild vector store if needed
3. Restart services
4. Verify functionality

## Maintenance

### Regular Tasks

1. **Update Dependencies**: Keep packages updated
2. **Security Patches**: Apply security updates
3. **Data Updates**: Keep scheme data current
4. **Performance Reviews**: Monitor and optimize performance

### Monitoring Alerts

Set up alerts for:
- Service downtime
- High error rates
- Performance degradation
- Security incidents
