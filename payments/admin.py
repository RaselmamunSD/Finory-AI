from django.contrib import admin
from .models import PaymentGateway, Payment


@admin.register(PaymentGateway)
class PaymentGatewayAdmin(admin.ModelAdmin):
    list_display = ['provider', 'company', 'is_active', 'created_at', 'updated_at']
    list_filter = ['provider', 'is_active', 'company', 'created_at']
    search_fields = ['company__name', 'provider']
    readonly_fields = ['id', 'created_at', 'updated_at']
    raw_id_fields = ['company']


@admin.register(Payment)
class PaymentAdmin(admin.ModelAdmin):
    list_display = ['amount', 'currency', 'payment_method', 'status', 'company', 'customer', 'invoice', 'ai_fraud_score', 'created_at']
    list_filter = ['status', 'payment_method', 'currency', 'company', 'created_at']
    search_fields = ['transaction_reference', 'company__name', 'customer__name', 'invoice__invoice_number']
    readonly_fields = ['id', 'created_at', 'updated_at']
    raw_id_fields = ['company', 'invoice', 'customer', 'gateway']
    date_hierarchy = 'created_at'
