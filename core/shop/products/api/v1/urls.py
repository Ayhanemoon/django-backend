from rest_framework.routers import DefaultRouter
from django.urls import path, include
from .views import ProductViewSet

app_name = "api-v1"

router = DefaultRouter()
router.register(r"products", ProductViewSet, basename="product")

urlpatterns = [
    path("", include(router.urls)),
]
