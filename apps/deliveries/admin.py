from django.contrib import admin
from apps.deliveries.models import DeliveryPartner, DeliveryDriver, Delivery, DeliveryAddress, DeliveryStatusUpdate

# Register your models here.
@admin.register(DeliveryDriver)
class DeliveryDriverAdmin(admin.ModelAdmin):
    list_display = ["id", "user", "name"]

@admin.register(DeliveryAddress)
class DeliveryAddressAdmin(admin.ModelAdmin):
    list_display = ["id", "customer", "pickup_station", "description"]