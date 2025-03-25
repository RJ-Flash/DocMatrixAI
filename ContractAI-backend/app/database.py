from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import QueuePool
import logging
import os

from app.config import settings

# Configure logging
logger = logging.getLogger(__name__)

# Create database URL from settings
SQLALCHEMY_DATABASE_URL = settings.DATABASE_URL

# Create engine with connection pooling
engine_kwargs = {
    "poolclass": QueuePool,
    "pool_size": 5,
    "max_overflow": 10,
    "pool_timeout": 30,
    "pool_pre_ping": True,
}

# If using SQLite, we need to disable check_same_thread
if "sqlite" in SQLALCHEMY_DATABASE_URL:
    engine_kwargs["connect_args"] = {"check_same_thread": False}
    
engine = create_engine(
    SQLALCHEMY_DATABASE_URL, 
    **engine_kwargs
)

# Create session factory
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Base class for models
Base = declarative_base()

# FastAPI dependency for database sessions
def get_db():
    """
    Dependency function to get a database session.
    Use this for FastAPI dependency injection.
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

def create_tables():
    """Create all tables in the database."""
    try:
        # Import all models here to ensure they're registered with Base.metadata
        from app.models.document import Document, DocumentText
        
        # Create tables
        Base.metadata.create_all(bind=engine)
        logger.info("Database tables created successfully")
    except Exception as e:
        logger.error(f"Error creating database tables: {str(e)}")
        raise
