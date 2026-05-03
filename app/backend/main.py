from http.server import HTTPServer, BaseHTTPRequestHandler
import json
import urllib.parse
import logging
import sys
import time
from datetime import datetime
from typing import Dict, Any, List, Optional

# Import RAG services
from rag.retriever_service import RetrieverService
from rag.llm_service import LLMService

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

# Initialize RAG services
retriever_service = None
llm_service = None

def initialize_rag_service():
    """Initialize the RAG and LLM services."""
    global retriever_service, llm_service
    try:
        logger.info("Initializing RAG and LLM services...")
        retriever_service = RetrieverService()
        llm_service = LLMService()
        retriever_service.initialize()
        logger.info("RAG and LLM services initialized successfully")
    except Exception as e:
        logger.error(f"Failed to initialize RAG/LLM services: {e}")
        retriever_service = None
        llm_service = None


class CORSHTTPRequestHandler(BaseHTTPRequestHandler):
    """HTTP request handler with CORS support."""
    
    def _set_cors_headers(self):
        """Set CORS headers."""
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'GET, POST, OPTIONS')
        self.send_header('Access-Control-Allow-Headers', 'Content-Type')
    
    def do_OPTIONS(self):
        """Handle OPTIONS requests for CORS preflight."""
        self.send_response(200)
        self._set_cors_headers()
        self.end_headers()
    
    def _send_json_response(self, status_code: int, data: Dict[str, Any]):
        """Send JSON response with CORS headers."""
        self.send_response(status_code)
        self.send_header('Content-type', 'application/json')
        self._set_cors_headers()
        self.end_headers()
        self.wfile.write(json.dumps(data).encode())
    
    def _parse_request_body(self) -> Dict[str, Any]:
        """Parse JSON request body."""
        content_length = int(self.headers['Content-Length'])
        post_data = self.rfile.read(content_length)
        return json.loads(post_data.decode('utf-8'))
    
    def do_GET(self):
        """Handle GET requests."""
        try:
            if self.path == '/':
                self._send_json_response(200, {
                    "message": f"Welcome to {APP_NAME} API",
                    "version": APP_VERSION,
                    "docs": "/docs"
                })
            elif self.path == '/api/health':
                self._handle_health_check()
            else:
                self._send_json_response(404, {
                    "message": "Endpoint not found",
                    "details": {"path": self.path}
                })
        except Exception as e:
            logger.error(f"GET request error: {str(e)}")
            self._send_json_response(500, {
                "message": "Internal server error",
                "details": {"error": str(e)}
            })
    
    def do_POST(self):
        """Handle POST requests."""
        try:
            if self.path == '/api/schemes/search':
                self._handle_scheme_search()
            elif self.path == '/api/schemes/recommend':
                self._handle_scheme_recommend()
            else:
                self._send_json_response(404, {
                    "message": "Endpoint not found",
                    "details": {"path": self.path}
                })
        except Exception as e:
            logger.error(f"POST request error: {str(e)}")
            self._send_json_response(500, {
                "message": "Internal server error",
                "details": {"error": str(e)}
            })
    
    def _handle_health_check(self):
        """Handle health check endpoint."""
        try:
            health_data = {
                "status": "ok",
                "version": APP_VERSION,
                "timestamp": datetime.utcnow().isoformat() + "Z"
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
        """Handle scheme search endpoint using RAG+LLM with filtering."""
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
            
            # Initialize RAG service if not already done
            global retriever_service
            if retriever_service is None:
                initialize_rag_service()
            
            if retriever_service is None:
                # Fallback to mock results if RAG fails
                self._send_fallback_search_results(request_data)
                return
            
            # Extract user profile from request if available
            user_profile = request_data.get('user_profile')
            
            # Extract filters from request if available
            filters = {}
            if request_data.get('state'):
                filters['state'] = request_data['state']
            if request_data.get('category'):
                filters['category'] = request_data['category']
            if request_data.get('income_limit'):
                filters['income_limit'] = request_data['income_limit']
            
            # Perform RAG+LLM search with filtering
            start_time = time.time()
            llm_response = retriever_service.search(
                query=request_data.get('query'),
                top_k=3,
                user_profile=user_profile,
                filters=filters
            )
            search_time = time.time() - start_time
            
            response = {
                "success": True,
                "message": f"Generated {len(llm_response.get('schemes', []))} personalized scheme recommendations",
                "data": llm_response.get('schemes', []),
                "total_results": len(llm_response.get('schemes', [])),
                "search_time": search_time,
                "search_method": "rag_llm",
                "filters_applied": filters
            }
            
            self._send_json_response(200, response)
            logger.info(f"RAG+LLM scheme search completed: {len(llm_response.get('schemes', []))} results in {search_time:.3f}s")
            
        except json.JSONDecodeError:
            self._send_json_response(400, {
                "message": "Invalid JSON in request body",
                "details": {}
            })
        except Exception as e:
            logger.error(f"RAG+LLM scheme search failed: {str(e)}")
            # Fallback to mock results
            self._send_fallback_search_results(request_data)
    
    def _handle_scheme_recommend(self):
        """Handle scheme recommendation endpoint using enhanced recommendation service."""
        try:
            request_data = self._parse_request_body()
            logger.info(f"Scheme recommendation request: {request_data}")
            
            # Validate request
            if not request_data.get('user_profile'):
                self._send_json_response(400, {
                    "message": "Validation error",
                    "details": {"user_profile": "User profile is required"}
                })
                return
            
            # Initialize recommendation service
            from rag.recommendation_service import RecommendationService
            recommendation_service = RecommendationService()
            
            # Generate personalized recommendations
            start_time = time.time()
            recommendations = recommendation_service.generate_personalized_recommendations(
                user_profile=request_data.get('user_profile'),
                max_recommendations=request_data.get('max_recommendations', 5)
            )
            response_time = time.time() - start_time
            
            response = {
                "success": True,
                "message": f"Generated {len(recommendations.get('recommendations', []))} personalized recommendations",
                "data": recommendations.get('recommendations', []),
                "total_recommendations": len(recommendations.get('recommendations', [])),
                "response_time": response_time,
                "recommendation_method": "personalized"
            }
            
            self._send_json_response(200, response)
            logger.info(f"Scheme recommendations completed: {len(recommendations.get('recommendations', []))} results in {response_time:.3f}s")
            
        except json.JSONDecodeError:
            self._send_json_response(400, {
                "message": "Invalid JSON in request body",
                "details": {}
            })
        except Exception as e:
            logger.error(f"Scheme recommendation failed: {str(e)}")
            self._send_json_response(500, {
                "message": "Failed to generate recommendations",
                "details": {"error": str(e)}
            })
    
    def _send_fallback_search_results(self, request_data):
        """Send fallback search results if RAG fails."""
        try:
            # Mock search implementation as fallback
            mock_schemes = [
                {
                    "id": "scheme_001",
                    "name": "National Scholarship Portal",
                    "description": "Centralized platform for various scholarship schemes",
                    "category": "education",
                    "eligibility_criteria": ["student", "merit_based", "income_criteria"],
                    "benefits": "Financial assistance for education",
                    "application_process": "Online application through NSP portal",
                    "deadline": "2024-12-31T00:00:00Z",
                    "state": None,
                    "official_link": "https://scholarships.gov.in",
                    "similarity_score": 0.85,
                    "matching_chunks": [],
                    "chunk_types": ["general"]
                },
                {
                    "id": "scheme_002",
                    "name": "Pradhan Mantri Awas Yojana",
                    "description": "Housing for All initiative",
                    "category": "housing",
                    "eligibility_criteria": ["adult", "income_criteria", "no_pucca_house"],
                    "benefits": "Subsidized housing loans",
                    "application_process": "Apply through common service centers",
                    "deadline": None,
                    "state": None,
                    "official_link": "https://pmaymis.gov.in",
                    "similarity_score": 0.75,
                    "matching_chunks": [],
                    "chunk_types": ["general"]
                }
            ]
            
            # Filter based on category if provided
            category = request_data.get('category')
            if category:
                mock_schemes = [s for s in mock_schemes if s['category'] == category]
            
            search_time = 0.123  # Mock search time
            
            response = {
                "success": True,
                "message": f"Found {len(mock_schemes)} schemes (fallback mode)",
                "data": mock_schemes,
                "total_results": len(mock_schemes),
                "search_time": search_time,
                "search_method": "fallback"
            }
            
            self._send_json_response(200, response)
            logger.info(f"Fallback scheme search completed: {len(mock_schemes)} results")
            
        except Exception as e:
            logger.error(f"Fallback search failed: {str(e)}")
            self._send_json_response(500, {
                "message": "Failed to search schemes",
                "details": {"error": str(e)}
            })
    
    def _handle_scheme_recommend(self):
        """Handle scheme recommendation endpoint."""
        try:
            request_data = self._parse_request_body()
            logger.info("Scheme recommendation request received")
            
            # Validate request
            if not request_data.get('user_profile'):
                self._send_json_response(400, {
                    "message": "Validation error",
                    "details": {"user_profile": "User profile is required"}
                })
                return
            
            user_profile = request_data.get('user_profile', {})
            max_results = request_data.get('max_results', 10)
            
            # Mock recommendation implementation
            mock_recommendations = [
                {
                    "id": "scheme_003",
                    "name": "Skill India Mission",
                    "description": "Skill development program for youth",
                    "category": "skill_development",
                    "eligibility_criteria": ["age_15_35", "indian_citizen"],
                    "benefits": "Free skill training and certification",
                    "application_process": "Register at nearest skill center",
                    "deadline": None,
                    "state": None,
                    "official_link": "https://skillindia.gov.in"
                }
            ]
            
            confidence_scores = [0.85]  # Mock confidence scores
            reasoning = f"Based on your profile (age: {user_profile.get('age', 'unknown')}, " \
                       f"occupation: {user_profile.get('occupation', 'unknown')}), " \
                       "these schemes are most suitable for you."
            
            response = {
                "success": True,
                "message": "Recommendations generated successfully",
                "recommendations": mock_recommendations[:max_results],
                "confidence_scores": confidence_scores[:max_results],
                "reasoning": reasoning
            }
            
            self._send_json_response(200, response)
            logger.info(f"Scheme recommendation completed: {len(mock_recommendations)} recommendations")
            
        except json.JSONDecodeError:
            self._send_json_response(400, {
                "message": "Invalid JSON in request body",
                "details": {}
            })
        except Exception as e:
            logger.error(f"Scheme recommendation failed: {str(e)}")
            self._send_json_response(500, {
                "message": "Failed to generate recommendations",
                "details": {"error": str(e)}
            })


def run_server():
    """Run the HTTP server."""
    server_address = (HOST, PORT)
    httpd = HTTPServer(server_address, CORSHTTPRequestHandler)
    
    logger.info(f"Starting {APP_NAME} v{APP_VERSION}")
    logger.info(f"Server running on http://{HOST}:{PORT}")
    logger.info("Available endpoints:")
    logger.info("  GET  /              - Welcome message")
    logger.info("  GET  /api/health    - Health check")
    logger.info("  POST /api/schemes/search   - Search schemes")
    logger.info("  POST /api/schemes/recommend - Get recommendations")
    
    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        logger.info("Shutting down server...")
        httpd.shutdown()


if __name__ == "__main__":
    run_server()
