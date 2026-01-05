from django.conf import settings
from django.db import models


class Address(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="addresses",
    )

    title = models.CharField(
        max_length=100,
        help_text="e.g. Home, Office",
    )

    receiver_name = models.CharField(max_length=255)

    phone_number = models.CharField(max_length=20)

    country = models.CharField(max_length=100, default="Iran")
    state = models.CharField(max_length=100)
    city = models.CharField(max_length=100)
    postal_code = models.CharField(max_length=20)

    address_line_1 = models.CharField(max_length=255)
    address_line_2 = models.CharField(
        max_length=255,
        blank=True,
        null=True,
    )

    is_default = models.BooleanField(default=False)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["-is_default", "-created_at"]
        indexes = [
            models.Index(fields=["user", "is_default"]),
        ]

    def __str__(self):
        return f"{self.title} - {self.user.email}"

    def save(self, *args, **kwargs):
        if self.is_default:
            Address.objects.filter(
                user=self.user,
                is_default=True,
            ).exclude(pk=self.pk).update(is_default=False)

        super().save(*args, **kwargs)
