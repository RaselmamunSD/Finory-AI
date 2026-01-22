"""
Legal module models
Legal Shield, Incidents, Reports, Blacklist
"""
import uuid
from django.db import models
from core.models import Company, User
from identity.models import Identity


class Incident(models.Model):
    """
    Incident model for legal/fraud incidents
    """
    CATEGORIES = [
        ('fraud', 'Fraud'),
        ('theft', 'Theft'),
        ('damage', 'Damage'),
        ('non_payment', 'Non Payment'),
        ('other', 'Other'),
    ]
    
    SEVERITY_LEVELS = [
        ('low', 'Low'),
        ('medium', 'Medium'),
        ('high', 'High'),
        ('critical', 'Critical'),
    ]
    
    STATUS_CHOICES = [
        ('reported', 'Reported'),
        ('investigating', 'Investigating'),
        ('resolved', 'Resolved'),
        ('closed', 'Closed'),
    ]
    
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    company = models.ForeignKey(Company, on_delete=models.CASCADE, related_name='incidents')
    reported_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='incidents_reported')
    accused_identity = models.ForeignKey(Identity, on_delete=models.SET_NULL, null=True, blank=True, related_name='incidents')
    
    category = models.CharField(max_length=20, choices=CATEGORIES)
    severity = models.CharField(max_length=20, choices=SEVERITY_LEVELS, null=True, blank=True, help_text="AI-calculated")
    description = models.TextField()
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='reported')
    
    # AI risk scoring
    legal_risk_score = models.IntegerField(null=True, blank=True, help_text="AI-calculated 0-100")
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        db_table = 'incidents'
        verbose_name = 'Incident'
        verbose_name_plural = 'Incidents'
        indexes = [
            models.Index(fields=['company', 'status']),
            models.Index(fields=['severity']),
        ]
    
    def __str__(self):
        return f"{self.category} - {self.company.name}"


class IncidentEvidence(models.Model):
    """
    Incident Evidence model
    """
    EVIDENCE_TYPES = [
        ('image', 'Image'),
        ('document', 'Document'),
        ('chat_log', 'Chat Log'),
        ('location', 'Location'),
    ]
    
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    incident = models.ForeignKey(Incident, on_delete=models.CASCADE, related_name='evidences')
    evidence_type = models.CharField(max_length=20, choices=EVIDENCE_TYPES)
    file_url = models.URLField()
    metadata = models.JSONField(default=dict, blank=True)
    
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        db_table = 'incident_evidences'
        verbose_name = 'Incident Evidence'
        verbose_name_plural = 'Incident Evidences'
    
    def __str__(self):
        return f"{self.incident.category} - {self.evidence_type}"


class LegalReport(models.Model):
    """
    Legal Report model
    """
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    incident = models.ForeignKey(Incident, on_delete=models.CASCADE, related_name='legal_reports')
    report_number = models.CharField(max_length=100, unique=True)
    pdf_url = models.URLField()
    hash_signature = models.CharField(max_length=255, help_text="For verification")
    qr_verification_code = models.CharField(max_length=100, unique=True)
    signed_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='legal_reports_signed')
    sent_to_authority_type = models.CharField(max_length=100, null=True, blank=True)
    sent_at = models.DateTimeField(null=True, blank=True)
    
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        db_table = 'legal_reports'
        verbose_name = 'Legal Report'
        verbose_name_plural = 'Legal Reports'
    
    def __str__(self):
        return f"{self.report_number} - {self.incident.category}"


class Blacklist(models.Model):
    """
    Blacklist model for high-risk identities/companies
    """
    STATUS_CHOICES = [
        ('active', 'Active'),
        ('lifted', 'Lifted'),
    ]
    
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    identity = models.ForeignKey(Identity, on_delete=models.CASCADE, null=True, blank=True, related_name='blacklist_entries')
    company = models.ForeignKey(Company, on_delete=models.CASCADE, null=True, blank=True, related_name='blacklist_entries')
    reason = models.TextField()
    source_incident = models.ForeignKey(Incident, on_delete=models.SET_NULL, null=True, blank=True, related_name='blacklist_entries')
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='active')
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        db_table = 'blacklist'
        verbose_name = 'Blacklist Entry'
        verbose_name_plural = 'Blacklist Entries'
        indexes = [
            models.Index(fields=['status']),
        ]
    
    def __str__(self):
        if self.identity:
            return f"{self.identity.full_name} - {self.status}"
        elif self.company:
            return f"{self.company.name} - {self.status}"
        return f"Blacklist Entry - {self.status}"
