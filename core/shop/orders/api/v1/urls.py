from rest_framework.routers import DefaultRouter
from .views import OrderViewSet

app_name = "order-api-v1"

router = DefaultRouter()
router.register("", OrderViewSet, basename="order")

urlpatterns = router.urls
