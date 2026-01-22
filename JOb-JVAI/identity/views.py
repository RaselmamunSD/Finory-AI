"""
Identity module views
"""
from rest_framework import viewsets, permissions
from .models import Identity, FaceVerification
from .serializers import IdentitySerializer, FaceVerificationSerializer


class IdentityViewSet(viewsets.ModelViewSet):
    serializer_class = IdentitySerializer
    permission_classes = [permissions.IsAuthenticated]
    queryset = Identity.objects.all()


class FaceVerificationViewSet(viewsets.ModelViewSet):
    serializer_class = FaceVerificationSerializer
    permission_classes = [permissions.IsAuthenticated]
    queryset = FaceVerification.objects.all()
