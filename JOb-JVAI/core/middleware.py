"""
Multi-tenancy middleware
Extracts company_id from JWT token and sets request.tenant
"""
from django.utils.deprecation import MiddlewareMixin
from django.core.cache import cache
from .models import Company, CompanyUser


class TenantMiddleware(MiddlewareMixin):
    """
    Middleware to handle multi-tenancy
    Extracts company_id from JWT token and sets request.tenant
    Caches the tenant information to reduce database hits
    """
    
    def process_request(self, request):
        """
        Extract company_id from JWT token and set request.tenant
        """
        request.tenant = None
        request.company_user = None
        
        # Try to get company_id from token
        if hasattr(request, 'user') and request.user.is_authenticated:
            user_id = str(request.user.id)
            cache_key = f"user_{user_id}_tenant"
            
            # Try to get from cache
            cached_data = cache.get(cache_key)
            if cached_data:
                request.tenant = cached_data.get('tenant')
                request.company_user = cached_data.get('company_user')
            else:
                # Get company from user's active company_user relationship
                company_user = request.user.company_users.select_related('company').filter(is_active=True).first()
                if company_user:
                    request.tenant = company_user.company
                    request.company_user = company_user
                    
                    # Cache for 1 hour
                    cache.set(cache_key, {
                        'tenant': request.tenant,
                        'company_user': request.company_user
                    }, 3600)
        
        return None
