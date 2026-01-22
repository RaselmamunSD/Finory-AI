"""
Accounting module views
"""
from rest_framework import viewsets, permissions
from .models import ChartOfAccounts, JournalEntry, FinancialStatement
from .serializers import ChartOfAccountsSerializer, JournalEntrySerializer, FinancialStatementSerializer


class ChartOfAccountsViewSet(viewsets.ModelViewSet):
    serializer_class = ChartOfAccountsSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def get_queryset(self):
        if hasattr(self.request, 'tenant') and self.request.tenant:
            return ChartOfAccounts.objects.filter(company=self.request.tenant)
        return ChartOfAccounts.objects.none()


class JournalEntryViewSet(viewsets.ModelViewSet):
    serializer_class = JournalEntrySerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def get_queryset(self):
        if hasattr(self.request, 'tenant') and self.request.tenant:
            return JournalEntry.objects.filter(company=self.request.tenant)
        return JournalEntry.objects.none()


class FinancialStatementViewSet(viewsets.ModelViewSet):
    serializer_class = FinancialStatementSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def get_queryset(self):
        if hasattr(self.request, 'tenant') and self.request.tenant:
            return FinancialStatement.objects.filter(company=self.request.tenant)
        return FinancialStatement.objects.none()
