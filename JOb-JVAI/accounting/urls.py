"""
Accounting module URLs
"""
from django.urls import path
from rest_framework import routers
from . import views

router = routers.DefaultRouter()
router.register(r'accounts', views.ChartOfAccountsViewSet, basename='account')
router.register(r'journal-entries', views.JournalEntryViewSet, basename='journal-entry')
router.register(r'financial-statements', views.FinancialStatementViewSet, basename='financial-statement')

urlpatterns = router.urls
