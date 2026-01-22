"""
HR module views
"""
from rest_framework import viewsets, permissions
from .models import Employee, Payroll, Contract
from .serializers import EmployeeSerializer, PayrollSerializer, ContractSerializer


class EmployeeViewSet(viewsets.ModelViewSet):
    serializer_class = EmployeeSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def get_queryset(self):
        if hasattr(self.request, 'tenant') and self.request.tenant:
            return Employee.objects.filter(company=self.request.tenant)
        return Employee.objects.none()


class PayrollViewSet(viewsets.ModelViewSet):
    serializer_class = PayrollSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def get_queryset(self):
        if hasattr(self.request, 'tenant') and self.request.tenant:
            return Payroll.objects.filter(company=self.request.tenant)
        return Payroll.objects.none()


class ContractViewSet(viewsets.ModelViewSet):
    serializer_class = ContractSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def get_queryset(self):
        if hasattr(self.request, 'tenant') and self.request.tenant:
            return Contract.objects.filter(company=self.request.tenant)
        return Contract.objects.none()
