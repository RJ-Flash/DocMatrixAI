"""
LLM metrics tracking for ContractAI.

This module provides functionality to track and analyze LLM usage metrics
including latency, token counts, costs, and success rates.
"""

import json
import time
import logging
import uuid
from typing import Dict, Any, List, Optional, Union
from datetime import datetime, timedelta
import aioredis

logger = logging.getLogger(__name__)

class LLMMetricsTracker:
    """
    Tracks and analyzes LLM usage metrics.
    
    This class provides methods to record and analyze metrics related to
    LLM API calls, including latency, token counts, costs, and success rates.
    """
    
    def __init__(self, redis_client: aioredis.Redis, retention_days: int = 30):
        """
        Initialize the LLM metrics tracker.
        
        Args:
            redis_client: Redis client for storing metrics
            retention_days: Number of days to retain metrics data
        """
        self.redis = redis_client
        self.retention_days = retention_days
        self.metrics_key_prefix = "llm:metrics:"
        self.daily_metrics_key = "llm:daily_metrics:"
        logger.info(f"Initialized LLM metrics tracker with {retention_days} days retention")
    
    async def record_call(
        self,
        model_name: str,
        operation: str,
        prompt_tokens: int,
        completion_tokens: int,
        latency_ms: float,
        success: bool,
        cached: bool = False,
        error_type: Optional[str] = None,
        metadata: Optional[Dict[str, Any]] = None
    ) -> str:
        """
        Record metrics for an LLM API call.
        
        Args:
            model_name: Name of the LLM model
            operation: Type of operation (e.g., 'completion', 'embedding')
            prompt_tokens: Number of tokens in the prompt
            completion_tokens: Number of tokens in the completion
            latency_ms: Latency in milliseconds
            success: Whether the call was successful
            cached: Whether the response was from cache
            error_type: Type of error if the call failed
            metadata: Additional metadata about the call
            
        Returns:
            ID of the recorded metrics entry
        """
        # Generate a unique ID for this metrics entry
        metrics_id = str(uuid.uuid4())
        
        # Get current timestamp
        timestamp = time.time()
        date_str = datetime.fromtimestamp(timestamp).strftime("%Y-%m-%d")
        
        # Calculate cost (simplified example - would need actual pricing)
        cost = self._calculate_cost(model_name, prompt_tokens, completion_tokens)
        
        # Create metrics entry
        metrics_entry = {
            "id": metrics_id,
            "timestamp": timestamp,
            "date": date_str,
            "model_name": model_name,
            "operation": operation,
            "prompt_tokens": prompt_tokens,
            "completion_tokens": completion_tokens,
            "total_tokens": prompt_tokens + completion_tokens,
            "latency_ms": latency_ms,
            "success": success,
            "cached": cached,
            "cost": cost
        }
        
        # Add error information if applicable
        if not success and error_type:
            metrics_entry["error_type"] = error_type
        
        # Add additional metadata if provided
        if metadata:
            metrics_entry["metadata"] = metadata
        
        # Store the metrics entry
        metrics_key = f"{self.metrics_key_prefix}{metrics_id}"
        daily_key = f"{self.daily_metrics_key}{date_str}"
        
        try:
            # Store detailed metrics with expiration
            expiry_seconds = self.retention_days * 86400  # days to seconds
            await self.redis.setex(
                metrics_key,
                expiry_seconds,
                json.dumps(metrics_entry)
            )
            
            # Update daily aggregated metrics
            await self._update_daily_metrics(daily_key, metrics_entry)
            
            logger.debug(f"Recorded metrics for {model_name} call with ID {metrics_id}")
            return metrics_id
            
        except Exception as e:
            logger.warning(f"Error recording metrics: {str(e)}")
            return metrics_id
    
    async def _update_daily_metrics(self, daily_key: str, metrics_entry: Dict[str, Any]) -> None:
        """
        Update daily aggregated metrics.
        
        Args:
            daily_key: Redis key for daily metrics
            metrics_entry: The metrics entry to add
        """
        try:
            # Get existing daily metrics or create new
            daily_metrics_json = await self.redis.get(daily_key)
            
            if daily_metrics_json:
                daily_metrics = json.loads(daily_metrics_json)
            else:
                daily_metrics = {
                    "date": metrics_entry["date"],
                    "total_calls": 0,
                    "successful_calls": 0,
                    "failed_calls": 0,
                    "cached_calls": 0,
                    "total_tokens": 0,
                    "prompt_tokens": 0,
                    "completion_tokens": 0,
                    "total_cost": 0.0,
                    "total_latency_ms": 0,
                    "models": {},
                    "operations": {}
                }
            
            # Update overall metrics
            daily_metrics["total_calls"] += 1
            daily_metrics["successful_calls"] += 1 if metrics_entry["success"] else 0
            daily_metrics["failed_calls"] += 0 if metrics_entry["success"] else 1
            daily_metrics["cached_calls"] += 1 if metrics_entry.get("cached", False) else 0
            daily_metrics["total_tokens"] += metrics_entry["total_tokens"]
            daily_metrics["prompt_tokens"] += metrics_entry["prompt_tokens"]
            daily_metrics["completion_tokens"] += metrics_entry["completion_tokens"]
            daily_metrics["total_cost"] += metrics_entry["cost"]
            daily_metrics["total_latency_ms"] += metrics_entry["latency_ms"]
            
            # Update model-specific metrics
            model_name = metrics_entry["model_name"]
            if model_name not in daily_metrics["models"]:
                daily_metrics["models"][model_name] = {
                    "calls": 0,
                    "successful_calls": 0,
                    "total_tokens": 0,
                    "total_cost": 0.0
                }
            
            daily_metrics["models"][model_name]["calls"] += 1
            daily_metrics["models"][model_name]["successful_calls"] += 1 if metrics_entry["success"] else 0
            daily_metrics["models"][model_name]["total_tokens"] += metrics_entry["total_tokens"]
            daily_metrics["models"][model_name]["total_cost"] += metrics_entry["cost"]
            
            # Update operation-specific metrics
            operation = metrics_entry["operation"]
            if operation not in daily_metrics["operations"]:
                daily_metrics["operations"][operation] = {
                    "calls": 0,
                    "successful_calls": 0,
                    "total_tokens": 0
                }
            
            daily_metrics["operations"][operation]["calls"] += 1
            daily_metrics["operations"][operation]["successful_calls"] += 1 if metrics_entry["success"] else 0
            daily_metrics["operations"][operation]["total_tokens"] += metrics_entry["total_tokens"]
            
            # Store updated daily metrics with expiration
            expiry_seconds = self.retention_days * 86400  # days to seconds
            await self.redis.setex(
                daily_key,
                expiry_seconds,
                json.dumps(daily_metrics)
            )
            
        except Exception as e:
            logger.warning(f"Error updating daily metrics: {str(e)}")
    
    def _calculate_cost(self, model_name: str, prompt_tokens: int, completion_tokens: int) -> float:
        """
        Calculate the cost of an LLM API call.
        
        Args:
            model_name: Name of the LLM model
            prompt_tokens: Number of tokens in the prompt
            completion_tokens: Number of tokens in the completion
            
        Returns:
            Estimated cost in USD
        """
        # Simplified pricing model - in a real implementation, this would use
        # actual pricing data for different models
        pricing = {
            "gpt-4": {"prompt": 0.03, "completion": 0.06},
            "gpt-3.5-turbo": {"prompt": 0.0015, "completion": 0.002},
            "text-embedding-ada-002": {"prompt": 0.0001, "completion": 0.0},
            "claude-3-opus": {"prompt": 0.015, "completion": 0.075},
            "claude-3-sonnet": {"prompt": 0.003, "completion": 0.015},
            "claude-3-haiku": {"prompt": 0.00025, "completion": 0.00125}
        }
        
        # Default pricing if model not found
        default_pricing = {"prompt": 0.001, "completion": 0.002}
        model_pricing = pricing.get(model_name, default_pricing)
        
        # Calculate cost per 1000 tokens
        prompt_cost = (prompt_tokens / 1000) * model_pricing["prompt"]
        completion_cost = (completion_tokens / 1000) * model_pricing["completion"]
        
        return prompt_cost + completion_cost
    
    async def get_metrics_by_id(self, metrics_id: str) -> Optional[Dict[str, Any]]:
        """
        Get metrics entry by ID.
        
        Args:
            metrics_id: ID of the metrics entry
            
        Returns:
            Metrics entry or None if not found
        """
        try:
            metrics_key = f"{self.metrics_key_prefix}{metrics_id}"
            metrics_json = await self.redis.get(metrics_key)
            
            if metrics_json:
                return json.loads(metrics_json)
            return None
            
        except Exception as e:
            logger.warning(f"Error retrieving metrics: {str(e)}")
            return None
    
    async def get_daily_metrics(self, date: Optional[str] = None) -> Optional[Dict[str, Any]]:
        """
        Get daily aggregated metrics.
        
        Args:
            date: Date string in format 'YYYY-MM-DD' (defaults to today)
            
        Returns:
            Daily metrics or None if not found
        """
        if not date:
            date = datetime.now().strftime("%Y-%m-%d")
            
        try:
            daily_key = f"{self.daily_metrics_key}{date}"
            daily_metrics_json = await self.redis.get(daily_key)
            
            if daily_metrics_json:
                return json.loads(daily_metrics_json)
            return None
            
        except Exception as e:
            logger.warning(f"Error retrieving daily metrics: {str(e)}")
            return None
    
    async def get_metrics_summary(self, days: int = 7) -> Dict[str, Any]:
        """
        Get a summary of metrics over a period of days.
        
        Args:
            days: Number of days to include in the summary
            
        Returns:
            Summary metrics
        """
        try:
            # Calculate date range
            end_date = datetime.now()
            start_date = end_date - timedelta(days=days-1)
            
            # Initialize summary
            summary = {
                "period": {
                    "start_date": start_date.strftime("%Y-%m-%d"),
                    "end_date": end_date.strftime("%Y-%m-%d"),
                    "days": days
                },
                "total_calls": 0,
                "successful_calls": 0,
                "failed_calls": 0,
                "cached_calls": 0,
                "total_tokens": 0,
                "total_cost": 0.0,
                "avg_latency_ms": 0.0,
                "success_rate": 0.0,
                "models": {},
                "operations": {},
                "daily": []
            }
            
            # Collect daily metrics
            current_date = start_date
            total_latency = 0
            
            while current_date <= end_date:
                date_str = current_date.strftime("%Y-%m-%d")
                daily_metrics = await self.get_daily_metrics(date_str)
                
                if daily_metrics:
                    # Add to summary totals
                    summary["total_calls"] += daily_metrics["total_calls"]
                    summary["successful_calls"] += daily_metrics["successful_calls"]
                    summary["failed_calls"] += daily_metrics["failed_calls"]
                    summary["cached_calls"] += daily_metrics["cached_calls"]
                    summary["total_tokens"] += daily_metrics["total_tokens"]
                    summary["total_cost"] += daily_metrics["total_cost"]
                    total_latency += daily_metrics["total_latency_ms"]
                    
                    # Update model stats
                    for model, model_stats in daily_metrics["models"].items():
                        if model not in summary["models"]:
                            summary["models"][model] = {
                                "calls": 0,
                                "successful_calls": 0,
                                "total_tokens": 0,
                                "total_cost": 0.0
                            }
                        
                        summary["models"][model]["calls"] += model_stats["calls"]
                        summary["models"][model]["successful_calls"] += model_stats["successful_calls"]
                        summary["models"][model]["total_tokens"] += model_stats["total_tokens"]
                        summary["models"][model]["total_cost"] += model_stats["total_cost"]
                    
                    # Update operation stats
                    for op, op_stats in daily_metrics["operations"].items():
                        if op not in summary["operations"]:
                            summary["operations"][op] = {
                                "calls": 0,
                                "successful_calls": 0,
                                "total_tokens": 0
                            }
                        
                        summary["operations"][op]["calls"] += op_stats["calls"]
                        summary["operations"][op]["successful_calls"] += op_stats["successful_calls"]
                        summary["operations"][op]["total_tokens"] += op_stats["total_tokens"]
                    
                    # Add to daily array
                    summary["daily"].append({
                        "date": date_str,
                        "calls": daily_metrics["total_calls"],
                        "tokens": daily_metrics["total_tokens"],
                        "cost": daily_metrics["total_cost"]
                    })
                
                current_date += timedelta(days=1)
            
            # Calculate averages and rates
            if summary["total_calls"] > 0:
                summary["avg_latency_ms"] = total_latency / summary["total_calls"]
                summary["success_rate"] = summary["successful_calls"] / summary["total_calls"]
            
            # Add success rates to models
            for model, stats in summary["models"].items():
                if stats["calls"] > 0:
                    stats["success_rate"] = stats["successful_calls"] / stats["calls"]
            
            # Add success rates to operations
            for op, stats in summary["operations"].items():
                if stats["calls"] > 0:
                    stats["success_rate"] = stats["successful_calls"] / stats["calls"]
            
            return summary
            
        except Exception as e:
            logger.warning(f"Error generating metrics summary: {str(e)}")
            return {
                "error": str(e),
                "period": {
                    "start_date": start_date.strftime("%Y-%m-%d"),
                    "end_date": end_date.strftime("%Y-%m-%d"),
                    "days": days
                }
            }
    
    async def export_metrics(self, start_date: str, end_date: str) -> List[Dict[str, Any]]:
        """
        Export detailed metrics for a date range.
        
        Args:
            start_date: Start date in format 'YYYY-MM-DD'
            end_date: End date in format 'YYYY-MM-DD'
            
        Returns:
            List of metrics entries
        """
        try:
            # Parse dates
            start = datetime.strptime(start_date, "%Y-%m-%d")
            end = datetime.strptime(end_date, "%Y-%m-%d")
            
            # Initialize results
            results = []
            
            # Scan through all metrics keys
            cursor = b'0'
            pattern = f"{self.metrics_key_prefix}*"
            
            while cursor:
                cursor, keys = await self.redis.scan(cursor=cursor, match=pattern, count=100)
                
                # Process each key
                for key in keys:
                    metrics_json = await self.redis.get(key)
                    if metrics_json:
                        metrics = json.loads(metrics_json)
                        
                        # Check if within date range
                        metrics_date = datetime.strptime(metrics["date"], "%Y-%m-%d")
                        if start <= metrics_date <= end:
                            results.append(metrics)
                
                if cursor == b'0':
                    break
            
            # Sort by timestamp
            results.sort(key=lambda x: x["timestamp"])
            return results
            
        except Exception as e:
            logger.warning(f"Error exporting metrics: {str(e)}")
            return []

    async def record_llm_call(
        self,
        provider: str,
        model: str,
        agent: str,
        input_tokens: int,
        output_tokens: int,
        latency_ms: float,
        success: bool,
        cost: float,
        cached: bool = False,
        error_type: Optional[str] = None,
        metadata: Optional[Dict[str, Any]] = None
    ) -> str:
        """
        Record metrics for an LLM call.
        
        Args:
            provider: LLM provider name
            model: Model name
            agent: Agent name
            input_tokens: Number of input tokens
            output_tokens: Number of tokens in the completion
            latency_ms: Latency in milliseconds
            success: Whether the call was successful
            cost: Estimated cost of the call
            cached: Whether the response was from cache
            error_type: Type of error if the call failed
            metadata: Additional metadata about the call
            
        Returns:
            ID of the recorded metrics entry
        """
        # Generate a unique ID for this metrics entry
        metrics_id = str(uuid.uuid4())
        
        # Get current timestamp
        timestamp = time.time()
        date_str = datetime.fromtimestamp(timestamp).strftime("%Y-%m-%d")
        
        # Create metrics entry
        metrics_entry = {
            "id": metrics_id,
            "timestamp": timestamp,
            "date": date_str,
            "provider": provider,
            "model": model,
            "agent": agent,
            "input_tokens": input_tokens,
            "output_tokens": output_tokens,
            "total_tokens": input_tokens + output_tokens,
            "latency_ms": latency_ms,
            "success": success,
            "cached": cached,
            "cost": cost
        }
        
        # Add error information if applicable
        if not success and error_type:
            metrics_entry["error_type"] = error_type
        
        # Add additional metadata if provided
        if metadata:
            metrics_entry["metadata"] = metadata
        
        # Store the metrics entry
        metrics_key = f"{self.metrics_key_prefix}{metrics_id}"
        day_key = f"llm:metrics:{date_str}"
        
        try:
            # Store detailed metrics with expiration
            expiry_seconds = self.retention_days * 86400  # days to seconds
            await self.redis.setex(
                metrics_key,
                expiry_seconds,
                json.dumps(metrics_entry)
            )
            
            # Update daily counters
            await self.redis.hincrby(f"{day_key}:counters", "total_calls", 1)
            await self.redis.hincrby(f"{day_key}:counters", "total_tokens", input_tokens + output_tokens)
            await self.redis.hincrbyfloat(f"{day_key}:counters", "total_cost", cost)
            
            # Update provider-specific counters
            await self.redis.hincrby(f"{day_key}:providers:{provider}", "calls", 1)
            await self.redis.hincrby(f"{day_key}:providers:{provider}", "input_tokens", input_tokens)
            await self.redis.hincrby(f"{day_key}:providers:{provider}", "output_tokens", output_tokens)
            await self.redis.hincrbyfloat(f"{day_key}:providers:{provider}", "cost", cost)
            
            # Update agent-specific counters
            await self.redis.hincrby(f"{day_key}:agents:{agent}", "calls", 1)
            await self.redis.hincrby(f"{day_key}:agents:{agent}", "input_tokens", input_tokens)
            await self.redis.hincrby(f"{day_key}:agents:{agent}", "output_tokens", output_tokens)
            await self.redis.hincrbyfloat(f"{day_key}:agents:{agent}", "cost", cost)
            
            # Update success/failure counters
            if success:
                await self.redis.hincrby(f"{day_key}:counters", "successful_calls", 1)
            else:
                await self.redis.hincrby(f"{day_key}:counters", "failed_calls", 1)
                if error_type:
                    await self.redis.hincrby(f"{day_key}:errors", error_type, 1)
            
            # Update cache counters
            if cached:
                await self.redis.hincrby(f"{day_key}:counters", "cached_calls", 1)
            
            logger.debug(f"Recorded LLM call metrics for {provider}/{model} with ID {metrics_id}")
            return metrics_id
            
        except Exception as e:
            logger.warning(f"Error recording LLM call metrics: {str(e)}")
            return metrics_id

    async def get_daily_llm_metrics(self, date: Optional[str] = None) -> Dict[str, Any]:
        """
        Get daily LLM metrics.
        
        Args:
            date: Date string in format 'YYYY-MM-DD' (defaults to today)
            
        Returns:
            Dictionary with daily LLM metrics
        """
        if not date:
            date = datetime.now().strftime("%Y-%m-%d")
            
        day_key = f"llm:metrics:{date}"
        
        try:
            # Get counters
            counters = await self.redis.hgetall(f"{day_key}:counters")
            
            # Convert string values to appropriate types
            for key in counters:
                if key in ["total_calls", "successful_calls", "failed_calls", "cached_calls", "total_tokens"]:
                    counters[key] = int(counters[key])
                elif key in ["total_cost"]:
                    counters[key] = float(counters[key])
            
            # Get provider metrics
            providers = {}
            provider_keys = await self.redis.keys(f"{day_key}:providers:*")
            
            for provider_key in provider_keys:
                provider_name = provider_key.split(":")[-1]
                provider_data = await self.redis.hgetall(provider_key)
                
                # Convert string values to appropriate types
                for key in provider_data:
                    if key in ["calls", "input_tokens", "output_tokens"]:
                        provider_data[key] = int(provider_data[key])
                    elif key in ["cost"]:
                        provider_data[key] = float(provider_data[key])
                
                providers[provider_name] = provider_data
            
            # Get agent metrics
            agents = {}
            agent_keys = await self.redis.keys(f"{day_key}:agents:*")
            
            for agent_key in agent_keys:
                agent_name = agent_key.split(":")[-1]
                agent_data = await self.redis.hgetall(agent_key)
                
                # Convert string values to appropriate types
                for key in agent_data:
                    if key in ["calls", "input_tokens", "output_tokens"]:
                        agent_data[key] = int(agent_data[key])
                    elif key in ["cost"]:
                        agent_data[key] = float(agent_data[key])
                
                agents[agent_name] = agent_data
            
            # Get error metrics
            errors = await self.redis.hgetall(f"{day_key}:errors")
            
            # Convert string values to integers
            for key in errors:
                errors[key] = int(errors[key])
            
            return {
                "date": date,
                "counters": counters,
                "providers": providers,
                "agents": agents,
                "errors": errors
            }
            
        except Exception as e:
            logger.warning(f"Error retrieving daily LLM metrics: {str(e)}")
            return {
                "date": date,
                "error": str(e)
            } 