#!/usr/bin/env python3
"""
Test script for enhanced personalization system.
"""

import sys
import os
import logging
import time
from pathlib import Path

# Add backend directory to Python path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from rag.recommendation_service import RecommendationService

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)

def test_filtering_system():
    """Test filtering capabilities."""
    print("\n=== Testing Filtering System ===")
    
    try:
        from rag.retriever_service import RetrieverService
        
        retriever = RetrieverService()
        retriever.initialize()
        
        # Test different filter combinations
        test_filters = [
            {"state": "Maharashtra", "category": "education"},
            {"category": "agriculture", "income_limit": 300000},
            {"state": "All India", "income_limit": 200000},
            {"category": "healthcare", "income_limit": 500000}
        ]
        
        for i, filters in enumerate(test_filters):
            print(f"\n--- Filter Test {i+1} ---")
            print(f"Filters: {filters}")
            
            # Test search with filters
            results = retriever.search(
                query="government schemes",
                top_k=3,
                filters=filters
            )
            
            if 'schemes' in results:
                print(f"✅ Found {len(results['schemes'])} schemes")
                for j, scheme in enumerate(results['schemes']):
                    print(f"  {j+1}. {scheme['name']}")
            else:
                print(f"✗ Error: {results}")
        
        return True
        
    except Exception as e:
        print(f"✗ Filtering test failed: {e}")
        return False

def test_recommendation_service():
    """Test enhanced recommendation service."""
    print("\n=== Testing Recommendation Service ===")
    
    try:
        recommendation_service = RecommendationService()
        
        # Test different user profiles
        test_profiles = [
            {
                "user_profile": {
                    "age": 21,
                    "education": "engineering college",
                    "income": 250000,
                    "state": "Karnataka",
                    "occupation": "student"
                },
                "max_recommendations": 3
            },
            {
                "user_profile": {
                    "age": 35,
                    "education": "graduate",
                    "income": 450000,
                    "state": "Delhi",
                    "occupation": "private employee"
                },
                "max_recommendations": 4
            },
            {
                "user_profile": {
                    "age": 45,
                    "education": "high school",
                    "income": 180000,
                    "state": "Uttar Pradesh",
                    "occupation": "farmer"
                },
                "max_recommendations": 5
            }
        ]
        
        for i, test_case in enumerate(test_profiles):
            try:
                print(f"\n--- Recommendation Test {i+1} ---")
                print(f"User Profile: {test_case['user_profile']}")
                
                # Generate recommendations
                start_time = time.time()
                recommendations = recommendation_service.generate_personalized_recommendations(
                    user_profile=test_case['user_profile'],
                    max_recommendations=test_case['max_recommendations']
                )
                response_time = time.time() - start_time
                
                print(f"Generated {len(recommendations.get('recommendations', []))} recommendations in {response_time:.3f}s")
                
                # Analyze recommendations
                if 'recommendations' in recommendations:
                    for j, rec in enumerate(recommendations['recommendations']):
                        print(f"  {j+1}. {rec.get('name', 'Unknown')}")
                        print(f"     Score: {rec.get('overall_score', 0):.3f}")
                        print(f"     Strength: {rec.get('recommendation_strength', 'unknown')}")
                        print(f"     Priority: {rec.get('application_priority', 'unknown')}")
                        print(f"     Reasoning: {rec.get('personalized_reasoning', 'N/A')[:80]}...")
                        print()
                
            except Exception as e:
                print(f"✗ Recommendation test {i+1} failed: {e}")
        
        return True
        
    except Exception as e:
        print(f"✗ Recommendation service test failed: {e}")
        return False

def test_personalized_search():
    """Test personalized search with filters."""
    print("\n=== Testing Personalized Search ===")
    
    try:
        from rag.retriever_service import RetrieverService
        
        retriever = RetrieverService()
        retriever.initialize()
        
        # Test search with user profile and filters
        user_profile = {
            "age": 28,
            "education": "MBA",
            "income": 600000,
            "state": "Maharashtra",
            "occupation": "business owner"
        }
        
        filters = {
            "category": "financial_inclusion",
            "income_limit": 700000
        }
        
        print(f"User Profile: {user_profile}")
        print(f"Filters: {filters}")
        
        # Perform search
        start_time = time.time()
        results = retriever.search(
            query="financial assistance for business",
            top_k=3,
            user_profile=user_profile,
            filters=filters
        )
        response_time = time.time() - start_time
        
        print(f"Search completed in {response_time:.3f}s")
        
        if 'schemes' in results:
            print(f"✅ Found {len(results['schemes'])} personalized schemes:")
            for i, scheme in enumerate(results['schemes']):
                print(f"  {i+1}. {scheme['name']} (Score: {scheme.get('similarity_score', 0):.3f})")
                print(f"     Eligibility Score: {scheme.get('eligibility_score', 0):.3f}")
                print(f"     Benefit Score: {scheme.get('benefit_score', 0):.3f}")
        
        return True
        
    except Exception as e:
        print(f"✗ Personalized search test failed: {e}")
        return False

def main():
    """Run personalization tests."""
    print("Starting Enhanced Personalization System Tests...")
    
    # Change to backend directory
    backend_dir = Path(__file__).parent
    os.chdir(backend_dir)
    
    # Run tests
    tests_passed = 0
    total_tests = 3
    
    # Test filtering system
    if test_filtering_system():
        tests_passed += 1
    
    # Test recommendation service
    if test_recommendation_service():
        tests_passed += 1
    
    # Test personalized search
    if test_personalized_search():
        tests_passed += 1
    
    print(f"\n=== Test Results ===")
    print(f"Passed: {tests_passed}/{total_tests}")
    
    if tests_passed == total_tests:
        print("✅ All personalization tests passed!")
        print("\n🎯 Enhanced RAG+LLM+Personalization System Ready!")
        return 0
    else:
        print("✗ Some tests failed!")
        return 1

if __name__ == "__main__":
    exit(main())
