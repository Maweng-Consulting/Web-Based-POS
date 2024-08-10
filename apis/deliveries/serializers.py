from rest_framework import serializers
from apps.deliveries.models import DeliveryAddress, PickupStation

class DeliveryAddressSerializer(serializers.ModelSerializer):
    class Meta:
        model = DeliveryAddress
        fields = "__all__"

class PickupStationSerializer(serializers.ModelSerializer):
    class Meta:
        model = PickupStation
        fields = "__all__"