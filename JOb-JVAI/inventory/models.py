"""
Inventory module models
Products, Warehouses, Stock, Stock Movements (Kardex)
"""
import uuid
from django.db import models
from django.core.validators import MinValueValidator
from decimal import Decimal
from core.models import Company, Branch, User


class ProductCategory(models.Model):
    """Product categories"""
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    company = models.ForeignKey(Company, on_delete=models.CASCADE, related_name='product_categories')
    name = models.CharField(max_length=255)
    parent = models.ForeignKey('self', on_delete=models.CASCADE, null=True, blank=True, related_name='children')
    description = models.TextField(null=True, blank=True)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        db_table = 'product_categories'
        verbose_name = 'Product Category'
        verbose_name_plural = 'Product Categories'
        unique_together = [['company', 'name']]
    
    def __str__(self):
        return self.name


class Product(models.Model):
    """
    Product model with AI demand forecasting
    """
    COST_METHODS = [
        ('fifo', 'FIFO'),
        ('average', 'Average'),
        ('standard', 'Standard'),
    ]
    
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    company = models.ForeignKey(Company, on_delete=models.CASCADE, related_name='products')
    sku = models.CharField(max_length=100)
    name = models.CharField(max_length=255)
    description = models.TextField(null=True, blank=True)
    category = models.ForeignKey(ProductCategory, on_delete=models.SET_NULL, null=True, blank=True, related_name='products')
    unit_of_measure = models.CharField(max_length=20, default='unit')
    
    # Costing
    cost_method = models.CharField(max_length=20, choices=COST_METHODS, default='average')
    reorder_point = models.DecimalField(max_digits=10, decimal_places=2, default=Decimal('0.00'), validators=[MinValueValidator(0)])
    
    # AI predictions
    ai_demand_forecast = models.JSONField(default=dict, blank=True)
    ai_optimal_stock_level = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        db_table = 'products'
        verbose_name = 'Product'
        verbose_name_plural = 'Products'
        unique_together = [['company', 'sku']]
        indexes = [
            models.Index(fields=['company', 'sku']),
            models.Index(fields=['company', 'is_active']),
        ]
    
    def __str__(self):
        return f"{self.sku} - {self.name}"


class Warehouse(models.Model):
    """
    Warehouse/Location model
    """
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    company = models.ForeignKey(Company, on_delete=models.CASCADE, related_name='warehouses')
    branch = models.ForeignKey(Branch, on_delete=models.SET_NULL, null=True, blank=True, related_name='warehouses')
    name = models.CharField(max_length=255)
    location = models.TextField(null=True, blank=True)
    is_active = models.BooleanField(default=True)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        db_table = 'warehouses'
        verbose_name = 'Warehouse'
        verbose_name_plural = 'Warehouses'
        unique_together = [['company', 'name']]
        indexes = [
            models.Index(fields=['company', 'is_active']),
        ]
    
    def __str__(self):
        return f"{self.company.name} - {self.name}"


class Stock(models.Model):
    """
    Stock model - Current inventory levels per product per warehouse
    """
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='stock')
    warehouse = models.ForeignKey(Warehouse, on_delete=models.CASCADE, related_name='stock')
    quantity = models.DecimalField(max_digits=10, decimal_places=2, default=Decimal('0.00'), validators=[MinValueValidator(0)])
    reserved_quantity = models.DecimalField(max_digits=10, decimal_places=2, default=Decimal('0.00'), validators=[MinValueValidator(0)])
    last_movement_date = models.DateTimeField(null=True, blank=True)
    
    class Meta:
        db_table = 'stock'
        verbose_name = 'Stock'
        verbose_name_plural = 'Stock'
        unique_together = [['product', 'warehouse']]
        indexes = [
            models.Index(fields=['product', 'warehouse']),
            models.Index(fields=['warehouse']),
        ]
    
    def __str__(self):
        return f"{self.product.name} - {self.warehouse.name}: {self.quantity}"
    
    @property
    def available_quantity(self):
        return self.quantity - self.reserved_quantity


class StockMovement(models.Model):
    """
    Stock Movement (Kardex) - Tracks all inventory movements
    """
    MOVEMENT_TYPES = [
        ('in', 'In'),
        ('out', 'Out'),
        ('adjustment', 'Adjustment'),
        ('transfer', 'Transfer'),
    ]
    
    REFERENCE_TYPES = [
        ('sale', 'Sale'),
        ('purchase', 'Purchase'),
        ('adjustment', 'Adjustment'),
        ('transfer', 'Transfer'),
    ]
    
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='stock_movements')
    warehouse = models.ForeignKey(Warehouse, on_delete=models.CASCADE, related_name='stock_movements')
    movement_type = models.CharField(max_length=20, choices=MOVEMENT_TYPES)
    quantity = models.DecimalField(max_digits=10, decimal_places=2, validators=[MinValueValidator(0)])
    unit_cost = models.DecimalField(max_digits=15, decimal_places=2, validators=[MinValueValidator(0)])
    
    # Reference to source transaction
    reference_type = models.CharField(max_length=20, choices=REFERENCE_TYPES, null=True, blank=True)
    reference_id = models.UUIDField(null=True, blank=True)
    
    date = models.DateTimeField()
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='stock_movements')
    
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        db_table = 'stock_movements'
        verbose_name = 'Stock Movement'
        verbose_name_plural = 'Stock Movements'
        indexes = [
            models.Index(fields=['product', 'warehouse', 'date']),
            models.Index(fields=['reference_type', 'reference_id']),
        ]
        ordering = ['-date']
    
    def __str__(self):
        return f"{self.movement_type} - {self.product.name} - {self.quantity}"
