import calendar
import csv
from datetime import datetime

from django.core.paginator import Paginator
from django.db.models import ExpressionWrapper, F, Q, Sum, fields
from django.db.models.functions import TruncDate, TruncMonth, TruncYear
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import redirect, render

from apps.inventory.models import Inventory
from apps.pos.models import Order, OrderItem
from apps.reports.models import ProductSale, Report
from apps.users.models import User

date_today = datetime.now().date()
# Create your views here.
def reports_home(request):
    reports = Report.objects.all().order_by("id")
    context = {
        "reports": reports
    }
    return render(request, "reports/home.html", context)

def sales_by_product(request):
    product_sales = ProductSale.objects.all().order_by("-created")

    if request.method == "POST":
        product_name = request.POST.get("product_name")
        action_type = request.POST.get("action_type")
        product_sale_month = request.POST.get("product_sale_month")
        product_sale_year = request.POST.get("product_sale_year")

        year_value = request.POST.get("year_value")
        month_value = request.POST.get("month_value")
        product_value = request.POST.get("product_value")

        if product_sale_month:
            product_sale_month = int(product_sale_month)

        if product_sale_year:
            product_sale_year = int(product_sale_year)

        if year_value:
            year_value = int(year_value)

        if month_value:
            month_value = int(month_value)

        if product_value and year_value and month_value:
            product_sales = (
                ProductSale.objects.filter(Q(item__name__icontains=product_value))
                .filter(created__year=year_value)
                .filter(created__month=month_value)
            )

        elif product_value and year_value:
            product_sales = ProductSale.objects.filter(
                Q(item__name__icontains=product_value)
            ).filter(created__year=year_value)

        elif year_value and month_value:
            product_sales = ProductSale.objects.filter(created__year=year_value).filter(
                created__month=month_value
            )

        elif product_value:
            product_sales = ProductSale.objects.filter(
                Q(item__name__icontains=product_value)
            )

        elif month_value:
            product_sales = ProductSale.objects.filter(created__month=month_value)

        elif year_value:
            product_sales = ProductSale.objects.filter(created__year=year_value)

        if action_type == "export":
            product_sales_export = ProductSale.objects.all()

            print(f"Product: {product_name}, Month: {product_sale_month}, Year: {product_sale_year}")

            report_name = "Product Sales Report"

            if product_name and product_sale_year and product_sale_month:
                product_sales_export = (
                    ProductSale.objects.filter(Q(item__name__icontains=product_name))
                    .filter(created__year=product_sale_year)
                    .filter(created__month=product_sale_month)
                )

                report_name = f"Products Sales Report -{calendar.month_name[product_sale_month]} - {product_sale_year}"

            elif product_name and product_sale_year:
                product_sales_export = ProductSale.objects.filter(
                    Q(item__name__icontains=product_name)
                ).filter(created__year=product_sale_year)

                report_name = f"Products Sales Report - {product_sale_year}"

            elif product_name and product_sale_month:
                product_sales_export = ProductSale.objects.filter(
                    Q(item__name__icontains=product_name)
                ).filter(created__month=product_sale_month)

                report_name = (
                    f"Products Sales Report -{calendar.month_name[product_sale_month]}"
                )

            elif product_sale_year and product_sale_month:
                product_sales_export = ProductSale.objects.filter(
                    created__year=product_sale_year
                ).filter(created__month=product_sale_month)

                report_name = f"Products Sales Report -{calendar.month_name[product_sale_month]} - {product_sale_year}"

            elif product_name:
                product_sales_export = ProductSale.objects.filter(
                    Q(item__name__icontains=product_name)
                )

                report_name = "Products Sales Report"

            elif product_sale_month:
                product_sales_export = ProductSale.objects.filter(
                    created__month=product_sale_month
                )
                report_name = (
                    f"Product Sales Report -{calendar.month_name[product_sale_month]}"
                )

            elif product_sale_year:
                product_sales_export = ProductSale.objects.filter(
                    created__year=product_sale_year
                )
                report_name = f"Product Sales Report - {product_sale_year}"

            response = HttpResponse(content_type="text/csv")
            file_name = f'attachment; filename="{report_name}.csv"'
            response["Content-Disposition"] = file_name
            writer = csv.writer(response)
            writer.writerow(
                [
                    "ID",
                    "Sale Date",
                    "Item Sold",
                    "Unit Price",
                    "Quantity",
                    "Sales Total",
                ]
            )
            product_sales_values = product_sales_export.values_list(
                "id",
                "created__date",
                "item__name",
                "unit_price",
                "total_quantity",
                "total_price",
            )

            cummulative_total = sum(
                list(product_sales_export.values_list("total_price", flat=True))
            )
            for sale in product_sales_values:
                writer.writerow(sale)
            writer.writerow(["", "", "", "", "", "", ""])
            writer.writerow(["Total Sales", "", "", "", "", "", cummulative_total])
            return response

    paginator = Paginator(product_sales, 10)
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)

    items = Inventory.objects.all()

    context = {"page_obj": page_obj, "items": items}
    return render(request, "reports/sales_by_product.html", context)


