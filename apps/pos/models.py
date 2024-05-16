from django.conf import settings
from django.db import models

from apps.core.models import AbstractBaseModel

# Create your models here.
ORDER_STATUS_CHOICES = (
    ("Cancelled", "Cancelled"),
    ("Processed", "Processed"),
    ("Pending", "Pending"),
    ("Paid", "Paid"),
)


PAYMENT_METHODS = (
    ("Mpesa", "Mpesa"),
    ("Cash", "Cash"),
    ("Wallet", "Wallet"),
    ("Credit", "Credit"),
)

ORDER_TYPES = (
    ("Paid", "Paid"),
    ("Credit", "Credit"),
)

ORDER_SOURCE = (
    ("Store", "Store"),
    ("Online", "Online"),
)


class Order(AbstractBaseModel):
    customer = models.ForeignKey("users.Customer", on_delete=models.SET_NULL, null=True)
    total_cost = models.DecimalField(max_digits=20, decimal_places=2)
    status = models.CharField(max_length=255, choices=ORDER_STATUS_CHOICES)
    served_by = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True
    )
    payment_method = models.CharField(
        max_length=255, null=True, choices=PAYMENT_METHODS
    )
    order_receipt = models.FileField(upload_to="receipts/", null=True)
    order_type = models.CharField(max_length=255, choices=ORDER_TYPES, null=True)
    order_source = models.CharField(max_length=255, choices=ORDER_SOURCE, default="Store")

    def __str__(self):
        return str(self.id)

    def items(self):
        return self.orderitems.all()

    def order_date(self):
        return self.created.date()

    def order_time(self):
        return self.created.time()


class OrderItem(AbstractBaseModel):
    user = models.ForeignKey("users.User", on_delete=models.SET_NULL, null=True)
    cashier_id = models.IntegerField(null=True)
    order = models.ForeignKey(
        Order, on_delete=models.CASCADE, related_name="orderitems"
    )
    item = models.ForeignKey(
        "inventory.Inventory", on_delete=models.SET_NULL, null=True
    )
    quantity = models.FloatField(default=0)
    price = models.DecimalField(max_digits=10, decimal_places=2)


class TemporaryCustomerCartItem(AbstractBaseModel):
    user = models.ForeignKey("users.User", on_delete=models.SET_NULL, null=True)
    customer = models.ForeignKey("users.Customer", on_delete=models.SET_NULL, null=True)
    cashier_id = models.IntegerField(null=True)
    item = models.ForeignKey("inventory.Inventory", on_delete=models.CASCADE)
    quantity = models.FloatField(default=0)
    price = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return self.item.name


class CreditOrder(AbstractBaseModel):
    customer = models.ForeignKey("users.Customer", on_delete=models.CASCADE)
    order = models.OneToOneField(Order, on_delete=models.SET_NULL, null=True)
    due_date = models.DateField()

    def __str__(self):
        return f"{self.customer.name} has borrowed goods worth {self.order.total_cost}"
