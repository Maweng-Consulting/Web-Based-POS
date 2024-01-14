from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.shortcuts import redirect, render

# Create your views here.
from users.models import Customer, User


# Create your views here.
@login_required(login_url="/users/login/")
def register(request):
    if request.method == 'POST':
        username = request.POST.get("username")
        email = request.POST.get("email")
        first_name = request.POST.get("first_name")
        last_name = request.POST.get("last_name")
        gender = request.POST.get("gender")
        role = request.POST.get("role")
        phone_number = request.POST.get("phone_number")
        id_number = request.POST.get("id_number")
        position = request.POST.get("position")

        user_by_email = User.objects.filter(email=email).first()
        user_by_username = User.objects.filter(username=username).first()

        if user_by_email:
            messages.error(
                request, f"User with this email exists already, try a different email!!")

        elif user_by_username:
            messages.error(
                request, f"User with this username exists already, try a different username!!")

            print(username, email, first_name, last_name)
        else:
            user = User.objects.create(
                first_name=first_name,
                last_name=last_name,
                username=username,
                email=email,
                role=role,
                gender=gender,
                phone_number=phone_number,
                id_number=id_number,
                position=position
            )
            user.set_password("1234")
            user.save()
            messages.success(request, f"User created successfully!!")

            return redirect('staff')

    return render(request, 'accounts/new_staff.html',)


@login_required(login_url="/users/login/")
def edit_staff(request):
    if request.method == 'POST':
        user_id = request.POST.get("user_id")
        if user_id:
            username = request.POST.get("username")
            email = request.POST.get("email")
            first_name = request.POST.get("first_name")
            last_name = request.POST.get("last_name")
            gender = request.POST.get("gender")
            role = request.POST.get("role")
            phone_number = request.POST.get("phone_number")
            id_number = request.POST.get("id_number")
            position = request.POST.get("position")

            user = User.objects.get(id=user_id)
            user.first_name = first_name if first_name else user.first_name
            user.last_name = last_name if last_name else user.last_name
            user.email = email if email else user.email
            user.gender = gender if gender else user.gender
            user.phone_number = phone_number if phone_number else user.phone_number
            user.id_number = id_number if id_number else user.id_number
            user.username = username if username else user.username
            user.role = role if role else user.role
            user.position = position
            user.save()
            messages.success(request, f"User created successfully!!")

        return redirect('staff')

    return render(request, 'accounts/edit_staff.html',)


@login_required(login_url="/users/login/")
def delete_staff(request):
    if request.method == "POST":
        user_id = request.POST.get("user_id")
        staff = User.objects.filter(id=user_id).first()
        if staff:
            staff.delete()
            return redirect("staff")
        else:
            return messages.error(request, f"Staff with id: {user_id} does not exist on the database")
    return render(request, "accounts/delete_staff.html")


def user_login(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            
            request.session["cashier_id"] = user.id

            login(request, user)
            return redirect('home')
    return render(request, 'accounts/login.html')


@login_required(login_url="/users/login/")
def user_logout(request):
    logout(request)
    return redirect('login')


@login_required(login_url="/users/login/")
def staff(request):
    staffs = User.objects.filter(role__in=["admin", "cashier", "agent", "broker"])

    if request.method == "POST":
        id_number = request.POST.get("id_number")
        staffs = User.objects.filter(id_number=id_number)

    paginator = Paginator(staffs, 10)
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)
    context = {
        "staffs": staffs,
        "page_obj": page_obj
    }
    return render(request, "accounts/staff.html", context)


def customers(request):
    customers = Customer.objects.all()

    paginator = Paginator(customers, 12)
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)

    context = {
        "page_obj": page_obj,
        "customers": customers
    }
    return render(request, "customers/customers.html", context)


def new_customer(request):
    if request.method == "POST":
        name = request.POST.get("name")
        email = request.POST.get("email")
        phone_number = request.POST.get("phone_number")
        id_number = request.POST.get("id_number")
        gender = request.POST.get("gender")
        address = request.POST.get("address")
        city = request.POST.get("city")
        country = request.POST.get("country")

        customer = Customer.objects.create(
            name=name,
            email=email,
            phone_number=phone_number,
            id_number=id_number,
            gender=gender,
            address=address,
            city=city,
            country=country
        )
        return redirect("customers")
        
    return render(request, "customers/new_customer.html")


def edit_customer(request):
    if request.method == "POST":
        customer_id = request.POST.get("customer_id")
        name = request.POST.get("name")
        email = request.POST.get("email")
        phone_number = request.POST.get("phone_number")
        id_number = request.POST.get("id_number")
        gender = request.POST.get("gender")
        address = request.POST.get("address")
        city = request.POST.get("city")
        country = request.POST.get("country")

        customer = Customer.objects.get(id=customer_id)
        customer.name = name
        customer.email = email
        customer.phone_number = phone_number
        customer.id_number = id_number
        customer.gender = gender
        customer.address = address
        customer.city = city
        customer.country = country
        customer.save()
        return redirect("customers")
    return render(request, "customers/edit_customer.html")


def delete_customer(request):
    if request.method == "POST":
        customer_id = request.POST.get("customer_id")
        customer = Customer.objects.get(id=customer_id)
        customer.delete()
        return redirect("customers")

    return render(request, "customers/delete_customer.html")