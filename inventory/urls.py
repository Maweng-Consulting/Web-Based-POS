from django.urls import path

from inventory.views import (delete_stock_item, edit_stock_item, inventory,
                             new_purchase, purchases, record_stock,
                             restock_item, stock_logs, take_out_stock)

urlpatterns = [
    path("", inventory, name="inventory"),
    path("record-stock/", record_stock, name="record-stock"),
    path("edit-stock-item/", edit_stock_item, name="edit-stock-item"),
    path("delete-stock-item/", delete_stock_item, name="delete-stock-item"),
    path("restock/", restock_item, name="restock"),
    path("takeout-stock/", take_out_stock, name="takeout-stock"),
    path("stock-logs/", stock_logs, name="stock-logs"),


    path("purchases/", purchases, name="purchases"),
    path("new-purchase/", new_purchase, name="new-purchase"),
]