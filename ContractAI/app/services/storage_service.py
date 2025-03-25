import logging
from typing import BinaryIO, Optional, List
from minio import Minio
from minio.error import S3Error, InvalidResponseError, MinioException
from fastapi import UploadFile
import io
import tempfile
import os
import time
from functools import wraps

from app.config import get_settings
from app.core.errors import StorageError, DocumentNotFoundError, BucketNotFoundError, StorageAuthError, StorageTimeoutError

settings = get_settings()
logger = logging.getLogger(__name__)

# Maximum retry attempts for transient storage failures
MAX_RETRY_ATTEMPTS = 3
# Delay between retry attempts (in seconds)
RETRY_DELAY = 1.5


def with_retry(func):
    """
    Decorator to retry storage operations on transient failures.
    
    Args:
        func: Function to decorate
        
    Returns:
        Decorated function
    """
    @wraps(func)
    async def wrapper(*args, **kwargs):
        last_exception = None
        
        for attempt in range(1, MAX_RETRY_ATTEMPTS + 1):
            try:
                return await func(*args, **kwargs)
            except (ConnectionError, TimeoutError, InvalidResponseError) as e:
                last_exception = e
                if attempt < MAX_RETRY_ATTEMPTS:
                    wait_time = RETRY_DELAY * attempt
                    logger.warning(
                        f"Transient storage error: {str(e)}. "
                        f"Retrying in {wait_time:.1f}s (attempt {attempt}/{MAX_RETRY_ATTEMPTS})"
                    )
                    time.sleep(wait_time)
                else:
                    logger.error(f"Maximum retry attempts reached for storage operation: {str(e)}")
                    raise StorageTimeoutError(f"Storage operation failed after {MAX_RETRY_ATTEMPTS} attempts: {str(e)}")
            except Exception as e:
                # Non-transient exception, don't retry
                raise
                
        # If we get here, we've exhausted all retries
        if last_exception:
            raise StorageTimeoutError(f"Storage operation failed after {MAX_RETRY_ATTEMPTS} attempts: {str(last_exception)}")
        
    return wrapper


