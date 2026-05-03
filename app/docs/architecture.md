# Architecture Documentation

## System Overview

The Smart Government Scheme Advisor is a RAG (Retrieval-Augmented Generation) based system that provides personalized government scheme recommendations to Indian citizens.

## High-Level Architecture

```
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│   Frontend      │    │   Backend       │    │   Data Layer    │
│                 │    │                 │    │                 │
│ React + TS      │◄──►│ Python HTTP     │◄──►│ JSON Schemes    │
│ Tailwind CSS    │    │ RAG Services    │    │ FAISS Index     │
│ React Router    │    │ OpenAI API      │    │ Metadata Store  │
└─────────────────┘    └─────────────────┘    └─────────────────┘
```

## Frontend Architecture

### Technology Stack
- **React 18** with TypeScript
- **React Router** for navigation
- **Tailwind CSS** for styling
- **Vite** for build tooling

### Component Structure
```
src/
├── App.tsx              # Main app with routing
├── pages/
│   ├── Home.tsx         # Landing page
│   ├── Advisor.tsx      # Main advisor interface
│   └── About.tsx        # About page
└── index.css           # Global styles
```

### Key Features
- **Responsive Design**: Mobile-first approach
- **Form Handling**: User profile input with validation
- **API Integration**: Backend connectivity with error handling
- **Results Display**: Interactive scheme cards with detailed information

## Backend Architecture

### Technology Stack
- **Python 3.14** with HTTP server
- **FAISS** for vector similarity search
- **Sentence Transformers** for embeddings
- **OpenAI API** for response generation
- **JSON** for data storage

### Service Architecture
```
rag/
├── embedding_service.py    # Text embeddings
├── vector_store_service.py # FAISS operations
├── retriever_service.py    # RAG orchestration
├── llm_service.py         # OpenAI integration
└── recommendation_service.py # Personalization
```

### Data Flow
1. **User Input** → Form data collection
2. **Filtering** → Pre-RAG scheme filtering
3. **Embedding** → Query vector generation
4. **Search** → FAISS similarity search
5. **LLM** → Structured response generation
6. **Response** → Formatted JSON output

## RAG System Architecture

### Retrieval Pipeline
```
Query → Embedding → Vector Search → Scheme Retrieval → LLM Generation → Response
```

### Key Components

#### Embedding Service
- **Model**: all-MiniLM-L6-v2 (384 dimensions)
- **Mock Fallback**: Hash-based embeddings for compatibility
- **Batch Processing**: Efficient embedding generation

#### Vector Store Service
- **Index Types**: Flat, IVF, HNSW (default: Flat)
- **Storage**: FAISS index + metadata pickle files
- **Operations**: Add, search, save, load

#### Retriever Service
- **Filtering**: State, category, income-based pre-filtering
- **Deduplication**: Scheme grouping and result consolidation
- **LLM Integration**: Structured response generation

#### LLM Service
- **Model**: GPT-3.5-turbo
- **Prompt Engineering**: System and user prompts for structured output
- **Fallback Mode**: Mock responses when API unavailable

#### Recommendation Service
- **Profile Analysis**: Multi-dimensional user assessment
- **Scoring**: Eligibility and benefit alignment scores
- **Personalization**: Custom reasoning and next steps

## Data Architecture

### Scheme Data Structure
```json
{
  "id": "unique_identifier",
  "name": "scheme_name",
  "description": "detailed_description",
  "category": "scheme_category",
  "benefits": "benefits_description",
  "documents_required": ["doc1", "doc2"],
  "eligibility_criteria": ["criteria1", "criteria2"],
  "state": "state_name",
  "income_limit": 500000,
  "official_link": "https://example.com"
}
```

### Vector Store Schema
- **Index**: FAISS vector index (384D embeddings)
- **Metadata**: Scheme information and chunk mappings
- **Persistence**: `.faiss` and `.pkl` files

### API Response Schema
```json
{
  "success": true,
  "message": "operation_result",
  "data": [scheme_objects],
  "total_results": 3,
  "search_time": 0.001,
  "search_method": "rag_llm"
}
```

## Security Architecture

### Frontend Security
- **CORS**: Enabled for frontend-backend communication
- **Input Validation**: Form data validation and sanitization
- **Error Handling**: Graceful error display without sensitive information

### Backend Security
- **API Keys**: Environment variable configuration
- **Input Validation**: Request body validation
- **Error Handling**: Sanitized error responses

### Data Security
- **Local Storage**: JSON files for scheme data
- **API Keys**: OpenAI key in environment variables
- **No PII**: No personally identifiable information stored

## Performance Architecture

### Frontend Performance
- **Lazy Loading**: Component-based loading
- **Caching**: Browser caching for static assets
- **Optimization**: Tailwind CSS purging in production

### Backend Performance
- **Vector Search**: FAISS for efficient similarity search
- **Caching**: In-memory caching for frequent queries
- **Batch Processing**: Efficient embedding generation

### Scalability Considerations
- **Horizontal Scaling**: Multiple backend instances
- **Database**: Migration to PostgreSQL for larger datasets
- **CDN**: Static asset delivery optimization

## Deployment Architecture

### Development Environment
- **Frontend**: `npm run dev` on localhost:5173
- **Backend**: `python main.py` on localhost:8000
- **Hot Reload**: Both frontend and backend support live reloading

### Production Environment
- **Docker**: Containerized deployment
- **Environment Variables**: Configuration management
- **Monitoring**: Health checks and logging

### Docker Architecture
```
┌─────────────────┐    ┌─────────────────┐
│ Frontend Docker │    │ Backend Docker  │
│                 │    │                 │
│ Node.js + Vite  │◄──►│ Python + HTTP  │
│ Nginx (optional)│    │ FAISS + OpenAI  │
└─────────────────┘    └─────────────────┘
```

## Monitoring & Logging

### Logging Strategy
- **Frontend**: Browser console for development
- **Backend**: Structured logging with timestamps
- **API Requests**: Request/response logging

### Health Monitoring
- **Health Endpoint**: `/api/health` for service status
- **Performance Metrics**: Response time tracking
- **Error Tracking**: Comprehensive error logging

## Future Architecture Considerations

### Scalability Enhancements
- **Database Migration**: PostgreSQL for scheme data
- **Microservices**: Separate services for different functionalities
- **Load Balancing**: Multiple backend instances

### Feature Enhancements
- **Real-time Updates**: WebSocket for live scheme updates
- **User Accounts**: Personalized recommendations history
- **Analytics**: Usage tracking and optimization

### Technology Upgrades
- **Frontend Framework**: Next.js for SSR/SSG
- **Backend Framework**: FastAPI for better performance
- **Vector Database**: Pinecone or Weaviate for production scale
