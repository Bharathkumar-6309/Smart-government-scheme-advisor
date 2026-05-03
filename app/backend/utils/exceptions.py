from fastapi import HTTPException
from typing import Any, Dict, Optional


class APIException(Exception):
    """Base API exception class."""
    
    def __init__(
        self,
        message: str,
        status_code: int = 500,
        details: Optional[Dict[str, Any]] = None
    ):
        self.message = message
        self.status_code = status_code
        self.details = details or {}
        super().__init__(self.message)
    
    def to_http_exception(self) -> HTTPException:
        """Convert to FastAPI HTTPException."""
        return HTTPException(
            status_code=self.status_code,
            detail={
                "message": self.message,
                "details": self.details
            }
        )


class NotFoundError(APIException):
    """Exception raised when a resource is not found."""
    
    def __init__(self, message: str = "Resource not found", details: Optional[Dict[str, Any]] = None):
        super().__init__(message=message, status_code=404, details=details)


class ValidationError(APIException):
    """Exception raised when validation fails."""
    
    def __init__(self, message: str = "Validation error", details: Optional[Dict[str, Any]] = None):
        super().__init__(message=message, status_code=422, details=details)


class InternalServerError(APIException):
    """Exception raised for internal server errors."""
    
    def __init__(self, message: str = "Internal server error", details: Optional[Dict[str, Any]] = None):
        super().__init__(message=message, status_code=500, details=details)
