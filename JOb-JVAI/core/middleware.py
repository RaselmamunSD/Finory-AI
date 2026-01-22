"""
Multi-tenancy middleware
Extracts company_id from JWT token and sets request.tenant
"""
from django.utils.deprecation import MiddlewareMixin
from .models import Company


class TenantMiddleware(MiddlewareMixin):
    """
    Middleware to handle multi-tenancy
    Extracts company_id from JWT token and sets request.tenant
    """
    
    def process_request(self, request):
        """
        Extract company_id from JWT token and set request.tenant
        """
        request.tenant = None
        
        # Try to get company_id from token
        if hasattr(request, 'user') and request.user.is_authenticated:
            # Get company from user's active company_user relationship
            company_user = request.user.company_users.filter(is_active=True).first()
            if company_user:
                request.tenant = company_user.company
                request.company_user = company_user
        
        return None
