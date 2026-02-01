"""
ASGI config for finory_ia project.
"""

import os

from django.core.asgi import get_asgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'finory_ia.settings')

application = get_asgi_application()
