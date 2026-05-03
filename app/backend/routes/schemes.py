from fastapi import APIRouter, HTTPException
from utils.logger import get_logger
from utils.exceptions import APIException
from services.scheme_service import SchemeService
from schemas.schemes import (
    SchemeSearchRequest, 
    SchemeSearchResponse, 
    SchemeRecommendRequest, 
    SchemeRecommendResponse
)

router = APIRouter(prefix="/api/schemes", tags=["schemes"])
logger = get_logger(__name__)
scheme_service = SchemeService()


@router.post("/search", response_model=SchemeSearchResponse)
async def search_schemes(request: SchemeSearchRequest):
    """
    Search for government schemes based on query parameters.
    
    Args:
        request: Scheme search request containing query and filters.
        
    Returns:
        Scheme search response with matching schemes.
    """
    try:
        logger.info(f"Received scheme search request: {request.query}")
        result = await scheme_service.search_schemes(request)
        return result
    except APIException as e:
        logger.error(f"API error in scheme search: {e.message}")
        raise e.to_http_exception()
    except Exception as e:
        logger.error(f"Unexpected error in scheme search: {str(e)}")
        raise HTTPException(status_code=500, detail="Internal server error")


@router.post("/recommend", response_model=SchemeRecommendResponse)
async def recommend_schemes(request: SchemeRecommendRequest):
    """
    Recommend schemes based on user profile.
    
    Args:
        request: Scheme recommendation request with user profile.
        
    Returns:
        Scheme recommendation response with personalized suggestions.
    """
    try:
        logger.info("Received scheme recommendation request")
        result = await scheme_service.recommend_schemes(request)
        return result
    except APIException as e:
        logger.error(f"API error in scheme recommendation: {e.message}")
        raise e.to_http_exception()
    except Exception as e:
        logger.error(f"Unexpected error in scheme recommendation: {str(e)}")
        raise HTTPException(status_code=500, detail="Internal server error")
