from django.db.models import Q
from rest_framework.response import Response
from rest_framework import status, generics
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.permissions import IsAuthenticated
from apps.core.custom_pagination import NoPagination

from apps.deliveries.models import DeliveryAddress, PickupStation, County, Town, SubCounty, Ward
from apis.deliveries.serializers import (
    DeliveryAddressSerializer,
    PickupStationSerializer,
    CountySerializer,
    TownSerializer,
    SubCountySerializer,
    WardSerializer
)


class CountyAPIView(generics.ListAPIView):
    queryset = County.objects.all()
    serializer_class = CountySerializer
    pagination_class = NoPagination


class SubCountyAPIView(generics.ListAPIView):
    queryset = SubCounty.objects.all()
    serializer_class = SubCountySerializer
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ["county", "county__name"]

    pagination_class = NoPagination

class WardAPIView(generics.ListAPIView):
    queryset = Ward.objects.all()
    serializer_class = WardSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ["sub_county", "sub_county__name"]

    pagination_class = NoPagination


class PickupStationAPIView(generics.ListAPIView):
    queryset = PickupStation.objects.all()
    serializer_class = PickupStationSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ["ward", "ward__name"]

    pagination_class = NoPagination

    def get_queryset(self):
        station_type = self.request.query_params.get("station_type")
        if station_type:
            return self.queryset.filter(station_type=station_type)
        return super().get_queryset()


class DeliveryAddressAPIView(generics.ListCreateAPIView):
    queryset = DeliveryAddress.objects.all()
    serializer_class = DeliveryAddressSerializer
    permission_classes = [IsAuthenticated]

    pagination_class = NoPagination


class DeliveryAddressDetailAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = DeliveryAddress.objects.all()
    serializer_class = DeliveryAddressSerializer
    permission_classes = [IsAuthenticated]

    lookup_field = "pk"
