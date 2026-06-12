from django.urls import path, include

urlpatterns = [
    path("orders/", include("shop.orders.api.v1.admin.urls")),
    path("products/", include("shop.products.api.v1.admin.urls")),
]