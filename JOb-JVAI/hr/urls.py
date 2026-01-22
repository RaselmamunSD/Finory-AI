"""
HR module URLs
"""
from django.urls import path
from rest_framework import routers
from . import views

router = routers.DefaultRouter()
router.register(r'employees', views.EmployeeViewSet, basename='employee')
router.register(r'payrolls', views.PayrollViewSet, basename='payroll')
router.register(r'contracts', views.ContractViewSet, basename='contract')

urlpatterns = router.urls
