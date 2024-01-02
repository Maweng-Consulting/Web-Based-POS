from django.contrib import admin

from .models import Order, OrderItem, TemporaryCustomerCartItem


# Register your models here.
@admin.register(TemporaryCustomerCartItem)
class TemporaryCustomerCartItemAdmin(admin.ModelAdmin):
    list_display = ["user", "cashier_id", "item", "quantity", "price"]


admin.site.register(Order)
admin.site.register(OrderItem)