def monthly_sales(request):
    this_month = datetime.now().month
    monthly_sales = ProductSale.objects.filter(created__month=this_month)

    if request.method == "POST":
        action_type = request.POST.get("action_type")

        product_name = request.POST.get("product_name")
        sales_year = request.POST.get("sales_year")
        sales_month = request.POST.get("sales_month")
        

        year = request.POST.get("year")
        month = request.POST.get("month")
        month_product = request.POST.get("month_product")

        if month:
            month = int(month)

        if year:
            year = int(year)

        if sales_year:
            sales_year = int(sales_year)

        if sales_month:
            sales_month = int(sales_month)

        print(f"Action Type: {action_type}, Year: {sales_year}, Month: {sales_month}")

        if month_product and year and month:
            monthly_sales = ProductSale.objects.filter(item__name=month_product).filter(created__year=year).filter(created__month=month)

        
        elif month_product and year:
            monthly_sales = ProductSale.objects.filter(item__name=month_product).filter(created__year=year)

        elif month_product and month:
            monthly_sales = ProductSale.objects.filter(item__name=month_product).filter(created__month=month)

        elif year and month:
            monthly_sales = ProductSale.objects.filter(created__year=year).filter(created__month=month)

        elif month_product:
            monthly_sales = ProductSale.objects.filter(item__name=month_product)

        elif year:
            monthly_sales = ProductSale.objects.filter(created__year=year)

        elif month:
            monthly_sales = ProductSale.objects.filter(created__month=month)

        if action_type == "export":
            monthly_sales_export = ProductSale.objects.all()

            report_name = "Monthly Sales Report"

            if product_name and sales_year and sales_month:
                monthly_sales_export = ProductSale.objects.filter(item__name=product_name).filter(created__year=sales_year).filter(created__month=sales_month)
                report_name = f"{product_name} Sales Report-{calendar.month_name[sales_month]}-{sales_year}"

            elif product_name and sales_year:
                monthly_sales_export = ProductSale.objects.filter(item__name=product_name).filter(created__year=sales_year)
                report_name = f"{product_name} Sales Report-{sales_year}"

            elif product_name and sales_month:
                monthly_sales_export = ProductSale.objects.filter(item__name=product_name).filter(created__month=sales_month)
                report_name = f"{product_name} Sales Report-{calendar.month_name[sales_month]}"

            elif sales_year and sales_month:
                monthly_sales_export = ProductSale.objects.filter(created__year=sales_year).filter(created__month=sales_month)
                report_name = f"Monthly Sales Report-{calendar.month_name[sales_month]}-{sales_year}"

            elif product_name:
                monthly_sales_export = ProductSale.objects.filter(item__name=product_name)
                report_name = f"{product_name} Sales Report"

            elif sales_year:
                monthly_sales_export = ProductSale.objects.filter(created__year=sales_year)
                report_name = f"Monthly Sales Report-{sales_year}"

            elif sales_month:
                monthly_sales_export = ProductSale.objects.filter(created__month=sales_month)
                report_name = f"Monthly Sales Report-{calendar.month_name[sales_month]}"

            response = HttpResponse(content_type="text/csv")
            file_name = f'attachment; filename="{report_name}.csv"'
            response["Content-Disposition"] = file_name
            writer = csv.writer(response)
            writer.writerow(
                [
                    "ID",
                    "Sale Date",
                    "Item Sold",
                    "Unit Price",
                    "Quantity",
                    "Sales Total",
                ]
            )
            monthly_sales_values = monthly_sales_export.values_list(
                "id",
                "created__date",
                "item__name",
                "unit_price",
                "total_quantity",
                "total_price",
            )

            cummulative_total = sum(
                list(monthly_sales_export.values_list("total_price", flat=True))
            )
            for sale in monthly_sales_values:
                writer.writerow(sale)

            writer.writerow(["", "", "", "", "", "", ""])
            writer.writerow(["Total Sales", "", "", "", "", "", cummulative_total])
            return response

    paginator = Paginator(monthly_sales, 10)
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)
    items = Inventory.objects.all()

    context = {"page_obj": page_obj, "items": items}
    return render(request, "reports/monthly_sales.html", context)


