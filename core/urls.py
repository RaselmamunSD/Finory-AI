"""
Core module URLs
"""
from django.urls import path
from rest_framework import routers
from . import views

router = routers.DefaultRouter()
router.register(r'companies', views.CompanyViewSet, basename='company')
router.register(r'users', views.UserViewSet, basename='user')
router.register(r'branches', views.BranchViewSet, basename='branch')
router.register(r'roles', views.RoleViewSet, basename='role')
router.register(r'company-users', views.CompanyUserViewSet, basename='company-user')

urlpatterns = router.urls
