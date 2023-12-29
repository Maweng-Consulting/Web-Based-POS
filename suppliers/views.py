from django.core.paginator import Paginator
from django.db import transaction
from django.db.models import Q
from django.shortcuts import redirect, render

from suppliers.models import Supplier
from users.models import User


# Create your views here.
def suppliers(request):
    suppliers = Supplier.objects.all()

    if request.method == "POST":
        search_text = request.POST.get("search_text")
        suppliers = Supplier.objects.filter(
            Q(name__icontains=search_text) | 
            Q(user__first_name__icontains=search_text) | 
            Q(user__last_name__icontains=search_text) |
            Q(city__icontains=search_text) |
            Q(country__icontains=search_text)
        )

    paginator = Paginator(suppliers, 10)
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)

    context = {
        "suppliers": suppliers,
        "page_obj": page_obj
    }
    return render(request, "suppliers/suppliers.html", context)

@transaction.atomic
def new_supplier(request):
    if request.method == "POST":
        username = request.POST.get("username")
        email = request.POST.get("email")
        first_name = request.POST.get("first_name")
        last_name = request.POST.get("last_name")
        gender = request.POST.get("gender")
        phone_number = request.POST.get("phone_number")
        id_number = request.POST.get("id_number")

        name = request.POST.get("name")
        supplier_phone = request.POST.get("supplier_phone")
        address = request.POST.get("address")
        city = request.POST.get("city")
        country = request.POST.get("country")
        supplier_email = request.POST.get("supplier_email")
        supplies = request.POST.get("supplies")

        user = User.objects.create(
            first_name=first_name,
            last_name=last_name,
            username=username,
            email=email,
            role="Supplier",
            gender=gender,
            phone_number=phone_number,
            id_number=id_number
        )
        user.set_password(id_number)
        user.save()

        supplier = Supplier.objects.create(
            user=user,
            name=name,
            phone_number=supplier_phone,
            email=supplier_email,
            supplies=supplies,
            address=address,
            city=city,
            country=country
        )
        return redirect("suppliers")


    return render(request, "suppliers/new_supplier.html")


@transaction.atomic
def edit_supplier(request):
    if request.method == "POST":
        supplier_id = request.POST.get("supplier_id")
        username = request.POST.get("username")
        email = request.POST.get("email")
        first_name = request.POST.get("first_name")
        last_name = request.POST.get("last_name")
        gender = request.POST.get("gender")
        phone_number = request.POST.get("phone_number")
        id_number = request.POST.get("id_number")

        name = request.POST.get("name")
        supplier_phone = request.POST.get("supplier_phone")
        address = request.POST.get("address")
        city = request.POST.get("city")
        country = request.POST.get("country")
        supplier_email = request.POST.get("supplier_email")
        supplies = request.POST.get("supplies")

        supplier = Supplier.objects.get(id=supplier_id)

        user = User.objects.get(id=supplier.user.id)
        user.first_name=first_name
        user.last_name=last_name
        user.username=username
        user.email=email
        user.role="Supplier"
        user.gender=gender
        user.phone_number=phone_number
        user.id_number=id_number
        user.save()
        user.set_password(id_number)
        user.save()

        supplier.user=user
        supplier.name=name
        supplier.phone_number=supplier_phone
        supplier.email=supplier_email
        supplier.supplies=supplies
        supplier.address=address
        supplier.city=city
        supplier.country=country
        supplier.save()
        
        return redirect("suppliers")


    return render(request, "suppliers/new_supplier.html")


def delete_supplier(request):
    if request.method == "POST":
        supplier_id = request.POST.get("supplier_id")
        supplier = Supplier.objects.get(id=supplier_id)
        supplier.delete()
        return redirect("suppliers")
    
    return render(request, "suppliers/delete_supplier.html")


def supplier_details(request, supplier_id=None):
    supplier = Supplier.objects.get(id=supplier_id)
    context = {
        "supplier": supplier
    }
    return render(request, "suppliers/supplier_details.html", context)