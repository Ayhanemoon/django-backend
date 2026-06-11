from django.db import models,transaction
from shop.orders.models import Order
from shop.products.models import Inventory

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
    
    def mark_success(self):
        if self.status != "pending":
            return

        self.status = "success"
        self.save(update_fields=["status"])

        self.order.mark_paid()

    def mark_failed(self):

        if self.status != "pending":
            return

        with transaction.atomic():
            for item in self.order.items.all():
                inventory = Inventory.objects.select_for_update().get(
                    product_id=item.product_id
                )

                inventory.reserved -= item.quantity
                inventory.save(update_fields=["reserved"])

            self.status = "failed"
            self.save(update_fields=["status"])

            self.order.status = "cancelled"
            self.order.save(update_fields=["status"])