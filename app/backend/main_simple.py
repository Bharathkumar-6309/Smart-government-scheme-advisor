#!/usr/bin/env python3
"""
Simplified backend server for testing frontend-backend connection.
"""

import json
import urllib.parse
import logging
import sys
import time
from datetime import datetime
from typing import Dict, Any, List, Optional
from http.server import BaseHTTPRequestHandler, HTTPServer
from urllib.parse import urlparse, parse_qs

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[logging.StreamHandler(sys.stdout)]
)
logger = logging.getLogger(__name__)

# Configuration
APP_NAME = "Smart Government Scheme Advisor"
APP_VERSION = "1.0.0"
HOST = "0.0.0.0"
PORT = 8000
CORS_ORIGINS = ["http://localhost:5173", "http://127.0.0.1:5173"]

# Mock scheme data
MOCK_SCHEMES = [
    {
        "id": "scheme_001",
        "name": "National Scholarship Portal",
        "description": "Centralized platform for various scholarship schemes",
        "category": "education",
        "benefits": "Financial assistance for education covering tuition fees and maintenance allowances",
        "documents_required": ["Aadhaar card", "Mark sheets", "Income certificate", "Bank account details"],
        "eligibility_criteria": ["Students from class 1 to post-graduation", "Minimum 50 marks in previous examination", "Annual family income below ₹2,50,000"],
        "state": "All India",
        "income_limit": 250000,
        "official_link": "https://scholarships.gov.in",
        "similarity_score": 0.92,
        "confidence_score": 0.88,
        "why_eligible": "Based on your student profile and income level, you meet the eligibility criteria for multiple scholarships available on this portal.",
        "application_steps": [
            "Register on scholarships.gov.in with your academic details",
            "Complete your profile with engineering branch information", 
            "Upload mark sheets and recommendation letters",
            "Apply for technical scholarships specifically",
            "Submit applications before deadlines"
        ]
    },
    {
        "id": "scheme_002", 
        "name": "Pradhan Mantri Awas Yojana (PMAY)",
        "description": "Housing for All mission to provide affordable housing",
        "category": "housing",
        "benefits": "Interest subsidy of up to 6.50% on home loans for 20 years, reducing EMI burden",
        "documents_required": ["Aadhaar card", "PAN card", "Income certificate", "Address proof", "Bank account details", "Photographs"],
        "eligibility_criteria": ["Annual family income below ₹6,00,000", "No existing pucca house", "Indian citizen", "Age between 21-55 years"],
        "state": "All India", 
        "income_limit": 600000,
        "official_link": "https://pmaymis.gov.in",
        "similarity_score": 0.85,
        "confidence_score": 0.82,
        "why_eligible": "Your income level and age make you eligible for the housing subsidy under PMAY.",
        "application_steps": [
            "Apply through your bank or housing finance company",
            "Submit income and identity proof", 
            "Provide property details",
            "Wait for subsidy approval and credit"
        ]
    },
    {
        "id": "scheme_003",
        "name": "Pradhan Mantri Kisan Samman Nidhi (PM-KISAN)",
        "description": "Income support scheme for small and marginal farmers",
        "category": "agriculture",
        "benefits": "₹6,000 per year in three equal installments directly to bank accounts",
        "documents_required": ["Aadhaar card", "Land records", "Bank account details", "Photographs"],
        "eligibility_criteria": ["Small and marginal farmers", "Landholding farmer families", "Annual income below ₹6,00,000", "Must have land records in their name"],
        "state": "All India",
        "income_limit": 600000,
        "official_link": "https://pmkisan.gov.in",
        "similarity_score": 0.78,
        "confidence_score": 0.75,
        "why_eligible": "As a farmer with income below the threshold, you qualify for this direct benefit transfer scheme.",
        "application_steps": [
            "Register on pmkisan.gov.in",
            "Upload land records and identity proof",
            "Verify bank account details",
            "Wait for approval and first installment"
        ]
    }
]

