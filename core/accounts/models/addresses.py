from django.db import models
from django.db.models import Q


class Address(models.Model):
    profile = models.ForeignKey(
        "accounts.Profile",
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
            models.Index(fields=["profile", "is_default"]),
        ]
        constraints = [
            models.UniqueConstraint(
                fields=["profile"],
                condition=Q(is_default=True),
                name="unique_default_address_per_profile",
            )
        ]

    def __str__(self):
        return f"{self.title} - {self.profile.user.email}"

    def save(self, *args, **kwargs):
        if self.is_default:
            Address.objects.filter(
                profile=self.profile,
                is_default=True,
            ).exclude(pk=self.pk).update(is_default=False)

        super().save(*args, **kwargs)
