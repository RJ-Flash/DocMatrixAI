"""
Notification tasks for ContractAI.

This module contains Celery tasks for sending notifications,
including email notifications, webhook calls, etc.
"""

import logging
import smtplib
import requests
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from app.worker import celery
from app.database import SessionLocal, User
from app.config import get_settings

settings = get_settings()
logger = logging.getLogger(__name__)


@celery.task(name="send_email_notification")
def send_email_notification(user_id: int, subject: str, message: str, html_message: str = None):
    """
    Send an email notification to a user.
    
    Args:
        user_id: The ID of the user to notify
        subject: The email subject
        message: The plain text message
        html_message: The HTML message (optional)
    """
    logger.info(f"Sending email notification to user {user_id}")
    db = SessionLocal()
    
    try:
        # Get the user
        user = db.query(User).filter(User.id == user_id).first()
        
        if not user:
            logger.error(f"User {user_id} not found")
            return {"status": "error", "message": "User not found"}
        
        # Create the email message
        msg = MIMEMultipart("alternative")
        msg["Subject"] = subject
        msg["From"] = "noreply@contractai.example.com"  # TODO: Configure from settings
        msg["To"] = user.email
        
        # Attach plain text and HTML parts
        msg.attach(MIMEText(message, "plain"))
        if html_message:
            msg.attach(MIMEText(html_message, "html"))
        
        # TODO: Configure email sending
        # This is a placeholder for actual email sending logic
        logger.info(f"Would send email to {user.email}: {subject}")
        
        # Uncomment to actually send emails when SMTP is configured
        """
        with smtplib.SMTP("smtp.example.com", 587) as server:
            server.starttls()
            server.login("username", "password")
            server.send_message(msg)
        """
        
        return {"status": "success", "recipient": user.email}
    
    except Exception as e:
        logger.exception(f"Error sending email notification to user {user_id}: {str(e)}")
        return {"status": "error", "message": str(e)}
    
    finally:
        db.close()


@celery.task(name="send_webhook_notification")
def send_webhook_notification(webhook_url: str, payload: dict):
    """
    Send a webhook notification.
    
    Args:
        webhook_url: The URL to send the webhook to
        payload: The JSON payload to send
    """
    logger.info(f"Sending webhook notification to {webhook_url}")
    
    try:
        # Send the webhook
        response = requests.post(webhook_url, json=payload, timeout=10)
        response.raise_for_status()
        
        return {
            "status": "success",
            "response_code": response.status_code,
            "response_text": response.text
        }
    
    except requests.exceptions.RequestException as e:
        logger.exception(f"Error sending webhook notification: {str(e)}")
        return {"status": "error", "message": str(e)} 