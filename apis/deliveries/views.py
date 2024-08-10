from django.db.models import Q
from rest_framework.response import Response
from rest_framework import status, generics
from rest_framework.permissions import IsAuthenticated

from apps.deliveries.models import DeliveryAddress, PickupStation, County, Town
from apis.deliveries.serializers import DeliveryAddressSerializer, PickupStationSerializer, CountySerializer, TownSerializer

class CountyAPIView(generics.ListAPIView):
    queryset = County.objects.all()
    serializer_class = CountySerializer

class TownAPIView(generics.ListAPIView):
    queryset = Town.objects.all()
    serializer_class = TownSerializer

    def get_queryset(self):
        county = self.request.query_params.get("county")
        if county:
            return self.queryset.filter(county_id=county)
        return super().get_queryset()

class PickupStationAPIView(generics.ListAPIView):
    queryset = PickupStation.objects.all()
    serializer_class = PickupStationSerializer

    def get_queryset(self):
        county = self.request.query_params.get("county")
        town = self.request.query_params.get("town")

        if county and town:
            return self.queryset.filter(county_id=county, town_id=town)
        elif county:
            return self.queryset.filter(county_id=county)
        elif town:
            return self.queryset.filter(town_id=town)
        
        return super().get_queryset()


class DeliveryAddressAPIView(generics.ListCreateAPIView):
    queryset = DeliveryAddress.objects.all()
    serializer_class = DeliveryAddressSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        return self.queryset.filter(Q(customer__user=user) | Q(customer__user__username="walkin@gmail.com"))

class DeliveryAddressDetailAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = DeliveryAddress.objects.all()
    serializer_class = DeliveryAddressSerializer
    permission_classes = [IsAuthenticated]

    lookup_field = "pk"