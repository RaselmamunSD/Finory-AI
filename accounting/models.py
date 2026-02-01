"""
Accounting module models
Chart of Accounts, Journal Entries, Financial Statements
"""
import uuid
from django.db import models
from django.core.validators import MinValueValidator
from decimal import Decimal
from core.models import Company, Branch, User


class ChartOfAccounts(models.Model):
    """
    Chart of Accounts - Multi-level hierarchical structure
    """
    ACCOUNT_TYPES = [
        ('asset', 'Asset'),
        ('liability', 'Liability'),
        ('equity', 'Equity'),
        ('income', 'Income'),
        ('expense', 'Expense'),
    ]
    
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    company = models.ForeignKey(Company, on_delete=models.CASCADE, related_name='chart_of_accounts')
    code = models.CharField(max_length=50, help_text="e.g., '1.1.01'")
    name = models.CharField(max_length=255)
    account_type = models.CharField(max_length=20, choices=ACCOUNT_TYPES)
    parent = models.ForeignKey(
        'self',
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name='children'
    )
    is_active = models.BooleanField(default=True)
    ai_classification_tags = models.JSONField(default=list, blank=True)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        db_table = 'chart_of_accounts'
        verbose_name = 'Chart of Account'
        verbose_name_plural = 'Chart of Accounts'
        unique_together = [['company', 'code']]
        indexes = [
            models.Index(fields=['company', 'code']),
            models.Index(fields=['company', 'account_type']),
            models.Index(fields=['parent']),
        ]
    
    def __str__(self):
        return f"{self.code} - {self.name}"


class JournalEntry(models.Model):
    """
    Journal Entry - Records all accounting transactions
    Can be manual, auto-generated from sales/purchases, or AI-generated
    """
    ENTRY_STATUS = [
        ('draft', 'Draft'),
        ('posted', 'Posted'),
        ('reversed', 'Reversed'),
    ]
    
    SOURCE_TYPES = [
        ('manual', 'Manual'),
        ('sale', 'Sale'),
        ('purchase', 'Purchase'),
        ('payment', 'Payment'),
        ('ai_generated', 'AI Generated'),
    ]
    
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    company = models.ForeignKey(Company, on_delete=models.CASCADE, related_name='journal_entries')
    branch = models.ForeignKey(Branch, on_delete=models.SET_NULL, null=True, blank=True, related_name='journal_entries')
    entry_number = models.CharField(max_length=50, unique=True)
    date = models.DateField()
    description = models.TextField()
    
    # Source tracking
    source_type = models.CharField(max_length=20, choices=SOURCE_TYPES, default='manual')
    source_id = models.UUIDField(null=True, blank=True, help_text="Reference to source entity")
    
    # Approval
    created_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='journal_entries_created')
    approved_by = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='journal_entries_approved'
    )
    
    # AI metadata
    ai_confidence_score = models.IntegerField(
        null=True,
        blank=True,
        validators=[MinValueValidator(0)],
        help_text="AI confidence score 0-100"
    )
    
    status = models.CharField(max_length=20, choices=ENTRY_STATUS, default='draft')
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        db_table = 'journal_entries'
        verbose_name = 'Journal Entry'
        verbose_name_plural = 'Journal Entries'
        indexes = [
            models.Index(fields=['company', 'date']),
            models.Index(fields=['company', 'status']),
            models.Index(fields=['source_type', 'source_id']),
        ]
        ordering = ['-date', '-created_at']
    
    def __str__(self):
        return f"{self.entry_number} - {self.description[:50]}"


class JournalLine(models.Model):
    """
    Journal Line - Individual debit/credit entries within a journal entry
    """
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    journal_entry = models.ForeignKey(JournalEntry, on_delete=models.CASCADE, related_name='lines')
    account = models.ForeignKey(ChartOfAccounts, on_delete=models.PROTECT, related_name='journal_lines')
    debit = models.DecimalField(max_digits=15, decimal_places=2, default=Decimal('0.00'), validators=[MinValueValidator(0)])
    credit = models.DecimalField(max_digits=15, decimal_places=2, default=Decimal('0.00'), validators=[MinValueValidator(0)])
    description = models.TextField(null=True, blank=True)
    
    class Meta:
        db_table = 'journal_lines'
        verbose_name = 'Journal Line'
        verbose_name_plural = 'Journal Lines'
        indexes = [
            models.Index(fields=['journal_entry']),
            models.Index(fields=['account']),
        ]
    
    def __str__(self):
        return f"{self.account.code} - Debit: {self.debit}, Credit: {self.credit}"


class FinancialStatement(models.Model):
    """
    Financial Statements - Generated by AI or manually
    Balance Sheet, Income Statement, Cash Flow Statement
    """
    STATEMENT_TYPES = [
        ('balance_sheet', 'Balance Sheet'),
        ('income_statement', 'Income Statement'),
        ('cash_flow', 'Cash Flow Statement'),
    ]
    
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    company = models.ForeignKey(Company, on_delete=models.CASCADE, related_name='financial_statements')
    period_start = models.DateField()
    period_end = models.DateField()
    statement_type = models.CharField(max_length=20, choices=STATEMENT_TYPES)
    
    # Statement data (complete structure)
    data = models.JSONField(default=dict)
    
    # AI analysis and insights
    ai_analysis = models.JSONField(default=dict, blank=True, help_text="Insights, warnings, recommendations")
    
    generated_at = models.DateTimeField(auto_now_add=True)
    generated_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='financial_statements_generated')
    
    class Meta:
        db_table = 'financial_statements'
        verbose_name = 'Financial Statement'
        verbose_name_plural = 'Financial Statements'
        indexes = [
            models.Index(fields=['company', 'statement_type', 'period_start', 'period_end']),
        ]
        ordering = ['-period_end', '-generated_at']
    
    def __str__(self):
        return f"{self.statement_type} - {self.company.name} ({self.period_start} to {self.period_end})"
