"""
Core models for Finory IA - Multi-tenancy, Users, Roles, Permissions, Audit
"""
import uuid
from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.utils import timezone
from django.core.validators import EmailValidator
import json


class UserManager(BaseUserManager):
    """Custom user manager"""
    
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError('The Email field must be set')
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user
    
    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        return self.create_user(email, password, **extra_fields)


class User(AbstractBaseUser, PermissionsMixin):
    """
    Custom User model with email as username
    Supports 2FA and biometric authentication
    """
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    email = models.EmailField(unique=True, validators=[EmailValidator()])
    full_name = models.CharField(max_length=255, null=True, blank=True)
    phone = models.CharField(max_length=20, unique=True, null=True, blank=True)
    
    # Email Verification
    is_email_verified = models.BooleanField(default=False)
    otp_code = models.CharField(max_length=4, null=True, blank=True)
    otp_expiry = models.DateTimeField(null=True, blank=True)
    
    # Password Reset
    password_reset_otp = models.CharField(max_length=6, null=True, blank=True)
    password_reset_otp_expiry = models.DateTimeField(null=True, blank=True)
    
    # Authentication
    is_2fa_enabled = models.BooleanField(default=False)
    two_factor_secret = models.CharField(max_length=32, null=True, blank=True)
    biometric_data = models.TextField(null=True, blank=True, help_text="Encrypted biometric template")
    
    # Status
    status = models.CharField(
        max_length=20,
        choices=[
            ('active', 'Active'),
            ('suspended', 'Suspended'),
            ('blocked', 'Blocked'),
        ],
        default='active'
    )
    
    # Django admin
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    
    # Timestamps
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    last_login = models.DateTimeField(null=True, blank=True)
    
    objects = UserManager()
    
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []
    
    class Meta:
        db_table = 'users'
        verbose_name = 'User'
        verbose_name_plural = 'Users'
        indexes = [
            models.Index(fields=['email']),
            models.Index(fields=['phone']),
            models.Index(fields=['status']),
        ]
    
    def __str__(self):
        return self.email

    def generate_otp(self):
        """Generate a 4-digit OTP and set expiry (10 minutes)"""
        import random
        self.otp_code = str(random.randint(1000, 9999))
        self.otp_expiry = timezone.now() + timezone.timedelta(minutes=10)
        self.save()
        return self.otp_code

    def generate_password_reset_otp(self):
        """Generate a 6-digit OTP for password reset and set expiry (15 minutes)"""
        import random
        self.password_reset_otp = str(random.randint(100000, 999999))
        self.password_reset_otp_expiry = timezone.now() + timezone.timedelta(minutes=15)
        self.save()
        return self.password_reset_otp


class Company(models.Model):
    """
    Multi-tenant company/tenant model
    Each company has isolated data
    """
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=255)
    tax_id = models.CharField(max_length=50, unique=True, null=True, blank=True)
    country = models.CharField(max_length=3, default='USA')
    currency = models.CharField(max_length=3, default='USD')
    timezone = models.CharField(max_length=50, default='UTC')
    
    # Legal representative
    legal_representative = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='companies_owned'
    )
    
    # AI Settings
    business_model = models.CharField(
        max_length=50,
        choices=[
            ('retail', 'Retail'),
            ('services', 'Services'),
            ('manufacturing', 'Manufacturing'),
            ('ecommerce', 'E-commerce'),
            ('other', 'Other'),
        ],
        null=True,
        blank=True
    )
    ai_autonomous_mode = models.BooleanField(default=False)
    
    # Settings (JSON field for flexible configuration)
    settings = models.JSONField(default=dict, blank=True)
    
    # Timestamps
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_active = models.BooleanField(default=True)
    
    class Meta:
        db_table = 'companies'
        verbose_name = 'Company'
        verbose_name_plural = 'Companies'
        indexes = [
            models.Index(fields=['tax_id']),
            models.Index(fields=['country']),
            models.Index(fields=['is_active']),
        ]
    
    def __str__(self):
        return self.name


