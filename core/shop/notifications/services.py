from .tasks import (
    send_order_created_email,
    send_payment_success_email,
    send_order_shipped_email,
    send_low_stock_alert,
)


class NotificationService:

    @staticmethod
    def order_created(order):
        send_order_created_email.delay(order.id)

    @staticmethod
    def payment_success(order):
        send_payment_success_email.delay(order.id)

    @staticmethod
    def order_shipped(order):
        send_order_shipped_email.delay(order.id)

    @staticmethod
    def low_stock(product):
        send_low_stock_alert.delay(product.id)