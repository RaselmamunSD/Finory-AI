# Finory IA - Next Generation Financial Intelligence Platform

# Python 3.14 compatibility: fix BaseContext.__copy__ (Django < 4.2.27 uses copy(super()) which fails on 3.14)
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
