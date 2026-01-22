"""
Sales module views
"""
from rest_framework import viewsets, permissions
from .models import Customer, Invoice
from .serializers import CustomerSerializer, InvoiceSerializer


class CustomerViewSet(viewsets.ModelViewSet):
    serializer_class = CustomerSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def get_queryset(self):
        if hasattr(self.request, 'tenant') and self.request.tenant:
            return Customer.objects.filter(company=self.request.tenant)
        return Customer.objects.none()


class InvoiceViewSet(viewsets.ModelViewSet):
    serializer_class = InvoiceSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def get_queryset(self):
        if hasattr(self.request, 'tenant') and self.request.tenant:
            return Invoice.objects.filter(company=self.request.tenant)
        return Invoice.objects.none()
