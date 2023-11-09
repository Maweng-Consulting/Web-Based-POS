from django.conf import settings
from django.db import models

from core.models import AbstractBaseModel

# Create your models here.
ORDER_STATUS_CHOICES = (
    ("Cancelled", "Cancelled"),
    ("Processed", "Processed"),
    ("Pending", "Pending"),
)


PAYMENT_METHODS = (
    ("Mpesa", "Mpesa"),
    ("Cash", "Cash"),
    ("Wallet", "Wallet"),
)

class Order(AbstractBaseModel):
    total_cost = models.DecimalField(max_digits=20, decimal_places=2)
    status = models.CharField(max_length=255, choices=ORDER_STATUS_CHOICES)
    served_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True)
    payment_method = models.CharField(max_length=255, null=True, choices=PAYMENT_METHODS)

    def __str__(self):
        return str(self.id)


class OrderItem(AbstractBaseModel):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name="orderitems")
    item = models.ForeignKey("inventory.Inventory", on_delete=models.SET_NULL, null=True)
    quantity = models.FloatField(default=0)
    price = models.DecimalField(max_digits=10, decimal_places=2)



class TemporaryCustomerCartItem(AbstractBaseModel):
    item = models.OneToOneField("inventory.Inventory", on_delete=models.CASCADE)
    quantity = models.FloatField(default=0)
    price = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return self.item.name    