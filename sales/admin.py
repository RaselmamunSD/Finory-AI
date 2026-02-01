from django.contrib import admin
from .models import Customer, Invoice, InvoiceItem


@admin.register(Customer)
class CustomerAdmin(admin.ModelAdmin):
    list_display = ['name', 'tax_id', 'email', 'phone', 'company', 'credit_limit', 'risk_score', 'is_active', 'created_at']
    list_filter = ['is_active', 'company', 'created_at']
    search_fields = ['name', 'tax_id', 'email', 'phone', 'company__name']
    readonly_fields = ['id', 'created_at', 'updated_at']
    raw_id_fields = ['company']


class InvoiceItemInline(admin.TabularInline):
    model = InvoiceItem
    extra = 2
    fields = ['product', 'description', 'quantity', 'unit_price', 'discount', 'tax_rate', 'total']
    readonly_fields = []


@admin.register(Invoice)
class InvoiceAdmin(admin.ModelAdmin):
    list_display = ['invoice_number', 'customer', 'date', 'due_date', 'total', 'status', 'company', 'ai_fraud_alert', 'created_at']
    list_filter = ['status', 'invoice_type', 'date', 'company', 'ai_fraud_alert', 'created_at']
    search_fields = ['invoice_number', 'customer__name', 'company__name']
    readonly_fields = ['id', 'created_at', 'updated_at']
    raw_id_fields = ['company', 'branch', 'customer']
    inlines = [InvoiceItemInline]
    date_hierarchy = 'date'


@admin.register(InvoiceItem)
class InvoiceItemAdmin(admin.ModelAdmin):
    list_display = ['invoice', 'product', 'description', 'quantity', 'unit_price', 'total']
    list_filter = ['invoice__company', 'invoice__date']
    search_fields = ['invoice__invoice_number', 'product__name', 'description']
    raw_id_fields = ['invoice', 'product']
