from rest_framework import generics, status
from rest_framework.response import Response

from apps.inventory.models import Inventory, ProductImage
from apis.products.serializers import ProductSerializer, ProductImageSerializer


class ProductListAPIView(generics.ListAPIView):
    queryset = Inventory.objects.all()
    serializer_class = ProductSerializer

class ProductImageAPIView(generics.ListCreateAPIView):
    queryset = ProductImage.objects.all()
    serializer_class = ProductImageSerializer

    def get(self, request, product_id, *args, **kwargs):
        images = ProductImage.objects.filter(product_id=product_id)
        serializer = self.serializer_class(instance=images, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
        #return super().get(request, *args, **kwargs)