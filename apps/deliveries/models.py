from django.db import models
from apps.core.models import AbstractBaseModel

# Create your models here.
DELIVERY_STATUS = (
    ("Delivered", "Delivered"),
    ("Transit", "Transit"),
    ("Pending Dispatch", "Pending Dispatch"),
    ("Initiated", "Initiated"),
    ("Dispatched", "Dispatched"),
    ("Abandoned", "Abandoned"),
)

DELIVERY_STYPE = (
    ("Self Pickup", "Self Pickup"),
    ("Door Delivery", "Door Delivery"),
    ("Pickup Station", "Pickup Station"),
)


class DeliveryPartner(AbstractBaseModel):
    name = models.CharField(max_length=255)
    town = models.CharField(max_length=255)
    country = models.CharField(max_length=255)
    email = models.EmailField(null=True)
    phone_number = models.CharField(max_length=255)

    def __str__(self):
        return self.name

class DeliveryDriver(AbstractBaseModel):
    user = models.OneToOneField("users.User", on_delete=models.CASCADE)
    partner = models.ForeignKey(DeliveryPartner, on_delete=models.SET_NULL, null=True)

    def __str__(self):
        return self.user.username
    

class PickupStation(AbstractBaseModel):
    name = models.CharField(max_length=255)
    town = models.CharField(max_length=255)
    county = models.CharField(max_length=255, null=True)
    country = models.CharField(max_length=255)
    description = models.TextField(null=True)
    phone_number = models.CharField(max_length=255, null=True)

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
    driver = models.ForeignKey(DeliveryDriver, on_delete=models.SET_NULL, null=True)

    def __str__(self):
        return self.customer.username


class DeliveryStatusUpdate(AbstractBaseModel):
    delivery = models.ForeignKey(Delivery, on_delete=models.CASCADE)
    previous_status = models.CharField(max_length=255)
    next_status = models.CharField(max_length=255)

    def __str__(self):
        return f"{self.previous_status} ==> {self.next_status}"