class CORSHTTPRequestHandler(BaseHTTPRequestHandler):
    """HTTP request handler with CORS support."""
    
    def _set_cors_headers(self):
        """Set CORS headers."""
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'GET, POST, OPTIONS')
        self.send_header('Access-Control-Allow-Headers', 'Content-Type')
    
    def _send_json_response(self, status_code: int, data: Dict[str, Any]):
        """Send JSON response."""
        self.send_response(status_code)
        self._set_cors_headers()
        self.send_header('Content-Type', 'application/json')
        self.end_headers()
        response_json = json.dumps(data, indent=2)
        self.wfile.write(response_json.encode('utf-8'))
    
    def _parse_request_body(self) -> Dict[str, Any]:
        """Parse JSON request body."""
        content_length = int(self.headers.get('Content-Length', 0))
        if content_length > 0:
            body = self.rfile.read(content_length).decode('utf-8')
            try:
                return json.loads(body)
            except json.JSONDecodeError:
                return {}
        return {}
    
    def do_OPTIONS(self):
        """Handle OPTIONS requests for CORS."""
        self.send_response(200)
        self._set_cors_headers()
        self.end_headers()
    
    def do_GET(self):
        """Handle GET requests."""
        try:
            parsed_path = urlparse(self.path)
            path = parsed_path.path
            
            if path == '/api/health':
                self._handle_health_check()
            else:
                self._send_json_response(404, {
                    "message": "Endpoint not found",
                    "details": {"path": path}
                })
                
        except Exception as e:
            logger.error(f"GET request failed: {str(e)}")
            self._send_json_response(500, {
                "message": "Internal server error",
                "details": {"error": str(e)}
            })
    
    def do_POST(self):
        """Handle POST requests."""
        try:
            parsed_path = urlparse(self.path)
            path = parsed_path.path
            
            if path == '/api/schemes/search':
                self._handle_scheme_search()
            elif path == '/api/schemes/recommend':
                self._handle_scheme_recommend()
            else:
                self._send_json_response(404, {
                    "message": "Endpoint not found", 
                    "details": {"path": path}
                })
                
        except Exception as e:
            logger.error(f"POST request failed: {str(e)}")
            self._send_json_response(500, {
                "message": "Internal server error",
                "details": {"error": str(e)}
            })
    
    def _handle_health_check(self):
        """Handle health check endpoint."""
        try:
            health_data = {
                "status": "healthy",
                "timestamp": datetime.now().isoformat(),
                "app": APP_NAME,
                "version": APP_VERSION,
                "services": {
                    "database": "connected",
                    "rag_system": "operational",
                    "llm_service": "mock_mode"
                }
            }
            
            self._send_json_response(200, health_data)
            logger.info("Health check completed successfully")
            
        except Exception as e:
            logger.error(f"Health check failed: {str(e)}")
            self._send_json_response(500, {
                "message": "Health check failed",
                "details": {"error": str(e)}
            })
    
    def _handle_scheme_search(self):
        """Handle scheme search endpoint."""
        try:
            request_data = self._parse_request_body()
            logger.info(f"Scheme search request: {request_data.get('query', 'N/A')}")
            
            # Validate request
            if not request_data.get('query'):
                self._send_json_response(400, {
                    "message": "Validation error",
                    "details": {"query": "Query is required"}
                })
                return
            
            # Filter schemes based on criteria
            filtered_schemes = self._filter_schemes(request_data)
            
            response = {
                "success": True,
                "message": f"Found {len(filtered_schemes)} relevant schemes",
                "data": filtered_schemes,
                "total_results": len(filtered_schemes),
                "search_time": 0.001,
                "search_method": "mock_search",
                "filters_applied": {
                    "category": request_data.get('filters', {}).get('category'),
                    "state": request_data.get('filters', {}).get('state'),
                    "income_limit": request_data.get('filters', {}).get('income_limit')
                }
            }
            
            self._send_json_response(200, response)
            logger.info(f"Scheme search completed: {len(filtered_schemes)} results")
            
        except Exception as e:
            logger.error(f"Scheme search failed: {str(e)}")
            self._send_json_response(500, {
                "message": "Search failed",
                "details": {"error": str(e)}
            })
    
    def _handle_scheme_recommend(self):
        """Handle scheme recommendation endpoint."""
        try:
            request_data = self._parse_request_body()
            logger.info(f"Scheme recommendation request")
            
            # Validate request
            if not request_data.get('user_profile'):
                self._send_json_response(400, {
                    "message": "Validation error",
                    "details": {"user_profile": "User profile is required"}
                })
                return
            
            # Get recommendations based on profile
            recommendations = self._get_recommendations(request_data.get('user_profile'))
            
            response = {
                "success": True,
                "message": f"Generated {len(recommendations)} personalized recommendations",
                "recommendations": recommendations,
                "total_recommendations": len(recommendations),
                "response_time": 0.002,
                "recommendation_method": "mock_personalized"
            }
            
            self._send_json_response(200, response)
            logger.info(f"Scheme recommendations completed: {len(recommendations)} results")
            
        except Exception as e:
            logger.error(f"Scheme recommendation failed: {str(e)}")
            self._send_json_response(500, {
                "message": "Recommendation failed",
                "details": {"error": str(e)}
            })
    
    def _filter_schemes(self, request_data: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Filter schemes based on request criteria."""
        filters = request_data.get('filters', {})
        user_profile = request_data.get('user_profile', {})
        
        filtered = MOCK_SCHEMES.copy()
        
        # Apply category filter
        if filters.get('category'):
            filtered = [s for s in filtered if s['category'] == filters['category']]
        
        # Apply state filter
        if filters.get('state'):
            filtered = [s for s in filtered if s['state'] == filters['state'] or s['state'] == 'All India']
        
        # Apply income filter
        if filters.get('income_limit'):
            filtered = [s for s in filtered if s['income_limit'] is None or s['income_limit'] <= filters['income_limit']]
        
        # Apply user profile filtering
        if user_profile.get('income'):
            filtered = [s for s in filtered if s['income_limit'] is None or s['income_limit'] >= user_profile['income']]
        
        return filtered[:3]  # Return top 3 results
    
    def _get_recommendations(self, user_profile: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Get personalized recommendations based on user profile."""
        recommendations = []
        
        for scheme in MOCK_SCHEMES:
            # Simple eligibility check
            if user_profile.get('income') and scheme['income_limit']:
                if user_profile['income'] <= scheme['income_limit']:
                    recommendations.append(scheme)
            else:
                recommendations.append(scheme)
        
        return recommendations[:5]  # Return top 5 recommendations

def run_server():
    """Run the HTTP server."""
    server_address = (HOST, PORT)
    httpd = HTTPServer(server_address, CORSHTTPRequestHandler)
    
    logger.info(f"Starting {APP_NAME} v{APP_VERSION}")
    logger.info(f"Server running on http://{HOST}:{PORT}")
    logger.info("Press Ctrl+C to stop the server")
    
    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        logger.info("Server stopped by user")
    finally:
        httpd.server_close()

if __name__ == "__main__":
    run_server()
