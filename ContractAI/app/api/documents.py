import logging
from typing import Any, List, Optional
from fastapi import APIRouter, Depends, File, Form, HTTPException, Query, UploadFile, status
from sqlalchemy.orm import Session
from app.database import get_db, Document, User, Analysis
from app.models.document import (
    DocumentCreate,
    DocumentUpdate,
    DocumentResponse,
    DocumentDetailResponse,
    DocumentListResponse,
)
from app.core.security import get_current_user
from app.services.document_service import process_document
from app.services.storage_service import store_document_file, get_document_content
from app.core.utils import generate_storage_path, verify_document_access
from app.core.errors import DocumentNotFoundError, AccessDeniedError
from app.config import get_settings

settings = get_settings()
router = APIRouter()
logger = logging.getLogger(__name__)


@router.post("/", response_model=DocumentResponse, status_code=status.HTTP_201_CREATED)
async def create_document(
    name: str = Form(...),
    file: UploadFile = File(...),
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
) -> Any:
    """
    Upload a new document for analysis.
    """
    # Validate file size
    if file.size > settings.MAX_DOCUMENT_SIZE:
        raise HTTPException(
            status_code=status.HTTP_413_REQUEST_ENTITY_TOO_LARGE,
            detail=f"File too large. Maximum size is {settings.MAX_DOCUMENT_SIZE // (1024 * 1024)}MB",
        )
    
    # Validate file type
    if file.content_type not in settings.ALLOWED_DOCUMENT_TYPES:
        raise HTTPException(
            status_code=status.HTTP_415_UNSUPPORTED_MEDIA_TYPE,
            detail=f"Unsupported file type: {file.content_type}. Allowed types: {settings.ALLOWED_DOCUMENT_TYPES}",
        )
    
    # Validate file name
    if not name:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Document name is required",
        )
    
    # Generate storage path
    storage_path = generate_storage_path(current_user.id, file.filename)
    
    # Create document in database
    db_document = Document(
        name=name,
        content_type=file.content_type,
        storage_path=storage_path,
        status="uploaded",
        owner_id=current_user.id,
    )
    db.add(db_document)
    db.commit()
    db.refresh(db_document)
    
    # Store file
    try:
        await store_document_file(file, storage_path)
    except Exception as e:
        # Update document status to error
        db_document.status = "error"
        db_document.error_message = str(e)
        db.add(db_document)
        db.commit()
        
        logger.error(f"Failed to store document: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to store document",
        )
    
    # Start processing asynchronously
    try:
        # Update document status to processing
        db_document.status = "processing"
        db.add(db_document)
        db.commit()
        
        # Process document asynchronously
        await process_document(db_document.id)
    except Exception as e:
        logger.error(f"Failed to start document processing: {e}")
        # Don't fail the request, processing will be retried
    
    return db_document


@router.get("/", response_model=DocumentListResponse)
async def list_documents(
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=100),
    status: Optional[str] = Query(None),
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
) -> Any:
    """
    List documents belonging to the current user.
    """
    # Validate pagination parameters
    if skip < 0 or limit < 1 or limit > 100:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid pagination parameters",
        )
    
    # Base query
    query = db.query(Document).filter(Document.owner_id == current_user.id)
    
    # Apply status filter if provided
    if status:
        query = query.filter(Document.status == status)
    
    # Get total count
    total = query.count()
    
    # Apply pagination
    documents = query.order_by(Document.created_at.desc()).offset(skip).limit(limit).all()
    
    return {
        "total": total,
        "documents": documents,
    }


