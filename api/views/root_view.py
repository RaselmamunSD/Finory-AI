"""
Root API view - Shows API information
"""
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework import serializers


class APIRootSerializer(serializers.Serializer):
    """Serializer for API root endpoint documentation"""
    pass


@api_view(['GET'])
@permission_classes([AllowAny])
def api_root(request):
    """
    Root API endpoint - Returns API information and available endpoints
    """
    return Response({
        'success': True,
        'message': 'Welcome to Finory IA API',
        'version': '1.0.0',
        'documentation': {
            'postman_collection': '/Finory_IA.postman_collection.json',
            'admin_panel': '/admin/',
        },
        'endpoints': {
            'authentication': {
                'register': '/api/v1/auth/register/',
                'login': '/api/v1/auth/login/',
                'refresh': '/api/v1/auth/refresh/',
                'verify_2fa': '/api/v1/auth/verify-2fa/',
            },
            'core': {
                'companies': '/api/v1/companies/',
                'users': '/api/v1/users/',
                'branches': '/api/v1/branches/',
                'roles': '/api/v1/roles/',
            },
            'accounting': {
                'accounts': '/api/v1/accounting/accounts/',
                'journal_entries': '/api/v1/accounting/journal-entries/',
                'financial_statements': '/api/v1/accounting/financial-statements/',
            },
            'sales': {
                'customers': '/api/v1/sales/customers/',
                'invoices': '/api/v1/sales/invoices/',
            },
            'inventory': {
                'products': '/api/v1/inventory/products/',
                'warehouses': '/api/v1/inventory/warehouses/',
                'stock': '/api/v1/inventory/stock/',
                'stock_movements': '/api/v1/inventory/stock-movements/',
            },
            'payments': {
                'gateways': '/api/v1/payments/gateways/',
                'payments': '/api/v1/payments/payments/',
            },
            'banking': {
                'accounts': '/api/v1/banking/accounts/',
                'transactions': '/api/v1/banking/transactions/',
            },
            'ai_engine': {
                'predictions': '/api/v1/ai/predictions/',
                'recommendations': '/api/v1/ai/recommendations/',
                'models': '/api/v1/ai/models/',
            },
            'crm': {
                'leads': '/api/v1/crm/leads/',
                'opportunities': '/api/v1/crm/opportunities/',
            },
            'hr': {
                'employees': '/api/v1/hr/employees/',
                'payrolls': '/api/v1/hr/payrolls/',
                'contracts': '/api/v1/hr/contracts/',
            },
            'purchases': {
                'suppliers': '/api/v1/purchases/suppliers/',
                'purchase_orders': '/api/v1/purchases/purchase-orders/',
            },
            'documents': {
                'documents': '/api/v1/documents/documents/',
                'voice_commands': '/api/v1/documents/voice-commands/',
            },
            'tasks': {
                'tasks': '/api/v1/tasks/tasks/',
            },
            'identity': {
                'identities': '/api/v1/identity/identities/',
                'verifications': '/api/v1/identity/verifications/',
            },
            'legal': {
                'incidents': '/api/v1/legal/incidents/',
                'legal_reports': '/api/v1/legal/legal-reports/',
                'blacklist': '/api/v1/legal/blacklist/',
            },
            'analytics': {
                'dashboards': '/api/v1/analytics/dashboards/',
                'kpis': '/api/v1/analytics/kpis/',
            },
        },
        'meta': {
            'status': 'operational',
            'framework': 'Django REST Framework',
        }
    })
