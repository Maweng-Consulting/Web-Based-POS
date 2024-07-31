from django.contrib.auth.models import AbstractUser
from django.db import models
from django.urls import reverse
from django.utils.translation import gettext_lazy as _

from apps.core.models import AbstractBaseModel

# Create your models here.
ROLE_CHOICES = (
    ("admin", "Admin"),
    ("cashier", "Cashier"),
    ("agent", "Agent"),
    ("broker", "Broker"),
    ("Supplier", "Supplier"),
)


class User(AbstractUser, AbstractBaseModel):
    role = models.CharField(choices=ROLE_CHOICES, max_length=32)
    phone_number = models.CharField(max_length=255)
    id_number = models.CharField(max_length=255, null=True)
    gender = models.CharField(max_length=255)
    position = models.CharField(max_length=255, null=True)

    def __str__(self):
        if self.first_name and self.last_name:
            return f"{self.first_name} {self.last_name}"
        else:
            return self.username

    def name(self):
        if not self.first_name and self.last_name:
            return self.username
        else:
            return f"{self.first_name} {self.last_name}"


class Customer(AbstractBaseModel):
    user = models.OneToOneField(User, on_delete=models.SET_NULL, null=True)
    address = models.CharField(max_length=255, null=True)
    city = models.CharField(max_length=255, null=True)
    country = models.CharField(max_length=255, null=True)

    def __str__(self):
        return self.name

    @property
    def is_walk_in(self):
        return True if self.name in ["Walk In Customer", "Walk-In Customer"] else False
