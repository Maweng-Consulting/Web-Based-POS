from django.contrib import admin
from apps.deliveries.models import DeliveryPartner, County, Town, DeliveryDriver, Delivery, DeliveryAddress, DeliveryStatusUpdate, PickupStation

# Register your models here.
@admin.register(DeliveryDriver)
class DeliveryDriverAdmin(admin.ModelAdmin):
    list_display = ["id", "user", "name"]

@admin.register(DeliveryAddress)
class DeliveryAddressAdmin(admin.ModelAdmin):
    list_display = ["id", "customer", "pickup_station", "description"]


@admin.register(Delivery)
class DeliveryAdmin(admin.ModelAdmin):
    list_display = ["id", "customer", "delivery_type", "delivery_status"]


@admin.register(County)
class CountyAdmin(admin.ModelAdmin):
    list_display = ["id", "created", "name"]


@admin.register(Town)
class TownAdmin(admin.ModelAdmin):
    list_display = ["id", "name", "county"]

@admin.register(PickupStation)
class PickupStationAdmin(admin.ModelAdmin):
    list_display = ["id", "name", "town", "county", "country"]