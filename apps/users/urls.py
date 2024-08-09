from django.urls import path

from apps.users.views import (
    create_customer_at_pos,
    customers,
    delete_customer,
    delete_staff,
    edit_customer,
    edit_staff,
    new_customer,
    new_staff,
    register,
    staff,
    user_login,
    user_logout,
    people_home,
)

urlpatterns = [
    path("", people_home, name="people"),
    path("login/", user_login, name="login"),
    path("register/", register, name="register"),
    path("new-staff/", new_staff, name="new-staff"),
    path("logout/", user_logout, name="logout"),
    path("staff/", staff, name="staff"),
    path("edit-staff/", edit_staff, name="edit-staff"),
    path("delete-staff/", delete_staff, name="delete-staff"),
    path("customers/", customers, name="customers"),
    path("new-customer/", new_customer, name="new-customer"),
    path("edit-customer/", edit_customer, name="edit-customer"),
    path("delete-customer/", delete_customer, name="delete-customer"),
    path("new-customer-at-pos/", create_customer_at_pos, name="new-customer-at-pos"),
]
