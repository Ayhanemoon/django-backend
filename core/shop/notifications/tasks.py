from celery import shared_task
from django.core.mail import send_mail
from django.conf import settings

@shared_task
def send_order_created_email(order_id):
    from shop.orders.models import Order
    order = Order.objects.select_related(
        "profile__user"
    ).get(id=order_id)

    send_mail(
        subject=f"Order #{order.id} Created",
        message="Your order has been received.",
        from_email= settings.DEFAULT_FROM_EMAIL,
        recipient_list=[
            order.profile.user.email
        ],
    )

@shared_task
def send_payment_success_email(order_id):
    from shop.orders.models import Order
    order = Order.objects.select_related(
        "profile__user"
    ).get(id=order_id)

    send_mail(
        subject=f"Order #{order.id} Payment Successful",
        message="Your payment has been processed successfully.",
        from_email= settings.DEFAULT_FROM_EMAIL,
        recipient_list=[
            order.profile.user.email
        ],
    )


@shared_task
def send_order_shipped_email(order_id):
    from shop.orders.models import Order
    order = Order.objects.select_related(
        "profile__user"
    ).get(id=order_id)

    send_mail(
        subject=f"Order #{order.id} Shipped",
        message="Your order has been shipped.",
        from_email= settings.DEFAULT_FROM_EMAIL,
        recipient_list=[
            order.profile.user.email
        ],
    )


@shared_task
def send_low_stock_alert(product_id):
    send_mail(
        subject=f"Low Stock Alert for Product ID {product_id}",
        message=f"The stock for product ID {product_id} is low.",
        from_email= settings.DEFAULT_FROM_EMAIL,
        recipient_list=[
            settings.LOW_STOCK_ALERT_EMAIL
        ]
    )