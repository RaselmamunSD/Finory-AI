"""
Tasks module URLs
"""
from django.urls import path
from rest_framework.routers import SimpleRouter
from . import views

router = SimpleRouter()
router.register(r'tasks', views.TaskViewSet, basename='task')

urlpatterns = router.urls
