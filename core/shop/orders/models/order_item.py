from django.db import models


class OrderItem(models.Model):
    order = models.ForeignKey(
        "orders.Order",
        related_name="items",
        on_delete=models.CASCADE,
    )

    product_id = models.PositiveIntegerField()
    product_title = models.CharField(max_length=255)

    unit_price = models.PositiveIntegerField()
    quantity = models.PositiveIntegerField()
    line_total = models.PositiveIntegerField()

    def save(self, *args, **kwargs):
        self.line_total = self.unit_price * self.quantity
        super().save(*args, **kwargs)

    def __str__(self):
        return f"OrderItem #{self.id} - {self.product_title} (x{self.quantity})"
