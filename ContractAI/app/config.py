import os
import secrets
from typing import List, Dict, Any, Optional, Union
from functools import lru_cache
from pydantic_settings import BaseSettings
from pydantic import validator, Field
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()


class LLMProviderSettings(BaseSettings):
    """Settings for an individual LLM provider."""
    api_key: Optional[str] = None
    model_name: str
    endpoint: Optional[str] = None
    timeout: int = 30
    enabled: bool = False
    max_tokens: int = 4096
    retry_attempts: int = 3
    cost_per_1k_tokens: float = 0.0  # For cost tracking
    
    @validator('enabled', always=True)
    def check_api_key_present(cls, v, values):
        """Enable only if API key is present and non-empty."""
        return bool('api_key' in values and values['api_key'])


class Settings(BaseSettings):
    """Application settings loaded from environment variables."""
    
    # API settings
    API_V1_STR: str = "/api"
    PROJECT_NAME: str = "ContractAI"
    
    # CORS settings - restrict in production
    CORS_ORIGINS: List[str] = Field(
        default_factory=lambda: os.getenv("CORS_ORIGINS", "http://localhost:3000,http://localhost:8000").split(",")
    )
    
    # Security settings
    ALLOWED_HOSTS: List[str] = Field(
        default_factory=lambda: os.getenv("ALLOWED_HOSTS", "localhost,127.0.0.1").split(",")
    )
    
    # Database settings
    DATABASE_URL: str = os.getenv("DATABASE_URL", "")
    
    # JWT settings
    SECRET_KEY: str = os.getenv("SECRET_KEY", "")
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", "43200"))  # 30 days
    
    # Minio settings
    MINIO_ENDPOINT: str = os.getenv("MINIO_ENDPOINT", "")
    MINIO_ACCESS_KEY: str = os.getenv("MINIO_ACCESS_KEY", "")
    MINIO_SECRET_KEY: str = os.getenv("MINIO_SECRET_KEY", "")
    MINIO_SECURE: bool = os.getenv("MINIO_SECURE", "False").lower() == "true"
    DOCUMENT_BUCKET: str = "documents"
    PROCESSED_BUCKET: str = "processed-documents"
    
    # Redis settings
    REDIS_URL: str = os.getenv("REDIS_URL", "")
    
    # AI settings
    SPACY_MODEL: str = "en_core_web_lg"
    TRANSFORMER_MODEL: str = "distilbert-base-uncased"
    SENTENCE_TRANSFORMER_MODEL: str = "all-MiniLM-L6-v2"
    
    # LLM API keys
    OPENAI_API_KEY: Optional[str] = os.getenv("OPENAI_API_KEY")
    ANTHROPIC_API_KEY: Optional[str] = os.getenv("ANTHROPIC_API_KEY")
    COHERE_API_KEY: Optional[str] = os.getenv("COHERE_API_KEY")
    MISTRAL_API_KEY: Optional[str] = os.getenv("MISTRAL_API_KEY")
    
    # Processing settings
    MAX_DOCUMENT_SIZE: int = 10 * 1024 * 1024  # 10 MB
    ALLOWED_DOCUMENT_TYPES: List[str] = ["application/pdf", "application/msword", 
                                        "application/vnd.openxmlformats-officedocument.wordprocessingml.document"]
    
    # Logging settings
    LOG_LEVEL: str = os.getenv("LOG_LEVEL", "INFO")
    
    @validator("DATABASE_URL")
    def validate_database_url(cls, v):
        """Validate that the database URL is set."""
        if not v:
            raise ValueError("DATABASE_URL environment variable must be set")
        return v
    
    @validator("SECRET_KEY")
    def validate_secret_key(cls, v):
        """Validate that the secret key is set and has sufficient length."""
        if not v:
            raise ValueError("SECRET_KEY environment variable must be set")
        if len(v) < 32:
            raise ValueError("SECRET_KEY must be at least 32 characters long")
        return v
    
    @validator("MINIO_ENDPOINT", "MINIO_ACCESS_KEY", "MINIO_SECRET_KEY")
    def validate_minio_settings(cls, v, values, field):
        """Validate that Minio settings are provided."""
        if not v:
            raise ValueError(f"{field.name} environment variable must be set")
        return v
    
    @validator("REDIS_URL")
    def validate_redis_url(cls, v):
        """Validate that the Redis URL is set."""
        if not v:
            raise ValueError("REDIS_URL environment variable must be set")
        return v
    
    class Config:
        env_file = ".env"
        case_sensitive = True
        
        # Extra security for production
        @classmethod
        def customise_sources(cls, init_settings, env_settings, file_secret_settings):
            return init_settings, env_settings, file_secret_settings


# Generate secret key if running in development mode and not set
def generate_development_secret_key():
    """Generate a secret key for development purposes."""
    if os.getenv("ENVIRONMENT") == "development" and not os.getenv("SECRET_KEY"):
        # Only use this for local development
        print("WARNING: Generating temporary SECRET_KEY for development. Do NOT use in production!")
        os.environ["SECRET_KEY"] = secrets.token_hex(32)


# LLM provider configurations
def get_llm_provider_settings() -> Dict[str, LLMProviderSettings]:
    """
    Get settings for all LLM providers.
    
    Returns:
        Dictionary of provider settings
    """
    settings = get_settings()
    
    return {
        "openai": LLMProviderSettings(
            api_key=settings.OPENAI_API_KEY,
            model_name="gpt-4",
            timeout=60,
            cost_per_1k_tokens=0.03,  # Input tokens cost
            max_tokens=8192
        ),
        "anthropic": LLMProviderSettings(
            api_key=settings.ANTHROPIC_API_KEY,
            model_name="claude-3-opus-20240229",
            timeout=60,
            cost_per_1k_tokens=0.015,  # Input tokens cost
            max_tokens=100000
        ),
        "cohere": LLMProviderSettings(
            api_key=settings.COHERE_API_KEY,
            model_name="command",
            timeout=30,
            cost_per_1k_tokens=0.015,  # Approximate cost
            max_tokens=4096
        ),
        "mistral": LLMProviderSettings(
            api_key=settings.MISTRAL_API_KEY,
            model_name="mistral-large-latest",
            timeout=30,
            cost_per_1k_tokens=0.008,  # Approximate cost
            max_tokens=8192
        )
    }


# Agent-specific LLM recommendations
agent_llm_settings = {
    "clause_detection": {
        "primary": "anthropic",  # Superior document structure understanding
        "alternatives": ["openai", "mistral"]
    },
    "risk_analysis": {
        "primary": "openai",  # Best reasoning for risk identification
        "alternatives": ["anthropic", "mistral"]
    },
    "document_comparison": {
        "primary": "cohere",  # Specialized in semantic comparison
        "alternatives": ["openai", "anthropic"]
    },
    "recommendation": {
        "primary": "mistral",  # Optimal performance/cost balance
        "alternatives": ["openai", "anthropic"]
    }
}


# Generate development secret key if needed
generate_development_secret_key()


@lru_cache()
def get_settings() -> Settings:
    """
    Returns application settings as a cached instance.
    
    Using lru_cache to avoid loading .env file for each request.
    """
    return Settings()


def get_enabled_llm_providers() -> Dict[str, LLMProviderSettings]:
    """
    Get only the enabled LLM providers.
    
    Returns:
        Dictionary of enabled provider settings
    """
    all_providers = get_llm_provider_settings()
    return {name: settings for name, settings in all_providers.items() if settings.enabled}