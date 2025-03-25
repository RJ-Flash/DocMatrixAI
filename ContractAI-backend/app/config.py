import os
from dotenv import load_dotenv
import logging
from typing import List, Optional

# Load variables from .env
load_dotenv()

class Settings:
    # Application settings
    SECRET_KEY: str = os.getenv("SECRET_KEY")
    ENVIRONMENT: str = os.getenv("ENVIRONMENT", "development")
    
    # MinIO settings
    MINIO_ENDPOINT: str = os.getenv("MINIO_ENDPOINT")
    MINIO_ACCESS_KEY: str = os.getenv("MINIO_ACCESS_KEY")
    MINIO_SECRET_KEY: str = os.getenv("MINIO_SECRET_KEY")
    MINIO_BUCKET: str = os.getenv("MINIO_BUCKET")
    MINIO_SECURE: bool = os.getenv("MINIO_SECURE", "false").lower() == "true"
    
    # Database settings
    DATABASE_URL: str = os.getenv("DATABASE_URL", "sqlite:///./contractai.db")
    
    # OCR settings
    TESSERACT_LANGUAGE: str = os.getenv("TESSERACT_LANGUAGE", "eng")
    MAX_FILE_SIZE_MB: int = int(os.getenv("MAX_FILE_SIZE_MB", "10"))
    MAX_FILE_SIZE_BYTES: int = MAX_FILE_SIZE_MB * 1024 * 1024
    MAX_PDF_PAGES: int = int(os.getenv("MAX_PDF_PAGES", "50"))
    
    # API settings
    API_RATE_LIMIT: int = int(os.getenv("API_RATE_LIMIT", "100"))
    ALLOWED_ORIGINS: List[str] = os.getenv("ALLOWED_ORIGINS", "http://localhost:3000,http://localhost:8000").split(",")
    
    # Logging
    LOG_LEVEL: str = os.getenv("LOG_LEVEL", "INFO")
    
    # Production configuration
    @property
    def is_production(self) -> bool:
        return self.ENVIRONMENT.lower() == "production"
    
    @property
    def is_development(self) -> bool:
        return self.ENVIRONMENT.lower() == "development"
    
    @property
    def is_testing(self) -> bool:
        return self.ENVIRONMENT.lower() == "testing"
    
    # Validate required settings
    @classmethod
    def validate(cls):
        # Required settings for all environments
        required_common = {
            "SECRET_KEY": cls.SECRET_KEY,
            "MINIO_ENDPOINT": cls.MINIO_ENDPOINT,
            "MINIO_ACCESS_KEY": cls.MINIO_ACCESS_KEY,
            "MINIO_SECRET_KEY": cls.MINIO_SECRET_KEY,
            "MINIO_BUCKET": cls.MINIO_BUCKET,
        }
        
        # Additional required settings for production
        if cls.ENVIRONMENT.lower() == "production":
            required_production = {
                # Add production-specific required settings here
            }
            required_common.update(required_production)
        
        # Check all required settings
        missing = [key for key, value in required_common.items() if not value]
        if missing:
            error_msg = f"Missing required environment variables: {', '.join(missing)}"
            logging.error(error_msg)
            raise ValueError(error_msg)
        
        # Configure logging based on the environment
        logging_level = getattr(logging, cls.LOG_LEVEL.upper(), logging.INFO)
        logging.basicConfig(
            level=logging_level,
            format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        )
        
        # Log startup configuration (but mask sensitive values)
        masked_config = {
            **{k: v for k, v in cls.__dict__.items() if not k.startswith('_') and k.isupper()},
            "SECRET_KEY": "*****" if cls.SECRET_KEY else None,
            "MINIO_SECRET_KEY": "*****" if cls.MINIO_SECRET_KEY else None,
            "MINIO_ACCESS_KEY": "*****" if cls.MINIO_ACCESS_KEY else None,
        }
        
        logging.info(f"Application starting with configuration: {masked_config}")
        
        # Warn about development settings in production
        if cls.ENVIRONMENT.lower() == "production":
            if cls.ALLOWED_ORIGINS == ["*"]:
                logging.warning("Security Warning: CORS allows all origins in production!")
            
            if "localhost" in str(cls.ALLOWED_ORIGINS):
                logging.warning("Security Warning: CORS allows localhost in production!")
                
            if not cls.MINIO_SECURE:
                logging.warning("Security Warning: MinIO connection is not secure in production!")

# Create and validate settings instance
settings = Settings()
settings.validate()
