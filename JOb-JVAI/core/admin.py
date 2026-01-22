from django.contrib import admin
from .models import User, Company, Branch, Role, CompanyUser, AuditLog


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ['email', 'phone', 'status', 'is_2fa_enabled', 'created_at']
    list_filter = ['status', 'is_2fa_enabled', 'created_at']
    search_fields = ['email', 'phone']
    readonly_fields = ['id', 'created_at', 'updated_at', 'last_login']


@admin.register(Company)
class CompanyAdmin(admin.ModelAdmin):
    list_display = ['name', 'tax_id', 'country', 'currency', 'ai_autonomous_mode', 'is_active']
    list_filter = ['country', 'business_model', 'ai_autonomous_mode', 'is_active']
    search_fields = ['name', 'tax_id']
    readonly_fields = ['id', 'created_at', 'updated_at']


@admin.register(Branch)
class BranchAdmin(admin.ModelAdmin):
    list_display = ['name', 'company', 'manager', 'is_active']
    list_filter = ['is_active', 'company']
    search_fields = ['name', 'company__name']
    readonly_fields = ['id', 'created_at', 'updated_at']


@admin.register(Role)
class RoleAdmin(admin.ModelAdmin):
    list_display = ['name', 'is_system_role', 'created_at']
    list_filter = ['is_system_role']
    search_fields = ['name']
    readonly_fields = ['id', 'created_at', 'updated_at']


@admin.register(CompanyUser)
class CompanyUserAdmin(admin.ModelAdmin):
    list_display = ['user', 'company', 'role', 'branch', 'is_active']
    list_filter = ['is_active', 'role', 'company']
    search_fields = ['user__email', 'company__name']
    readonly_fields = ['id', 'created_at', 'updated_at']


@admin.register(AuditLog)
class AuditLogAdmin(admin.ModelAdmin):
    list_display = ['action', 'entity_type', 'user', 'company', 'timestamp']
    list_filter = ['action', 'entity_type', 'timestamp']
    search_fields = ['user__email', 'entity_type', 'ip_address']
    readonly_fields = ['id', 'timestamp']
    date_hierarchy = 'timestamp'
