"""
Base agent class for ContractAI.

This module provides a base agent class that all specialized agents will inherit from.
"""

import logging
import time
import json
from typing import Dict, Any, List, Optional, Union, Tuple
import asyncio

from app.services.cache_service import LLMResponseCache
from app.monitoring.llm_metrics import LLMMetricsTracker
from app.ai.llm_factory import LLMFactory, LLMNotAvailableError
from app.ai.token_counter import count_tokens, count_messages_tokens
from app.config import get_llm_provider_settings

logger = logging.getLogger(__name__)

class BaseAgent:
    """
    Base agent class for ContractAI.
    
    This class provides common functionality for all agents, including:
    - LLM client management
    - Caching
    - Metrics tracking
    - Error handling
    - Retry logic
    """
    
    def __init__(
        self,
        agent_name: str,
        cache_service: LLMResponseCache,
        metrics_tracker: LLMMetricsTracker,
        max_retries: int = 3,
        retry_delay: float = 1.0
    ):
        """
        Initialize the base agent.
        
        Args:
            agent_name: Name of the agent
            cache_service: Cache service for LLM responses
            metrics_tracker: Metrics tracker for LLM usage
            max_retries: Maximum number of retries for LLM calls
            retry_delay: Delay between retries in seconds
        """
        self.agent_name = agent_name
        self.cache_service = cache_service
        self.metrics_tracker = metrics_tracker
        self.max_retries = max_retries
        self.retry_delay = retry_delay
        self.provider = None
        self.model = None
        self.llm = None
        self.initialized = False
        
        logger.info(f"Initialized {agent_name} agent")
    
    async def initialize(self) -> None:
        """
        Initialize the agent by setting up the LLM client.
        
        This method should be called before using the agent.
        """
        if self.initialized:
            return
            
        try:
            # Get LLM client for this agent
            self.provider, self.model, self.llm = await LLMFactory.get_agent_llm(self.agent_name)
            logger.info(f"{self.agent_name} agent initialized with {self.provider}/{self.model}")
            self.initialized = True
        except LLMNotAvailableError as e:
            logger.error(f"Failed to initialize {self.agent_name} agent: {str(e)}")
            raise
    
    async def _call_llm(
        self,
        prompt: str,
        system_prompt: Optional[str] = None,
        temperature: Optional[float] = None,
        max_tokens: Optional[int] = None,
        use_cache: bool = True,
        cache_ttl: Optional[int] = None,
        operation: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        Call the LLM with retry logic, caching, and metrics tracking.
        
        Args:
            prompt: The user prompt
            system_prompt: Optional system prompt
            temperature: Optional temperature override
            max_tokens: Optional max tokens override
            use_cache: Whether to use cache
            cache_ttl: Optional cache TTL override
            operation: Optional operation name for metrics
            
        Returns:
            LLM response
        """
        if not self.initialized:
            await self.initialize()
            
        # Prepare messages
        messages = []
        if system_prompt:
            messages.append({"role": "system", "content": system_prompt})
        messages.append({"role": "user", "content": prompt})
        
        # Get provider settings
        provider_settings = get_llm_provider_settings().get(self.provider)
        
        # Prepare parameters
        params = {
            "temperature": temperature if temperature is not None else 0.0,
            "max_tokens": max_tokens if max_tokens is not None else (
                provider_settings.max_tokens if provider_settings else 2000
            )
        }
        
        # Generate cache key
        cache_key = None
        if use_cache:
            cache_data = {
                "messages": messages,
                "params": params,
                "provider": self.provider,
                "model": self.model
            }
            cache_key = self.cache_service.generate_agent_cache_key(
                self.agent_name,
                operation or "call_llm",
                cache_data
            )
            
            # Check cache
            cached_response = await self.cache_service.get_with_key(cache_key)
            if cached_response:
                logger.info(f"Using cached response for {self.agent_name} agent")
                
                # Record cache hit in metrics
                if operation:
                    await self.metrics_tracker.record_llm_call(
                        provider=self.provider,
                        model=self.model,
                        agent=self.agent_name,
                        input_tokens=0,  # Not counted for cache hits
                        output_tokens=0,  # Not counted for cache hits
                        latency_ms=0,    # Not counted for cache hits
                        success=True,
                        cost=0.0,        # No cost for cache hits
                        cached=True,
                        metadata={"operation": operation}
                    )
                
                return cached_response
        
        # Count tokens
        prompt_tokens = count_messages_tokens(messages, self.model)
        
        # Call LLM with retries
        start_time = time.time()
        response = None
        error = None
        
        for attempt in range(self.max_retries):
            try:
                if self.provider == "openai":
                    response = await self._call_openai(messages, params)
                elif self.provider == "anthropic":
                    response = await self._call_anthropic(messages, params)
                elif self.provider == "cohere":
                    response = await self._call_cohere(messages, params)
                elif self.provider == "mistral":
                    response = await self._call_mistral(messages, params)
                else:
                    raise ValueError(f"Unsupported provider: {self.provider}")
                    
                # Break if successful
                break
                
            except Exception as e:
                error = e
                logger.warning(f"LLM call attempt {attempt+1} failed: {str(e)}")
                
                if attempt < self.max_retries - 1:
                    # Wait before retrying
                    await asyncio.sleep(self.retry_delay * (2 ** attempt))
        
        # Calculate metrics
        end_time = time.time()
        latency_ms = (end_time - start_time) * 1000
        
        if response:
            # Extract completion tokens
            completion_tokens = count_tokens(response["content"], self.model)
            
            # Calculate cost
            cost = 0.0
            if provider_settings:
                # Input cost
                input_cost = (prompt_tokens / 1000) * provider_settings.cost_per_1k_tokens
                # Output cost (typically higher, use 2x as estimate)
                output_cost = (completion_tokens / 1000) * (provider_settings.cost_per_1k_tokens * 2)
                cost = input_cost + output_cost
            
            # Record metrics
            if operation:
                await self.metrics_tracker.record_llm_call(
                    provider=self.provider,
                    model=self.model,
                    agent=self.agent_name,
                    input_tokens=prompt_tokens,
                    output_tokens=completion_tokens,
                    latency_ms=latency_ms,
                    success=True,
                    cost=cost,
                    cached=False,
                    metadata={"operation": operation}
                )
            
            # Update token usage in LLM factory
            LLMFactory.update_token_count(
                provider=self.provider,
                input_tokens=prompt_tokens,
                output_tokens=completion_tokens,
                cost=cost
            )
            
            # Cache response if enabled
            if use_cache and cache_key:
                await self.cache_service.set_with_key(
                    cache_key=cache_key,
                    response=response,
                    ttl=cache_ttl
                )
                
            return response
        else:
            # Record failed call
            if operation:
                await self.metrics_tracker.record_llm_call(
                    provider=self.provider,
                    model=self.model,
                    agent=self.agent_name,
                    input_tokens=prompt_tokens,
                    output_tokens=0,
                    latency_ms=latency_ms,
                    success=False,
                    cost=0.0,
                    error_type=str(type(error).__name__) if error else "Unknown",
                    metadata={"operation": operation, "error": str(error) if error else "Unknown"}
                )
            
            # Re-raise the last error
            if error:
                raise error
            else:
                raise RuntimeError(f"LLM call failed after {self.max_retries} attempts")
    
    async def _call_openai(self, messages: List[Dict[str, str]], params: Dict[str, Any]) -> Dict[str, Any]:
        """
        Call OpenAI API.
        
        Args:
            messages: List of message dictionaries
            params: Parameters for the API call
            
        Returns:
            Response dictionary
        """
        response = await self.llm.chat.completions.create(
            model=self.model,
            messages=messages,
            temperature=params.get("temperature", 0.0),
            max_tokens=params.get("max_tokens", 2000),
            top_p=params.get("top_p", 1.0),
            frequency_penalty=params.get("frequency_penalty", 0.0),
            presence_penalty=params.get("presence_penalty", 0.0)
        )
        
        return {
            "content": response.choices[0].message.content,
            "model": self.model,
            "provider": self.provider,
            "finish_reason": response.choices[0].finish_reason
        }
    
    async def _call_anthropic(self, messages: List[Dict[str, str]], params: Dict[str, Any]) -> Dict[str, Any]:
        """
        Call Anthropic API.
        
        Args:
            messages: List of message dictionaries
            params: Parameters for the API call
            
        Returns:
            Response dictionary
        """
        # Convert messages to Anthropic format
        system = None
        prompt = ""
        
        for message in messages:
            if message["role"] == "system":
                system = message["content"]
            elif message["role"] == "user":
                prompt += message["content"]
        
        response = await self.llm.messages.create(
            model=self.model,
            messages=[{"role": "user", "content": prompt}],
            system=system,
            temperature=params.get("temperature", 0.0),
            max_tokens=params.get("max_tokens", 2000)
        )
        
        return {
            "content": response.content[0].text,
            "model": self.model,
            "provider": self.provider,
            "finish_reason": response.stop_reason
        }
    
    async def _call_cohere(self, messages: List[Dict[str, str]], params: Dict[str, Any]) -> Dict[str, Any]:
        """
        Call Cohere API.
        
        Args:
            messages: List of message dictionaries
            params: Parameters for the API call
            
        Returns:
            Response dictionary
        """
        # Convert messages to Cohere format
        system = None
        prompt = ""
        
        for message in messages:
            if message["role"] == "system":
                system = message["content"]
            elif message["role"] == "user":
                prompt += message["content"]
        
        # Cohere doesn't have async client, use sync
        response = self.llm.generate(
            prompt=prompt,
            model=self.model,
            temperature=params.get("temperature", 0.0),
            max_tokens=params.get("max_tokens", 2000),
            p=params.get("top_p", 1.0)
        )
        
        return {
            "content": response.generations[0].text,
            "model": self.model,
            "provider": self.provider,
            "finish_reason": "stop"  # Cohere doesn't provide finish reason
        }
    
    async def _call_mistral(self, messages: List[Dict[str, str]], params: Dict[str, Any]) -> Dict[str, Any]:
        """
        Call Mistral API.
        
        Args:
            messages: List of message dictionaries
            params: Parameters for the API call
            
        Returns:
            Response dictionary
        """
        response = await self.llm.chat(
            model=self.model,
            messages=messages,
            temperature=params.get("temperature", 0.0),
            max_tokens=params.get("max_tokens", 2000),
            top_p=params.get("top_p", 1.0)
        )
        
        return {
            "content": response.choices[0].message.content,
            "model": self.model,
            "provider": self.provider,
            "finish_reason": response.choices[0].finish_reason
        }
    
    def _format_prompt_for_provider(
        self, 
        base_prompt: str, 
        provider: str,
        format_type: str = "json"
    ) -> str:
        """
        Format a prompt based on the provider's preferred format.
        
        Args:
            base_prompt: The base prompt content
            provider: The provider name
            format_type: The desired output format (json, xml, etc.)
            
        Returns:
            Formatted prompt
        """
        if provider == "openai":
            # OpenAI works well with direct JSON instructions
            if format_type == "json":
                return f"{base_prompt}\n\nRespond with a valid JSON object only, no additional text."
            else:
                return base_prompt
                
        elif provider == "anthropic":
            # Anthropic works well with XML tags for structured output
            if format_type == "json":
                return f"{base_prompt}\n\n<output_format>\nJSON object\n</output_format>\n\nRespond with a valid JSON object only, no additional text."
            else:
                return base_prompt
                
        elif provider == "cohere":
            # Cohere needs explicit formatting instructions
            if format_type == "json":
                return f"{base_prompt}\n\nIMPORTANT: Your response must be a valid JSON object only, with no additional text, explanations, or markdown formatting."
            else:
                return base_prompt
                
        elif provider == "mistral":
            # Mistral works well with clear, direct instructions
            if format_type == "json":
                return f"{base_prompt}\n\nYour response must be a valid JSON object only. Do not include any explanations, markdown formatting, or additional text."
            else:
                return base_prompt
                
        else:
            # Default format
            return base_prompt
    
    def parse_llm_json_response(self, response: Dict[str, Any]) -> Dict[str, Any]:
        """
        Parse JSON from LLM response.
        
        Args:
            response: LLM response dictionary
            
        Returns:
            Parsed JSON data
            
        Raises:
            ValueError: If JSON parsing fails
        """
        try:
            # Extract JSON from response
            content = response["content"]
            
            # Find JSON block
            json_start = content.find("{")
            json_end = content.rfind("}")
            
            if json_start >= 0 and json_end >= 0:
                json_str = content[json_start:json_end+1]
                result = json.loads(json_str)
            else:
                # Fallback: try to parse the entire content
                result = json.loads(content)
                
            return result
        except Exception as e:
            logger.error(f"Error parsing JSON response: {str(e)}")
            return {
                "error": "Failed to parse response",
                "raw_response": response["content"]
            }
    
    async def process(self, input_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Process input data and return results.
        
        This method should be implemented by subclasses.
        
        Args:
            input_data: Input data for processing
            
        Returns:
            Processing results
        """
        raise NotImplementedError("Subclasses must implement process method") 