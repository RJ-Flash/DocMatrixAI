"""
Factory for creating and managing LLM clients.

This module provides a factory for creating and managing LLM clients
for different providers, with support for fallbacks and dynamic selection.
"""

import logging
import asyncio
from typing import Dict, Any, Optional, List, Tuple, Union
from enum import Enum

from app.config import get_llm_provider_settings, agent_llm_settings, get_enabled_llm_providers
from app.ai.token_counter import count_tokens, count_messages_tokens

logger = logging.getLogger(__name__)

class LLMProvider(str, Enum):
    """Enum of supported LLM providers."""
    OPENAI = "openai"
    ANTHROPIC = "anthropic"
    COHERE = "cohere"
    MISTRAL = "mistral"

class LLMNotAvailableError(Exception):
    """Exception raised when an LLM is not available."""
    pass

class LLMFactory:
    """Factory for creating LLM clients based on configuration."""
    
    _instances: Dict[str, Any] = {}
    _token_counters: Dict[str, Dict[str, Union[int, float]]] = {}
    _initialized: bool = False
    
    @classmethod
    def initialize(cls):
        """
        Initialize the factory with settings.
        """
        # Initialize token counters
        for provider in [p.value for p in LLMProvider]:
            cls._token_counters[provider] = {"input": 0, "output": 0, "cost": 0.0}
        
        # Log available providers
        enabled_providers = get_enabled_llm_providers()
        
        if enabled_providers:
            logger.info(f"Available LLM providers: {', '.join(enabled_providers.keys())}")
        else:
            logger.warning("No LLM providers available. Check API key configuration.")
            
        cls._initialized = True
    
    @classmethod
    async def get_llm(cls, provider_name: str) -> Any:
        """
        Get an LLM client for the specified provider.
        
        Args:
            provider_name: Name of the LLM provider
            
        Returns:
            LLM client instance
            
        Raises:
            LLMNotAvailableError: If the LLM is not available
        """
        if not cls._initialized:
            cls.initialize()
            
        if provider_name in cls._instances:
            return cls._instances[provider_name]
        
        # Get provider settings
        provider_settings = get_llm_provider_settings().get(provider_name)
        if not provider_settings or not provider_settings.enabled:
            raise LLMNotAvailableError(f"LLM provider '{provider_name}' is not available or not enabled")
        
        # Create the client based on provider type
        try:
            client = await cls._create_client(provider_name, provider_settings)
            cls._instances[provider_name] = client
            return client
        except Exception as e:
            logger.error(f"Failed to initialize {provider_name} client: {str(e)}")
            raise LLMNotAvailableError(f"Failed to initialize {provider_name} client: {str(e)}")
    
    @classmethod
    async def get_agent_llm(cls, agent_name: str) -> Tuple[str, str, Any]:
        """
        Get the appropriate LLM for a specific agent, falling back to alternatives if needed.
        
        Args:
            agent_name: Name of the agent (e.g., "clause_detection")
            
        Returns:
            Tuple of (provider_name, model_name, llm_client)
            
        Raises:
            LLMNotAvailableError: If no suitable LLM is available
        """
        if not cls._initialized:
            cls.initialize()
            
        # Get agent settings
        if agent_name not in agent_llm_settings:
            raise ValueError(f"No configuration found for agent '{agent_name}'")
            
        agent_config = agent_llm_settings[agent_name]
        
        # Try primary provider first
        primary_provider = agent_config.get("primary")
        
        if primary_provider:
            try:
                provider_settings = get_llm_provider_settings().get(primary_provider)
                if provider_settings and provider_settings.enabled:
                    llm = await cls.get_llm(primary_provider)
                    logger.info(f"Using {primary_provider}/{provider_settings.model_name} for {agent_name} agent")
                    return primary_provider, provider_settings.model_name, llm
            except LLMNotAvailableError as e:
                logger.warning(f"Primary LLM {primary_provider} for {agent_name} not available: {str(e)}")
        
        # Try alternatives
        alternatives = agent_config.get("alternatives", [])
        for provider_name in alternatives:
            try:
                provider_settings = get_llm_provider_settings().get(provider_name)
                if provider_settings and provider_settings.enabled:
                    llm = await cls.get_llm(provider_name)
                    logger.info(f"Using alternative LLM {provider_name}/{provider_settings.model_name} for {agent_name} agent")
                    return provider_name, provider_settings.model_name, llm
            except LLMNotAvailableError:
                continue
        
        # If we get here, no suitable LLM was found
        raise LLMNotAvailableError(f"No suitable LLM available for agent '{agent_name}'")
    
    @classmethod
    async def list_available_providers(cls) -> List[str]:
        """
        List all available LLM providers.
        
        Returns:
            List of available provider names
        """
        if not cls._initialized:
            cls.initialize()
            
        enabled_providers = get_enabled_llm_providers()
        return list(enabled_providers.keys())
    
    @classmethod
    async def _create_client(cls, provider_name: str, provider_settings: Any) -> Any:
        """
        Create an LLM client for the specified provider.
        
        Args:
            provider_name: Name of the LLM provider
            provider_settings: Settings for the provider
            
        Returns:
            LLM client instance
        """
        if provider_name == LLMProvider.OPENAI.value:
            # Import here to avoid dependencies if not used
            from openai import AsyncOpenAI
            client = AsyncOpenAI(api_key=provider_settings.api_key)
            # Verify connection
            await client.models.list()
            return client
            
        elif provider_name == LLMProvider.ANTHROPIC.value:
            from anthropic import AsyncAnthropic
            client = AsyncAnthropic(api_key=provider_settings.api_key)
            # Verify connection by listing models
            await client.models.list()
            return client
            
        elif provider_name == LLMProvider.COHERE.value:
            import cohere
            # Cohere doesn't have async client, use sync
            client = cohere.Client(api_key=provider_settings.api_key)
            # Verify connection
            client.check_api_key()
            return client
            
        elif provider_name == LLMProvider.MISTRAL.value:
            from mistralai.async_client import MistralAsyncClient
            client = MistralAsyncClient(api_key=provider_settings.api_key)
            # Verify connection
            await client.list_models()
            return client
            
        else:
            raise ValueError(f"Unsupported LLM provider: {provider_name}")
    
    @classmethod
    def update_token_count(cls, provider: str, input_tokens: int, output_tokens: int, cost: float = None) -> None:
        """
        Update token usage counters.
        
        Args:
            provider: Provider name
            input_tokens: Number of input tokens
            output_tokens: Number of output tokens
            cost: Optional cost of the request
        """
        if not cls._initialized:
            cls.initialize()
            
        if provider not in cls._token_counters:
            cls._token_counters[provider] = {"input": 0, "output": 0, "cost": 0.0}
            
        cls._token_counters[provider]["input"] += input_tokens
        cls._token_counters[provider]["output"] += output_tokens
        
        if cost is not None:
            cls._token_counters[provider]["cost"] += cost
        else:
            # Calculate cost based on provider settings
            provider_settings = get_llm_provider_settings().get(provider)
            if provider_settings:
                input_cost = (input_tokens / 1000) * provider_settings.cost_per_1k_tokens
                # Output cost is typically higher, use 2x as a rough estimate if not specified
                output_cost = (output_tokens / 1000) * (provider_settings.cost_per_1k_tokens * 2)
                cls._token_counters[provider]["cost"] += input_cost + output_cost
    
    @classmethod
    def get_token_usage(cls) -> Dict[str, Dict[str, Union[int, float]]]:
        """
        Get token usage statistics.
        
        Returns:
            Dictionary of token usage by provider
        """
        if not cls._initialized:
            cls.initialize()
            
        return cls._token_counters.copy() 