from django.db import models
from apps.core.models import AbstractBaseModel
# Create your models here.
DELIVERY_STATUS = (
    ("Delivered", "Delivered"),
    ("Transit", "Transit"),
    ("Pending Dispatch", "Pending Dispatch"),
)

DELIVERY_STYPE = (
    ("Self Pickup", "Self Pickup"),
    ("Door Delivery", "Door Delivery"),
    ("Pickup Station Delivery", "Pickup Station Delivery")
)

class DeliveryPartner(AbstractBaseModel):
    name = models.CharField(max_length=255)
    town = models.CharField(max_length=255)
    country = models.CharField(max_length=255)
    email = models.EmailField(null=True)
    phone_number = models.CharField(max_length=255)

    def __str__(self):
        return self.name
    
class PickupStation(AbstractBaseModel):
    name = models.CharField(max_length=255)
    town = models.CharField(max_length=255)
    county = models.CharField(max_length=255, null=True)
    country = models.CharField(max_length=255)
    description = models.TextField(null=True)

    def __str__(self):
        return self.name
    
class DeliveryAddress(AbstractBaseModel):
    customer = models.ForeignKey("users.User", on_delete=models.CASCADE)
    pickup_station = models.ForeignKey(PickupStation, on_delete=models.SET_NULL, null=True)
    description = models.TextField(null=True)

    def __str__(self):
        return self.customer.username


class Delivery(AbstractBaseModel):
    customer = models.ForeignKey("users.User", on_delete=models.SET_NULL, null=True)
    order = models.ForeignKey("pos.Order", on_delete=models.SET_NULL, null=True)
    cost = models.DecimalField(max_digits=100, decimal_places=2, default=0)
    delivery_status = models.CharField(max_length=255, choices=DELIVERY_STATUS, default="Pending Dispatch")
    address = models.ForeignKey(DeliveryAddress, on_delete=models.SET_NULL, null=True)
    delivery_partner = models.ForeignKey(DeliveryPartner, on_delete=models.SET_NULL, null=True)
    delivery_type = models.CharField(max_length=255, choices=DELIVERY_STYPE, default="Self Pickup")

    def __str__(self):
        return self.customer.username
