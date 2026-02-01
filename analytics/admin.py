from django.contrib import admin
from .models import Dashboard, KPI


@admin.register(Dashboard)
class DashboardAdmin(admin.ModelAdmin):
    list_display = ['name', 'company', 'is_default', 'created_by', 'created_at']
    list_filter = ['is_default', 'company', 'created_at']
    search_fields = ['name', 'description', 'company__name']
    readonly_fields = ['id', 'created_at', 'updated_at']
    raw_id_fields = ['company', 'created_by']


@admin.register(KPI)
class KPIAdmin(admin.ModelAdmin):
    list_display = ['name', 'company', 'current_value', 'target_value', 'unit', 'is_active', 'created_at']
    list_filter = ['is_active', 'company', 'created_at']
    search_fields = ['name', 'description', 'company__name']
    readonly_fields = ['id', 'created_at', 'updated_at']
    raw_id_fields = ['company']
