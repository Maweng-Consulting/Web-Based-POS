from django.contrib import admin
from apps.core.models import MeasureUnit


# Register your models here.
@admin.register(MeasureUnit)
class MeasureUnitAdmin(admin.ModelAdmin):
    list_display = ["id", "title"]
