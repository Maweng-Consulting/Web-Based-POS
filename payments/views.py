from decimal import Decimal

from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.shortcuts import redirect, render

from payments.models import SupplyInvoice, SupplyInvoiceLog
from suppliers.models import Supplier


# Create your views here.
@login_required(login_url="/users/login/")
def invoices(request):
    invoices = SupplyInvoice.objects.all()
    suppliers = Supplier.objects.all()

    paginator = Paginator(invoices, 12)
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)

    context = {
        "page_obj": page_obj,
        "invoices": invoices,
        "suppliers": suppliers
    }
    return render(request, "payments/invoices.html", context)


@login_required(login_url="/users/login/")
def new_invoice(request):
    user = request.user
    if request.method == "POST":
        supplier_id = request.POST.get("supplier_id")
        amount_expected = request.POST.get("amount_expected")
        date_supplied = request.POST.get("date_supplied")
        date_due = request.POST.get("date_due")

        supplier = Supplier.objects.get(id=supplier_id)
        invoice = SupplyInvoice.objects.create(
            supplier=supplier,
            amount_expected=amount_expected,
            date_supplied=date_supplied,
            date_due=date_due,
            status="Review"
        )

        invoice_log = SupplyInvoiceLog.objects.create(
            invoice=invoice,
            actioned_by=user,
            action="New invoice created"
        )

        return redirect("invoices")

    return render(request, "payments/new_invoice.html")


@login_required(login_url="/users/login/")
def edit_invoice(request):
    user = request.user
    if request.method == "POST":
        invoice_id = request.POST.get("invoice_id")
        supplier_id = request.POST.get("supplier_id")
        amount_expected = request.POST.get("amount_expected")
        date_supplied = request.POST.get("date_supplied")
        date_due = request.POST.get("date_due")
        amount_paid = request.POST.get("amount_paid")
        status = request.POST.get("status")

        supplier = Supplier.objects.get(id=supplier_id)
        invoice = SupplyInvoice.objects.get(id=invoice_id)

        initial_invoice_status = invoice.status

        invoice.supplier = supplier
        invoice.amount_expected = amount_expected
        invoice.amount_paid = amount_paid
        invoice.date_supplied = date_supplied
        invoice.date_due = date_due
        invoice.status = status
        invoice.save()

        new_invoice_status = invoice.status

        invoice_log = SupplyInvoiceLog.objects.create(
            invoice=invoice,
            actioned_by=user,
            action=f"Invoice status changed from {initial_invoice_status} to {new_invoice_status}"
        )

        return redirect("invoices")
    return render(request, "payments/edit_invoice.html")


@login_required(login_url="/users/login/")
def pay_invoice(request):
    user = request.user
    if request.method == "POST":
        invoice_id = request.POST.get("invoice_id")
        amount = request.POST.get("amount")

        invoice = SupplyInvoice.objects.get(id=invoice_id)
        initial_invoice_status = invoice.status
        invoice.amount_paid += Decimal(amount)
        invoice.status = "Paying"
        invoice.save()

        if invoice.amount_paid >= invoice.amount_expected:
            invoice.status = "Paid"
            invoice.save()

        new_invoice_status = invoice.status
        invoice_log = SupplyInvoiceLog.objects.create(
            invoice=invoice,
            actioned_by=user,
            action=f"Invoice status changed from {initial_invoice_status} to {new_invoice_status}"
        )
        return redirect("invoices")

    return render(request, "payments/pay_invoice.html")
