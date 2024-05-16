from rest_framework import serializers
from apps.inventory.models import Inventory, ProductImage

class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Inventory
        fields = "__all__"


class ProductImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductImage
        fields = "__all__"