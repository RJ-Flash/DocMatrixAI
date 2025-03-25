"""Health check endpoints for system monitoring."""

import logging
from typing import Dict
import os
import requests

from django.conf import settings
from django.core.cache import cache
from django.db import connections
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from rest_framework.response import Response

logger = logging.getLogger(__name__)

@api_view(['GET'])
@permission_classes([AllowAny])
def health_check(request) -> Response:
    """
    Check the health of critical system components.
    
    Returns:
        Response with health status of each component
    """
    health_status = {
        'status': 'healthy',
        'components': {}
    }
    
    # Check database
    try:
        for name, _ in settings.DATABASES.items():
            connections[name].cursor()
            health_status['components'][f'database_{name}'] = 'healthy'
    except Exception as e:
        logger.error(f"Database health check failed: {str(e)}", exc_info=True)
        health_status['status'] = 'unhealthy'
        health_status['components']['database'] = {
            'status': 'unhealthy',
            'error': str(e)
        }
    
    # Check cache
    try:
        cache.set('health_check', 'ok', 1)
        result = cache.get('health_check')
        if result != 'ok':
            raise Exception("Cache get/set test failed")
        health_status['components']['cache'] = 'healthy'
    except Exception as e:
        logger.error(f"Cache health check failed: {str(e)}", exc_info=True)
        health_status['status'] = 'unhealthy'
        health_status['components']['cache'] = {
            'status': 'unhealthy',
            'error': str(e)
        }
    
    # Check media storage
    try:
        media_root = settings.MEDIA_ROOT
        if not media_root.exists():
            raise Exception("Media directory does not exist")
        if not os.access(media_root, os.W_OK):
            raise Exception("Media directory is not writable")
        health_status['components']['media_storage'] = 'healthy'
    except Exception as e:
        logger.error(f"Media storage health check failed: {str(e)}", exc_info=True)
        health_status['status'] = 'unhealthy'
        health_status['components']['media_storage'] = {
            'status': 'unhealthy',
            'error': str(e)
        }
    
    # Check AI service
    try:
        headers = {
            'Authorization': f'Bearer {settings.AI_SERVICE["API_KEY"]}',
            'Content-Type': 'application/json'
        }
        response = requests.get(
            f"{settings.AI_SERVICE['MODEL_ENDPOINT']}/health",
            headers=headers,
            timeout=5
        )
        if response.status_code == 200:
            health_status['components']['ai_service'] = 'healthy'
        else:
            raise Exception(f"AI service returned status {response.status_code}")
    except Exception as e:
        logger.error(f"AI service health check failed: {str(e)}", exc_info=True)
        health_status['status'] = 'unhealthy'
        health_status['components']['ai_service'] = {
            'status': 'unhealthy',
            'error': str(e)
        }
    
    # Return health status with appropriate status code
    status_code = 200 if health_status['status'] == 'healthy' else 503
    return Response(health_status, status=status_code) 