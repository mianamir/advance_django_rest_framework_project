"""
Provides a set of pluggable jwt auth policies.
"""
import json
import jwt
from django.contrib.auth import get_user_model

from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework_simplejwt.exceptions import InvalidToken

from mvpsite.settings import SECRET_KEY

User = get_user_model()


class CustomJWTAuthentication(JWTAuthentication):
    def authenticate(self, request):
        print(f'request obj: {request}')
        token = request.META.get('HTTP_AUTHORIZATION', " ").split(' ')[1]
        print(f'Access token: {token}')
        try:
            print(f'decoding access token...')
            payload = jwt.decode(jwt=token, key=SECRET_KEY, algorithms=['HS256'])
            print(f'decode access token payload: {payload}')
            user = User.objects.get(id=payload['user_id'])
            print(f'user object found: {user}')
            if user.is_active:
                return (user, None)
            # return super().authenticate(request=request)
        except InvalidToken:
            return None
        return None