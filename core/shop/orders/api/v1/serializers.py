from rest_framework import serializers
from ...models import Order


class OrderSerializer(serializers.ModelSerializer):
    class Meta:
        model = Order
        fields = ["id", "profile", "created_at", "updated_at"]
        read_only_fields = ["id", "created_at", "updated_at", "profile"]

    def create(self, validated_data):
        # Assign the logged-in user's profile
        validated_data["profile"] = self.context["request"].user.profile
        return super().create(validated_data)
