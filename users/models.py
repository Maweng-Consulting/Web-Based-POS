from django.contrib.auth.models import AbstractUser
from django.db import models
from django.urls import reverse
from django.utils.translation import gettext_lazy as _

# Create your models here.
ROLE_CHOICES = (
    ("admin", "Admin"),
    ("cashier", "Cashier"),
    ("agent", "Agent"),
    ("broker", "Broker"),
    ("Supplier", "Supplier"),
)

class User(AbstractUser):
    role = models.CharField(choices=ROLE_CHOICES, max_length=32, null=True)
    phone_number = models.CharField(max_length=255, null=True)
    id_number = models.CharField(max_length=255, null=True)
    gender = models.CharField(max_length=255, null=True)

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