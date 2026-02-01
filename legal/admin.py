from django.contrib import admin
from .models import Incident, IncidentEvidence, LegalReport, Blacklist


class IncidentEvidenceInline(admin.TabularInline):
    model = IncidentEvidence
    extra = 1
    fields = ['evidence_type', 'file_url', 'metadata']
    readonly_fields = []


@admin.register(Incident)
class IncidentAdmin(admin.ModelAdmin):
    list_display = ['category', 'severity', 'company', 'status', 'legal_risk_score', 'reported_by', 'accused_identity', 'created_at']
    list_filter = ['category', 'severity', 'status', 'company', 'created_at']
    search_fields = ['description', 'company__name']
    readonly_fields = ['id', 'created_at', 'updated_at']
    raw_id_fields = ['company', 'reported_by', 'accused_identity']
    inlines = [IncidentEvidenceInline]
    date_hierarchy = 'created_at'


@admin.register(IncidentEvidence)
class IncidentEvidenceAdmin(admin.ModelAdmin):
    list_display = ['incident', 'evidence_type', 'created_at']
    list_filter = ['evidence_type', 'incident__category', 'created_at']
    search_fields = ['incident__description']
    readonly_fields = ['id', 'created_at']
    raw_id_fields = ['incident']


@admin.register(LegalReport)
class LegalReportAdmin(admin.ModelAdmin):
    list_display = ['report_number', 'incident', 'signed_by', 'sent_to_authority_type', 'sent_at', 'created_at']
    list_filter = ['sent_to_authority_type', 'created_at']
    search_fields = ['report_number', 'qr_verification_code', 'incident__category']
    readonly_fields = ['id', 'created_at']
    raw_id_fields = ['incident', 'signed_by']
    date_hierarchy = 'created_at'


@admin.register(Blacklist)
class BlacklistAdmin(admin.ModelAdmin):
    list_display = ['identity', 'company', 'status', 'source_incident', 'created_at']
    list_filter = ['status', 'created_at']
    search_fields = ['identity__full_name', 'company__name', 'reason']
    readonly_fields = ['id', 'created_at', 'updated_at']
    raw_id_fields = ['identity', 'company', 'source_incident']
