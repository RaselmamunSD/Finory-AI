"""
Custom exception handlers for API
"""
from rest_framework.views import exception_handler
from rest_framework.response import Response
from rest_framework import status
from django.utils import timezone
import logging
import uuid

logger = logging.getLogger(__name__)


def custom_exception_handler(exc, context):
    """
    Custom exception handler that returns consistent error format
    """
    # Call REST framework's default exception handler first
    response = exception_handler(exc, context)
    
    # Get request from context
    request = context.get('request', None)
    request_id = getattr(request, 'id', str(uuid.uuid4())) if request else str(uuid.uuid4())
    
    if response is not None:
        # Extract error details
        error_details = response.data
        if isinstance(error_details, dict):
            # Handle validation errors
            if 'detail' in error_details:
                error_message = error_details['detail']
            elif 'non_field_errors' in error_details:
                error_message = error_details['non_field_errors']
            else:
                error_message = 'Validation error'
        elif isinstance(error_details, list):
            error_message = error_details[0] if error_details else 'An error occurred'
            error_details = {'errors': error_details}
        else:
            error_message = str(error_details)
            error_details = {'message': error_message}
        
        custom_response_data = {
            'success': False,
            'error': {
                'code': response.status_code,
                'message': str(error_message) if not isinstance(error_message, list) else error_message[0],
                'details': error_details if isinstance(error_details, dict) else {'errors': error_details}
            },
            'meta': {
                'timestamp': timezone.now().isoformat(),
                'request_id': request_id
            }
        }
        response.data = custom_response_data
    else:
        # Handle unexpected exceptions
        logger.exception(f'Unhandled exception: {exc}')
        custom_response_data = {
            'success': False,
            'error': {
                'code': status.HTTP_500_INTERNAL_SERVER_ERROR,
                'message': 'An unexpected error occurred',
                'details': {'exception': str(exc)} if logger.level <= logging.DEBUG else {}
            },
            'meta': {
                'timestamp': timezone.now().isoformat(),
                'request_id': request_id
            }
        }
        response = Response(custom_response_data, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    
    return response
