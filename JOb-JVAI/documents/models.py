"""
Documents module models
OCR, Document Intelligence, Classification
"""
import uuid
from django.db import models
from core.models import Company, User


class Document(models.Model):
    """
    Document model with OCR and AI classification
    """
    FILE_TYPES = [
        ('pdf', 'PDF'),
        ('image', 'Image'),
        ('excel', 'Excel'),
        ('audio', 'Audio'),
        ('other', 'Other'),
    ]
    
    CLASSIFICATION_TYPES = [
        ('invoice', 'Invoice'),
        ('contract', 'Contract'),
        ('receipt', 'Receipt'),
        ('id_card', 'ID Card'),
        ('tax_cert', 'Tax Certificate'),
        ('other', 'Other'),
    ]
    
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('processed', 'Processed'),
        ('classified', 'Classified'),
    ]
    
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    company = models.ForeignKey(Company, on_delete=models.CASCADE, related_name='documents')
    uploaded_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='documents_uploaded')
    
    file_name = models.CharField(max_length=255)
    file_type = models.CharField(max_length=20, choices=FILE_TYPES)
    file_url = models.URLField()
    
    # OCR extracted data
    ocr_extracted_data = models.JSONField(default=dict, blank=True)
    
    # AI classification
    ai_classification = models.CharField(max_length=50, choices=CLASSIFICATION_TYPES, null=True, blank=True)
    
    # Linked entity
    linked_entity_type = models.CharField(max_length=100, null=True, blank=True)
    linked_entity_id = models.UUIDField(null=True, blank=True)
    
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        db_table = 'documents'
        verbose_name = 'Document'
        verbose_name_plural = 'Documents'
        indexes = [
            models.Index(fields=['company', 'status']),
            models.Index(fields=['linked_entity_type', 'linked_entity_id']),
        ]
    
    def __str__(self):
        return f"{self.file_name} - {self.company.name}"


class VoiceCommand(models.Model):
    """
    Voice Command model for voice-based interactions
    """
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    company = models.ForeignKey(Company, on_delete=models.CASCADE, related_name='voice_commands')
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='voice_commands')
    
    audio_url = models.URLField()
    transcription = models.TextField()
    detected_intent = models.CharField(max_length=100, null=True, blank=True)
    extracted_entities = models.JSONField(default=dict, blank=True)
    executed_action = models.JSONField(default=dict, blank=True)
    
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        db_table = 'voice_commands'
        verbose_name = 'Voice Command'
        verbose_name_plural = 'Voice Commands'
        indexes = [
            models.Index(fields=['company', 'created_at']),
        ]
    
    def __str__(self):
        return f"{self.user.email if self.user else 'System'} - {self.detected_intent}"
