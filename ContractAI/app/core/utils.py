import os
import random
import string
import logging
from typing import List, Dict, Any, Optional
import json
from datetime import datetime

logger = logging.getLogger(__name__)


def generate_random_string(length: int = 10) -> str:
    """
    Generate a random string of fixed length.
    
    Args:
        length: Length of the string to generate
        
    Returns:
        Random string
    """
    letters = string.ascii_lowercase + string.digits
    return ''.join(random.choice(letters) for _ in range(length))


def generate_storage_path(user_id: int, filename: str) -> str:
    """
    Generate a storage path for a document.
    
    Args:
        user_id: ID of the document owner
        filename: Original filename
        
    Returns:
        Storage path in the format: {user_id}/{timestamp}_{random_string}_{filename}
    """
    timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
    random_string = generate_random_string(6)
    _, ext = os.path.splitext(filename)
    
    # Sanitize filename
    safe_filename = "".join(c for c in filename if c.isalnum() or c in ['.', '_', '-']).lower()
    
    return f"{user_id}/{timestamp}_{random_string}_{safe_filename}"


def verify_document_access(user_id: int, document_id: int, db) -> bool:
    """
    Verify if a user has access to a document.
    
    Args:
        user_id: ID of the user
        document_id: ID of the document
        db: Database session
        
    Returns:
        True if user has access to the document, False otherwise
    """
    from app.database import Document
    
    document = db.query(Document).filter(Document.id == document_id).first()
    if not document:
        return False
    
    # Check if user is the owner
    if document.owner_id == user_id:
        return True
    
    # TODO: Add logic for shared documents if needed
    
    return False


def chunks(lst: List[Any], n: int) -> List[List[Any]]:
    """
    Split a list into chunks of size n.
    
    Args:
        lst: List to split
        n: Size of each chunk
        
    Returns:
        List of chunks
    """
    return [lst[i:i + n] for i in range(0, len(lst), n)]


def format_json_response(data: Dict[str, Any]) -> Dict[str, Any]:
    """
    Format a dictionary for JSON response, ensuring all values are serializable.
    
    Args:
        data: Dictionary to format
        
    Returns:
        Formatted dictionary
    """
    # Convert any datetime objects to ISO format
    for key, value in data.items():
        if isinstance(value, datetime):
            data[key] = value.isoformat()
    
    return data


def safe_json_loads(json_str: str, default: Optional[Any] = None) -> Any:
    """
    Safely load JSON string, returning default value on error.
    
    Args:
        json_str: JSON string to load
        default: Default value to return on error
        
    Returns:
        Parsed JSON object or default value
    """
    try:
        return json.loads(json_str)
    except (json.JSONDecodeError, TypeError) as e:
        logger.warning(f"Error parsing JSON: {e}")
        return default if default is not None else {}