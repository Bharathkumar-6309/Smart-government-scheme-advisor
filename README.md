# Smart Government Scheme Advisor

A production-ready RAG-based government scheme advisor that helps Indian citizens find and apply for relevant government schemes using AI-powered search and personalized recommendations.

## 🚀 Features

- **🤖 RAG-Powered Search**: Retrieval-Augmented Generation for accurate scheme recommendations
- **🎯 Personalized Recommendations**: AI-driven suggestions based on user profile
- **🔍 Advanced Filtering**: Filter by state, category, and income criteria
- **📊 Confidence Scoring**: Match percentages and similarity scores
- **🎨 Modern UI**: Responsive React frontend with Tailwind CSS
- **🐳 Docker Support**: Containerized deployment ready
- **📚 Comprehensive Docs**: Full API and architecture documentation

## 🏗️ Architecture

```
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│   Frontend      │    │   Backend       │    │   Data Layer    │
│                 │    │                 │    │                 │
│ React + TS      │◄──►│ Python HTTP     │◄──►│ JSON Schemes    │
│ Tailwind CSS    │    │ RAG Services    │    │ FAISS Index     │
│ React Router    │    │ OpenAI API      │    │ Metadata Store  │
└─────────────────┘    └─────────────────┘    └─────────────────┘
```

## 📋 Prerequisites

- **Python**: 3.14 (recommended)
- **Node.js**: 18.0.0 or higher
- **npm**: 8.0.0 or higher
- **Git**: For version control
- **Docker**: 20.0.0 or higher (optional)

## 🚀 Quick Start

### 1. Clone the Repository

```bash
git clone <repository-url>
cd Smart-Government-Scheme-Advisor
```

### 2. Backend Setup

```bash
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

# Start backend server
python main.py
```

Backend will be available at `http://localhost:8000`

### 3. Frontend Setup

```bash
cd app/frontend

# Install dependencies
npm install

# Start development server
npm run dev
```

Frontend will be available at `http://localhost:5173`

### 4. Initialize RAG System

```bash
cd app/backend
python test_ingestion.py
```

This will create the vector embeddings and FAISS index for scheme search.

## 🐳 Docker Setup

### Using Docker Compose

```bash
cd app
docker-compose up -d
```

This will start:
- Backend on `http://localhost:8000`
- Frontend on `http://localhost:3000`

### Manual Docker Build

```bash
# Backend
cd app/backend
docker build -t scheme-advisor-backend .

# Frontend
cd app/frontend
docker build -t scheme-advisor-frontend .

# Run containers
docker run -p 8000:8000 scheme-advisor-backend
docker run -p 3000:3000 scheme-advisor-frontend
```

## 📖 Documentation

- **[Architecture](app/docs/architecture.md)** - System architecture and design
- **[API Documentation](app/docs/api.md)** - Complete API reference
- **[Setup Guide](app/docs/setup.md)** - Detailed setup instructions
- **[RAG Explained](app/docs/rag-explained.md)** - RAG system deep dive

## 🔧 Configuration

### Environment Variables

Create a `.env` file in `app/backend/`:

```env
# OpenAI API Key (optional, has fallback)
OPENAI_API_KEY=your_openai_api_key_here

# Backend Configuration
PORT=8000
CORS_ORIGINS=http://localhost:5173,http://127.0.0.1:5173

# Logging
LOG_LEVEL=info
```

### Frontend Configuration

Create a `.env` file in `app/frontend/`:

```env
# API URL
VITE_API_URL=http://localhost:8000

# App Configuration
VITE_APP_NAME=Smart Government Scheme Advisor
```

## 🧪 Testing

### Backend Tests

```bash
cd app/backend

# Install test dependencies
pip install pytest pytest-asyncio

# Run tests
pytest tests/ -v

# Test coverage
pytest tests/ --cov=rag --cov-report=html
```

### Frontend Tests

```bash
cd app/frontend

# Run tests
npm test

# Test coverage
npm run test:coverage
```

## 📊 API Endpoints

### Health Check
```bash
GET /api/health
```

### Scheme Search
```bash
POST /api/schemes/search
Content-Type: application/json

{
  "query": "scholarship for engineering students",
  "user_profile": {
    "age": 21,
    "income": 250000,
    "occupation": "student",
    "education": "engineering",
    "state": "Karnataka"
  },
  "filters": {
    "category": "education",
    "income_limit": 300000
  }
}
```

