from django.db import models

class Product(models.Model):
    class ProductStatus(models.TextChoices):
        Draft = "draft", "Draft"
        ACTIVE = "active", "Active"
        ARCHIVED = "archived", "Archived"

    title = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)
    price = models.PositiveIntegerField(default=0)  # store in smallest currency unit
    slug = models.SlugField(max_length=255, unique=True)
    status = models.CharField(
        max_length=20,
        choices=ProductStatus.choices,
        default=ProductStatus.Draft,
    )
    category = models.ForeignKey(
        "products.Category",
        on_delete=models.PROTECT,
        null=True,
        blank=True,
        related_name="products",
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["title"]

        indexes = [
            models.Index(fields=["status"]),
            models.Index(fields=["category"]),
            models.Index(fields=["price"]),
            models.Index(fields=["slug"]),
        ]

    def __str__(self):
        return self.title
