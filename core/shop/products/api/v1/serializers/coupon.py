from rest_framework import serializers
from shop.products.models import Coupon, CouponUsage


class CouponSerializer(serializers.ModelSerializer):

    class Meta:
        model = Coupon
        fields = "__all__"


class CouponUsageSerializer(serializers.ModelSerializer):

    class Meta:
        model = CouponUsage
        fields = [
            "id",
            "profile",
            "order",
            "created_at",
        ]

class CouponValidateSerializer(serializers.Serializer):
    code = serializers.CharField()
    amount = serializers.IntegerField(min_value=0)