from django.urls import path
from apis.products.views import ProductListAPIView, ProductImageAPIView
from apis.orders.views import PlaceOrderAPIView
from rest_framework_simplejwt.views import TokenVerifyView

from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
    TokenVerifyView,
)


urlpatterns = [
    path('users/login/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('users/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('users/token/verify/', TokenVerifyView.as_view(), name='token_verify'),
    path("products/", ProductListAPIView.as_view(), name="products"),
    path("products/images/", ProductImageAPIView.as_view(), name="images"),
    path("place-order/", PlaceOrderAPIView.as_view(), name="place-order"),
]