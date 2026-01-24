"""
API URL Configuration
"""
from django.urls import path, include
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from .views import auth_views

urlpatterns = [
    # Authentication
    path('auth/login/', auth_views.LoginView.as_view(), name='login'),
    path('auth/register/', auth_views.RegisterView.as_view(), name='register'),
    path('auth/verify-email/', auth_views.VerifyEmailOTPView.as_view(), name='verify-email'),
    path('auth/resend-otp/', auth_views.ResendOTPView.as_view(), name='resend-otp'),
    path('auth/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('auth/verify-2fa/', auth_views.Verify2FAView.as_view(), name='verify-2fa'),
    path('auth/setup-2fa/', auth_views.Setup2FAView.as_view(), name='setup-2fa'),
    path('auth/enable-2fa/', auth_views.Enable2FAView.as_view(), name='enable-2fa'),
    path('auth/forgot-password/', auth_views.ForgotPasswordView.as_view(), name='forgot-password'),
    path('auth/reset-password/', auth_views.ResetPasswordView.as_view(), name='reset-password'),
    
    # Core
    path('companies/', include('core.urls')),
    path('users/', include('core.urls')),
    
    # Modules
    path('accounting/', include('accounting.urls')),
    path('sales/', include('sales.urls')),
    path('purchases/', include('purchases.urls')),
    path('inventory/', include('inventory.urls')),
    path('payments/', include('payments.urls')),
    path('banking/', include('banking.urls')),
    path('crm/', include('crm.urls')),
    path('hr/', include('hr.urls')),
    path('documents/', include('documents.urls')),
    path('tasks/', include('tasks.urls')),
    path('identity/', include('identity.urls')),
    path('legal/', include('legal.urls')),
    path('ai/', include('ai_engine.urls')),
    path('analytics/', include('analytics.urls')),
]
