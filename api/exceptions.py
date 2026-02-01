"""
Custom exception handlers for API
"""
from rest_framework.views import exception_handler
from rest_framework.response import Response
from rest_framework import status
import logging

logger = logging.getLogger(__name__)


def custom_exception_handler(exc, context):
    """
    Custom exception handler that returns consistent error format
    """
    response = exception_handler(exc, context)
    
    if response is not None:
        custom_response_data = {
            'success': False,
            'error': {
                'code': response.status_code,
                'message': str(exc),
                'details': response.data if isinstance(response.data, dict) else {'errors': response.data}
            },
            'meta': {
                'timestamp': None,  # Will be set by middleware
                'request_id': None
            }
        }
        response.data = custom_response_data
    
    return response
