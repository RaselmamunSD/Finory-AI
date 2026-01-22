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
    path('auth/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('auth/verify-2fa/', auth_views.Verify2FAView.as_view(), name='verify-2fa'),
    
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
