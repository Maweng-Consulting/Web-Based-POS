import csv
from datetime import datetime

from django.core.paginator import Paginator
from django.db.models import ExpressionWrapper, F, Q, Sum, fields
from django.db.models.functions import TruncDate, TruncMonth, TruncYear
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render

from pos.models import Order, OrderItem
from reports.models import ProductSale

date_today = datetime.now().date()
# Create your views here.
def sales_by_product(request):
    product_sales = ProductSale.objects.all().order_by("-created")

    if request.method == "POST":
        search_text = request.POST.get("search_text")
        action_type = request.POST.get("action_type")
        starting_date = request.POST.get("starting_date")
        ending_date = request.POST.get("ending_date")

        if search_text:
            product_sales = ProductSale.objects.filter(Q(item__name__icontains=search_text))

    paginator = Paginator(product_sales, 15)
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)


    # Assuming your model is named OrderItem
    queryset = OrderItem.objects.annotate(
        year=TruncYear('created'),
        month=TruncMonth('created'),
    ).values('year', 'month', 'item').annotate(
        total_quantity=Sum('quantity'),
        total_price=Sum('price'),
    ).order_by('year', 'month', 'item')

    for x in queryset:
        print(x)


    context = {
        "page_obj": page_obj
    }
    return render(request, "reports/sales_by_product.html", context)


def monthly_sales(request):
    this_month = datetime.now().month
    monthly_sales = ProductSale.objects.filter(
        created__month=this_month
    )

    if request.method == "POST":
        action_type = request.POST.get("action_type")

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
        
        print(f"Action Type: {action_type}, Year: {sales_year}, Month: {sales_month}")

        
        if year and month:
            monthly_sales = ProductSale.objects.filter(created__year=year).filter(created__month=month)

        elif year:
            monthly_sales = ProductSale.objects.filter(created__year=year)

        elif month:
            monthly_sales = ProductSale.objects.filter(created__month=month)
        
        if action_type == "export":
            monthly_sales_export = ProductSale.objects.all()

            if sales_year and sales_month:
                monthly_sales_export = ProductSale.objects.filter(created__year=sales_year).filter(created__month=sales_month)

            elif sales_year:
                monthly_sales_export = ProductSale.objects.filter(created__year=sales_year)

            elif sales_month:
                monthly_sales_export = ProductSale.objects.filter(created__month=sales_month)

        
            response = HttpResponse(content_type='text/csv')
            file_name =  f'attachment; filename="Monthly Sales Report - {date_today}.csv"'    
            response['Content-Disposition'] = file_name
            writer = csv.writer(response)
            writer.writerow(["ID", "Sale Date", "Item Sold", "Unit Price", "Quantity", "Sales Total"]) 
            monthly_sales_values = monthly_sales_export.values_list('id', 'created__date', 'item__name', 'unit_price', 'total_quantity', 'total_price')  

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
