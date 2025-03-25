from fastapi import HTTPException, status
from typing import Dict, Any, Optional, List, Union
import logging

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
)
logger = logging.getLogger(__name__)

class ContractAIError(Exception):
    """
    Base exception class for ContractAI backend
    """
    def __init__(
        self, 
        message: str, 
        status_code: int = status.HTTP_500_INTERNAL_SERVER_ERROR, 
        details: Optional[Dict[str, Any]] = None
    ):
        self.message = message
        self.status_code = status_code
        self.details = details or {}
        super().__init__(self.message)
        
        # Log the error
        logger.error(
            f"{self.__class__.__name__}: {message}", 
            extra={"details": self.details}
        )

    def to_http_exception(self) -> HTTPException:
        """Convert to FastAPI HTTPException"""
        return HTTPException(
            status_code=self.status_code,
            detail={
                "message": self.message,
                "details": self.details,
                "error_type": self.__class__.__name__
            }
        )


class DocumentProcessingError(ContractAIError):
    """Exception for document processing failures"""
    def __init__(self, message: str, details: Optional[Dict[str, Any]] = None):
        super().__init__(
            message=message,
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            details=details
        )


class StorageError(ContractAIError):
    """Exception for storage service failures"""
    def __init__(self, message: str, details: Optional[Dict[str, Any]] = None):
        super().__init__(
            message=message,
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            details=details
        )


class ValidationError(ContractAIError):
    """Exception for input validation failures"""
    def __init__(self, message: str, details: Optional[Dict[str, Any]] = None):
        super().__init__(
            message=message,
            status_code=status.HTTP_400_BAD_REQUEST,
            details=details
        )


class NotFoundError(ContractAIError):
    """Exception for resource not found"""
    def __init__(self, message: str, details: Optional[Dict[str, Any]] = None):
        super().__init__(
            message=message,
            status_code=status.HTTP_404_NOT_FOUND,
            details=details
        )


# Exception handler for FastAPI
def register_exception_handlers(app):
    """Register exception handlers with the FastAPI app"""
    
    @app.exception_handler(ContractAIError)
    async def contractai_exception_handler(request, exc):
        return exc.to_http_exception()
    
    # Add more exception handlers as needed 