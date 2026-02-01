"""
Documents module URLs
"""
from django.urls import path
from rest_framework.routers import SimpleRouter
from . import views

router = SimpleRouter()
router.register(r'documents', views.DocumentViewSet, basename='document')
router.register(r'voice-commands', views.VoiceCommandViewSet, basename='voice-command')

urlpatterns = router.urls
