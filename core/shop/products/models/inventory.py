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

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        indexes = [
            models.Index(fields=["product"]),
        ]

    @property
    def available_stock(self):
        return self.stock - self.reserved

    def __str__(self):
        return f"{self.product.title} stock"

    def restock(self, quantity, note=None): 
        from shop.products.models import InventoryMovement       
        self.stock += quantity

        self.save(update_fields=["stock"])

        InventoryMovement.objects.create(
            product=self.product,
            movement_type=InventoryMovement.Type.RESTOCK,
            quantity=quantity,
            note=note,
        )

    