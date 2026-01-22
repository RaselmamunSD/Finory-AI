"""
Legal module views
"""
from rest_framework import viewsets, permissions
from .models import Incident, LegalReport, Blacklist
from .serializers import IncidentSerializer, LegalReportSerializer, BlacklistSerializer


class IncidentViewSet(viewsets.ModelViewSet):
    serializer_class = IncidentSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def get_queryset(self):
        if hasattr(self.request, 'tenant') and self.request.tenant:
            return Incident.objects.filter(company=self.request.tenant)
        return Incident.objects.none()


class LegalReportViewSet(viewsets.ModelViewSet):
    serializer_class = LegalReportSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def get_queryset(self):
        if hasattr(self.request, 'tenant') and self.request.tenant:
            return LegalReport.objects.filter(incident__company=self.request.tenant)
        return LegalReport.objects.none()


class BlacklistViewSet(viewsets.ModelViewSet):
    serializer_class = BlacklistSerializer
    permission_classes = [permissions.IsAuthenticated]
    queryset = Blacklist.objects.all()
