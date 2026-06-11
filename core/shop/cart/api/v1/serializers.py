from rest_framework import serializers
from shop.cart.models import Cart, CartItem

class CartItemSerializer(serializers.ModelSerializer):
    product_title = serializers.CharField(source="product.title", read_only=True)
    price = serializers.IntegerField(source="product.price", read_only=True)

    class Meta:
        model = CartItem
        fields = ["id", "product", "product_title", "price", "quantity"]

class CartSerializer(serializers.ModelSerializer):
    items = CartItemSerializer(many=True, read_only=True)

    class Meta:
        model = Cart
        fields = ["id", "items"]

class CartItemCreateUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = CartItem
        fields = ["product", "quantity"]