from rest_framework.routers import DefaultRouter
from .views import AdminInventoryViewSet, AdminCouponViewSet

app_name = "product-admin-api-v1"

router = DefaultRouter()
router.register(r"", AdminInventoryViewSet, basename="admin-inventory")
router.register(
    "coupons",
    AdminCouponViewSet,
    basename="admin-coupons",
)

urlpatterns = router.urls

