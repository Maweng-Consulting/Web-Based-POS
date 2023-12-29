from django.db import models

from core.models import AbstractBaseModel

UNIT_OF_MEASURE_CHOICES = (
    ("Kilogram", "Kilograms"),
    ("Litres", "Litres"),
    ("Units", "Units"),
    ("Cartons", "Cartons"),
    ("Pieces", "Pieces"),
    ("Metres", "Metres"),
)

CATEGORY_OPTIONS = (
    ("Beverages", "Beverages"),
    ("Drinks", "Drinks"),
    ("Food", "Food"),
)

STOCK_ACTION_OPTIONS = (
    ("Buy", "Buy"),
    ("Sale", "Sale"),
    ("Damaged", "Damaged"),
    ("Stolen", "Stolen"),
    ("Family", "Family use"),
    ("Fashion", "Out of fashion"),
    ("New Stock", "New Stock"),
    ("Stock Edit", "Stock Edited"),
    ("Stock Delete", "Stock Delete"),
)

# Create your models here.
class Inventory(AbstractBaseModel):
    name = models.CharField(max_length=255)
    buying_price = models.DecimalField(max_digits=100, decimal_places=2)
    selling_price = models.DecimalField(max_digits=100, decimal_places=2)
    quantity = models.FloatField(default=0)
    unit_of_measure = models.CharField(max_length=255)
    brand = models.CharField(max_length=255, null=True)


    def __str__(self):
        return self.name



class InventoryLog(AbstractBaseModel):
    actioned_by = models.ForeignKey("users.User", on_delete=models.SET_NULL, null=True)
    item = models.ForeignKey(Inventory, on_delete=models.SET_NULL, null=True)
    action = models.CharField(max_length=255, choices=STOCK_ACTION_OPTIONS)
    quantity = models.FloatField(default=0)
    reason = models.CharField(max_length=255, null=True)

    def __str__(self):
        return self.item.name


class MpesaPayment(AbstractBaseModel):
    phone_number = models.CharField(max_length=255)
    amount = models.DecimalField(max_digits=100, decimal_places=2)
    processed = models.BooleanField(default=False)

    def __str__(self):
        return self.phone_number