from datetime import datetime, timedelta

from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect, render

from pos.models import Order
from users.models import Customer, User

date_today = datetime.now().date()

# Get the current date and time
now = datetime.now()

# Calculate the date 7 days ago
seven_days_ago = now - timedelta(days=7)


# Create your views here.
@login_required(login_url="/users/login/")
def home(request):
    if request.user.role == "cashier":
        return redirect("inventory")

    customers_count = Customer.objects.all().count()
    staff_count = User.objects.exclude(role__in=["Supplier", "Broker"]).count()

    orders_placed_today = Order.objects.filter(created__date=date_today).count()
    orders_today = sum(
        list(
            Order.objects.filter(created__date=date_today).values_list(
                "total_cost", flat=True
            )
        )
    )

    week_orders = sum(
        list(
            Order.objects.filter(created__date__gte=seven_days_ago).values_list(
                "total_cost", flat=True
            )
        )
    )

    month_orders = sum(
        list(
            Order.objects.filter(created__date__month=date_today.month).values_list(
                "total_cost", flat=True
            )
        )
    )

    context = {
        "customers_count": customers_count,
        "orders_today": orders_today,
        "orders_placed_today": orders_placed_today,
        "staff_count": staff_count,
        "month_orders": month_orders,
        "week_orders": week_orders,
    }
    return render(request, "home.html", context)
