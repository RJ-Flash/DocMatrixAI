import os
from datetime import date
from decimal import Decimal
from unittest.mock import patch

import pytest
from django.core.files.uploadedfile import SimpleUploadedFile
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient

from expense_doc.core.models import ExpenseDocument, ExpenseEntry
from expense_doc.ai.services import DocumentProcessingError

@pytest.fixture
def api_client():
    return APIClient()

@pytest.fixture
def authenticated_client(api_client, django_user_model):
    user = django_user_model.objects.create_user(
        username='testuser',
        password='testpass123'
    )
    api_client.force_authenticate(user=user)
    return api_client, user

@pytest.fixture
def sample_document():
    return SimpleUploadedFile(
        "receipt.jpg",
        b"file_content",
        content_type="image/jpeg"
    )

@pytest.mark.django_db
class TestExpenseDocumentAPI:
    """Test the expense document API endpoints."""

    def test_upload_document(self, authenticated_client, sample_document):
        client, user = authenticated_client
        url = reverse('document-upload')
        
        with patch('expense_doc.ai.services.AIService.validate_document') as mock_validate:
            mock_validate.return_value = (True, None)
            
            response = client.post(url, {
                'file': sample_document,
                'process_now': False
            }, format='multipart')
        
        assert response.status_code == status.HTTP_201_CREATED
        assert ExpenseDocument.objects.count() == 1
        document = ExpenseDocument.objects.first()
        assert document.user == user
        assert document.status == ExpenseDocument.Status.PENDING

    def test_upload_and_process_document(self, authenticated_client, sample_document):
        client, user = authenticated_client
        url = reverse('document-upload')
        
        mock_expense_data = [{
            'amount': Decimal('100.00'),
            'currency': 'USD',
            'date': date.today(),
            'vendor': 'Test Vendor',
            'category': ExpenseEntry.Category.MEALS,
            'confidence_score': 0.95
        }]
        
        with patch('expense_doc.ai.services.AIService.validate_document') as mock_validate, \
             patch('expense_doc.ai.services.AIService._process_with_ai') as mock_process:
            mock_validate.return_value = (True, None)
            mock_process.return_value = mock_expense_data
            
            response = client.post(url, {
                'file': sample_document,
                'process_now': True
            }, format='multipart')
        
        assert response.status_code == status.HTTP_201_CREATED
        assert ExpenseDocument.objects.count() == 1
        assert ExpenseEntry.objects.count() == 1
        
        document = ExpenseDocument.objects.first()
        assert document.status == ExpenseDocument.Status.COMPLETED
        
        entry = ExpenseEntry.objects.first()
        assert entry.amount == Decimal('100.00')
        assert entry.vendor == 'Test Vendor'

    def test_upload_invalid_file(self, authenticated_client):
        client, _ = authenticated_client
        url = reverse('document-upload')
        
        invalid_file = SimpleUploadedFile(
            "document.txt",
            b"invalid content",
            content_type="text/plain"
        )
        
        response = client.post(url, {
            'file': invalid_file,
            'process_now': False
        }, format='multipart')
        
        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert ExpenseDocument.objects.count() == 0

    def test_process_existing_document(self, authenticated_client, sample_document):
        client, user = authenticated_client
        
        # Create a document
        document = ExpenseDocument.objects.create(
            user=user,
            file=sample_document,
            file_type='jpg',
            status=ExpenseDocument.Status.PENDING
        )
        
        url = reverse('document-process', kwargs={'pk': document.pk})
        
        mock_expense_data = [{
            'amount': Decimal('150.00'),
            'currency': 'EUR',
            'date': date.today(),
            'vendor': 'Another Vendor',
            'category': ExpenseEntry.Category.TRAVEL,
            'confidence_score': 0.98
        }]
        
        with patch('expense_doc.ai.services.AIService._process_with_ai') as mock_process:
            mock_process.return_value = mock_expense_data
            response = client.post(url)
        
        assert response.status_code == status.HTTP_200_OK
        document.refresh_from_db()
        assert document.status == ExpenseDocument.Status.COMPLETED
        assert ExpenseEntry.objects.count() == 1
        
        entry = ExpenseEntry.objects.first()
        assert entry.amount == Decimal('150.00')
        assert entry.vendor == 'Another Vendor'

    def test_process_document_error(self, authenticated_client, sample_document):
        client, user = authenticated_client
        
        # Create a document
        document = ExpenseDocument.objects.create(
            user=user,
            file=sample_document,
            file_type='jpg',
            status=ExpenseDocument.Status.PENDING
        )
        
        url = reverse('document-process', kwargs={'pk': document.pk})
        
        with patch('expense_doc.ai.services.AIService._process_with_ai') as mock_process:
            mock_process.side_effect = DocumentProcessingError("AI service unavailable")
            response = client.post(url)
        
        assert response.status_code == status.HTTP_500_INTERNAL_SERVER_ERROR
        document.refresh_from_db()
        assert document.status == ExpenseDocument.Status.ERROR
        assert "AI service unavailable" in document.error_message

@pytest.mark.django_db
class TestExpenseEntryAPI:
    """Test the expense entry API endpoints."""

    def test_list_entries(self, authenticated_client, sample_document):
        client, user = authenticated_client
        
        # Create a document and entry
        document = ExpenseDocument.objects.create(
            user=user,
            file=sample_document,
            file_type='jpg',
            status=ExpenseDocument.Status.COMPLETED
        )
        
        entry = ExpenseEntry.objects.create(
            document=document,
            amount=Decimal('200.00'),
            currency='USD',
            date=date.today(),
            vendor='Test Store',
            category=ExpenseEntry.Category.SUPPLIES,
            confidence_score=0.92
        )
        
        url = reverse('entry-list')
        response = client.get(url)
        
        assert response.status_code == status.HTTP_200_OK
        assert len(response.data['results']) == 1
        assert response.data['results'][0]['amount'] == '200.00'
        assert response.data['results'][0]['vendor'] == 'Test Store'

    def test_retrieve_entry(self, authenticated_client, sample_document):
        client, user = authenticated_client
        
        # Create a document and entry
        document = ExpenseDocument.objects.create(
            user=user,
            file=sample_document,
            file_type='jpg',
            status=ExpenseDocument.Status.COMPLETED
        )
        
        entry = ExpenseEntry.objects.create(
            document=document,
            amount=Decimal('75.50'),
            currency='EUR',
            date=date.today(),
            vendor='Coffee Shop',
            category=ExpenseEntry.Category.MEALS,
            confidence_score=0.89
        )
        
        url = reverse('entry-detail', kwargs={'pk': entry.pk})
        response = client.get(url)
        
        assert response.status_code == status.HTTP_200_OK
        assert response.data['amount'] == '75.50'
        assert response.data['vendor'] == 'Coffee Shop'
        assert response.data['category'] == ExpenseEntry.Category.MEALS 