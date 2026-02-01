"""
Payments module URLs
"""
from django.urls import path
from rest_framework.routers import SimpleRouter
from . import views

router = SimpleRouter()
router.register(r'gateways', views.PaymentGatewayViewSet, basename='payment-gateway')
router.register(r'payments', views.PaymentViewSet, basename='payment')

urlpatterns = router.urls
