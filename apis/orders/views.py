from rest_framework.response import Response
from rest_framework import generics, status
from rest_framework.permissions import IsAuthenticated

from apis.orders.serializers import PlaceOrderSerializer


class PlaceOrderAPIView(generics.CreateAPIView):
    serializer_class = PlaceOrderSerializer
    permission_classes = [IsAuthenticated]

    def get_serializer_context(self):
        return {"user": self.request.user}

    def create(self, request, *args, **kwargs):
        return super().create(request, *args, **kwargs)
