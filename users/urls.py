from django.urls import path

from users.views import (customers, delete_customer, delete_staff,
                         edit_customer, edit_staff, new_customer, register,
                         staff, user_login, user_logout)

urlpatterns = [
    path("login/", user_login, name="login"),
    path("register/", register, name="register"),
    path("logout/", user_logout, name="logout"),
    path("staff/", staff, name="staff"),
    path("edit-staff/", edit_staff, name="edit-staff"),
    path("delete-staff/", delete_staff, name="delete-staff"),

    path("customers/", customers, name="customers"),
    path("new-customer/", new_customer, name="new-customer"),
    path("edit-customer/", edit_customer, name="edit-customer"),
    path("delete-customer/", delete_customer, name="delete-customer"),
]