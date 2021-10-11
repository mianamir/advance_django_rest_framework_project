"""
Provides a set of pluggable jwt auth policies.
"""
import json
import jwt
from django.contrib.auth import get_user_model

from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework_simplejwt.exceptions import InvalidToken

from mvpsite.settings import SECRET_KEY
from users.models import UserProfile
from users.constants import ( 
    ADMIN, 
    SELLER, 
    BUYER
)

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
            print(f'user object found: {str(user)}')
            if user:
                up_obj = UserProfile.objects.get(user_id=user.id)
                print(f'user profile object found: {str(up_obj)},\
                 role: {str(up_obj.role)}, current deposit: {up_obj.deposit}')

                # users with a “buyer” role can deposit 5, 10, 20, 50 and 100 cent 
                # coins into their vending machine account

                if up_obj and up_obj.role == BUYER:
                    return (user, None)
            
        except InvalidToken as it_ex:
            print(f'User has not valid data to perform this action, error: {it_ex}')
            return (None, None)

        print(f'Unable to perform this action, please check your input.')
        return (None, None)


class CustomJWTAuthenticationSeller(JWTAuthentication):
    def authenticate(self, request):
        print(f'request obj: {request}')
        token = request.META.get('HTTP_AUTHORIZATION', " ").split(' ')[1]
        print(f'Access token: {token}')
        try:
            print(f'decoding access token...')
            payload = jwt.decode(jwt=token, key=SECRET_KEY, algorithms=['HS256'])
            print(f'decode access token payload: {payload}')
            user = User.objects.get(id=payload['user_id'])
            print(f'user object found: {str(user)}')
            if user:
                up_obj = UserProfile.objects.get(user_id=user.id)
                print(f'user profile object found: {str(up_obj)},\
                 role: {str(up_obj.role)}, current deposit: {up_obj.deposit}')

                if up_obj and up_obj.role == SELLER:
                    return (user, None)
            
        except InvalidToken as it_ex:
            print(f'User has not valid data to perform this action, error: {it_ex}')
            return (None, None)

        print(f'Unable to perform this action, please check your input.')
        return (None, None)