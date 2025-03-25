"""
Cache service for LLM responses.

This module provides caching functionality for LLM responses to improve
performance and reduce costs by avoiding redundant API calls.
"""

import json
import logging
import hashlib
from typing import Dict, Any, Optional, Union
import aioredis
import time

logger = logging.getLogger(__name__)

class LLMResponseCache:
    """
    Cache for LLM responses to avoid redundant API calls.
    
    This class provides methods to cache and retrieve LLM responses
    based on input prompts and model parameters.
    """
    
    def __init__(self, redis_client: aioredis.Redis, ttl: int = 86400):
        """
        Initialize the LLM response cache.
        
        Args:
            redis_client: Redis client for storing cache entries
            ttl: Time-to-live for cache entries in seconds (default: 24 hours)
        """
        self.redis = redis_client
        self.ttl = ttl
        self.cache_hits = 0
        self.cache_misses = 0
        logger.info(f"Initialized LLM response cache with TTL of {ttl} seconds")
    
    def _generate_cache_key(self, prompt: str, model_name: str, params: Dict[str, Any]) -> str:
        """
        Generate a cache key based on the prompt, model name, and parameters.
        
        Args:
            prompt: The input prompt
            model_name: The name of the LLM model
            params: Model parameters
            
        Returns:
            A unique cache key
        """
        # Create a string representation of the parameters
        params_str = json.dumps(params, sort_keys=True)
        
        # Combine prompt, model name, and parameters
        combined = f"{prompt}:{model_name}:{params_str}"
        
        # Generate a hash
        key = hashlib.md5(combined.encode()).hexdigest()
        return f"llm:cache:{key}"
    
    async def get(self, prompt: str, model_name: str, params: Dict[str, Any]) -> Optional[Dict[str, Any]]:
        """
        Get a cached LLM response.
        
        Args:
            prompt: The input prompt
            model_name: The name of the LLM model
            params: Model parameters
            
        Returns:
            The cached response or None if not found
        """
        key = self._generate_cache_key(prompt, model_name, params)
        
        try:
            cached = await self.redis.get(key)
            
            if cached:
                self.cache_hits += 1
                response = json.loads(cached)
                logger.debug(f"Cache hit for key {key}")
                
                # Add cache metadata
                response["cached"] = True
                response["cache_time"] = time.time()
                
                return response
            else:
                self.cache_misses += 1
                logger.debug(f"Cache miss for key {key}")
                return None
                
        except Exception as e:
            logger.warning(f"Error retrieving from cache: {str(e)}")
            return None
    
    async def set(self, prompt: str, model_name: str, params: Dict[str, Any], 
                 response: Dict[str, Any]) -> bool:
        """
        Cache an LLM response.
        
        Args:
            prompt: The input prompt
            model_name: The name of the LLM model
            params: Model parameters
            response: The LLM response to cache
            
        Returns:
            True if successful, False otherwise
        """
        key = self._generate_cache_key(prompt, model_name, params)
        
        # Create a copy of the response to avoid modifying the original
        cache_data = response.copy()
        
        # Remove any cache metadata if present
        cache_data.pop("cached", None)
        cache_data.pop("cache_time", None)
        
        try:
            # Add timestamp for when this was cached
            cache_data["_cached_at"] = time.time()
            
            # Store in Redis with TTL
            await self.redis.setex(
                key, 
                self.ttl,
                json.dumps(cache_data)
            )
            logger.debug(f"Cached response for key {key}")
            return True
            
        except Exception as e:
            logger.warning(f"Error caching response: {str(e)}")
            return False
    
    async def invalidate(self, prompt: str, model_name: str, params: Dict[str, Any]) -> bool:
        """
        Invalidate a cached response.
        
        Args:
            prompt: The input prompt
            model_name: The name of the LLM model
            params: Model parameters
            
        Returns:
            True if successful, False otherwise
        """
        key = self._generate_cache_key(prompt, model_name, params)
        
        try:
            await self.redis.delete(key)
            logger.debug(f"Invalidated cache for key {key}")
            return True
            
        except Exception as e:
            logger.warning(f"Error invalidating cache: {str(e)}")
            return False
    
    async def get_stats(self) -> Dict[str, int]:
        """
        Get cache statistics.
        
        Returns:
            Dictionary with cache hit and miss counts
        """
        return {
            "hits": self.cache_hits,
            "misses": self.cache_misses,
            "hit_ratio": self.cache_hits / (self.cache_hits + self.cache_misses) if (self.cache_hits + self.cache_misses) > 0 else 0
        }
    
    async def clear(self) -> bool:
        """
        Clear all cached responses.
        
        Returns:
            True if successful, False otherwise
        """
        try:
            # Get all keys matching the pattern
            cursor = b'0'
            keys = []
            
            while cursor:
                cursor, partial_keys = await self.redis.scan(
                    cursor=cursor, 
                    match="llm:cache:*", 
                    count=100
                )
                keys.extend(partial_keys)
                
                if cursor == b'0':
                    break
            
            # Delete all keys
            if keys:
                await self.redis.delete(*keys)
                
            logger.info(f"Cleared {len(keys)} cache entries")
            return True
            
        except Exception as e:
            logger.warning(f"Error clearing cache: {str(e)}")
            return False
    
    async def get_with_key(self, cache_key: str) -> Optional[Dict[str, Any]]:
        """
        Get a cached LLM response using a pre-generated cache key.
        
        Args:
            cache_key: The cache key
            
        Returns:
            The cached response or None if not found
        """
        try:
            cached = await self.redis.get(cache_key)
            
            if cached:
                self.cache_hits += 1
                response = json.loads(cached)
                logger.debug(f"Cache hit for key {cache_key}")
                
                # Add cache metadata
                response["cached"] = True
                response["cache_time"] = time.time()
                
                return response
            else:
                self.cache_misses += 1
                logger.debug(f"Cache miss for key {cache_key}")
                return None
                
        except Exception as e:
            logger.warning(f"Error retrieving from cache: {str(e)}")
            return None
    
    async def set_with_key(self, cache_key: str, response: Dict[str, Any], ttl: Optional[int] = None) -> bool:
        """
        Cache an LLM response using a pre-generated cache key.
        
        Args:
            cache_key: The cache key
            response: The LLM response to cache
            ttl: Optional custom TTL in seconds
            
        Returns:
            True if successful, False otherwise
        """
        # Create a copy of the response to avoid modifying the original
        cache_data = response.copy()
        
        # Remove any cache metadata if present
        cache_data.pop("cached", None)
        cache_data.pop("cache_time", None)
        
        try:
            # Add timestamp for when this was cached
            cache_data["_cached_at"] = time.time()
            
            # Store in Redis with TTL
            await self.redis.setex(
                cache_key, 
                ttl or self.ttl,
                json.dumps(cache_data)
            )
            logger.debug(f"Cached response for key {cache_key}")
            return True
            
        except Exception as e:
            logger.warning(f"Error caching response: {str(e)}")
            return False
    
    def generate_agent_cache_key(self, agent_name: str, operation: str, input_data: Dict[str, Any]) -> str:
        """
        Generate a cache key for an agent operation.
        
        Args:
            agent_name: Name of the agent
            operation: Operation being performed
            input_data: Input data for the operation
            
        Returns:
            A unique cache key
        """
        # Create a string representation of the input data
        input_str = json.dumps(input_data, sort_keys=True)
        
        # Combine agent name, operation, and input data
        combined = f"{agent_name}:{operation}:{input_str}"
        
        # Generate a hash
        key = hashlib.md5(combined.encode()).hexdigest()
        return f"llm:agent_cache:{key}" 