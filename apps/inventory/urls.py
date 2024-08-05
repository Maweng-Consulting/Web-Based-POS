from django.urls import path

from apps.inventory.views import (delete_stock_item, edit_stock_item,
                                  inventory, new_purchase, purchases,
                                  record_stock, restock_item, stock_logs,
                                  take_out_stock, upload_stock_items, inventory_home, categories, new_category, edit_category, delete_category)

urlpatterns = [
    path("home/", inventory_home, name="inventory-home"),
    path("", inventory, name="inventory"),
    path("record-stock/", record_stock, name="record-stock"),
    path("edit-stock-item/", edit_stock_item, name="edit-stock-item"),
    path("delete-stock-item/", delete_stock_item, name="delete-stock-item"),
    path("restock/", restock_item, name="restock"),
    path("takeout-stock/", take_out_stock, name="takeout-stock"),
    path("stock-logs/", stock_logs, name="stock-logs"),
    path("purchases/", purchases, name="purchases"),
    path("new-purchase/", new_purchase, name="new-purchase"),
    path("upload-stock/", upload_stock_items, name="upload-stock"),

    path("product-categories/", categories, name="product-categories"),
    path("new-category/", new_category, name="new-category"),
    path("edit-category/", edit_category, name="edit-category"),
    path("delete-category/", delete_category, name="delete-category"),
]
