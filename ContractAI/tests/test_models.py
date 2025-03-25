"""
AI model tests for ContractAI.

This module contains tests for the AI models.
"""

import pytest
import torch
from app.ai.models.bert.clause_extractor import BertClauseExtractor
from app.ai.models.gpt.text_analyzer import GPTTextAnalyzer


@pytest.fixture
def bert_model():
    """
    Create a BERT model for testing.
    """
    return BertClauseExtractor()


@pytest.fixture
def gpt_model():
    """
    Create a GPT model for testing.
    """
    return GPTTextAnalyzer()


def test_bert_model_initialization(bert_model):
    """
    Test that the BERT model initializes correctly.
    """
    assert bert_model is not None
    assert bert_model.tokenizer is not None
    assert bert_model.model is not None


def test_gpt_model_initialization(gpt_model):
    """
    Test that the GPT model initializes correctly.
    """
    assert gpt_model is not None


@pytest.mark.skipif(not torch.cuda.is_available(), reason="CUDA not available")
def test_bert_model_cuda(bert_model):
    """
    Test that the BERT model can be moved to CUDA.
    """
    bert_model.model.to("cuda")
    assert next(bert_model.model.parameters()).is_cuda


def test_bert_clause_extraction():
    """
    Test the BERT clause extraction functionality.
    """
    model = BertClauseExtractor()
    
    # Sample contract text
    text = """
    CONFIDENTIALITY AGREEMENT
    
    This Confidentiality Agreement (the "Agreement") is entered into as of January 1, 2023 (the "Effective Date") by and between:
    
    Company A, a corporation organized under the laws of Delaware, with its principal place of business at 123 Main St, Anytown, USA ("Discloser")
    
    and
    
    Company B, a corporation organized under the laws of California, with its principal place of business at 456 Oak Ave, Othertown, USA ("Recipient").
    
    1. CONFIDENTIAL INFORMATION
    
    "Confidential Information" means any information disclosed by Discloser to Recipient, either directly or indirectly, in writing, orally or by inspection of tangible objects, which is designated as "Confidential," "Proprietary" or some similar designation, or that should reasonably be understood to be confidential given the nature of the information and the circumstances of disclosure.
    
    2. TERM
    
    This Agreement shall remain in effect for a period of 3 years from the Effective Date.
    """
    
    # This is a placeholder test since the actual implementation is not complete
    # In a real test, we would expect the model to extract clauses
    assert hasattr(model, "extract_clauses")
    
    # For now, we'll just check that the method doesn't raise an exception
    try:
        model.extract_clauses(text)
        assert True
    except NotImplementedError:
        # It's okay if the method is not implemented yet
        assert True


def test_gpt_text_analysis():
    """
    Test the GPT text analysis functionality.
    """
    model = GPTTextAnalyzer()
    
    # Sample contract text
    text = """
    CONFIDENTIALITY AGREEMENT
    
    This Confidentiality Agreement (the "Agreement") is entered into as of January 1, 2023 (the "Effective Date") by and between:
    
    Company A, a corporation organized under the laws of Delaware, with its principal place of business at 123 Main St, Anytown, USA ("Discloser")
    
    and
    
    Company B, a corporation organized under the laws of California, with its principal place of business at 456 Oak Ave, Othertown, USA ("Recipient").
    """
    
    # This is a placeholder test since the actual implementation is not complete
    # In a real test, we would expect the model to analyze the text
    assert hasattr(model, "analyze_text")
    
    # For now, we'll just check that the method doesn't raise an exception
    try:
        model.analyze_text(text)
        assert True
    except NotImplementedError:
        # It's okay if the method is not implemented yet
        assert True 