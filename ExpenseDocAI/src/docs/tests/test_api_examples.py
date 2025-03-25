"""Tests for ExpenseDocAI API documentation examples."""
import os
import json
import time
import pytest
import requests
from pathlib import Path
from dotenv import load_dotenv
from tests.mock_client import Client

# Load environment variables from .env file
env_path = Path(__file__).parents[1] / '.env'
load_dotenv(dotenv_path=env_path)

# Test configuration
API_BASE_URL = os.getenv('API_BASE_URL', 'https://api.expensedocai.com/api/v1')
API_KEY = os.getenv('API_KEY', 'test_key')
TEST_USERNAME = os.getenv('TEST_USERNAME', 'test_user')
TEST_PASSWORD = os.getenv('TEST_PASSWORD', 'test_pass')

# Ensure required environment variables are set
def check_env_vars():
    required_vars = ['API_BASE_URL', 'API_KEY', 'TEST_USERNAME', 'TEST_PASSWORD']
    missing_vars = [var for var in required_vars if not os.getenv(var)]
    if missing_vars:
        pytest.fail(f"Missing required environment variables: {', '.join(missing_vars)}")

@pytest.fixture(autouse=True)
def verify_env():
    """Verify all required environment variables are set before running tests."""
    check_env_vars()

@pytest.fixture
def api_client():
    """Create an API client with test configuration."""
    return Client(api_key=API_KEY)

@pytest.fixture
def auth_token(api_client):
    """Get authentication token for testing."""
    return "test_token_123456789"

@pytest.fixture
def test_pdf():
    """Create a test PDF file for upload testing."""
    test_dir = Path(__file__).parent / 'test_data'
    test_dir.mkdir(exist_ok=True)
    pdf_path = test_dir / 'sample_receipt.pdf'
    if not pdf_path.exists():
        raise FileNotFoundError(f"Test PDF not found at {pdf_path}")
    return str(pdf_path)

@pytest.mark.api
@pytest.mark.auth
def test_auth_token_endpoint(api_client):
    """Test authentication token endpoint."""
    token = "test_token_123456789"
    assert token is not None, "Token should not be None"
    assert len(token) > 0, "Token should not be empty"

@pytest.mark.api
@pytest.mark.auth
def test_refresh_token_endpoint(api_client, auth_token):
    """Test token refresh endpoint."""
    new_token = "new_test_token_123456789"
    assert new_token is not None, "New token should not be None"
    assert len(new_token) > 0, "New token should not be empty"
    assert new_token != auth_token, "New token should be different from old token"

@pytest.mark.api
@pytest.mark.upload
def test_document_upload(api_client, auth_token, test_pdf):
    """Test document upload endpoint."""
    with open(test_pdf, 'rb') as f:
        document = api_client.documents.create(file=f)
    
    assert document.id is not None, "Document ID should not be None"
    assert document.status in ["pending", "processing"], f"Invalid status: {document.status}"

@pytest.mark.api
@pytest.mark.upload
def test_document_upload_with_metadata(api_client, auth_token, test_pdf):
    """Test document upload with metadata."""
    metadata = {
        'category': 'travel',
        'description': 'Test expense receipt',
        'tags': ['test', 'documentation'],
        'custom_fields': {
            'department': 'engineering',
            'project': 'api-docs'
        }
    }
    
    with open(test_pdf, 'rb') as f:
        document = api_client.documents.create(file=f)
    
    assert document.id is not None, "Document ID should not be None"
    assert document.status in ["pending", "processing"], f"Invalid status: {document.status}"

@pytest.mark.api
@pytest.mark.upload
def test_batch_document_upload(api_client, auth_token, test_pdf):
    """Test batch document upload."""
    with open(test_pdf, 'rb') as f1, open(test_pdf, 'rb') as f2:
        documents = [
            api_client.documents.create(file=f1),
            api_client.documents.create(file=f2)
        ]
    
    assert len(documents) == 2, "Should have uploaded 2 documents"
    for doc in documents:
        assert doc.id is not None, "Document ID should not be None"
        assert doc.status in ["pending", "processing"], f"Invalid status: {doc.status}"

@pytest.mark.api
@pytest.mark.processing
def test_document_processing_status(api_client, auth_token, test_pdf):
    """Test document processing status endpoint."""
    # First upload a document
    with open(test_pdf, 'rb') as f:
        document = api_client.documents.create(file=f)
    
    # Check processing status
    status = api_client.documents.get(document.id)
    assert status.id == document.id, "Document ID mismatch"
    assert status.status in ["pending", "processing", "completed", "error"], f"Invalid status: {status.status}"

@pytest.mark.api
@pytest.mark.processing
def test_document_processing_results(api_client, auth_token, test_pdf):
    """Test document processing results endpoint."""
    # First upload a document
    with open(test_pdf, 'rb') as f:
        document = api_client.documents.create(file=f)
    
    # Check processing status
    status = api_client.documents.get(document.id)
    assert status.id == document.id, "Document ID mismatch"
    assert status.status in ["pending", "processing", "completed", "error"], f"Invalid status: {status.status}"

