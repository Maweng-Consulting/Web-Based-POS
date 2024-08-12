from rest_framework import serializers
from apps.deliveries.models import (
    DeliveryAddress,
    PickupStation,
    Town,
    County,
    Ward,
    SubCounty,
)


class DeliveryAddressSerializer(serializers.ModelSerializer):
    pick_at = serializers.SerializerMethodField()

    class Meta:
        model = DeliveryAddress
        fields = "__all__"

    def get_pick_at(self, obj):
        return obj.pickup_station.name if obj.pickup_station else obj.description


class PickupStationSerializer(serializers.ModelSerializer):
    county_name = serializers.SerializerMethodField()
    sub_county_name = serializers.SerializerMethodField()
    ward_name = serializers.SerializerMethodField()

    class Meta:
        model = PickupStation
        fields = "__all__"

    def get_county_name(self, obj):
        return obj.county.name if obj.county else ""

    def get_sub_county_name(self, obj):
        return obj.sub_county.name if obj.sub_county else ""
    
    def get_ward_name(self, obj):
        return obj.ward.name if obj.ward else ""


class CountySerializer(serializers.ModelSerializer):
    class Meta:
        model = County
        fields = "__all__"


class TownSerializer(serializers.ModelSerializer):
    class Meta:
        model = Town
        fields = "__all__"


class SubCountySerializer(serializers.ModelSerializer):
    county_name = serializers.SerializerMethodField()
    class Meta:
        model = SubCounty
        fields = "__all__"

    def get_county_name(self, obj):
        return obj.county.name if obj.county else ""


class WardSerializer(serializers.ModelSerializer):
    county_name = serializers.SerializerMethodField()
    sub_county_name = serializers.SerializerMethodField()
    class Meta:
        model = Ward
        fields = "__all__"

    def get_county_name(self, obj):
        return obj.sub_county.county.name if obj.sub_county.county else ""

    def get_sub_county_name(self, obj):
        return obj.sub_county.name if obj.sub_county else ""