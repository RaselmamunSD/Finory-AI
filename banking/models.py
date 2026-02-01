"""
Banking module models
Bank Accounts, Transactions, Reconciliation
"""
import uuid
from django.db import models
from django.core.validators import MinValueValidator
from decimal import Decimal
from core.models import Company
from payments.models import Payment


class BankAccount(models.Model):
    """
    Bank Account model
    """
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    company = models.ForeignKey(Company, on_delete=models.CASCADE, related_name='bank_accounts')
    account_number = models.CharField(max_length=100)
    bank_name = models.CharField(max_length=255)
    currency = models.CharField(max_length=3, default='USD')
    current_balance = models.DecimalField(max_digits=15, decimal_places=2, default=Decimal('0.00'))
    last_reconciliation_date = models.DateField(null=True, blank=True)
    
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        db_table = 'bank_accounts'
        verbose_name = 'Bank Account'
        verbose_name_plural = 'Bank Accounts'
        unique_together = [['company', 'account_number']]
        indexes = [
            models.Index(fields=['company', 'is_active']),
        ]
    
    def __str__(self):
        return f"{self.bank_name} - {self.account_number}"


class BankTransaction(models.Model):
    """
    Bank Transaction model with AI classification
    """
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    bank_account = models.ForeignKey(BankAccount, on_delete=models.CASCADE, related_name='transactions')
    date = models.DateField()
    description = models.TextField()
    debit = models.DecimalField(max_digits=15, decimal_places=2, default=Decimal('0.00'), validators=[MinValueValidator(0)])
    credit = models.DecimalField(max_digits=15, decimal_places=2, default=Decimal('0.00'), validators=[MinValueValidator(0)])
    balance = models.DecimalField(max_digits=15, decimal_places=2)
    
    is_reconciled = models.BooleanField(default=False)
    matched_payment = models.ForeignKey(Payment, on_delete=models.SET_NULL, null=True, blank=True, related_name='bank_transactions')
    
    # AI classification
    ai_classification = models.JSONField(default=dict, blank=True)
    
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        db_table = 'bank_transactions'
        verbose_name = 'Bank Transaction'
        verbose_name_plural = 'Bank Transactions'
        indexes = [
            models.Index(fields=['bank_account', 'date']),
            models.Index(fields=['is_reconciled']),
        ]
        ordering = ['-date']
    
    def __str__(self):
        return f"{self.bank_account.bank_name} - {self.date} - {self.description[:50]}"
