from django.contrib import admin

from apps.reports.models import ProductSale


# Register your models here.
@admin.register(ProductSale)
class ProductSaleAdmin(admin.ModelAdmin):
    list_display = [
        "id",
        "created",
        "order",
        "item",
        "unit_price",
        "total_quantity",
        "total_price",
    ]
