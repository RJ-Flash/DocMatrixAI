"""
LLM configuration module for ContractAI.

This module provides configuration settings for different LLM models
and manages the loading of API keys and other settings from environment
variables or configuration files.
"""

import os
import json
import logging
from typing import Dict, Any, Tuple, List, Optional
from pathlib import Path

logger = logging.getLogger(__name__)

# Default model settings
DEFAULT_LLM_SETTINGS = {
    "openai": {
        "gpt-4": {
            "temperature": 0.0,
            "max_tokens": 4000,
            "top_p": 1.0,
            "frequency_penalty": 0.0,
            "presence_penalty": 0.0,
            "timeout": 60,
            "retry_count": 3,
            "backoff_factor": 2.0
        },
        "gpt-3.5-turbo": {
            "temperature": 0.0,
            "max_tokens": 2000,
            "top_p": 1.0,
            "frequency_penalty": 0.0,
            "presence_penalty": 0.0,
            "timeout": 30,
            "retry_count": 3,
            "backoff_factor": 2.0
        }
    },
    "anthropic": {
        "claude-3-opus": {
            "temperature": 0.0,
            "max_tokens": 4000,
            "top_p": 1.0,
            "timeout": 60,
            "retry_count": 3,
            "backoff_factor": 2.0
        },
        "claude-3-sonnet": {
            "temperature": 0.0,
            "max_tokens": 4000,
            "top_p": 1.0,
            "timeout": 45,
            "retry_count": 3,
            "backoff_factor": 2.0
        },
        "claude-3-haiku": {
            "temperature": 0.0,
            "max_tokens": 2000,
            "top_p": 1.0,
            "timeout": 30,
            "retry_count": 3,
            "backoff_factor": 2.0
        }
    },
    "cohere": {
        "command": {
            "temperature": 0.0,
            "max_tokens": 2000,
            "timeout": 30,
            "retry_count": 3,
            "backoff_factor": 2.0
        }
    }
}

# Default agent LLM settings
DEFAULT_AGENT_LLM_SETTINGS = {
    "clause_detection": {
        "primary": {
            "provider": "anthropic",
            "model": "claude-3-sonnet",
            "fallbacks": [
                {"provider": "openai", "model": "gpt-4"},
                {"provider": "anthropic", "model": "claude-3-haiku"}
            ]
        }
    },
    "risk_analysis": {
        "primary": {
            "provider": "anthropic",
            "model": "claude-3-opus",
            "fallbacks": [
                {"provider": "openai", "model": "gpt-4"},
                {"provider": "anthropic", "model": "claude-3-sonnet"}
            ]
        }
    },
    "document_comparison": {
        "primary": {
            "provider": "anthropic",
            "model": "claude-3-opus",
            "fallbacks": [
                {"provider": "openai", "model": "gpt-4"}
            ]
        }
    },
    "recommendation": {
        "primary": {
            "provider": "openai",
            "model": "gpt-4",
            "fallbacks": [
                {"provider": "anthropic", "model": "claude-3-sonnet"}
            ]
        }
    }
}

def load_api_keys() -> Dict[str, str]:
    """
    Load API keys from environment variables.
    
    Returns:
        Dictionary of API keys by provider
    """
    api_keys = {}
    
    # OpenAI
    openai_api_key = os.environ.get("OPENAI_API_KEY")
    if openai_api_key:
        api_keys["openai"] = openai_api_key
    
    # Anthropic
    anthropic_api_key = os.environ.get("ANTHROPIC_API_KEY")
    if anthropic_api_key:
        api_keys["anthropic"] = anthropic_api_key
    
    # Cohere
    cohere_api_key = os.environ.get("COHERE_API_KEY")
    if cohere_api_key:
        api_keys["cohere"] = cohere_api_key
    
    # Log which providers have keys configured
    configured_providers = list(api_keys.keys())
    logger.info(f"Loaded API keys for providers: {', '.join(configured_providers)}")
    
    return api_keys

def load_custom_settings() -> Dict[str, Any]:
    """
    Load custom settings from configuration file.
    
    Returns:
        Dictionary of custom settings
    """
    config_path = Path("config/llm_settings.json")
    
    if not config_path.exists():
        logger.info("No custom LLM settings file found, using defaults")
        return {}
    
    try:
        with open(config_path, "r") as f:
            custom_settings = json.load(f)
        logger.info("Loaded custom LLM settings from config file")
        return custom_settings
    except Exception as e:
        logger.warning(f"Error loading custom LLM settings: {str(e)}")
        return {}

def merge_settings(
    default_settings: Dict[str, Any],
    custom_settings: Dict[str, Any]
) -> Dict[str, Any]:
    """
    Merge default and custom settings.
    
    Args:
        default_settings: Default settings
        custom_settings: Custom settings to override defaults
        
    Returns:
        Merged settings
    """
    merged = default_settings.copy()
    
    # Merge at provider level
    for provider, provider_settings in custom_settings.items():
        if provider not in merged:
            merged[provider] = provider_settings
            continue
            
        # Merge at model level
        for model, model_settings in provider_settings.items():
            if model not in merged[provider]:
                merged[provider][model] = model_settings
                continue
                
            # Merge model settings
            merged[provider][model].update(model_settings)
    
    return merged

def initialize_llm_settings() -> Tuple[Dict[str, Any], Dict[str, Any]]:
    """
    Initialize LLM settings by loading defaults, custom settings, and API keys.
    
    Returns:
        Tuple of (llm_settings, agent_llm_settings)
    """
    # Load custom settings
    custom_settings = load_custom_settings()
    
    # Merge with defaults
    llm_settings = merge_settings(
        DEFAULT_LLM_SETTINGS,
        custom_settings.get("llm_settings", {})
    )
    
    agent_llm_settings = merge_settings(
        DEFAULT_AGENT_LLM_SETTINGS,
        custom_settings.get("agent_llm_settings", {})
    )
    
    # Load API keys
    api_keys = load_api_keys()
    
    # Add API keys to settings
    llm_settings["api_keys"] = api_keys
    
    return llm_settings, agent_llm_settings

def get_available_providers() -> List[str]:
    """
    Get list of available LLM providers based on configured API keys.
    
    Returns:
        List of available provider names
    """
    api_keys = load_api_keys()
    return list(api_keys.keys())

def get_available_models(provider: str) -> List[str]:
    """
    Get list of available models for a provider.
    
    Args:
        provider: Provider name
        
    Returns:
        List of available model names
    """
    llm_settings, _ = initialize_llm_settings()
    
    if provider not in llm_settings:
        return []
    
    # Return all models except special keys
    return [model for model in llm_settings[provider].keys() 
            if model != "api_key"]

def get_model_settings(
    provider: str,
    model: str,
    override_settings: Optional[Dict[str, Any]] = None
) -> Dict[str, Any]:
    """
    Get settings for a specific model.
    
    Args:
        provider: Provider name
        model: Model name
        override_settings: Optional settings to override defaults
        
    Returns:
        Model settings
    """
    llm_settings, _ = initialize_llm_settings()
    
    if provider not in llm_settings or model not in llm_settings[provider]:
        logger.warning(f"Settings not found for {provider}/{model}")
        return {}
    
    # Get base settings
    settings = llm_settings[provider][model].copy()
    
    # Apply overrides
    if override_settings:
        settings.update(override_settings)
    
    return settings 