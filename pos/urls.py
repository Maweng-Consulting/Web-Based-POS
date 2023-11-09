from django.urls import path

from pos.views import (InventoryAPIView, MpesaPaymentAPIView, add_to_cart,
                       get_inventory_data, redeem_mpesa_payment,
                       remove_from_cart, sales_point)

urlpatterns = [
    path("", sales_point, name="sales-point"),

    path("add-to-cart/<int:item_id>/", add_to_cart, name="add-to-cart"),
    path("remove-from-cart/<int:item_id>/", remove_from_cart, name="remove-from-cart"),
    path("redeem-mpesa-payment/<int:payment_id>/", redeem_mpesa_payment, name="redeem-mpesa-payment"),

    path("inventories/", InventoryAPIView.as_view(), name="get_table_data"),
    path("inventory-data/", get_inventory_data, name="inventory-data"),
    path("mpesa-payments/", MpesaPaymentAPIView.as_view(), name="mpesa-payments"),
]