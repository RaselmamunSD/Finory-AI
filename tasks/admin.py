from django.contrib import admin
from .models import Task


@admin.register(Task)
class TaskAdmin(admin.ModelAdmin):
    list_display = ['title', 'company', 'status', 'priority', 'source', 'assigned_to', 'due_date', 'created_at']
    list_filter = ['status', 'priority', 'source', 'company', 'created_at']
    search_fields = ['title', 'description', 'company__name']
    readonly_fields = ['id', 'created_at', 'updated_at', 'completed_at']
    raw_id_fields = ['company', 'created_by', 'assigned_to']
    date_hierarchy = 'due_date'
