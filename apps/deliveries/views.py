from django.shortcuts import render, redirect
from django.core.paginator import Paginator
from django.db.models import Q
from apps.deliveries.models import (
    Delivery,
    DeliveryAddress,
    DeliveryPartner,
    PickupStation,
    DeliveryStatusUpdate,
    DeliveryDriver,
)
from apps.pos.models import Order

DELIVERY_STATUS_CHOICES = [
    "Delivered" "Transit",
    "Pending Dispatch",
    "Initiated",
    "Dispatched",
    "Abandoned",
]
DELIVERY_TYPE_CHOICES = ["Self Pickup", "Door Delivery", "Pickup Station"]


# Create your views here.
def home(request):
    stations_count = PickupStation.objects.count()
    partners_count = DeliveryPartner.objects.count()
    deliveries_count = Delivery.objects.count()
    drivers_count = DeliveryDriver.objects.count()
    addresses_count = DeliveryAddress.objects.count()

    context = {
        "stations_count": stations_count,
        "deliveries_count": deliveries_count,
        "partners_count": partners_count,
        "drivers_count": drivers_count,
        "addresses_count": addresses_count,
    }

    return render(request, "deliveries/home.html", context)


def delivery_partners(request):
    partners = DeliveryPartner.objects.all().order_by("-created")
    if request.method == "POST":
        search_text = request.POST.get("search_text")
        partners = DeliveryPartner.objects.filter(Q(name__icontains=search_text))

    paginator = Paginator(partners, 10)
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)

    context = {"page_obj": page_obj}
    return render(request, "deliveries/partners/partners.html", context)


def new_delivery_partner(request):
    if request.method == "POST":
        name = request.POST.get("name")
        town = request.POST.get("town")
        country = request.POST.get("country")
        email = request.POST.get("email")
        phone_number = request.POST.get("phone_number")

        DeliveryPartner.objects.create(
            name=name,
            town=town,
            country=country,
            email=email,
            phone_number=phone_number,
        )
        return redirect("delivery-partners")
    return render(request, "deliveries/partners/new_partner.html")


def pickup_stations(request):
    stations = PickupStation.objects.all().order_by("-created")

    if request.method == "POST":
        search_text = request.POST.get("search_text")
        stations = PickupStation.objects.filter(
            Q(name__icontains=search_text)
            | Q(town__icontains=search_text)
            | Q(phone_number__icontains=search_text)
        )

    paginator = Paginator(stations, 10)
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)

    context = {"page_obj": page_obj}
    return render(request, "deliveries/stations/stations.html", context)


def new_pickup_station(request):
    if request.method == "POST":
        name = request.POST.get("name")
        town = request.POST.get("town")
        country = request.POST.get("country")
        county = request.POST.get("county")
        description = request.POST.get("description")
        phone_number = request.POST.get("phone_number")

        PickupStation.objects.create(
            name=name,
            town=town,
            county=county,
            country=country,
            description=description,
            phone_number=phone_number,
        )

        return redirect("pickup-stations")
    return render(request, "deliveries/stations/new_station.html")


def deliveries(request):
    deliveries = Delivery.objects.all().order_by("-created")

    delivery_partners = DeliveryPartner.objects.all().order_by("-id")
    delivery_addresses = DeliveryAddress.objects.all().order_by("-id")
    drivers = DeliveryDriver.objects.all().order_by("-id")

    if request.method == "POST":
        search_text = request.POST.get("search_text")
        deliveries = Delivery.objects.filter(
            Q(customer__first_name__icontains=search_text)
            | Q(town__icontains=search_text)
            | Q(customer__phone_number__icontains=search_text)
            | Q(customer__last_name__icontains=search_text)
        )

    paginator = Paginator(deliveries, 10)
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)

    context = {
        "page_obj": page_obj,
        "delivery_statuses": DELIVERY_STATUS_CHOICES,
        "delivery_types": DELIVERY_TYPE_CHOICES,
        "delivery_partners": delivery_partners,
        "delivery_addresses": delivery_addresses,
        "drivers": drivers
    }
    return render(request, "deliveries/deliveries.html", context)


def new_delivery(request):
    if request.method == "POST":
        order_id = request.POST.get("order")
        cost = request.POST.get("cost")
        delivery_type = request.POST.get("delivery_type")
        order = Order.objects.get(id=order_id)

        delivery = Delivery.objects.create(
            customer=order.customer.user,
            order=order,
            cost=cost,
            delivery_type=delivery_type,
        )

        DeliveryStatusUpdate.objects.create(
            delivery=delivery,
            previous_status="Initiated",
            next_status="Pending Dispatch",
        )

        return redirect("deliveries")
    return render(request, "deliveries/new_delivery.html")


def edit_delivery(request):
    if request.method == "POST":
        order_id = request.POST.get("order")
        cost = request.POST.get("cost")
        delivery_type = request.POST.get("delivery_type")

    return render(request, "deliveries/edit_delivery.html")
