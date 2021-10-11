"""
Provides a set of pluggable custom permission policies.
"""

from django.contrib.auth import get_user_model
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
from users.constants import (
    AMOUNT_DATA, 
    ADMIN, 
    SELLER, 
    BUYER
)
from users.models import UserProfile
from products.models import Product

User = get_user_model()


class IsOwnerOrReadOnly(BasePermission):
    """
    Object-level permission to only allow owners of an object to edit it.

    """

    def has_permission(self, request, view):

        if request.method in SAFE_METHODS:
            
            return True

    def has_object_permission(self, request, view, obj):
        # Read permissions are allowed to any request,
        # so we'll always allow GET, HEAD or OPTIONS requests.
        if request.method in SAFE_METHODS:
            return True

        if request.method in UNSAFE_REQUEST_METHODS:
            try:
                obj = Product.objects.get(seller_id=user.id)
            except Product.DoesNotExist as u_ex:
                print(f'Product not found for seller with #{request.user.id} ID.')
                return None
            else:
                if obj:
                    return True
        return False