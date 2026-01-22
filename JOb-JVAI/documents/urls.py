"""
Documents module URLs
"""
from django.urls import path
from rest_framework import routers
from . import views

router = routers.DefaultRouter()
router.register(r'documents', views.DocumentViewSet, basename='document')
router.register(r'voice-commands', views.VoiceCommandViewSet, basename='voice-command')

urlpatterns = router.urls
