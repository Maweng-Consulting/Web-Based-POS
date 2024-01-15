import csv
import io
import json
from datetime import datetime
from decimal import Decimal

from django.contrib.auth.decorators import login_required
from django.core.files import File
from django.core.files.base import ContentFile
from django.core.paginator import Paginator
from django.db import transaction
from django.db.models import Q
from django.http import HttpResponse, JsonResponse
from django.shortcuts import redirect, render
from django.template.loader import render_to_string
from rest_framework import generics, status

from inventory.models import Inventory, MpesaPayment
from pos.generate_receipt import render_to_pdf
from reports.models import MontlyProductSale, ProductSale
from users.models import Customer, User

from .models import CreditOrder, Order, OrderItem, TemporaryCustomerCartItem
from .serializers import InventorySerializer, MpesaPaymentSerializer

date_today = datetime.now().date()


class InventoryAPIView(generics.ListAPIView):
    queryset = Inventory.objects.filter(quantity__gte=1)
    serializer_class = InventorySerializer


class MpesaPaymentAPIView(generics.ListCreateAPIView):
    queryset = MpesaPayment.objects.filter(processed=False)
    serializer_class = MpesaPaymentSerializer


def orders(request):
    orders = Order.objects.all().order_by("-created")

    if request.method == "POST":
        search_text = request.POST.get("search_text")
        sale_type = request.POST.get("sale_type")

        print(f"Search Text: {search_text}, Order Type: {sale_type}")

        if search_text and sale_type:
            orders = Order.objects.filter(
                Q(served_by__first_name__icontains=search_text)
                | Q(served_by__last_name__icontains=search_text)
                | Q(status__icontains=search_text)
                | Q(id__icontains=search_text)
            ).filter(order_type=sale_type)

        elif search_text:
            orders = Order.objects.filter(
                Q(served_by__first_name__icontains=search_text)
                | Q(served_by__last_name__icontains=search_text)
                | Q(status__icontains=search_text)
                | Q(id__icontains=search_text)
            )
        elif sale_type:
            orders = Order.objects.filter(order_type=sale_type)

    paginator = Paginator(orders, 12)
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)

    context = {"orders": orders, "page_obj": page_obj}
    return render(request, "orders/orders.html", context)


def credit_orders(request):
    orders = Order.objects.filter(order_type="Credit")
    paginator = Paginator(orders, 12)
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)

    context = {"orders": orders, "page_obj": page_obj}
    return render(request, "orders/credit_orders.html", context)


@login_required(login_url="/users/login/")
def sales_point(request):
    user = request.user
    cashier_id = request.session.get("cashier_id")
    selected_customer = request.session.get(f"selected_customer_{cashier_id}")

    customer = Customer.objects.get(name="Walk In Customer")
    if not selected_customer:
        request.session[f"selected_customer_{cashier_id}"] = {
            "id": customer.id,
            "name": customer.name,
            "cashier_id": cashier_id if cashier_id else user.id,
            "is_walkin": customer.is_walk_in,
        }

    print(f"Selected Customer: {selected_customer}")

    customers = Customer.objects.all()
    selected_customer = request.session.get(f"selected_customer_{cashier_id}")

    if request.method == "POST":
        new_amount = float(request.POST.get("new_amount"))
        item_id = request.POST.get("item_id")
        print(f"Item ID: {item_id}, New Amount: {new_amount}")

        temp_item = TemporaryCustomerCartItem.objects.get(
            id=item_id,
            user=user,
            cashier_id=cashier_id,
            customer_id=selected_customer["id"],
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
        user=user, cashier_id=cashier_id, customer_id=selected_customer["id"]
    )

    total_cost = sum(list(cart_items.values_list("price", flat=True)))

    paginator = Paginator(items, 5)
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)

    context = {
        "orders": items,
        "page_obj": page_obj,
        "cart_items": cart_items,
        "total_cost": total_cost,
        "customers": customers,
        "selected_customer": selected_customer,
    }
    return render(request, "pos/sale.html", context)


@login_required(login_url="/users/login/")
def add_to_cart(request, item_id=None):
    user = request.user
    cashier_id = request.session.get("cashier_id")
    selected_customer = request.session.get(f"selected_customer_{cashier_id}", {})

    item = Inventory.objects.get(id=item_id)

    item_exists = TemporaryCustomerCartItem.objects.filter(
        item=item, user=user, cashier_id=cashier_id, customer_id=selected_customer["id"]
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
            price=item.selling_price,
            customer_id=selected_customer["id"],
        )
        temp_item.item.quantity -= 1
        temp_item.item.save()
    return redirect("sales-point")


