from django.db import transaction
from django.conf import settings
from rest_framework.exceptions import ValidationError
from shop.notifications.services import NotificationService

from shop.products.models import (
    Inventory,
    InventoryMovement,
)

class InventoryService:

    @staticmethod
    @transaction.atomic
    def reserve(
        *,
        product,
        quantity,
        order_id=None,
    ):

        inventory = (
            Inventory.objects
            .select_for_update()
            .get(product=product)
        )

        if inventory.available_stock() < quantity:
            raise ValidationError(
                f"Not enough stock for {product.title}"
            )

        inventory.reserved += quantity

        inventory.save(
            update_fields=[
                "reserved"
            ]
        )

        InventoryMovement.objects.create(
            product=inventory.product,
            movement_type=(
                InventoryMovement.Type.RESERVE
            ),
            quantity=quantity,
            order_id=order_id,
        )

        return inventory


    @staticmethod
    @transaction.atomic
    def release(
        *,
        product_id,
        quantity,
        order_id=None,
    ):

        inventory = (
            Inventory.objects
            .select_for_update()
            .get(
                product_id=product_id
            )
        )

        inventory.reserved -= quantity

        inventory.save(
            update_fields=[
                "reserved"
            ]
        )


        InventoryMovement.objects.create(
            product=inventory.product,
            movement_type=(
                InventoryMovement.Type.RELEASE
            ),
            quantity=quantity,
            order_id=order_id,
        )

        return inventory


    @staticmethod
    @transaction.atomic
    def deduct(
        *,
        product_id,
        quantity,
        order_id=None,
    ):

        inventory = (
            Inventory.objects
            .select_for_update()
            .get(
                product_id=product_id
            )
        )

        if inventory.stock < quantity:
            raise ValidationError(
                "Insufficient stock."
            )


        inventory.stock -= quantity
        inventory.reserved -= quantity


        inventory.save(
            update_fields=[
                "stock",
                "reserved",
            ]
        )


        InventoryMovement.objects.create(
            product=inventory.product,
            movement_type=(
                InventoryMovement.Type.SALE
            ),
            quantity=quantity,
            order_id=order_id,
        )

        if inventory.available_stock <= settings.LOW_STOCK_THRESHOLD:
            NotificationService.low_stock(inventory.product)
        return inventory