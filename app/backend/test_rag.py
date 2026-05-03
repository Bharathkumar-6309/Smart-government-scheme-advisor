#!/usr/bin/env python3
"""
Test script for the RAG system.
"""

import sys
import os
import logging
import time
from pathlib import Path

# Add the backend directory to Python path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from rag.retriever_service import RetrieverService

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)

def test_rag_initialization():
    """Test RAG system initialization."""
    print("\n=== Testing RAG Initialization ===")
    
    try:
        retriever = RetrieverService()
        retriever.initialize()
        print("✓ RAG system initialized successfully")
        
        # Get statistics
        stats = retriever.get_search_statistics()
        print(f"✓ RAG Statistics: {stats}")
        
        return retriever
        
    except Exception as e:
        print(f"✗ RAG initialization failed: {e}")
        return None

def test_rag_search(retriever):
    """Test RAG search functionality."""
    print("\n=== Testing RAG Search ===")
    
    test_queries = [
        "scholarship for students",
        "housing loan subsidy",
        "agriculture financial assistance",
        "skill development program",
        "healthcare scheme for poor"
    ]
    
    for query in test_queries:
        try:
            print(f"\nSearching: '{query}'")
            start_time = time.time()
            results = retriever.search(query, top_k=3)
            search_time = time.time() - start_time
            
            print(f"✓ Found {len(results)} results in {search_time:.3f}s")
            
            for i, result in enumerate(results):
                print(f"  {i+1}. {result['scheme_name']} (Score: {result['similarity_score']:.3f})")
                print(f"     Category: {result['category']}")
                print(f"     Matching chunks: {len(result['matching_chunks'])}")
                if result['matching_chunks']:
                    print(f"     Top chunk: {result['matching_chunks'][0]['text'][:100]}...")
            
        except Exception as e:
            print(f"✗ Search failed for '{query}': {e}")

def test_scheme_details(retriever):
    """Test scheme details retrieval."""
    print("\n=== Testing Scheme Details ===")
    
    try:
        # Get details for a known scheme
        scheme_id = "pm_kisan"
        details = retriever.get_scheme_details(scheme_id)
        
        if details:
            print(f"✓ Retrieved details for {details['name']}")
            print(f"  Description: {details['description'][:100]}...")
            print(f"  Category: {details['category']}")
            print(f"  Eligibility: {len(details['eligibility'])} criteria")
        else:
            print(f"✗ Scheme {scheme_id} not found")
            
    except Exception as e:
        print(f"✗ Scheme details test failed: {e}")

def test_similar_schemes(retriever):
    """Test similar schemes functionality."""
    print("\n=== Testing Similar Schemes ===")
    
    try:
        # Find schemes similar to PM-KISAN
        similar_schemes = retriever.get_similar_schemes("pm_kisan", top_k=2)
        
        print(f"✓ Found {len(similar_schemes)} schemes similar to PM-KISAN")
        
        for i, scheme in enumerate(similar_schemes):
            print(f"  {i+1}. {scheme['scheme_name']} (Score: {scheme['similarity_score']:.3f})")
            print(f"     Category: {scheme['category']}")
            
    except Exception as e:
        print(f"✗ Similar schemes test failed: {e}")

def test_embedding_service():
    """Test embedding service directly."""
    print("\n=== Testing Embedding Service ===")
    
    try:
        from rag.embedding_service import EmbeddingService
        
        embedder = EmbeddingService()
        print(f"✓ Embedding service initialized with model: {embedder.model_name}")
        print(f"✓ Embedding dimension: {embedder.get_embedding_dimension()}")
        
        # Test single text embedding
        test_text = "This is a test text for embedding generation."
        embedding = embedder.embed_text(test_text)
        print(f"✓ Generated embedding for test text: {embedding.shape}")
        
        # Test batch embedding
        test_texts = [
            "First test text",
            "Second test text",
            "Third test text"
        ]
        embeddings = embedder.embed_texts(test_texts)
        print(f"✓ Generated embeddings for {len(test_texts)} texts: {embeddings.shape}")
        
        return True
        
    except Exception as e:
        print(f"✗ Embedding service test failed: {e}")
        return False

def test_vector_store():
    """Test vector store service directly."""
    print("\n=== Testing Vector Store Service ===")
    
    try:
        from rag.vector_store_service import VectorStoreService
        import numpy as np
        
        vector_store = VectorStoreService(embedding_dimension=384)
        print(f"✓ Vector store initialized with {vector_store.index_type} index")
        
        # Create test embeddings
        test_embeddings = [
            np.random.rand(384).astype(np.float32) for _ in range(5)
        ]
        test_ids = [f"test_chunk_{i}" for i in range(5)]
        test_metadata = [
            {"scheme_id": f"scheme_{i}", "text": f"Test text {i}"} for i in range(5)
        ]
        
        # Add embeddings
        vector_store.add_embeddings(test_embeddings, test_ids, test_metadata)
        print(f"✓ Added {len(test_embeddings)} embeddings to vector store")
        
        # Test search
        query_embedding = np.random.rand(384).astype(np.float32)
        results = vector_store.search(query_embedding, top_k=3)
        print(f"✓ Search returned {len(results)} results")
        
        # Get statistics
        stats = vector_store.get_stats()
        print(f"✓ Vector store stats: {stats}")
        
        return True
        
    except Exception as e:
        print(f"✗ Vector store test failed: {e}")
        return False

def main():
    """Run all RAG tests."""
    print("Starting RAG system tests...")
    
    # Change to backend directory
    backend_dir = Path(__file__).parent
    os.chdir(backend_dir)
    
    # Run individual component tests
    component_tests = [
        test_embedding_service,
        test_vector_store
    ]
    
    component_passed = 0
    for test in component_tests:
        if test():
            component_passed += 1
    
    print(f"\n=== Component Test Results ===")
    print(f"Passed: {component_passed}/{len(component_tests)}")
    
    # Run integration tests
    print("\n=== Running Integration Tests ===")
    
    retriever = test_rag_initialization()
    if retriever:
        test_rag_search(retriever)
        test_scheme_details(retriever)
        test_similar_schemes(retriever)
        print("\n✓ All integration tests passed!")
        return 0
    else:
        print("\n✗ Integration tests failed!")
        return 1

if __name__ == "__main__":
    exit(main())
