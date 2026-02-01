"""
Tasks module models
Workflow Automation, Tasks, WhatsApp Integration
"""
import uuid
from django.db import models
from core.models import Company, User


class Task(models.Model):
    """
    Task model with AI-recommended priority and due dates
    """
    PRIORITY_LEVELS = [
        ('low', 'Low'),
        ('medium', 'Medium'),
        ('high', 'High'),
        ('urgent', 'Urgent'),
    ]
    
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('in_progress', 'In Progress'),
        ('completed', 'Completed'),
        ('cancelled', 'Cancelled'),
    ]
    
    SOURCE_TYPES = [
        ('manual', 'Manual'),
        ('whatsapp', 'WhatsApp'),
        ('document', 'Document'),
        ('ai_generated', 'AI Generated'),
    ]
    
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    company = models.ForeignKey(Company, on_delete=models.CASCADE, related_name='tasks')
    created_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='tasks_created')
    assigned_to = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='tasks_assigned')
    
    title = models.CharField(max_length=255)
    description = models.TextField(null=True, blank=True)
    source = models.CharField(max_length=20, choices=SOURCE_TYPES, default='manual')
    
    # AI-recommended fields
    priority = models.CharField(max_length=20, choices=PRIORITY_LEVELS, default='medium')
    due_date = models.DateTimeField(null=True, blank=True)
    
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    ai_context = models.JSONField(default=dict, blank=True)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    completed_at = models.DateTimeField(null=True, blank=True)
    
    class Meta:
        db_table = 'tasks'
        verbose_name = 'Task'
        verbose_name_plural = 'Tasks'
        indexes = [
            models.Index(fields=['company', 'status', 'priority']),
            models.Index(fields=['assigned_to', 'status']),
        ]
        ordering = ['-priority', 'due_date']
    
    def __str__(self):
        return f"{self.title} - {self.status}"
