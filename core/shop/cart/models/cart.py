from django.db import models
from accounts.models import Profile

class Cart(models.Model):
    profile = models.OneToOneField(
        Profile,
        on_delete=models.CASCADE,
        related_name="cart",
    )

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


