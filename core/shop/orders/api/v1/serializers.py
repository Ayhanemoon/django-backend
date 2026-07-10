from rest_framework import serializers
from shop.orders.services import CheckoutService
from shop.orders.models import Order, OrderItem


class OrderSerializer(serializers.ModelSerializer):
    class Meta:
        model = Order
        fields = [
            "id",
            "profile",
            "address_snapshot",
            "status",
            "total_amount",
            "created_at",
            "updated_at",
        ]
        read_only_fields = fields

class OrderItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = OrderItem
        fields = [
            "id",
            "product_id",
            "product_title",
            "unit_price",
            "quantity",
            "line_total",
            "created_at",
        ]
        read_only_fields = fields


class OrderDetailSerializer(serializers.ModelSerializer):
    items = OrderItemSerializer(many=True, read_only=True)

    class Meta:
        model = Order
        fields = [
            "id",
            "status",
            "total_amount",
            "address_snapshot",
            "items",
            "created_at",
            "updated_at",
        ]
        read_only_fields = fields

class CheckoutSerializer(serializers.Serializer):
    address_id = serializers.IntegerField()
    idempotency_key = serializers.CharField(required=True)
    coupon_code = serializers.CharField(required=False, allow_blank=True)

    def create(self, validated_data):
        request = self.context["request"]

        return CheckoutService.checkout(
                profile=request.user.profile,
                **validated_data,
        )