from pydantic import BaseModel, Field
from typing import List, Optional, Dict, Any
from datetime import datetime


class SchemeSearchRequest(BaseModel):
    query: str = Field(..., description="Search query for government schemes", min_length=1, max_length=500)
    category: Optional[str] = Field(None, description="Filter by scheme category")
    state: Optional[str] = Field(None, description="Filter by state/region")
    eligibility: Optional[List[str]] = Field(None, description="Eligibility criteria filters")
    
    class Config:
        schema_extra = {
            "example": {
                "query": "education scholarships for students",
                "category": "education",
                "state": "Maharashtra",
                "eligibility": ["student", "below_poverty_line"]
            }
        }


class Scheme(BaseModel):
    id: str
    name: str
    description: str
    category: str
    eligibility_criteria: List[str]
    benefits: str
    application_process: str
    deadline: Optional[datetime] = None
    state: Optional[str] = None
    official_link: Optional[str] = None


class SchemeSearchResponse(BaseModel):
    success: bool
    message: str
    data: List[Scheme]
    total_results: int
    search_time: float
    
    class Config:
        schema_extra = {
            "example": {
                "success": True,
                "message": "Search completed successfully",
                "data": [],
                "total_results": 0,
                "search_time": 0.123
            }
        }


class SchemeRecommendRequest(BaseModel):
    user_profile: Dict[str, Any] = Field(..., description="User profile information")
    preferences: Optional[Dict[str, Any]] = Field(None, description="User preferences")
    max_results: Optional[int] = Field(10, description="Maximum number of recommendations", ge=1, le=50)
    
    class Config:
        schema_extra = {
            "example": {
                "user_profile": {
                    "age": 25,
                    "income": 300000,
                    "education": "graduate",
                    "state": "Maharashtra",
                    "occupation": "student"
                },
                "preferences": {
                    "categories": ["education", "healthcare"],
                    "priority": "financial_benefits"
                },
                "max_results": 10
            }
        }


class SchemeRecommendResponse(BaseModel):
    success: bool
    message: str
    recommendations: List[Scheme]
    confidence_scores: List[float]
    reasoning: str
    
    class Config:
        schema_extra = {
            "example": {
                "success": True,
                "message": "Recommendations generated successfully",
                "recommendations": [],
                "confidence_scores": [],
                "reasoning": "Based on your profile, these schemes are most suitable"
            }
        }
