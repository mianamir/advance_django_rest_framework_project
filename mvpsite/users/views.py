from rest_framework import generics
from rest_framework.views import APIView
from rest_framework.permissions import (
    IsAuthenticated,
    AllowAny
)
from rest_framework.authentication import (
    BasicAuthentication,
    SessionAuthentication
)
from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework import status
from django.contrib.auth import get_user_model
from rest_framework_simplejwt.views import TokenObtainPairView

User = get_user_model()

from .serializers import (
    MyTokenObtainPairSerializer,
    RegisterSerializer,
    UserSerializer
)
from .models import (
    UserProfile, 
    get_user_by_id, 
    get_user_profile_by_id
    )
from products.models import (
    get_product_by_id, 
    Product, 
    BuyerPurchase
    )
from users.constants import (
    AMOUNT_DATA, 
    ADMIN, 
    SELLER, 
    BUYER
)

from custom_helpers.custom_responses import (
    get_success_response,
    get_failure_response
)

from custom_helpers.messages import (
    VENDING_MACHINE_COINS_VALID_MESSAGE
)

from custom_helpers.custom_jwt_authentication import CustomJWTAuthentication


class MyObtainTokenPairView(TokenObtainPairView):
    permission_classes = (AllowAny,)
    serializer_class = MyTokenObtainPairSerializer


class RegisterView(generics.CreateAPIView):
    queryset = User.objects.all()
    permission_classes = (AllowAny,)
    serializer_class = RegisterSerializer


class LogoutView(APIView):
    permission_classes = (IsAuthenticated,)

    def post(self, request):
        try:
            refresh_token = request.data["refresh_token"]
            token = RefreshToken(refresh_token)
            token.blacklist()

            return Response(status=status.HTTP_205_RESET_CONTENT)
        except Exception as e:
            return Response(status=status.HTTP_400_BAD_REQUEST)


class UserViewSet(viewsets.ModelViewSet):
    """
    A viewset for getting users instances.
    """
    permission_classes = list()
    serializer_class = UserSerializer
    queryset = User.objects.order_by('-id').all()


class CreateUserAPIView(APIView):
    authentication_classes = []
    permission_classes = []

    def post(self, request):
        data = request.data

        # get user profile data
        role = data.pop('role')
        deposit = data.pop('deposit')

        try:
            user = User.objects.create(**data)

            user.set_password(data['password'])
            user.save()
            
            print(f'User created: {str(user)}')

            if user:
                # prepare the request data for user profile
                up_data = dict()

                up_data['user_id'] = user.id
                up_data['role'] =  role
                up_data['deposit'] = deposit
                up_data['reset_deposit'] = deposit
                    
                # save user profile
                user_profile_obj = UserProfile.objects.create(**up_data)

                # prepare the final response
                
                res = {
                    'id': user.id, 
                    'first_name': user.first_name, 
                    'last_name': user.last_name, 
                    'username': user.username, 
                    'email': user.email 
                }

                # append user profile data into the final response

                res['role'] = user_profile_obj.role
                res['deposit'] = user_profile_obj.deposit

                data = {'data': res}

                return Response(get_success_response(**data), 
                status=status.HTTP_201_CREATED)        
        except Exception as e:
            print(e)
            return Response(get_failure_response(**{'error': e}), 
            status=status.HTTP_400_BAD_REQUEST)

        return Response(get_failure_response(), 
        status=status.HTTP_400_BAD_REQUEST)