class Branch(models.Model):
    """
    Branch/Sucursal model for multi-branch companies
    """
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    company = models.ForeignKey(Company, on_delete=models.CASCADE, related_name='branches')
    name = models.CharField(max_length=255)
    address = models.TextField(null=True, blank=True)
    manager = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='managed_branches'
    )
    is_active = models.BooleanField(default=True)
    settings = models.JSONField(default=dict, blank=True)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        db_table = 'branches'
        verbose_name = 'Branch'
        verbose_name_plural = 'Branches'
        indexes = [
            models.Index(fields=['company', 'is_active']),
        ]
    
    def __str__(self):
        return f"{self.company.name} - {self.name}"


class Role(models.Model):
    """
    Role model for RBAC
    """
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=100, unique=True)
    description = models.TextField(null=True, blank=True)
    is_system_role = models.BooleanField(default=False, help_text="System roles cannot be deleted")
    
    # Permissions (JSON field for granular permissions)
    permissions = models.JSONField(default=dict, blank=True)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        db_table = 'roles'
        verbose_name = 'Role'
        verbose_name_plural = 'Roles'
    
    def __str__(self):
        return self.name


class CompanyUser(models.Model):
    """
    Many-to-Many relationship between Companies and Users
    Links users to companies with specific roles and permissions
    """
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    company = models.ForeignKey(Company, on_delete=models.CASCADE, related_name='company_users')
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='company_users')
    role = models.ForeignKey(Role, on_delete=models.SET_NULL, null=True, related_name='company_users')
    branch = models.ForeignKey(
        Branch,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='company_users'
    )
    
    # Additional permissions override role permissions
    permissions = models.JSONField(default=dict, blank=True)
    
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        db_table = 'company_users'
        verbose_name = 'Company User'
        verbose_name_plural = 'Company Users'
        unique_together = [['company', 'user']]
        indexes = [
            models.Index(fields=['company', 'user']),
            models.Index(fields=['company', 'is_active']),
        ]
    
    def __str__(self):
        return f"{self.user.email} - {self.company.name}"


class AuditLog(models.Model):
    """
    Comprehensive audit log for all actions
    Tracks user actions, IP addresses, changes, etc.
    """
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='audit_logs')
    company = models.ForeignKey(Company, on_delete=models.CASCADE, null=True, related_name='audit_logs')
    
    # Action details
    action = models.CharField(
        max_length=20,
        choices=[
            ('create', 'Create'),
            ('update', 'Update'),
            ('delete', 'Delete'),
            ('view', 'View'),
            ('login', 'Login'),
            ('logout', 'Logout'),
            ('export', 'Export'),
            ('import', 'Import'),
        ]
    )
    entity_type = models.CharField(max_length=100, help_text="Model name")
    entity_id = models.UUIDField(null=True, blank=True)
    
    # Change tracking
    old_value = models.JSONField(null=True, blank=True)
    new_value = models.JSONField(null=True, blank=True)
    
    # Request metadata
    ip_address = models.GenericIPAddressField(null=True, blank=True)
    user_agent = models.TextField(null=True, blank=True)
    request_path = models.CharField(max_length=500, null=True, blank=True)
    request_method = models.CharField(max_length=10, null=True, blank=True)
    
    # Timestamp
    timestamp = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        db_table = 'audit_logs'
        verbose_name = 'Audit Log'
        verbose_name_plural = 'Audit Logs'
        indexes = [
            models.Index(fields=['user', 'timestamp']),
            models.Index(fields=['company', 'timestamp']),
            models.Index(fields=['entity_type', 'entity_id']),
            models.Index(fields=['timestamp']),
        ]
        ordering = ['-timestamp']
    
    def __str__(self):
        return f"{self.action} {self.entity_type} by {self.user.email if self.user else 'System'} at {self.timestamp}"
