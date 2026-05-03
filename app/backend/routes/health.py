from fastapi import APIRouter, HTTPException
from utils.logger import get_logger
from services.health_service import HealthService
from schemas.health import HealthResponse

router = APIRouter(prefix="/api", tags=["health"])
logger = get_logger(__name__)
health_service = HealthService()


@router.get("/health", response_model=HealthResponse)
async def health_check():
    """
    Health check endpoint.
    
    Returns:
        Health status of the application.
    """
    try:
        health_data = await health_service.get_health_status()
        return HealthResponse(**health_data)
    except Exception as e:
        logger.error(f"Health check failed: {str(e)}")
        raise HTTPException(status_code=500, detail="Health check failed")
