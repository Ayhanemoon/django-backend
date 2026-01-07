from rest_framework.routers import DefaultRouter
from .views import OrderViewSet

app_name = "api-v1"

router = DefaultRouter()
router.register("order", OrderViewSet, basename="order")

urlpatterns = router.urls
