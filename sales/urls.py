"""
Sales module URLs
"""
from django.urls import path
from rest_framework.routers import SimpleRouter
from . import views

router = SimpleRouter()
router.register(r'customers', views.CustomerViewSet, basename='customer')
router.register(r'invoices', views.InvoiceViewSet, basename='invoice')

urlpatterns = router.urls
