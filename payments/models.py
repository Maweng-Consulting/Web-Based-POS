from django.db import models

from core.models import AbstractBaseModel

# Create your models here.
INVOICE_STATUS_CHOICES = (
    ("Paid", "Paid"),
    ("Cancelled", "Cancelled"),
    ("Payment Pending", "Payment Pending"),
    ("Defaulted", "Defaulted"),
    ("Paying", "Paying"),
    ("Review", "Review"),
)


class SupplyInvoice(AbstractBaseModel):
    supplier = models.ForeignKey(
        "suppliers.Supplier", related_name="supplierinvoices", on_delete=models.CASCADE
    )
    amount_expected = models.DecimalField(max_digits=100, decimal_places=2, default=0)
    amount_paid = models.DecimalField(max_digits=100, decimal_places=2, default=0)
    date_supplied = models.DateField()
    status = models.CharField(max_length=255, choices=INVOICE_STATUS_CHOICES)
    date_due = models.DateField(null=True)

    def __str__(self):
        return f"{self.supplier.name} supplied goods worth {self.amount_expected}"

    def invoice_balance(self):
        return self.amount_expected - self.amount_paid


class SupplyInvoiceLog(AbstractBaseModel):
    invoice = models.ForeignKey(SupplyInvoice, on_delete=models.SET_NULL, null=True)
    actioned_by = models.ForeignKey("users.User", on_delete=models.SET_NULL, null=True)
    action = models.CharField(max_length=255)
