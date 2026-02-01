# Finory IA - Next Generation Financial Intelligence Platform

**Finory IA** is a comprehensive, AI-powered financial intelligence platform that unifies accounting, inventory, CRM, payments, and business intelligence into a single, global, multi-tenant system.

## 🎯 Features

### Core Modules

1. **Administration & Security**
   - Multi-tenant / multi-branch architecture
   - Role-Based Access Control (RBAC)
   - Complete audit trail
   - 2FA and biometric authentication
   - Automatic backups and data encryption

2. **Sales & Invoicing**
   - Quotations, orders, and electronic invoices
   - Credit control per customer
   - Recurring invoicing and automatic reminders
   - Email/WhatsApp delivery
   - Sales and collections dashboard
   - International payment gateway integration

3. **Purchases & Suppliers**
   - Purchase orders, receipts, and purchase invoices
   - Accounts payable control
   - OCR for scanning invoices
   - Supplier ranking and delivery times

4. **Intelligent Inventory**
   - Batch, serial, location, and kit control
   - Predictive replenishment alerts (AI)
   - Automatic Kardex (entries/exits)
   - FIFO / Average valuation
   - Rotation, cost, and margin reports

5. **Accounting & Finance**
   - Multi-level chart of accounts
   - Automatic entries from sales/purchases
   - Financial statements, balance sheet, cash flow
   - AI-automated bank reconciliation
   - Local tax compliance by country
   - Excel/PDF export and automatic report delivery

6. **HR & Payroll**
   - Employee management, contracts, and vacations
   - Payroll calculation with AFP, SFS, and taxes
   - Employee portal with receipts and certificates
   - AI-powered performance evaluation

7. **CRM & Marketing**
   - Lead registration, opportunities, and sales funnels
   - Email and WhatsApp automation
   - Targeted campaigns and quote tracking
   - Customer scoring by profitability and reliability

8. **AI Intelligence & Analytics**
   - OCR for accounting documents and invoices
   - Automatic expense classification
   - Cash flow, sales, and inventory predictions
   - Behavior analysis and early alerts
   - Chatbot for queries ("How much did I sell this month?")

9. **Identity Verification (Extra Value)**
   - Integration with Google/AWS Rekognition AI
   - Facial verification vs. document
   - Public database queries (blacklists, police, datacredit)
   - Risk reporting and archiving for people or companies

10. **Legal Shield**
    - Incident reporting
    - Legal report generation
    - Blacklist management
    - Evidence tracking

## 🏗️ Technical Stack

- **Backend**: Django 4.2 + Django REST Framework
- **Database**: SQLite3 (Development) → PostgreSQL (Production)
- **Authentication**: JWT + 2FA + Biometric support
- **Task Queue**: Celery + Redis (for async AI processing)
- **API Documentation**: Postman Collection

## 📦 Installation

### Prerequisites

- Python 3.10+
- pip
- virtualenv (recommended)

### Setup

1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd finory_ia
   ```

2. **Create virtual environment**
   ```bash
   python -m venv venv
   source venv/bin/activate
   "C:/Rasel/perez project/Finory-AI/.venv/Scripts/Activate.ps1"  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Configure environment variables**
   ```bash
   cp .env.example .env
   # Edit .env with your settings
   ```

5. **Run migrations**
   ```bash
   python manage.py makemigrations
   python manage.py migrate
   ```

6. **Create superuser**
   ```bash
   python manage.py createsuperuser
   ```

7. **Run development server**
   ```bash
   python manage.py runserver
   ```

## 🔐 Authentication

### Login

```bash
POST /api/v1/auth/login/
Content-Type: application/json

{
  "email": "user@example.com",
  "password": "password123"
}
```

### Register

```bash
POST /api/v1/auth/register/
Content-Type: application/json

{
  "email": "user@example.com",
  "password": "password123",
  "company_name": "My Company"
}
```

### Using JWT Token

Include the token in the Authorization header:

```
Authorization: Bearer <access_token>
```

## 📡 API Endpoints

### Core
- `/api/v1/companies/` - Company management
- `/api/v1/users/` - User management
- `/api/v1/branches/` - Branch management
- `/api/v1/roles/` - Role management

### Accounting
- `/api/v1/accounting/accounts/` - Chart of accounts
- `/api/v1/accounting/journal-entries/` - Journal entries
- `/api/v1/accounting/financial-statements/` - Financial statements

