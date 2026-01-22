"""
Identity module URLs
"""
from django.urls import path
from rest_framework import routers
from . import views

router = routers.DefaultRouter()
router.register(r'identities', views.IdentityViewSet, basename='identity')
router.register(r'verifications', views.FaceVerificationViewSet, basename='face-verification')

urlpatterns = router.urls