def daily_and_weekly_sales(request):
    weekly_sales = ProductSale.objects.all().order_by("-created")

    if request.method == "POST":
        action_type = request.POST.get("action_type")
        product_name = request.POST.get("weekly_product_name")
        export_product_name = request.POST.get("product_name")
        report_start_date = request.POST.get("report_start_date")
        report_end_date = request.POST.get("report_end_date")

        start_date = request.POST.get("report_start")
        end_date = request.POST.get("report_end")

        if start_date:
            if isinstance(start_date, str):
                start_date = datetime.strptime(start_date, "%Y-%m-%d").date()

        if end_date:
            if isinstance(end_date, str):
                end_date = datetime.strptime(end_date, "%Y-%m-%d").date()

        if product_name and start_date and end_date:
            weekly_sales = (
                ProductSale.objects.filter(Q(item__name__icontains=product_name))
                .filter(created__date__gte=start_date)
                .filter(created__date__lte=end_date)
            )

        elif product_name and start_date:
            weekly_sales = ProductSale.objects.filter(
                Q(item__name__icontains=product_name)
            ).filter(created__date__gte=start_date)

        elif product_name and end_date:
            weekly_sales = ProductSale.objects.filter(
                Q(item__name__icontains=product_name)
            ).filter(created__date__lte=end_date)

        elif start_date and end_date:
            weekly_sales = ProductSale.objects.filter(
                created__date__gte=start_date
            ).filter(created__date__lte=end_date)

        elif product_name:
            weekly_sales = ProductSale.objects.filter(
                Q(item__name__icontains=product_name)
            )

        elif start_date:
            weekly_sales = ProductSale.objects.filter(created__date=start_date)

        elif end_date:
            weekly_sales = ProductSale.objects.filter(created__date=end_date)

        if action_type == "export":
            weekly_and_daily_sales_export = ProductSale.objects.all()

            if report_start_date:
                if isinstance(report_start_date, str):
                    report_start_date = datetime.strptime(
                        report_start_date, "%Y-%m-%d"
                    ).date()

            elif report_end_date:
                if isinstance(report_end_date, str):
                    report_end_date = datetime.strptime(
                        report_end_date, "%Y-%m-%d"
                    ).date()

            if export_product_name and report_end_date and report_end_date:
                weekly_and_daily_sales_export = (
                    ProductSale.objects.filter(
                        Q(item__name__icontains=export_product_name)
                    )
                    .filter(created__date__gte=report_start_date)
                    .filter(created__date__lte=report_end_date)
                )

            elif export_product_name and report_start_date:
                weekly_and_daily_sales_export = ProductSale.objects.filter(
                    Q(item__name__icontains=export_product_name)
                ).filter(created__date__gte=report_start_date)

            elif export_product_name and end_date:
                weekly_and_daily_sales_export = ProductSale.objects.filter(
                    Q(item__name__icontains=export_product_name)
                ).filter(created__date__lte=report_end_date)

            elif start_date and end_date:
                weekly_and_daily_sales_export = ProductSale.objects.filter(
                    created__date__gte=report_start_date
                ).filter(created__date__lte=report_end_date)

            elif export_product_name:
                weekly_and_daily_sales_export = ProductSale.objects.filter(
                    Q(item__name__icontains=export_product_name)
                )

            elif start_date:
                weekly_and_daily_sales_export = ProductSale.objects.filter(
                    created__date=report_start_date
                )

            elif end_date:
                weekly_and_daily_sales_export = ProductSale.objects.filter(
                    created__date=report_end_date
                )

            response = HttpResponse(content_type="text/csv")
            file_name = f'attachment; filename="Daily or Weekly Sales Report.csv"'
            response["Content-Disposition"] = file_name
            writer = csv.writer(response)
            writer.writerow(
                [
                    "ID",
                    "Sale Date",
                    "Item Sold",
                    "Unit Price",
                    "Quantity",
                    "Sales Total",
                ]
            )
            weekly_sales_values = weekly_and_daily_sales_export.values_list(
                "id",
                "created__date",
                "item__name",
                "unit_price",
                "total_quantity",
                "total_price",
            )

            cummulative_total = sum(
                list(
                    weekly_and_daily_sales_export.values_list("total_price", flat=True)
                )
            )

            for sale in weekly_sales_values:
                writer.writerow(sale)

            writer.writerow(["", "", "", "", "", "", ""])
            writer.writerow(["Total Sales", "", "", "", "", "", cummulative_total])
            return response

        print(
            f"Product: {product_name}, Start Date: {type(start_date)}, End Date: {type(end_date)}"
        )

    paginator = Paginator(weekly_sales, 10)
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)

    items = Inventory.objects.all()
    context = {"page_obj": page_obj, "items": items}
    return render(request, "reports/weekly_sales.html", context)


