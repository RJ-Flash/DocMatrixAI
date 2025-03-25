import pytesseract
from pdf2image import convert_from_bytes
from minio import Minio
from minio.error import S3Error
import logging
import io
from PIL import Image
from typing import List, Dict, Any, Optional

from app.config import settings
from app.core.errors import DocumentProcessingError, StorageError

# Configure logging
logger = logging.getLogger(__name__)

# Initialize MinIO client
try:
    minio_client = Minio(
        settings.MINIO_ENDPOINT,
        access_key=settings.MINIO_ACCESS_KEY,
        secret_key=settings.MINIO_SECRET_KEY,
        secure=settings.MINIO_SECURE
    )

    # Ensure the bucket exists
    if not minio_client.bucket_exists(settings.MINIO_BUCKET):
        minio_client.make_bucket(settings.MINIO_BUCKET)
        logger.info(f"Created MinIO bucket: {settings.MINIO_BUCKET}")
    else:
        logger.info(f"Using existing MinIO bucket: {settings.MINIO_BUCKET}")
except S3Error as e:
    logger.error(f"Failed to initialize MinIO client: {str(e)}")
    raise StorageError(f"Storage initialization failed: {str(e)}", details={"error": str(e)})

async def process_document(document_id: str, file) -> str:
    """
    Process the uploaded document:
      1. Save the original file to MinIO.
      2. If PDF, convert to images.
      3. Run OCR on each image and combine text.
      4. Save the processed text to MinIO.
      5. Return the extracted text.
      
    Args:
        document_id: Unique identifier for the document
        file: FastAPI UploadFile object
        
    Returns:
        Extracted text from the document
        
    Raises:
        DocumentProcessingError: If OCR processing fails
        StorageError: If storing to MinIO fails
    """
    try:
        # Read file content
        file_bytes = await file.read()
        if not file_bytes:
            raise DocumentProcessingError("Empty file content")
            
        logger.info(f"Processing document {file.filename} (ID: {document_id})")

        # Check file size against configured maximum
        if len(file_bytes) > settings.MAX_FILE_SIZE_BYTES:
            logger.warning(f"File size exceeds limit: {len(file_bytes)} bytes > {settings.MAX_FILE_SIZE_BYTES} bytes")
            raise DocumentProcessingError(
                f"File size exceeds the maximum allowed size of {settings.MAX_FILE_SIZE_MB} MB",
                details={
                    "document_id": document_id,
                    "file_size": len(file_bytes),
                    "max_size": settings.MAX_FILE_SIZE_BYTES
                }
            )

        # Save original file to MinIO
        try:
            original_filename = f"{document_id}.pdf" if file.content_type == "application/pdf" else f"{document_id}.jpg"
            minio_client.put_object(
                settings.MINIO_BUCKET,
                original_filename,
                data=io.BytesIO(file_bytes),
                length=len(file_bytes),
                content_type=file.content_type
            )
            logger.info(f"Stored original file as {original_filename}")
        except S3Error as e:
            logger.error(f"Failed to store original file: {str(e)}")
            raise StorageError(f"Failed to store original document: {str(e)}", details={"document_id": document_id})

        # Process file based on type
        text_content = ""
        try:
            if file.content_type == "application/pdf":
                # Convert PDF to images
                logger.info(f"Converting PDF to images for OCR processing")
                images = convert_from_bytes(file_bytes)
                page_count = len(images)
                logger.info(f"PDF has {page_count} pages")
                
                # Check against max page limit
                if page_count > settings.MAX_PDF_PAGES:
                    logger.warning(f"PDF exceeds page limit: {page_count} > {settings.MAX_PDF_PAGES}")
                    raise DocumentProcessingError(
                        f"PDF exceeds the maximum allowed page count of {settings.MAX_PDF_PAGES}",
                        details={
                            "document_id": document_id,
                            "page_count": page_count,
                            "max_pages": settings.MAX_PDF_PAGES
                        }
                    )
                
                for i, image in enumerate(images):
                    # Use configured language
                    page_text = pytesseract.image_to_string(
                        image, 
                        lang=settings.TESSERACT_LANGUAGE
                    )
                    text_content += f"=== Page {i+1} ===\n{page_text}\n\n"
                    logger.debug(f"Processed page {i+1}/{page_count}")
            else:
                # For images directly
                logger.info(f"Processing image file directly")
                image = Image.open(io.BytesIO(file_bytes))
                # Use configured language
                text_content = pytesseract.image_to_string(
                    image,
                    lang=settings.TESSERACT_LANGUAGE
                )
                
            if not text_content.strip():
                logger.warning(f"OCR extracted empty text for document {document_id}")
        except Exception as e:
            logger.error(f"OCR processing failed: {str(e)}")
            raise DocumentProcessingError(f"OCR processing failed: {str(e)}", details={"document_id": document_id})

        # Save processed text to MinIO (as a .txt file)
        try:
            text_filename = f"{document_id}.txt"
            text_bytes = text_content.encode('utf-8')
            minio_client.put_object(
                settings.MINIO_BUCKET,
                text_filename,
                data=io.BytesIO(text_bytes),
                length=len(text_bytes),
                content_type="text/plain"
            )
            logger.info(f"Stored extracted text as {text_filename}")
        except S3Error as e:
            logger.error(f"Failed to store extracted text: {str(e)}")
            raise StorageError(f"Failed to store extracted text: {str(e)}", details={"document_id": document_id})

        logger.info(f"Successfully processed document {document_id}")
        return text_content
        
    except (DocumentProcessingError, StorageError):
        # Let these errors propagate up as they are already properly formatted
        raise
    except Exception as e:
        # Catch any other unexpected errors
        logger.error(f"Unexpected error in document processing: {str(e)}")
        raise DocumentProcessingError(
            f"Unexpected error during document processing: {str(e)}",
            details={"document_id": document_id}
        )
