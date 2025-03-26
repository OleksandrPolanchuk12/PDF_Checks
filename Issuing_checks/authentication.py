from rest_framework.authentication import BaseAuthentication
from rest_framework.exceptions import AuthenticationFailed
from rest_framework_api_key.models import APIKey
from rest_framework.response import Response

class APIKeyAuthentication(BaseAuthentication):
    def authenticate(self, request):
        api_key = request.headers.get('Authorization')

        if not api_key:
            raise AuthenticationFailed('API Key is required')

        if api_key.startswith('Api-Key '):
            api_key = api_key.replace('Api-Key ', '')

        try:
            api_key_obj = APIKey.objects.get_from_key(api_key)
        except APIKey.DoesNotExist:
            raise AuthenticationFailed('Invalid API Key')
        return (None, api_key_obj)