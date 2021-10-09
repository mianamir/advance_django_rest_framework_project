"""
Provides a set of pluggable auth policies.
"""

from rest_framework.authentication import BaseAuthentication
from rest_framework.exceptions import AuthenticationFailed
from django.contrib.auth import get_user_model

User = get_user_model()


class CustomAuthentication(BaseAuthentication):
    def authenticate(self, request):
        username = request.GET.get('username')
        if username is None:
            return None
        try:
            user = User.objects.get(username=username)
        except User.DoesNotExist:
            raise AuthenticationFailed(f'No such user exist.')
        else:
            return (user, None)
        return None