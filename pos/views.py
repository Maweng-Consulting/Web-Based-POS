import json

from django.core.paginator import Paginator
from django.http import JsonResponse
from django.shortcuts import redirect, render
from rest_framework import generics, status

from inventory.models import Inventory, MpesaPayment

from .models import Order, OrderItem, TemporaryCustomerCartItem
from .serializers import InventorySerializer, MpesaPaymentSerializer
from .tables import InventoryTable


class InventoryAPIView(generics.ListAPIView):
    queryset = Inventory.objects.all()
    serializer_class = InventorySerializer

class MpesaPaymentAPIView(generics.ListCreateAPIView):
    queryset = MpesaPayment.objects.filter(processed=False)
    serializer_class = MpesaPaymentSerializer


def get_inventory_data(request):
    items = InventoryTable()
    return render(request, "hello.html", {"items": items})
    



def sales_point(request):
    items = Inventory.objects.all()

    cart_items = TemporaryCustomerCartItem.objects.all()

    total_cost = sum(list(cart_items.values_list("price", flat=True)))

    paginator = Paginator(items, 5)
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)


    context = {
        "orders": items,
        "page_obj": page_obj,
        "cart_items": cart_items,
        "total_cost": total_cost
    }
    return render(request, "pos/sale.html", context)




def add_to_cart(request, item_id=None):
    item = Inventory.objects.get(id=item_id)

    item_exists = TemporaryCustomerCartItem.objects.filter(
        item=item
    ).first()

    if item_exists:
        item_exists.quantity += 1
        item_exists.price += item.selling_price
        item_exists.save()
    else:
        TemporaryCustomerCartItem.objects.create(
            item=item,
            quantity=1,
            price=item.selling_price
        )
    return redirect("sales-point")


def remove_from_cart(request, item_id=None):
    item = TemporaryCustomerCartItem.objects.get(id=item_id)
    item.delete()
    return redirect("sales-point")


def redeem_mpesa_payment(request, payment_id=None):
    mpesa_payment = MpesaPayment.objects.get(id=payment_id)
    mpesa_payment.processed = True
    mpesa_payment.save()
    return redirect("sales-point")