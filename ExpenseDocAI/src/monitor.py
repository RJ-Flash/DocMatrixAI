#!/usr/bin/env python
"""Monitoring script for ExpenseDocAI."""

import os
import sys
import json
import logging
import smtplib
from datetime import datetime
from email.mime.text import MIMEText
from pathlib import Path
import requests
from typing import Dict, List, Optional

# Add project directory to Python path
BASE_DIR = Path(__file__).resolve().parent
sys.path.append(str(BASE_DIR))

# Load Django settings
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'expense_doc.settings')
import django
django.setup()

from django.conf import settings
from django.core.mail import send_mail

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler(BASE_DIR / 'logs/monitor.log'),
        logging.StreamHandler()
    ]
)

logger = logging.getLogger(__name__)

class SystemMonitor:
    """Monitor system health and send alerts."""
    
    def __init__(self):
        self.base_url = os.getenv('EXPENSE_DOC_URL', 'http://localhost:8000')
        self.admin_email = settings.ADMINS[0][1]
        self.alert_history_file = BASE_DIR / 'logs/alert_history.json'
        self.alert_cooldown = 3600  # 1 hour
    
    def check_health(self) -> Dict:
        """
        Check system health via health check endpoint.
        
        Returns:
            Health status data
        """
        try:
            response = requests.get(f"{self.base_url}/health/", timeout=30)
            return response.json()
        except Exception as e:
            logger.error(f"Health check failed: {str(e)}", exc_info=True)
            return {
                'status': 'unhealthy',
                'components': {
                    'health_check': {
                        'status': 'unhealthy',
                        'error': str(e)
                    }
                }
            }
    
    def check_metrics(self) -> Dict:
        """
        Check system metrics.
        
        Returns:
            Dictionary of metrics
        """
        from django.db import connection
        from django.core.cache import cache
        from expense_doc.core.models import ExpenseDocument
        
        metrics = {}
        
        # Database metrics
        try:
            with connection.cursor() as cursor:
                # Check pending documents
                cursor.execute("""
                    SELECT COUNT(*) FROM core_expensedocument 
                    WHERE status = 'PENDING'
                """)
                metrics['pending_documents'] = cursor.fetchone()[0]
                
                # Check error rate
                cursor.execute("""
                    SELECT COUNT(*) FROM core_expensedocument 
                    WHERE status = 'ERROR' 
                    AND processing_completed_at >= NOW() - INTERVAL 1 HOUR
                """)
                metrics['error_rate_1h'] = cursor.fetchone()[0]
                
                # Check processing time
                cursor.execute("""
                    SELECT AVG(TIMESTAMPDIFF(SECOND, processing_started_at, processing_completed_at))
                    FROM core_expensedocument 
                    WHERE status = 'COMPLETED'
                    AND processing_completed_at >= NOW() - INTERVAL 1 HOUR
                """)
                metrics['avg_processing_time_1h'] = cursor.fetchone()[0] or 0
        except Exception as e:
            logger.error(f"Failed to collect database metrics: {str(e)}", exc_info=True)
            metrics['database_error'] = str(e)
        
        # Cache metrics
        try:
            cache_stats = cache.get_stats()
            if cache_stats:
                metrics['cache_hits'] = cache_stats[0].get('hits', 0)
                metrics['cache_misses'] = cache_stats[0].get('misses', 0)
        except Exception as e:
            logger.error(f"Failed to collect cache metrics: {str(e)}", exc_info=True)
            metrics['cache_error'] = str(e)
        
        # Storage metrics
        try:
            media_path = settings.MEDIA_ROOT
            total, used, free = os.statvfs(media_path)
            metrics['storage_total_mb'] = (total * free) / (1024 * 1024)
            metrics['storage_used_mb'] = ((total - free) * free) / (1024 * 1024)
            metrics['storage_free_mb'] = (free * free) / (1024 * 1024)
        except Exception as e:
            logger.error(f"Failed to collect storage metrics: {str(e)}", exc_info=True)
            metrics['storage_error'] = str(e)
        
        return metrics
    
    def should_send_alert(self, component: str, error: str) -> bool:
        """
        Check if an alert should be sent based on history and cooldown.
        
        Args:
            component: The component that failed
            error: The error message
            
        Returns:
            True if alert should be sent
        """
        try:
            if self.alert_history_file.exists():
                with open(self.alert_history_file, 'r') as f:
                    history = json.load(f)
            else:
                history = {}
            
            now = datetime.now().timestamp()
            key = f"{component}:{error}"
            
            if key in history:
                last_alert = history[key]
                if now - last_alert < self.alert_cooldown:
                    return False
            
            history[key] = now
            with open(self.alert_history_file, 'w') as f:
                json.dump(history, f)
            
            return True
            
        except Exception as e:
            logger.error(f"Failed to check alert history: {str(e)}", exc_info=True)
            return True
    
    def send_alert(self, subject: str, message: str) -> None:
        """
        Send alert email.
        
        Args:
            subject: Email subject
            message: Email message
        """
        try:
            send_mail(
                subject=f"ExpenseDocAI Alert: {subject}",
                message=message,
                from_email=settings.DEFAULT_FROM_EMAIL,
                recipient_list=[self.admin_email],
                fail_silently=False
            )
            logger.info(f"Alert sent: {subject}")
        except Exception as e:
            logger.error(f"Failed to send alert: {str(e)}", exc_info=True)
    
    def run(self) -> None:
        """Run monitoring checks and send alerts if needed."""
        # Check health
        health_data = self.check_health()
        if health_data['status'] == 'unhealthy':
            for component, data in health_data['components'].items():
                if isinstance(data, dict) and data['status'] == 'unhealthy':
                    if self.should_send_alert(component, data['error']):
                        self.send_alert(
                            f"{component} Unhealthy",
                            f"Component {component} is unhealthy: {data['error']}"
                        )
        
        # Check metrics
        metrics = self.check_metrics()
        
        # Alert on high error rate
        error_rate = metrics.get('error_rate_1h', 0)
        if error_rate > 10:  # More than 10 errors per hour
            if self.should_send_alert('error_rate', f"{error_rate} errors in last hour"):
                self.send_alert(
                    "High Error Rate",
                    f"Error rate is {error_rate} in the last hour"
                )
        
        # Alert on high processing time
        avg_time = metrics.get('avg_processing_time_1h', 0)
        if avg_time > 300:  # More than 5 minutes
            if self.should_send_alert('processing_time', f"Average time {avg_time}s"):
                self.send_alert(
                    "High Processing Time",
                    f"Average processing time is {avg_time} seconds"
                )
        
        # Alert on low storage
        storage_free = metrics.get('storage_free_mb', 0)
        if storage_free < 1024:  # Less than 1GB free
            if self.should_send_alert('storage', f"Only {storage_free}MB free"):
                self.send_alert(
                    "Low Storage Space",
                    f"Only {storage_free}MB of storage space remaining"
                )
        
        # Log metrics
        logger.info(f"Metrics: {json.dumps(metrics, indent=2)}")

if __name__ == '__main__':
    monitor = SystemMonitor()
    monitor.run() 