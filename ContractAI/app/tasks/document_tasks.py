"""
Document processing tasks for ContractAI.

This module contains Celery tasks for document processing,
including text extraction, analysis, and cleanup.
"""

import logging
from datetime import datetime, timedelta
from sqlalchemy.orm import Session
from app.worker import celery
from app.database import SessionLocal, Document
from app.services.document_service import process_document
from app.config import get_settings

settings = get_settings()
logger = logging.getLogger(__name__)


@celery.task(name="process_document")
def process_document_task(document_id: int):
    """
    Process a document asynchronously.
    
    Args:
        document_id: The ID of the document to process
    """
    logger.info(f"Processing document {document_id}")
    db = SessionLocal()
    
    try:
        # Get the document
        document = db.query(Document).filter(Document.id == document_id).first()
        
        if not document:
            logger.error(f"Document {document_id} not found")
            return {"status": "error", "message": "Document not found"}
        
        # Update document status
        document.status = "processing"
        db.commit()
        
        # Process the document
        result = process_document(document, db)
        
        # Update document status
        document.status = "processed"
        db.commit()
        
        return {"status": "success", "result": result}
    
    except Exception as e:
        logger.exception(f"Error processing document {document_id}: {str(e)}")
        
        # Update document status to error
        if document:
            document.status = "error"
            document.error_message = str(e)
            db.commit()
        
        return {"status": "error", "message": str(e)}
    
    finally:
        db.close()


@celery.task(name="cleanup_expired_documents")
def cleanup_expired_documents(days: int = 30):
    """
    Clean up documents that have been processed more than X days ago.
    
    Args:
        days: Number of days after which documents are considered expired
    """
    logger.info(f"Cleaning up documents older than {days} days")
    db = SessionLocal()
    
    try:
        # Calculate the cutoff date
        cutoff_date = datetime.utcnow() - timedelta(days=days)
        
        # Find expired documents
        expired_documents = (
            db.query(Document)
            .filter(Document.created_at < cutoff_date)
            .filter(Document.status == "processed")
            .all()
        )
        
        logger.info(f"Found {len(expired_documents)} expired documents")
        
        # Process each expired document
        for document in expired_documents:
            try:
                # TODO: Implement document cleanup logic
                # This could include removing files from storage, etc.
                logger.info(f"Cleaning up document {document.id}")
            except Exception as e:
                logger.error(f"Error cleaning up document {document.id}: {str(e)}")
        
        return {"status": "success", "count": len(expired_documents)}
    
    except Exception as e:
        logger.exception(f"Error cleaning up expired documents: {str(e)}")
        return {"status": "error", "message": str(e)}
    
    finally:
        db.close() 