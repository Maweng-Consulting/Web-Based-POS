from django.urls import path
from inventory.views import (
    inventory, record_stock, edit_stock_item, 
    delete_stock_item, restock_item, take_out_stock
)

urlpatterns = [
    path("", inventory, name="inventory"),
    path("record-stock/", record_stock, name="record-stock"),
    path("edit-stock-item/", edit_stock_item, name="edit-stock-item"),
    path("delete-stock-item/", delete_stock_item, name="delete-stock-item"),
    path("restock/", restock_item, name="restock"),
    path("takeout-stock/", take_out_stock, name="takeout-stock"),
]