from django.db import transaction
from rest_framework import serializers
from apps.pos.models import Order, OrderItem
from apps.users.models import Customer
from apps.deliveries.models import Delivery, DeliveryStatusUpdate


class PlaceOrderSerializer(serializers.Serializer):
    order_items = serializers.JSONField()
    total_cost = serializers.DecimalField(max_digits=100, decimal_places=2)
    delivery_details = serializers.JSONField()

    @transaction.atomic
    def save(self, **kwargs):
        order_items = self.validated_data.get("order_items")
        total_cost = self.validated_data.get("total_cost")
        delivery_details = self.validated_data.get("delivery_details")
        user = self.context.get("user")
        print(user.email)

        customer = Customer.objects.get(user=user)

        order = Order.objects.create(
            order_source="Online",
            customer=customer,
            total_cost=total_cost,
            status="Pending",
            order_type="Online",
            payment_method="Online",
            served_by=user,
        )

        order_items_list = [
            OrderItem(
                order=order,
                user=user,
                item_id=x["id"],
                quantity=x["quantity"],
                price=x["cost"],
            )
            for x in order_items
        ]
        order_items = OrderItem.objects.bulk_create(order_items_list)
        for order_item in order_items:
            order_item.item.quantity -= order_item.quantity
            order_item.item.save()

        delivery = Delivery.objects.create(
            customer=customer,
            order=order,
            cost=delivery_details["delivery_cost"],
            delivery_status="Pending Dispatch",
            address_id=delivery_details["address"],
            delivery_type=delivery_details["delivery_type"],
        )

        DeliveryStatusUpdate.objects.create(
            delivery=delivery,
            previous_status="Initiated",
            next_status="Pending Dispatch",
        )

        return {}
