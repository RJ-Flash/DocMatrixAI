import logging
from typing import Any, List
from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.orm import Session
from app.database import get_db, User, Document, Analysis
from app.models.user import UserResponse
from app.core.security import get_current_active_superuser

router = APIRouter()
logger = logging.getLogger(__name__)


@router.get("/users", response_model=List[UserResponse])
async def get_users(
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=100),
    current_user: User = Depends(get_current_active_superuser),
    db: Session = Depends(get_db),
) -> Any:
    """
    Get all users. Only accessible to superusers.
    """
    users = db.query(User).offset(skip).limit(limit).all()
    return users


@router.get("/users/{user_id}", response_model=UserResponse)
async def get_user(
    user_id: int,
    current_user: User = Depends(get_current_active_superuser),
    db: Session = Depends(get_db),
) -> Any:
    """
    Get a specific user by ID. Only accessible to superusers.
    """
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"User with ID {user_id} not found",
        )
    return user


@router.put("/users/{user_id}/activate", response_model=UserResponse)
async def activate_user(
    user_id: int,
    current_user: User = Depends(get_current_active_superuser),
    db: Session = Depends(get_db),
) -> Any:
    """
    Activate a user. Only accessible to superusers.
    """
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"User with ID {user_id} not found",
        )
    
    user.is_active = True
    db.add(user)
    db.commit()
    db.refresh(user)
    
    return user


@router.put("/users/{user_id}/deactivate", response_model=UserResponse)
async def deactivate_user(
    user_id: int,
    current_user: User = Depends(get_current_active_superuser),
    db: Session = Depends(get_db),
) -> Any:
    """
    Deactivate a user. Only accessible to superusers.
    """
    # Prevent deactivation of own account
    if user_id == current_user.id:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Cannot deactivate your own account",
        )
    
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"User with ID {user_id} not found",
        )
    
    user.is_active = False
    db.add(user)
    db.commit()
    db.refresh(user)
    
    return user


@router.get("/stats/documents", response_model=dict)
async def get_document_stats(
    current_user: User = Depends(get_current_active_superuser),
    db: Session = Depends(get_db),
) -> Any:
    """
    Get statistics about documents. Only accessible to superusers.
    """
    total = db.query(Document).count()
    
    # Count by status
    by_status = {}
    statuses = ["uploaded", "processing", "processed", "error"]
    for status in statuses:
        count = db.query(Document).filter(Document.status == status).count()
        by_status[status] = count
    
    # Recent documents (last 7 days)
    import datetime
    seven_days_ago = datetime.datetime.now() - datetime.timedelta(days=7)
    recent = db.query(Document).filter(Document.created_at >= seven_days_ago).count()
    
    return {
        "total": total,
        "by_status": by_status,
        "recent": recent,
    }


@router.get("/stats/users", response_model=dict)
async def get_user_stats(
    current_user: User = Depends(get_current_active_superuser),
    db: Session = Depends(get_db),
) -> Any:
    """
    Get statistics about users. Only accessible to superusers.
    """
    total = db.query(User).count()
    active = db.query(User).filter(User.is_active == True).count()
    inactive = db.query(User).filter(User.is_active == False).count()
    superusers = db.query(User).filter(User.is_superuser == True).count()
    
    # Recent users (last 30 days)
    import datetime
    thirty_days_ago = datetime.datetime.now() - datetime.timedelta(days=30)
    recent = db.query(User).filter(User.created_at >= thirty_days_ago).count()
    
    # Users by document count
    from sqlalchemy import func
    
    user_doc_counts = db.query(
        Document.owner_id, 
        func.count(Document.id).label("doc_count")
    ).group_by(Document.owner_id).all()
    
    # Categorize users by document count
    users_by_doc_count = {
        "0": db.query(User).filter(~User.id.in_([u[0] for u in user_doc_counts])).count(),
        "1-5": 0,
        "6-20": 0,
        "21-100": 0,
        "100+": 0,
    }
    
    for owner_id, count in user_doc_counts:
        if count <= 5:
            users_by_doc_count["1-5"] += 1
        elif count <= 20:
            users_by_doc_count["6-20"] += 1
        elif count <= 100:
            users_by_doc_count["21-100"] += 1
        else:
            users_by_doc_count["100+"] += 1
    
    return {
        "total": total,
        "active": active,
        "inactive": inactive,
        "superusers": superusers,
        "recent": recent,
        "by_document_count": users_by_doc_count,
    }


@router.post("/documents/{document_id}/reset", response_model=dict)
async def reset_document_processing(
    document_id: int,
    current_user: User = Depends(get_current_active_superuser),
    db: Session = Depends(get_db),
) -> Any:
    """
    Reset a document's processing status and remove analysis. Only accessible to superusers.
    """
    # Get document
    document = db.query(Document).filter(Document.id == document_id).first()
    if not document:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Document with ID {document_id} not found",
        )
    
    # Reset status
    document.status = "uploaded"
    document.error_message = None
    db.add(document)
    
    # Remove analysis if exists
    analysis = db.query(Analysis).filter(Analysis.document_id == document_id).first()
    if analysis:
        db.delete(analysis)
    
    db.commit()
    
    return {"message": f"Document {document_id} has been reset"}