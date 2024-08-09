from django.urls import path
from apps.deliveries.views import (
    home,
    delivery_partners,
    new_delivery_partner,
    pickup_stations,
    new_pickup_station,
    deliveries,
    new_delivery,
)

urlpatterns = [
    path("deliveries-home/", home, name="deliveries-home"),
    path("", deliveries, name="deliveries"),
    path("new-delivery/", new_delivery, name="new-delivery"),
    path("delivery-partners/", delivery_partners, name="delivery-partners"),
    path("new-delivery-partner/", new_delivery_partner, name="new-delivery-partner"),
    path("pickup-stations/", pickup_stations, name="pickup-stations"),
    path("new-pickup-station/", new_pickup_station, name="new-pickup-station"),
]
