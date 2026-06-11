from django.urls import path, include

urlpatterns = [
    path("orders/", include("shop.orders.api.v1.urls")),
    path("products/", include("shop.products.api.v1.urls")),
    path("cart/", include("shop.cart.api.v1.urls")),
]