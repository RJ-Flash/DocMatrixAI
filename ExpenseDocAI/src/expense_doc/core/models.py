from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MinValueValidator
from django.utils.translation import gettext_lazy as _

class ExpenseDocument(models.Model):
    """Model for storing expense documents (receipts, invoices, etc.)."""
    
    class Status(models.TextChoices):
        PENDING = 'PENDING', _('Pending')
        PROCESSING = 'PROCESSING', _('Processing')
        COMPLETED = 'COMPLETED', _('Completed')
        ERROR = 'ERROR', _('Error')
    
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='expense_documents')
    file = models.FileField(upload_to='expenses/%Y/%m/%d/')
    file_type = models.CharField(max_length=50)
    uploaded_at = models.DateTimeField(auto_now_add=True)
    status = models.CharField(
        max_length=20,
        choices=Status.choices,
        default=Status.PENDING
    )
    processing_started_at = models.DateTimeField(null=True, blank=True)
    processing_completed_at = models.DateTimeField(null=True, blank=True)
    error_message = models.TextField(blank=True)
    
    class Meta:
        indexes = [
            models.Index(fields=['user', 'status']),
            models.Index(fields=['uploaded_at']),
        ]
        ordering = ['-uploaded_at']

class ExpenseEntry(models.Model):
    """Model for storing extracted expense data."""
    
    class Category(models.TextChoices):
        TRAVEL = 'TRAVEL', _('Travel')
        MEALS = 'MEALS', _('Meals')
        SUPPLIES = 'SUPPLIES', _('Supplies')
        SERVICES = 'SERVICES', _('Services')
        OTHER = 'OTHER', _('Other')
    
    document = models.ForeignKey(
        ExpenseDocument,
        on_delete=models.CASCADE,
        related_name='entries'
    )
    amount = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        validators=[MinValueValidator(0)]
    )
    currency = models.CharField(max_length=3)  # ISO 4217 currency code
    date = models.DateField()
    vendor = models.CharField(max_length=255)
    category = models.CharField(
        max_length=20,
        choices=Category.choices,
        default=Category.OTHER
    )
    description = models.TextField(blank=True)
    tax_amount = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        validators=[MinValueValidator(0)],
        null=True,
        blank=True
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    confidence_score = models.FloatField(
        validators=[MinValueValidator(0.0)],
        help_text=_('AI confidence score for the extracted data')
    )
    
    class Meta:
        indexes = [
            models.Index(fields=['document', 'category']),
            models.Index(fields=['date']),
            models.Index(fields=['vendor']),
        ]
        ordering = ['-date']

class PolicyViolation(models.Model):
    """Model for tracking expense policy violations."""
    
    class Severity(models.TextChoices):
        LOW = 'LOW', _('Low')
        MEDIUM = 'MEDIUM', _('Medium')
        HIGH = 'HIGH', _('High')
    
    expense_entry = models.ForeignKey(
        ExpenseEntry,
        on_delete=models.CASCADE,
        related_name='policy_violations'
    )
    rule_name = models.CharField(max_length=100)
    description = models.TextField()
    severity = models.CharField(
        max_length=10,
        choices=Severity.choices,
        default=Severity.LOW
    )
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        indexes = [
            models.Index(fields=['expense_entry', 'severity']),
        ]
        ordering = ['-severity', '-created_at']

class AuditLog(models.Model):
    """Model for tracking all changes to expense documents and entries."""
    
    class Action(models.TextChoices):
        CREATE = 'CREATE', _('Create')
        UPDATE = 'UPDATE', _('Update')
        DELETE = 'DELETE', _('Delete')
        PROCESS = 'PROCESS', _('Process')
    
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    action = models.CharField(max_length=10, choices=Action.choices)
    model_name = models.CharField(max_length=50)
    object_id = models.PositiveIntegerField()
    changes = models.JSONField()
    timestamp = models.DateTimeField(auto_now_add=True)
    ip_address = models.GenericIPAddressField()
    user_agent = models.CharField(max_length=255)
    
    class Meta:
        indexes = [
            models.Index(fields=['user', 'action']),
            models.Index(fields=['timestamp']),
            models.Index(fields=['model_name', 'object_id']),
        ]
        ordering = ['-timestamp'] 