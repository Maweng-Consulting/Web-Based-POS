from django.urls import path

from users.views import (delete_staff, edit_staff, register, staff,
                              user_login, user_logout)

urlpatterns = [
    path("login/", user_login, name="login"),
    path("register/", register, name="register"),
    path("logout/", user_logout, name="logout"),
    path("staff/", staff, name="staff"),
    path("edit-staff/", edit_staff, name="edit-staff"),
    path("delete-staff/", delete_staff, name="delete-staff"),
]