from rest_framework import serializers
from apps.pos.models import Order, OrderItem


class PlaceOrderSerializer(serializers.Serializer):
    items = serializers.JSONField(default=list)
    total_cost = serializers.DecimalField(max_digits=100, decimal_places=2)

    def save(self, **kwargs):
        items = self.validated_data.get("items")
        total_cost = self.validated_data.get("total_cost")
        user = self.context.get("user")
        print(user.email)
        order_items = []

        for item in items:
            print(item)
        return {}
