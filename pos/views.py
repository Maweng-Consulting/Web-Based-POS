import json
from decimal import Decimal

from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.db import transaction
from django.http import JsonResponse
from django.shortcuts import redirect, render
from rest_framework import generics, status

from inventory.models import Inventory, MpesaPayment
from users.models import User

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


def orders(request):
    orders = Order.objects.all()
    
    paginator = Paginator(orders, 12)
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)

    context = {
        "orders": orders,
        "page_obj": page_obj
    }
    return render(request, "orders/orders.html", context)


@login_required(login_url="/users/login/")
def sales_point(request):
    user = request.user
    cashier_id = request.session.get("cashier_id")

    if request.method == "POST":
        new_amount = float(request.POST.get("new_amount"))
        item_id = request.POST.get("item_id")
        print(f"Item ID: {item_id}, New Amount: {new_amount}")

        temp_item = TemporaryCustomerCartItem.objects.get(
            id=item_id,
            user=user,
            cashier_id=cashier_id
        )

        if new_amount <= float(temp_item.item.quantity):
            temp_item.quantity = new_amount
            temp_item.price = temp_item.item.selling_price * Decimal(new_amount)
            temp_item.save()

            temp_item.item.quantity -= new_amount
            temp_item.item.save()

        else:
            return redirect("sales-point")

    print(f"User ID: {user.id}, Cashier ID: {cashier_id}")
    items = Inventory.objects.all()

    cart_items = TemporaryCustomerCartItem.objects.filter(
        user=user, cashier_id=cashier_id)

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


@login_required(login_url="/users/login/")
def add_to_cart(request, item_id=None):
    user = request.user
    cashier_id = request.session.get("cashier_id")
    item = Inventory.objects.get(id=item_id)

    item_exists = TemporaryCustomerCartItem.objects.filter(
        item=item, user=user, cashier_id=cashier_id
    ).first()

    if item_exists:
        item_exists.quantity += 1
        item_exists.price += item.selling_price
        item_exists.save()

        item_exists.item.quantity -= 1
        item_exists.item.save()
    else:
        temp_item = TemporaryCustomerCartItem.objects.create(
            user=user,
            cashier_id=cashier_id,
            item=item,
            quantity=1,
            price=item.selling_price
        )
        temp_item.item.quantity -= 1
        temp_item.item.save()
    return redirect("sales-point")


@login_required(login_url="/users/login/")
def remove_from_cart(request, item_id=None):
    temp_item = TemporaryCustomerCartItem.objects.get(id=item_id)

    temp_item.item.quantity += temp_item.quantity
    temp_item.item.save()
    temp_item.delete()
    return redirect("sales-point")


@login_required(login_url="/users/login/")
def redeem_mpesa_payment(request, payment_id=None):
    mpesa_payment = MpesaPayment.objects.get(id=payment_id)
    mpesa_payment.processed = True
    mpesa_payment.save()
    return redirect("sales-point")


@login_required(login_url="/users/login/")
@transaction.atomic
def mark_order_as_paid(request, user_id=None):
    user = User.objects.get(id=user_id)
    cashier_id = request.session.get("cashier_id")

    temp_items = TemporaryCustomerCartItem.objects.filter(
        user=user, cashier_id=cashier_id
    )

    total_cost = sum(list(temp_items.values_list("price", flat=True)))

    order = Order.objects.create(
        served_by=user,
        status="Paid",
        payment_method="Cash",
        total_cost=total_cost
    )

    order_items = []
    for temp_item in temp_items:
        order_items.append(OrderItem(order=order, item=temp_item.item,
                           quantity=temp_item.quantity, price=temp_item.price))

    OrderItem.objects.bulk_create(order_items)

    temp_items.delete()
    return redirect("sales-point")



@login_required(login_url="/users/login/")
def increase_order_item_quantity(request, item_id=None, user_id=None):
    user = User.objects.get(id=user_id)
    cashier_id = request.session.get("cashier_id")
    temp_item = TemporaryCustomerCartItem.objects.get(
        id=item_id,
        user=user,
        cashier_id=cashier_id
    )
    temp_item.quantity += 1
    temp_item.price += temp_item.item.price
    temp_item.save()
    
    return redirect("sales-point")


@login_required(login_url="/users/login/")
def decrease_order_item_quantity(request, item_id=None, user_id=None):
    user = User.objects.get(id=user_id)
    cashier_id = request.session.get("cashier_id")
    temp_item = TemporaryCustomerCartItem.objects.get(
        id=item_id,
        user=user,
        cashier_id=cashier_id
    )
    if temp_item.quantity == 0:
        temp_item.quantity = 0
        temp_item.save()
    else:
        temp_item.quantity -= 1
        temp_item.price -= temp_item.item.price
        temp_item.save()
    return redirect("sales-point")

def update_cart_items(request, item_id=None, user_id=None):
    user = User.objects.get(id=user_id)
    cashier_id = request.session.get("cashier_id")

    if request.method == "POST":
        new_amount = int(request.POST.get("new_amount"))

        temp_item = TemporaryCustomerCartItem.objects.get(
            id=item_id,
            user=user,
            cashier_id=cashier_id
        )

        if new_amount <= temp_item.item.quantity:
            temp_item.quantity = new_amount
            temp_item.price = temp_item.item.price * Decimal(new_amount)
            temp_item.save()
        else:
            return redirect("sales-point")
        
    return redirect("sales-point")