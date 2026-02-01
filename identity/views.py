"""
Identity module views
"""
from rest_framework import viewsets, permissions
from .models import Identity, FaceVerification
from .serializers import IdentitySerializer, FaceVerificationSerializer


class IdentityViewSet(viewsets.ModelViewSet):
    serializer_class = IdentitySerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def get_queryset(self):
        return Identity.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class FaceVerificationViewSet(viewsets.ModelViewSet):
    serializer_class = FaceVerificationSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def get_queryset(self):
        return FaceVerification.objects.filter(identity__user=self.request.user)
