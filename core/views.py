from django.contrib.auth.decorators import login_required
from django.shortcuts import render

from users.models import Customer, User


# Create your views here.
@login_required(login_url="/users/login/")
def home(request):
    customers_count = Customer.objects.all().count()
    staff_count = User.objects.exclude(role__in=["Supplier", "Broker"]).count()

    context = {
        "customers_count": customers_count,
        "staff_count": staff_count
    }
    return render(request, "home.html", context)