from django.urls import path

from pos.views import (InventoryAPIView, MpesaPaymentAPIView, add_to_cart,
                       get_inventory_data, sales_point)

urlpatterns = [
    path("", sales_point, name="sales-point"),
    path("add-to-cart/<int:item_id>/", add_to_cart, name="add-to-cart"),
    path("inventories/", InventoryAPIView.as_view(), name="get_table_data"),
    path("inventory-data/", get_inventory_data, name="inventory-data"),
    path("mpesa-payments/", MpesaPaymentAPIView.as_view(), name="mpesa-payments"),
]