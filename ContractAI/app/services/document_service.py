import logging
from typing import Optional
from sqlalchemy.orm import Session
from app.database import Document, Analysis, get_db
from app.services.storage_service import get_document_content
from app.ai.orchestrator import AgentOrchestrator
from app.core.errors import DocumentNotFoundError, DocumentProcessingError

logger = logging.getLogger(__name__)


async def process_document(document_id: int) -> None:
    """
    Process a document using the AI agent orchestrator.
    
    Args:
        document_id: ID of the document to process
    """
    logger.info(f"Starting document processing for document {document_id}")
    
    # Get database session
    db = next(get_db())
    
    try:
        # Get document
        document = db.query(Document).filter(Document.id == document_id).first()
        if not document:
            raise DocumentNotFoundError(document_id)
        
        # Get document content
        content = await get_document_content(document.storage_path)
        
        # Initialize orchestrator
        orchestrator = AgentOrchestrator()
        
        # Process document
        results = await orchestrator.process_document(content)
        
        # Create or update analysis
        analysis = db.query(Analysis).filter(Analysis.document_id == document_id).first()
        if not analysis:
            analysis = Analysis(document_id=document_id)
        
        # Update analysis fields
        analysis.clauses = results["clauses"]
        analysis.risks = results["risks"]
        analysis.comparisons = results["comparisons"]
        analysis.recommendations = results["recommendations"]
        analysis.summary = results["summary"]
        
        # Update document status
        document.status = "processed"
        document.error_message = None
        
        # Save changes
        db.add(analysis)
        db.add(document)
        db.commit()
        
        logger.info(f"Successfully processed document {document_id}")
        
    except Exception as e:
        logger.error(f"Error processing document {document_id}: {e}")
        
        try:
            # Update document status to error
            document.status = "error"
            document.error_message = str(e)
            db.add(document)
            db.commit()
        except Exception as db_error:
            logger.error(f"Error updating document status: {db_error}")
        
        raise DocumentProcessingError(f"Failed to process document: {str(e)}")
    
    finally:
        db.close()


async def reprocess_document(document_id: int) -> None:
    """
    Reprocess a document to update its analysis.
    
    Args:
        document_id: ID of the document to reprocess
    """
    logger.info(f"Starting document reprocessing for document {document_id}")
    
    # Get database session
    db = next(get_db())
    
    try:
        # Delete existing analysis if any
        analysis = db.query(Analysis).filter(Analysis.document_id == document_id).first()
        if analysis:
            db.delete(analysis)
            db.commit()
        
        # Process document again
        await process_document(document_id)
        
        logger.info(f"Successfully reprocessed document {document_id}")
        
    except Exception as e:
        logger.error(f"Error reprocessing document {document_id}: {e}")
        raise
    
    finally:
        db.close()


async def get_document_analysis(document_id: int) -> Optional[Analysis]:
    """
    Get the analysis results for a document.
    
    Args:
        document_id: ID of the document
        
    Returns:
        Analysis object if found, None otherwise
    """
    db = next(get_db())
    
    try:
        return db.query(Analysis).filter(Analysis.document_id == document_id).first()
    
    finally:
        db.close() 