from rest_framework import serializers
from shop.products.models import Product, category, ProductImage

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = category
        fields = ["id", "name", "slug", "parent"]
        read_only_fields = ["id"]
        ref_name = "BlogCategorySerializer"

class ProductImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductImage
        fields = ["id", "image", "alt_text", "is_primary", "created_at"]
        read_only_fields = ["id", "created_at"]

class ProductSerializer(serializers.ModelSerializer):
    images = ProductImageSerializer(many=True, read_only=True)
    category = CategorySerializer(read_only=True)
    class Meta:
        model = Product
        fields = [
            "id",
            "title",
            "slug",
            "description",
            "price",
            "status",
            "category",
            "images",
            "created_at",
            "updated_at",
        ]
        read_only_fields = ["id", "created_at", "updated_at"]
