from rest_framework import generics, status
from rest_framework.response import Response
from django_filters.rest_framework import DjangoFilterBackend

from apps.inventory.models import Inventory, ProductImage, ProductCategory
from apis.products.serializers import (
    ProductSerializer,
    ProductImageSerializer,
    ProductCategorySerializer,
)
from apps.core.custom_pagination import NoPagination
from apis.products.filters import ProductFilter


class ProductListAPIView(generics.ListCreateAPIView):
    queryset = Inventory.objects.all().order_by("-created")
    serializer_class = ProductSerializer
    filter_backends = [DjangoFilterBackend]
    # filterset_fields = ["category__name", "name"]
    filterset_class = ProductFilter


class ProductDetailAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Inventory.objects.all()
    serializer_class = ProductSerializer

    lookup_field = "pk"


class ProductImageAPIView(generics.ListAPIView):
    queryset = ProductImage.objects.all()
    serializer_class = ProductImageSerializer

    def get(self, request, *args, **kwargs):
        params = self.request.query_params.get("product")
        queryset = self.queryset.filter(product_id=params).values()
        return Response(queryset)


class ProductCategoryAPIView(generics.ListCreateAPIView):
    queryset = ProductCategory.objects.all()
    serializer_class = ProductCategorySerializer
