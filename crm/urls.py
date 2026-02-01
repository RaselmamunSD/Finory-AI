"""
CRM module URLs
"""
from django.urls import path
from rest_framework.routers import SimpleRouter
from . import views

router = SimpleRouter()
router.register(r'leads', views.LeadViewSet, basename='lead')
router.register(r'opportunities', views.OpportunityViewSet, basename='opportunity')

urlpatterns = router.urls
