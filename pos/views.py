import json

from django.core.paginator import Paginator
from django.http import JsonResponse
from django.shortcuts import redirect, render
from rest_framework import generics, status

from inventory.models import Inventory, MpesaPayment

from .models import Order, OrderItem, TemporaryCustomerCartItem
from .serializers import InventorySerializer, MpesaPaymentSerializer
from .tables import InventoryTable

# Create your views here.
data = [['Maize flour', 100, 120, 100, 'kg'], ['Rice', 200, 240, 50, 'kg'], ['Sugar', 300, 360, 25, 'kg'], ['Milk', 400, 480, 10, 'ltr'], ['Soap', 500, 600, 20, 'bar'], ['Cooking oil', 600, 720, 15, 'ltr'], ['Tea leaves', 700, 840, 10, 'pkt'], ['Salt', 800, 960, 5, 'kg'], ['Biscuits', 900, 1080, 15, 'pkt'], ['Chocolate', 1000, 1200, 10, 'bar'], ['Bread', 50, 60, 50, 'loaf'], ['Eggs', 10, 12, 100, 'dozen'], ['Potatoes', 20, 24, 25, 'kg'], ['Onions', 30, 36, 15, 'kg'], ['Tomatoes', 40, 48, 10, 'kg'], ['Cabbages', 50, 60, 5, 'head']]

items_list = [
    {
        "id": 1,
        "created": "2023-11-09T13:53:38.017038Z",
        "modified": "2023-11-09T13:53:38.017419Z",
        "name": "Maize flour",
        "buying_price": "100.00",
        "selling_price": "120.00",
        "quantity": 100.0,
        "unit_of_measure": "kg"
    },
    {
        "id": 2,
        "created": "2023-11-09T13:53:38.020196Z",
        "modified": "2023-11-09T13:53:38.020246Z",
        "name": "Rice",
        "buying_price": "200.00",
        "selling_price": "240.00",
        "quantity": 50.0,
        "unit_of_measure": "kg"
    },
    {
        "id": 3,
        "created": "2023-11-09T13:53:38.020299Z",
        "modified": "2023-11-09T13:53:38.020320Z",
        "name": "Sugar",
        "buying_price": "300.00",
        "selling_price": "360.00",
        "quantity": 25.0,
        "unit_of_measure": "kg"
    },
    {
        "id": 4,
        "created": "2023-11-09T13:53:38.020365Z",
        "modified": "2023-11-09T13:53:38.020396Z",
        "name": "Milk",
        "buying_price": "400.00",
        "selling_price": "480.00",
        "quantity": 10.0,
        "unit_of_measure": "ltr"
    },
    {
        "id": 5,
        "created": "2023-11-09T13:53:38.020424Z",
        "modified": "2023-11-09T13:53:38.020437Z",
        "name": "Soap",
        "buying_price": "500.00",
        "selling_price": "600.00",
        "quantity": 20.0,
        "unit_of_measure": "bar"
    },
    {
        "id": 6,
        "created": "2023-11-09T13:53:38.020463Z",
        "modified": "2023-11-09T13:53:38.020475Z",
        "name": "Cooking oil",
        "buying_price": "600.00",
        "selling_price": "720.00",
        "quantity": 15.0,
        "unit_of_measure": "ltr"
    },
    {
        "id": 7,
        "created": "2023-11-09T13:53:38.020502Z",
        "modified": "2023-11-09T13:53:38.020513Z",
        "name": "Tea leaves",
        "buying_price": "700.00",
        "selling_price": "840.00",
        "quantity": 10.0,
        "unit_of_measure": "pkt"
    },
    {
        "id": 8,
        "created": "2023-11-09T13:53:38.020540Z",
        "modified": "2023-11-09T13:53:38.020552Z",
        "name": "Salt",
        "buying_price": "800.00",
        "selling_price": "960.00",
        "quantity": 5.0,
        "unit_of_measure": "kg"
    },
    {
        "id": 9,
        "created": "2023-11-09T13:53:38.020578Z",
        "modified": "2023-11-09T13:53:38.020590Z",
        "name": "Biscuits",
        "buying_price": "900.00",
        "selling_price": "1080.00",
        "quantity": 15.0,
        "unit_of_measure": "pkt"
    },
    {
        "id": 10,
        "created": "2023-11-09T13:53:38.020616Z",
        "modified": "2023-11-09T13:53:38.020628Z",
        "name": "Chocolate",
        "buying_price": "1000.00",
        "selling_price": "1200.00",
        "quantity": 10.0,
        "unit_of_measure": "bar"
    },
    {
        "id": 11,
        "created": "2023-11-09T13:53:38.020655Z",
        "modified": "2023-11-09T13:53:38.020666Z",
        "name": "Bread",
        "buying_price": "50.00",
        "selling_price": "60.00",
        "quantity": 50.0,
        "unit_of_measure": "loaf"
    },
    {
        "id": 12,
        "created": "2023-11-09T13:53:38.020693Z",
        "modified": "2023-11-09T13:53:38.020705Z",
        "name": "Eggs",
        "buying_price": "10.00",
        "selling_price": "12.00",
        "quantity": 100.0,
        "unit_of_measure": "dozen"
    },
    {
        "id": 13,
        "created": "2023-11-09T13:53:38.020731Z",
        "modified": "2023-11-09T13:53:38.020743Z",
        "name": "Potatoes",
        "buying_price": "20.00",
        "selling_price": "24.00",
        "quantity": 25.0,
        "unit_of_measure": "kg"
    },
    {
        "id": 14,
        "created": "2023-11-09T13:53:38.020770Z",
        "modified": "2023-11-09T13:53:38.020781Z",
        "name": "Onions",
        "buying_price": "30.00",
        "selling_price": "36.00",
        "quantity": 15.0,
        "unit_of_measure": "kg"
    },
    {
        "id": 15,
        "created": "2023-11-09T13:53:38.020808Z",
        "modified": "2023-11-09T13:53:38.020819Z",
        "name": "Tomatoes",
        "buying_price": "40.00",
        "selling_price": "48.00",
        "quantity": 10.0,
        "unit_of_measure": "kg"
    },
    {
        "id": 16,
        "created": "2023-11-09T13:53:38.020845Z",
        "modified": "2023-11-09T13:53:38.020856Z",
        "name": "Cabbages",
        "buying_price": "50.00",
        "selling_price": "60.00",
        "quantity": 5.0,
        "unit_of_measure": "head"
    }
]

class InventoryAPIView(generics.ListAPIView):
    queryset = Inventory.objects.all()
    serializer_class = InventorySerializer

class MpesaPaymentAPIView(generics.ListCreateAPIView):
    queryset = MpesaPayment.objects.all()
    serializer_class = MpesaPaymentSerializer


def get_inventory_data(request):
    items = InventoryTable()
    return render(request, "hello.html", {"items": items})
    



def sales_point(request):
    items = Inventory.objects.all()

    cart_items = TemporaryCustomerCartItem.objects.all()

    paginator = Paginator(items, 5)
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)



    context = {
        "orders": items,
        "page_obj": page_obj,
        "cart_items": cart_items
    }
    return render(request, "pos/sale.html", context)




def add_to_cart(request, item_id=None):
    item = Inventory.objects.get(id=item_id)



    TemporaryCustomerCartItem.objects.create(
        item=item,
        quantity=1,
        price=item.selling_price
    )
    return redirect("sales-point")


