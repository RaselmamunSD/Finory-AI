"""
Inventory module URLs
"""
from django.urls import path
from rest_framework import routers
from . import views

router = routers.DefaultRouter()
router.register(r'products', views.ProductViewSet, basename='product')
router.register(r'warehouses', views.WarehouseViewSet, basename='warehouse')
router.register(r'stock', views.StockViewSet, basename='stock')
router.register(r'stock-movements', views.StockMovementViewSet, basename='stock-movement')

urlpatterns = router.urls
