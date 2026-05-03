# RAG System Explained

## Overview

RAG (Retrieval-Augmented Generation) is an AI architecture that combines information retrieval with language model generation. Our Smart Government Scheme Advisor uses RAG to provide accurate, contextual scheme recommendations based on user queries and profiles.

## How RAG Works

### Traditional LLM vs RAG

**Traditional LLM:**
- Relies solely on training data
- May hallucinate or provide outdated information
- Limited knowledge of specific, recent schemes

**RAG System:**
- Retrieves relevant information from knowledge base
- Augments LLM with current, accurate data
- Provides verifiable, contextual responses

### Our RAG Pipeline

```
User Query → Embedding → Vector Search → Context Retrieval → LLM Generation → Response
```

## Components

### 1. Embedding Service

**Purpose**: Convert text into numerical vectors for similarity search

**How it works:**
- Uses sentence-transformers model (all-MiniLM-L6-v2)
- Converts queries and scheme text into 384-dimensional vectors
- Captures semantic meaning and context

**Code Example:**
```python
from rag.embedding_service import EmbeddingService

# Initialize embedding service
embedding_service = EmbeddingService()

# Generate query embedding
query_vector = embedding_service.embed_text("scholarship for engineering students")

# Generate batch embeddings
scheme_vectors = embedding_service.embed_texts(scheme_texts)
```

**Fallback System**: When sentence-transformers is unavailable, uses hash-based mock embeddings for compatibility.

### 2. Vector Store Service

**Purpose**: Store and search vector embeddings efficiently

**How it works:**
- Uses FAISS (Facebook AI Similarity Search) library
- Supports multiple index types (Flat, IVF, HNSW)
- Enables fast similarity search across thousands of vectors

**Index Types:**
- **Flat Index**: Exact search, best for small datasets
- **IVF Index**: Inverted File, faster for larger datasets
- **HNSW Index**: Hierarchical Navigable Small World, best for production

**Code Example:**
```python
from rag.vector_store_service import VectorStoreService

# Initialize vector store
vector_store = VectorStoreService(embedding_dimension=384)

# Add embeddings
vector_store.add_embeddings(embeddings, metadata)

# Search for similar vectors
results = vector_store.search(query_vector, top_k=10)
```

### 3. Text Processing & Chunking

**Purpose**: Prepare scheme data for embedding and retrieval

**Processing Steps:**
1. **Text Cleaning**: Remove special characters, normalize text
2. **Chunking**: Split long text into manageable pieces
3. **Metadata Addition**: Add scheme information to chunks

**Chunking Strategy:**
- Overlapping chunks (50% overlap)
- Maximum 500 characters per chunk
- Preserve context and meaning

**Code Example:**
```python
from ingestion.chunker import TextChunker

# Initialize chunker
chunker = TextChunker(chunk_size=500, overlap=250)

# Create chunks from scheme
chunks = chunker.chunk_scheme(scheme_data)
```

### 4. Retriever Service

**Purpose**: Orchestrate the RAG pipeline and coordinate components

**Key Functions:**
- Initialize all RAG components
- Handle filtering (state, category, income)
- Perform similarity search
- Group and deduplicate results

**Filtering Logic:**
```python
def _apply_filters(self, filters):
    # State filtering
    if filters.get('state'):
        schemes = [s for s in schemes if s['state'] == filters['state']]
    
    # Category filtering
    if filters.get('category'):
        schemes = [s for s in schemes if s['category'] == filters['category']]
    
    # Income filtering
    if filters.get('income_limit'):
        schemes = [s for s in schemes if s['income_limit'] <= filters['income_limit']]
```

### 5. LLM Service

**Purpose**: Generate structured, human-readable responses

**How it works:**
- Uses OpenAI GPT-3.5-turbo model
- Provides context from retrieved schemes
- Generates structured JSON responses
- Includes personalized explanations

**Prompt Engineering:**
```python
system_prompt = """You are a helpful government scheme advisor assistant.
Use ONLY the information provided in the context.
Generate structured JSON response with exact format specified.
Do not hallucinate or make up information."""
```

