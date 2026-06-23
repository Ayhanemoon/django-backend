from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status

from shop.products.models import Coupon

from ..serializers import (
    CouponValidateSerializer
)

class CouponValidateAPIView(APIView):

    permission_classes = [IsAuthenticated]

    def post(self, request):

        serializer = CouponValidateSerializer(
            data=request.data
        )

        serializer.is_valid(
            raise_exception=True
        )

        code = serializer.validated_data["code"]
        amount = serializer.validated_data["amount"]

        try:
            coupon = Coupon.objects.get(
                code=code
            )
        except Coupon.DoesNotExist:
            return Response(
                {
                    "valid": False,
                    "detail": "Invalid coupon."
                },
                status=status.HTTP_400_BAD_REQUEST,
            )

        if not coupon.is_valid():
            return Response(
                {
                    "valid": False,
                    "detail": "Coupon is not valid."
                },
                status=status.HTTP_400_BAD_REQUEST,
            )

        if amount < coupon.min_order_amount:
            return Response(
                {
                    "valid": False,
                    "detail": (
                        f"Minimum order amount is "
                        f"{coupon.min_order_amount}"
                    ),
                },
                status=status.HTTP_400_BAD_REQUEST,
            )

        discount_amount = coupon.calculate_discount(
            amount
        )

        return Response(
            {
                "valid": True,
                "code": coupon.code,
                "discount_type": coupon.discount_type,
                "value": coupon.value,
                "discount_amount": discount_amount,
                "final_amount": amount - discount_amount,
            }
        )
    
