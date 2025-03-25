"""
Redis service for ContractAI.
"""

import logging
import aioredis
from typing import Optional

logger = logging.getLogger(__name__)

class RedisService:
    """Service for Redis connections and operations."""
    
    _instance: Optional[aioredis.Redis] = None
    
    @classmethod
    async def get_redis(cls) -> aioredis.Redis:
        """
        Get a Redis client instance.
        
        Returns:
            Redis client
        """
        if cls._instance is None:
            from app.config import get_settings
            settings = get_settings()
            
            try:
                logger.info(f"Connecting to Redis at {settings.REDIS_URL}")
                cls._instance = await aioredis.from_url(
                    settings.REDIS_URL,
                    encoding="utf-8",
                    decode_responses=False
                )
                logger.info("Connected to Redis successfully")
            except Exception as e:
                logger.error(f"Failed to connect to Redis: {e}")
                raise
                
        return cls._instance
    
    @classmethod
    async def close(cls) -> None:
        """Close the Redis connection."""
        if cls._instance is not None:
            await cls._instance.close()
            cls._instance = None
            logger.info("Redis connection closed") 