from rest_framework import serializers


class SessionCreateSerializer(serializers.Serializer):
    customer_id = serializers.IntegerField()
