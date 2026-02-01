from django.contrib import admin
from .models import BankAccount, BankTransaction


@admin.register(BankAccount)
class BankAccountAdmin(admin.ModelAdmin):
    list_display = ['bank_name', 'account_number', 'company', 'currency', 'current_balance', 'is_active', 'last_reconciliation_date', 'created_at']
    list_filter = ['is_active', 'currency', 'company', 'created_at']
    search_fields = ['bank_name', 'account_number', 'company__name']
    readonly_fields = ['id', 'created_at', 'updated_at']
    raw_id_fields = ['company']


@admin.register(BankTransaction)
class BankTransactionAdmin(admin.ModelAdmin):
    list_display = ['bank_account', 'date', 'description', 'debit', 'credit', 'balance', 'is_reconciled', 'created_at']
    list_filter = ['is_reconciled', 'date', 'bank_account__company', 'created_at']
    search_fields = ['description', 'bank_account__bank_name', 'bank_account__account_number']
    readonly_fields = ['id', 'created_at']
    raw_id_fields = ['bank_account', 'matched_payment']
    date_hierarchy = 'date'
