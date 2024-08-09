from django.urls import path
from apis.products.views import (
    ProductListAPIView,
    ProductImageAPIView,
    ProductCategoryAPIView,
    ProductDetailAPIView,
)
from apis.orders.views import PlaceOrderAPIView
from rest_framework_simplejwt.views import TokenVerifyView
from apis.users.views import RegisterUserAPIView

from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
    TokenVerifyView,
)


urlpatterns = [
    # Users Management
    path("users/register/", RegisterUserAPIView.as_view(), name="register"),
    path("users/login/", TokenObtainPairView.as_view(), name="login"),
    path("users/token/refresh/", TokenRefreshView.as_view(), name="refresh-token"),
    path("users/token/verify/", TokenVerifyView.as_view(), name="verify-token"),
    # Products
    path("products/", ProductListAPIView.as_view(), name="products"),
    path("products/<int:pk>/", ProductDetailAPIView.as_view(), name="product-details"),
    path("products/images/", ProductImageAPIView.as_view(), name="images"),
    path("place-order/", PlaceOrderAPIView.as_view(), name="place-order"),
    # Categories
    path("categories/", ProductCategoryAPIView.as_view(), name="categories"),
]
