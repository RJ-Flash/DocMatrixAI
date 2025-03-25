import logging
from fastapi import FastAPI, Request, status
from fastapi.responses import JSONResponse
from fastapi.exceptions import RequestValidationError
from sqlalchemy.exc import SQLAlchemyError
from jose import JWTError

logger = logging.getLogger(__name__)


class ContractAIException(Exception):
    """Base exception class for ContractAI application."""
    
    def __init__(self, status_code: int, detail: str):
        self.status_code = status_code
        self.detail = detail


class DocumentProcessingError(ContractAIException):
    """Exception raised when document processing fails."""
    
    def __init__(self, detail: str):
        super().__init__(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=detail)


class StorageError(ContractAIException):
    """Exception raised when storage operations fail."""
    
    def __init__(self, detail: str):
        super().__init__(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=detail)


class StorageAuthError(StorageError):
    """Exception raised when storage authentication fails."""
    
    def __init__(self, detail: str):
        super().__init__(detail=detail)
        self.status_code = status.HTTP_401_UNAUTHORIZED


class StorageTimeoutError(StorageError):
    """Exception raised when storage operations timeout."""
    
    def __init__(self, detail: str):
        super().__init__(detail=detail)
        self.status_code = status.HTTP_504_GATEWAY_TIMEOUT


class BucketNotFoundError(StorageError):
    """Exception raised when a storage bucket is not found."""
    
    def __init__(self, detail: str):
        super().__init__(detail=detail)
        self.status_code = status.HTTP_404_NOT_FOUND


class DocumentNotFoundError(ContractAIException):
    """Exception raised when a document is not found."""
    
    def __init__(self, document_id_or_path):
        # Handle both integer IDs and string paths
        if isinstance(document_id_or_path, int):
            detail = f"Document with ID {document_id_or_path} not found"
        else:
            detail = f"Document not found: {document_id_or_path}"
            
        super().__init__(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=detail,
        )


class AnalysisNotFoundError(ContractAIException):
    """Exception raised when an analysis is not found."""
    
    def __init__(self, document_id: int):
        super().__init__(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Analysis for document {document_id} not found",
        )


class AccessDeniedError(ContractAIException):
    """Exception raised when user does not have access to a resource."""
    
    def __init__(self):
        super().__init__(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Access denied to this resource",
        )


class InactiveUserError(ContractAIException):
    """Exception raised when a user account is inactive."""
    
    def __init__(self):
        super().__init__(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Inactive user",
        )


class RateLimitExceededError(ContractAIException):
    """Exception raised when API rate limit is exceeded."""
    
    def __init__(self, detail: str = "Rate limit exceeded"):
        super().__init__(
            status_code=status.HTTP_429_TOO_MANY_REQUESTS,
            detail=detail,
        )


def configure_exception_handlers(app: FastAPI):
    """Configure exception handlers for the FastAPI application."""
    
    @app.exception_handler(ContractAIException)
    async def contractai_exception_handler(request: Request, exc: ContractAIException):
        """Handle ContractAIException and its subclasses."""
        logger.error(f"ContractAIException: {exc.detail}")
        return JSONResponse(
            status_code=exc.status_code,
            content={"detail": exc.detail},
        )
    
    @app.exception_handler(RequestValidationError)
    async def validation_exception_handler(request: Request, exc: RequestValidationError):
        """Handle validation errors."""
        logger.error(f"ValidationError: {exc.errors()}")
        return JSONResponse(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            content={"detail": exc.errors()},
        )
    
    @app.exception_handler(JWTError)
    async def jwt_exception_handler(request: Request, exc: JWTError):
        """Handle JWT errors."""
        logger.error(f"JWTError: {str(exc)}")
        return JSONResponse(
            status_code=status.HTTP_401_UNAUTHORIZED,
            content={"detail": "Invalid authentication credentials"},
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    @app.exception_handler(SQLAlchemyError)
    async def sqlalchemy_exception_handler(request: Request, exc: SQLAlchemyError):
        """Handle SQLAlchemy errors."""
        logger.error(f"SQLAlchemyError: {str(exc)}")
        return JSONResponse(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            content={"detail": "Database error occurred"},
        )
    
    @app.exception_handler(Exception)
    async def general_exception_handler(request: Request, exc: Exception):
        """Handle all unhandled exceptions."""
        logger.exception(f"Unhandled exception: {str(exc)}")
        return JSONResponse(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            content={"detail": "An unexpected error occurred"},
        )