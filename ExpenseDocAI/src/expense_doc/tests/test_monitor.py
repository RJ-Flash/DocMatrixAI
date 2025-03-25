"""Tests for system monitoring."""

import json
from pathlib import Path
from unittest.mock import patch, MagicMock
import pytest
from django.conf import settings
from django.core import mail

from monitor import SystemMonitor

@pytest.fixture
def monitor():
    """Create a SystemMonitor instance."""
    return SystemMonitor()

@pytest.fixture
def mock_health_response():
    """Create a mock health check response."""
    return {
        'status': 'healthy',
        'components': {
            'database_default': 'healthy',
            'cache': 'healthy',
            'media_storage': 'healthy',
            'ai_service': 'healthy'
        }
    }

@pytest.fixture
def mock_metrics():
    """Create mock system metrics."""
    return {
        'pending_documents': 5,
        'error_rate_1h': 2,
        'avg_processing_time_1h': 120,
        'cache_hits': 1000,
        'cache_misses': 100,
        'storage_total_mb': 10240,
        'storage_used_mb': 5120,
        'storage_free_mb': 5120
    }

def test_check_health_success(monitor, mock_health_response):
    """Test successful health check."""
    with patch('requests.get') as mock_get:
        mock_get.return_value.json.return_value = mock_health_response
        health_data = monitor.check_health()
        
        assert health_data['status'] == 'healthy'
        assert all(v == 'healthy' for v in health_data['components'].values())

def test_check_health_failure(monitor):
    """Test health check failure."""
    with patch('requests.get') as mock_get:
        mock_get.side_effect = Exception("Connection failed")
        health_data = monitor.check_health()
        
        assert health_data['status'] == 'unhealthy'
        assert 'health_check' in health_data['components']
        assert health_data['components']['health_check']['status'] == 'unhealthy'

def test_check_metrics_success(monitor, mock_metrics):
    """Test successful metrics collection."""
    with patch('django.db.connection.cursor') as mock_cursor, \
         patch('django.core.cache.cache.get_stats') as mock_cache_stats, \
         patch('os.statvfs') as mock_statvfs:
        
        # Mock database queries
        mock_cursor.return_value.__enter__.return_value.fetchone.side_effect = [
            (mock_metrics['pending_documents'],),
            (mock_metrics['error_rate_1h'],),
            (mock_metrics['avg_processing_time_1h'],)
        ]
        
        # Mock cache stats
        mock_cache_stats.return_value = [{
            'hits': mock_metrics['cache_hits'],
            'misses': mock_metrics['cache_misses']
        }]
        
        # Mock storage stats
        mock_statvfs.return_value = (1024, 1024, 5120)  # total, used, free
        
        metrics = monitor.check_metrics()
        
        assert metrics['pending_documents'] == mock_metrics['pending_documents']
        assert metrics['error_rate_1h'] == mock_metrics['error_rate_1h']
        assert metrics['avg_processing_time_1h'] == mock_metrics['avg_processing_time_1h']
        assert metrics['cache_hits'] == mock_metrics['cache_hits']
        assert metrics['cache_misses'] == mock_metrics['cache_misses']
        assert 'storage_free_mb' in metrics

def test_should_send_alert_cooldown(monitor, tmp_path):
    """Test alert cooldown functionality."""
    # Mock alert history file
    monitor.alert_history_file = tmp_path / 'alert_history.json'
    
    # First alert should be sent
    assert monitor.should_send_alert('test', 'error1') is True
    
    # Second alert for same error within cooldown should not be sent
    assert monitor.should_send_alert('test', 'error1') is False
    
    # Different error should be sent
    assert monitor.should_send_alert('test', 'error2') is True

def test_send_alert(monitor):
    """Test alert sending."""
    subject = "Test Alert"
    message = "Test message"
    
    monitor.send_alert(subject, message)
    
    assert len(mail.outbox) == 1
    assert mail.outbox[0].subject == f"ExpenseDocAI Alert: {subject}"
    assert mail.outbox[0].body == message
    assert mail.outbox[0].to == [monitor.admin_email]

@pytest.mark.django_db
def test_run_with_unhealthy_system(monitor):
    """Test monitoring run with unhealthy system."""
    unhealthy_response = {
        'status': 'unhealthy',
        'components': {
            'database': {
                'status': 'unhealthy',
                'error': 'Connection failed'
            }
        }
    }
    
    high_error_metrics = {
        'error_rate_1h': 15,
        'avg_processing_time_1h': 400,
        'storage_free_mb': 512
    }
    
    with patch('requests.get') as mock_get, \
         patch.object(monitor, 'check_metrics') as mock_check_metrics, \
         patch.object(monitor, 'should_send_alert', return_value=True):
        
        mock_get.return_value.json.return_value = unhealthy_response
        mock_check_metrics.return_value = high_error_metrics
        
        monitor.run()
        
        # Should send alerts for:
        # 1. Unhealthy database
        # 2. High error rate
        # 3. High processing time
        # 4. Low storage
        assert len(mail.outbox) == 4 