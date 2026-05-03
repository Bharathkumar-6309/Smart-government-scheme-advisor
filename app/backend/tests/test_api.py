#!/usr/bin/env python3
"""
API tests for the Smart Government Scheme Advisor backend.
"""

import pytest
import json
import requests
from urllib.parse import urljoin
import time

# Test configuration
BASE_URL = "http://localhost:8000"
API_BASE = urljoin(BASE_URL, "/api/")

class TestAPI:
    """Test class for API endpoints."""
    
    @classmethod
    def setup_class(cls):
        """Setup test class."""
        cls.base_url = BASE_URL
        cls.api_base = API_BASE
        
        # Wait for server to start
        time.sleep(1)
    
    def test_health_check(self):
        """Test health check endpoint."""
        response = requests.get(f"{self.api_base}health")
        
        assert response.status_code == 200
        data = response.json()
        
        assert data["status"] == "healthy"
        assert "timestamp" in data
        assert "app" in data
        assert "version" in data
        assert "services" in data
    
    def test_scheme_search_valid_request(self):
        """Test scheme search with valid request."""
        payload = {
            "query": "scholarship for students",
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
        
        response = requests.post(
            f"{self.api_base}schemes/search",
            json=payload,
            headers={"Content-Type": "application/json"}
        )
        
        assert response.status_code == 200
        data = response.json()
        
        assert data["success"] is True
        assert "data" in data
        assert "total_results" in data
        assert "search_time" in data
        assert "search_method" in data
        
        # Validate response data structure
        schemes = data["data"]
        assert isinstance(schemes, list)
        
        if schemes:
            scheme = schemes[0]
            required_fields = [
                "id", "name", "category", "description", 
                "benefits", "documents_required", "eligibility_criteria",
                "state", "income_limit", "official_link"
            ]
            
            for field in required_fields:
                assert field in scheme
    
    def test_scheme_search_missing_query(self):
        """Test scheme search with missing query."""
        payload = {
            "user_profile": {
                "age": 21,
                "income": 250000
            }
        }
        
        response = requests.post(
            f"{self.api_base}schemes/search",
            json=payload,
            headers={"Content-Type": "application/json"}
        )
        
        assert response.status_code == 400
        data = response.json()
        
        assert "message" in data
        assert "details" in data
        assert "query" in data["details"]
    
    def test_scheme_recommend_valid_request(self):
        """Test scheme recommendation with valid request."""
        payload = {
            "user_profile": {
                "age": 25,
                "income": 400000,
                "occupation": "private employee",
                "education": "graduate",
                "state": "Delhi"
            },
            "max_recommendations": 3
        }
        
        response = requests.post(
            f"{self.api_base}schemes/recommend",
            json=payload,
            headers={"Content-Type": "application/json"}
        )
        
        assert response.status_code == 200
        data = response.json()
        
        assert data["success"] is True
        assert "recommendations" in data
        assert "total_recommendations" in data
        assert "response_time" in data
        assert "recommendation_method" in data
        
        # Validate recommendations structure
        recommendations = data["recommendations"]
        assert isinstance(recommendations, list)
        assert len(recommendations) <= 3
        
        if recommendations:
            rec = recommendations[0]
            required_fields = [
                "id", "name", "category", "description",
                "benefits", "documents_required", "eligibility_criteria",
                "state", "income_limit", "official_link"
            ]
            
            for field in required_fields:
                assert field in rec
    
    def test_scheme_recommend_missing_profile(self):
        """Test scheme recommendation with missing user profile."""
        payload = {
            "max_recommendations": 5
        }
        
        response = requests.post(
            f"{self.api_base}schemes/recommend",
            json=payload,
            headers={"Content-Type": "application/json"}
        )
        
        assert response.status_code == 400
        data = response.json()
        
        assert "message" in data
        assert "details" in data
        assert "user_profile" in data["details"]
    
    def test_invalid_endpoint(self):
        """Test invalid endpoint returns 404."""
        response = requests.get(f"{self.api_base}invalid")
        
        assert response.status_code == 404
        data = response.json()
        
        assert "message" in data
        assert "details" in data
    
    def test_invalid_json_request(self):
        """Test request with invalid JSON."""
        response = requests.post(
            f"{self.api_base}schemes/search",
            data="invalid json",
            headers={"Content-Type": "application/json"}
        )
        
        # Should handle invalid JSON gracefully
        assert response.status_code in [400, 500]
    
    def test_cors_headers(self):
        """Test CORS headers are present."""
        response = requests.options(f"{self.api_base}health")
        
        assert response.status_code == 200
        assert "Access-Control-Allow-Origin" in response.headers
        assert "Access-Control-Allow-Methods" in response.headers
        assert "Access-Control-Allow-Headers" in response.headers

class TestSearchFunctionality:
    """Test class for search functionality."""
    
    def setup_method(self):
        """Setup test method."""
        self.api_base = "http://localhost:8000/api/"
    
    def test_search_with_different_queries(self):
        """Test search with various query types."""
        queries = [
            "scholarship for students",
            "housing loan subsidy", 
            "agriculture financial assistance",
            "skill development programs"
        ]
        
        for query in queries:
            payload = {
                "query": query,
                "user_profile": {
                    "age": 25,
                    "income": 300000,
                    "state": "Maharashtra"
                }
            }
            
            response = requests.post(
                f"{self.api_base}schemes/search",
                json=payload,
                headers={"Content-Type": "application/json"}
            )
            
            assert response.status_code == 200
            data = response.json()
            assert data["success"] is True
            assert isinstance(data["data"], list)
    
    def test_search_with_filters(self):
        """Test search with different filter combinations."""
        filter_combinations = [
            {"category": "education"},
            {"state": "Maharashtra"},
            {"income_limit": 300000},
            {"category": "education", "state": "Maharashtra"},
            {"category": "education", "income_limit": 300000}
        ]
        
        for filters in filter_combinations:
            payload = {
                "query": "government schemes",
                "filters": filters,
                "user_profile": {
                    "age": 25,
                    "income": 300000
                }
            }
            
            response = requests.post(
                f"{self.api_base}schemes/search",
                json=payload,
                headers={"Content-Type": "application/json"}
            )
            
            assert response.status_code == 200
            data = response.json()
            assert data["success"] is True
            assert "filters_applied" in data

class TestRecommendationFunctionality:
    """Test class for recommendation functionality."""
    
    def setup_method(self):
        """Setup test method."""
        self.api_base = "http://localhost:8000/api/"
    
    def test_recommend_different_profiles(self):
        """Test recommendations with different user profiles."""
        profiles = [
            {
                "age": 21,
                "income": 250000,
                "occupation": "student",
                "education": "engineering",
                "state": "Karnataka"
            },
            {
                "age": 35,
                "income": 600000,
                "occupation": "private employee",
                "education": "graduate",
                "state": "Delhi"
            },
            {
                "age": 45,
                "income": 180000,
                "occupation": "farmer",
                "education": "high school",
                "state": "Uttar Pradesh"
            }
        ]
        
        for profile in profiles:
            payload = {
                "user_profile": profile,
                "max_recommendations": 3
            }
            
            response = requests.post(
                f"{self.api_base}schemes/recommend",
                json=payload,
                headers={"Content-Type": "application/json"}
            )
            
            assert response.status_code == 200
            data = response.json()
            assert data["success"] is True
            assert isinstance(data["recommendations"], list)
    
    def test_recommend_with_max_limit(self):
        """Test recommendations with different max limits."""
        max_limits = [1, 3, 5, 10]
        
        for max_limit in max_limits:
            payload = {
                "user_profile": {
                    "age": 25,
                    "income": 300000,
                    "state": "Maharashtra"
                },
                "max_recommendations": max_limit
            }
            
            response = requests.post(
                f"{self.api_base}schemes/recommend",
                json=payload,
                headers={"Content-Type": "application/json"}
            )
            
            assert response.status_code == 200
            data = response.json()
            assert data["success"] is True
            assert len(data["recommendations"]) <= max_limit

if __name__ == "__main__":
    # Run tests
    pytest.main([__file__, "-v"])
