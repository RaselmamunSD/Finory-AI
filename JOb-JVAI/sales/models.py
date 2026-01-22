"""
Sales module models
Customers, Invoices, Invoice Items
"""
import uuid
from django.db import models
from django.core.validators import MinValueValidator
from decimal import Decimal
from core.models import Company, Branch, User


class Customer(models.Model):
    """
    Customer model with AI-powered risk and profitability scoring
    """
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    company = models.ForeignKey(Company, on_delete=models.CASCADE, related_name='customers')
    name = models.CharField(max_length=255)
    tax_id = models.CharField(max_length=50, null=True, blank=True)
    email = models.EmailField(null=True, blank=True)
    phone = models.CharField(max_length=20, null=True, blank=True)
    address = models.TextField(null=True, blank=True)
    
    # Credit management
    credit_limit = models.DecimalField(max_digits=15, decimal_places=2, default=Decimal('0.00'))
    payment_terms = models.IntegerField(default=30, help_text="Days to pay")
    
    # AI scoring
    risk_score = models.IntegerField(
        null=True,
        blank=True,
        validators=[MinValueValidator(0)],
        help_text="AI-calculated risk score 0-100"
    )
    profitability_score = models.IntegerField(
        null=True,
        blank=True,
        validators=[MinValueValidator(0)],
        help_text="AI-calculated profitability score 0-100"
    )
    ai_behavior_analysis = models.JSONField(default=dict, blank=True)
    
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        db_table = 'customers'
        verbose_name = 'Customer'
        verbose_name_plural = 'Customers'
        indexes = [
            models.Index(fields=['company', 'is_active']),
            models.Index(fields=['tax_id']),
        ]
    
    def __str__(self):
        return self.name


class Invoice(models.Model):
    """
    Invoice model - Sales invoices with AI fraud detection and payment prediction
    """
    INVOICE_TYPES = [
        ('standard', 'Standard'),
        ('credit_note', 'Credit Note'),
        ('debit_note', 'Debit Note'),
    ]
    
    STATUS_CHOICES = [
        ('draft', 'Draft'),
        ('sent', 'Sent'),
        ('paid', 'Paid'),
        ('overdue', 'Overdue'),
        ('cancelled', 'Cancelled'),
    ]
    
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    company = models.ForeignKey(Company, on_delete=models.CASCADE, related_name='invoices')
    branch = models.ForeignKey(Branch, on_delete=models.SET_NULL, null=True, blank=True, related_name='invoices')
    customer = models.ForeignKey(Customer, on_delete=models.PROTECT, related_name='invoices')
    
    invoice_number = models.CharField(max_length=50)
    invoice_type = models.CharField(max_length=20, choices=INVOICE_TYPES, default='standard')
    date = models.DateField()
    due_date = models.DateField()
    
    # Financial amounts
    subtotal = models.DecimalField(max_digits=15, decimal_places=2, default=Decimal('0.00'))
    tax = models.DecimalField(max_digits=15, decimal_places=2, default=Decimal('0.00'))
    total = models.DecimalField(max_digits=15, decimal_places=2, default=Decimal('0.00'))
    currency = models.CharField(max_length=3, default='USD')
    
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='draft')
    
    # Payment link
    payment_link_url = models.URLField(null=True, blank=True)
    
    # AI metadata
    ai_fraud_alert = models.BooleanField(default=False)
    ai_payment_prediction = models.JSONField(default=dict, blank=True)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        db_table = 'invoices'
        verbose_name = 'Invoice'
        verbose_name_plural = 'Invoices'
        unique_together = [['company', 'invoice_number']]
        indexes = [
            models.Index(fields=['company', 'invoice_number']),
            models.Index(fields=['company', 'customer', 'date']),
            models.Index(fields=['status', 'due_date']),
        ]
        ordering = ['-date', '-created_at']
    
    def __str__(self):
        return f"{self.invoice_number} - {self.customer.name}"


class InvoiceItem(models.Model):
    """
    Invoice Line Items
    """
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    invoice = models.ForeignKey(Invoice, on_delete=models.CASCADE, related_name='items')
    product = models.ForeignKey(
        'inventory.Product',
        on_delete=models.PROTECT,
        null=True,
        blank=True,
        related_name='invoice_items'
    )
    description = models.TextField()
    quantity = models.DecimalField(max_digits=10, decimal_places=2, validators=[MinValueValidator(0)])
    unit_price = models.DecimalField(max_digits=15, decimal_places=2, validators=[MinValueValidator(0)])
    discount = models.DecimalField(max_digits=5, decimal_places=2, default=Decimal('0.00'), validators=[MinValueValidator(0)])
    tax_rate = models.DecimalField(max_digits=5, decimal_places=2, default=Decimal('0.00'), validators=[MinValueValidator(0)])
    total = models.DecimalField(max_digits=15, decimal_places=2, validators=[MinValueValidator(0)])
    
    # AI margin analysis
    ai_margin_analysis = models.JSONField(default=dict, blank=True)
    
    class Meta:
        db_table = 'invoice_items'
        verbose_name = 'Invoice Item'
        verbose_name_plural = 'Invoice Items'
        indexes = [
            models.Index(fields=['invoice']),
            models.Index(fields=['product']),
        ]
    
    def __str__(self):
        return f"{self.invoice.invoice_number} - {self.description[:50]}"
