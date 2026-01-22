"""
Tasks module URLs
"""
from django.urls import path
from rest_framework import routers
from . import views

router = routers.DefaultRouter()
router.register(r'tasks', views.TaskViewSet, basename='task')

urlpatterns = router.urls
