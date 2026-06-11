from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from shop.cart.models import Cart, CartItem
from .serializers import CartSerializer, CartItemSerializer,CartItemCreateUpdateSerializer
from rest_framework.decorators import action
from rest_framework.response import Response

class CartViewSet(viewsets.ModelViewSet):
    serializer_class = CartSerializer
    permission_classes = [IsAuthenticated]
    
    def get_cart(self, request):
        cart, _ = Cart.objects.get_or_create(profile=request.user.profile)
        return cart

    def list(self, request):
        cart = self.get_cart(request)
        return Response(CartSerializer(cart).data)
    
    @action(detail=False, methods=["post"])
    def add_item(self, request):
        cart = self.get_cart(request)

        serializer = CartItemCreateUpdateSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        product = serializer.validated_data["product"]
        quantity = serializer.validated_data["quantity"]

        item, created = CartItem.objects.get_or_create(
            cart=cart,
            product=product,
            defaults={"quantity": quantity},
        )

        if not created:
            item.quantity += quantity
            item.save(update_fields=["quantity"])

        return Response(CartSerializer(cart).data)
    
    @action(detail=True, methods=["patch"])
    def update_item(self, request, pk=None):
        item = CartItem.objects.get(id=pk, cart__profile=request.user.profile)

        quantity = request.data.get("quantity")
        item.quantity = quantity
        item.save(update_fields=["quantity"])

        return Response({"detail": "updated"})
    
    @action(detail=True, methods=["delete"])
    def remove_item(self, request, pk=None):
        item = CartItem.objects.get(id=pk, cart__profile=request.user.profile)
        item.delete()

        return Response({"detail": "deleted"})