from rest_framework import serializers
from accounts.models.addresses import Address


class AddressSerializer(serializers.ModelSerializer):
    full_name = serializers.CharField(source="profile.fullname", read_only=True)

    class Meta:
        model = Address
        fields = [
            "id",
            "title",
            "full_name",
            "receiver_name",
            "phone_number",
            "country",
            "state",
            "city",
            "postal_code",
            "address_line_1",
            "address_line_2",
            "is_default",
            "created_at",
            "updated_at",
        ]
        read_only_fields = ["id", "created_at", "updated_at"]
