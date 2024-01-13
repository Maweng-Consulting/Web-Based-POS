from django.urls import path

from reports.views import monthly_sales, sales_by_product

urlpatterns = [
    path("sales-by-product/", sales_by_product, name="sales-by-product"),
    path("monthly-sales/", monthly_sales, name="monthly-sales"),
]