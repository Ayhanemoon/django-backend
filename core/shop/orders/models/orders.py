from django.db import models, transaction
from rest_framework.exceptions import ValidationError
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
        CANCELLED = "cancelled", "Cancelled"

        choices = [
            PENDING,
            PROCESSING,
            SHIPPED,
            DELIVERED,
            CANCELLED,
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
    coupon_code = models.CharField(
        max_length=50,
        null=True,
        blank=True,
    )

    discount_amount = models.PositiveIntegerField(
        default=0,
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
    
    def cancel(self):
        if self.status == self.Status.CANCELLED:
            return

        with transaction.atomic():
            for item in self.items.select_related("product"):
                inventory = Inventory.objects.select_for_update().get(
                    product_id=item.product_id
                )

                inventory.release(
                    quantity=item.quantity,
                    order_id=self.id,
                )

            self.status = self.Status.CANCELLED
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
                inventory.deduct(
                    quantity=item.quantity,
                    order_id=self.id,
                )

            self.status = "paid"
            self.save(update_fields=["status"])

    def mark_shipped(self):
        if self.status != self.Status.PROCESSING:
            raise ValidationError("Only processing orders can be shipped.")

        self.status = self.Status.SHIPPED
        self.save(update_fields=["status"])


    def mark_delivered(self):
        if self.status != self.Status.SHIPPED:
            raise ValidationError("Only shipped orders can be delivered.")

        self.status = self.Status.DELIVERED
        self.save(update_fields=["status"])    

class CheckoutRequestLog(models.Model):
    key = models.CharField(max_length=255, unique=True)
    profile = models.ForeignKey(Profile, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)