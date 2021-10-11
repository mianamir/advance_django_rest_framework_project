from django.urls import path
from rest_framework.routers import DefaultRouter

"""
JSON Web Token Authentication
JSON Web Token is a fairly new standard which can be used for token-based authentication. 
Unlike the built-in TokenAuthentication scheme, JWT Authentication doesn't need to use a 
database to validate a token. A package for JWT authentication is djangorestframework-simplejwt 
which provides some features as well as a pluggable token blacklist app.
ref: https://www.django-rest-framework.org/api-guide/authentication/
"""
from rest_framework_simplejwt.views import (
    TokenRefreshView,
    TokenVerifyView
)

from users.views import (
    MyObtainTokenPairView,
    RegisterView,
    LogoutView,
    UserViewSet,
    DepositAPIView, 
    CreateUserAPIView, 
    BuyAPIView
)

router = DefaultRouter()
router.register(r'users', UserViewSet, basename='users')


urlpatterns = [
    path('login/', MyObtainTokenPairView.as_view(), name='token_obtain_pair'),
    path('token-refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('token-verify/', TokenVerifyView.as_view(), name='token_verify'),
    path('register/', RegisterView.as_view(), name='auth_register'),
    path('logout/', LogoutView.as_view(), name='auth_logout'),
    path('deposit/', DepositAPIView.as_view(), name='deposit'),
    path('users/create/', CreateUserAPIView().as_view(), name='create'),
    path('buy/', BuyAPIView.as_view(), name='buy'),
]


urlpatterns += router.urls
