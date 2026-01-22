"""
CRM module views
"""
from rest_framework import viewsets, permissions
from .models import Lead, Opportunity
from .serializers import LeadSerializer, OpportunitySerializer


class LeadViewSet(viewsets.ModelViewSet):
    serializer_class = LeadSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def get_queryset(self):
        if hasattr(self.request, 'tenant') and self.request.tenant:
            return Lead.objects.filter(company=self.request.tenant)
        return Lead.objects.none()


class OpportunityViewSet(viewsets.ModelViewSet):
    serializer_class = OpportunitySerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def get_queryset(self):
        if hasattr(self.request, 'tenant') and self.request.tenant:
            return Opportunity.objects.filter(company=self.request.tenant)
        return Opportunity.objects.none()
