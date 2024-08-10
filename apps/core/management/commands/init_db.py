from typing import Any
from django.core.management.base import BaseCommand
from django.db import transaction
from apps.users.models import User, Customer
from apps.deliveries.models import DeliveryAddress

class Command(BaseCommand):
    def handle(self, *args: Any, **options: Any) -> str | None:
        self.create_walk_in_customer()
        self.create_walkin_delivery_address()
    
    def create_walk_in_customer(self):
        try:
            walkin_customer = User.objects.get(email="walkin@gmail.com")
            if walkin_customer:
                self.stdout.write(self.style.SUCCESS("Walkin Customer already exists!"))
            else:
                user = User.objects.create(
                    first_name="Walk In",
                    last_name="Customer",
                    email="walkin@gmail.com",
                    username="walkin@gmail.com",
                    role="Customer",
                    gender="Male",
                    phone_number="07123456789"
                )
                Customer.objects.create(
                    user=user,
                    name=f"{user.first_name} {user.last_name}",
                    address="0100",
                    city="Nairobi",
                    country="Kenya"
                )
                self.stdout.write(self.style.SUCCESS("Walkin Customer Successfully Created!!"))
        except Exception as e:
            raise e
        
    def create_walkin_delivery_address(self):
        try:
            user = User.objects.get(email="walkin@gmail.com")
            customer = Customer.objects.get(user=user)

            if customer:
                address = DeliveryAddress.objects.filter(customer=customer)
                if address:
                    self.stdout.write(self.style.SUCCESS("Address already exists!!"))
                else:
                    DeliveryAddress.objects.create(customer=customer)
                    self.stdout.write(self.style.SUCCESS("Address successfully created!!"))
            elif not customer:
                new_customer = self.create_walk_in_customer()
                DeliveryAddress.objects.create(customer=new_customer)
                self.stdout.write(self.style.SUCCESS("Address successfully created!!"))
        except Exception as e:
            raise e