### Personalized Recommendations
```bash
POST /api/schemes/recommend
Content-Type: application/json

{
  "user_profile": {
    "age": 25,
    "income": 400000,
    "occupation": "private employee",
    "education": "graduate",
    "state": "Delhi"
  },
  "max_recommendations": 5
}
```

## 🎯 Sample Queries

### Basic Search
- "scholarship for students"
- "housing loan subsidy"
- "agriculture financial assistance"
- "skill development programs"

### Profile-Based Recommendations
- Age: 21, Income: ₹2,50,000, Occupation: Student
- Age: 35, Income: ₹6,00,000, Occupation: Private Employee
- Age: 45, Income: ₹1,80,000, Occupation: Farmer

### Filtered Search
- Category: "education", State: "Maharashtra"
- Category: "agriculture", Income Limit: ₹3,00,000
- Category: "housing", State: "All India"

## 🏗️ Project Structure

```
Smart-Government-Scheme-Advisor/
├── app/
│   ├── frontend/                 # React frontend
│   │   ├── src/
│   │   │   ├── pages/           # Page components
│   │   │   ├── App.tsx          # Main app component
│   │   │   └── index.css        # Global styles
│   │   ├── package.json
│   │   └── Dockerfile
│   ├── backend/                  # Python backend
│   │   ├── rag/                 # RAG services
│   │   │   ├── embedding_service.py
│   │   │   ├── vector_store_service.py
│   │   │   ├── retriever_service.py
│   │   │   ├── llm_service.py
│   │   │   └── recommendation_service.py
│   │   ├── ingestion/           # Data processing
│   │   │   ├── data_loader.py
│   │   │   ├── text_processor.py
│   │   │   └── chunker.py
│   │   ├── main.py              # Main server
│   │   ├── requirements.txt
│   │   └── Dockerfile
│   ├── data/                    # Data files
│   │   ├── schemes.json         # Scheme data
│   │   ├── vector_store.faiss   # FAISS index
│   │   └── vector_store.pkl     # Metadata
│   └── docs/                    # Documentation
│       ├── architecture.md
│       ├── api.md
│       ├── setup.md
│       └── rag-explained.md
├── docker-compose.yml
└── README.md
```

## 🛠️ Technology Stack

### Frontend
- **React 18** - UI framework
- **TypeScript** - Type safety
- **Tailwind CSS** - Utility-first CSS
- **React Router** - Navigation
- **Vite** - Build tool

### Backend
- **Python 3.14** - Backend language
- **FAISS** - Vector similarity search
- **Sentence Transformers** - Text embeddings
- **OpenAI API** - LLM integration
- **JSON** - Data storage

### Infrastructure
- **Docker** - Containerization
- **Docker Compose** - Multi-container orchestration
- **HTTP Server** - Built-in Python server

## 🔍 RAG System Details

### Components
1. **Embedding Service**: Text to vector conversion
2. **Vector Store**: FAISS-based similarity search
3. **Retriever Service**: RAG orchestration
4. **LLM Service**: OpenAI integration
5. **Recommendation Service**: Personalization engine

### Data Flow
```
User Query → Embedding → Vector Search → Context Retrieval → LLM Generation → Response
```

### Features
- **Semantic Search**: Understand query meaning
- **Contextual Responses**: Based on retrieved schemes
- **Personalization**: User profile integration
- **Confidence Scoring**: Match quality indicators

## 🚀 Deployment

### Production Setup

1. **Environment Configuration**
   ```bash
   # Backend
   NODE_ENV=production
   PORT=8000
   
   # Frontend
   VITE_API_URL=https://api.yourdomain.com
   ```

2. **Build for Production**
   ```bash
   # Frontend
   cd app/frontend
   npm run build
   
   # Backend
   cd app/backend
   python -m py_compile *.py
   ```

3. **Docker Deployment**
   ```bash
   docker-compose -f docker-compose.prod.yml up -d
   ```

### Monitoring

- **Health Check**: `GET /api/health`
- **Performance**: Response time tracking
- **Logging**: Structured logging system

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests for new functionality
5. Submit a pull request

## 📝 License

MIT License - see [LICENSE](LICENSE) file for details

## 🆘 Support

For issues and questions:
1. Check the [documentation](app/docs/)
2. Review [common issues](app/docs/setup.md#troubleshooting)
3. Create an issue in the repository

## 🔮 Future Enhancements

- **Multi-Modal RAG**: Include images and documents
- **User Accounts**: Personalized recommendation history
- **Real-time Updates**: Live scheme updates
- **Advanced Analytics**: Usage tracking and optimization
- **Mobile App**: React Native implementation

---

**Built with ❤️ for Indian citizens to access government schemes easily**
