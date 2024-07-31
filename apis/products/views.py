from rest_framework import generics, status
from rest_framework.response import Response

from apps.inventory.models import Inventory, ProductImage, ProductCategory
from apis.products.serializers import ProductSerializer, ProductImageSerializer, ProductCategorySerializer


class ProductListAPIView(generics.ListAPIView):
    queryset = Inventory.objects.all()
    serializer_class = ProductSerializer

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