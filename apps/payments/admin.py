from django.contrib import admin

from apps.payments.models import SupplyInvoice, SupplyInvoiceLog


# Register your models here.
@admin.register(SupplyInvoice)
class SupplyInvoiceAdmin(admin.ModelAdmin):
    list_display = [
        "supplier",
        "date_supplied",
        "date_due",
        "amount_expected",
        "amount_paid",
        "status",
    ]


@admin.register(SupplyInvoiceLog)
class SupplyInvoiceLogAdmin(admin.ModelAdmin):
    list_display = ["created", "invoice", "action", "actioned_by"]
