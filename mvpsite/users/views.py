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
from users.constants import (
    AMOUNT_DATA
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
    queryset = User.objects.all()


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