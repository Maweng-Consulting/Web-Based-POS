from django.db.models import Q
from django.shortcuts import redirect, render
from inventory.models import Inventory, InventoryLog

from django.core.paginator import Paginator
# Create your views here.
def inventory(request):
    stock_items = Inventory.objects.all()
   
    if request.method == "POST":
        name = request.POST.get("name")
        stock_items = Inventory.objects.filter(Q(name__icontains=name))

    paginator = Paginator(stock_items, 10)
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)

    context = {
        "stock_items": stock_items,
        "page_obj": page_obj
    }
    return render(request, "inventory/inventory.html", context)


def record_stock(request):
    if request.method == "POST":
        name = request.POST.get("name")
        quantity = request.POST.get("quantity")
        buying_price = request.POST.get("buying_price")
        selling_price = request.POST.get("selling_price")
        unit_of_measure = request.POST.get("unit")

        inv = Inventory.objects.create(
            name = name,
            quantity=quantity,
            buying_price=buying_price,
            selling_price=selling_price,
            unit_of_measure=unit_of_measure
        )

        return redirect("inventory")

    return render(request, "inventory/new_stock_item.html")


def edit_stock_item(request):
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
        return redirect("inventory")

    return render(request, "inventory/edit_stock_item.html")


def delete_stock_item(request):
    if request.method == "POST":
        stock_id = request.POST.get("item_id")
        stock_item = Inventory.objects.get(id=stock_id)
        stock_item.delete()
        return redirect("inventory")

    return redirect(request, "inventory/delete_stock_item.html")



def restock_item(request):
    if request.method == "POST":
        stock_id = request.POST.get("item_id")
        quantity = float(request.POST.get("quantity"))
        stock_item = Inventory.objects.get(id=stock_id)

        stock_item.quantity += quantity
        stock_item.save()

        stock_log = InventoryLog.objects.create(
            item=stock_item,
            action="New Stock",
            quantity=quantity
        )

        return redirect("inventory")

    return render(request, "inventory/restock.html")


def take_out_stock(request):
    if request.method == "POST":
        stock_id = request.POST.get("item_id")
        quantity = float(request.POST.get("quantity"))
        reason = request.POST.get("reason")
        stock_item = Inventory.objects.get(id=stock_id)

        stock_item.quantity -= quantity
        stock_item.save()

        stock_log = InventoryLog.objects.create(
            item=stock_item,
            action=reason,
            quantity=quantity
        )
        return redirect("inventory")

    return render(request, "inventory/restock.html")