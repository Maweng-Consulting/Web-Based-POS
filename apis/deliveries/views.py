from rest_framework.response import Response
from rest_framework import status, generics
from rest_framework.permissions import IsAuthenticated

from apps.deliveries.models import DeliveryAddress, PickupStation
from apis.deliveries.serializers import DeliveryAddressSerializer, PickupStationSerializer

class PickupStationAPIView(generics.ListAPIView):
    queryset = PickupStation.objects.all()
    serializer_class = PickupStationSerializer


class DeliveryAddressAPIView(generics.ListCreateAPIView):
    queryset = DeliveryAddress.objects.all()
    serializer_class = DeliveryAddressSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        return self.queryset.filter(customer__user=user)

class DeliveryAddressDetailAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = DeliveryAddress.objects.all()
    serializer_class = DeliveryAddressSerializer
    permission_classes = [IsAuthenticated]

    lookup_field = "pk"