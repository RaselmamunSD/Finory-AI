"""
Analytics module URLs
"""
from django.urls import path
from rest_framework import routers
from . import views

router = routers.DefaultRouter()
router.register(r'dashboards', views.DashboardViewSet, basename='dashboard')
router.register(r'kpis', views.KPIViewSet, basename='kpi')

urlpatterns = router.urls