class StorageService:
    """Service for handling document storage using MinIO."""
    
    def __init__(self):
        """Initialize the storage service."""
        try:
            # Initialize MinIO client
            self.client = Minio(
                settings.MINIO_ENDPOINT,
                access_key=settings.MINIO_ACCESS_KEY,
                secret_key=settings.MINIO_SECRET_KEY,
                secure=settings.MINIO_SECURE
            )
            
            # Ensure buckets exist
            self._ensure_bucket(settings.DOCUMENT_BUCKET)
            self._ensure_bucket(settings.PROCESSED_BUCKET)
            
            logger.info("Initialized StorageService with MinIO")
            
        except S3Error as e:
            logger.error(f"S3 error initializing StorageService: {e}")
            if "AccessDenied" in str(e):
                raise StorageAuthError("Authentication failed with storage provider")
            raise StorageError(f"S3 error initializing storage service: {str(e)}")
        except Exception as e:
            logger.error(f"Error initializing StorageService: {e}")
            raise StorageError(f"Failed to initialize storage service: {str(e)}")
    
    def _ensure_bucket(self, bucket_name: str) -> None:
        """
        Ensure a bucket exists, creating it if necessary.
        
        Args:
            bucket_name: Name of the bucket
        """
        try:
            if not self.client.bucket_exists(bucket_name):
                self.client.make_bucket(bucket_name)
                logger.info(f"Created bucket: {bucket_name}")
        except S3Error as e:
            logger.error(f"S3 error ensuring bucket {bucket_name}: {e}")
            if "AccessDenied" in str(e):
                raise StorageAuthError(f"Not authorized to create bucket {bucket_name}")
            raise StorageError(f"Failed to ensure bucket exists: {str(e)}")
        except Exception as e:
            logger.error(f"Error ensuring bucket {bucket_name}: {e}")
            raise StorageError(f"Failed to ensure bucket exists: {str(e)}")
    
    @with_retry
    async def store_document(self, file: UploadFile, storage_path: str) -> None:
        """
        Store a document file.
        
        Args:
            file: File to store
            storage_path: Path to store the file at
        """
        temp_file_path = None
        
        try:
            # Create a temporary file
            with tempfile.NamedTemporaryFile(delete=False) as temp_file:
                temp_file_path = temp_file.name
                
                # Write uploaded file to temporary file
                content = await file.read()
                temp_file.write(content)
                temp_file.flush()
                
                # Upload to MinIO
                self.client.fput_object(
                    settings.DOCUMENT_BUCKET,
                    storage_path,
                    temp_file.name,
                    content_type=file.content_type
                )
            
            logger.info(f"Stored document at {storage_path}")
            
        except S3Error as e:
            logger.error(f"S3 error storing document: {e}")
            if "NoSuchBucket" in str(e):
                raise BucketNotFoundError(f"Document bucket '{settings.DOCUMENT_BUCKET}' not found")
            elif "AccessDenied" in str(e):
                raise StorageAuthError("Not authorized to store document")
            raise StorageError(f"S3 error storing document: {str(e)}")
        except Exception as e:
            logger.error(f"Error storing document: {e}")
            raise StorageError(f"Failed to store document: {str(e)}")
        finally:
            # Clean up temporary file
            if temp_file_path and os.path.exists(temp_file_path):
                try:
                    os.unlink(temp_file_path)
                except Exception as e:
                    logger.warning(f"Failed to clean up temporary file {temp_file_path}: {e}")
    
    @with_retry
    async def get_document_content(self, storage_path: str) -> str:
        """
        Get the text content of a document.
        
        Args:
            storage_path: Path to the document
            
        Returns:
            Document text content
        """
        try:
            # Check if object exists first to provide a clearer error message
            try:
                self.client.stat_object(settings.DOCUMENT_BUCKET, storage_path)
            except S3Error as e:
                if "NoSuchKey" in str(e) or "Not Found" in str(e):
                    raise DocumentNotFoundError(f"Document not found at path: {storage_path}")
                raise
                
            # Get object data
            data = self.client.get_object(
                settings.DOCUMENT_BUCKET,
                storage_path
            )
            
            # Read content
            content = data.read()
            
            # TODO: Add document text extraction based on file type
            # For now, assume text content
            text_content = content.decode('utf-8')
            
            logger.info(f"Retrieved content from {storage_path}")
            return text_content
            
        except DocumentNotFoundError:
            # Re-raise document not found errors
            raise
        except S3Error as e:
            logger.error(f"S3 error getting document content: {e}")
            if "NoSuchBucket" in str(e):
                raise BucketNotFoundError(f"Document bucket '{settings.DOCUMENT_BUCKET}' not found")
            elif "AccessDenied" in str(e):
                raise StorageAuthError("Not authorized to access document")
            elif "NoSuchKey" in str(e) or "Not Found" in str(e):
                raise DocumentNotFoundError(f"Document not found at path: {storage_path}")
            raise StorageError(f"S3 error getting document content: {str(e)}")
        except UnicodeDecodeError as e:
            logger.error(f"Document decoding error: {e}")
            raise StorageError(f"Invalid document encoding or non-text document: {str(e)}")
        except Exception as e:
            logger.error(f"Error getting document content: {e}")
            raise StorageError(f"Failed to get document content: {str(e)}")
    
    @with_retry
    async def store_processed_document(
        self,
        document_id: int,
        content: bytes,
        content_type: str
    ) -> str:
        """
        Store a processed document.
        
        Args:
            document_id: ID of the document
            content: Processed content
            content_type: Content type of the processed document
            
        Returns:
            Storage path of the processed document
        """
        try:
            # Generate storage path
            storage_path = f"{document_id}/processed.txt"
            
            # Store content
            self.client.put_object(
                settings.PROCESSED_BUCKET,
                storage_path,
                io.BytesIO(content),
                len(content),
                content_type=content_type
            )
            
            logger.info(f"Stored processed document at {storage_path}")
            return storage_path
            
        except S3Error as e:
            logger.error(f"S3 error storing processed document: {e}")
            if "NoSuchBucket" in str(e):
                raise BucketNotFoundError(f"Processed bucket '{settings.PROCESSED_BUCKET}' not found")
            elif "AccessDenied" in str(e):
                raise StorageAuthError("Not authorized to store processed document")
            raise StorageError(f"S3 error storing processed document: {str(e)}")
        except Exception as e:
            logger.error(f"Error storing processed document: {e}")
            raise StorageError(f"Failed to store processed document: {str(e)}")
    
    @with_retry
    async def delete_document(self, storage_path: str) -> None:
        """
        Delete a document.
        
        Args:
            storage_path: Path to the document
        """
        document_deletion_success = False
        processed_deletion_success = False
        
        try:
            # Check if original document exists
            try:
                self.client.stat_object(settings.DOCUMENT_BUCKET, storage_path)
                
                # Remove from document bucket
                self.client.remove_object(settings.DOCUMENT_BUCKET, storage_path)
                document_deletion_success = True
                logger.info(f"Deleted document at {storage_path}")
                
            except S3Error as e:
                if "NoSuchKey" in str(e) or "Not Found" in str(e):
                    logger.warning(f"Document not found at path during deletion: {storage_path}")
                    # Continue to try deleting processed version
                else:
                    raise
            
            # Try to remove processed version if it exists
            processed_path = f"{storage_path}/processed.txt"
            try:
                self.client.stat_object(settings.PROCESSED_BUCKET, processed_path)
                self.client.remove_object(settings.PROCESSED_BUCKET, processed_path)
                processed_deletion_success = True
                logger.info(f"Deleted processed document at {processed_path}")
            except S3Error as e:
                if "NoSuchKey" in str(e) or "Not Found" in str(e):
                    logger.info(f"No processed document found at {processed_path}")
                else:
                    logger.warning(f"Error removing processed document {processed_path}: {e}")
                    # Continue execution - we've already deleted the main document
            
            # Check if we deleted at least one file
            if not document_deletion_success and not processed_deletion_success:
                raise DocumentNotFoundError(f"No document found to delete at {storage_path}")
                
        except DocumentNotFoundError:
            # Re-raise specific exception
            raise
        except S3Error as e:
            logger.error(f"S3 error deleting document: {e}")
            if "NoSuchBucket" in str(e):
                raise BucketNotFoundError(f"Document bucket not found")
            elif "AccessDenied" in str(e):
                raise StorageAuthError("Not authorized to delete document")
            raise StorageError(f"S3 error deleting document: {str(e)}")
        except Exception as e:
            logger.error(f"Error deleting document: {e}")
            raise StorageError(f"Failed to delete document: {str(e)}")
    
    async def list_documents(self, prefix: str = "") -> List[str]:
        """
        List documents in the document bucket.
        
        Args:
            prefix: Optional prefix to filter by
            
        Returns:
            List of document paths
        """
        try:
            objects = self.client.list_objects(
                settings.DOCUMENT_BUCKET,
                prefix=prefix,
                recursive=True
            )
            
            paths = [obj.object_name for obj in objects]
            logger.info(f"Listed {len(paths)} documents with prefix '{prefix}'")
            return paths
            
        except S3Error as e:
            logger.error(f"S3 error listing documents: {e}")
            if "NoSuchBucket" in str(e):
                raise BucketNotFoundError(f"Document bucket '{settings.DOCUMENT_BUCKET}' not found")
            elif "AccessDenied" in str(e):
                raise StorageAuthError("Not authorized to list documents")
            raise StorageError(f"S3 error listing documents: {str(e)}")
        except Exception as e:
            logger.error(f"Error listing documents: {e}")
            raise StorageError(f"Failed to list documents: {str(e)}")


# Create global instance
storage_service = StorageService()

# Export functions that use the global instance
store_document = storage_service.store_document
get_document_content = storage_service.get_document_content
store_processed_document = storage_service.store_processed_document
delete_document = storage_service.delete_document
list_documents = storage_service.list_documents