### Sales
- `/api/v1/sales/customers/` - Customer management
- `/api/v1/sales/invoices/` - Invoice management

### Inventory
- `/api/v1/inventory/products/` - Product management
- `/api/v1/inventory/warehouses/` - Warehouse management
- `/api/v1/inventory/stock/` - Stock levels
- `/api/v1/inventory/stock-movements/` - Stock movements

### Payments
- `/api/v1/payments/gateways/` - Payment gateway configuration
- `/api/v1/payments/payments/` - Payment processing

### Banking
- `/api/v1/banking/accounts/` - Bank account management
- `/api/v1/banking/transactions/` - Bank transaction management

### AI Engine
- `/api/v1/ai/predictions/` - AI predictions
- `/api/v1/ai/recommendations/` - AI recommendations
- `/api/v1/ai/models/` - AI model management

### CRM
- `/api/v1/crm/leads/` - Lead management
- `/api/v1/crm/opportunities/` - Opportunity management

### HR
- `/api/v1/hr/employees/` - Employee management
- `/api/v1/hr/payrolls/` - Payroll management
- `/api/v1/hr/contracts/` - Contract management

### Purchases
- `/api/v1/purchases/suppliers/` - Supplier management
- `/api/v1/purchases/purchase-orders/` - Purchase order management

### Documents
- `/api/v1/documents/documents/` - Document management
- `/api/v1/documents/voice-commands/` - Voice command processing

### Tasks
- `/api/v1/tasks/tasks/` - Task management

### Identity
- `/api/v1/identity/identities/` - Identity verification
- `/api/v1/identity/verifications/` - Face verification

### Legal
- `/api/v1/legal/incidents/` - Incident management
- `/api/v1/legal/legal-reports/` - Legal report management
- `/api/v1/legal/blacklist/` - Blacklist management

### Analytics
- `/api/v1/analytics/dashboards/` - Dashboard management
- `/api/v1/analytics/kpis/` - KPI management

## 🗄️ Database Models

The system uses a multi-tenant architecture where each company's data is isolated. Key models include:

- **Core**: User, Company, Branch, Role, CompanyUser, AuditLog
- **Accounting**: ChartOfAccounts, JournalEntry, JournalLine, FinancialStatement
- **Sales**: Customer, Invoice, InvoiceItem
- **Inventory**: Product, Warehouse, Stock, StockMovement
- **Payments**: PaymentGateway, Payment
- **Banking**: BankAccount, BankTransaction
- **AI Engine**: AIModel, AIPrediction, AIRecommendation, AIAuditLog
- **CRM**: Lead, Opportunity
- **HR**: Employee, Payroll, Contract
- **Purchases**: Supplier, PurchaseOrder, PurchaseOrderItem
- **Documents**: Document, VoiceCommand
- **Tasks**: Task
- **Identity**: Identity, IdentityDocument, FaceVerification
- **Legal**: Incident, IncidentEvidence, LegalReport, Blacklist
- **Analytics**: Dashboard, KPI

## 🤖 AI Features

The platform includes AI-powered features:

- **Cash Flow Prediction**: Forecast future cash flow based on historical data
- **Sales Forecasting**: Predict sales trends
- **Demand Forecasting**: Predict inventory demand
- **Fraud Detection**: Detect suspicious transactions
- **Payment Prediction**: Predict payment likelihood
- **Expense Classification**: Automatically classify expenses
- **Document OCR**: Extract data from documents
- **Voice Commands**: Process voice commands

## 🔒 Security

- JWT token-based authentication
- 2FA support (TOTP)
- Biometric authentication support
- Role-based access control (RBAC)
- Complete audit trail
- Data encryption at rest and in transit

## 📝 Postman Collection

Import the `Finory_IA.postman_collection.json` file into Postman to access all API endpoints with example requests.

## 🚀 Deployment

### Production Settings

1. Set `DEBUG=False` in settings
2. Configure PostgreSQL database
3. Set up Redis for Celery
4. Configure environment variables
5. Set up static file serving
6. Configure SSL/TLS

## 📄 License

[Your License Here]

## 👥 Contributors

[Your Team Here]

## 📞 Support

For support, email support@finoryia.com or create an issue in the repository.

---

**Built with  using Django and AI**
