from datetime import datetime
from typing import Dict, Any
from utils.logger import get_logger
from config.settings import settings


class HealthService:
    """Service for health check operations."""
    
    def __init__(self):
        self.logger = get_logger(__name__)
    
    async def get_health_status(self) -> Dict[str, Any]:
        """
        Get the health status of the application.
        
        Returns:
            Dictionary containing health status information.
        """
        try:
            self.logger.info("Health check requested")
            
            health_data = {
                "status": "ok",
                "version": settings.app_version,
                "timestamp": datetime.utcnow().isoformat() + "Z"
            }
            
            self.logger.info("Health check completed successfully")
            return health_data
            
        except Exception as e:
            self.logger.error(f"Health check failed: {str(e)}")
            raise
