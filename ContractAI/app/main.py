import logging
from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.middleware.cors import CORSMiddleware
from app.api import auth, documents, analysis, admin
from app.core.errors import configure_exception_handlers
from app.database import Base, engine
from app.config import get_settings

# Create tables
Base.metadata.create_all(bind=engine)

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
)
logger = logging.getLogger(__name__)

# Initialize application
app = FastAPI(
    title="ContractAI API",
    description="AI-powered contract analysis API",
    version="1.0.0",
)

# Configure CORS
settings = get_settings()
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Configure exception handlers
configure_exception_handlers(app)

# Include API routers
app.include_router(auth.router, prefix="/api/auth", tags=["Authentication"])
app.include_router(documents.router, prefix="/api/documents", tags=["Documents"])
app.include_router(analysis.router, prefix="/api/analysis", tags=["Analysis"])
app.include_router(admin.router, prefix="/api/admin", tags=["Admin"])


@app.get("/", tags=["Health"])
async def health_check():
    """
    Health check endpoint for API status monitoring.
    """
    return {"status": "healthy", "version": "1.0.0"}


def run_app():
    """
    Entry point for the application when installed as a package.
    This function is referenced in setup.py.
    """
    import uvicorn
    uvicorn.run("app.main:app", host="0.0.0.0", port=8000, reload=True)


if __name__ == "__main__":
    run_app()