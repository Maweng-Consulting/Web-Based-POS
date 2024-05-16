from django.urls import path
from apis.products.views import ProductListAPIView, ProductImageAPIView

urlpatterns = [
    path("products/", ProductListAPIView.as_view(), name="products"),
    path("products/<int:product_id>/images/", ProductImageAPIView.as_view(), name="images"),
]