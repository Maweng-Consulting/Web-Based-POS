from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver

from apps.core.models import AbstractBaseModel


# Create your models here.
class ProductSale(AbstractBaseModel):
    order = models.ForeignKey("pos.Order", on_delete=models.CASCADE)
    item = models.ForeignKey("inventory.Inventory", on_delete=models.CASCADE)
    total_quantity = models.FloatField(default=0)
    total_price = models.DecimalField(max_digits=100, decimal_places=2, default=0)
    unit_price = models.DecimalField(max_digits=100, decimal_places=2, default=0)

    def __str__(self):
        return self.item.name


class MontlyProductSale(AbstractBaseModel):
    order = models.ForeignKey("pos.Order", on_delete=models.CASCADE)
    item = models.ForeignKey("inventory.Inventory", on_delete=models.CASCADE)
    total_quantity = models.FloatField(default=0)
    total_price = models.DecimalField(max_digits=100, decimal_places=2, default=0)
    unit_price = models.DecimalField(max_digits=100, decimal_places=2, default=0)

    def __str__(self):
        return self.item.name


class SalesLog(AbstractBaseModel):
    sold_by = models.ForeignKey("users.User", on_delete=models.CASCADE)
    order = models.ForeignKey("pos.Order", on_delete=models.CASCADE)
    item = models.ForeignKey("inventory.Inventory", on_delete=models.CASCADE)
    total_quantity = models.FloatField(default=0)
    total_price = models.DecimalField(max_digits=100, decimal_places=2, default=0)
    unit_price = models.DecimalField(max_digits=100, decimal_places=2, default=0)

    def __str__(self):
        return self.item.name
