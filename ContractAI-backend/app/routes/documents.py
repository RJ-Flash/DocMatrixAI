from fastapi import APIRouter, File, UploadFile, HTTPException, Query, Path
from pydantic import BaseModel, Field
from datetime import datetime
import uuid
import logging

from app.services import ocr_service
from app.core.errors import ValidationError, DocumentProcessingError, StorageError
from app.config import settings

# Configure logging
logger = logging.getLogger(__name__)

router = APIRouter()

# Response models
class DocumentResponse(BaseModel):
    id: str
    filename: str
    status: str
    created_at: datetime
    file_type: str = Field(..., description="MIME type of the original document")
    file_size: int = Field(..., description="Size of the original document in bytes")

class DocumentTextResponse(BaseModel):
    id: str
    text_content: str
    extracted_at: datetime

# Allowed file types
ALLOWED_FILE_TYPES = ["application/pdf", "image/jpeg", "image/png"]

@router.post("/upload", response_model=DocumentResponse)
async def upload_document(file: UploadFile = File(...)):
    """
    Upload a document for processing with OCR.
    
    The document can be a PDF or an image file.
    The text will be extracted using OCR and stored.
    
    Args:
        file: The document file to upload
        
    Returns:
        Information about the processed document
    """
    logger.info(f"Received upload request for file: {file.filename}")
    
    # Validate file type
    if file.content_type not in ALLOWED_FILE_TYPES:
        logger.warning(f"Rejected file with unsupported type: {file.content_type}")
        raise ValidationError(
            "Unsupported file type",
            details={
                "content_type": file.content_type,
                "allowed_types": ALLOWED_FILE_TYPES
            }
        )
    
    document_id = str(uuid.uuid4())
    created_at = datetime.utcnow()
    
    # Read a small part of the file to get its size
    file_start = await file.read(1024)
    file_size = len(file_start)
    
    # Reset file position
    await file.seek(0)
    
    # Continue reading to check total file size
    chunk_size = 1024 * 1024  # 1 MB
    total_read = file_size
    
    while True:
        chunk = await file.read(chunk_size)
        if not chunk:
            break
        total_read += len(chunk)
        if total_read > settings.MAX_FILE_SIZE_BYTES:
            logger.warning(f"Rejected file exceeding size limit: {total_read} bytes")
            raise ValidationError(
                f"File size exceeds the maximum allowed size of {settings.MAX_FILE_SIZE_MB} MB",
                details={
                    "file_size": total_read,
                    "max_allowed": settings.MAX_FILE_SIZE_BYTES
                }
            )
    
    # Reset file position for processing
    await file.seek(0)
    
    # Process document with OCR
    try:
        # This function will store the file and process OCR
        text_content = await ocr_service.process_document(document_id, file)
        logger.info(f"Successfully processed document {document_id}")
    except (DocumentProcessingError, StorageError) as e:
        # These are already properly formatted
        raise
    except Exception as e:
        logger.error(f"Unexpected error during document upload: {str(e)}")
        raise DocumentProcessingError(
            f"Document processing failed: {str(e)}",
            details={"document_id": document_id}
        )

    # Return the upload response
    return DocumentResponse(
        id=document_id,
        filename=file.filename,
        status="processed",
        created_at=created_at,
        file_type=file.content_type,
        file_size=total_read
    )

@router.get("/{document_id}/text", response_model=DocumentTextResponse)
async def get_document_text(document_id: str = Path(..., description="Unique document ID")):
    """
    Retrieve the extracted text for a specific document.
    
    Args:
        document_id: The ID of the document
        
    Returns:
        The extracted text content
    """
    # This would typically retrieve from database and/or MinIO
    # For now, just return a placeholder
    return DocumentTextResponse(
        id=document_id,
        text_content="Document text would be retrieved here",
        extracted_at=datetime.utcnow()
    )
