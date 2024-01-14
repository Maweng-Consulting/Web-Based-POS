from django.contrib import admin

from .models import CreditOrder, Order, OrderItem, TemporaryCustomerCartItem


# Register your models here.
@admin.register(TemporaryCustomerCartItem)
class TemporaryCustomerCartItemAdmin(admin.ModelAdmin):
    list_display = ["user", "cashier_id", "item", "quantity", "price"]


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ["id", "order_date", "order_time", "served_by", "total_cost", "status", "order_type", "payment_method"]

@admin.register(OrderItem)
class OrderItemAdmin(admin.ModelAdmin):
    list_display = ["id", "created", "order", "item", "quantity", "price"]


@admin.register(CreditOrder)
class CreditOrderAdmin(admin.ModelAdmin):
    list_display = ["customer", "order", "due_date"]