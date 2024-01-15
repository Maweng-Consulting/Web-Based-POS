from django.contrib import admin

from users.models import Customer, User


# Register your models here.
@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ["id", "email", "username", "name", "position", "role"]


@admin.register(Customer)
class CustomerAdmin(admin.ModelAdmin):
    list_display = ["id", "name", "phone_number", "id_number", "gender"]