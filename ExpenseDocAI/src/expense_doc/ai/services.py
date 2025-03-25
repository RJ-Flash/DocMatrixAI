import logging
from datetime import datetime
from typing import Dict, List, Optional, Tuple

import pytesseract
from django.conf import settings
from django.core.files.base import ContentFile
from django.utils import timezone
from pdf2image import convert_from_bytes
from PIL import Image
import requests

from expense_doc.core.models import ExpenseDocument, ExpenseEntry
from .models import ExpenseExtractor

logger = logging.getLogger(__name__)

class DocumentProcessingError(Exception):
    """Base exception for document processing errors."""
    pass

class AIService:
    """Service for processing expense documents using AI."""

    def __init__(self):
        self.model_endpoint = settings.AI_SERVICE['MODEL_ENDPOINT']
        self.api_key = settings.AI_SERVICE['API_KEY']
        self.timeout = settings.AI_SERVICE['TIMEOUT']
        self.extractor = ExpenseExtractor()

    def process_document(self, document: ExpenseDocument) -> List[ExpenseEntry]:
        """
        Process an expense document using OCR and AI to extract expense data.
        
        Args:
            document: The ExpenseDocument instance to process
            
        Returns:
            List of created ExpenseEntry instances
            
        Raises:
            DocumentProcessingError: If processing fails
        """
        try:
            # Update document status
            document.status = ExpenseDocument.Status.PROCESSING
            document.processing_started_at = timezone.now()
            document.save()

            # Extract text from document
            text_blocks = self._extract_text_with_layout(document)
            if not text_blocks['lines']:
                raise DocumentProcessingError("No text could be extracted from document")

            # Process text with AI model
            expense_data = self._process_with_ai(text_blocks)
            
            # Create expense entries
            entries = []
            for data in expense_data:
                entry = ExpenseEntry.objects.create(
                    document=document,
                    amount=data['amount'],
                    currency=data['currency'],
                    date=data['date'],
                    vendor=data['vendor'],
                    category=data['category'],
                    description=data.get('description', ''),
                    tax_amount=data.get('tax_amount'),
                    confidence_score=data['confidence_score']
                )
                entries.append(entry)

            # Update document status
            document.status = ExpenseDocument.Status.COMPLETED
            document.processing_completed_at = timezone.now()
            document.save()

            return entries

        except Exception as e:
            logger.error(f"Error processing document {document.id}: {str(e)}", exc_info=True)
            document.status = ExpenseDocument.Status.ERROR
            document.error_message = str(e)
            document.save()
            raise DocumentProcessingError(f"Failed to process document: {str(e)}")

    def _extract_text_with_layout(self, document: ExpenseDocument) -> Dict[str, List[Dict]]:
        """
        Extract text with layout information from document using OCR.
        
        Args:
            document: The ExpenseDocument instance
            
        Returns:
            Dictionary containing extracted text blocks with positions
            
        Raises:
            DocumentProcessingError: If text extraction fails
        """
        try:
            if document.file_type.lower() in ['jpg', 'jpeg', 'png']:
                image = Image.open(document.file)
                text_blocks = self.extractor.extract_text_with_layout(image)
            elif document.file_type.lower() == 'pdf':
                # Convert PDF to images
                pdf_bytes = document.file.read()
                images = convert_from_bytes(pdf_bytes)
                
                # Extract text from each page
                text_blocks = {'lines': []}
                for image in images:
                    page_blocks = self.extractor.extract_text_with_layout(image)
                    text_blocks['lines'].extend(page_blocks['lines'])
            else:
                raise DocumentProcessingError(f"Unsupported file type: {document.file_type}")

            return text_blocks

        except Exception as e:
            logger.error(f"Error extracting text from document {document.id}: {str(e)}", exc_info=True)
            raise DocumentProcessingError(f"Failed to extract text: {str(e)}")

    def _process_with_ai(self, text_blocks: Dict[str, List[Dict]]) -> List[Dict]:
        """
        Process text blocks with AI model to identify expense data.
        
        Args:
            text_blocks: Dictionary of text blocks with layout information
            
        Returns:
            List of dictionaries containing extracted expense data
            
        Raises:
            DocumentProcessingError: If AI processing fails
        """
        try:
            # Extract expense data using our model
            expense_data = self.extractor.extract_expense_data(text_blocks)
            
            # Validate required fields
            required_fields = ['amount', 'currency', 'date', 'vendor', 'category', 'confidence_score']
            if not all(expense_data.get(field) for field in required_fields):
                raise DocumentProcessingError("Missing required fields in extracted data")
            
            # If confidence score is too low, try external AI service
            if expense_data['confidence_score'] < 0.8:
                logger.info("Low confidence score, trying external AI service")
                try:
                    external_data = self._process_with_external_ai(text_blocks)
                    if external_data['confidence_score'] > expense_data['confidence_score']:
                        expense_data = external_data
                except Exception as e:
                    logger.warning(f"External AI service failed: {str(e)}")
            
            return [expense_data]

        except Exception as e:
            logger.error(f"Error processing text with AI: {str(e)}", exc_info=True)
            raise DocumentProcessingError(f"Failed to process text with AI: {str(e)}")

    def _process_with_external_ai(self, text_blocks: Dict[str, List[Dict]]) -> Dict:
        """
        Process text with external AI service as backup.
        
        Args:
            text_blocks: Dictionary of text blocks with layout information
            
        Returns:
            Dictionary containing extracted expense data
            
        Raises:
            DocumentProcessingError: If AI processing fails
        """
        try:
            # Prepare text for API
            text = "\n".join(" ".join(block['text'] for block in line) 
                           for line in text_blocks['lines'])
            
            headers = {
                'Authorization': f'Bearer {self.api_key}',
                'Content-Type': 'application/json'
            }
            
            payload = {
                'text': text,
                'task': 'expense_extraction'
            }
            
            response = requests.post(
                self.model_endpoint,
                headers=headers,
                json=payload,
                timeout=self.timeout
            )
            
            if response.status_code != 200:
                raise DocumentProcessingError(
                    f"AI service returned error: {response.status_code} - {response.text}"
                )
                
            result = response.json()
            
            # Validate response format
            if not isinstance(result, list) or not result:
                raise DocumentProcessingError("Invalid response format from AI service")
            
            return result[0]

        except requests.exceptions.RequestException as e:
            logger.error(f"Error calling AI service: {str(e)}", exc_info=True)
            raise DocumentProcessingError(f"Failed to process with AI service: {str(e)}")

    def validate_document(self, file_content: bytes, file_type: str) -> Tuple[bool, Optional[str]]:
        """
        Validate document before processing.
        
        Args:
            file_content: The document file content
            file_type: The document file type
            
        Returns:
            Tuple of (is_valid, error_message)
        """
        # Check file type
        allowed_types = ['jpg', 'jpeg', 'png', 'pdf']
        if file_type.lower() not in allowed_types:
            return False, f"Unsupported file type. Allowed types: {', '.join(allowed_types)}"

        # Check file size (max 10MB)
        if len(file_content) > 10 * 1024 * 1024:
            return False, "File size exceeds maximum limit of 10MB"

        # For images, check dimensions
        if file_type.lower() in ['jpg', 'jpeg', 'png']:
            try:
                image = Image.open(ContentFile(file_content))
                width, height = image.size
                
                # Check minimum dimensions (500x500)
                if width < 500 or height < 500:
                    return False, "Image dimensions too small. Minimum size: 500x500 pixels"
                
                # Check maximum dimensions (5000x5000)
                if width > 5000 or height > 5000:
                    return False, "Image dimensions too large. Maximum size: 5000x5000 pixels"
                
            except Exception as e:
                return False, f"Invalid image file: {str(e)}"

        return True, None 