from decimal import Decimal

from django.core.files.base import ContentFile
from django.core.files.storage import FileSystemStorage
import csv

from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.db.models import Q
from django.shortcuts import redirect, render

from apps.inventory.models import Inventory, InventoryLog, Purchase
from apps.suppliers.models import Supplier, SupplyLog
from apps.payments.models import SupplyInvoice
from apps.inventory.upload_items import UploadNewStockMixin

fs = FileSystemStorage(location="temp")

# Create your views here.
@login_required(login_url="/users/login/")
def stock_logs(request):
    stock_logs = InventoryLog.objects.all().order_by("-created")

    if request.method == "POST":
        search_text = request.POST.get("search_text")
        stock_logs = InventoryLog.objects.filter(
            Q(item__name__icontains=search_text)
            | Q(actioned_by__first_name__icontains=search_text)
            | Q(actioned_by__last_name__icontains=search_text)
        )

    paginator = Paginator(stock_logs, 15)
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)

    context = {"page_obj": page_obj, "stock_logs": stock_logs}

    return render(request, "inventory/stock_logs.html", context)


@login_required(login_url="/users/login/")
def inventory(request):
    stock_items = Inventory.objects.all().order_by("-created")
    suppliers = Supplier.objects.all()

    if request.method == "POST":
        name = request.POST.get("name")
        stock_items = Inventory.objects.filter(Q(name__icontains=name))

    paginator = Paginator(stock_items, 12)
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)

    context = {"stock_items": stock_items, "page_obj": page_obj, "suppliers": suppliers}
    return render(request, "inventory/inventory.html", context)


@login_required(login_url="/users/login/")
def record_stock(request):
    user = request.user
    if request.method == "POST":
        name = request.POST.get("name")
        quantity = request.POST.get("quantity")
        buying_price = request.POST.get("buying_price")
        selling_price = request.POST.get("selling_price")
        unit_of_measure = request.POST.get("unit")

        inv = Inventory.objects.create(
            name=name,
            quantity=quantity,
            buying_price=buying_price,
            selling_price=selling_price,
            unit_of_measure=unit_of_measure,
        )

        stock_log = InventoryLog.objects.create(
            actioned_by=user, item=inv, action="New Stock", quantity=quantity
        )

        return redirect("inventory")

    return render(request, "inventory/new_stock_item.html")


@login_required(login_url="/users/login/")
def edit_stock_item(request):
    user = request.user
    if request.method == "POST":
        stock_id = request.POST.get("item_id")
        name = request.POST.get("name")
        quantity = request.POST.get("quantity")
        buying_price = request.POST.get("buying_price")
        selling_price = request.POST.get("selling_price")
        unit_of_measure = request.POST.get("unit")

        stock_item = Inventory.objects.get(id=stock_id)
        stock_item.name = name
        stock_item.quantity = quantity
        stock_item.buying_price = buying_price
        stock_item.selling_price = selling_price
        stock_item.unit_of_measure = unit_of_measure
        stock_item.save()

        stock_log = InventoryLog.objects.create(
            actioned_by=user, item=stock_item, action="Stock Edit", quantity=quantity
        )

        return redirect("inventory")

    return render(request, "inventory/edit_stock_item.html")


@login_required(login_url="/users/login/")
def delete_stock_item(request):
    user = request.user
    if request.method == "POST":
        stock_id = request.POST.get("item_id")
        stock_item = Inventory.objects.get(id=stock_id)

        stock_log = InventoryLog.objects.create(
            actioned_by=user,
            item=stock_item,
            action="Stock Delete",
            quantity=stock_item.quantity,
        )

        stock_item.delete()
        return redirect("inventory")

    return redirect(request, "inventory/delete_stock_item.html")


@login_required(login_url="/users/login/")
def restock_item(request):
    user = request.user
    if request.method == "POST":
        stock_id = request.POST.get("item_id")
        quantity = float(request.POST.get("quantity"))
        supplier_id = request.POST.get("supplier_id")
        stock_item = Inventory.objects.get(id=stock_id)

        stock_item.quantity += quantity
        stock_item.save()

        supplier = Supplier.objects.get(id=supplier_id)

        stock_log = InventoryLog.objects.create(
            actioned_by=user, item=stock_item, action="New Stock", quantity=quantity
        )

        supply_cost = Decimal(quantity) * stock_item.buying_price

        supply_log = SupplyLog.objects.create(
            supplier=supplier,
            recorded_by=user,
            item=stock_item,
            quantity=quantity,
            unit_price=stock_item.buying_price,
            supply_cost=supply_cost,
        )

        return redirect("inventory")

    return render(request, "inventory/restock.html")


@login_required(login_url="/users/login/")
def take_out_stock(request):
    user = request.user
    if request.method == "POST":
        stock_id = request.POST.get("item_id")
        quantity = float(request.POST.get("quantity"))
        reason = request.POST.get("reason")
        stock_item = Inventory.objects.get(id=stock_id)

        stock_item.quantity -= quantity
        stock_item.save()

        stock_log = InventoryLog.objects.create(
            actioned_by=user,
            item=stock_item,
            action=reason,
            quantity=quantity,
            reason=reason,
        )
        return redirect("inventory")

    return render(request, "inventory/restock.html")


def purchases(request):
    purchases = Purchase.objects.all().order_by("-created")

    paginator = Paginator(purchases, 15)
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)

    suppliers = Supplier.objects.all()

    context = {"page_obj": page_obj, "purchases": purchases, "suppliers": suppliers}

    return render(request, "purchases/purchases.html", context)


def new_purchase(request):
    if request.method == "POST":
        recorded_by = request.POST.get("recorded_by")
        supplier_id = request.POST.get("supplier_id")
        cost = Decimal(request.POST.get("cost"))
        amount_paid = Decimal(request.POST.get("amount_paid"))
        purchase_type = request.POST.get("purchase_type")
        pay_by = request.POST.get("pay_by_when")
        date_supplied = request.POST.get("date_supplied")

        purchase = Purchase.objects.create(
            recorded_by_id=recorded_by,
            supplier_id=supplier_id,
            cost=cost,
            amount_paid=amount_paid,
            purchase_type=purchase_type,
        )

        if purchase_type == "Credit":
            invoice = SupplyInvoice()
            invoice.supplier = purchase.supplier
            invoice.amount_expected = purchase.cost
            invoice.amount_paid = purchase.amount_paid
            invoice.status = "Payment Pending"
            invoice.date_due = pay_by
            invoice.date_supplied = date_supplied
            invoice.save()

        return redirect("purchases")

    return render(request, "purchases/new_purchase.html")


def pay_purchase(request):
    pass


def upload_stock_items(request):
    if request.method == "POST":
        stock_file = request.FILES["stock_file"]

        source_file_content = stock_file.read()
        source_file_content = ContentFile(source_file_content)
        source_file_name = fs.save(
            "temp_source_file.csv", source_file_content
        )
        temp_source_file = fs.path(source_file_name)
        with open(temp_source_file) as f:
            data = list(csv.DictReader(f))
            try:
                upload_mixin = UploadNewStockMixin(data=data)
                upload_mixin.run()
            except Exception as e:
                raise e
        return redirect("inventory")
    return render(request, "inventory/upload_stock_items.html")