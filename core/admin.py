from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.forms import UserChangeForm as BaseUserChangeForm, UserCreationForm as BaseUserCreationForm
from .models import User, Company, Branch, Role, CompanyUser, AuditLog


class UserCreationForm(BaseUserCreationForm):
    class Meta(BaseUserCreationForm.Meta):
        model = User
        fields = ('email',)


class UserChangeForm(BaseUserChangeForm):
    class Meta(BaseUserChangeForm.Meta):
        model = User
        fields = '__all__'


@admin.register(User)
class UserAdmin(BaseUserAdmin):
    form = UserChangeForm
    add_form = UserCreationForm
    list_display = ['email', 'full_name', 'phone', 'status', 'is_staff', 'is_2fa_enabled', 'created_at']
    list_filter = ['status', 'is_staff', 'is_2fa_enabled', 'created_at']
    search_fields = ['email', 'phone', 'full_name']
    ordering = ['email']
    readonly_fields = ['id', 'created_at', 'updated_at', 'last_login']

    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        ('Personal', {'fields': ('full_name', 'phone')}),
        ('Permissions', {'fields': ('is_staff', 'is_active', 'is_superuser', 'groups', 'user_permissions')}),
        ('Status', {'fields': ('status', 'is_email_verified', 'is_2fa_enabled')}),
        ('Important dates', {'fields': ('last_login', 'created_at', 'updated_at')}),
    )

    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'password1', 'password2'),
        }),
    )


@admin.register(Company)
class CompanyAdmin(admin.ModelAdmin):
    list_display = ['name', 'tax_id', 'country', 'currency', 'ai_autonomous_mode', 'is_active', 'created_at']
    list_filter = ['country', 'business_model', 'ai_autonomous_mode', 'is_active', 'created_at']
    search_fields = ['name', 'tax_id']
    readonly_fields = ['id', 'created_at', 'updated_at']
    raw_id_fields = ['legal_representative']


@admin.register(Branch)
class BranchAdmin(admin.ModelAdmin):
    list_display = ['name', 'company', 'manager', 'is_active', 'created_at']
    list_filter = ['is_active', 'company', 'created_at']
    search_fields = ['name', 'company__name']
    readonly_fields = ['id', 'created_at', 'updated_at']
    raw_id_fields = ['company', 'manager']


@admin.register(Role)
class RoleAdmin(admin.ModelAdmin):
    list_display = ['name', 'is_system_role', 'created_at']
    list_filter = ['is_system_role', 'created_at']
    search_fields = ['name', 'description']
    readonly_fields = ['id', 'created_at', 'updated_at']


@admin.register(CompanyUser)
class CompanyUserAdmin(admin.ModelAdmin):
    list_display = ['user', 'company', 'role', 'branch', 'is_active', 'created_at']
    list_filter = ['is_active', 'role', 'company', 'created_at']
    search_fields = ['user__email', 'company__name']
    readonly_fields = ['id', 'created_at', 'updated_at']
    raw_id_fields = ['user', 'company', 'role', 'branch']


@admin.register(AuditLog)
class AuditLogAdmin(admin.ModelAdmin):
    list_display = ['action', 'entity_type', 'user', 'company', 'timestamp']
    list_filter = ['action', 'entity_type', 'timestamp']
    search_fields = ['user__email', 'entity_type', 'ip_address', 'request_path']
    readonly_fields = ['id', 'timestamp']
    raw_id_fields = ['user', 'company']
    date_hierarchy = 'timestamp'
