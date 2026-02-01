# Finory IA - Project Structure

## Directory Structure

```
finory_ia/
├── core/                    # Multi-tenancy, Authentication, RBAC
│   ├── models.py           # User, Company, Branch, Role, CompanyUser, AuditLog
│   ├── views.py            # ViewSets for core models
│   ├── serializers.py      # Serializers for core models
│   ├── urls.py             # URL routing
│   ├── middleware.py       # TenantMiddleware for multi-tenancy
│   └── managers.py         # Custom managers
│
├── accounting/              # Accounting module
│   ├── models.py           # ChartOfAccounts, JournalEntry, FinancialStatement
│   ├── views.py            # ViewSets
│   ├── serializers.py      # Serializers
│   └── urls.py             # URL routing
│
├── sales/                   # Sales module
│   ├── models.py           # Customer, Invoice, InvoiceItem
│   ├── views.py            # ViewSets
│   ├── serializers.py      # Serializers
│   └── urls.py             # URL routing
│
├── inventory/               # Inventory module
│   ├── models.py           # Product, Warehouse, Stock, StockMovement
│   ├── views.py            # ViewSets
│   ├── serializers.py      # Serializers
│   └── urls.py             # URL routing
│
├── payments/                # Payments module
│   ├── models.py           # PaymentGateway, Payment
│   ├── views.py            # ViewSets
│   ├── serializers.py      # Serializers
│   └── urls.py             # URL routing
│
├── banking/                  # Banking module
│   ├── models.py           # BankAccount, BankTransaction
│   ├── views.py            # ViewSets
│   ├── serializers.py      # Serializers
│   └── urls.py             # URL routing
│
├── ai_engine/               # AI Engine module
│   ├── models.py           # AIModel, AIPrediction, AIRecommendation
│   ├── views.py            # ViewSets
│   ├── serializers.py      # Serializers
│   └── urls.py             # URL routing
│
├── crm/                     # CRM module
│   ├── models.py           # Lead, Opportunity
│   ├── views.py            # ViewSets
│   ├── serializers.py      # Serializers
│   └── urls.py             # URL routing
│
├── hr/                      # HR module
│   ├── models.py           # Employee, Payroll, Contract
│   ├── views.py            # ViewSets
│   ├── serializers.py      # Serializers
│   └── urls.py             # URL routing
│
├── purchases/               # Purchases module
│   ├── models.py           # Supplier, PurchaseOrder
│   ├── views.py            # ViewSets
│   ├── serializers.py      # Serializers
│   └── urls.py             # URL routing
│
├── documents/               # Documents module
│   ├── models.py           # Document, VoiceCommand
│   ├── views.py            # ViewSets
│   ├── serializers.py      # Serializers
│   └── urls.py             # URL routing
│
├── tasks/                   # Tasks module
│   ├── models.py           # Task
│   ├── views.py            # ViewSets
│   ├── serializers.py      # Serializers
│   └── urls.py             # URL routing
│
├── identity/                # Identity module
│   ├── models.py           # Identity, IdentityDocument, FaceVerification
│   ├── views.py            # ViewSets
│   ├── serializers.py      # Serializers
│   └── urls.py             # URL routing
│
├── legal/                   # Legal module
│   ├── models.py           # Incident, LegalReport, Blacklist
│   ├── views.py            # ViewSets
│   ├── serializers.py      # Serializers
│   └── urls.py             # URL routing
│
├── analytics/               # Analytics module
│   ├── models.py           # Dashboard, KPI
│   ├── views.py            # ViewSets
│   ├── serializers.py      # Serializers
│   └── urls.py             # URL routing
│
├── api/                     # API module
│   ├── urls.py             # Main API URL routing
│   ├── exceptions.py       # Custom exception handlers
│   └── views/
│       └── auth_views.py   # Authentication views
│
├── finory_ia/               # Django project settings
│   ├── settings.py         # Django settings
│   ├── urls.py             # Root URL configuration
│   ├── wsgi.py             # WSGI configuration
│   └── asgi.py             # ASGI configuration
│
├── manage.py                # Django management script
├── requirements.txt         # Python dependencies
├── README.md                # Project documentation
├── .gitignore              # Git ignore rules
└── Finory_IA.postman_collection.json  # Postman collection
```

## Key Features

### Multi-Tenancy
- Every model includes `company` foreign key for data isolation
- `TenantMiddleware` automatically filters queries by company
- Users can belong to multiple companies with different roles

### Authentication
- JWT token-based authentication
- 2FA support (TOTP)
- Biometric authentication support
- Custom User model with email as username

### API Structure
- RESTful API design
- Versioned endpoints (`/api/v1/`)
- Consistent response format
- Comprehensive error handling

### AI Integration
- AI models registry
- Predictions and recommendations
- AI audit logging
- Autonomous mode support

## Database Models Summary

### Core (6 models)
- User, Company, Branch, Role, CompanyUser, AuditLog

### Accounting (4 models)
- ChartOfAccounts, JournalEntry, JournalLine, FinancialStatement

### Sales (3 models)
- Customer, Invoice, InvoiceItem

### Inventory (5 models)
- ProductCategory, Product, Warehouse, Stock, StockMovement

### Payments (2 models)
- PaymentGateway, Payment

### Banking (2 models)
- BankAccount, BankTransaction

### AI Engine (4 models)
- AIModel, AIPrediction, AIRecommendation, AIAuditLog

### CRM (2 models)
- Lead, Opportunity

### HR (3 models)
- Employee, Payroll, Contract

### Purchases (3 models)
- Supplier, PurchaseOrder, PurchaseOrderItem

### Documents (2 models)
- Document, VoiceCommand

### Tasks (1 model)
- Task

### Identity (3 models)
- Identity, IdentityDocument, FaceVerification

### Legal (4 models)
- Incident, IncidentEvidence, LegalReport, Blacklist

### Analytics (2 models)
- Dashboard, KPI

**Total: 42+ models**

## Next Steps

1. Run migrations: `python manage.py makemigrations && python manage.py migrate`
2. Create superuser: `python manage.py createsuperuser`
3. Import Postman collection
4. Start development server: `python manage.py runserver`
5. Test API endpoints
