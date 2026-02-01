"""
HR module models
Employees, Payroll, Contracts
"""
import uuid
from django.db import models
from django.core.validators import MinValueValidator
from decimal import Decimal
from core.models import Company, Branch, User


class Employee(models.Model):
    """
    Employee model
    """
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    company = models.ForeignKey(Company, on_delete=models.CASCADE, related_name='employees')
    branch = models.ForeignKey(Branch, on_delete=models.SET_NULL, null=True, blank=True, related_name='employees')
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='employee_profile')
    
    employee_number = models.CharField(max_length=50)
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    email = models.EmailField()
    phone = models.CharField(max_length=20, null=True, blank=True)
    position = models.CharField(max_length=100)
    department = models.CharField(max_length=100, null=True, blank=True)
    hire_date = models.DateField()
    
    is_active = models.BooleanField(default=True)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        db_table = 'employees'
        verbose_name = 'Employee'
        verbose_name_plural = 'Employees'
        unique_together = [['company', 'employee_number']]
        indexes = [
            models.Index(fields=['company', 'is_active']),
        ]
    
    def __str__(self):
        return f"{self.first_name} {self.last_name} - {self.employee_number}"


class Payroll(models.Model):
    """
    Payroll model
    """
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    company = models.ForeignKey(Company, on_delete=models.CASCADE, related_name='payrolls')
    employee = models.ForeignKey(Employee, on_delete=models.CASCADE, related_name='payrolls')
    
    period_start = models.DateField()
    period_end = models.DateField()
    gross_salary = models.DecimalField(max_digits=15, decimal_places=2, validators=[MinValueValidator(0)])
    
    # Deductions
    afp_deduction = models.DecimalField(max_digits=15, decimal_places=2, default=Decimal('0.00'), help_text="Pension fund")
    sfs_deduction = models.DecimalField(max_digits=15, decimal_places=2, default=Decimal('0.00'), help_text="Health insurance")
    tax_deduction = models.DecimalField(max_digits=15, decimal_places=2, default=Decimal('0.00'))
    other_deductions = models.DecimalField(max_digits=15, decimal_places=2, default=Decimal('0.00'))
    
    net_salary = models.DecimalField(max_digits=15, decimal_places=2, validators=[MinValueValidator(0)])
    
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        db_table = 'payrolls'
        verbose_name = 'Payroll'
        verbose_name_plural = 'Payrolls'
        indexes = [
            models.Index(fields=['company', 'period_start', 'period_end']),
        ]
    
    def __str__(self):
        return f"{self.employee.first_name} {self.employee.last_name} - {self.period_start} to {self.period_end}"


class Contract(models.Model):
    """
    Employee Contract model
    """
    CONTRACT_TYPES = [
        ('full_time', 'Full Time'),
        ('part_time', 'Part Time'),
        ('contractor', 'Contractor'),
        ('intern', 'Intern'),
    ]
    
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    company = models.ForeignKey(Company, on_delete=models.CASCADE, related_name='contracts')
    employee = models.ForeignKey(Employee, on_delete=models.CASCADE, related_name='contracts')
    contract_type = models.CharField(max_length=20, choices=CONTRACT_TYPES)
    start_date = models.DateField()
    end_date = models.DateField(null=True, blank=True)
    salary = models.DecimalField(max_digits=15, decimal_places=2, validators=[MinValueValidator(0)])
    is_active = models.BooleanField(default=True)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        db_table = 'contracts'
        verbose_name = 'Contract'
        verbose_name_plural = 'Contracts'
        indexes = [
            models.Index(fields=['company', 'is_active']),
        ]
    
    def __str__(self):
        return f"{self.employee.first_name} {self.employee.last_name} - {self.contract_type}"
