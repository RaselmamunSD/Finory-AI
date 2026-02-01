"""
Banking module URLs
"""
from django.urls import path
from rest_framework.routers import SimpleRouter
from . import views

router = SimpleRouter()
router.register(r'accounts', views.BankAccountViewSet, basename='bank-account')
router.register(r'transactions', views.BankTransactionViewSet, basename='bank-transaction')

urlpatterns = router.urls
