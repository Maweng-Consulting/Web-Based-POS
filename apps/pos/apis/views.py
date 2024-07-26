from rest_framework import generics, status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from apps.pos.apis.serializers import SessionCreateSerializer, CustomerOrderPaidSerializer
from apps.users.models import Customer
from apps.pos.models import Order, TemporaryCustomerCartItem


class SessionCreateAPIView(generics.CreateAPIView):
    serializer_class = SessionCreateSerializer
    permission_classes = [IsAuthenticated]

    def post(self, request, *args, **kwargs):
        data = request.data

        cashier_id = request.current_cashier

        serializer = self.serializer_class(data=data)

        if serializer.is_valid(raise_exception=True):
            customer_id = serializer.validated_data["customer_id"]
            customer = Customer.objects.get(id=customer_id)
            
            request.session[f"selected_customer_{cashier_id}"] = {
                "id": customer.id,
                "name": customer.name,
                "cashier_id": cashier_id,
                "is_walkin": customer.is_walk_in,
            }

            selected_customer = request.session.get(
                f"selected_customer_{cashier_id}", {}
            )

            print(f"User With Cashier: {selected_customer}")

            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class CustomerOrderPaidAPIView(generics.CreateAPIView):
    serializer_class = CustomerOrderPaidSerializer

    def post(self, request, *args, **kwargs):
        data = request.data
        serializer = self.serializer_class(data=data)
        if serializer.is_valid(raise_exception=True):
            customer_id = data["customer_id"]
            order_id = data["order_id"]
            cashier_id = data["cashier_id"]

            order = Order.objects.get(id=order_id)
            items = TemporaryCustomerCartItem.objects.filter(
                order=order,
                cashier_id=cashier_id,
                customer_id=customer_id
            )

            items.delete()
            del request.session[f"selected_customer_{cashier_id}"]
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)