from django.urls import path, include

urlpatterns = [
    path("api/v1/", include("shop.orders.api.v1.urls")),
]
