from django.db import models

from core.models import AbstractBaseModel

# Create your models here.
INVOICE_STATUS_CHOICES = (
    ("Paid", "Paid"),
    ("Cancelled", "Cancelled"),
    ("Payment Pending", "Payment Pending"),
    ("Defaulted", "Defaulted"),
)

class SupplyInvoice(AbstractBaseModel):
    supplier = models.ForeignKey("suppliers.Supplier", on_delete=models.CASCADE)
    amount_owed = models.DecimalField(max_digits=100, decimal_places=2)
    date_supplied = models.DateField()
    status = models.CharField(max_length=255, choices=INVOICE_STATUS_CHOICES)

    def __str__(self):
        return f"{self.supplier.name} supplied goods worth {self.amount_owed}"
