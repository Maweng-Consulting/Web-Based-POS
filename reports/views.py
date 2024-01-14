import calendar
import csv
from datetime import datetime

from django.core.paginator import Paginator
from django.db.models import ExpressionWrapper, F, Q, Sum, fields
from django.db.models.functions import TruncDate, TruncMonth, TruncYear
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render

from inventory.models import Inventory
from pos.models import Order, OrderItem
from reports.models import ProductSale

date_today = datetime.now().date()
# Create your views here.


def sales_by_product(request):
    product_sales = ProductSale.objects.all().order_by("-created")

    if request.method == "POST":
        product_name = request.POST.get("product_name")
        action_type = request.POST.get("action_type")
        product_sale_month = request.POST.get("product_sale_month")
        product_sale_year = request.POST.get("product_sale_year")

        if product_sale_month:
            product_sale_month = int(product_sale_month)

        if product_sale_year:
            product_sale_year = int(product_sale_year)

        if product_name:
            product_sales = ProductSale.objects.filter(
                Q(item__name__icontains=product_name))

        if action_type == "export":
            product_sales_export = ProductSale.objects.all()

            report_name = "Product Sales Report"

            if product_name and product_sale_year and product_sale_month:
                product_sales_export = ProductSale.objects.filter(
                    Q(item__name__icontains=product_name)
                ).filter(created__year=product_sale_year).filter(created__month=product_sale_month)

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

                report_name = f"Products Sales Report -{calendar.month_name[product_sale_month]}"

            elif product_sale_year and product_sale_month:
                product_sales_export = ProductSale.objects.filter(
                    created__year=product_sale_year).filter(created__month=product_sale_month)

                report_name = f"Products Sales Report -{calendar.month_name[product_sale_month]} - {product_sale_year}"

            elif product_name:
                product_sales_export = ProductSale.objects.filter(
                    Q(item__name__icontains=product_name))

                report_name = "Products Sales Report"

            elif product_sale_month:
                product_sales_export = ProductSale.objects.filter(
                    created__month=product_sale_month)
                report_name = f"Product Sales Report -{calendar.month_name[product_sale_month]}"

            elif product_sale_year:
                product_sales_export = ProductSale.objects.filter(
                    created__year=product_sale_year)
                report_name = f"Product Sales Report - {product_sale_year}"

            response = HttpResponse(content_type='text/csv')
            file_name = f'attachment; filename="{report_name}.csv"'
            response['Content-Disposition'] = file_name
            writer = csv.writer(response)
            writer.writerow(["ID", "Sale Date", "Item Sold",
                            "Unit Price", "Quantity", "Sales Total"])
            product_sales_values = product_sales_export.values_list(
                'id', 'created__date', 'item__name', 'unit_price', 'total_quantity', 'total_price')

            for sale in product_sales_values:
                writer.writerow(sale)
            return response

    paginator = Paginator(product_sales, 15)
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)

    items = Inventory.objects.all()

    context = {
        "page_obj": page_obj,
        "items": items
    }
    return render(request, "reports/sales_by_product.html", context)


