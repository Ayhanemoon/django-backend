from django.db import models, transaction
from accounts.models import Profile
from shop.products.models import Inventory


class Order(models.Model):
    """Model representing a customer's order."""

    class Status:
        """Enumeration of possible order statuses."""

        PENDING = "pending", "Pending"
        PROCESSING = "processing", "Processing"
        SHIPPED = "shipped", "Shipped"
        DELIVERED = "delivered", "Delivered"
        CANCELED = "canceled", "Canceled"

        choices = [
            PENDING,
            PROCESSING,
            SHIPPED,
            DELIVERED,
            CANCELED,
        ]

    profile = models.ForeignKey(
        Profile, on_delete=models.CASCADE, related_name="orders"
    )

    address_snapshot = models.JSONField(
        help_text="Immutable snapshot of the address at the time of order placement",
        null=True,
        blank=True,
    )
    status = models.CharField(max_length=50, choices=Status.choices, default=Status.PENDING)
    total_amount = models.PositiveIntegerField(default=0)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["-created_at"]
        indexes = [
            models.Index(fields=["profile"]),
            models.Index(fields=["status"]),
            models.Index(fields=["created_at"]),
        ]

    def __str__(self):
        return f"Order #{self.id} - {self.profile.user.email}"
    
    def cancel(self):
        if self.status == "cancelled":
            return

        with transaction.atomic():
            for item in self.items.select_related("product"):
                inventory = Inventory.objects.select_for_update().get(
                    product_id=item.product_id
                )

                inventory.reserved -= item.quantity
                inventory.save(update_fields=["reserved"])

            self.status = "cancelled"
            self.save(update_fields=["status"])
    
    def mark_paid(self):

        if self.status == "paid":
            return

        with transaction.atomic():
            for item in self.items.all():
                inventory = Inventory.objects.select_for_update().get(
                    product_id=item.product_id
                )

                # finalize reservation → actual stock deduction
                inventory.stock -= item.quantity
                inventory.reserved -= item.quantity
                inventory.save(update_fields=["stock", "reserved"])

            self.status = "paid"
            self.save(update_fields=["status"])
