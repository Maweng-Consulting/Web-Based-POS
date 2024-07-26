from rest_framework import serializers
from apps.inventory.models import Inventory, ProductImage

class ProductImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductImage
        fields = "__all__"

class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Inventory
        fields = "__all__"
