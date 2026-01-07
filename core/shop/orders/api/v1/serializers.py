from rest_framework import serializers
from shop.orders.models import Order
from accounts.models import Address


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


class OrderCreateSerializer(serializers.Serializer):
    address_id = serializers.IntegerField()

    def create(self, validated_data):
        request = self.context["request"]
        profile = request.user.profile

        address = Address.objects.alive().get(
            id=validated_data["address_id"],
            profile=profile,
        )

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

        return Order.objects.create(
            profile=profile,
            address_snapshot=snapshot,
            total_amount=0,
        )
