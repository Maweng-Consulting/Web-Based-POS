from django.db import models

from core.models import AbstractBaseModel


# Create your models here.
class Supplier(AbstractBaseModel):
    user = models.OneToOneField("users.User", on_delete=models.CASCADE)
    name = models.CharField(max_length=255)
    phone_number = models.CharField(max_length=255)
    email = models.EmailField(null=True)
    supplies = models.JSONField(default=list)
    address = models.CharField(max_length=255, null=True)
    city = models.CharField(max_length=255)
    country = models.CharField(max_length=255)

    def __str__(self):
        return self.name


class SupplyLog(AbstractBaseModel):
    supplier = models.ForeignKey(Supplier, on_delete=models.SET_NULL, null=True)
    item = models.ForeignKey("inventory.Inventory", on_delete=models.SET_NULL, null=True)
    quantity = models.IntegerField(default=0)
    unit_price = models.DecimalField(max_digits=100, decimal_places=2, default=0)
    supply_cost = models.DecimalField(max_digits=100, decimal_places=2, default=0)
    recorded_by = models.ForeignKey("users.User", on_delete=models.SET_NULL, null=True)