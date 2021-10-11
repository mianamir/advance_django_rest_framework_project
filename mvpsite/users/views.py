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
from .models import UserProfile
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

                # users with a “buyer” role can deposit 5, 10, 20, 50 
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
            user = User.objects.get(id=kwargs['user_id'])
        except User.DoesNotExist as u_ex:
            print(f'User not found for #{kwargs["user_id"]} ID.')
            return None
        else:
            if user:
                # get user profile obj
                up_obj = UserProfile.objects.get(user_id=user.id)

                print(f'User #{kwargs["user_id"]} ID \
                is depositing {kwargs["deposit"]} amount in vending machine account')

                up_obj.deposit += kwargs['deposit']
                up_obj.save()

                return user, up_obj


    def post(self, request):
        print(f'User is authenticated using JWT token: {request.user.id}')
        data = request.data
        try:
            buy_amount = data['buy_amount']
            if request.user and buy_amount:

                user_req = {
                    'user_id': request.user.id,
                    'buy_amount': buy_amount
                }

                user, up = self.buy_product(**user_req)

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