@login_required(login_url="/users/login/")
def remove_from_cart(request, item_id=None):
    user = request.user
    cashier_id = request.session.get("cashier_id")
    selected_customer = request.session.get(f"selected_customer_{cashier_id}", {})

    temp_item = TemporaryCustomerCartItem.objects.get(
        id=item_id, user=user, customer_id=selected_customer["id"]
    )

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

    selected_customer = request.session.get(f"selected_customer_{cashier_id}", {})

    temp_items = TemporaryCustomerCartItem.objects.filter(
        user=user, cashier_id=cashier_id, customer_id=selected_customer["id"]
    )

    total_cost = sum(list(temp_items.values_list("price", flat=True)))

    order = Order.objects.create(
        served_by=user,
        status="Paid",
        payment_method="Cash",
        order_type="Paid",
        total_cost=total_cost,
        customer_id=selected_customer["id"],
    )

    order_items = []

    for temp_item in temp_items:
        order_items.append(
            OrderItem(
                order=order,
                item=temp_item.item,
                quantity=temp_item.quantity,
                price=temp_item.price,
                cashier_id=cashier_id,
            )
        )

    items = OrderItem.objects.bulk_create(order_items)

    for order_item in items:
        product_sale = (
            ProductSale.objects.filter(item=order_item.item)
            .filter(created__date=date_today)
            .first()
        )

        if product_sale:
            product_sale.total_quantity += order_item.quantity
            product_sale.total_price += order_item.price
            product_sale.save()
        else:
            ProductSale.objects.create(
                order=order,
                item=order_item.item,
                total_price=order_item.price,
                total_quantity=order_item.quantity,
                unit_price=order_item.item.selling_price,
            )

    temp_items.delete()
    del request.session[f"selected_customer_{cashier_id}"]
    return redirect("sales-point")


@login_required(login_url="/users/login/")
def increase_order_item_quantity(request, item_id=None, user_id=None):
    user = User.objects.get(id=user_id)
    cashier_id = request.session.get("cashier_id")
    temp_item = TemporaryCustomerCartItem.objects.get(
        id=item_id, user=user, cashier_id=cashier_id
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
        id=item_id, user=user, cashier_id=cashier_id
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
            id=item_id, user=user, cashier_id=cashier_id
        )

        if new_amount <= temp_item.item.quantity:
            temp_item.quantity = new_amount
            temp_item.price = temp_item.item.price * Decimal(new_amount)
            temp_item.save()
        else:
            return redirect("sales-point")

    return redirect("sales-point")


def print_order_receipt(request, order_id=None):
    order = Order.objects.get(id=order_id)
    order_items = order.items
    context = {"order": order, "order_items": order_items}
    return render(request, "receipts/order.html", context)


@login_required(login_url="/users/login/")
@transaction.atomic
def new_credit_order(request):
    user = request.user
    cashier_id = request.session.get("cashier_id")

    selected_customer = request.session.get(f"selected_customer_{cashier_id}", {})

    temp_items = TemporaryCustomerCartItem.objects.filter(
        user=user, cashier_id=cashier_id, customer_id=selected_customer["id"]
    )

    total_cost = sum(list(temp_items.values_list("price", flat=True)))

    order = Order.objects.create(
        served_by=user,
        status="Processed",
        payment_method="Credit",
        order_type="Credit",
        total_cost=total_cost,
        customer_id=selected_customer["id"],
    )

    order_items = []

    for temp_item in temp_items:
        order_items.append(
            OrderItem(
                order=order,
                item=temp_item.item,
                quantity=temp_item.quantity,
                price=temp_item.price,
                cashier_id=cashier_id,
            )
        )

    items = OrderItem.objects.bulk_create(order_items)

    for order_item in items:
        product_sale = (
            ProductSale.objects.filter(item=order_item.item)
            .filter(created__date=date_today)
            .first()
        )

        if product_sale:
            product_sale.total_quantity += order_item.quantity
            product_sale.total_price += order_item.price
            product_sale.save()
        else:
            ProductSale.objects.create(
                order=order,
                item=order_item.item,
                total_price=order_item.price,
                total_quantity=order_item.quantity,
                unit_price=order_item.item.selling_price,
            )

    temp_items.delete()
    del request.session[f"selected_customer_{cashier_id}"]
    return redirect("sales-point")


@login_required(login_url="/users/login/")
def credit_sales_point(request):
    user = request.user
    cashier_id = request.session.get("cashier_id")
    customers = Customer.objects.all()

    if request.method == "POST":
        new_amount = float(request.POST.get("new_amount"))
        item_id = request.POST.get("item_id")
        print(f"Item ID: {item_id}, New Amount: {new_amount}")

        temp_item = TemporaryCustomerCartItem.objects.get(
            id=item_id, user=user, cashier_id=cashier_id
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
        user=user, cashier_id=cashier_id
    )

    total_cost = sum(list(cart_items.values_list("price", flat=True)))

    paginator = Paginator(items, 5)
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)

    context = {
        "orders": items,
        "page_obj": page_obj,
        "cart_items": cart_items,
        "total_cost": total_cost,
        "customers": customers,
    }
    return render(request, "pos/credit_sale.html", context)