class DepositAPIView(APIView):
    authentication_classes = [CustomJWTAuthentication,]
    permission_classes = [IsAuthenticated, ]

    def deposit_amount(self, *args, **kwargs):
        try:
            user = User.objects.get(id=kwargs['user_id'])
        except User.DoesNotExist as u_ex:
            print(f'User not found for #{kwargs["user_id"]} ID.')
            return None
        else:
            if user:
                # get user profile obj
                up_obj = UserProfile.objects.get(user_id=user.id)

                # users with a ???buyer??? role can deposit 5, 10, 20, 50 
                # and 100 cent coins into their vending machine account
                print(f'User #{kwargs["user_id"]} ID \
                is depositing {kwargs["deposit"]} amount in vending machine account')

                up_obj.deposit += kwargs['deposit']
                up_obj.save()

                return user, up_obj


    def post(self, request):
        print(f'User is authenticated using JWT token: {request.user.id}')
        data = request.data
        try:
            deposit = data['deposit']
            if deposit in AMOUNT_DATA:

                user_req = {
                    'user_id': request.user.id,
                    'deposit': deposit
                }

                user, up = self.deposit_amount(**user_req)

                res = {
                    'id': user.id, 
                    'first_name': user.first_name, 
                    'last_name': user.last_name, 
                    'username': user.username, 
                    'email': user.email,
                    'role': up.role,
                   'deposit': up.deposit
                }

                data = {"data": res}
                return Response(get_success_response(**data), status=status.HTTP_200_OK)
        except Exception as e:
            return Response(get_failure_response(**{'error': e}), 
            status=status.HTTP_400_BAD_REQUEST)

        return Response(get_failure_response(**{'error': VENDING_MACHINE_COINS_VALID_MESSAGE}), 
        status=status.HTTP_406_NOT_ACCEPTABLE)


class BuyAPIView(APIView):
    authentication_classes = [CustomJWTAuthentication,]
    permission_classes = [IsAuthenticated, ]

    def buy_product(self, *args, **kwargs):
        try:
            # product object
            product = get_product_by_id(**kwargs)

            # user object
            user = get_user_by_id(**kwargs)

            # user profile object
            up_obj = get_user_profile_by_id(**kwargs)

            if product and user and up_obj:
                res_obj = BuyerPurchase.objects.create(
                    purchase_price=kwargs['purchase_price'], 
                    product=product, 
                    buyer=user
                    )

                # update the user profile obj
                if up_obj.deposit > res_obj.purchase_price:
                        up_obj.deposit -= res_obj.purchase_price
                        up_obj.save()

                # prepare the response

                purchases_objs = BuyerPurchase.objects.filter(user_id=kwargs['user_id']).all()

                total_purchase = 0.0

                list_products = list()

                for purchase in purchases_objs:
                    total_purchase += purchase.purchase_price

                    product = get_product_by_id(**{'product_id': purchase.product_id})

                    if product:
                        list_products.append({
                            'id': product.id,
                            'product_name': product.product_name
                        })


                res = {
                    'total_purchase': total_purchase,
                    'list_products': list_products
                }
                return res
        except:
            return None

        return None

    def post(self, request):
        
        user = request.user

        print(f'User is authenticated using JWT token: {user.id}')

        data = request.data

        try:
            if 'product_id' in data and 'product_amount' in data:

                product_req = {
                    'user_id': user.id,
                    'purchase_price': data['product_amount'],
                    'product_id': data['product_id']
                }

                res_obj = self.buy_product(**product_req)

                data = {"data": res_obj}
                return Response(get_success_response(**data), status=status.HTTP_200_OK)
        except Exception as e:
            return Response(get_failure_response(**{'error': str(e)}), 
            status=status.HTTP_400_BAD_REQUEST)

        return Response(get_failure_response(**{'error': VENDING_MACHINE_COINS_VALID_MESSAGE}), 
        status=status.HTTP_406_NOT_ACCEPTABLE)



class ResetVendingMachineAccountAPIView(APIView):
    authentication_classes = [CustomJWTAuthentication,]
    permission_classes = [IsAuthenticated, ]

    def reset_user(self, *args, **kwargs):
        try:
            # user profile object
            up_obj = get_user_profile_by_id(**kwargs)
            up_obj.deposit = up_obj.reset_deposit
            up_obj.save()

        except:
            print(f'User not found for #{kwargs["user_id"]} ID.')
            return None

        return None

    def post(self, request):
        
        user = request.user

        print(f'User is authenticated using JWT token: {user.id}')

        data = request.data

        try:
            if user:

                user_req = {
                    'user_id': user.id
                }

                res_obj = self.reset_user(**user_req)

                res = "Reset user for current products purchases"

                data = {"data": res}
                return Response(get_success_response(**data), status=status.HTTP_200_OK)
        except Exception as e:
            return Response(get_failure_response(**{'error': str(e)}), 
            status=status.HTTP_400_BAD_REQUEST)

        return Response(get_failure_response(**{'error': VENDING_MACHINE_COINS_VALID_MESSAGE}), 
        status=status.HTTP_406_NOT_ACCEPTABLE)