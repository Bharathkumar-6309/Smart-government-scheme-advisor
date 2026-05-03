#!/usr/bin/env python3
"""
Test script for the ingestion module.
"""

import sys
import os
import logging
from pathlib import Path

# Add the backend directory to Python path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from ingestion.data_loader import DataLoader
from ingestion.text_processor import TextProcessor
from ingestion.chunker import TextChunker

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)

def test_data_loader():
    """Test the data loader functionality."""
    print("\n=== Testing DataLoader ===")
    
    try:
        # Initialize data loader
        loader = DataLoader()
        
        # Load schemes
        schemes = loader.load_schemes()
        print(f"✓ Loaded {len(schemes)} schemes")
        
        # Test getting statistics
        stats = loader.get_statistics()
        print(f"✓ Statistics: {stats}")
        
        # Test getting a specific scheme
        scheme = loader.get_scheme_by_id("pm_kisan")
        print(f"✓ Found scheme: {scheme['name'] if scheme else 'None'}")
        
        # Test category filtering
        education_schemes = loader.get_schemes_by_category("education")
        print(f"✓ Education schemes: {len(education_schemes)}")
        
        return True
        
    except Exception as e:
        print(f"✗ DataLoader test failed: {e}")
        return False

def test_text_processor():
    """Test the text processor functionality."""
    print("\n=== Testing TextProcessor ===")
    
    try:
        # Initialize text processor
        processor = TextProcessor()
        
        # Test text cleaning
        dirty_text = "  This is a   test\nwith   multiple   spaces and\nnewlines!  "
        clean_text = processor.clean_text(dirty_text)
        print(f"✓ Text cleaning: '{dirty_text}' -> '{clean_text}'")
        
        # Test processing all schemes
        processed_schemes = processor.process_all_schemes()
        print(f"✓ Processed {len(processed_schemes)} schemes")
        
        # Test creating searchable text
        if processed_schemes:
            searchable_text = processor.create_searchable_text(processed_schemes[0])
            print(f"✓ Searchable text length: {len(searchable_text)} characters")
        
        # Test text statistics
        text_stats = processor.get_text_statistics(processed_schemes)
        print(f"✓ Text statistics: {text_stats}")
        
        return True
        
    except Exception as e:
        print(f"✗ TextProcessor test failed: {e}")
        return False

def test_chunker():
    """Test the chunker functionality."""
    print("\n=== Testing TextChunker ===")
    
    try:
        # Initialize chunker
        chunker = TextChunker(chunk_size=300, chunk_overlap=50)
        
        # Test basic chunking
        test_text = "This is a test text. It has multiple sentences. We want to see how it gets chunked. The chunker should break at sentence boundaries when possible."
        chunks = chunker.create_chunks(test_text)
        print(f"✓ Created {len(chunks)} chunks from test text")
        
        # Test scheme chunking
        embedding_chunks = chunker.create_embedding_ready_chunks()
        print(f"✓ Created {len(embedding_chunks)} embedding-ready chunks")
        
        # Test chunk statistics
        chunk_stats = chunker.get_chunk_statistics(embedding_chunks)
        print(f"✓ Chunk statistics: {chunk_stats}")
        
        # Test saving chunks
        output_path = "../data/test_chunks.json"
        chunker.save_chunks_to_file(embedding_chunks, output_path)
        print(f"✓ Saved chunks to {output_path}")
        
        # Display sample chunk
        if embedding_chunks:
            sample_chunk = embedding_chunks[0]
            print(f"✓ Sample chunk preview:")
            print(f"  ID: {sample_chunk['chunk_id']}")
            print(f"  Type: {sample_chunk['metadata']['chunk_type']}")
            print(f"  Text: {sample_chunk['text'][:100]}...")
        
        return True
        
    except Exception as e:
        print(f"✗ TextChunker test failed: {e}")
        return False

def main():
    """Run all tests."""
    print("Starting ingestion module tests...")
    
    # Change to backend directory
    backend_dir = Path(__file__).parent
    os.chdir(backend_dir)
    
    # Run tests
    tests = [
        test_data_loader,
        test_text_processor,
        test_chunker
    ]
    
    passed = 0
    total = len(tests)
    
    for test in tests:
        if test():
            passed += 1
    
    print(f"\n=== Test Results ===")
    print(f"Passed: {passed}/{total}")
    
    if passed == total:
        print("✓ All tests passed!")
        return 0
    else:
        print("✗ Some tests failed!")
        return 1

if __name__ == "__main__":
    exit(main())
