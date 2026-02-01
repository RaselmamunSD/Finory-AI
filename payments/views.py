"""
Payments module views
"""
from rest_framework import viewsets, permissions
from .models import PaymentGateway, Payment
from .serializers import PaymentGatewaySerializer, PaymentSerializer


class PaymentGatewayViewSet(viewsets.ModelViewSet):
    serializer_class = PaymentGatewaySerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def get_queryset(self):
        if hasattr(self.request, 'tenant') and self.request.tenant:
            return PaymentGateway.objects.filter(company=self.request.tenant)
        return PaymentGateway.objects.none()


class PaymentViewSet(viewsets.ModelViewSet):
    serializer_class = PaymentSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def get_queryset(self):
        if hasattr(self.request, 'tenant') and self.request.tenant:
            return Payment.objects.filter(company=self.request.tenant)
        return Payment.objects.none()
