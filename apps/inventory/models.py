from django.db import models

from apps.core.models import AbstractBaseModel

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
class ProductCategory(AbstractBaseModel):
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name

class Inventory(AbstractBaseModel):
    category = models.ForeignKey(ProductCategory, on_delete=models.SET_NULL, null=True)
    name = models.CharField(max_length=255)
    buying_price = models.DecimalField(max_digits=100, decimal_places=2)
    selling_price = models.DecimalField(max_digits=100, decimal_places=2)
    quantity = models.FloatField(default=0)
    unit_of_measure = models.CharField(max_length=255)
    brand = models.CharField(max_length=255, null=True)
    image = models.ImageField(upload_to="product_images/", null=True)

    def __str__(self):
        return self.name


class ProductImage(AbstractBaseModel):
    product = models.ForeignKey(Inventory, on_delete=models.CASCADE, related_name="productimages")
    image = models.ImageField(upload_to="product_images")

    def __str__(self):
        return self.product.name


class InventoryLog(AbstractBaseModel):
    actioned_by = models.ForeignKey("users.User", on_delete=models.SET_NULL, null=True)
    item = models.ForeignKey(Inventory, on_delete=models.SET_NULL, null=True)
    action = models.CharField(max_length=255, choices=STOCK_ACTION_OPTIONS)
    quantity = models.FloatField(default=0)
    reason = models.CharField(max_length=255, null=True)


class MpesaPayment(AbstractBaseModel):
    phone_number = models.CharField(max_length=255)
    amount = models.DecimalField(max_digits=100, decimal_places=2)
    processed = models.BooleanField(default=False)

    def __str__(self):
        return self.phone_number


PURCHASE_TYPES = (
    ("Paid", "Paid"),
    ("Credit", "Credit"),
)


class Purchase(AbstractBaseModel):
    recorded_by = models.ForeignKey("users.User", on_delete=models.SET_NULL, null=True)
    supplier = models.ForeignKey(
        "suppliers.Supplier", on_delete=models.SET_NULL, null=True
    )
    cost = models.DecimalField(max_digits=100, decimal_places=2, default=0)
    amount_paid = models.DecimalField(max_digits=100, decimal_places=2, default=0)
    purchase_type = models.CharField(max_length=255, choices=PURCHASE_TYPES, null=True)

    def __str__(self):
        return self.recorded_by.username
