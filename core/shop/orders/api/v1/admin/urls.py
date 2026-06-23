from rest_framework.routers import DefaultRouter
from .views import AdminOrderViewSet

app_name = "orders-admin-api-v1"

router = DefaultRouter()
router.register(r"", AdminOrderViewSet, basename="admin-orders")

urlpatterns = router.urls