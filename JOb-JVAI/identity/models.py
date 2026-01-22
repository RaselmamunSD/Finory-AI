"""
Identity module models
KYC/KYB Verification, Identity Shield
"""
import uuid
from django.db import models
from core.models import User


class Identity(models.Model):
    """
    Identity model for KYC/KYB verification
    """
    VERIFICATION_STATUS = [
        ('pending', 'Pending'),
        ('verified', 'Verified'),
        ('rejected', 'Rejected'),
        ('expired', 'Expired'),
    ]
    
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='identities')
    full_name = models.CharField(max_length=255)
    date_of_birth = models.DateField(null=True, blank=True)
    national_id_number = models.CharField(max_length=100, null=True, blank=True)
    country = models.CharField(max_length=3)
    
    # AI risk scoring
    risk_score = models.IntegerField(null=True, blank=True, help_text="AI-calculated risk score 0-100")
    verification_status = models.CharField(max_length=20, choices=VERIFICATION_STATUS, default='pending')
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        db_table = 'identities'
        verbose_name = 'Identity'
        verbose_name_plural = 'Identities'
        indexes = [
            models.Index(fields=['national_id_number']),
            models.Index(fields=['verification_status']),
        ]
    
    def __str__(self):
        return f"{self.full_name} - {self.verification_status}"


class IdentityDocument(models.Model):
    """
    Identity Document model
    """
    DOCUMENT_TYPES = [
        ('id_card', 'ID Card'),
        ('passport', 'Passport'),
        ('license', 'Driver License'),
        ('tax_cert', 'Tax Certificate'),
    ]
    
    VERIFICATION_STATUS = [
        ('pending', 'Pending'),
        ('verified', 'Verified'),
        ('rejected', 'Rejected'),
    ]
    
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    identity = models.ForeignKey(Identity, on_delete=models.CASCADE, related_name='documents')
    document_type = models.CharField(max_length=20, choices=DOCUMENT_TYPES)
    document_number = models.CharField(max_length=100)
    front_image_url = models.URLField()
    back_image_url = models.URLField(null=True, blank=True)
    
    # OCR data
    ocr_data = models.JSONField(default=dict, blank=True)
    
    verification_status = models.CharField(max_length=20, choices=VERIFICATION_STATUS, default='pending')
    verified_at = models.DateTimeField(null=True, blank=True)
    
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        db_table = 'identity_documents'
        verbose_name = 'Identity Document'
        verbose_name_plural = 'Identity Documents'
    
    def __str__(self):
        return f"{self.identity.full_name} - {self.document_type}"


class FaceVerification(models.Model):
    """
    Face Verification model for biometric authentication
    """
    VERIFICATION_STATUS = [
        ('pending', 'Pending'),
        ('verified', 'Verified'),
        ('rejected', 'Rejected'),
    ]
    
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    identity = models.ForeignKey(Identity, on_delete=models.CASCADE, related_name='face_verifications')
    selfie_image_url = models.URLField()
    match_score = models.IntegerField(null=True, blank=True, help_text="0-100")
    liveness_score = models.IntegerField(null=True, blank=True, help_text="0-100")
    verification_status = models.CharField(max_length=20, choices=VERIFICATION_STATUS, default='pending')
    verified_at = models.DateTimeField(null=True, blank=True)
    
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        db_table = 'face_verifications'
        verbose_name = 'Face Verification'
        verbose_name_plural = 'Face Verifications'
    
    def __str__(self):
        return f"{self.identity.full_name} - {self.verification_status}"
