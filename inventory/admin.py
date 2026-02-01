from django.contrib import admin
from .models import ProductCategory, Product, Warehouse, Stock, StockMovement


@admin.register(ProductCategory)
class ProductCategoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'company', 'parent', 'created_at']
    list_filter = ['company', 'created_at']
    search_fields = ['name', 'company__name']
    readonly_fields = ['id', 'created_at', 'updated_at']
    raw_id_fields = ['company', 'parent']


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ['sku', 'name', 'category', 'company', 'cost_method', 'reorder_point', 'is_active', 'created_at']
    list_filter = ['cost_method', 'is_active', 'company', 'category', 'created_at']
    search_fields = ['sku', 'name', 'company__name']
    readonly_fields = ['id', 'created_at', 'updated_at']
    raw_id_fields = ['company', 'category']


@admin.register(Warehouse)
class WarehouseAdmin(admin.ModelAdmin):
    list_display = ['name', 'company', 'branch', 'is_active', 'created_at']
    list_filter = ['is_active', 'company', 'created_at']
    search_fields = ['name', 'company__name', 'location']
    readonly_fields = ['id', 'created_at', 'updated_at']
    raw_id_fields = ['company', 'branch']


@admin.register(Stock)
class StockAdmin(admin.ModelAdmin):
    list_display = ['product', 'warehouse', 'quantity', 'reserved_quantity', 'available_quantity', 'last_movement_date']
    list_filter = ['warehouse__company', 'warehouse']
    search_fields = ['product__name', 'product__sku', 'warehouse__name']
    readonly_fields = ['id', 'available_quantity']
    raw_id_fields = ['product', 'warehouse']


@admin.register(StockMovement)
class StockMovementAdmin(admin.ModelAdmin):
    list_display = ['product', 'warehouse', 'movement_type', 'quantity', 'unit_cost', 'date', 'user', 'created_at']
    list_filter = ['movement_type', 'reference_type', 'date', 'warehouse__company', 'created_at']
    search_fields = ['product__name', 'product__sku', 'warehouse__name']
    readonly_fields = ['id', 'created_at']
    raw_id_fields = ['product', 'warehouse', 'user']
    date_hierarchy = 'date'
