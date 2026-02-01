"""
Payments module models
Payment Gateways, Payments, Transactions
"""
import uuid
from django.db import models
from django.core.validators import MinValueValidator
from decimal import Decimal
from core.models import Company, User
from sales.models import Invoice, Customer


class PaymentGateway(models.Model):
    """
    Payment Gateway configuration
    """
    PROVIDERS = [
        ('stripe', 'Stripe'),
        ('mercadopago', 'MercadoPago'),
        ('paypal', 'PayPal'),
        ('square', 'Square'),
        ('other', 'Other'),
    ]
    
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    company = models.ForeignKey(Company, on_delete=models.CASCADE, related_name='payment_gateways')
    provider = models.CharField(max_length=50, choices=PROVIDERS)
    credentials = models.JSONField(default=dict, help_text="Encrypted credentials")
    is_active = models.BooleanField(default=True)
    supported_currencies = models.JSONField(default=list, blank=True)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        db_table = 'payment_gateways'
        verbose_name = 'Payment Gateway'
        verbose_name_plural = 'Payment Gateways'
    
    def __str__(self):
        return f"{self.company.name} - {self.provider}"


class Payment(models.Model):
    """
    Payment model with AI fraud detection
    """
    PAYMENT_METHODS = [
        ('gateway', 'Payment Gateway'),
        ('bank_transfer', 'Bank Transfer'),
        ('cash', 'Cash'),
        ('check', 'Check'),
    ]
    
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('completed', 'Completed'),
        ('failed', 'Failed'),
        ('refunded', 'Refunded'),
    ]
    
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    company = models.ForeignKey(Company, on_delete=models.CASCADE, related_name='payments')
    invoice = models.ForeignKey(Invoice, on_delete=models.SET_NULL, null=True, blank=True, related_name='payments')
    customer = models.ForeignKey(Customer, on_delete=models.SET_NULL, null=True, blank=True, related_name='payments')
    
    amount = models.DecimalField(max_digits=15, decimal_places=2, validators=[MinValueValidator(0)])
    currency = models.CharField(max_length=3, default='USD')
    payment_method = models.CharField(max_length=20, choices=PAYMENT_METHODS)
    gateway = models.ForeignKey(PaymentGateway, on_delete=models.SET_NULL, null=True, blank=True, related_name='payments')
    transaction_reference = models.CharField(max_length=255, null=True, blank=True)
    
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    
    # AI fraud detection
    ai_fraud_score = models.IntegerField(null=True, blank=True, validators=[MinValueValidator(0)], help_text="0-100")
    
    metadata = models.JSONField(default=dict, blank=True)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        db_table = 'payments'
        verbose_name = 'Payment'
        verbose_name_plural = 'Payments'
        indexes = [
            models.Index(fields=['company', 'status']),
            models.Index(fields=['invoice']),
            models.Index(fields=['customer']),
        ]
    
    def __str__(self):
        return f"Payment {self.amount} {self.currency} - {self.status}"
