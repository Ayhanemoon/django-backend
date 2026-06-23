from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import (
    SearchFilter,
    OrderingFilter,
)
from shop.products.api.v1.filters import ProductFilter
from shop.products.api.v1.paginations import StandardPagination
from shop.products.models import Product, Category
from ..serializers import (
    ProductSerializer, 
    CategorySerializer,
)

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
    
    filter_backends = [
        DjangoFilterBackend,
        SearchFilter,
        OrderingFilter,
    ]

    filterset_class = ProductFilter

    search_fields = [
        "title",
        "description",
        "slug",
    ]

    ordering_fields = [
        "price",
        "created_at",
        "title",
    ]

    ordering = [
        "-created_at",
    ]

    pagination_class = StandardPagination


class CategoryViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Category.objects.all().select_related("parent")
    serializer_class = CategorySerializer
    permission_classes = [IsAuthenticated]