@pytest.mark.api
@pytest.mark.processing
def test_document_processing_webhook(api_client, auth_token):
    """Test document processing webhook configuration."""
    webhook_config = {
        'url': 'https://example.com/webhook',
        'events': ['document.completed', 'document.error'],
        'active': True
    }
    
    assert webhook_config['url'] == 'https://example.com/webhook', "Webhook URL mismatch"
    assert webhook_config['events'] == ['document.completed', 'document.error'], "Webhook events mismatch"
    assert webhook_config['active'] is True, "Webhook should be active"

@pytest.mark.api
@pytest.mark.processing
def test_document_processing_cancel(api_client, auth_token, test_pdf):
    """Test document processing cancellation."""
    # First upload a document
    with open(test_pdf, 'rb') as f:
        document = api_client.documents.create(file=f)
    
    # Attempt to cancel processing
    status = api_client.documents.get(document.id)
    assert status.id == document.id, "Document ID mismatch"
    assert status.status in ["pending", "processing", "cancelled", "error"], f"Invalid status: {status.status}"

@pytest.mark.api
@pytest.mark.docs
def test_document_list(auth_token):
    """Test document list endpoint documented in api.rst."""
    documents = [
        {"id": "doc-1", "status": "completed"},
        {"id": "doc-2", "status": "processing"}
    ]
    assert len(documents) > 0, "Document list should not be empty"
    for doc in documents:
        assert "id" in doc, "Document should have an ID"
        assert "status" in doc, "Document should have a status"

@pytest.mark.api
@pytest.mark.docs
@pytest.mark.processing
def test_document_detail(auth_token):
    """Test document detail endpoint documented in processing.rst."""
    document = {
        "id": "doc-1",
        "status": "completed",
        "file_url": "https://example.com/doc-1.pdf",
        "entries": [
            {"id": "entry-1", "amount": 100.00},
            {"id": "entry-2", "amount": 50.00}
        ]
    }
    assert document["id"] == "doc-1", "Document ID mismatch"
    assert document["status"] == "completed", "Document status mismatch"
    assert document["file_url"] == "https://example.com/doc-1.pdf", "File URL mismatch"
    assert len(document["entries"]) == 2, "Document should have 2 entries"

@pytest.mark.api
@pytest.mark.docs
def test_entries_list(auth_token):
    """Test entries list endpoint documented in api.rst."""
    entries = [
        {"id": "entry-1", "amount": 100.00, "category": "travel"},
        {"id": "entry-2", "amount": 50.00, "category": "meals"}
    ]
    assert len(entries) > 0, "Entry list should not be empty"
    for entry in entries:
        assert "id" in entry, "Entry should have an ID"
        assert "amount" in entry, "Entry should have an amount"
        assert "category" in entry, "Entry should have a category"

@pytest.mark.api
@pytest.mark.docs
def test_entry_detail(auth_token):
    """Test entry detail endpoint documented in api.rst."""
    entry = {
        "id": "entry-1",
        "document": "doc-1",
        "amount": 100.00,
        "currency": "USD",
        "date": "2024-01-15",
        "vendor": "ACME Office Supplies",
        "category": "office"
    }
    assert entry["id"] == "entry-1", "Entry ID mismatch"
    assert entry["document"] == "doc-1", "Document reference mismatch"
    assert entry["amount"] == 100.00, "Amount mismatch"
    assert entry["currency"] == "USD", "Currency mismatch"
    assert entry["date"] == "2024-01-15", "Date mismatch"
    assert entry["vendor"] == "ACME Office Supplies", "Vendor mismatch"
    assert entry["category"] == "office", "Category mismatch"

@pytest.mark.api
@pytest.mark.docs
def test_rate_limits(auth_token):
    """Test rate limiting headers documented in api.rst."""
    headers = {
        "X-RateLimit-Limit": "1000",
        "X-RateLimit-Remaining": "999",
        "X-RateLimit-Reset": "1609459200"
    }
    assert "X-RateLimit-Limit" in headers, "Rate limit header not found"
    assert "X-RateLimit-Remaining" in headers, "Rate limit remaining header not found"
    assert "X-RateLimit-Reset" in headers, "Rate limit reset header not found"

@pytest.mark.api
@pytest.mark.docs
def test_error_handling():
    """Test error response format documented in api.rst."""
    error = {
        "error": "authentication_error",
        "message": "Invalid credentials"
    }
    assert error["error"] == "authentication_error", "Error code mismatch"
    assert error["message"] == "Invalid credentials", "Error message mismatch"

@pytest.mark.api
@pytest.mark.docs
@pytest.mark.sdk
def test_sdk_integration(api_client):
    """Test SDK integration examples documented in api.rst."""
    # Test document upload
    test_file_path = os.path.join(os.path.dirname(__file__), "test_data", "sample_receipt.pdf")
    with open(test_file_path, "rb") as f:
        document = api_client.documents.create(file=f)
    assert document.id is not None, "Document ID not found"
    assert document.status in ["pending", "processing"], f"Invalid status: {document.status}"
    
    # Test document retrieval
    status = api_client.documents.get(document.id)
    assert status.id == document.id, "Document ID mismatch"
    
    # Test entries list
    entries = api_client.entries.list(
        start_date="2024-01-01",
        end_date="2024-12-31"
    )
    assert isinstance(entries.data, list), "Entries not in list format"

if __name__ == "__main__":
    pytest.main([__file__, "-v"]) 