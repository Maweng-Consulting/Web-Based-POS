from django.contrib import admin

from .models import Inventory, InventoryLog, MpesaPayment

# Register your models here.
admin.site.register(MpesaPayment)
admin.site.register(Inventory)
admin.site.register(InventoryLog)