from django.urls import path
from django.views.decorators.csrf import csrf_exempt

from .verify import VerifyTokenAPI

auth_apis = [
    path('verify/', csrf_exempt(VerifyTokenAPI.as_view())),
]

__all__ = [
    'auth_apis',
]
