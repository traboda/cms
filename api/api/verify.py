from django.http import JsonResponse
from django.views import View

from api.utils.decorator import verify_API_key


class VerifyTokenAPI(View):

    @staticmethod
    @verify_API_key
    def get(request, *args, **kwargs):
        return JsonResponse('Valid Token', status=200)


__all__ = [
    'VerifyTokenAPI'
]
