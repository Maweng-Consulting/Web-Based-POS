from typing import Iterable
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

PICKUP_STATION_TYPES = (
    ("General", "General"),
    ("Shop", "Shop"),
)

class County(AbstractBaseModel):
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name


class SubCounty(AbstractBaseModel):
    name = models.CharField(max_length=255)
    county = models.ForeignKey(County, on_delete=models.CASCADE)

    def __str__(self):
        return self.name


class Ward(AbstractBaseModel):
    name = models.CharField(max_length=255)
    sub_county = models.ForeignKey(SubCounty, on_delete=models.CASCADE)

    def __str__(self):
        return self.name


class Town(AbstractBaseModel):
    name = models.CharField(max_length=255)
    county = models.ForeignKey(County, on_delete=models.CASCADE)
    sub_county = models.ForeignKey(SubCounty, on_delete=models.SET_NULL, null=True)
    ward = models.ForeignKey(Ward, on_delete=models.SET_NULL, null=True)

    def __str__(self):
        return self.name
    
class Branch(AbstractBaseModel):
    name = models.CharField(max_length=255)
    county = models.ForeignKey(County, on_delete=models.CASCADE)
    sub_county = models.ForeignKey(SubCounty, on_delete=models.SET_NULL, null=True)
    ward = models.ForeignKey(Ward, on_delete=models.SET_NULL, null=True)
    town = models.CharField(max_length=255)

    def __str__(self):
        return self.name


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

    @property
    def name(self):
        return f"{self.user.first_name} {self.user.last_name}"


class PickupStation(AbstractBaseModel):
    name = models.CharField(max_length=255)
    town = models.CharField(max_length=255, null=True)
    county = models.ForeignKey(County, on_delete=models.SET_NULL, null=True)
    sub_county = models.ForeignKey(SubCounty, on_delete=models.SET_NULL, null=True)
    ward = models.ForeignKey(Ward, on_delete=models.SET_NULL, null=True)
    country = models.CharField(max_length=255)
    description = models.TextField(null=True)
    phone_number = models.CharField(max_length=255, null=True)
    station_type = models.CharField(max_length=255, choices=PICKUP_STATION_TYPES, default="General")

    def __str__(self):
        return self.name


class DeliveryAddress(AbstractBaseModel):
    name = models.CharField(max_length=255, null=True)
    phone_number = models.CharField(max_length=255, null=True)
    id_number = models.CharField(max_length=255, null=True)
    customer = models.ForeignKey("users.Customer", on_delete=models.CASCADE, null=True)
    pickup_station = models.ForeignKey(PickupStation, on_delete=models.SET_NULL, null=True, blank=True)
    description = models.TextField(null=True, blank=True)
    town = models.CharField(max_length=255, null=True)
    county = models.ForeignKey(County, on_delete=models.SET_NULL, null=True)
    sub_county = models.ForeignKey(SubCounty, on_delete=models.SET_NULL, null=True)
    ward = models.ForeignKey(Ward, on_delete=models.SET_NULL, null=True)
    address_type = models.CharField(max_length=255, choices=DELIVERY_STYPE, default="Pickup Station")

    def __str__(self):
        return self.customer.user.username


class Delivery(AbstractBaseModel):
    customer = models.ForeignKey("users.Customer", on_delete=models.SET_NULL, null=True)
    order = models.ForeignKey("pos.Order", on_delete=models.SET_NULL, null=True)
    cost = models.DecimalField(max_digits=100, decimal_places=2, default=0)
    delivery_status = models.CharField(
        max_length=255, choices=DELIVERY_STATUS, default="Pending Dispatch"
    )
    address = models.ForeignKey(DeliveryAddress, on_delete=models.SET_NULL, null=True)
    delivery_partner = models.ForeignKey(
        DeliveryPartner, on_delete=models.SET_NULL, null=True
    )
    delivery_type = models.CharField(
        max_length=255, choices=DELIVERY_STYPE, default="Self Pickup"
    )
    driver = models.ForeignKey(DeliveryDriver, on_delete=models.SET_NULL, null=True)

    def __str__(self):
        return self.customer.user.username

    def delivery_address(self):
        if self.delivery_type == "Door Delivery":
            return self.address.description if self.address else ""
        elif self.delivery_type == "Pickup Station":
            return (
                f"""
                    {self.address.pickup_station.name}, {self.address.pickup_station.town}\n,
                    {self.address.pickup_station.description}
                """
                if self.address
                else ""
            )
        else:
            return "Pickup your order from our shop located at Juja City Mall, 2nd Floor, No.: 300"


class DeliveryStatusUpdate(AbstractBaseModel):
    delivery = models.ForeignKey(Delivery, on_delete=models.CASCADE)
    previous_status = models.CharField(max_length=255)
    next_status = models.CharField(max_length=255)

    def __str__(self):
        return f"{self.previous_status} ==> {self.next_status}"
