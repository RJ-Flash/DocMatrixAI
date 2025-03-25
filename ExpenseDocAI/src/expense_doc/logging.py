"""Logging configuration for ExpenseDocAI."""

import os
import logging.config
from pathlib import Path

def configure_logging(base_dir: Path) -> None:
    """
    Configure logging for the application.
    
    Args:
        base_dir: Base directory for log files
    """
    # Create logs directory if it doesn't exist
    logs_dir = base_dir / 'logs'
    logs_dir.mkdir(exist_ok=True)
    
    # Logging configuration
    config = {
        'version': 1,
        'disable_existing_loggers': False,
        'formatters': {
            'verbose': {
                'format': '{levelname} {asctime} {module} {process:d} {thread:d} {message}',
                'style': '{',
            },
            'simple': {
                'format': '{levelname} {message}',
                'style': '{',
            },
        },
        'filters': {
            'require_debug_true': {
                '()': 'django.utils.log.RequireDebugTrue',
            },
        },
        'handlers': {
            'console': {
                'level': 'INFO',
                'filters': ['require_debug_true'],
                'class': 'logging.StreamHandler',
                'formatter': 'simple',
            },
            'file': {
                'level': 'ERROR',
                'class': 'logging.FileHandler',
                'filename': str(logs_dir / 'error.log'),
                'formatter': 'verbose',
            },
            'ai_service': {
                'level': 'INFO',
                'class': 'logging.FileHandler',
                'filename': str(logs_dir / 'ai_service.log'),
                'formatter': 'verbose',
            },
            'security': {
                'level': 'INFO',
                'class': 'logging.FileHandler',
                'filename': str(logs_dir / 'security.log'),
                'formatter': 'verbose',
            },
            'audit': {
                'level': 'INFO',
                'class': 'logging.FileHandler',
                'filename': str(logs_dir / 'audit.log'),
                'formatter': 'verbose',
            },
            'mail_admins': {
                'level': 'ERROR',
                'class': 'django.utils.log.AdminEmailHandler',
                'formatter': 'verbose',
            },
        },
        'loggers': {
            'django': {
                'handlers': ['console', 'file', 'mail_admins'],
                'level': 'INFO',
                'propagate': True,
            },
            'expense_doc.ai': {
                'handlers': ['console', 'ai_service', 'mail_admins'],
                'level': 'INFO',
                'propagate': False,
            },
            'expense_doc.security': {
                'handlers': ['security', 'mail_admins'],
                'level': 'INFO',
                'propagate': False,
            },
            'expense_doc.audit': {
                'handlers': ['audit'],
                'level': 'INFO',
                'propagate': False,
            },
        },
    }
    
    # Apply configuration
    logging.config.dictConfig(config) 