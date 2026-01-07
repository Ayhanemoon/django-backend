from django.contrib import admin
from .models import Order


class OrderAdmin(admin.ModelAdmin):
    list_display = ("id", "profile", "created_at", "updated_at")
    list_filter = ("created_at", "updated_at")
    search_fields = ("profile__user__email",)


admin.site.register(Order, OrderAdmin)
