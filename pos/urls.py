from django.urls import path

from pos.views import (InventoryAPIView, MpesaPaymentAPIView, add_to_cart,
                       credit_orders, credit_sales_point, get_inventory_data,
                       mark_order_as_paid, new_credit_order, orders,
                       print_order_receipt, redeem_mpesa_payment,
                       remove_from_cart, sales_point)

urlpatterns = [
    path("", sales_point, name="sales-point"),
    path("credit-sales-point/", credit_sales_point, name="credit-sales-point"),

    path("add-to-cart/<int:item_id>/", add_to_cart, name="add-to-cart"),
    path("remove-from-cart/<int:item_id>/", remove_from_cart, name="remove-from-cart"),
    path("redeem-mpesa-payment/<int:payment_id>/", redeem_mpesa_payment, name="redeem-mpesa-payment"),

    path("inventories/", InventoryAPIView.as_view(), name="get_table_data"),
    path("inventory-data/", get_inventory_data, name="inventory-data"),
    path("mpesa-payments/", MpesaPaymentAPIView.as_view(), name="mpesa-payments"),

    path("orders/", orders, name="orders"),
    path("credit-orders/", credit_orders, name="credit-orders"),
    path("mark-order-as-paid/<int:user_id>/", mark_order_as_paid, name="mark-order-as-paid"),
    path("new-credit-order/", new_credit_order, name="new-credit-order"),

    path("print-order/<int:order_id>/", print_order_receipt, name="print-order"),
]