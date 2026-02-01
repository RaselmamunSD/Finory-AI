from django.contrib import admin
from .models import Employee, Payroll, Contract


@admin.register(Employee)
class EmployeeAdmin(admin.ModelAdmin):
    list_display = ['employee_number', 'first_name', 'last_name', 'email', 'position', 'company', 'branch', 'is_active', 'hire_date', 'created_at']
    list_filter = ['is_active', 'position', 'department', 'company', 'hire_date', 'created_at']
    search_fields = ['employee_number', 'first_name', 'last_name', 'email', 'company__name']
    readonly_fields = ['id', 'created_at', 'updated_at']
    raw_id_fields = ['company', 'branch', 'user']


@admin.register(Payroll)
class PayrollAdmin(admin.ModelAdmin):
    list_display = ['employee', 'period_start', 'period_end', 'gross_salary', 'net_salary', 'company', 'created_at']
    list_filter = ['company', 'period_start', 'period_end', 'created_at']
    search_fields = ['employee__first_name', 'employee__last_name', 'employee__employee_number', 'company__name']
    readonly_fields = ['id', 'created_at']
    raw_id_fields = ['company', 'employee']
    date_hierarchy = 'period_start'


@admin.register(Contract)
class ContractAdmin(admin.ModelAdmin):
    list_display = ['employee', 'contract_type', 'start_date', 'end_date', 'salary', 'company', 'is_active', 'created_at']
    list_filter = ['contract_type', 'is_active', 'company', 'start_date', 'created_at']
    search_fields = ['employee__first_name', 'employee__last_name', 'company__name']
    readonly_fields = ['id', 'created_at', 'updated_at']
    raw_id_fields = ['company', 'employee']
    date_hierarchy = 'start_date'
