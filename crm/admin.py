from django.contrib import admin
from .models import Lead, Opportunity


@admin.register(Lead)
class LeadAdmin(admin.ModelAdmin):
    list_display = ['name', 'email', 'phone', 'company_name', 'company', 'status', 'source', 'assigned_to', 'created_at']
    list_filter = ['status', 'source', 'company', 'created_at']
    search_fields = ['name', 'email', 'phone', 'company_name', 'company__name']
    readonly_fields = ['id', 'created_at', 'updated_at']
    raw_id_fields = ['company', 'created_by', 'assigned_to']


@admin.register(Opportunity)
class OpportunityAdmin(admin.ModelAdmin):
    list_display = ['name', 'company', 'stage', 'expected_value', 'probability', 'expected_close_date', 'assigned_to', 'created_at']
    list_filter = ['stage', 'company', 'expected_close_date', 'created_at']
    search_fields = ['name', 'company__name']
    readonly_fields = ['id', 'created_at', 'updated_at']
    raw_id_fields = ['company', 'lead', 'customer', 'assigned_to']
    date_hierarchy = 'expected_close_date'