**Response Format:**
```json
{
  "schemes": [
    {
      "name": "scheme_name",
      "why_eligible": "explanation",
      "benefits": "key benefits",
      "how_to_apply": "steps",
      "documents": ["doc1", "doc2"],
      "confidence_score": 0.85
    }
  ]
}
```

### 6. Recommendation Service

**Purpose**: Provide personalized scheme recommendations

**Personalization Features:**
- **Eligibility Scoring**: Match user profile to scheme criteria
- **Benefit Alignment**: Score scheme benefits against user needs
- **Priority Determination**: Assess application urgency
- **Next Steps**: Provide actionable guidance

**Scoring Algorithm:**
```python
def calculate_eligibility_score(user_profile, scheme):
    score = 0.5  # Base score
    
    # Age matching
    if user_age_matches_scheme(user_profile['age'], scheme):
        score += 0.3
    
    # Income matching
    if user_profile['income'] <= scheme['income_limit']:
        score += 0.3
    
    # State matching
    if user_profile['state'] == scheme['state']:
        score += 0.2
    
    return min(score, 1.0)
```

## Data Flow

### 1. Data Ingestion

```
Scheme JSON → Text Processing → Chunking → Embedding → Vector Store
```

**Steps:**
1. Load scheme data from JSON file
2. Clean and process text fields
3. Create overlapping text chunks
4. Generate embeddings for each chunk
5. Store in FAISS index with metadata

### 2. Query Processing

```
User Query → Embedding → Vector Search → Context Retrieval → LLM Generation → Response
```

**Steps:**
1. Convert user query to embedding
2. Search vector store for similar chunks
3. Group results by scheme
4. Apply user profile filters
5. Generate LLM response with context

### 3. Response Generation

```
Retrieved Schemes → Context Building → LLM Prompt → Structured Response → UI Display
```

**Steps:**
1. Format retrieved schemes as context
2. Create system and user prompts
3. Call OpenAI API with structured output
4. Parse and validate response
5. Return to frontend for display

## Performance Optimization

### Vector Search Optimization

**Index Selection:**
- **Development**: Flat index for accuracy
- **Production**: HNSW index for speed
- **Large Datasets**: IVF index for memory efficiency

**Batch Processing:**
```python
# Process embeddings in batches
batch_size = 32
for i in range(0, len(texts), batch_size):
    batch = texts[i:i+batch_size]
    embeddings = embedding_service.embed_texts(batch)
```

### Caching Strategy

**Query Caching:**
- Cache frequent query results
- TTL (Time To Live) for cache invalidation
- Redis for distributed caching

**Embedding Caching:**
- Cache text embeddings
- Reduce computation for repeated queries
- Memory-based caching for speed

## Quality Assurance

### Retrieval Quality

**Metrics:**
- **Precision**: Relevant schemes / Total retrieved
- **Recall**: Relevant schemes / All relevant schemes
- **F1 Score**: Harmonic mean of precision and recall

**Validation:**
```python
def validate_retrieval(query, expected_schemes, retrieved_schemes):
    relevant = set(expected_schemes)
    retrieved = set(retrieved_schemes)
    
    precision = len(relevant & retrieved) / len(retrieved)
    recall = len(relevant & retrieved) / len(relevant)
    
    return precision, recall
```

### Response Quality

**Validation Checks:**
- Response format validation
- Hallucination detection
- Factual accuracy verification

**Code Example:**
```python
def validate_llm_response(response, context):
    # Check if all schemes in response exist in context
    response_schemes = [s['name'] for s in response['schemes']]
    context_schemes = [s['name'] for s in context]
    
    invalid_schemes = set(response_schemes) - set(context_schemes)
    return len(invalid_schemes) == 0
```

## Scaling Considerations

### Horizontal Scaling

**Multiple Backend Instances:**
- Load balancer for request distribution
- Shared vector store (database or distributed storage)
- Session affinity for consistent user experience