def general_sales_report(request):
    orders = Order.objects.all().order_by("-created")

    sellers = User.objects.filter(role__in=["cashier", "admin"])

    if request.method == "POST":
        # Filter Data
        sold_by = request.POST.get("sold_by")
        sale_type = request.POST.get("sale_type")
        sales_from = request.POST.get("sales_from")
        sales_to = request.POST.get("sales_to")
        action_type = request.POST.get("action_type")

        # Download Filters
        served_by = request.POST.get("served_by")
        sales_from_date = request.POST.get("sales_from_date")
        sales_to_date = request.POST.get("sales_to_date")
        order_type = request.POST.get("order_type")

        filter_object = {
            "sold_by": sold_by,
            "sale_type": sale_type,
            "sales_from": sales_from,
            "sales_to": sales_to,
        }

        request.session["filter_object"] = filter_object

        if sales_from:
            if isinstance(sales_from, str):
                sales_from = datetime.strptime(sales_from, "%Y-%m-%d").date()

        if sales_to:
            if isinstance(sales_to, str):
                sales_to = datetime.strptime(sales_to, "%Y-%m-%d").date()

        if sold_by and sale_type and sales_from and sales_to:
            orders = (
                Order.objects.filter(order_type=sale_type, served_by__id=sold_by)
                .filter(created__date__gte=sales_from)
                .filter(created__date__lte=sales_to)
            )

        elif sold_by and sale_type and sales_from:
            orders = Order.objects.filter(
                order_type=sale_type, served_by__id=sold_by
            ).filter(created__date=sales_from)

        elif sold_by and sale_type and sales_to:
            orders = Order.objects.filter(
                order_type=sale_type, served_by__id=sold_by
            ).filter(created__date=sales_to)

        elif sold_by and sales_from and sales_to:
            orders = (
                Order.objects.filter(served_by__id=sold_by)
                .filter(created__date__gte=sales_from)
                .filter(created__date__lte=sales_to)
            )

        elif sold_by and sale_type:
            orders = Order.objects.filter(order_type=sale_type, served_by__id=sold_by)

        elif sold_by and sales_from:
            orders = Order.objects.filter(served_by__id=sold_by).filter(
                created__date=sales_from
            )

        elif sold_by and sales_to:
            orders = Order.objects.filter(served_by__id=sold_by).filter(
                created__date=sales_to
            )

        elif sales_from and sales_to:
            orders = Order.objects.filter(created__date__gte=sales_from).filter(
                created__date__lte=sales_to
            )

        elif sold_by:
            orders = Order.objects.filter(served_by__id=sold_by)

        elif sale_type:
            orders = Order.objects.filter(order_type=sale_type)

        elif sales_from:
            orders = Order.objects.filter(created__date=sales_from)

        elif sales_to:
            orders = Order.objects.filter(created__date=sales_to)

        if action_type == "export":
            orders_export = Order.objects.all().order_by("-created")

            print(
                f"Sold By: {served_by}, Sale Type: {order_type}, From: {sales_from_date}, To: {sales_to_date}"
            )

            if sales_from_date:
                if isinstance(sales_from_date, str):
                    sales_from_date = datetime.strptime(
                        sales_from_date, "%Y-%m-%d"
                    ).date()

            if sales_to_date:
                if isinstance(sales_to_date, str):
                    sales_to_date = datetime.strptime(sales_to_date, "%Y-%m-%d").date()

            if served_by and order_type and sales_from_date and sales_to_date:
                orders_export = (
                    Order.objects.filter(order_type=order_type, served_by__id=served_by)
                    .filter(created__date__gte=sales_from_date)
                    .filter(created__date__lte=sales_to_date)
                )

            elif served_by and order_type and sales_from_date:
                orders_export = Order.objects.filter(
                    order_type=order_type, served_by__id=served_by
                ).filter(created__date=sales_from_date)

            elif served_by and order_type and sales_to_date:
                orders_export = Order.objects.filter(
                    order_type=order_type, served_by__id=served_by
                ).filter(created__date=sales_to_date)

            elif served_by and sales_from_date and sales_to_date:
                orders_export = (
                    Order.objects.filter(served_by__id=served_by)
                    .filter(created__date__gte=sales_from_date)
                    .filter(created__date__lte=sales_to_date)
                )

            elif served_by and order_type:
                orders_export = Order.objects.filter(
                    order_type=order_type, served_by__id=served_by
                )

            elif served_by and sales_from_date:
                orders_export = Order.objects.filter(served_by__id=served_by).filter(
                    created__date=sales_from_date
                )

            elif served_by and sales_to_date:
                orders_export = Order.objects.filter(served_by__id=served_by).filter(
                    created__date=sales_to_date
                )

            elif sales_from_date and sales_to_date:
                orders_export = Order.objects.filter(
                    created__date__gte=sales_from_date
                ).filter(created__date__lte=sales_to_date)

            elif served_by:
                orders_export = Order.objects.filter(served_by__id=served_by)

            elif order_type:
                orders_export = Order.objects.filter(order_type=order_type)

            elif sales_from_date:
                orders_export = Order.objects.filter(created__date=sales_from_date)

            elif sales_to_date:
                orders_export = Order.objects.filter(created__date=sales_to_date)

            response = HttpResponse(content_type="text/csv")
            file_name = f'attachment; filename="Sales Report.csv"'
            response["Content-Disposition"] = file_name
            writer = csv.writer(response)
            writer.writerow(["ID", "Sale Date", "Sold By", "Order Type", "Sales Total"])
            orders_export_values = orders_export.values_list(
                "id", "created__date", "served_by__username", "order_type", "total_cost"
            )

            cummulative_total = sum(
                list(orders_export.values_list("total_cost", flat=True))
            )

            for sale in orders_export_values:
                writer.writerow(sale)

            writer.writerow(["", "", "", "", ""])
            writer.writerow(["Total Sales", "", "", "", cummulative_total])
            return response

        # return redirect("general-sales-report")

    paginator = Paginator(orders, 15)
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)

    context = {"orders": orders, "page_obj": page_obj, "sellers": sellers}
    return render(request, "reports/general_sales.html", context)



