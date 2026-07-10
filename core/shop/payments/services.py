from django.db import transaction

from shop.notifications.services import NotificationService
from shop.products.models import Coupon, CouponUsage, Inventory
from shop.payments.models import Payment


class PaymentService:

    @staticmethod
    @transaction.atomic
    def mark_success(payment: Payment):

        if payment.status != Payment.Status.PENDING:
            return payment

        payment.status = Payment.Status.SUCCESS
        payment.save(
            update_fields=["status"]
        )

        order = payment.order

        # finalize order
        order.mark_paid()

        # consume coupon after successful payment
        if order.coupon_code:

            coupon = Coupon.objects.select_for_update().get(
                code=order.coupon_code
            )

            coupon.used_count += 1
            coupon.save(
                update_fields=[
                    "used_count"
                ]
            )

            CouponUsage.objects.create(
                coupon=coupon,
                profile=order.profile,
                order=order,
            )

        NotificationService.payment_success(
            order
        )

        return payment
    
    @staticmethod
    @transaction.atomic
    def mark_failed(payment: Payment):

        if payment.status != Payment.Status.PENDING:
            return payment

        payment.status = Payment.Status.FAILED
        payment.save(
            update_fields=["status"]
        )

        payment.order.cancel()

        return payment