from rest_framework.routers import DefaultRouter
from django.urls import path, include
from shop.orders.views import OrderViewSet

app_name = "api-v1"

router = DefaultRouter()
router.register(r"orders", OrderViewSet, basename="order")

urlpatterns = [
    path("", include(router.urls)),
]