def monthly_sales(request):
    this_month = datetime.now().month
    monthly_sales = ProductSale.objects.filter(
        created__month=this_month
    )

    if request.method == "POST":
        action_type = request.POST.get("action_type")
        search_text = request.POST.get("search_text")

        sales_year = request.POST.get("sales_year")
        sales_month = request.POST.get("sales_month")

        year = request.POST.get("year")
        month = request.POST.get("month")

        if month:
            month = int(month)

        if year:
            year = int(year)

        if sales_year:
            sales_year = int(sales_year)

        if sales_month:
            sales_month = int(sales_month)

        print(
            f"Action Type: {action_type}, Year: {sales_year}, Month: {sales_month}")

        if search_text:
            monthly_sales = ProductSale.objects.filter(
                Q(item__name__icontains=search_text))

        if year and month:
            monthly_sales = ProductSale.objects.filter(
                created__year=year).filter(created__month=month)

        elif year:
            monthly_sales = ProductSale.objects.filter(created__year=year)

        elif month:
            monthly_sales = ProductSale.objects.filter(created__month=month)

        if action_type == "export":
            monthly_sales_export = ProductSale.objects.all()

            report_name = "Monthly Sales Report"

            if sales_year and sales_month:
                monthly_sales_export = ProductSale.objects.filter(
                    created__year=sales_year).filter(created__month=sales_month)
                report_name = f"Monthly Sales Report - {calendar.month_name[sales_month]} - {sales_year}"

            elif sales_year:
                monthly_sales_export = ProductSale.objects.filter(
                    created__year=sales_year)
                report_name = f"Monthly Sales Report - {sales_year}"

            elif sales_month:
                monthly_sales_export = ProductSale.objects.filter(
                    created__month=sales_month)
                report_name = f"Monthly Sales Report - {calendar.month_name[sales_month]}"

            response = HttpResponse(content_type='text/csv')
            file_name = f'attachment; filename="{report_name}.csv"'
            response['Content-Disposition'] = file_name
            writer = csv.writer(response)
            writer.writerow(["ID", "Sale Date", "Item Sold",
                            "Unit Price", "Quantity", "Sales Total"])
            monthly_sales_values = monthly_sales_export.values_list(
                'id', 'created__date', 'item__name', 'unit_price', 'total_quantity', 'total_price')

            for sale in monthly_sales_values:
                writer.writerow(sale)
            return response

    paginator = Paginator(monthly_sales, 15)
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)

    context = {
        "page_obj": page_obj
    }
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
            weekly_sales = ProductSale.objects.filter(Q(item__name__icontains=product_name)
                                                      ).filter(created__date__gte=start_date).filter(created__date__lte=end_date)

        elif product_name and start_date:
            weekly_sales = ProductSale.objects.filter(Q(item__name__icontains=product_name)
                                                      ).filter(created__date__gte=start_date)

        elif product_name and end_date:
            weekly_sales = ProductSale.objects.filter(Q(item__name__icontains=product_name)
                                                      ).filter(created__date__lte=end_date)

        elif start_date and end_date:
            weekly_sales = ProductSale.objects.filter(
                created__date__gte=start_date).filter(created__date__lte=end_date)

        elif product_name:
            weekly_sales = ProductSale.objects.filter(
                Q(item__name__icontains=product_name))

        elif start_date:
            weekly_sales = ProductSale.objects.filter(created__date=start_date)

        elif end_date:
            weekly_sales = ProductSale.objects.filter(created__date=end_date)

        if action_type == "export":
            weekly_and_daily_sales_export = ProductSale.objects.all()

            if report_start_date:
                if isinstance(report_start_date, str):
                    report_start_date = datetime.strptime(
                        report_start_date, "%Y-%m-%d").date()

            elif report_end_date:
                if isinstance(report_end_date, str):
                    report_end_date = datetime.strptime(
                        report_end_date, "%Y-%m-%d").date()

            if export_product_name and report_end_date and report_end_date:
                weekly_and_daily_sales_export = ProductSale.objects.filter(Q(item__name__icontains=export_product_name)
                                                                           ).filter(created__date__gte=report_start_date).filter(created__date__lte=report_end_date)

            elif export_product_name and report_start_date:
                weekly_and_daily_sales_export = ProductSale.objects.filter(Q(item__name__icontains=export_product_name)
                                                                           ).filter(created__date__gte=report_start_date)

            elif export_product_name and end_date:
                weekly_and_daily_sales_export = ProductSale.objects.filter(Q(item__name__icontains=export_product_name)
                                                                           ).filter(created__date__lte=report_end_date)

            elif start_date and end_date:
                weekly_and_daily_sales_export = ProductSale.objects.filter(
                    created__date__gte=report_start_date).filter(created__date__lte=report_end_date)

            elif export_product_name:
                weekly_and_daily_sales_export = ProductSale.objects.filter(
                    Q(item__name__icontains=export_product_name))

            elif start_date:
                weekly_and_daily_sales_export = ProductSale.objects.filter(
                    created__date=report_start_date)

            elif end_date:
                weekly_and_daily_sales_export = ProductSale.objects.filter(
                    created__date=report_end_date)

            response = HttpResponse(content_type='text/csv')
            file_name = f'attachment; filename="Daily or Weekly Sales Report.csv"'
            response['Content-Disposition'] = file_name
            writer = csv.writer(response)
            writer.writerow(["ID", "Sale Date", "Item Sold",
                            "Unit Price", "Quantity", "Sales Total"])
            weekly_sales_values = weekly_and_daily_sales_export.values_list(
                'id', 'created__date', 'item__name', 'unit_price', 'total_quantity', 'total_price')

            for sale in weekly_sales_values:
                writer.writerow(sale)
            return response

        print(
            f"Product: {product_name}, Start Date: {type(start_date)}, End Date: {type(end_date)}")

    paginator = Paginator(weekly_sales, 15)
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)

    items = Inventory.objects.all()
    context = {
        "page_obj": page_obj,
        "items": items
    }
    return render(request, "reports/weekly_sales.html", context)
