from django.urls import path

from reports.views import (
    daily_and_weekly_sales,
    general_sales_report,
    monthly_sales,
    sales_by_product,
)

urlpatterns = [
    path("sales-by-product/", sales_by_product, name="sales-by-product"),
    path("monthly-sales/", monthly_sales, name="monthly-sales"),
    path(
        "weekly-and-daily-sales/", daily_and_weekly_sales, name="weekly-and-daily-sales"
    ),
    path("general-sales-report/", general_sales_report, name="general-sales-report"),
]
