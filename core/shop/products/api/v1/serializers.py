from rest_framework import serializers
from shop.products.models import Product, category, ProductImage, Inventory, InventoryMovement

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

class InventorySerializer(serializers.ModelSerializer):
    available_stock = serializers.IntegerField(read_only=True)

    class Meta:
        model = Inventory
        fields = [
            "id",
            "product",
            "stock",
            "reserved",
            "available_stock",
            "created_at",
            "updated_at",
        ]
        read_only_fields = fields

class InventoryMovementSerializer(serializers.ModelSerializer):

    class Meta:
        model = InventoryMovement
        fields = "__all__"
        read_only_fields = fields

class RestockSerializer(serializers.Serializer):
    quantity = serializers.IntegerField(min_value=1)
    note = serializers.CharField(
        required=False,
        allow_blank=True,
    )