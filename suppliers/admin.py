from django.contrib import admin

from suppliers.models import SupplyLog


# Register your models here.
@admin.register(SupplyLog)
class SupplyLogAdmin(admin.ModelAdmin):
    list_display = ["supplier", "item", "quantity", "unit_price", "supply_cost", "recorded_by"]