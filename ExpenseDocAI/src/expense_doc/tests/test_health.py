"""Tests for health check endpoint."""

from unittest.mock import patch, MagicMock
import pytest
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient

@pytest.fixture
def api_client():
    return APIClient()

@pytest.mark.django_db
class TestHealthCheck:
    """Test health check endpoint."""
    
    def test_health_check_success(self, api_client):
        """Test successful health check."""
        # Mock external service calls
        with patch('requests.get') as mock_get:
            mock_get.return_value = MagicMock(status_code=200)
            
            # Call health check endpoint
            url = reverse('health_check')
            response = api_client.get(url)
            
            # Check response
            assert response.status_code == status.HTTP_200_OK
            assert response.data['status'] == 'healthy'
            assert 'components' in response.data
            
            # Check components
            components = response.data['components']
            assert components['database_default'] == 'healthy'
            assert components['cache'] == 'healthy'
            assert components['media_storage'] == 'healthy'
            assert components['ai_service'] == 'healthy'
    
    def test_health_check_database_failure(self, api_client):
        """Test health check with database failure."""
        # Mock database error
        with patch('django.db.backends.base.base.BaseDatabaseWrapper.cursor') as mock_cursor, \
             patch('requests.get') as mock_get:
            mock_cursor.side_effect = Exception("Database connection failed")
            mock_get.return_value = MagicMock(status_code=200)
            
            # Call health check endpoint
            url = reverse('health_check')
            response = api_client.get(url)
            
            # Check response
            assert response.status_code == status.HTTP_503_SERVICE_UNAVAILABLE
            assert response.data['status'] == 'unhealthy'
            assert 'database' in response.data['components']
            assert response.data['components']['database']['status'] == 'unhealthy'
            assert 'error' in response.data['components']['database']
    
    def test_health_check_cache_failure(self, api_client):
        """Test health check with cache failure."""
        # Mock cache error
        with patch('django.core.cache.cache.set') as mock_set, \
             patch('requests.get') as mock_get:
            mock_set.side_effect = Exception("Cache connection failed")
            mock_get.return_value = MagicMock(status_code=200)
            
            # Call health check endpoint
            url = reverse('health_check')
            response = api_client.get(url)
            
            # Check response
            assert response.status_code == status.HTTP_503_SERVICE_UNAVAILABLE
            assert response.data['status'] == 'unhealthy'
            assert 'cache' in response.data['components']
            assert response.data['components']['cache']['status'] == 'unhealthy'
            assert 'error' in response.data['components']['cache']
    
    def test_health_check_ai_service_failure(self, api_client):
        """Test health check with AI service failure."""
        # Mock AI service error
        with patch('requests.get') as mock_get:
            mock_get.return_value = MagicMock(status_code=500)
            
            # Call health check endpoint
            url = reverse('health_check')
            response = api_client.get(url)
            
            # Check response
            assert response.status_code == status.HTTP_503_SERVICE_UNAVAILABLE
            assert response.data['status'] == 'unhealthy'
            assert 'ai_service' in response.data['components']
            assert response.data['components']['ai_service']['status'] == 'unhealthy'
            assert 'error' in response.data['components']['ai_service']
    
    def test_health_check_media_storage_failure(self, api_client):
        """Test health check with media storage failure."""
        # Mock media storage error
        with patch('pathlib.Path.exists') as mock_exists, \
             patch('requests.get') as mock_get:
            mock_exists.return_value = False
            mock_get.return_value = MagicMock(status_code=200)
            
            # Call health check endpoint
            url = reverse('health_check')
            response = api_client.get(url)
            
            # Check response
            assert response.status_code == status.HTTP_503_SERVICE_UNAVAILABLE
            assert response.data['status'] == 'unhealthy'
            assert 'media_storage' in response.data['components']
            assert response.data['components']['media_storage']['status'] == 'unhealthy'
            assert 'error' in response.data['components']['media_storage'] 