import json
from functools import wraps

from django.http import HttpResponse

from api.models import APIToken


def verify_API_key(resolver):
    """
    Decorator to check if a request has valid API key.
    """

    @wraps(resolver)
    def wrapper(request, *args, **kwargs):
        key = request.headers.get('Authorization')
        if key is not None:
            key = key.split(' ')[1]
        if key is None:
            body = request.body.decode('utf-8')
            if body != '' and request.content_type == 'application/json':
                data = json.loads(body)
                if 'siteKey' in data.keys():
                    key = data['siteKey']
        if key is None:
            return HttpResponse('A siteKey is required to interact with the API', status=401)
        try:
            token = APIToken.objects.get(token=key)
            request.token = token
            return resolver(request, *args, **kwargs)
        except APIToken.DoesNotExist:
            return HttpResponse('Invalid siteKey provided. Your request could not be processed.', status=401)

    return wrapper


__all__ = [
    'verify_API_key'
]
