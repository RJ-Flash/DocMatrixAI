import logging
from typing import Any, List
from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.orm import Session
from app.database import get_db, Document, User, Analysis
from app.models.document import AnalysisResponse
from app.models.analysis import BatchAnalysisRequest, BatchAnalysisResponse
from app.core.security import get_current_user
from app.services.document_service import process_document
from app.core.utils import verify_document_access
from app.core.errors import DocumentNotFoundError, AnalysisNotFoundError, AccessDeniedError

router = APIRouter()
logger = logging.getLogger(__name__)


@router.get("/{document_id}", response_model=AnalysisResponse)
async def get_analysis(
    document_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
) -> Any:
    """
    Get the analysis results for a document.
    """
    # Check if document exists
    document = db.query(Document).filter(Document.id == document_id).first()
    if not document:
        raise DocumentNotFoundError(document_id)
    
    # Check access
    if not verify_document_access(current_user.id, document_id, db):
        raise AccessDeniedError()
    
    # Get analysis
    analysis = db.query(Analysis).filter(Analysis.document_id == document_id).first()
    if not analysis:
        raise AnalysisNotFoundError(document_id)
    
    # If document is still processing, return appropriate message
    if document.status == "processing":
        raise HTTPException(
            status_code=status.HTTP_202_ACCEPTED,
            detail="Document is still being processed",
        )
    
    # If document processing failed, return error
    if document.status == "error":
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=document.error_message or "Document processing failed",
        )
    
    return analysis


@router.post("/batch", response_model=BatchAnalysisResponse)
async def batch_analysis(
    batch_request: BatchAnalysisRequest,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
) -> Any:
    """
    Start batch analysis for multiple documents.
    """
    processed = 0
    failed = 0
    
    for document_id in batch_request.document_ids:
        # Check if document exists and user has access
        document = db.query(Document).filter(Document.id == document_id).first()
        if not document or not verify_document_access(current_user.id, document_id, db):
            failed += 1
            continue
        
        # Skip already processed documents
        if document.status == "processed":
            processed += 1
            continue
        
        # Update document status
        document.status = "processing"
        document.error_message = None
        db.add(document)
        
        # Delete existing analysis if any
        analysis = db.query(Analysis).filter(Analysis.document_id == document_id).first()
        if analysis:
            db.delete(analysis)
        
        try:
            # Start processing asynchronously (will be queued)
            await process_document(document_id)
            processed += 1
        except Exception as e:
            logger.error(f"Failed to start processing for document {document_id}: {e}")
            document.status = "error"
            document.error_message = str(e)
            failed += 1
    
    # Commit all changes
    db.commit()
    
    return {
        "total": len(batch_request.document_ids),
        "processed": processed,
        "failed": failed,
        "task_id": None  # In a real implementation, this would be a batch task ID
    }


@router.get("/documents/{document_id}/clauses", response_model=List[Any])
async def get_document_clauses(
    document_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
) -> Any:
    """
    Get just the clauses from a document analysis.
    """
    # Check if document exists
    document = db.query(Document).filter(Document.id == document_id).first()
    if not document:
        raise DocumentNotFoundError(document_id)
    
    # Check access
    if not verify_document_access(current_user.id, document_id, db):
        raise AccessDeniedError()
    
    # Get analysis
    analysis = db.query(Analysis).filter(Analysis.document_id == document_id).first()
    if not analysis:
        raise AnalysisNotFoundError(document_id)
    
    return analysis.clauses


@router.get("/documents/{document_id}/risks", response_model=List[Any])
async def get_document_risks(
    document_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
) -> Any:
    """
    Get just the risks from a document analysis.
    """
    # Check if document exists
    document = db.query(Document).filter(Document.id == document_id).first()
    if not document:
        raise DocumentNotFoundError(document_id)
    
    # Check access
    if not verify_document_access(current_user.id, document_id, db):
        raise AccessDeniedError()
    
    # Get analysis
    analysis = db.query(Analysis).filter(Analysis.document_id == document_id).first()
    if not analysis:
        raise AnalysisNotFoundError(document_id)
    
    return analysis.risks


@router.get("/documents/{document_id}/recommendations", response_model=List[Any])
async def get_document_recommendations(
    document_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
) -> Any:
    """
    Get just the recommendations from a document analysis.
    """
    # Check if document exists
    document = db.query(Document).filter(Document.id == document_id).first()
    if not document:
        raise DocumentNotFoundError(document_id)
    
    # Check access
    if not verify_document_access(current_user.id, document_id, db):
        raise AccessDeniedError()
    
    # Get analysis
    analysis = db.query(Analysis).filter(Analysis.document_id == document_id).first()
    if not analysis:
        raise AnalysisNotFoundError(document_id)
    
    return analysis.recommendations


@router.get("/documents/{document_id}/summary", response_model=str)
async def get_document_summary(
    document_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
) -> Any:
    """
    Get just the summary from a document analysis.
    """
    # Check if document exists
    document = db.query(Document).filter(Document.id == document_id).first()
    if not document:
        raise DocumentNotFoundError(document_id)
    
    # Check access
    if not verify_document_access(current_user.id, document_id, db):
        raise AccessDeniedError()
    
    # Get analysis
    analysis = db.query(Analysis).filter(Analysis.document_id == document_id).first()
    if not analysis:
        raise AnalysisNotFoundError(document_id)
    
    if not analysis.summary:
        return "No summary available for this document."
    
    return analysis.summary