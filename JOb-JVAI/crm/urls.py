"""
CRM module URLs
"""
from django.urls import path
from rest_framework import routers
from . import views

router = routers.DefaultRouter()
router.register(r'leads', views.LeadViewSet, basename='lead')
router.register(r'opportunities', views.OpportunityViewSet, basename='opportunity')

urlpatterns = router.urls
