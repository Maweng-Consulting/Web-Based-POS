from django.contrib import admin

from apps.reports.models import ProductSale, Report


# Register your models here.
@admin.register(Report)
class ReportAdmin(admin.ModelAdmin):
    list_display = ["id", "name", "report_url"]

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
