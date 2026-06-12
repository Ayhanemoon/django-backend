from rest_framework import status, viewsets
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from shop.orders.models import Order
from .serializers import (
    OrderSerializer,
    OrderDetailSerializer,
    CheckoutSerializer,
)


class OrderViewSet(viewsets.ReadOnlyModelViewSet):
    """
    Users can:
    - List their orders
    - Retrieve order details
    - Checkout (create order from cart)
    - Cancel eligible orders

    Orders cannot be directly created, updated, or deleted.
    """

    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Order.objects.filter(
            profile=self.request.user.profile
        )

    def get_serializer_class(self):
        if self.action == "retrieve":
            return OrderDetailSerializer

        if self.action == "checkout":
            return CheckoutSerializer

        return OrderSerializer

    @action(detail=False, methods=["post"])
    def checkout(self, request):
        serializer = CheckoutSerializer(
            data=request.data,
            context={"request": request},
        )
        serializer.is_valid(raise_exception=True)

        order = serializer.save()

        return Response(
            OrderDetailSerializer(order).data,
            status=status.HTTP_201_CREATED,
        )

    @action(detail=True, methods=["post"])
    def cancel(self, request, pk=None):
        order = self.get_object()

        if order.status in [
            Order.OrderStatus.PAID,
            Order.OrderStatus.CANCELLED,
        ]:
            return Response(
                {"detail": "Order cannot be cancelled."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        order.cancel()

        return Response(
            {"detail": "Order cancelled."},
            status=status.HTTP_200_OK,
        )
    