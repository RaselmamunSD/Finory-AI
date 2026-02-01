from django.contrib import admin
from .models import Supplier, PurchaseOrder, PurchaseOrderItem


@admin.register(Supplier)
class SupplierAdmin(admin.ModelAdmin):
    list_display = ['name', 'tax_id', 'email', 'phone', 'company', 'delivery_time_avg', 'quality_score', 'is_active', 'created_at']
    list_filter = ['is_active', 'company', 'created_at']
    search_fields = ['name', 'tax_id', 'email', 'phone', 'company__name']
    readonly_fields = ['id', 'created_at', 'updated_at']
    raw_id_fields = ['company']


class PurchaseOrderItemInline(admin.TabularInline):
    model = PurchaseOrderItem
    extra = 2
    fields = ['product', 'quantity', 'unit_price', 'total']
    readonly_fields = []


@admin.register(PurchaseOrder)
class PurchaseOrderAdmin(admin.ModelAdmin):
    list_display = ['order_number', 'supplier', 'date', 'expected_delivery_date', 'total', 'status', 'company', 'created_at']
    list_filter = ['status', 'date', 'company', 'created_at']
    search_fields = ['order_number', 'supplier__name', 'company__name']
    readonly_fields = ['id', 'created_at', 'updated_at']
    raw_id_fields = ['company', 'branch', 'supplier', 'created_by']
    inlines = [PurchaseOrderItemInline]
    date_hierarchy = 'date'


@admin.register(PurchaseOrderItem)
class PurchaseOrderItemAdmin(admin.ModelAdmin):
    list_display = ['purchase_order', 'product', 'quantity', 'unit_price', 'total']
    list_filter = ['purchase_order__company', 'purchase_order__date']
    search_fields = ['purchase_order__order_number', 'product__name']
    raw_id_fields = ['purchase_order', 'product']