**Database Migration:**
- Move from JSON to PostgreSQL for scheme data
- Use pgvector for vector storage
- Implement proper indexing and optimization

### Vector Database Options

**Production Alternatives:**
- **Pinecone**: Managed vector database
- **Weaviate**: Open-source vector database
- **Milvus**: Open-source vector database
- **Chroma**: Lightweight vector database

**Migration Strategy:**
```python
# Example migration to pgvector
def migrate_faiss_to_pgvector(faiss_index, metadata):
    # Convert FAISS index to pgvector format
    # Migrate embeddings to PostgreSQL
    # Update retrieval service to use pgvector
```

## Monitoring and Analytics

### Performance Metrics

**Key Indicators:**
- Query response time
- Embedding generation time
- LLM response time
- Vector search accuracy

**Monitoring Code:**
```python
import time

def monitor_performance(func):
    def wrapper(*args, **kwargs):
        start_time = time.time()
        result = func(*args, **kwargs)
        end_time = time.time()
        
        logger.info(f"{func.__name__}: {end_time - start_time:.3f}s")
        return result
    return wrapper
```

### Usage Analytics

**Tracking:**
- Popular search queries
- User demographics
- Scheme interaction rates
- Conversion metrics

**Analytics Dashboard:**
- Real-time usage statistics
- Performance trends
- Error rates and patterns
- User satisfaction metrics

## Future Enhancements

### Advanced RAG Features

**Multi-Modal RAG:**
- Include images and documents
- Process PDF scheme documents
- Extract information from government websites

**Conversational RAG:**
- Multi-turn conversations
- Context retention
- Follow-up question handling

**Hybrid Search:**
- Combine vector search with keyword search
- Improve relevance for specific queries
- Better handling of niche queries

### Model Improvements

**Better Embeddings:**
- Fine-tune embedding models on scheme data
- Use domain-specific models
- Implement semantic search improvements

**Advanced LLMs:**
- Use GPT-4 for better responses
- Implement fine-tuned models
- Add domain-specific instruction tuning

## Best Practices

### RAG Implementation

1. **Data Quality**: Ensure scheme data is accurate and up-to-date
2. **Chunking Strategy**: Optimize chunk size for your use case
3. **Index Selection**: Choose appropriate FAISS index type
4. **Prompt Engineering**: Craft clear, specific prompts
5. **Validation**: Implement comprehensive response validation

### Performance Optimization

1. **Batch Processing**: Process embeddings in batches
2. **Caching**: Implement intelligent caching strategies
3. **Index Optimization**: Choose appropriate index types
4. **Load Balancing**: Distribute requests across instances

### Security and Privacy

1. **API Keys**: Securely store and rotate API keys
2. **Data Privacy**: Protect user information
3. **Input Validation**: Validate all user inputs
4. **Rate Limiting**: Implement appropriate rate limits

## Troubleshooting

### Common Issues

**Poor Retrieval Quality:**
- Check embedding model performance
- Verify chunking strategy
- Improve text preprocessing

**Slow Response Times:**
- Optimize FAISS index type
- Implement caching
- Use batch processing

**LLM Hallucinations:**
- Improve prompt engineering
- Add response validation
- Use retrieval constraints

### Debug Tools

**Embedding Visualization:**
```python
import matplotlib.pyplot as plt
from sklearn.decomposition import PCA

# Visualize embeddings in 2D
pca = PCA(n_components=2)
reduced_embeddings = pca.fit_transform(embeddings)

plt.scatter(reduced_embeddings[:, 0], reduced_embeddings[:, 1])
plt.show()
```

**Search Analysis:**
```python
def analyze_search_results(query, results):
    print(f"Query: {query}")
    print(f"Results found: {len(results)}")
    
    for i, result in enumerate(results):
        print(f"{i+1}. {result['name']} (Score: {result['similarity_score']})")
```

This RAG system provides a robust foundation for accurate, contextual government scheme recommendations while maintaining high performance and scalability.
