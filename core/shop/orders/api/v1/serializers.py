from django.db import transaction
from rest_framework import serializers
from shop.orders.models import Order, OrderItem, CheckoutRequestLog
from accounts.models import Address
from shop.products.models import Inventory
from shop.cart.models import Cart


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

"""
class OrderCreateSerializer(serializers.Serializer):
    address_id = serializers.IntegerField()
    items = serializers.ListField(
        child=serializers.DictField(),
        allow_empty=False,
    )

    def validate_items(self, items):
        for item in items:
            if "product_id" not in item or "quantity" not in item:
                raise serializers.ValidationError(
                    "Each item must include product_id and quantity"
                )
            if item["quantity"] <= 0:
                raise serializers.ValidationError("Quantity must be greater than zero")
        return items

    @transaction.atomic
    def create(self, validated_data):
        request = self.context["request"]
        profile = request.user.profile

        # 1. Load and validate address
        address = Address.objects.alive().get(
            id=validated_data["address_id"],
            profile=profile,
        )

        # 2. Snapshot address
        address_snapshot = {
            "receiver_name": address.receiver_name,
            "phone_number": address.phone_number,
            "country": address.country,
            "state": address.state,
            "city": address.city,
            "postal_code": address.postal_code,
            "address_line_1": address.address_line_1,
            "address_line_2": address.address_line_2,
        }

        # 3. Create order shell
        order = Order.objects.create(
            profile=profile,
            address_snapshot=address_snapshot,
            total_amount=0,
        )

        total = 0

        # 4. Create order items
        for item in validated_data["items"]:
            product = Product.objects.get(
                id=item["product_id"],
                status=Product.ProductStatus.ACTIVE,
            )

            inventory = Inventory.objects.select_for_update().get(
                product=product
            )

            quantity = item["quantity"]

            # 1. Validate stock
            if inventory.available_stock() < quantity:
                raise serializers.ValidationError(
                    f"Not enough stock for {product.title}"
                )

            # 2. Reserve stock immediately
            inventory.reserved += quantity
            inventory.save(update_fields=["reserved"])

            # 3. Create order item snapshot
            order_item = OrderItem.objects.create(
                order=order,
                product_id=product.id,
                product_title=product.title,
                unit_price=product.price,
                quantity=item["quantity"],
            )

            total += order_item.line_total

        # 5. Finalize total
        order.total_amount = total
        order.save(update_fields=["total_amount"])

        return order
"""

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

    @transaction.atomic
    def create(self, validated_data):
        request = self.context["request"]
        profile = request.user.profile

        # ----------------------------
        # 1. Idempotency protection
        # ----------------------------
        key = validated_data["idempotency_key"]

        if CheckoutRequestLog.objects.filter(key=key, profile=profile).exists():
            raise serializers.ValidationError("Duplicate checkout request.")

        # ----------------------------
        # 2. Lock cart
        # ----------------------------
        cart = (
            Cart.objects
            .select_for_update()
            .prefetch_related("items__product")
            .get(profile=profile)
        )

        items = list(cart.items.select_related("product"))

        if not items:
            raise serializers.ValidationError("Cart is empty.")

        # ----------------------------
        # 3. Validate address
        # ----------------------------
        address = Address.objects.alive().get(
            id=validated_data["address_id"],
            profile=profile,
        )

        # ----------------------------
        # 4. Lock + validate inventory first
        # ----------------------------
        for item in items:
            inventory = Inventory.objects.select_for_update().get(
                product=item.product
            )

            if inventory.available_stock() < item.quantity:
                raise serializers.ValidationError(
                    f"Not enough stock for {item.product.title}"
                )

        # ----------------------------
        # 5. Create order snapshot
        # ----------------------------
        snapshot = {
            "receiver_name": address.receiver_name,
            "phone_number": address.phone_number,
            "country": address.country,
            "state": address.state,
            "city": address.city,
            "postal_code": address.postal_code,
            "address_line_1": address.address_line_1,
            "address_line_2": address.address_line_2,
        }

        order = Order.objects.create(
            profile=profile,
            address_snapshot=snapshot,
            total_amount=0,
        )

        # ----------------------------
        # 6. Reserve inventory + create items
        # ----------------------------
        total = 0

        for item in items:
            inventory = Inventory.objects.select_for_update().get(
                product=item.product
            )

            inventory.reserve(
                quantity=item.quantity,
                order_id=order.id,
            )

            order_item = OrderItem.objects.create(
                order=order,
                product_id=item.product.id,
                product_title=item.product.title,
                unit_price=item.product.price,
                quantity=item.quantity,
            )

            total += order_item.line_total

        # ----------------------------
        # 7. Finalize order total
        # ----------------------------
        order.total_amount = total
        order.save(update_fields=["total_amount"])

        # ----------------------------
        # 8. Clear cart
        # ----------------------------
        cart.items.all().delete()

        # ----------------------------
        # 9. Store idempotency key
        # ----------------------------
        CheckoutRequestLog.objects.create(
            key=key,
            profile=profile
        )

        return order