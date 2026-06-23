from django.db import models, transaction

from shop.orders.models import Order
from shop.products.models import Coupon, CouponUsage


class Payment(models.Model):

    class Status(models.TextChoices):
        PENDING = "pending", "Pending"
        SUCCESS = "success", "Success"
        FAILED = "failed", "Failed"

    order = models.OneToOneField(
        Order,
        on_delete=models.CASCADE,
        related_name="payment",
    )

    amount = models.PositiveIntegerField()

    status = models.CharField(
        max_length=20,
        choices=Status.choices,
        default=Status.PENDING,
    )

    provider = models.CharField(
        max_length=50,
        default="manual",
    )

    transaction_id = models.CharField(
        max_length=255,
        blank=True,
        null=True,
    )

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    @transaction.atomic
    def mark_success(self):

        if self.status != self.Status.PENDING:
            return

        with transaction.atomic():

            self.status = self.Status.SUCCESS
            self.save(update_fields=["status"])

            self.order.mark_paid()

            if self.order.coupon_code:

                coupon = Coupon.objects.get(
                    code=self.order.coupon_code
                )

                coupon.used_count += 1
                coupon.save(
                    update_fields=["used_count"]
                )

                CouponUsage.objects.create(
                    coupon=coupon,
                    profile=self.order.profile,
                    order=self.order,
                )

    @transaction.atomic
    def mark_failed(self):
        if self.status != self.Status.PENDING:
            return

        self.status = self.Status.FAILED
        self.save(update_fields=["status"])

        self.order.cancel()