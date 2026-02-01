from django.contrib import admin
from .models import AIModel, AIPrediction, AIRecommendation, AIAuditLog


@admin.register(AIModel)
class AIModelAdmin(admin.ModelAdmin):
    list_display = ['name', 'model_type', 'version', 'is_active', 'created_at', 'updated_at']
    list_filter = ['model_type', 'is_active', 'created_at']
    search_fields = ['name', 'version']
    readonly_fields = ['id', 'created_at', 'updated_at']


@admin.register(AIPrediction)
class AIPredictionAdmin(admin.ModelAdmin):
    list_display = ['prediction_type', 'company', 'model', 'confidence_score', 'created_at']
    list_filter = ['prediction_type', 'company', 'model', 'created_at']
    search_fields = ['company__name', 'model__name']
    readonly_fields = ['id', 'created_at']
    raw_id_fields = ['company', 'model']
    date_hierarchy = 'created_at'


@admin.register(AIRecommendation)
class AIRecommendationAdmin(admin.ModelAdmin):
    list_display = ['title', 'recommendation_type', 'company', 'priority', 'status', 'created_at']
    list_filter = ['priority', 'status', 'recommendation_type', 'company', 'created_at']
    search_fields = ['title', 'description', 'company__name']
    readonly_fields = ['id', 'created_at', 'executed_at']
    raw_id_fields = ['company']
    date_hierarchy = 'created_at'


@admin.register(AIAuditLog)
class AIAuditLogAdmin(admin.ModelAdmin):
    list_display = ['action_type', 'entity_type', 'company', 'ai_model', 'anomaly_detected', 'severity', 'created_at']
    list_filter = ['anomaly_detected', 'severity', 'action_type', 'company', 'created_at']
    search_fields = ['action_type', 'entity_type', 'company__name']
    readonly_fields = ['id', 'created_at']
    raw_id_fields = ['company', 'ai_model']
    date_hierarchy = 'created_at'