@router.get("/{document_id}", response_model=DocumentDetailResponse)
async def get_document(
    document_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
) -> Any:
    """
    Get a specific document by ID.
    """
    # Validate document ID
    if document_id <= 0:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid document ID",
        )
    
    # Get document
    document = db.query(Document).filter(Document.id == document_id).first()
    if not document:
        raise DocumentNotFoundError(document_id)
    
    # Check access
    if not verify_document_access(current_user.id, document_id, db):
        raise AccessDeniedError()
    
    # Get analysis if available
    analysis = db.query(Analysis).filter(Analysis.document_id == document_id).first()
    
    # Create response with analysis included
    response = DocumentDetailResponse.model_validate(document)
    if analysis:
        response.analysis = {
            "clauses": analysis.clauses,
            "risks": analysis.risks,
            "comparisons": analysis.comparisons,
            "recommendations": analysis.recommendations,
            "summary": analysis.summary,
        }
    
    return response


@router.put("/{document_id}", response_model=DocumentResponse)
async def update_document(
    document_id: int,
    document_update: DocumentUpdate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
) -> Any:
    """
    Update a specific document.
    """
    # Validate document ID
    if document_id <= 0:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid document ID",
        )
    
    # Get document
    document = db.query(Document).filter(Document.id == document_id).first()
    if not document:
        raise DocumentNotFoundError(document_id)
    
    # Check access
    if not verify_document_access(current_user.id, document_id, db):
        raise AccessDeniedError()
    
    # Update document
    if document_update.name is not None:
        document.name = document_update.name
    if document_update.status is not None:
        # Only superusers can update status
        if not current_user.is_superuser:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Only superusers can update document status",
            )
        document.status = document_update.status
    
    db.add(document)
    db.commit()
    db.refresh(document)
    
    return document


@router.delete("/{document_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_document(
    document_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
) -> Any:
    """
    Delete a document.
    """
    # Validate document ID
    if document_id <= 0:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid document ID",
        )
    
    # Get document
    document = db.query(Document).filter(Document.id == document_id).first()
    if not document:
        raise DocumentNotFoundError(document_id)
    
    # Check access
    if not verify_document_access(current_user.id, document_id, db):
        raise AccessDeniedError()
    
    # Delete analysis if exists
    analysis = db.query(Analysis).filter(Analysis.document_id == document_id).first()
    if analysis:
        db.delete(analysis)
    
    # Delete document
    db.delete(document)
    db.commit()
    
    # Note: In a production system, we would also remove the file from storage
    # This is omitted here for simplicity
    
    return None


@router.get("/{document_id}/content", response_model=str)
async def get_document_content_endpoint(
    document_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
) -> Any:
    """
    Get the raw text content of a document.
    """
    # Validate document ID
    if document_id <= 0:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid document ID",
        )
    
    # Get document
    document = db.query(Document).filter(Document.id == document_id).first()
    if not document:
        raise DocumentNotFoundError(document_id)
    
    # Check access
    if not verify_document_access(current_user.id, document_id, db):
        raise AccessDeniedError()
    
    # Get document content
    try:
        content = await get_document_content(document.storage_path)
        return content
    except Exception as e:
        logger.error(f"Failed to get document content: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to retrieve document content",
        )


@router.post("/{document_id}/reprocess", response_model=DocumentResponse)
async def reprocess_document(
    document_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
) -> Any:
    """
    Reprocess a document to regenerate analysis.
    """
    # Validate document ID
    if document_id <= 0:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid document ID",
        )
    
    # Get document
    document = db.query(Document).filter(Document.id == document_id).first()
    if not document:
        raise DocumentNotFoundError(document_id)
    
    # Check access
    if not verify_document_access(current_user.id, document_id, db):
        raise AccessDeniedError()
    
    # Update document status
    document.status = "processing"
    document.error_message = None
    db.add(document)
    db.commit()
    db.refresh(document)
    
    # Delete existing analysis if any
    analysis = db.query(Analysis).filter(Analysis.document_id == document_id).first()
    if analysis:
        db.delete(analysis)
        db.commit()
    
    # Start processing asynchronously
    try:
        await process_document(document.id)
    except Exception as e:
        logger.error(f"Failed to start document processing: {e}")
        # Don't fail the request, processing will be retried
    
    return document