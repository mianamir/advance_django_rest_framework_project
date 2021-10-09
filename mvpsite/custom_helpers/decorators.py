from rest_framework.response import Response
from rest_framework import status
from django.http import Http404

from users.constants import (
    ADMIN,
    SELLER,
    BUYER
)

def custom_unauthenticated_user(view_func):
    def wrapper_func(request, *args, **kwargs):
        if request.user.is_authenticated:
            return view_func(request, *args, **kwargs)
        else:
            return Response(f'You are not login.')

        return wrapper_func


def custom_allowed_users(allowed_roles=list()):
    def decorator(view_func):
        def wrapper_func(request, *args, **kwargs):
            group = None
            if request.user.groups.exist():
                group = request.user.groups.all()[0].name

            if group in allowed_roles:
                return view_func(request, *args, **kwargs)
            else:
                return Response(f'You are not authorized to this page.')

        return wrapper_func

    return decorator

def custom_admin_only(view_func):
    def wrapper_func(request, *args, **kwargs):
        group = None
        if request.user.groups.exist():
            group = request.user.groups.all()[0].name

        if group == BUYER:
            return Response(f'{BUYER} API accessed.')

        if group == SELLER:
            return Response(f'{SELLER} API accessed.')

        if group == ADMIN:
            return return view_func(request, *args, **kwargs)

        else:
            return Response(f'You are not authorized to this page.')

    return wrapper_func
