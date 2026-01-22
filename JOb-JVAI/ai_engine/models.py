"""
AI Engine module models
AI Models, Predictions, Recommendations, Audit Logs
"""
import uuid
from django.db import models
from django.core.validators import MinValueValidator
from core.models import Company, User


class AIModel(models.Model):
    """
    AI Model registry
    """
    MODEL_TYPES = [
        ('accounting_ai', 'Accounting AI'),
        ('inventory_ai', 'Inventory AI'),
        ('fraud_ai', 'Fraud AI'),
        ('cash_flow_ai', 'Cash Flow AI'),
        ('sales_ai', 'Sales AI'),
        ('decision_ai', 'Decision AI'),
    ]
    
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=100)
    model_type = models.CharField(max_length=50, choices=MODEL_TYPES)
    version = models.CharField(max_length=20)
    is_active = models.BooleanField(default=True)
    configuration = models.JSONField(default=dict, blank=True)
    performance_metrics = models.JSONField(default=dict, blank=True)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        db_table = 'ai_models'
        verbose_name = 'AI Model'
        verbose_name_plural = 'AI Models'
        unique_together = [['name', 'version']]
    
    def __str__(self):
        return f"{self.name} v{self.version}"


class AIPrediction(models.Model):
    """
    AI Predictions - Cash flow, sales forecast, demand, fraud
    """
    PREDICTION_TYPES = [
        ('cash_flow', 'Cash Flow'),
        ('sales_forecast', 'Sales Forecast'),
        ('demand', 'Demand'),
        ('fraud', 'Fraud'),
        ('payment', 'Payment'),
    ]
    
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    company = models.ForeignKey(Company, on_delete=models.CASCADE, related_name='ai_predictions')
    model = models.ForeignKey(AIModel, on_delete=models.PROTECT, related_name='predictions')
    prediction_type = models.CharField(max_length=50, choices=PREDICTION_TYPES)
    input_data = models.JSONField(default=dict)
    prediction = models.JSONField(default=dict)
    confidence_score = models.IntegerField(validators=[MinValueValidator(0)], help_text="0-100")
    actual_outcome = models.JSONField(null=True, blank=True, help_text="For model learning")
    
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        db_table = 'ai_predictions'
        verbose_name = 'AI Prediction'
        verbose_name_plural = 'AI Predictions'
        indexes = [
            models.Index(fields=['company', 'prediction_type', 'created_at']),
        ]
        ordering = ['-created_at']
    
    def __str__(self):
        return f"{self.prediction_type} - {self.company.name} - {self.confidence_score}%"


class AIRecommendation(models.Model):
    """
    AI Recommendations - Actionable insights and suggestions
    """
    PRIORITY_LEVELS = [
        ('low', 'Low'),
        ('medium', 'Medium'),
        ('high', 'High'),
        ('critical', 'Critical'),
    ]
    
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('accepted', 'Accepted'),
        ('rejected', 'Rejected'),
        ('executed', 'Executed'),
    ]
    
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    company = models.ForeignKey(Company, on_delete=models.CASCADE, related_name='ai_recommendations')
    recommendation_type = models.CharField(max_length=100)
    priority = models.CharField(max_length=20, choices=PRIORITY_LEVELS, default='medium')
    title = models.CharField(max_length=255)
    description = models.TextField()
    impact_analysis = models.JSONField(default=dict, blank=True)
    suggested_actions = models.JSONField(default=list, blank=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    
    created_at = models.DateTimeField(auto_now_add=True)
    executed_at = models.DateTimeField(null=True, blank=True)
    
    class Meta:
        db_table = 'ai_recommendations'
        verbose_name = 'AI Recommendation'
        verbose_name_plural = 'AI Recommendations'
        indexes = [
            models.Index(fields=['company', 'status', 'priority']),
        ]
        ordering = ['-priority', '-created_at']
    
    def __str__(self):
        return f"{self.title} - {self.priority}"


class AIAuditLog(models.Model):
    """
    AI Audit Log - Tracks AI actions and anomalies
    """
    SEVERITY_LEVELS = [
        ('low', 'Low'),
        ('medium', 'Medium'),
        ('high', 'High'),
        ('critical', 'Critical'),
    ]
    
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    company = models.ForeignKey(Company, on_delete=models.CASCADE, related_name='ai_audit_logs')
    ai_model = models.ForeignKey(AIModel, on_delete=models.PROTECT, related_name='audit_logs')
    action_type = models.CharField(max_length=100)
    entity_type = models.CharField(max_length=100)
    entity_id = models.UUIDField(null=True, blank=True)
    anomaly_detected = models.BooleanField(default=False)
    severity = models.CharField(max_length=20, choices=SEVERITY_LEVELS, null=True, blank=True)
    details = models.JSONField(default=dict, blank=True)
    
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        db_table = 'ai_audit_logs'
        verbose_name = 'AI Audit Log'
        verbose_name_plural = 'AI Audit Logs'
        indexes = [
            models.Index(fields=['company', 'created_at']),
            models.Index(fields=['anomaly_detected', 'severity']),
        ]
        ordering = ['-created_at']
    
    def __str__(self):
        return f"{self.action_type} - {self.company.name} - {self.created_at}"
