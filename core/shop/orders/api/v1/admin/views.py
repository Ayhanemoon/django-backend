from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.permissions import IsAdminUser
from rest_framework.response import Response

from shop.orders.api.v1.serializers import OrderSerializer
from shop.orders.models import Order
   
class AdminOrderViewSet(viewsets.ReadOnlyModelViewSet):
    """
    Admin order management:
    - ship orders
    - deliver orders
    """

    queryset = Order.objects.all()
    serializer_class = OrderSerializer
    permission_classes = [IsAdminUser]

    @action(detail=True, methods=["post"])
    def ship(self, request, pk=None):
        order = self.get_object()
        order.mark_shipped()

        return Response({
            "detail": "Order shipped.",
            "status": order.status,
        })
    
    @action(detail=True, methods=["post"])
    def deliver(self, request, pk=None):
        order = self.get_object()
        order.mark_delivered()

        return Response({
            "detail": "Order delivered.",
            "status": order.status,
        })