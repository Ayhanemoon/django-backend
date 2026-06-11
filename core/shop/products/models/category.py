from django.db import models

class Category(models.Model):
    name = models.CharField(max_length=100)
    slug = models.SlugField(unique=True)

    parent = models.ForeignKey(
        "self",
        null=True,
        blank=True,
        on_delete=models.CASCADE,
        related_name="children",
    )

    class Meta:
        verbose_name_plural = "Categories"
        ordering = ["name"]
    
    def __str__(self):
        return self.name