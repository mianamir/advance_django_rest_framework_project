"""
Provides a set of pluggable permission policies.
"""

from rest_framework.permissions import (
    BasePermission,
    SAFE_METHODS
)

from users.constants import (
    UNSAFE_REQUEST_METHODS
)
from custom_helpers.messages import (
    ADD_RECORD_NOT_ALLOWED
)


class CustomReadOnly(BasePermission):

    message = ADD_RECORD_NOT_ALLOWED

    def has_permission(self, request, view):
        if request.method in SAFE_METHODS:
            #'user': str(request.user),  # `django.contrib.auth.User` instance.
            #'auth': str(request.auth),  # None
            return True


class IsOwnerOrReadOnly(BasePermission):
    """
    Object-level permission to only allow owners of an object to edit it.
    Assumes the model instance has an `owner` attribute.
    """

    def has_object_permission(self, request, view, obj):
        # Read permissions are allowed to any request,
        # so we'll always allow GET, HEAD or OPTIONS requests.
        if request.method in SAFE_METHODS:
            return True

        # Instance must have an attribute named `owner`.
        # return obj.owner == request.user
        return bool(request.user and request.user.is_authenticated)