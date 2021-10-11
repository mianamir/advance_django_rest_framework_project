from rest_framework import generics
from rest_framework.permissions import (
    IsAuthenticated,
    IsAuthenticatedOrReadOnly,
    DjangoModelPermissions,
    DjangoModelPermissionsOrAnonReadOnly,
    AllowAny,
    IsAdminUser
)
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework import viewsets
from rest_framework.decorators import api_view

from .models import Product
from .serializers import ProductSerializer
from custom_helpers.custom_auth import CustomAuthentication
from custom_helpers.custompermissions import IsOwnerOrReadOnly
from custom_helpers.custom_jwt_authentication import (
    CustomJWTAuthentication,
    CustomJWTAuthenticationSeller
    )
from custom_helpers.custom_responses import (
    get_success_response,
    get_failure_response
)
from users.models import get_user_by_id



class ProductViewSet(viewsets.ModelViewSet):
    """
    A viewset for getting products instances.
    """
    authentication_classes = []
    permission_classes = []
    serializer_class = ProductSerializer
    queryset = Product.objects.order_by('-id').all()
    
    http_method_names = ['get']

class ProductWithSellerAPIView(APIView):
    authentication_classes = [CustomJWTAuthenticationSeller, ]
    permission_classes = [IsAuthenticated, ]

    def post(self, request):
        user = request.user
        print(f'User is authenticated using JWT token: {user.id}')

        data = request.data
        
        try:
            if 'product_name' in data and \
            'amount_available' in data and \
             'cost' in data:

                # add user as seller for this product data
                data['seller_id'] = user

                product = Product.objects.create(**data)

                print(f'Seller with #{user.id} ID, \
                has created the product: {str(product)}')

                if product:
                    data = {"data": ProductSerializer(product).data}
                    return Response(get_success_response(**data), 
                    status=status.HTTP_201_CREATED)
        except Exception as e:
            return Response(get_failure_response(**{'error': str(e)}), 
            status=status.HTTP_400_BAD_REQUEST)

        return Response(get_failure_response(**{'error': FAILED_RESPONSE_MESSAGE}), 
        status=status.HTTP_406_NOT_ACCEPTABLE)

   
class ProductWithSellerUpdateAPIView(APIView):
    authentication_classes = [CustomJWTAuthenticationSeller, ]
    permission_classes = [IsAuthenticated, ]

    def put(self, request, pk=None):
        user = request.user
        print(f'User is authenticated using JWT token: {user.id}')

        data = request.data
        
        try:
            id = pk
            product = Product.objects.get(pk=id)
            
            if product:

                if 'product_name' in data:
                    product.product_name = data['product_name']
                
                if 'amount_available' in data:
                    product.amount_available = data['amount_available']

                if 'cost' in data:
                    product.cost = data['cost']

                product.save()


            print(f'Seller with #{user.id} ID, \
            has updated the product: {str(product)}')
                
            data = {"data": ProductSerializer(product).data}
            return Response(get_success_response(**data), 
            status=status.HTTP_200_OK)

        except Exception as e:
            return Response(get_failure_response(**{'error': str(e)}), 
            status=status.HTTP_400_BAD_REQUEST)

        return Response(get_failure_response(**{'error': FAILED_RESPONSE_MESSAGE}), 
        status=status.HTTP_406_NOT_ACCEPTABLE)


class ProductWithSellerDeleteAPIView(APIView):
    authentication_classes = [CustomJWTAuthenticationSeller, ]
    permission_classes = [IsAuthenticated, ]

    def delete(self, request, pk=None):
        user = request.user
        print(f'User is authenticated using JWT token: {user.id}')

        data = request.data
        
        try:
            id = pk
            product = Product.objects.get(pk=id)

            product_copy = product
            
            if product:
                product.delete()


            print(f'Seller with #{user.id} ID, \
            has delete the product: {str(product_copy)}')
                
            data = {"data": ""}
            return Response(get_success_response(**data), 
            status=status.HTTP_204_NO_CONTENT)

        except Exception as e:
            return Response(get_failure_response(**{'error': str(e)}), 
            status=status.HTTP_400_BAD_REQUEST)

        return Response(get_failure_response(**{'error': FAILED_RESPONSE_MESSAGE}), 
        status=status.HTTP_406_NOT_ACCEPTABLE)

