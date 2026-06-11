from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from shop.products.models import Product, Category
from .serializers import ProductSerializer, CategorySerializer


class ProductViewSet(viewsets.ModelViewSet):
    serializer_class = ProductSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        queryset = Product.objects.filter(
            status=Product.ProductStatus.ACTIVE
        ).select_related("category").prefetch_related("images")

        category_slug = self.request.query_params.get("category")
        if category_slug:
            queryset = queryset.filter(category__slug=category_slug)

        return queryset


class CategoryViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Category.objects.all().select_related("parent")
    serializer_class = CategorySerializer
    permission_classes = [IsAuthenticated]