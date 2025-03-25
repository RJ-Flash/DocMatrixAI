"""AI models for expense document processing."""

from typing import Dict, List, Optional
import numpy as np
from PIL import Image
import pytesseract
from transformers import AutoTokenizer, AutoModelForSequenceClassification

class ExpenseExtractor:
    """Model for extracting expense information from documents."""
    
    def __init__(self):
        # Load pre-trained models for document classification and data extraction
        self.tokenizer = AutoTokenizer.from_pretrained("microsoft/layoutlm-base-uncased")
        self.model = AutoModelForSequenceClassification.from_pretrained("microsoft/layoutlm-base-uncased")
        
        # Configure OCR settings
        self.ocr_config = '--oem 3 --psm 6'
    
    def preprocess_image(self, image: Image.Image) -> Image.Image:
        """
        Preprocess image for better OCR results.
        
        Args:
            image: PIL Image to preprocess
            
        Returns:
            Preprocessed image
        """
        # Convert to grayscale
        image = image.convert('L')
        
        # Increase contrast
        image = Image.fromarray(np.uint8(255 * (np.array(image) / 255) ** 1.5))
        
        return image
    
    def extract_text_with_layout(self, image: Image.Image) -> Dict[str, List[Dict]]:
        """
        Extract text with layout information using OCR.
        
        Args:
            image: PIL Image to process
            
        Returns:
            Dictionary containing extracted text blocks with positions
        """
        # Preprocess image
        processed_image = self.preprocess_image(image)
        
        # Get OCR data with layout
        ocr_data = pytesseract.image_to_data(
            processed_image,
            config=self.ocr_config,
            output_type=pytesseract.Output.DICT
        )
        
        # Group text by lines
        lines = []
        current_line = []
        current_line_number = -1
        
        for i in range(len(ocr_data['text'])):
            if ocr_data['text'][i].strip():
                if ocr_data['line_num'][i] != current_line_number:
                    if current_line:
                        lines.append(current_line)
                    current_line = []
                    current_line_number = ocr_data['line_num'][i]
                
                current_line.append({
                    'text': ocr_data['text'][i],
                    'conf': ocr_data['conf'][i],
                    'left': ocr_data['left'][i],
                    'top': ocr_data['top'][i],
                    'width': ocr_data['width'][i],
                    'height': ocr_data['height'][i]
                })
        
        if current_line:
            lines.append(current_line)
        
        return {'lines': lines}
    
    def classify_text_block(self, text: str) -> Optional[str]:
        """
        Classify text block into expense fields (amount, date, vendor, etc.).
        
        Args:
            text: Text block to classify
            
        Returns:
            Field type or None if not recognized
        """
        # Tokenize text
        inputs = self.tokenizer(
            text,
            padding=True,
            truncation=True,
            return_tensors="pt"
        )
        
        # Get model predictions
        outputs = self.model(**inputs)
        predictions = outputs.logits.argmax(dim=-1)
        
        # Map prediction to field type
        field_types = [
            'amount',
            'date',
            'vendor',
            'description',
            'category',
            'tax_amount',
            'other'
        ]
        
        return field_types[predictions[0]] if predictions[0] < len(field_types) else None
    
    def extract_expense_data(self, text_blocks: Dict[str, List[Dict]]) -> Dict:
        """
        Extract structured expense data from text blocks.
        
        Args:
            text_blocks: Dictionary of text blocks with layout information
            
        Returns:
            Dictionary containing extracted expense data
        """
        expense_data = {
            'amount': None,
            'date': None,
            'vendor': None,
            'description': None,
            'category': None,
            'tax_amount': None,
            'confidence_score': 0.0
        }
        
        total_confidence = 0
        field_count = 0
        
        for line in text_blocks['lines']:
            # Combine text in line
            line_text = ' '.join(block['text'] for block in line)
            
            # Get average confidence for line
            line_conf = sum(block['conf'] for block in line) / len(line)
            
            # Classify text and update expense data
            field_type = self.classify_text_block(line_text)
            if field_type and field_type in expense_data:
                expense_data[field_type] = line_text
                total_confidence += line_conf
                field_count += 1
        
        # Calculate overall confidence score
        if field_count > 0:
            expense_data['confidence_score'] = total_confidence / field_count / 100.0
        
        return expense_data 