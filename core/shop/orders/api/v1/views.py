from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from shop.orders.models import Order
from .serializers import OrderSerializer, OrderCreateSerializer, OrderDetailSerializer,CheckoutSerializer


class OrderViewSet(viewsets.ModelViewSet):
    """
    Order API.
    Users can list and create their own orders.
    Orders are immutable after creation (no update/delete by user).
    """

    permission_classes = [IsAuthenticated]

    def get_serializer_class(self):
        """Return appropriate serializer class based on action."""
        if self.action == "create":
            return OrderCreateSerializer
        if self.action == "retrieve":
            return OrderDetailSerializer
        return OrderSerializer

    def get_queryset(self):
        """Retrieve orders for the authenticated user's profile."""
        return Order.objects.filter(profile=self.request.user.profile)

    def create(self, request, *args, **kwargs):
        """Create a new order with an address snapshot."""
        serializer = OrderCreateSerializer(
            data=request.data,
            context={"request": request},
        )
        serializer.is_valid(raise_exception=True)

        order = serializer.save()

        output = OrderSerializer(order, context={"request": request})
        return Response(output.data, status=status.HTTP_201_CREATED)

    # Disable updates and deletes for users
    def update(self, request, *args, **kwargs):
        return Response(
            {"detail": "Orders cannot be updated."}, status=status.HTTP_403_FORBIDDEN
        )

    def partial_update(self, request, *args, **kwargs):
        return Response(
            {"detail": "Orders cannot be updated."}, status=status.HTTP_403_FORBIDDEN
        )

    def destroy(self, request, *args, **kwargs):
        return Response(
            {"detail": "Orders cannot be deleted."}, status=status.HTTP_403_FORBIDDEN
        )
    
    @action(detail=True, methods=["post"])
    def cancel(self, request, pk=None):
        order = self.get_object()

        if order.status in ["paid", "cancelled"]:
            return Response(
                {"detail": "Order cannot be cancelled."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        order.cancel()

        return Response({"detail": "Order cancelled."})

    @action(detail=False, methods=["post"])
    def checkout(self, request):

        serializer = CheckoutSerializer(
            data=request.data,
            context={"request": request},
        )

        serializer.is_valid(raise_exception=True)

        order = serializer.save()

        return Response(
            OrderSerializer(order).data,
            status=status.HTTP_201_CREATED,
        )