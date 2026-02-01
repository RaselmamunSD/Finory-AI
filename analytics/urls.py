"""
Analytics module URLs
"""
from django.urls import path
from rest_framework.routers import SimpleRouter
from . import views

router = SimpleRouter()
router.register(r'dashboards', views.DashboardViewSet, basename='dashboard')
router.register(r'kpis', views.KPIViewSet, basename='kpi')

urlpatterns = router.urls
