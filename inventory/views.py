"""
Inventory module views
"""
from rest_framework import viewsets, permissions
from .models import Product, Warehouse, Stock, StockMovement
from .serializers import ProductSerializer, WarehouseSerializer, StockSerializer, StockMovementSerializer


class ProductViewSet(viewsets.ModelViewSet):
    serializer_class = ProductSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def get_queryset(self):
        if hasattr(self.request, 'tenant') and self.request.tenant:
            return Product.objects.filter(company=self.request.tenant)
        return Product.objects.none()


class WarehouseViewSet(viewsets.ModelViewSet):
    serializer_class = WarehouseSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def get_queryset(self):
        if hasattr(self.request, 'tenant') and self.request.tenant:
            return Warehouse.objects.filter(company=self.request.tenant)
        return Warehouse.objects.none()


class StockViewSet(viewsets.ModelViewSet):
    serializer_class = StockSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def get_queryset(self):
        if hasattr(self.request, 'tenant') and self.request.tenant:
            return Stock.objects.filter(product__company=self.request.tenant)
        return Stock.objects.none()


class StockMovementViewSet(viewsets.ModelViewSet):
    serializer_class = StockMovementSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def get_queryset(self):
        if hasattr(self.request, 'tenant') and self.request.tenant:
            return StockMovement.objects.filter(product__company=self.request.tenant)
        return StockMovement.objects.none()
