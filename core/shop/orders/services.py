from django.db import transaction

from rest_framework.exceptions import ValidationError

from shop.cart.models import Cart
from shop.orders.models import Order, OrderItem
from shop.orders.models import CheckoutRequestLog
from shop.products.models import Inventory, Coupon

from shop.notifications.services import NotificationService

from accounts.models import Address


class CheckoutService:

    @staticmethod
    @transaction.atomic
    def checkout(
        *,
        profile,
        address_id,
        idempotency_key,
        coupon_code=None,
    ):

        # ----------------------------
        # 1. Idempotency protection
        # ----------------------------
        if CheckoutRequestLog.objects.filter(
            key=idempotency_key,
            profile=profile,
        ).exists():

            raise ValidationError(
                "Duplicate checkout request."
            )


        # ----------------------------
        # 2. Lock cart
        # ----------------------------
        cart = (
            Cart.objects
            .select_for_update()
            .prefetch_related(
                "items__product"
            )
            .get(profile=profile)
        )


        items = list(
            cart.items.select_related(
                "product"
            )
        )


        if not items:
            raise ValidationError(
                "Cart is empty."
            )


        # ----------------------------
        # 3. Validate Address
        # ----------------------------
        address = Address.objects.alive().get(
            id=address_id,
            profile=profile,
        )


        # ----------------------------
        # 4. Inventory validation
        # ----------------------------
        for item in items:

            inventory = (
                Inventory.objects
                .select_for_update()
                .get(
                    product=item.product
                )
            )

            if (
                inventory.available_stock()
                <
                item.quantity
            ):
                raise ValidationError(
                    f"Not enough stock for {item.product.title}"
                )


        # ----------------------------
        # 5. Calculate subtotal
        # ----------------------------
        subtotal = sum(
            item.product.price * item.quantity
            for item in items
        )


        discount_amount = 0
        coupon = None


        # ----------------------------
        # 6. Coupon
        # ----------------------------
        if coupon_code:

            try:
                coupon = Coupon.objects.get(
                    code=coupon_code
                )

            except Coupon.DoesNotExist:
                raise ValidationError(
                    "Invalid coupon."
                )


            if not coupon.is_valid():
                raise ValidationError(
                    "Coupon is not valid."
                )


            if subtotal < coupon.min_order_amount:
                raise ValidationError(
                    "Minimum order amount not reached."
                )


            discount_amount = (
                coupon.calculate_discount(
                    subtotal
                )
            )


        # ----------------------------
        # 7. Address Snapshot
        # ----------------------------
        snapshot = {
            "receiver_name": address.receiver_name,
            "phone_number": address.phone_number,
            "country": address.country,
            "state": address.state,
            "city": address.city,
            "postal_code": address.postal_code,
            "address_line_1": address.address_line_1,
            "address_line_2": address.address_line_2,
        }
        
        final_total = subtotal - discount_amount

        # ----------------------------
        # 8. Create order
        # ----------------------------
        order = Order.objects.create(
            profile=profile,
            address_snapshot=snapshot,
            total_amount=final_total,
            coupon_code=(
                coupon.code
                if coupon
                else None
            ),
            discount_amount=discount_amount,
        )


        # ----------------------------
        # 9. Reserve stock + items
        # ----------------------------
        for item in items:

            inventory = (
                Inventory.objects
                .select_for_update()
                .get(
                    product=item.product
                )
            )


            inventory.reserve(
                quantity=item.quantity,
                order_id=order.id,
            )


            OrderItem.objects.create(
                order=order,
                product_id=item.product.id,
                product_title=item.product.title,
                unit_price=item.product.price,
                quantity=item.quantity,
            )


        # ----------------------------
        # 10. Clear cart
        # ----------------------------
        cart.items.all().delete()


        # ----------------------------
        # 11. Store idempotency
        # ----------------------------
        CheckoutRequestLog.objects.create(
            key=idempotency_key,
            profile=profile,
        )


        NotificationService.order_created(
            order
        )


        return order