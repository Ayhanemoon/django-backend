from django.db import models
from shop.products.models import Product

class InventoryMovement(models.Model):

    class Type(models.TextChoices):
        RESERVE = "reserve", "Reserve"
        RELEASE = "release", "Release"
        DEDUCT = "deduct", "Deduct"
        RESTOCK = "restock", "Restock"

    product = models.ForeignKey(
        Product,
        on_delete=models.CASCADE,
        related_name="inventory_movements",
    )

    movement_type = models.CharField(
        max_length=20,
        choices=Type.choices,
    )

    quantity = models.PositiveIntegerField()

    order_id = models.PositiveIntegerField(
        null=True,
        blank=True,
    )

    note = models.CharField(
        max_length=255,
        blank=True,
        null=True,
    )

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ["-created_at"]

        indexes = [
        models.Index(fields=["product"]),
        models.Index(fields=["movement_type"]),
        models.Index(fields=["created_at"]),
    ]

    def __str__(self):
        return (
            f"{self.product.title} | "
            f"{self.movement_type} | "
            f"{self.quantity}"
        )