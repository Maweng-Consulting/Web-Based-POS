from django.urls import path

from apps.payments.views import (edit_invoice, invoices, new_invoice,
                                 pay_invoice)

urlpatterns = [
    path("invoices/", invoices, name="invoices"),
    path("new-invoice/", new_invoice, name="new-invoice"),
    path("pay-invoice/", pay_invoice, name="pay-invoice"),
    path("edit-invoice/", edit_invoice, name="edit-invoice"),
]
