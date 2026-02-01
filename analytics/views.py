"""
Analytics module views
"""
from rest_framework import viewsets, permissions
from .models import Dashboard, KPI
from .serializers import DashboardSerializer, KPISerializer


class DashboardViewSet(viewsets.ModelViewSet):
    serializer_class = DashboardSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def get_queryset(self):
        if hasattr(self.request, 'tenant') and self.request.tenant:
            return Dashboard.objects.filter(company=self.request.tenant)
        return Dashboard.objects.none()


class KPIViewSet(viewsets.ModelViewSet):
    serializer_class = KPISerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def get_queryset(self):
        if hasattr(self.request, 'tenant') and self.request.tenant:
            return KPI.objects.filter(company=self.request.tenant)
        return KPI.objects.none()
