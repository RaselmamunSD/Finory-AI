from django.contrib import admin
from .models import ChartOfAccounts, JournalEntry, JournalLine, FinancialStatement


@admin.register(ChartOfAccounts)
class ChartOfAccountsAdmin(admin.ModelAdmin):
    list_display = ['code', 'name', 'account_type', 'company', 'is_active', 'created_at']
    list_filter = ['account_type', 'is_active', 'company', 'created_at']
    search_fields = ['code', 'name', 'company__name']
    readonly_fields = ['id', 'created_at', 'updated_at']
    raw_id_fields = ['parent', 'company']


class JournalLineInline(admin.TabularInline):
    model = JournalLine
    extra = 2
    fields = ['account', 'debit', 'credit', 'description']
    readonly_fields = []


@admin.register(JournalEntry)
class JournalEntryAdmin(admin.ModelAdmin):
    list_display = ['entry_number', 'date', 'description', 'company', 'status', 'source_type', 'created_at']
    list_filter = ['status', 'source_type', 'date', 'company', 'created_at']
    search_fields = ['entry_number', 'description', 'company__name']
    readonly_fields = ['id', 'created_at', 'updated_at']
    raw_id_fields = ['company', 'branch', 'created_by', 'approved_by']
    inlines = [JournalLineInline]
    date_hierarchy = 'date'


@admin.register(JournalLine)
class JournalLineAdmin(admin.ModelAdmin):
    list_display = ['journal_entry', 'account', 'debit', 'credit', 'description']
    list_filter = ['journal_entry__company', 'journal_entry__date']
    search_fields = ['journal_entry__entry_number', 'account__code', 'account__name', 'description']
    raw_id_fields = ['journal_entry', 'account']


@admin.register(FinancialStatement)
class FinancialStatementAdmin(admin.ModelAdmin):
    list_display = ['statement_type', 'company', 'period_start', 'period_end', 'generated_at', 'generated_by']
    list_filter = ['statement_type', 'company', 'period_start', 'period_end', 'generated_at']
    search_fields = ['company__name']
    readonly_fields = ['id', 'generated_at']
    raw_id_fields = ['company', 'generated_by']
    date_hierarchy = 'period_end'
