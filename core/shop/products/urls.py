from django.urls import path, include

app_name = "products"

urlpatterns = [
    path("api/v1/", include("shop.products.api.v1.urls")),
]