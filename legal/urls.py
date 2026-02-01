"""
Legal module URLs
"""
from django.urls import path
from rest_framework.routers import SimpleRouter
from . import views

router = SimpleRouter()
router.register(r'incidents', views.IncidentViewSet, basename='incident')
router.register(r'legal-reports', views.LegalReportViewSet, basename='legal-report')
router.register(r'blacklist', views.BlacklistViewSet, basename='blacklist')

urlpatterns = router.urls
