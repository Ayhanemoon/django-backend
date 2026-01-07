from django.db import models
from accounts.models import Profile


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

    profile = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name="orders")

    address_snapshot = models.JSONField(
        help_text="Immutable snapshot of the address at the time of order placement",
        null=True,
        blank=True,
    )
    status = models.CharField(
        max_length=50,
        choices=Status.choices,
        default="pending"
    )
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
