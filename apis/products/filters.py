from django_filters import rest_framework as filters
from apps.inventory.models import Inventory

class ProductFilter(filters.FilterSet):
    categories = filters.CharFilter(method='filter_by_categories')

    class Meta:
        model = Inventory
        fields = ['categories', 'name']

    def filter_by_categories(self, queryset, name, value):
        categories = value.split(',')
        return queryset.filter(category__name__in=categories)
