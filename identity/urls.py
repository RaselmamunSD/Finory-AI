"""
Identity module URLs
"""
from django.urls import path
from rest_framework.routers import SimpleRouter
from . import views

router = SimpleRouter()
router.register(r'identities', views.IdentityViewSet, basename='identity')
router.register(r'verifications', views.FaceVerificationViewSet, basename='face-verification')

urlpatterns = router.urls
