"""Tests for AI models."""

import os
from pathlib import Path
import pytest
from PIL import Image
import numpy as np

from expense_doc.ai.models import ExpenseExtractor

@pytest.fixture
def sample_receipt():
    """Create a sample receipt image for testing."""
    # Create a white image with black text
    img = Image.new('RGB', (1000, 1000), 'white')
    pixels = np.array(img)
    
    # Add sample text
    text_lines = [
        "ACME Store",
        "123 Main St",
        "Date: 2024-02-20",
        "Amount: $123.45",
        "Tax: $10.00",
        "Category: Office Supplies",
    ]
    
    # Convert text to image
    from PIL import ImageDraw
    draw = ImageDraw.Draw(img)
    y = 100
    for line in text_lines:
        draw.text((100, y), line, fill='black')
        y += 50
    
    return img

@pytest.fixture
def expense_extractor():
    """Create an ExpenseExtractor instance."""
    return ExpenseExtractor()

def test_preprocess_image(expense_extractor, sample_receipt):
    """Test image preprocessing."""
    processed = expense_extractor.preprocess_image(sample_receipt)
    
    # Check that image is grayscale
    assert processed.mode == 'L'
    
    # Check dimensions are preserved
    assert processed.size == sample_receipt.size

def test_extract_text_with_layout(expense_extractor, sample_receipt):
    """Test text extraction with layout information."""
    text_blocks = expense_extractor.extract_text_with_layout(sample_receipt)
    
    # Check structure
    assert 'lines' in text_blocks
    assert isinstance(text_blocks['lines'], list)
    
    # Check content
    found_fields = set()
    for line in text_blocks['lines']:
        text = ' '.join(block['text'] for block in line)
        if 'ACME Store' in text:
            found_fields.add('vendor')
        elif 'Date:' in text:
            found_fields.add('date')
        elif 'Amount:' in text:
            found_fields.add('amount')
    
    # Verify key fields were found
    assert 'vendor' in found_fields
    assert 'date' in found_fields
    assert 'amount' in found_fields

def test_classify_text_block(expense_extractor):
    """Test text block classification."""
    # Test amount
    assert expense_extractor.classify_text_block("Total: $123.45") == 'amount'
    
    # Test date
    assert expense_extractor.classify_text_block("Date: 2024-02-20") == 'date'
    
    # Test vendor
    assert expense_extractor.classify_text_block("ACME Store") == 'vendor'
    
    # Test category
    assert expense_extractor.classify_text_block("Category: Office Supplies") == 'category'
    
    # Test unrecognized text
    assert expense_extractor.classify_text_block("Random text") == 'other'

def test_extract_expense_data(expense_extractor, sample_receipt):
    """Test full expense data extraction."""
    # Extract text blocks
    text_blocks = expense_extractor.extract_text_with_layout(sample_receipt)
    
    # Extract expense data
    expense_data = expense_extractor.extract_expense_data(text_blocks)
    
    # Check required fields
    assert 'amount' in expense_data
    assert 'date' in expense_data
    assert 'vendor' in expense_data
    assert 'category' in expense_data
    assert 'confidence_score' in expense_data
    
    # Check confidence score
    assert 0 <= expense_data['confidence_score'] <= 1.0

def test_confidence_score_calculation(expense_extractor):
    """Test confidence score calculation."""
    # Create test data with known confidence values
    text_blocks = {
        'lines': [
            [{'text': 'Amount: $100', 'conf': 90}],
            [{'text': 'Date: 2024-02-20', 'conf': 95}],
            [{'text': 'ACME Store', 'conf': 85}]
        ]
    }
    
    # Extract expense data
    expense_data = expense_extractor.extract_expense_data(text_blocks)
    
    # Expected confidence score: (90 + 95 + 85) / 3 / 100 = 0.9
    assert abs(expense_data['confidence_score'] - 0.9) < 0.1 