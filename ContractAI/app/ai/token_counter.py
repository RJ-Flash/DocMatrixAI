"""
Token counting utilities for LLM text.

This module provides functions for counting tokens in text for different LLM models.
"""

import logging
import tiktoken
from typing import Dict, Any, Optional, Union, List

logger = logging.getLogger(__name__)

# Default tokenizer cache
_TOKENIZERS = {}

def get_tokenizer(model_name: str) -> Any:
    """
    Get a tokenizer for the specified model.
    
    Args:
        model_name: Name of the model
        
    Returns:
        Tokenizer instance
    """
    if model_name in _TOKENIZERS:
        return _TOKENIZERS[model_name]
    
    try:
        # For OpenAI models
        if model_name.startswith("gpt-"):
            encoding = tiktoken.encoding_for_model(model_name)
        else:
            # Default to cl100k_base for non-OpenAI models
            encoding = tiktoken.get_encoding("cl100k_base")
            
        _TOKENIZERS[model_name] = encoding
        return encoding
    except Exception as e:
        logger.warning(f"Error creating tokenizer for {model_name}: {str(e)}")
        # Fall back to cl100k_base
        encoding = tiktoken.get_encoding("cl100k_base")
        _TOKENIZERS[model_name] = encoding
        return encoding

def count_tokens(text: str, model_name: str = "gpt-3.5-turbo") -> int:
    """
    Count the number of tokens in a text string.
    
    Args:
        text: Text to count tokens for
        model_name: Name of the model to use for counting
        
    Returns:
        Number of tokens
    """
    if not text:
        return 0
        
    try:
        tokenizer = get_tokenizer(model_name)
        tokens = tokenizer.encode(text)
        return len(tokens)
    except Exception as e:
        logger.warning(f"Error counting tokens: {str(e)}")
        # Fallback to approximate count (1 token ≈ 4 characters)
        return len(text) // 4

def count_messages_tokens(messages: List[Dict[str, str]], model_name: str = "gpt-3.5-turbo") -> int:
    """
    Count the number of tokens in a list of chat messages.
    
    Args:
        messages: List of message dictionaries with 'role' and 'content' keys
        model_name: Name of the model to use for counting
        
    Returns:
        Number of tokens
    """
    if not messages:
        return 0
        
    try:
        # Count tokens in each message
        token_count = 0
        tokenizer = get_tokenizer(model_name)
        
        # Add tokens for each message
        for message in messages:
            # Add message role tokens
            role = message.get("role", "user")
            content = message.get("content", "")
            
            # Count role tokens
            role_tokens = len(tokenizer.encode(role))
            
            # Count content tokens
            content_tokens = len(tokenizer.encode(content))
            
            # Add tokens for this message
            # Format: <im_start>{role}\n{content}<im_end>
            token_count += role_tokens + content_tokens + 4
        
        # Add tokens for the overall format
        token_count += 2  # <|start_of_message|> and <|end_of_message|>
        
        return token_count
    except Exception as e:
        logger.warning(f"Error counting message tokens: {str(e)}")
        # Fallback to approximate count
        total_text = ""
        for message in messages:
            total_text += message.get("content", "")
        return len(total_text) // 4

def estimate_completion_tokens(prompt_tokens: int, model_name: str = "gpt-3.5-turbo") -> int:
    """
    Estimate the number of completion tokens based on prompt tokens.
    
    Args:
        prompt_tokens: Number of tokens in the prompt
        model_name: Name of the model
        
    Returns:
        Estimated number of completion tokens
    """
    # Simple heuristic based on model
    if "gpt-4" in model_name:
        # GPT-4 tends to be more verbose
        return min(prompt_tokens * 2, 4000)
    elif "gpt-3.5" in model_name:
        return min(prompt_tokens * 1.5, 2000)
    elif "claude" in model_name:
        if "opus" in model_name:
            return min(prompt_tokens * 2, 4000)
        elif "sonnet" in model_name:
            return min(prompt_tokens * 1.8, 4000)
        else:  # haiku
            return min(prompt_tokens * 1.5, 2000)
    else:
        # Default estimate
        return min(prompt_tokens * 1.5, 2000) 