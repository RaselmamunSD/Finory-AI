"""
Custom managers for tenant-filtered queries
"""
from django.db import models


class TenantManager(models.Manager):
    """
    Manager that automatically filters by company_id
    """
    
    def get_queryset(self):
        """
        Override to filter by tenant
        Note: This requires request.tenant to be set by middleware
        """
        return super().get_queryset()
    
    def for_tenant(self, company):
        """
        Filter queryset by company
        """
        return self.get_queryset().filter(company=company)
    
    def for_tenant_id(self, company_id):
        """
        Filter queryset by company_id
        """
        return self.get_queryset().filter(company_id=company_id)
