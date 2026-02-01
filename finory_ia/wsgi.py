"""
WSGI config for finory_ia project.
"""
# Python 3.14: patch Django BaseContext.__copy__ before any Django code runs
import sys
if sys.version_info >= (3, 14):
    from copy import copy
    from django.template.context import BaseContext
    def _base_context_copy(self):
        duplicate = BaseContext()
        duplicate.__class__ = self.__class__
        duplicate.__dict__.update(copy(self.__dict__))
        duplicate.dicts = self.dicts[:]
        return duplicate
    BaseContext.__copy__ = _base_context_copy

import os

from django.core.wsgi import get_wsgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'finory_ia.settings')

application = get_wsgi_application()
