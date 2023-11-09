from django.contrib import admin

from .models import Order, OrderItem, TemporaryCustomerCartItem

# Register your models here.
admin.site.register(TemporaryCustomerCartItem)
