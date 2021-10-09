from rest_framework.authentication import (
    SessionAuthentication,
    BasicAuthentication,
    TokenAuthentication
)
from rest_framework import generics
from rest_framework.permissions import (
    IsAuthenticated,
    IsAuthenticatedOrReadOnly,
    DjangoModelPermissions,
    DjangoModelPermissionsOrAnonReadOnly,
    AllowAny,
    IsAdminUser
)
from django.http import Http404
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework import viewsets
from rest_framework.decorators import api_view

from .models import Product
from .serializers import ProductSerializer
from custom_helpers.custom_auth import CustomAuthentication
from custom_helpers.custompermissions import CustomReadOnly


class ProductViewSet(viewsets.ModelViewSet):
    """
    A viewset for getting products instances.
    """
    authentication_classes = [CustomAuthentication, ]
    permission_classes = [CustomReadOnly, ]
    serializer_class = ProductSerializer
    queryset = Product.objects.all()