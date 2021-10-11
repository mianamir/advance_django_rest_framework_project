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
from custom_helpers.custom_jwt_authentication import CustomJWTAuthentication
# from rest_framework_simplejwt.authentication import JWTAuthentication


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

                return Response(get_success_response(**data), status=status.HTTP_201_CREATED)        
        except Exception as e:
            print(e)
            return Response(f'{get_failure_response()}, {e}', 
            status=status.HTTP_400_BAD_REQUEST)

        return Response(get_failure_response(), status=status.HTTP_406_NOT_ACCEPTABLE)


class DepositAPIView(APIView):
    authentication_classes = [CustomJWTAuthentication,]
    permission_classes = [IsAuthenticated, ]

    def post(self, request):
        try:
            deposit_amount = request.data.get("deposit_amount")
            if deposit_amount in AMOUNT_DATA:
                data = {"data": deposit_amount}
                return Response(get_success_response(**data), status=status.HTTP_200_OK)
        except Exception as e:
            return Response(get_failure_response(), status=status.HTTP_400_BAD_REQUEST)

        return Response(get_failure_response(), status=status.HTTP_406_NOT_ACCEPTABLE)