from rest_framework import serializers
from apps.deliveries.models import DeliveryAddress, PickupStation, Town, County

class DeliveryAddressSerializer(serializers.ModelSerializer):
    pick_at = serializers.SerializerMethodField()
    class Meta:
        model = DeliveryAddress
        fields = "__all__"

    def get_pick_at(self, obj):
        return obj.pickup_station.name if obj.pickup_station else obj.description

class PickupStationSerializer(serializers.ModelSerializer):
    county_name = serializers.SerializerMethodField()
    town_name = serializers.SerializerMethodField()

    class Meta:
        model = PickupStation
        fields = "__all__"

    def get_county_name(self, obj):
        return obj.county.name if obj.county else ""
    
    def get_town_name(self, obj):
        return obj.town.name if obj.town else ""


class CountySerializer(serializers.ModelSerializer):
    class Meta:
        model = County
        fields = "__all__"



class TownSerializer(serializers.ModelSerializer):
    class Meta:
        model = Town
        fields = "__all__"