def sales_today(request):
    weekly_sales = ProductSale.objects.filter(created__date=date_today).order_by("-created")

    if request.method == "POST":
        action_type = request.POST.get("action_type")
        product_name = request.POST.get("weekly_product_name")
        export_product_name = request.POST.get("product_name")
        

        if product_name:
            weekly_sales = (
                ProductSale.objects.filter(Q(item__name__icontains=product_name))
            )

        if action_type == "export":
            weekly_and_daily_sales_export = ProductSale.objects.all()

            if export_product_name:
                weekly_and_daily_sales_export = ProductSale.objects.filter(
                    Q(item__name__icontains=export_product_name)
                )

            response = HttpResponse(content_type="text/csv")
            file_name = f'attachment; filename="Today Sales Report.csv"'
            response["Content-Disposition"] = file_name
            writer = csv.writer(response)
            writer.writerow(
                [
                    "ID",
                    "Sale Date",
                    "Item Sold",
                    "Unit Price",
                    "Quantity",
                    "Sales Total",
                ]
            )
            weekly_sales_values = weekly_and_daily_sales_export.values_list(
                "id",
                "created__date",
                "item__name",
                "unit_price",
                "total_quantity",
                "total_price",
            )

            cummulative_total = sum(
                list(
                    weekly_and_daily_sales_export.values_list("total_price", flat=True)
                )
            )

            for sale in weekly_sales_values:
                writer.writerow(sale)

            writer.writerow(["", "", "", "", "", "", ""])
            writer.writerow(["Total Sales", "", "", "", "", "", cummulative_total])
            return response


    paginator = Paginator(weekly_sales, 10)
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)

    items = Inventory.objects.all()
    context = {"page_obj": page_obj, "items": items}
    return render(request, "reports/sales_today.html", context)
