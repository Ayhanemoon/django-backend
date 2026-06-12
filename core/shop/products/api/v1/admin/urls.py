from rest_framework.routers import DefaultRouter
from .views import AdminInventoryViewSet

app_name = "product-admin-api-v1"

router = DefaultRouter()
router.register(r"", AdminInventoryViewSet, basename="admin-inventory")

urlpatterns = router.urls