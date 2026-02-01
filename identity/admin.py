from django.contrib import admin
from .models import Identity, IdentityDocument, FaceVerification


@admin.register(Identity)
class IdentityAdmin(admin.ModelAdmin):
    list_display = ['full_name', 'national_id_number', 'country', 'verification_status', 'risk_score', 'user', 'created_at']
    list_filter = ['verification_status', 'country', 'created_at']
    search_fields = ['full_name', 'national_id_number', 'user__email']
    readonly_fields = ['id', 'created_at', 'updated_at']
    raw_id_fields = ['user']


@admin.register(IdentityDocument)
class IdentityDocumentAdmin(admin.ModelAdmin):
    list_display = ['identity', 'document_type', 'document_number', 'verification_status', 'verified_at', 'created_at']
    list_filter = ['document_type', 'verification_status', 'created_at']
    search_fields = ['identity__full_name', 'document_number']
    readonly_fields = ['id', 'created_at', 'verified_at']
    raw_id_fields = ['identity']


@admin.register(FaceVerification)
class FaceVerificationAdmin(admin.ModelAdmin):
    list_display = ['identity', 'match_score', 'liveness_score', 'verification_status', 'verified_at', 'created_at']
    list_filter = ['verification_status', 'created_at']
    search_fields = ['identity__full_name']
    readonly_fields = ['id', 'created_at', 'verified_at']
    raw_id_fields = ['identity']
