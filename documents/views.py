"""
Documents module views
"""
from rest_framework import viewsets, permissions
from .models import Document, VoiceCommand
from .serializers import DocumentSerializer, VoiceCommandSerializer


class DocumentViewSet(viewsets.ModelViewSet):
    serializer_class = DocumentSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def get_queryset(self):
        if hasattr(self.request, 'tenant') and self.request.tenant:
            return Document.objects.filter(company=self.request.tenant)
        return Document.objects.none()


class VoiceCommandViewSet(viewsets.ModelViewSet):
    serializer_class = VoiceCommandSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def get_queryset(self):
        if hasattr(self.request, 'tenant') and self.request.tenant:
            return VoiceCommand.objects.filter(company=self.request.tenant)
        return VoiceCommand.objects.none()
