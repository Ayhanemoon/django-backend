from rest_framework.routers import DefaultRouter
from django.urls import path, include
from .views import ProductViewSet,CategoryViewSet

app_name = "product-api-v1"

router = DefaultRouter()
router.register(r"", ProductViewSet, basename="product")
router.register(r"categories", CategoryViewSet, basename="category")

urlpatterns = [
    path("", include(router.urls)),
]
