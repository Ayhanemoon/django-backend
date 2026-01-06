from django.db import models
from accounts.models import Profile


class Order(models.Model):
    profile = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name="orders")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Order #{self.id} - {self.profile.user.email}"
