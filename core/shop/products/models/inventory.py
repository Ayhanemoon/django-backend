from django.db import models
from shop.products.models import Product


class Inventory(models.Model):
    product = models.OneToOneField(
        Product,
        on_delete=models.CASCADE,
        related_name="inventory",
    )

    stock = models.PositiveIntegerField(default=0)

    reserved = models.PositiveIntegerField(default=0)

    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        indexes = [
            models.Index(fields=["product"]),
        ]

    def available_stock(self):
        return self.stock - self.reserved

    def __str__(self):
        return f"{self.product.title} stock"