"""
WSGI config for finory_ia project.
"""

import os

from django.core.wsgi import get_wsgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'finory_ia.settings')

application = get_wsgi_application()
