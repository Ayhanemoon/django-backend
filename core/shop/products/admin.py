from django.contrib import admin
from shop.products.models import Product, Category, ProductImage, Inventory, Coupon, CouponUsage

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ["name", "slug", "parent"]
    search_fields = ["name", "slug"]
    prepopulated_fields = {"slug": ("name",)}

class ProductImageInline(admin.TabularInline):
    model = ProductImage
    extra = 1

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ["title", "price", "status", "category"]
    list_filter = ["status", "category"]
    search_fields = ["title", "slug"]
    prepopulated_fields = {"slug": ("title",)}
    inlines = [ProductImageInline]

admin.site.register(ProductImage)

@admin.register(Inventory)
class InventoryAdmin(admin.ModelAdmin):
    list_display = ["product", "stock", "reserved"]
    search_fields = ["product__title"]

admin.site.register(Coupon)

admin.site.register(CouponUsage)