"""
Payments module URLs
"""
from django.urls import path
from rest_framework import routers
from . import views

router = routers.DefaultRouter()
router.register(r'gateways', views.PaymentGatewayViewSet, basename='payment-gateway')
router.register(r'payments', views.PaymentViewSet, basename='payment')

urlpatterns = router.urls
