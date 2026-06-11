from django.db import models
from shop.orders.models import Order


class OrderItem(models.Model):
    order = models.ForeignKey(
        Order,
        on_delete=models.CASCADE,
        related_name="items",
    )

    product_id = models.PositiveIntegerField(
        help_text="Product ID at time of order",
    )

    product_title = models.CharField(
        max_length=255,
        help_text="Snapshot of product title",
    )

    unit_price = models.PositiveIntegerField(
        help_text="Snapshot price per unit at order time",
    )

    quantity = models.PositiveIntegerField()

    line_total = models.PositiveIntegerField(
        help_text="unit_price * quantity",
    )

    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["id"]
        indexes = [
            models.Index(fields=["order"]),
            models.Index(fields=["product_id"]),
        ]

    def __str__(self):
        return f"{self.product_title} x {self.quantity}"

    def save(self, *args, **kwargs):
        # Enforce immutability
        if self.pk:
            raise ValueError("Order items cannot be modified once created")

        self.line_total = self.unit_price * self.quantity
        super().save(*args, **kwargs)
