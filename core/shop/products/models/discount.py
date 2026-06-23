from django.db import models
from django.utils import timezone


class Coupon(models.Model):

    class DiscountType(models.TextChoices):
        PERCENT = "percent", "Percent"
        FIXED = "fixed", "Fixed"

    code = models.CharField(
        max_length=50,
        unique=True,
    )

    discount_type = models.CharField(
        max_length=20,
        choices=DiscountType.choices,
    )

    value = models.PositiveIntegerField()

    is_active = models.BooleanField(default=True)

    max_usage = models.PositiveIntegerField(
        null=True,
        blank=True,
    )

    used_count = models.PositiveIntegerField(default=0)

    min_order_amount = models.PositiveIntegerField(default=0)

    expires_at = models.DateTimeField(
        null=True,
        blank=True,
    )

    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-created_at"]
        indexes = [
            models.Index(fields=["code"]),
            models.Index(fields=["is_active"]),
            models.Index(fields=["expires_at"]),
        ]

    def is_valid(self):

        if not self.is_active:
            return False

        if (
            self.expires_at
            and self.expires_at < timezone.now()
        ):
            return False

        if (
            self.max_usage is not None
            and self.used_count >= self.max_usage
        ):
            return False

        return True

    def calculate_discount(self, amount):

        if self.discount_type == self.DiscountType.PERCENT:
            discount = amount * self.value // 100
        else:
            discount = self.value

        return min(discount, amount)

    def apply_discount(self, amount):

        return amount - self.calculate_discount(amount)

    def __str__(self):
        return self.code
    
class CouponUsage(models.Model):

    coupon = models.ForeignKey(
        Coupon,
        on_delete=models.CASCADE,
        related_name="usages",
    )

    profile = models.ForeignKey(
        "accounts.Profile",
        on_delete=models.CASCADE,
        related_name="coupon_usages",
    )

    order = models.ForeignKey(
        "orders.Order",
        on_delete=models.CASCADE,
        related_name="coupon_usages",
    )

    created_at = models.DateTimeField(
        auto_now_add=True,
    )

    class Meta:
        unique_together = [
            ("coupon", "order"),
        ]