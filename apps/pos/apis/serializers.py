from rest_framework import serializers


class SessionCreateSerializer(serializers.Serializer):
    customer_id = serializers.IntegerField()


class CustomerOrderPaidSerializer(serializers.Serializer):
    customer_id = serializers.IntegerField()
    cashier_id = serializers.IntegerField()
    order_id = serializers.IntegerField()
