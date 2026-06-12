from rest_framework import serializers
from shop.payments.models import Payment


class PaymentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Payment
        fields = [
            "id",
            "order",
            "amount",
            "status",
            "provider",
            "transaction_id",
            "created_at",
        ]
        read_only_fields = fields