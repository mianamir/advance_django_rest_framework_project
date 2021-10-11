from django.urls import path
from .views import (
    ProductViewSet, 
    ProductWithSellerAPIView, 
    ProductWithSellerUpdateAPIView, 
    ProductWithSellerDeleteAPIView
)

from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register(r'products', ProductViewSet, basename='products')

urlpatterns = [
    path('products/create/', 
    ProductWithSellerAPIView.as_view(), 
    name='create'),
    path('products/update/<int:pk>/', 
    ProductWithSellerUpdateAPIView.as_view(), 
    name='update'),
    path('products/delete/<int:pk>/', 
    ProductWithSellerDeleteAPIView.as_view(), 
    name='delete')
]



urlpatterns += router.urls


