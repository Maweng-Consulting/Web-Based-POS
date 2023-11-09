from rest_framework import serializers

from inventory.models import Inventory, MpesaPayment


class InventorySerializer(serializers.ModelSerializer):
    button = serializers.SerializerMethodField()
    class Meta:
        model = Inventory
        fields = "__all__"

    def get_button(self, obj):
        return f'<a href="/add-to-cart/{obj.id}" class="btn btn-primary btn-sm"><i class="bi bi-cart-plus"></i></a>'


class MpesaPaymentSerializer(serializers.ModelSerializer):
    button = serializers.SerializerMethodField()
    class Meta:
        model = MpesaPayment
        fields = "__all__"

    def get_button(self, obj):
        return f'<a href="/add-to-cart/{obj.id}" class="btn btn-primary btn-sm">Pay</a>'