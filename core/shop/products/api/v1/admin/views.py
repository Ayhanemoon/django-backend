from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAdminUser
from shop.products.models import Inventory, InventoryMovement, Coupon, CouponUsage
from shop.products.api.v1.serializers import (
    InventorySerializer,
    InventoryMovementSerializer,
    RestockSerializer,
    CouponSerializer,
    CouponUsageSerializer
)
   
class AdminInventoryViewSet(viewsets.ReadOnlyModelViewSet):

    queryset = Inventory.objects.select_related(
        "product"
    )

    serializer_class = InventorySerializer
    permission_classes = [IsAdminUser]

    @action(
        detail=True,
        methods=["post"],
    )
    def restock(self, request, pk=None):

        inventory = self.get_object()

        serializer = RestockSerializer(
            data=request.data
        )

        serializer.is_valid(
            raise_exception=True
        )

        inventory.restock(
            quantity=serializer.validated_data["quantity"],
            note=serializer.validated_data.get("note"),
        )

        return Response(
            InventorySerializer(inventory).data
        )
    
    @action(
        detail=True,
        methods=["get"],
    )
    def movements(self, request, pk=None):

        inventory = self.get_object()

        queryset = InventoryMovement.objects.filter(
            product=inventory.product
        )

        serializer = InventoryMovementSerializer(
            queryset,
            many=True,
        )

        return Response(serializer.data)
    
class AdminCouponViewSet(viewsets.ModelViewSet):

    queryset = Coupon.objects.all()

    serializer_class = CouponSerializer

    permission_classes = [IsAdminUser]

    @action(
        detail=True,
        methods=["get"],
    )
    def usages(self, request, pk=None):

        coupon = self.get_object()

        queryset = CouponUsage.objects.filter(
            coupon=coupon
        ).select_related(
            "profile",
            "order",
        )

        serializer = CouponUsageSerializer(
            queryset,
            many=True,
        )

        return Response(serializer.data)