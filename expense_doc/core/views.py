import os
import time
import psutil
from django.http import JsonResponse
from django.db import connections
from django.db.utils import OperationalError
from django.core.cache import cache
from django.views.decorators.cache import cache_page
from django.views.decorators.csrf import csrf_exempt
from django.conf import settings
from redis.exceptions import RedisError
import redis

@csrf_exempt
@cache_page(60)  # Cache for 1 minute
def health_check(request):
    """
    Enhanced health check endpoint that verifies:
    1. Database connectivity and performance
    2. Redis connectivity (if configured)
    3. Application status and resource usage
    4. File system status
    5. Cache status
    """
    start_time = time.time()
    health_status = {
        'status': 'healthy',
        'timestamp': time.time(),
        'components': {
            'database': {
                'status': 'healthy',
                'latency_ms': 0,
                'errors': []
            },
            'redis': {
                'status': 'not_configured',
                'latency_ms': 0,
                'errors': []
            },
            'filesystem': {
                'status': 'healthy',
                'errors': []
            },
            'cache': {
                'status': 'healthy',
                'errors': []
            }
        },
        'system': {
            'cpu_usage': 0,
            'memory_usage': 0,
            'disk_usage': 0
        }
    }

    # Check database
    try:
        db_start = time.time()
        connections['default'].ensure_connection()
        health_status['components']['database']['latency_ms'] = round((time.time() - db_start) * 1000, 2)
    except OperationalError as e:
        health_status['status'] = 'unhealthy'
        health_status['components']['database']['status'] = 'unhealthy'
        health_status['components']['database']['errors'].append(str(e))

    # Check Redis
    if settings.REDIS_URL:
        try:
            redis_start = time.time()
            redis_client = redis.from_url(settings.REDIS_URL)
            redis_client.ping()
            health_status['components']['redis']['status'] = 'healthy'
            health_status['components']['redis']['latency_ms'] = round((time.time() - redis_start) * 1000, 2)
        except RedisError as e:
            health_status['status'] = 'unhealthy'
            health_status['components']['redis']['status'] = 'unhealthy'
            health_status['components']['redis']['errors'].append(str(e))

    # Check filesystem
    required_paths = [
        settings.MEDIA_ROOT,
        settings.STATIC_ROOT,
        os.path.join(settings.BASE_DIR, 'logs'),
        os.path.join(settings.BASE_DIR, 'cache')
    ]
    
    for path in required_paths:
        try:
            if not os.path.exists(path):
                health_status['components']['filesystem']['errors'].append(f"Path not found: {path}")
            elif not os.access(path, os.W_OK):
                health_status['components']['filesystem']['errors'].append(f"Path not writable: {path}")
        except Exception as e:
            health_status['components']['filesystem']['errors'].append(f"Error checking path {path}: {str(e)}")

    if health_status['components']['filesystem']['errors']:
        health_status['status'] = 'unhealthy'
        health_status['components']['filesystem']['status'] = 'unhealthy'

    # Check cache
    try:
        cache_key = 'health_check_test'
        cache.set(cache_key, 'test', 10)
        if cache.get(cache_key) != 'test':
            raise Exception("Cache read/write test failed")
    except Exception as e:
        health_status['status'] = 'unhealthy'
        health_status['components']['cache']['status'] = 'unhealthy'
        health_status['components']['cache']['errors'].append(str(e))

    # System metrics (if available)
    try:
        health_status['system'].update({
            'cpu_usage': psutil.cpu_percent(interval=0.1),
            'memory_usage': psutil.virtual_memory().percent,
            'disk_usage': psutil.disk_usage('/').percent
        })
    except Exception as e:
        health_status['system']['error'] = str(e)

    # Calculate total response time
    health_status['response_time_ms'] = round((time.time() - start_time) * 1000, 2)

    status_code = 200 if health_status['status'] == 'healthy' else 503
    return JsonResponse(health_status, status=status_code) 