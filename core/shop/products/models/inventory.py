from django.db import models
from django.conf import settings
from shop.notifications.services import NotificationService
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
    
    def reserve(self, quantity, order_id=None):
        from .inventory_movement import InventoryMovement

        if self.available_stock < quantity:
            raise ValueError("Insufficient stock")

        self.reserved += quantity
        self.save(update_fields=["reserved"])

        InventoryMovement.objects.create(
            product=self.product,
            movement_type=InventoryMovement.Type.RESERVE,
            quantity=quantity,
            order_id=order_id,
        )

    def release(self, quantity, order_id=None):
        from .inventory_movement import InventoryMovement

        self.reserved = max(0, self.reserved - quantity)

        self.save(update_fields=["reserved"])

        InventoryMovement.objects.create(
            product=self.product,
            movement_type=InventoryMovement.Type.RELEASE,
            quantity=quantity,
            order_id=order_id,
        )

    def deduct(self, quantity, order_id=None):
        from .inventory_movement import InventoryMovement
        if self.stock < quantity:
            raise ValueError("Insufficient stock")

        self.stock -= quantity
        self.reserved = max(0, self.reserved - quantity)

        self.save(
            update_fields=[
                "stock",
                "reserved",
            ]
        )

        InventoryMovement.objects.create(
            product=self.product,
            movement_type=InventoryMovement.Type.DEDUCT,
            quantity=quantity,
            order_id=order_id,
        )
        
        if self.available_stock <= settings.LOW_STOCK_THRESHOLD:
            NotificationService.low_stock(self.product)

    def restock(self, quantity, note=None):
        from .inventory_movement import InventoryMovement
        
        self.stock += quantity

        self.save(update_fields=["stock"])

        InventoryMovement.objects.create(
            product=self.product,
            movement_type=InventoryMovement.Type.RESTOCK,
            quantity=quantity,
            note=note,
        )

    