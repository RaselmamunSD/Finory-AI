"""
AI Engine module URLs
"""
from django.urls import path
from rest_framework import routers
from . import views

router = routers.DefaultRouter()
router.register(r'predictions', views.AIPredictionViewSet, basename='ai-prediction')
router.register(r'recommendations', views.AIRecommendationViewSet, basename='ai-recommendation')
router.register(r'models', views.AIModelViewSet, basename='ai-model')

urlpatterns = router.urls
