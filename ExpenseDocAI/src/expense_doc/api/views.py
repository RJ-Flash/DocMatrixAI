from typing import Any, Dict

from django.db import transaction
from django.utils import timezone
from rest_framework import status, viewsets
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.parsers import MultiPartParser, FormParser

from expense_doc.ai.services import AIService, DocumentProcessingError
from expense_doc.core.models import ExpenseDocument, ExpenseEntry
from .serializers import (
    ExpenseDocumentSerializer,
    ExpenseEntrySerializer,
    ExpenseDocumentUploadSerializer
)

class ExpenseDocumentViewSet(viewsets.ModelViewSet):
    """
    ViewSet for managing expense documents.
    """
    permission_classes = [IsAuthenticated]
    serializer_class = ExpenseDocumentSerializer
    parser_classes = (MultiPartParser, FormParser)
    
    def get_queryset(self):
        """Filter queryset to return only documents belonging to the current user."""
        return ExpenseDocument.objects.filter(user=self.request.user)
    
    def perform_create(self, serializer: ExpenseDocumentSerializer) -> None:
        """Add the current user when creating a document."""
        serializer.save(user=self.request.user)
    
    @action(detail=False, methods=['post'])
    def upload(self, request: Request) -> Response:
        """
        Upload and process a new expense document.
        
        Request body should be multipart/form-data with:
        - file: The document file (required)
        - process_now: Boolean indicating whether to process immediately (optional)
        """
        serializer = ExpenseDocumentUploadSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
        file_obj = serializer.validated_data['file']
        process_now = serializer.validated_data.get('process_now', False)
        
        # Validate file
        ai_service = AIService()
        is_valid, error_message = ai_service.validate_document(
            file_obj.read(),
            file_obj.name.split('.')[-1]
        )
        
        if not is_valid:
            return Response(
                {'error': error_message},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        # Reset file pointer after validation
        file_obj.seek(0)
        
        try:
            with transaction.atomic():
                # Create document
                document = ExpenseDocument.objects.create(
                    user=request.user,
                    file=file_obj,
                    file_type=file_obj.name.split('.')[-1],
                    status=ExpenseDocument.Status.PENDING
                )
                
                # Process document if requested
                if process_now:
                    entries = ai_service.process_document(document)
                    return Response({
                        'document': ExpenseDocumentSerializer(document).data,
                        'entries': ExpenseEntrySerializer(entries, many=True).data
                    }, status=status.HTTP_201_CREATED)
                
                return Response(
                    ExpenseDocumentSerializer(document).data,
                    status=status.HTTP_201_CREATED
                )
                
        except DocumentProcessingError as e:
            return Response(
                {'error': str(e)},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
    
    @action(detail=True, methods=['post'])
    def process(self, request: Request, pk: int = None) -> Response:
        """
        Process an existing document.
        """
        document = self.get_object()
        
        # Check if document is already processed
        if document.status == ExpenseDocument.Status.COMPLETED:
            return Response(
                {'error': 'Document is already processed'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        # Check if document is currently processing
        if document.status == ExpenseDocument.Status.PROCESSING:
            return Response(
                {'error': 'Document is currently being processed'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        try:
            ai_service = AIService()
            entries = ai_service.process_document(document)
            return Response({
                'document': ExpenseDocumentSerializer(document).data,
                'entries': ExpenseEntrySerializer(entries, many=True).data
            })
            
        except DocumentProcessingError as e:
            return Response(
                {'error': str(e)},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

class ExpenseEntryViewSet(viewsets.ReadOnlyModelViewSet):
    """
    ViewSet for viewing expense entries.
    Read-only as entries are created through document processing.
    """
    permission_classes = [IsAuthenticated]
    serializer_class = ExpenseEntrySerializer
    
    def get_queryset(self):
        """Filter queryset to return only entries from documents belonging to the current user."""
        return ExpenseEntry.objects.filter(document__user=self.request.user)
    
    def get_serializer_context(self) -> Dict[str, Any]:
        """Add additional context to serializer."""
        context = super().get_serializer_context()
        context['request'] = self.request
        return context 