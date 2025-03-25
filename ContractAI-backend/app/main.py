from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.middleware.gzip import GZipMiddleware
from fastapi.middleware.trustedhost import TrustedHostMiddleware
from app.routes import documents
from app.config import settings
from app.core.errors import register_exception_handlers
from app.database import create_tables
import logging
import os

# Configure logging
logger = logging.getLogger(__name__)

# Create FastAPI application
app = FastAPI(
    title="ContractAI API",
    description="AI-powered contract analysis and intelligence platform",
    version="0.1.0"
)

# Security middlewares
app.add_middleware(GZipMiddleware, minimum_size=1000)
app.add_middleware(
    TrustedHostMiddleware, 
    allowed_hosts=["localhost", "127.0.0.1", "*"] if os.getenv("ENVIRONMENT") == "development" else ["api.contractai.com"]
)

# CORS configuration
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.ALLOWED_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Register custom exception handlers
register_exception_handlers(app)

# Include routes
app.include_router(documents.router, prefix="/api/documents")

# Health check endpoint
@app.get("/health")
async def health_check():
    """
    Health check endpoint for monitoring and load balancers.
    """
    return {
        "status": "healthy", 
        "version": "0.1.0",
        "environment": settings.ENVIRONMENT
    }

# Startup event
@app.on_event("startup")
async def startup_event():
    """
    Run tasks on application startup.
    """
    logger.info("Starting ContractAI API application")
    
    # Create database tables
    create_tables()
    
    logger.info("ContractAI API application started successfully")

# Shutdown event
@app.on_event("shutdown")
async def shutdown_event():
    """
    Run tasks on application shutdown.
    """
    logger.info("Shutting down ContractAI API application")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("app.main:app", host="0.0.0.0", port=8000, reload=True)
