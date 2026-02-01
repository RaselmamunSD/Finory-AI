from django.contrib import admin
from .models import Document, VoiceCommand


@admin.register(Document)
class DocumentAdmin(admin.ModelAdmin):
    list_display = ['file_name', 'file_type', 'company', 'ai_classification', 'status', 'uploaded_by', 'created_at']
    list_filter = ['file_type', 'ai_classification', 'status', 'company', 'created_at']
    search_fields = ['file_name', 'company__name']
    readonly_fields = ['id', 'created_at', 'updated_at']
    raw_id_fields = ['company', 'uploaded_by']


@admin.register(VoiceCommand)
class VoiceCommandAdmin(admin.ModelAdmin):
    list_display = ['user', 'company', 'detected_intent', 'created_at']
    list_filter = ['company', 'detected_intent', 'created_at']
    search_fields = ['transcription', 'detected_intent', 'user__email', 'company__name']
    readonly_fields = ['id', 'created_at']
    raw_id_fields = ['company', 'user']
    date_hierarchy = 'created_at'
