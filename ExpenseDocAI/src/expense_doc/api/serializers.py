from rest_framework import serializers
from django.core.validators import FileExtensionValidator

from expense_doc.core.models import ExpenseDocument, ExpenseEntry, PolicyViolation

class PolicyViolationSerializer(serializers.ModelSerializer):
    """Serializer for policy violations."""
    
    class Meta:
        model = PolicyViolation
        fields = ['id', 'rule_name', 'description', 'severity', 'created_at']
        read_only_fields = fields

class ExpenseEntrySerializer(serializers.ModelSerializer):
    """Serializer for expense entries."""
    
    policy_violations = PolicyViolationSerializer(many=True, read_only=True)
    
    class Meta:
        model = ExpenseEntry
        fields = [
            'id', 'document', 'amount', 'currency', 'date', 'vendor',
            'category', 'description', 'tax_amount', 'created_at',
            'updated_at', 'confidence_score', 'policy_violations'
        ]
        read_only_fields = fields

class ExpenseDocumentSerializer(serializers.ModelSerializer):
    """Serializer for expense documents."""
    
    entries = ExpenseEntrySerializer(many=True, read_only=True)
    file_url = serializers.SerializerMethodField()
    
    class Meta:
        model = ExpenseDocument
        fields = [
            'id', 'user', 'file', 'file_url', 'file_type', 'uploaded_at',
            'status', 'processing_started_at', 'processing_completed_at',
            'error_message', 'entries'
        ]
        read_only_fields = [
            'user', 'file_type', 'uploaded_at', 'status',
            'processing_started_at', 'processing_completed_at',
            'error_message', 'entries'
        ]
    
    def get_file_url(self, obj):
        """Get the URL for accessing the document file."""
        request = self.context.get('request')
        if request and obj.file:
            return request.build_absolute_uri(obj.file.url)
        return None

class ExpenseDocumentUploadSerializer(serializers.Serializer):
    """Serializer for document upload endpoint."""
    
    file = serializers.FileField(
        validators=[FileExtensionValidator(allowed_extensions=['jpg', 'jpeg', 'png', 'pdf'])]
    )
    process_now = serializers.BooleanField(default=False)
    
    def validate_file(self, value):
        """Validate file size."""
        if value.size > 10 * 1024 * 1024:  # 10MB
            raise serializers.ValidationError(
                'File size too large. Maximum size is 10MB.'
            )
        return value 