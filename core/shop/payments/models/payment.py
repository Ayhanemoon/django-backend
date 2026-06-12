from django.db import models, transaction

from shop.orders.models import Order


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

        self.status = self.Status.SUCCESS
        self.save(update_fields=["status"])

        self.order.mark_paid()

    @transaction.atomic
    def mark_failed(self):
        if self.status != self.Status.PENDING:
            return

        self.status = self.Status.FAILED
        self.save(update_fields=["status"])

        self.order.cancel()